from typing import Optional

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from gymrat.crud.base import ORMRep
from gymrat.db.models.user import User
from gymrat.schemas.user import UserCreate, UserUpdate, UserUpdatePassword, UserUpdateMyData
from security import get_hashed_password, verify_password


class UserCRUDRep(ORMRep):
    def get_user_by_username(self, db: Session, username: str):
        user = self.get_one(db, self._model.username == username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with '{username}' username not found",
            )
        return user

    def get_user_by_email(self, db: Session, email: str):
        user = self.get_one(db, self._model.email == email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with '{email}' email not found",
            )
        return user

    def create_user(self, db: Session, user_create: UserCreate):
        user_username = self.get_user_by_username(db, username=user_create.username)
        user_email = self.get_user_by_email(db, email=user_create.email)
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

    def delete_user(self, db: Session, user_id: int, current_user: User):
        user = self.get_one(db, User.user_id == user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found")
        elif user_id != current_user.user_id and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You don`t have permission to delete this user")
        elif user == current_user and current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Super users can`t delete themselves'
            )
        try:

            db.delete(user)
            db.commit()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Can`t delete this user, {str(e)}'
            )
        return {f'User with id {user_id} deleted'}

    def update_user(self, db: Session, user_update: UserUpdate, current_user: User):
        if user_update.password is not None:
            user_password = user_update.password
            current_user.hashed_password = get_hashed_password(user_password)
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
        return current_user

    def update_my_own_data(self, db: Session, new_data: UserUpdateMyData, current_user: User) -> User:
        user_username = self.get_user_by_username(db, username=new_data.username)
        user_email = self.get_user_by_email(db, email=new_data.email)
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

    def update_my_owm_password(self, db: Session, new_password_data: UserUpdatePassword, current_user: User):
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

    def authenticate(self, db: Session, username: str, password: str) -> Optional[User]:
        user = self.get_user_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


user_crud = UserCRUDRep(model=User)
