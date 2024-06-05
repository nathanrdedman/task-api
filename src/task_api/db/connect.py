# pylint: disable=E0401
"""Methods to support connection to a database"""
import os
from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL: Any = os.environ.get("SQLALCHEMY_DATABASE_URL")


def get_db() -> Generator[Session, None, None]:
    """Return a session to
    connect to the database

    Yields:
        Session: DB session
    """
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = session_local()
    try:
        yield db
    finally:
        db.close()
