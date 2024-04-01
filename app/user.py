import fastapi
from fastapi import Path

router = fastapi.APIRouter()

users = []


@router.get("/users")
async def get_user():
    return users


@router.get("/users/{user_id}")
async def get_user(user_id: int = Path(..., description='The id of the user')):
    return {'user': users[user_id]}
