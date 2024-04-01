from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from schemas.exercise import ExerciseOut
from schemas.exercise_set import ExerciseSetOut


class WorkoutBase(BaseModel):
    name: str
    description: Optional[str] = None
    expires: Optional[datetime] = None
    exercises: List[ExerciseOut]
    owner_id: int


class WorkoutCreate(WorkoutBase):
    ...


class WorkoutUpdate(WorkoutBase):
    ...


class WorkoutOut(WorkoutBase):
    workout_id: int
    ex_set: Optional[List[ExerciseSetOut]]
    owner_id: int
    expires: datetime
