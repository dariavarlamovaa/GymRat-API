# from sqlalchemy import Column, Integer, Text, ForeignKey, Float, Time
# from sqlalchemy.orm import relationship
#
# from db.db_setup import Base
# from db.models.mixins import Timestamp
#
#
# class ExerciseSet(Timestamp, Base):
#     __tablename__ = 'exercise_sets'
#     exercise_set_id = Column(Integer, primary_key=True, index=True)
#     exercise_id = Column(Integer, ForeignKey('exercises.exercise_id'), nullable=False)
#     set_number = Column(Integer, nullable=True)
#     reps = Column(Integer, nullable=False)
#     weight = Column(Float, nullable=True)
#     rest_time = Column(Time, nullable=True)
#     tips = Column(Text, nullable=True)
#
#     exercise = relationship('Exercise', back_populates='ex_set')
#     workout = relationship('Workout', back_populates='ex_set')
#
#     def __repr__(self):
#         return f"<Set(id={self.exercise_id}, title={self.title})>"
