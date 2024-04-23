from datetime import date

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlmodel import Session

from gymrat.crud.exercises import exercise_crud
from gymrat.crud.user import user_crud
from gymrat.crud.workout import workout_crud
from gymrat.db.models.exercise import Exercise
from gymrat.db.models.user import User
from gymrat.db.models.workout import Workout
from gymrat.schemas.exercise import ExerciseCreate
from gymrat.schemas.user import UserCreate
from gymrat.schemas.workout import WorkoutCreate
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
                     level: str,
                     sets: int = None,
                     reps: int = None,
                     description: str = None,
                     tips: str = None
                     ) -> Exercise:
    owner_id = user.user_id
    assert owner_id is not None

    item_in = ExerciseCreate(title=title, equipment=equipment, muscle=muscle, exercise_type=exercise_type, level=level,
                             sets=sets, reps=reps, description=description, tips=tips)
    return exercise_crud.create_with_owner(db, item_in, owner_id)


def _create_workout(db: Session,
                    user: User,
                    name: str,
                    description: str = None,
                    expires: date = None
                    ) -> Workout:
    owner_id = user.user_id
    assert owner_id is not None

    item_in = WorkoutCreate(name=name, description=description, expires=expires)
    return workout_crud.create_with_owner(db, item_in, owner_id)
