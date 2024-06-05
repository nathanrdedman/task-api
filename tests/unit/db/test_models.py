import pytest

from task_api.db.models import DeletedTask, Task, User
from tests.unit.db.utils import db_engine, db_session, db_session_factory


def test_add_user(db_session):
    user = User(username="test", email="test", hashed_password="test")
    db_session.add(user)
    db_session.commit()
    users = db_session.query(User).all()
    assert len(users) == 1


def test_add_incomplete_user(db_session):
    user = User(username=None, email="test", hashed_password="test")
    with pytest.raises(Exception):
        db_session.add(user)
        db_session.commit()


def test_fails_add_duplicate_user(db_session):
    user = User(username="test", email="test", hashed_password="test")
    user_2 = User(username="test", email="test", hashed_password="test")
    with pytest.raises(Exception):
        db_session.add(user)
        db_session.add(user_2)
        db_session.commit()


def test_add_additional_users(db_session):
    user = User(username="test", email="test", hashed_password="test")
    user_2 = User(username="test2", email="test2", hashed_password="test")
    db_session.add(user)
    db_session.add(user_2)
    db_session.commit()
    users = db_session.query(User).all()
    assert len(users) == 2


def test_add_task(db_session):
    user = User(username="test", email="test", hashed_password="test")
    db_session.add(user)
    db_session.commit()
    user = db_session.query(User).first()
    # We add id manually here since SQlite does not support sequences
    task = Task(id=1, description="a test task", user_id=user.id, status="pending")
    db_session.add(task)
    db_session.commit()

    tasks = db_session.query(Task).all()
    assert len(tasks) == 1
    assert task.user_id == user.id


def test_add_deleted_task(db_session):
    user = User(username="test", email="test", hashed_password="test")
    db_session.add(user)
    db_session.commit()
    user = db_session.query(User).first()
    deleted_task = DeletedTask(
        id=1, description="a test task", user_id=user.id, status="pending"
    )
    db_session.add(deleted_task)
    db_session.commit()

    tasks = db_session.query(DeletedTask).all()
    assert len(tasks) == 1
