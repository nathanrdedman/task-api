from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from .connect import Base

STATUS_OPTIONS = (
    ("pending", "Pending"),
    ("doing", "Doing"),
    ("blocked", "Blocked"),
    ("done", "Done"),
)

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    description = Column(String)
    status = relationship("Status", back_populates="status")
    user = relationship("User", back_populates="user")


class DeletedTask(Task):
    __tablename__ = "task_deleted"
    deleted_id = Column(Integer, primary_key=True)
    active_id = Column(Integer, ForeignKey("task.id"))


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True)
    status = ChoiceType(STATUS_OPTIONS, impl=String(length=10))

#
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)
