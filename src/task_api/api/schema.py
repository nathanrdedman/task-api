from typing import Optional, Union

from pydantic import BaseModel, field_validator


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

    # We use a field validator here to check
    # and return the value field of the Choice
    # parameter for the status value.
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
