from typing import Optional, List

import fastapi
from pydantic import BaseModel

router = fastapi.APIRouter()

exercises = []


class Exercise(BaseModel):
    email: str
    is_active: bool
    bio: Optional[str]


@router.get("/exercises", response_model=List[Exercise])
async def get_exercises():
    return exercises


@router.get("/exercises/{exercise_id}")
async def get_exercise(exercise_id):
    return exercises
