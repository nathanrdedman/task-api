from typing import Union

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class TaskBase(BaseModel):
    description: str


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    class Config:
        from_attributes = True


class User(BaseModel):
    id: int
    username: str
    email: Union[str, None] = None

    class Config:
        from_attributes = True


class UserCreate(User):
    password: str


class UserInDB(User):
    id: int
    hashed_password: str
