from sqlalchemy import Column, Integer, Text, String, Date, ForeignKey, UniqueConstraint, Table
from sqlalchemy.orm import relationship

from db.db_setup import Base
from db.models.mixins import Timestamp

workouts_exercises = Table(
    "workouts_exercises",
    Base.metadata,
    Column("workout_id", Integer, ForeignKey("workouts.workout_id")),
    Column('exercise_id', Integer, ForeignKey('exercises.exercise_id'))

)


class Workout(Timestamp, Base):
    __tablename__ = 'workouts'

    __table_args__ = (
        UniqueConstraint("name", "owner_id"),
    )

    workout_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40), nullable=False)
    description = Column(Text, nullable=True)
    expires = Column(Date, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.user_id'))

    exercises = relationship('Exercise', secondary=workouts_exercises, back_populates="workout")

    def __repr__(self):
        return f'<Workout(id={self.workout_id}, name={self.name}>'
