# pylint: disable=E0401,C0115,R0903
"""ORM model definitions"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import ChoiceType, EmailType

Base = declarative_base()

# To make this more extensible,
# we could have added a table to hold
# these options allowing additional
# status options to be added, but
# we've opted for a constant set via
# nested tuples
STATUS_OPTIONS = (
    ("pending", "Pending"),
    ("doing", "Doing"),
    ("blocked", "Blocked"),
    ("done", "Done"),
)

DEFAULT_STATUS = STATUS_OPTIONS[0][0]


class SerialisableBase(Base):  # type: ignore
    __abstract__ = True

    def to_dict(self) -> dict:
        """Method to serialise a row object to dict
        which is preferable to the dunder method
        __dict__ which yields a dictionary containing
        unwated fields.

        Returns:
            dict: Dict of key:values from row object
        """
        return {field.name: getattr(self, field.name) for field in self.__table__.c}


class User(Base):  # type: ignore
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email: Column = Column(EmailType, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Task(SerialisableBase):
    """Tasks table"""

    OPTIONS = STATUS_OPTIONS
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(1000))
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    status: Column = Column(
        ChoiceType(OPTIONS, impl=String(15)), default=DEFAULT_STATUS
    )


class DeletedTask(SerialisableBase):  # type: ignore
    OPTIONS = STATUS_OPTIONS
    __tablename__ = "task_deleted"

    id = Column(Integer, primary_key=True)
    description = Column(String(1000))
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), primary_key=True)
    status: Column = Column(
        ChoiceType(OPTIONS, impl=String(15)), default=DEFAULT_STATUS
    )
