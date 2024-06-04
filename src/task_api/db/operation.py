from typing import List, Union

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


def new_user(db: Session, user: schema.UserCreate) -> models.User:
    """Given a username, password and email, create a new user

    Args:
        db (Session): DB sessions
        user (schema.UserCreate): pydantic user class

    Returns:
        models.User: Newly created user object
    """
    hashpassword = hash_password(user.password)
    new_user = models.User(
        email=user.email, hashed_password=hashpassword, username=user.username
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def read_task(db: Session, task_id: int, user_id: int) -> models.Task:
    """Given a user ID and task ID return the task object

    Args:
        db (Session): DB session
        task_id (int): Task ID
        user_id (int): User ID

    Returns:
        models.Task: Task object
    """
    return (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .filter(models.Task.user_id == user_id)
        .one()
    )


def read_tasks(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> List[models.Task]:
    """Given a user ID return all user tasks, with paging options.

    Args:
        db (Session): DB sessions
        user_id (int): Used ID
        skip (int, optional): Page offset. Defaults to 0.
        limit (int, optional): Page limit. Defaults to 100.

    Returns:
        List[models.Task]: List of task objects
    """
    return (
        db.query(models.Task)
        .filter(models.Task.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def write_task(db: Session, description: str, user_id: int) -> models.Task:
    """Given a task description, create a new task entry for the user.

    Args:
        db (Session): DB session
        description (str): Task description
        user_id (int): User ID

    Returns:
        models.Task: Newly created task object
    """
    task = models.Task(description=description, user_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def archive_task(db: Session, task_id: int, user_id: int) -> models.Task:
    """Given a task ID and user ID move a task to the deleted task table
    whist protecting the task id. Task ID is derived from a sequence, so
    we can track previous task ID.


    Args:
        db (Session): DB sessions
        task_id (int): Task ID
        user_id (int): User ID

    Returns:
        models.Task: Task object
    """
    task = read_task(db=db, task_id=task_id, user_id=user_id)

    deleted_task = models.DeletedTask(**task.dict())

    db.add(deleted_task)
    db.delete(task)
    db.commit()

    db.refresh(deleted_task)

    return deleted_task


def modify_task_status(
    db: Session, task_id: int, user_id: int, new_status: str
) -> models.Task:
    """Given a task id and new status, update the task object and return

    Args:
        db (Session): DB sessions
        task_id (int): Task ID
        user_id (int): User ID
        new_status (str): New status

    Returns:
        models.Task: Updated task object

    Raises:
        ValueError: Update status is not valid
    """
    task = read_task(db=db, task_id=task_id, user_id=user_id)

    if new_status not in [t[0] for t in models.STATUS_OPTIONS]:
        raise ValueError(f"{new_status=} is not a valid status")

    task.status = new_status  # type: ignore
    db.commit()
    db.refresh(task)

    return task


def read_status_values() -> dict:
    """Return all permitted status options for
    tasks

    Returns:
        dict: Dictionary of status types {"code":"value"}
    """
    return dict(models.STATUS_OPTIONS)
