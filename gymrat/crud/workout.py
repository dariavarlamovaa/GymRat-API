from sqlalchemy.orm import Session

from gymrat.crud.base import ORMRep
from gymrat.db.models.workout import Workout
from gymrat.schemas.workout import WorkoutCreate


class WorkoutCRUDRep(ORMRep):
    @staticmethod
    def create_workout(
            workout_create: WorkoutCreate,
            db: Session,
            owner_id: int):
        workout_data = workout_create.model_dump(exclude_unset=True)
        workout_obj = Workout(**workout_data, owner_id=owner_id)
        db.add(workout_obj)
        db.commit()
        db.refresh(workout_obj)
        return workout_obj


workout_crud = WorkoutCRUDRep(model=Workout)
