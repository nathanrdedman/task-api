from typing import List

from sqlalchemy import Boolean, Column, ForeignKey, Integer, Sequence, String
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy_utils import ChoiceType, EmailType

from .connect import Base

STATUS_OPTIONS = (
    ("pending", "Pending"),
    ("doing", "Doing"),
    ("blocked", "Blocked"),
    ("done", "Done"),
)

DEFAULT_STATUS = STATUS_OPTIONS[0][0]


class Task(Base):
    STATUS_OPTIONS = STATUS_OPTIONS
    __tablename__ = "task"

    id = Column(Integer, Sequence("task_id_seq", start=1), primary_key=True)
    description = Column(String(1000))
    user_id = mapped_column(ForeignKey("user.id"))
    status: str = Column(
        ChoiceType(STATUS_OPTIONS, impl=String(15)), default=DEFAULT_STATUS
    )


class DeletedTask(Base):
    STATUS_OPTIONS = STATUS_OPTIONS
    __tablename__ = "task_deleted"

    id = Column(Integer, primary_key=True)
    description = Column(String(1000))
    user_id = mapped_column(ForeignKey("user.id"))
    status: str = Column(
        ChoiceType(STATUS_OPTIONS, impl=String(15)), default=DEFAULT_STATUS
    )


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(EmailType, unique=True)
    hashed_password = Column(String)
    # tasks = relationship("Task", back_populates="user_id")
