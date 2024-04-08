from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from gymrat.schemas.user import UserOut


class ExerciseBase(BaseModel):
    title: str
    equipment: str
    muscle: Optional[int] = Field(title='arms(1), core(2), full body(3), back(4), legs(5)')
    exercise_type: int = Field(title='weight(1), cardio(2)')
    level: int = Field(title='beginner(1), intermediate(2), expert(3)')
    description: int = Field(title='The description of the exercise')
    reps: Optional[int]
    tips: Optional[str]


class ExerciseCreate(ExerciseBase):
    ...


class ExerciseUpdate(ExerciseBase):
    title: Optional[str] = None
    muscle: Optional[int] = Field(title='arms(1), core(2), full body(3), back(4), legs(5)')
    exercise_type: Optional[int] = Field(title='weight(1), cardio(2)')
    level: Optional[int] = Field(title='beginner(1), intermediate(2), expert(3)')
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
    owner: Optional[UserOut]


class Exercise(ExerciseBase):
    exercise_id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int
    model_config = ConfigDict(from_attributes=True)
