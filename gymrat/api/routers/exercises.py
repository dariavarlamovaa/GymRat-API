from typing import Optional, List, Annotated

from fastapi import Path, Depends, status, HTTPException, APIRouter, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel

from gymrat.api.dependencies import get_current_super_user, get_current_user
from gymrat.crud.exercises import exercise_crud
from gymrat.crud.users import user_crud
from gymrat.db.db_setup import get_db
from gymrat.db.models.user import User
from gymrat.schemas.exercise import ExerciseOut, ExerciseCreate, ExerciseUpdate
from gymrat.db.models.exercise import Exercise

router = APIRouter()


@router.get("/all", response_model=List[ExerciseOut], status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_super_user)])
async def fetch_all_exercises(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100):
    return exercise_crud.get_many(db, skip=skip, limit=limit)


@router.get("/all/{exercise_id}", response_model=Optional[ExerciseOut],
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
    return exercise


@router.get("/title/{exercise_title}", response_model=Optional[ExerciseOut],
            dependencies=[Depends(get_current_super_user)])
async def fetch_one_exercise(
        exercise_title: str = Path(..., description='The title of the exercise'),
        db: Session = Depends(get_db)):
    exercise = exercise_crud.get_one(db, Exercise.title == exercise_title)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with title: '{exercise_title}' not found",
        )
    return exercise


@router.get('/my', response_model=List[Optional[ExerciseOut]], status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user)])
async def fetch_my_exercises(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    exercises = exercise_crud.get_many(db, Exercise.owner_id == current_user.user_id)
    if not exercises:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"You don`t have any exercises",
        )
    return exercises


@router.get('/my/{exercise_id}', response_model=Optional[ExerciseOut], status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user)])
async def fetch_my_one_exercise(
        exercise_id: int = Path(..., description='The id of the exercise'),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    exercise = exercise_crud.get_one(db, Exercise.owner_id == current_user.user_id, Exercise.exercise_id == exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with id - {exercise_id} not found in your storage",
        )
    return exercise


@router.post('/create', response_model=Optional[ExerciseOut], status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(get_current_user)])
async def create_new_exercise(
        exercise_create: Annotated[
            ExerciseCreate,
            Body(examples=[
                {
                    "title": "Leg Press",
                    "equipment": "Leg Press machine",
                    "muscle": "Choose one: arms, core, full body, back, legs",
                    "exercise_type": "Choose one: weight, cardio",
                    "level": "Choose one: beginner, intermediate, expert",
                    "description": "string",
                    "sets": 3,
                    "reps": 15,
                    "tips": "string"
                }
            ])],
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    try:
        exercise_crud.create_exercise(exercise_create, db, current_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Something went wrong. {str(e)}'
        )
    return exercise_create


@router.put('/update', response_model=Optional[ExerciseOut], status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user)])
async def update_exercise(
        exercise_id: int,
        exercise_update: ExerciseUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    exercise = exercise_crud.get_one(db, Exercise.exercise_id == exercise_id)
    if exercise is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Exercise with id {exercise_id} not found'
        )
    if not current_user.is_superuser and (exercise.owner_id != current_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don`t have permission to delete this user")
    try:
        exercise_crud.update_exercise(db, exercise_update, current_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Something went wrong. {str(e)}'
        )
    return exercise_update
