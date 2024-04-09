from typing import Optional

from sqlalchemy.orm import Session

from gymrat.crud.base import ORMRep
from gymrat.db.models.user import User
from gymrat.schemas.user import UserCreate, UserUpdate, UserUpdatePassword
from security import get_hashed_password, verify_password


class UserCRUDRep(ORMRep):
    def get_user_by_username(self, db: Session, username: str):
        user = self.get_one(db, self._model.username == username)
        return user

    def get_user_by_email(self, db: Session, email: str):
        user = self.get_one(db, self._model.email == email)
        return user

    @staticmethod
    def create_user(db: Session, user_create: UserCreate):
        hashed_password = get_hashed_password(user_create.password)
        db_user = User(username=user_create.username, email=user_create.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user: User):
        db.delete(user)
        db.commit()

    @staticmethod
    def update_user(db: Session, user_update: UserUpdate, current_user: User):
        if user_update.password is not None:
            user_password = user_update.password
            current_user.hashed_password = get_hashed_password(user_password)
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
        return current_user

    @staticmethod
    def update_my_own_data(db: Session, current_user: User) -> User:
        db.add(current_user)
        db.commit()
        return current_user

    @staticmethod
    def update_my_owm_password(db: Session, new_password_data: UserUpdatePassword, current_user: User):
        hashed_password = get_hashed_password(new_password_data.new_password)
        current_user.hashed_password = hashed_password
        db.add(current_user)
        db.commit()
        return current_user

    def authenticate(self, db: Session, username: str, password: str) -> Optional[User]:
        user = self.get_user_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


user_crud = UserCRUDRep(model=User)
