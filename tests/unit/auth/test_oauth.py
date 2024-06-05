from unittest.mock import patch

import pytest

from task_api.api.schema import UserInDB
from task_api.auth.oauth import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_current_user,
)

MOCK_USER = UserInDB(
    username="test",
    email="email@domain.com",
    password="apassword",
    hashed_password="a-hashed-password",
)


@patch("task_api.auth.oauth.get_user_by_username")
@patch("task_api.auth.oauth.verify_password")
def test_fail_authenticate_user(verify_password, get_user_by_username):
    get_user_by_username.return_value = None
    verify_password.return_value = None
    user = authenticate_user({}, username="test", password="test1")

    assert user == None


@patch("task_api.auth.oauth.get_user_by_username")
@patch("task_api.auth.oauth.verify_password")
def test_pass_authenticate_user(verify_password, get_user_by_username):
    get_user_by_username.return_value = MOCK_USER
    verify_password.return_value = True
    user = authenticate_user({}, username="test", password="test1")

    assert user is not None


def test_create_access_token():
    jwt_token = create_access_token(MOCK_USER.model_dump())

    assert jwt_token is not None


@patch("task_api.auth.oauth.get_user_by_username")
async def test_fail_get_current_user(get_user_by_username):
    get_user_by_username.return_value = None
    jwt_token = create_access_token(MOCK_USER.model_dump())

    with pytest.raises(Exception):
        current_user = await get_current_user(jwt_token)


@patch("task_api.auth.oauth.get_user_by_username")
async def test_get_current_user(get_user_by_username):
    get_user_by_username.return_value = MOCK_USER
    data_dict = MOCK_USER.model_dump()
    data_dict["sub"] = data_dict.get("username")
    jwt_token = create_access_token(data_dict)
    current_user = await get_current_user(jwt_token, {})

    assert current_user is not None


async def test_get_current_active_user():
    assert await get_current_active_user(MOCK_USER) is not None
