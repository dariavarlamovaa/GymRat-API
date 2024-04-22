from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlmodel import Session

from gymrat.crud.exercises import exercise_crud
from gymrat.crud.user import user_crud
from gymrat.db.models.exercise import Exercise
from gymrat.db.models.user import User
from gymrat.schemas.exercise import ExerciseCreate
from gymrat.schemas.user import UserCreate
from security import get_hashed_password


def _create_user(
        db: Session,
        username: str,
        email: EmailStr,
        password: str,
        is_active: bool,
        is_superuser: bool) -> User:
    user = user_crud.get_user_by_username(db, username=username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User already exists'
        )

    created_user = UserCreate(
        username=username,
        email=email,
        hashed_password=get_hashed_password(password),
        is_active=is_active,
        is_superuser=is_superuser
    )
    user = user_crud.create(db, create_obj=created_user)
    return user


def _create_exercise(db: Session,
                     user: User,
                     title: str,
                     equipment: str,
                     muscle: str,
                     exercise_type: str,
                     level: str
                     ) -> Exercise:
    owner_id = user.user_id
    assert owner_id is not None

    item_in = ExerciseCreate(title=title, equipment=equipment, muscle=muscle, exercise_type=exercise_type, level=level)
    return exercise_crud.create_with_owner(db, item_in, owner_id)
