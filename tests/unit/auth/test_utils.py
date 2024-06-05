from task_api.auth.utils import hash_password, verify_password

PLAIN_PASSWORD = "a-password-string"


def test_hash_password():
    assert hash_password(PLAIN_PASSWORD) is not None


def test_verify_password():
    hashed_password = hash_password(PLAIN_PASSWORD)
    assert (
        verify_password(plain_password=PLAIN_PASSWORD, hashed_password=hashed_password)
        is True
    )
