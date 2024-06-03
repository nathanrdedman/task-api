from typing import Union

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class TaskBase(BaseModel):
    id: int
    description: str
    status: str
    user: str


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    class Config:
        from_attributes = True


# class UserBase(BaseModel):
#     id: int
#     username: str
#     email: str

class User(BaseModel):
    id
    username: str
    email: Union[str, None] = None    
    
    class Config:
        from_attributes = True

class UserCreate(User):
    password: str


# class User(UserBase):
#     id: int
#     tasks: list[Task] = []

#     class Config:
#         orm_mode = True


class UserInDB(User):
    hashed_password: str
