from datetime import date
from typing import Optional, List

from pydantic import BaseModel

from gymrat.schemas.exercise import ExerciseOut


class WorkoutBase(BaseModel):
    name: str
    description: Optional[str] = None
    expires: Optional[date] = None


class WorkoutCreate(WorkoutBase):
    ...


class WorkoutUpdate(WorkoutBase):
    name: str = None


class WorkoutOut(WorkoutBase):
    workout_id: int
    owner_id: int
    exercises: Optional[List[ExerciseOut]] = []
    expires: Optional[date] = None
