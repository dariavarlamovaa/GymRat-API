from fastapi import FastAPI
from app import exercise, user

from db.db_setup import engine
from db.models import user, exercise, exercise_set, workout

user.Base.metadata.create_all(bind=engine)
exercise.Base.metadata.create_all(bind=engine)
exercise_set.Base.metadata.create_all(bind=engine)
workout.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gym Exercises API",
              description='API for managing Gym Exercises',
              version="0.0.1",
              contact={
                  "name": "Dora",
              },
              license_info={
                  "name": "MIT",
              }, )

app.include_router(exercises.router)
app.include_router(users.router)
