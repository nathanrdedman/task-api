from sqlalchemy.orm import Session

from ..api import schema
from . import models


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schema.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
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
    return task.id


def archive_task(db: Session, task_id: int, user_id: int):
    task = read_task(db=db, task_id=task_id, user_id=user_id)

    # Explicit assignment of values - could generalise
    deleted_task = models.DeletedTask(
        description=task.description,
        id=task.id,
        user_id=task.user_id,
        status=task.status,
    )

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


def read_status_values():
    return [t[0] for t in models.STATUS_OPTIONS]
