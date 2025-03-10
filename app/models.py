from sqlalchemy import Integer,String
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(Integer, autoincrement= True, primary_key=True)
    name:Mapped[str] = mapped_column(String)
    email:Mapped[str] = mapped_column(String, unique=True)