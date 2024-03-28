from typing import Optional, List

import fastapi
from fastapi import Path
from pydantic import BaseModel

router = fastapi.APIRouter()

exercises = []


class Exercise(BaseModel):
    email: str
    is_active: bool
    bio: Optional[str]


@router.get("/exercises", response_model=List[Exercise])
async def get_user():
    return exercises


@router.get("/users/{user_id}")
async def get_user(exercise_id: int = Path(..., description='The id of the exercise')):
    return {'user': exercises[exercise_id]}
