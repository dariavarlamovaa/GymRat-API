import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from gymrat.crud.users import user_crud
from gymrat.db.db_setup import get_db
from gymrat.db.models.user import User
from gymrat.schemas.auth import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_token(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    try:
        token_payload = jwt.decode(token, key="secretkey", algorithms=["HS256"])
        token_data = TokenPayload(**token_payload)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail='Can`t return token')
    return token_data


def get_current_user(db: Session = Depends(get_db), token: TokenPayload = Depends(get_token)) -> User:
    user = user_crud.get_one(db, User.user_id == token.sub)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail='User not found')
    return user


def get_current_super_user(current_user: User = Depends(get_current_user)) -> User:
    if not is_super_user(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Access Forbidden'
        )
    return current_user


def is_super_user(user: User) -> bool:
    return user.is_superuser
