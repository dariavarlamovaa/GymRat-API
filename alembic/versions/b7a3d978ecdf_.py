"""empty message

Revision ID: c22637079635
Revises:
Create Date: 2024-04-02 16:08:50.292778

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c22637079635'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('user_id', sa.INTEGER(), server_default=sa.text("nextval('users_user_id_seq'::regclass)"),
                              autoincrement=True, nullable=False),
                    sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
                    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('is_active', sa.BOOLEAN(), default=True, autoincrement=False, nullable=True),
                    sa.Column('is_superuser', sa.BOOLEAN(), default=False, autoincrement=False, nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=True),
                              server_default=sa.text("now()"), autoincrement=False, nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True),
                              server_default=sa.text("now()"), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('user_id', name='users_pkey'),
                    sa.UniqueConstraint('username', name='users_username_key'),
                    postgresql_ignore_search_path=False
                    )
    op.create_index('ix_users_user_id', 'users', ['user_id'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    op.create_table('workouts',
                    sa.Column('workout_id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=40), autoincrement=False, nullable=False),
                    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
                    sa.Column('expires', sa.DATE(), autoincrement=False, nullable=True),
                    sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=True),
                              server_default=sa.text("now()"), autoincrement=False, nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True),
                              server_default=sa.text("now()"), autoincrement=False, nullable=False),
                    sa.ForeignKeyConstraint(['owner_id'], ['users.user_id'], name='workouts_owner_id_fkey'),
                    sa.PrimaryKeyConstraint('workout_id', name='workouts_pkey'),
                    sa.UniqueConstraint('name', 'owner_id', name='workouts_name_owner_id_key')
                    )
    op.create_index('ix_workouts_workout_id', 'workouts', ['workout_id'], unique=False)
    op.create_table('exercises',
                    sa.Column('exercise_id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('title', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
                    sa.Column('equipment', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
                    sa.Column('sets', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('reps', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('tips', sa.TEXT(), autoincrement=False, nullable=True),
                    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
                    sa.Column('url', sa.TEXT(), autoincrement=False, nullable=True),
                    sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['owner_id'], ['users.user_id'], name='exercises_owner_id_fkey'),
                    sa.Column('created_at', sa.DateTime(timezone=True),
                              server_default=sa.text("now()"), autoincrement=False, nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True),
                              server_default=sa.text("now()"), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('exercise_id', name='exercises_pkey'),
                    sa.UniqueConstraint('title', name='exercises_title_key')
                    )
    op.add_column('exercises',
                  sa.Column('exercise_type', sa.ENUM('weight', 'cardio', name='type'), autoincrement=False,
                            nullable=True))
    op.add_column('exercises',
                  sa.Column('muscle', sa.ENUM('arms', 'core', 'full_body', 'back', 'legs', name='majormuscle'),
                            autoincrement=False, nullable=True))
    op.add_column('exercises',
                  sa.Column('level', sa.ENUM('beginner', 'intermediate', 'expert', name='level'),
                            autoincrement=False, nullable=True))
    op.create_index('ix_exercises_exercise_id', 'exercises', ['exercise_id'], unique=False)

    op.create_table('workouts_exercises',
                    sa.Column('workout_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('exercise_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['exercise_id'], ['exercises.exercise_id'],
                                            name='workouts_exercises_exercise_id_fkey'),
                    sa.ForeignKeyConstraint(['workout_id'], ['workouts.workout_id'],
                                            name='workouts_exercises_workout_id_fkey')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_workouts_workout_id', table_name='workouts')
    op.drop_table('workouts')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_user_id', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_exercises_exercise_id', table_name='exercises')
    op.drop_table('exercises')
    op.drop_table('workouts_exercises')
    # ### end Alembic commands ###
