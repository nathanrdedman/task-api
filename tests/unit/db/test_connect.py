import os
from typing import Generator
from unittest import mock

import pytest

from task_api.db.connect import get_db


@pytest.fixture(scope="class")
def mock_env_vars(scope="class"):
    with mock.patch.dict(os.environ, {"SQLALCHEMY_DATABASE_URL": "sqlite:///:memory:"}):
        yield


def test_get_db(mock_env_vars):
    db = get_db()
    assert db is not None
    assert isinstance(db, Generator) == True
