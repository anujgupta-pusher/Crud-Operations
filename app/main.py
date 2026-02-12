from sqlite3 import IntegrityError
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db, Base
from app import model, structure
from app.database import engine, SessionLocal
from app.structure import UserCreate
from app.auth import get_current_user
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import app.auth as auth

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    








# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
@app.post("/register")
def register(user: structure.UserCreate, db: Session = Depends(get_db)):
    hashed = auth.hash_password(user.password)
    new_user = model.User(
        username=user.username,
        hashed_password=hashed
    )

    db.add(new_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()  
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    return {"message": "User created successfully"}

@app.post("/login")
def login(form_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

    
@app.post("/todos", response_model=structure.TodoResponse)
def create_todo(
    todo: structure.TodoCreate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user)
):
    new_todo = model.Todo(
        title=todo.title,
        user_id=current_user.id
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.get("/todos", response_model=List[structure.TodoResponse])
def get_todos(
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user)
):
    return db.query(model.Todo).filter(
        model.Todo.user_id == current_user.id
    ).all()

@app.delete("/todos", response_model=List[structure.TodoResponse])
def get_todos(
    db : Session = Depends(get_db),
    current_user : model.User = Depends(get_current_user)
):
    return db.query(model.Todo).filter(
        model.Todo.user_id == current_user.id
        ).all()

