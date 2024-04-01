from typing import Optional

from pydantic import BaseModel, Field

from schemas.exercise_set import ExerciseSetOut
from schemas.user import UserOut


class ExerciseBase(BaseModel):
    title: str
    exercise_type: int = Field(..., gt=0, description='The number of the ')
    muscle: int = Field(..., gt=0, description='The number of the muscle')
    level: int = Field(..., gt=0, description='The number of the level'
                       )
    description: Optional[str] = Field(title='The description of the exercise')


class ExerciseCreate(ExerciseBase):
    ...


class ExerciseUpdate(ExerciseBase):
    title: Optional[str] = None
    exercise_type: Optional[int] = None
    muscle: Optional[int] = None
    level: Optional[int] = None
    description: Optional[str] = None


class ExerciseOut(ExerciseBase):
    exercise_id: int
    ex_set: Optional[ExerciseSetOut]
    title: str
    exercise_type: Optional[int] = None
    muscle: Optional[int] = None
    level: Optional[int] = None
    description: Optional[str] = None
    owner_id: Optional[UserOut]

# class ExerciseInDatabase(ExerciseBase):
#     exercise_id: int
#     created_at: datetime
#     updated_at: datetime
#     owner_id: int
