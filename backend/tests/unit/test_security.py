from datetime import timedelta

import jwt
import pytest

from security import get_hashed_password, verify_password, create_access_token


@pytest.mark.parametrize(
    'sub, expires_delta',
    [
        ('user1', timedelta(minutes=30)),
        ('user2', None)
    ],
)
def test_create_access_token(sub, expires_delta, test_settings):
    # check token creation
    token = create_access_token(sub, expires_delta)
    assert token is not None

    # check if the token is str type
    assert isinstance(token, str)

    # check if the decoded token is not None
    decoded = jwt.decode(
        token,
        test_settings.SECRET_KEY,
        algorithms=test_settings.ALGORITHM,
        options={'verify_aud': False}
    )

    assert decoded is not None


def test_get_hashed_password():
    password = '111'
    hashed_password = get_hashed_password(password)
    assert password not in hashed_password


def test_verify_password():
    user_password = '111'
    hashed_password = get_hashed_password(user_password)
    assert verify_password(user_password, hashed_password)


def test_not_verified_passwords():
    user_password = '111'
    hashed_password = get_hashed_password(user_password)
    assert verify_password('222', hashed_password) == False
