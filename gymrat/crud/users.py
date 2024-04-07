from typing import Optional

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from gymrat.db.models.user import User
from gymrat.schemas.user import UserCreate, UserUpdate, UserUpdatePassword, UserUpdateMyData
from security import get_hashed_password, verify_password


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


def delete_user(db: Session, user_id: int, current_user: User):
    user = get_user_by_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found. Cannot delete.")
    if user_id == current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You cannot delete yourself")
    try:
        db.delete(user)
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Can`t delete this user, {str(e)}'
        )
    return {f'User with id {user_id} deleted'}


def update_user(db: Session, user_update: UserUpdate, current_user: User):
    if user_update.password is not None:
        user_password = user_update.password
        current_user.hashed_password = get_hashed_password(user_password)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


def update_my_own_data(db: Session, new_data: UserUpdateMyData, current_user: User) -> User:
    user_username = get_user_by_username(db, username=new_data.username)
    user_email = get_user_by_email(db, email=new_data.email)
    if user_username is not None or user_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with this email or username already exists'
        )
    if new_data.username is not None:
        current_user.username = new_data.username
    if new_data.email is not None:
        current_user.email = new_data.email
    db.add(current_user)
    db.commit()
    return current_user


def update_my_owm_password(db: Session, new_password_data: UserUpdatePassword, current_user: User):
    if not verify_password(new_password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Incorrect password'
        )
    if new_password_data.current_password == new_password_data.new_password:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='New password cannot be the same as the current one'
        )
    hashed_password = get_hashed_password(new_password_data.new_password)
    current_user.hashed_password = hashed_password
    db.add(current_user)
    db.commit()
    return 'Password successfully updated'


def authenticate(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
