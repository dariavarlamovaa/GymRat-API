from fastapi import Path, Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from gymrat.db.models.user import User
from gymrat.api.dependencies import get_current_super_user, get_current_user
from gymrat.crud.users import user_crud

from gymrat.db.db_setup import get_db
from gymrat.schemas.user import UserOut, UserCreate, UserUpdate, UserUpdatePassword, UserUpdateMyData

router = APIRouter()


@router.get("/users", response_model=List[Optional[UserOut]], status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_super_user)])
async def fetch_all_users(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100):
    return user_crud.get_many(db, skip=skip, limit=limit)


@router.get("/users/{user_id}", response_model=Optional[UserOut], status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_super_user)])
async def fetch_user_by_id(
        user_id: int = Path(..., description='The id of the user'),
        db: Session = Depends(get_db)):
    user = user_crud.get_one(db, User.user_id == user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id - {user_id} not found",
        )
    return user


@router.get("/username/{username}", response_model=Optional[UserOut], status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_super_user)])
async def fetch_user_by_username(
        username: str = Path(..., description='The username of the user'),
        db: Session = Depends(get_db)):
    user = user_crud.get_user_by_username(db=db, username=username)
    return user


@router.get("/email/{email}", response_model=Optional[UserOut], status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_super_user)])
async def fetch_user_by_email(
        email: str = Path(..., description='The email of the user'),
        db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db=db, email=email)
    return user


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(get_current_super_user)])
async def create_new_user(
        user_create: UserCreate,
        db: Session = Depends(get_db)):
    return user_crud.create_user(db=db, user_create=user_create)


@router.delete('/delete-user/{user_id}', status_code=status.HTTP_200_OK)
async def delete_one_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    return user_crud.delete_user(db, user_id, current_user)


@router.put('/update-user/{user_id}', status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_super_user)])
async def update_one_user(
        user_id: int,
        user_update: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_super_user)):
    user = user_crud.get_user_by_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with {user_id} not found'
        )
    try:
        user = user_crud.update_user(db, user_update, current_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Something went wrong. Error: {str(e)}'
        )
    return user


@router.get('/me', status_code=status.HTTP_200_OK)
async def fetch_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put('/update-my-data', status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)],
            response_model=UserOut)
async def update_my_data(new_data: UserUpdateMyData, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    user_crud.update_my_own_data(db, new_data, current_user)
    return current_user


@router.patch('/update-my-password', status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)],
              response_model=UserOut)
async def update_my_password(new_password_data: UserUpdatePassword, db: Session = Depends(get_db),
                             current_user: User = Depends(get_current_user)):
    try:
        user_crud.update_my_owm_password(db, new_password_data, current_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Something went wrong. Error - {str(e)}'
        )
    return current_user
