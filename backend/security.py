import datetime
from datetime import timedelta, datetime
from typing import Union, Any

import jwt
from passlib.context import CryptContext

from gymrat.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(sub: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode = {"exp": expire, "sub": str(sub)}
    encoded = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded


def get_hashed_password(not_hashed_password: str) -> str:
    return pwd_context.hash(not_hashed_password)


def verify_password(user_password: str, hashed_password: str):
    return pwd_context.verify(user_password, hashed_password)
