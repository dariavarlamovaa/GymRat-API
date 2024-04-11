from typing import Optional

from sqlalchemy.orm import Session

from gymrat.crud.base import ORMRep
from gymrat.db.models.user import User
from gymrat.schemas.user import UserCreate
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

    def authenticate(self, db: Session, username: str, password: str) -> Optional[User]:
        user = self.get_user_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


user_crud = UserCRUDRep(model=User)
