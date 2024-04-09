from typing import Optional, Annotated

from fastapi import HTTPException, Depends, Body
from fastapi import status
from sqlalchemy.orm import Session

from gymrat.crud.base import ORMRep
from gymrat.db.models.exercise import Exercise
from gymrat.db.models.user import User
from gymrat.schemas.exercise import ExerciseCreate, ExerciseUpdate


class ExerciseCRUDRep(ORMRep):
    @staticmethod
    def create_exercise(
            exercise_create: ExerciseCreate,
            db: Session,
            current_user: User):
        exercise_create_data = exercise_create.model_dump(exclude_unset=True, exclude_defaults=True)
        db_exercise = Exercise(**exercise_create_data, owner_id=current_user.user_id)
        db.add(db_exercise)
        db.commit()
        return db_exercise

    def update_exercise(
            self,
            db: Session,
            exercise_update: ExerciseUpdate,
            current_user: User):
        update_objmodel = exercise_update.model_dump(exclude_unset=True)
        update_objmodel.sqlupdate_model(update_objmodel)


exercise_crud = ExerciseCRUDRep(model=Exercise)
