from datetime import timedelta

import fastapi
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Dict, Any

from gymrat.crud.user import user_crud
from gymrat.db.db_setup import get_db
from gymrat.schemas.auth import Token, Register
from gymrat.schemas.user import UserCreate
from security import create_access_token, get_hashed_password

router = fastapi.APIRouter()


@router.post('/login', response_model=Token)
async def login_user(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, Any]:
    user = user_crud.authenticate(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password')
    if not user.is_active:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail='User is not active'
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        sub=user.user_id, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/signup', status_code=status.HTTP_201_CREATED)
def register(new_user: Register, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_username(db, new_user.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'User with username - "{new_user.username}" already exists'
        )
    user_created = UserCreate(
        **new_user.model_dump(exclude_unset=True, exclude_defaults=True),
        hashed_password=get_hashed_password(new_user.password)
    )
    user_crud.create(db, user_created)
    return user_created
