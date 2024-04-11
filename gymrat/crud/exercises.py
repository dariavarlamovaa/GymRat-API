from sqlalchemy.orm import Session
from gymrat.crud.base import ORMRep
from gymrat.db.models.exercise import Exercise
from gymrat.schemas.exercise import ExerciseCreate


class ExerciseCRUDRep(ORMRep):
    @staticmethod
    def create_exercise(
            exercise_create: ExerciseCreate,
            db: Session,
            owner_id: int):
        exercise_create_data = exercise_create.model_dump(exclude_unset=True, exclude_none=True, exclude_defaults=True)
        exercise_obj = Exercise(**exercise_create_data, owner_id=owner_id)
        db.add(exercise_obj)
        db.commit()
        db.refresh(exercise_obj)
        return exercise_obj


exercise_crud = ExerciseCRUDRep(model=Exercise)
