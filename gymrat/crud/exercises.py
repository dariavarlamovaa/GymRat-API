from typing import Optional

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from gymrat.crud.base import ORMRep
from gymrat.db.models.exercise import Exercise


class ExerciseCRUDRep(ORMRep):
    pass


exercise_crud = ExerciseCRUDRep(model=Exercise)
