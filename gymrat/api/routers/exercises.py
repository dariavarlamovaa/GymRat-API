from typing import Optional, List

from fastapi import Path, Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel

from gymrat.api.dependencies import get_current_super_user
from gymrat.crud.exercises import exercise_crud
from gymrat.crud.users import user_crud
from gymrat.db.db_setup import get_db
from gymrat.db.models.user import User
from gymrat.schemas.exercise import ExerciseOut
from gymrat.db.models.exercise import Exercise

router = APIRouter()


@router.get("/all-exercises", response_model=List[ExerciseOut], status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_super_user)])
async def fetch_all_exercises(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100):
    return exercise_crud.get_many(db, skip=skip, limit=limit)


@router.get("/all-exercises/{exercise_id}", response_model=Optional[ExerciseOut],
            dependencies=[Depends(get_current_super_user)])
async def fetch_one_exercise(
        exercise_id: int = Path(..., description='The id of the exercise'),
        db: Session = Depends(get_db)):
    exercise = exercise_crud.get_one(db, Exercise.exercise_id == exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with id - {exercise_id} not found",
        )
    owner = user_crud.get_one(db, User.user_id == exercise.owner_id)
    exercise.owner = owner
    return exercise
