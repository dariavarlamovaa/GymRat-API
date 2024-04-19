from unittest.mock import patch, MagicMock
import pytest
from fastapi import HTTPException
from sqlmodel import Session

from gymrat.api.dependencies import get_token, get_current_user, get_current_super_user
from gymrat.crud.user import user_crud
from gymrat.db.models.user import User
from gymrat.schemas.auth import TokenPayload


def test_get__valid_token():
    token = 'valid'
    payload = TokenPayload(sub='1111111', username='user1')

    with patch('jwt.decode', return_value={'sub': '1111111', 'username': 'user1'}) as j:
        result = get_token(token)
    assert result == payload


def test_get_invalid_token():
    token = 'invalid'
    with pytest.raises(HTTPException):
        get_token(token)


def test_get_current_user():
    mock_db = MagicMock(spec=Session)
    mock_token = MagicMock(spec=TokenPayload)
    mock_token.sub = 1

    mock_user = User(user_id=1, username='user1', email='user1@mail.ru')
    user_crud.get_one = MagicMock(return_value=mock_user)

    result = get_current_user(db=mock_db, token=mock_token)

    assert result == mock_user


def test_get_current_not_found_user():
    mock_db = MagicMock(spec=Session)
    mock_token = MagicMock(spec=TokenPayload)
    mock_token.sub = 1

    user_crud.get_one = MagicMock(return_value=None)

    with pytest.raises(HTTPException) as error:
        get_current_user(db=mock_db, token=mock_token)

    assert error.value.status_code == 404
    assert error.value.detail == 'User not found'


def test_get_current_super_user():
    current_user = User(is_superuser=True)
    result = get_current_super_user(current_user)
    assert result == current_user