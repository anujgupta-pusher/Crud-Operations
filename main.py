from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import model, structure
from database import engine, SessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import extraction
from extraction import oauth2_scheme # Import from your extraction file

app = FastAPI()







oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/register")
def register(user: structure.UserCreate, db: Session = Depends(get_db)):
    hashed = extraction.hash_password(user.password)
    new_user = model.User(username=user.username, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    return {"message": "User created"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.username == form_data.username).first()
    if not user or not extraction.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = extraction.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

model.Base.metadata.create_all(bind=engine)





@app.post("/todos", response_model=structure.TodoResponse)
def create_todo(todo: structure.TodoCreate, db: Session = Depends(get_db)):
    new_todo = model.Todo(title=todo.title)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@app.get("/todos", response_model=List[structure.TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(model.Todo).all()
    return todos


@app.put("/todos/{todo_id}", response_model=structure.TodoResponse)
def update_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(model.Todo).filter(model.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.completed = True
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(model.Todo).filter(model.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted"}



def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    username = extraction.decode_access_token(token)
    user = db.query(model.User).filter(model.User.username == username).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
    
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

