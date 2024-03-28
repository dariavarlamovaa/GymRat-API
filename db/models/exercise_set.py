from sqlalchemy import Column, String, Integer, Enum, Text, Time, ForeignKey
from sqlalchemy.orm import relationship

from .all_exercises import Exercise
from ..db_setup import Base


# class ExerciseSet(Base):
#     __tablename__ = 'exercise_set'
#     exercise_set_id = Column(Integer, primary_key=True, index=True)
#     exercise_id = Column(Integer, ForeignKey(Exercise.exercise_id))
#     set_number = Column(Integer, nullable=True)
#     reps = Column(Integer, nullable=False)
#     weight = Column(Text, nullable=True)
#     rest_time = Column(Time, nullable=True)
#     tips = Column(Text, nullable=True)
#
#     exercise = relationship('Exercise', )
