from fastapi import FastAPI,HTTPException,status,Depends
from db import get_db
from sqlalchemy.orm import Session
from schema import UserSchema,UserResponseSchema
from models import User
import uvicorn


app=FastAPI()

@app.get('/')
def root():
    return 'Hi this is the beginning of the mental health app!'

@app.post('/user', response_model=UserResponseSchema)
def create_user(user:UserSchema, db:Session =Depends(get_db)):
    user_data = user.model_dump()
    db_user = User(**user_data)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = f'failed to add user to db:{e}')
    return db_user



@app.get("/recommendations/{user_id}")
def get_recommendations(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_preferences = db.query(UserPreference).filter(UserPreference.user_id == user_id).first()

    payload = {
        "favorite_genres": user_preferences.favorite_genres,
        "favorite_actors": user_preferences.favorite_actors,
        "preferred_language": user_preferences.preferred_language
    }

    # Send user data to Gemini API
    response = requests.post(GEMINI_API_URL, json=payload)
    if response.status_code == 200:
        movie_data = response.json()
        
        # Save movies in database if not exists
        for movie in movie_data:
            existing_movie = db.query(Movie).filter(Movie.title == movie["title"]).first()
            if not existing_movie:
                new_movie = Movie(
                    title=movie["title"],
                    poster_url=movie.get("poster_url"),
                    description=movie.get("description"),
                    genres=movie.get("genres"),
                    release_date=movie.get("release_date"),
                )
                db.add(new_movie)
        db.commit()

        return movie_data
    return {"error": "Failed to fetch recommendations"}




if __name__ == '__main__':
    uvicorn.run(app)