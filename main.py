from typing import Optional, List
from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI(title="Gym Plan API",
              description='API for managing Gym Plan',
              version="0.0.1",
              contact={
                  "name": "Dora",
              },
              license_info={
                  "name": "MIT",
              }, )

users = []


class User(BaseModel):
    email: str
    is_active: bool
    bio: Optional[str]


@app.get("/users", response_model=List[User])
async def get_user():
    return users


@app.post("/users")
async def create_user(user: User):
    users.append(user)
    return 'Success'


@app.get("/users/{user_id}")
async def get_user(user_id: int = Path(..., description='The id of the user')):
    return {'user': users[user_id]}

# @app.delete("/users/delete")
# async def delete_user(user):
#     users.remove(user)
#     return {"message": "User has been deleted"}
