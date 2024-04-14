from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from gymrat.crud.base import ORMRep
from gymrat.db.models.exercise import Exercise
from gymrat.db.models.workout import Workout


class WorkoutCRUDRep(ORMRep):
    @staticmethod
    def add_exercise_to_workout(db: Session, workout: Workout, exercise: Exercise):
        workout.exercises.append(exercise)
        db.add(workout)
        db.commit()
        db.refresh(workout)
        return workout

    @staticmethod
    def remove_exercise_from_workout(db: Session, workout: Workout, exercise: Exercise):
        workout.exercises.remove(exercise)
        db.add(workout)
        db.commit()
        db.refresh(workout)
        return workout


workout_crud = WorkoutCRUDRep(model=Workout)
