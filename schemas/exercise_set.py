from datetime import time
from typing import Optional

from pydantic import BaseModel

from schemas.exercise import ExerciseOut


class ExerciseSetBase(BaseModel):
    title: str
    exercise_id: int


class ExerciseSetCreate(ExerciseSetBase):
    ...


class ExerciseUpdate(ExerciseSetBase):
    title: Optional[str] = None
    set_number: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None
    rest_time: Optional[time] = None
    tips: Optional[str] = None


class ExerciseSetOut(ExerciseSetBase):
    exercise_set_id: int
    title: str
    exercise_id: Optional[ExerciseOut]
    muscle: Optional[int] = None
    level: Optional[int] = None
    description: Optional[str] = None
