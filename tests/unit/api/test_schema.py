from dataclasses import dataclass

from task_api.api.schema import (
    Task,
    TaskBase,
    TaskCreate,
    Token,
    TokenData,
    User,
    UserCreate,
)

TOKEN_TYPE = "bearer"
ACCESS_TOKEN = "a-very-long-hashed-token"
USERNAME = "a_user"
DESCRIPTION = "a task description"
EMAIL = "email@domain.com"
PASSWORD = "password123"


@dataclass
class STATUS:
    code: str = "pending"
    value: str = "Pending"


def test_token():
    token_type = TOKEN_TYPE
    access_token = ACCESS_TOKEN
    token = Token(token_type=token_type, access_token=access_token)

    assert token.token_type == token_type
    assert token.access_token == access_token


def test_tokendata():
    tokendata = TokenData(username=USERNAME)
    assert tokendata.username == USERNAME


def test_taskbase():
    taskbase = TaskBase(description=DESCRIPTION)
    assert taskbase.description == DESCRIPTION


def test_taskcreate():
    taskcreate = TaskCreate(description=DESCRIPTION)
    assert taskcreate.description == DESCRIPTION


def test_task():
    task = Task(description=DESCRIPTION, status=STATUS, id=1)
    assert task.description == DESCRIPTION
    assert task.status == STATUS.value
    assert task.id == 1


def test_user():
    user = User(id=1, username=USERNAME, email=EMAIL)
    assert user.id == 1
    assert user.username == USERNAME
    assert user.email == EMAIL


def test_usercreate():
    usercreate = UserCreate(password=PASSWORD, username=USERNAME, email=EMAIL)
    assert usercreate.username == USERNAME
    assert usercreate.email == EMAIL
    assert usercreate.password == PASSWORD
