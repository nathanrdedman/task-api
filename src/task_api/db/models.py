from typing import List

from sqlalchemy import Boolean, Column, ForeignKey, Integer, Sequence, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType, EmailType

from .connect import Base

# To make this more extensible,
# we could have added a table to hold
# these options allowing additional
# status options to be added, but
# we've opted for a constant set.
STATUS_OPTIONS = (
    ("pending", "Pending"),
    ("doing", "Doing"),
    ("blocked", "Blocked"),
    ("done", "Done"),
)

DEFAULT_STATUS = STATUS_OPTIONS[0][0]


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email: Column = Column(EmailType, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Task(Base):
    """Tasks table"""

    OPTIONS = STATUS_OPTIONS
    __tablename__ = "task"

    id = Column(Integer, Sequence("task_id_seq", start=1), primary_key=True)
    description = Column(String(1000))
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    status: Column = Column(
        ChoiceType(OPTIONS, impl=String(15)), default=DEFAULT_STATUS
    )


class DeletedTask(Base):
    OPTIONS = STATUS_OPTIONS
    __tablename__ = "task_deleted"

    id = Column(Integer, primary_key=True)
    description = Column(String(1000))
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    status: Column = Column(
        ChoiceType(OPTIONS, impl=String(15)), default=DEFAULT_STATUS
    )
