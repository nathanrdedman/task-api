import pytest

from task_api.api import schema
from task_api.db.models import STATUS_OPTIONS, DeletedTask, Task, User
from task_api.db.operation import (
    archive_task,
    get_user,
    get_user_by_email,
    get_user_by_username,
    modify_task_status,
    new_user,
    read_status_values,
    read_task,
    read_tasks,
    write_task,
)
from tests.unit.db.utils import db_engine, db_session, db_session_factory


def create_test_user_input():
    return schema.UserCreate(username="test", password="test", email="test@domain.com")


def test_add_user(db_session):
    user = new_user(db=db_session, user=create_test_user_input())

    assert user is not None
    assert user.id is not None
    assert user.hashed_password is not None


def test_get_user(db_session):
    user = new_user(db=db_session, user=create_test_user_input())

    existing_user = get_user(db=db_session, user_id=user.id)
    assert existing_user is not None


def test_get_user_by_username(db_session):
    user = new_user(db=db_session, user=create_test_user_input())

    stored_user = get_user_by_username(db=db_session, username=user.username)
    assert stored_user is not None
    assert stored_user.username == user.username


def test_get_user_by_email(db_session):
    user = new_user(db=db_session, user=create_test_user_input())

    stored_user = get_user_by_email(db=db_session, email=user.email)
    assert stored_user is not None
    assert stored_user.email == user.email


def test_write_task(db_session):
    user = new_user(db=db_session, user=create_test_user_input())
    task = write_task(db=db_session, description="a test task", user_id=user.id)

    assert task is not None
    assert task.user_id == user.id


def test_read_task(db_session):
    user = new_user(db=db_session, user=create_test_user_input())
    task = write_task(db=db_session, description="a test task", user_id=user.id)

    task_out = read_task(db=db_session, task_id=task.id, user_id=user.id)

    assert task_out is not None
    assert task_out.user_id == user.id


def test_read_tasks(db_session):
    user = new_user(db=db_session, user=create_test_user_input())
    for i in range(0, 5):
        task = write_task(db=db_session, description=f"task {i}", user_id=user.id)

    tasks_out = read_tasks(db=db_session, user_id=user.id)

    assert isinstance(tasks_out, list) == True
    assert len(tasks_out) == 5


def test_archive_task(db_session):
    user = new_user(db=db_session, user=create_test_user_input())
    task = write_task(db=db_session, description=f"task to be deleted", user_id=user.id)

    archived_task = archive_task(db=db_session, task_id=task.id, user_id=user.id)
    tasks_out = read_tasks(db=db_session, user_id=user.id)

    assert len(tasks_out) == 0
    assert archived_task is not None


def test_modify_task_status(db_session):
    user = new_user(db=db_session, user=create_test_user_input())
    task = write_task(db=db_session, description=f"task to be updated", user_id=user.id)
    assert task.status == STATUS_OPTIONS[0][0]

    modify_task_status(
        db=db_session, task_id=task.id, user_id=user.id, new_status=STATUS_OPTIONS[1][0]
    )

    updated_task = read_task(db=db_session, task_id=task.id, user_id=user.id)

    assert task.status == STATUS_OPTIONS[1][0]
    assert task.status != STATUS_OPTIONS[0][0]


def test_modify_task_unknown_status(db_session):
    user = new_user(db=db_session, user=create_test_user_input())
    task = write_task(db=db_session, description=f"task to be updated", user_id=user.id)
    assert task.status == STATUS_OPTIONS[0][0]

    with pytest.raises(Exception):
        modify_task_status(
            db=db_session, task_id=task.id, user_id=user.id, new_status="undefined"
        )


def test_read_status_values(db_session):
    status_values = read_status_values()
    assert status_values == dict(STATUS_OPTIONS)
