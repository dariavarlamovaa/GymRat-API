from fastapi import FastAPI
from gymrat.api.routers import user, exercises, auth, workout as w

from gymrat.db.db_setup import engine
from gymrat.db.models import workout, exercise, user as u

u.Base.metadata.create_all(bind=engine)
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

app.include_router(exercises.router, prefix='/exercises', tags=['exercises'])
app.include_router(user.router, prefix='/users', tags=['users'])
app.include_router(w.router, prefix='/workouts', tags=['workouts'])
app.include_router(auth.router, prefix='/auth', tags=['auth'])


@app.get("/")
def root():
    return {"message": "Hi, Gym Rat <3"}
