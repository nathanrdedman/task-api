import os

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

from task_api.db.models import Base

# https://stackoverflow.com/questions/58660378/how-use-pytest-to-unit-test-sqlalchemy-orm-classes

DB_URL = os.environ.get("SQLALCHEMY_DATABASE_URL", "sqlite:///:memory:")


@pytest.fixture(scope="session")
def db_engine(request):
    """Yields a SQLAlchemy disposed after
    each session"""

    engine_ = create_engine(DB_URL, echo=True)
    Base.metadata.create_all(engine_)

    yield engine_
    Base.metadata.drop_all(engine_)
    engine_.dispose()


@pytest.fixture(scope="session")
def db_session_factory(db_engine):
    """returns a SQLAlchemy scoped
    session factory"""
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope="function")
def db_session(db_session_factory):
    """yields a SQLAlchemy connection which is
    rollbacked after the test"""
    session_ = db_session_factory()

    yield session_
    session_.rollback()

    for table in Base.metadata.sorted_tables:
        session_.execute(table.delete())
        session_.commit()

    session_.close()
