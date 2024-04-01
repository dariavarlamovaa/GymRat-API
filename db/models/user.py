from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from db.db_setup import Base
from db.models.mixins import Timestamp


class User(Timestamp, Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    workouts = relationship('Workout', back_populates='owner')

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
# op.add_column('exercises',
#                   sa.Column('exercise_type', postgresql.ENUM('weight', 'cardio', name='type'), autoincrement=False,
#                             nullable=True))
#     op.add_column('exercises',
#                   sa.Column('muscle', postgresql.ENUM('arms', 'core', 'full_body', 'back', 'legs', name='majormuscle'),
#                             autoincrement=False, nullable=True))
#     op.add_column('exercises',
#                   sa.Column('level', postgresql.ENUM('beginner', 'intermediate', 'expert', name='level'),
#                             autoincrement=False, nullable=True))