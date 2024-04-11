from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ExerciseBase(BaseModel):
    title: str
    equipment: str
    muscle: Optional[str] = Field(title='arms, core, full body, back, legs')
    exercise_type: Optional[str] = Field(title='weight, cardio')
    level: Optional[str] = Field(title='beginner, intermediate, expert')
    description: Optional[str] = Field(title='The description of the exercise')
    tips: Optional[str] = Field(title='The tips of the exercise')


class ExerciseCreate(ExerciseBase):
    sets: Optional[int]
    reps: Optional[int]
    tips: Optional[str]
    description: Optional[str] = None
    tips: Optional[str] = None


class ExerciseUpdate(ExerciseBase):
    title: Optional[str] = None
    equipment: Optional[str] = None
    exercise_type: Optional[str] = None
    muscle: Optional[str] = None
    level: Optional[str] = None
    sets: Optional[int] = None
    reps: Optional[int] = None
    tips: Optional[str] = None
    description: Optional[str] = None


class ExerciseOut(ExerciseBase):
    exercise_id: int
    title: str
    exercise_type: Optional[str] = None
    muscle: Optional[str] = None
    level: Optional[str] = None
    sets: Optional[int] = None
    reps: Optional[int] = None
    tips: Optional[str] = None
    description: Optional[str] = None
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class Exercise(ExerciseBase):
    exercise_id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int
    model_config = ConfigDict(from_attributes=True)
