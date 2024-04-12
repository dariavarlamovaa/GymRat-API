from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, status, HTTPException, Path, Body
from typing import List, Optional, Annotated

from gymrat.api.dependencies import get_current_super_user, get_current_user
from gymrat.db.db_setup import get_db
from gymrat.crud.workout import workout_crud
from gymrat.db.models.user import User
from gymrat.db.models.workout import Workout
from gymrat.schemas.workout import WorkoutOut, WorkoutCreate

router = APIRouter()


@router.get('/all', dependencies=[Depends(get_current_super_user)], status_code=status.HTTP_200_OK)
async def fetch_all_workouts(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100):
    workouts = workout_crud.get_many(db, skip=skip, limit=limit)
    return workouts


@router.get('/all/{workout_id}', dependencies=[Depends(get_current_super_user)], status_code=status.HTTP_200_OK)
async def fetch_one_workout(
        workout_id: int,
        db: Session = Depends(get_db)):
    workout = workout_crud.get_one(db, Workout.workout_id == workout_id)
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Workout with id - {workout_id} not found'
        )
    return workout


@router.get('/my', response_model=List[Optional[WorkoutOut]], status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user)])
async def fetch_my_workouts(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    exercises = workout_crud.get_many(db, Workout.owner_id == current_user.user_id)
    if not exercises:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"You don`t have any workouts",
        )
    return exercises


@router.get('/my/{workout_id}', response_model=Optional[WorkoutOut], status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user)])
async def fetch_my_one_workout(
        workout_id: int = Path(..., description='The id of the workout'),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    exercise = workout_crud.get_one(db, Workout.owner_id == current_user.user_id, Workout.workout_id == workout_id)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workout with id - {workout_id} not found in your storage",
        )
    return exercise


@router.get("/name/{workout_name}", response_model=Optional[WorkoutOut],
            dependencies=[Depends(get_current_super_user), Depends(get_current_user)])
async def fetch_one_exercise_by_title(
        workout_name: str = Path(..., description='The title of the workout'),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    workout = workout_crud.get_one(db, Workout.name == workout_name)
    if workout is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workout with name: '{workout_name}' not found",
        )
    if not current_user.is_superuser and (workout.owner_id != current_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Access forbidden'
        )
    return workout


@router.post('/create', response_model=Optional[WorkoutOut],
             response_model_exclude_none=True,
             response_model_exclude_unset=True,
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(get_current_user)])
async def create_new_workout(
        workout_create: Annotated[
            WorkoutCreate,
            Body(examples=[
                {
                    "name": "The name of the workout",
                    "description": "The description of the workout",
                    "expires": "Expire date (2024-04-12) Optional"
                }
            ])],
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    workout = workout_crud.get_one(db, Workout.name == workout_create.name, Workout.owner_id == current_user.user_id)
    if workout:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Workout with name '{workout_create.name}' already exists"
        )
    try:
        workout = workout_crud.create_workout(workout_create, db, owner_id=current_user.user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Something went wrong. {str(e)}'
        )
    return workout


