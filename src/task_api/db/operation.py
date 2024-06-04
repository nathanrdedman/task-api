from typing import Union

from sqlalchemy.orm import Session

from ..api import schema
from ..auth.utils import hash_password
from . import models


def get_user(db: Session, user_id: int) -> Union[models.User, None]:
    """Get the user object by user id

    Args:
        db (Session): Database session
        user_id (int): User id

    Returns:
        Union[models.User, None]: User object or None
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db, username: str) -> Union[models.User, None]:
    """Get the user object by username

    Args:
        db (_type_): Database session
        username (str): Username

    Returns:
        Union[models.User, None]: User object or None
    """
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Union[models.User, None]:
    """_summary_

    Args:
        db (Session): Database session
        email (str): Email address

    Returns:
        Union[models.User, None]: User object or None
    """
    return db.query(models.User).filter(models.User.email == email).first()


def new_user(db: Session, user: schema.UserCreate):
    hashpassword = hash_password(user.password)
    db_user = models.User(
        email=user.email, hashed_password=hashpassword, username=user.username
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def read_task(db: Session, task_id: int, user_id: int):
    return (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .filter(models.Task.user_id == user_id)
        .one()
    )


def read_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Task)
        .filter(models.Task.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def write_task(db: Session, description: str, user_id: int):
    task = models.Task(description=description, user_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def archive_task(db: Session, task_id: int, user_id: int):
    task = read_task(db=db, task_id=task_id, user_id=user_id)
    deleted_task = models.DeletedTask(**task.dict())
    db.add(deleted_task)
    db.delete(task)
    db.commit()

    db.refresh(deleted_task)

    return deleted_task


def modify_task_status(db: Session, task_id: int, user_id: int, status: str):
    task = read_task(db=db, task_id=task_id, user_id=user_id)
    task.status = status
    db.commit()
    db.refresh(task)
    return task


def read_status_values() -> dict:
    return dict(models.STATUS_OPTIONS)
