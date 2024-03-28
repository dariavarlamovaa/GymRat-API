import enum

from sqlalchemy import Column, String, Integer, Enum, Text

from ..db_setup import Base


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
    __tablename__ = 'all_exercises'
    exercise_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), unique=True, nullable=False)
    equipment = Column(String(100), nullable=False)
    ex_type = Column(Enum(Type))
    major_muscle = Column(Enum(MajorMuscle))
    minor_muscle = Column(Text, nullable=False)
    level = Column(Enum(Level))
    description = Column(Text, nullable=False)
    url = Column(Text, nullable=True)
