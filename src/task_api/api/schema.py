from typing import Optional, Union

from pydantic import (BaseModel, ConfigDict, Field, field_serializer,
                      field_validator)
from sqlalchemy_utils import Choice, ChoiceType, Country


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
    status: str
    id: int

    @field_validator("status", mode="before")
    @classmethod
    def serialize_status(cls, status):
        if status:
            return status.value

    class Config:
        from_attributes = True


class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    password: str
    username: str
    email: str


class UserInDB(User):
    id: int
    hashed_password: str
