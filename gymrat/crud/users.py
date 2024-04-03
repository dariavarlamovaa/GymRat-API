from typing import Optional

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from gymrat.db.models.user import User
from gymrat.schemas.user import UserCreate
from security import get_hashed_password


def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {user_id} id not found",
        )
    return user


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user_create: UserCreate):
    user_username = get_user_by_username(db, username=user_create.username)
    user_email = get_user_by_email(db, email=user_create.email)
    if user_username is not None or user_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with this email or username already exists'
        )

    hashed_password = get_hashed_password(user_create.password)
    db_user = User(username=user_create.username, email=user_create.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
