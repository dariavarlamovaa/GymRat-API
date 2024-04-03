import fastapi
from fastapi import Path, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..crud.users import get_user_by_id, get_user_by_username, get_user_by_email, get_users, create_user
from ..db.db_setup import get_db
from ..schemas.user import UserOut, UserCreate

router = fastapi.APIRouter()


@router.get("/users", response_model=List[Optional[UserOut]], status_code=status.HTTP_200_OK)
async def fetch_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=Optional[UserOut], status_code=status.HTTP_200_OK)
async def fetch_user_by_id(user_id: int = Path(..., description='The id of the user'), db: Session = Depends(get_db)):
    user = get_user_by_id(db=db, user_id=user_id)
    return user


@router.get("/username/{username}", response_model=Optional[UserOut], status_code=status.HTTP_200_OK)
async def fetch_user_by_username(username: str = Path(..., description='The username of the user'), db: Session = Depends(get_db)):
    user = get_user_by_username(db=db, username=username)
    return user


@router.get("/email/{email}", response_model=Optional[UserOut], status_code=status.HTTP_200_OK)
async def fetch_user_by_email(email: str = Path(..., description='The email of the user'), db: Session = Depends(get_db)):
    user = get_user_by_email(db=db, email=email)
    return user


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_new_user(user_create: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user_create=user_create)
