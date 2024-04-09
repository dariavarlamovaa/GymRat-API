import enum

from sqlalchemy import Column, String, Integer, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from gymrat.db.db_setup import Base
from gymrat.db.models.workout import workouts_exercises
from gymrat.db.models.mixins import Timestamp


class Type(enum.Enum):
    weight = 'weight'
    cardio = 'cardio'


class MajorMuscle(enum.Enum):
    arms = 'arms'
    core = 'core'
    full_body = 'full body'
    back = 'back'
    legs = 'legs'


class Level(enum.Enum):
    beginner = 'beginner'
    intermediate = 'intermediate'
    expert = 'expert'


class Exercise(Timestamp, Base):
    __tablename__ = 'exercises'
    exercise_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), unique=True, nullable=False)
    equipment = Column(String(100), nullable=False)
    exercise_type = Column(Enum(Type))
    muscle = Column(Enum(MajorMuscle))
    level = Column(Enum(Level))
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=False)
    tips = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    url = Column(URLType, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.user_id'))

    workouts = relationship("Workout", secondary=workouts_exercises, back_populates='exercises')

    def __repr__(self):
        return f"<Exercise(id={self.exercise_id}, title={self.title})>"
