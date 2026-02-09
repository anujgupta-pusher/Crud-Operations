

from pydantic import BaseModel, ConfigDict

class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool

    
    model_config = ConfigDict(from_attributes=True)


class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        orm_mode = True  # Allows SQLAlchemy model to be returned directly


class TodoCreate(BaseModel):
    title: str

class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        orm_mode = True
        
class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
