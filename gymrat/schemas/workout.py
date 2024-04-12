from datetime import date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from gymrat.schemas.exercise import ExerciseOut


class WorkoutBase(BaseModel):
    name: str
    description: Optional[str] = None
    expires: Optional[date] = None


class WorkoutCreate(WorkoutBase):
    ...


class WorkoutUpdate(WorkoutBase):
    ...


class WorkoutOut(WorkoutBase):
    workout_id: int
    owner_id: int
    expires: Optional[date] = None


class Workout(WorkoutBase):
    workout_id: int
    exercises: Optional[List[ExerciseOut]]
    owner_id: int
    model_config = ConfigDict(from_attributes=True)
