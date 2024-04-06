from fastapi import FastAPI
from gymrat.api.routers import users, exercises, auth

from gymrat.db.db_setup import engine
from gymrat.db.models import workout, exercise, user

user.Base.metadata.create_all(bind=engine)
exercise.Base.metadata.create_all(bind=engine)
workout.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gym Rat API",
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
app.include_router(auth.router)
