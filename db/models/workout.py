from sqlalchemy import Column, Integer, Text, String, Date, ForeignKey, UniqueConstraint, Table
from sqlalchemy.orm import relationship

from db.db_setup import Base
from db.models.mixins import Timestamp

training_plan_training_unit = Table(
    "workout_plan",
    Base.metadata,
    Column("workout_id", Integer, ForeignKey("workout.workout_id")),
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
    exercise_set_id = Column(Integer, ForeignKey('exercise_sets.exercise_set_id'), nullable=True)
    owner_id = Column(Integer, ForeignKey('users.user_id'))

    ex_set = relationship('ExerciseSet', back_populates="workout")
    owner = relationship('User')

    def __repr__(self):
        return f'<Workout(id={self.workout_id}, name={self.name}>'
