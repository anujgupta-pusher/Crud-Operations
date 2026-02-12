from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#DATABASE_URL = "postgresql://postgres:operation@localhost/todo_db"DATABASE_URL = "postgresql://postgres:newpassword@localhost:5432/todo_db"
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/todo_db"
from dotenv import load_dotenv
# app/database.py
# REMOVE THIS: from tests.test_todos import DATABASE_URL 
from app.config import DATABASE_URL

# ... rest of your SQLAlchemy/database setup
# from tests.test_todos import DATABASE_URL
load_dotenv()

import os



SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://myuser:mypassword@localhost:5432/todo_db"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

