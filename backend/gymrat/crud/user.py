from typing import Optional

from sqlalchemy.orm import Session

from gymrat.crud.base import ORMRep
from gymrat.db.models.user import User
from security import verify_password


class UserCRUDRep(ORMRep):
    def get_user_by_username(self, db: Session, username: str):
        user = self.get_one(db, self._model.username == username)
        return user

    def get_user_by_email(self, db: Session, email: str):
        user = self.get_one(db, self._model.email == email)
        return user

    def authenticate(self, db: Session, username: str, password: str) -> Optional[User]:
        user = self.get_user_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


user_crud = UserCRUDRep(model=User)
