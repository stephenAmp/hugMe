from fastapi import FastAPI
import uvicorn

app=FastAPI()

@app.get('/')
def root():
    return 'Hi this is the beginning of the mental health app!'

if __name__ == '__main__':
    uvicorn.run(app)