from gymrat.crud.base import ORMRep
from gymrat.db.models.exercise import Exercise

exercise_crud = ORMRep(model=Exercise)
