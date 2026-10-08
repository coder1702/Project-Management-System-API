import os

from dotenv import load_dotenv
from sqlalchemy import create_engine,text
from sqlalchemy.orm import DeclarativeBase,sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(
    DATABASE_URL,
    echo=True   #echo = True is written for logging in database 
    )

SessionLocal = sessionmaker(     #Helps python to generate changes in database
    autocommit=False,            #So that sessionmaker does not automatically change anything 
    autoflush=False,             #Controls whether SQLAlchemy automatically sends pending changes to the database before certain queries
    bind=engine                  #To use engine 
)


class Base(DeclarativeBase):     #DeclarativeBase is use to create Base class and the class that inherits base is recognized as database 
    pass

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
