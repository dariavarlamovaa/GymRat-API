from sqlalchemy.orm import Session

from gymrat.crud.base import ORMRep
from gymrat.db.models.workout import Workout
from gymrat.schemas.workout import WorkoutCreate


class WorkoutCRUDRep(ORMRep):
    pass


workout_crud = WorkoutCRUDRep(model=Workout)
