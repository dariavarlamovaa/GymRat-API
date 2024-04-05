from datetime import timedelta

import fastapi
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Dict, Any

from gymrat.crud.users import authenticate
from gymrat.db.db_setup import get_db
from gymrat.schemas.auth import Token
from security import create_access_token

router = fastapi.APIRouter()


@router.post('login-user/', response_model=Token)
async def login_user(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, Any]:
    user = authenticate(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail='Invalid username or password')
    if not user.is_active:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail='User is not active'
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        subject=user.user_id, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

