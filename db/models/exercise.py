import enum

from sqlalchemy import Column, String, Integer, Enum, Text, ForeignKey, Time, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType


from db.db_setup import Base


class Type(enum.Enum):
    weight = 1
    cardio = 2


class MajorMuscle(enum.Enum):
    arms = 1
    core = 2
    full_body = 3
    back = 4
    legs = 5


class Level(enum.Enum):
    beginner = 1
    intermediate = 2
    expert = 3


class Exercise(Base):
    __tablename__ = 'exercises'
    exercise_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), unique=True, nullable=False)
    equipment = Column(String(100), nullable=False)
    exercise_type = Column(Enum(Type))
    muscle = Column(Enum(MajorMuscle))
    level = Column(Enum(Level))
    description = Column(Text, nullable=False)
    url = Column(URLType, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.user_id'))

    owner = relationship("User")
    ex_set = relationship('ExerciseSet', back_populates="exercise")

    def __repr__(self):
        return f"<Exercise(id={self.exercise_id}, title={self.title})>"
