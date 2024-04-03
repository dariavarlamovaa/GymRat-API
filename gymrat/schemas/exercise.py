from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from gymrat.schemas.user import UserOut


class ExerciseBase(BaseModel):
    title: str
    description: Optional[str] = Field(title='The description of the exercise')


class ExerciseCreate(ExerciseBase):
    ...


class ExerciseUpdate(ExerciseBase):
    title: Optional[str] = None
    exercise_type: Optional[int] = None
    level: Optional[int] = None
    set_number: Optional[int] = None
    reps: Optional[int] = None
    tips: Optional[str] = None
    description: Optional[str] = None


class ExerciseOut(ExerciseBase):
    exercise_id: int
    title: str
    exercise_type: Optional[int] = None
    muscle: Optional[int] = None
    level: Optional[int] = None
    set_number: Optional[int] = None
    reps: Optional[int] = None
    tips: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[UserOut]


class Exercise(ExerciseBase):
    exercise_id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int
    model_config = ConfigDict(from_attributes=True)
