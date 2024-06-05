# pylint: disable=E0401
"""Util functions to support auth methods"""
import bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using the Bcrypt
    hashpw function.

    Args:
        password (str): Password string

    Returns:
        str: Computed Hash
    """
    return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt()).decode("utf8")


def verify_password(plain_password, hashed_password) -> bool:
    """Verify a password against the hashed version
    using bcrypt checkpw function.

    Args:
        plain_password (str): Password
        hashed_password (bool): Prehashed password (from DB)

    Returns:
        bool: Verification of password
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
