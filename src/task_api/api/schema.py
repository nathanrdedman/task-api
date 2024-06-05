# pylint: disable=C0114,E0401,C0115,R0903
from typing import Union

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

    @field_validator("status", mode="before")
    @classmethod
    def serialize_status(cls, status) -> Union[str, None]:
        """We use a field validator here to check
        and return the value field of the Choice
        parameter for the status value.

        Args:
            status (Choice): Status choice object

        Returns:
            str: Choice value (Human readable)
        """
        if status:
            return status.value

        return None

    class ConfigDict:
        from_attributes = True


class User(BaseModel):
    id: int
    username: str
    email: str

    class ConfigDict:
        from_attributes = True


class UserCreate(BaseModel):
    password: str
    username: str
    email: str


class UserInDB(BaseModel):
    password: str
    username: str
    email: str
    hashed_password: str
