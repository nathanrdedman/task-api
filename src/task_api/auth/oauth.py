# pylint: disable=E0401
"""Module with functions supporting OAuth and JWT authentication"""
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from task_api.api.schema import TokenData
from task_api.auth.utils import verify_password
from task_api.db.connect import get_db
from task_api.db.models import User
from task_api.db.operation import get_user_by_username

SECRET_KEY = "ee670cbd960dab20eac3df2e0bb0ecef0700dac53eb922b6d88afca064556c3c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(db, username: str, password: str) -> Union[User, None]:
    """Given a set of credentials, authenticate the user
    via stored user object, verifying the password against the
    hashed password.

    Args:
        db (Session): Database session
        username (str): Username
        password (str): Password

    Returns:
        Union[User, bool]: user object or 'False' if authentication fails
    """
    user = get_user_by_username(db, username)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = None
) -> str:
    """Given a data dictionary of user parameters, generate a JWT token with the
    specified expiration date.

    Args:
        data (dict): Data dict of
        expires_delta (Union[timedelta, None], optional):\
            Time window for expiration. Defaults to None.

    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
) -> User:
    """Given a token, decode the token, check if valid and return
    the user object by username.

    Args:
        token (Annotated[str, Depends): JWT token
        db (Session, optional): DB session. Defaults to Depends(get_db).

    Raises:
        credentials_exception:

    Returns:
        User: authenticated user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError as err:
        raise credentials_exception from err

    user = None

    if token_data.username:
        user = get_user_by_username(db, username=token_data.username)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Return the current authenticated user for the current
    session.

    Args:
        current_user (Annotated[User, Depends): Currently authenticated user

    Returns:
        User: User object
    """
    return current_user
