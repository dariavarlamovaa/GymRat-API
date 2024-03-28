from fastapi import FastAPI
from app.exercises import router

app = FastAPI(title="Gym Exercises API",
              description='API for managing Gym Exercises',
              version="0.0.1",
              contact={
                  "name": "Dora",
              },
              license_info={
                  "name": "MIT",
              }, )

app.include_router(router)