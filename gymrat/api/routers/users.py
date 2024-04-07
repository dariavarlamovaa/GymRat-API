import fastapi
from fastapi import Path, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from gymrat.db.models.user import User
from gymrat.api.dependencies import get_current_super_user, get_current_user
from gymrat.crud.users import get_user_by_id, get_user_by_username, get_user_by_email, get_users, create_user, \
    delete_user, update_user, update_my_owm_password, update_my_own_data

from gymrat.db.db_setup import get_db
from gymrat.schemas.user import UserOut, UserCreate, UserUpdate, UserUpdatePassword, UserUpdateMyData

router = fastapi.APIRouter()


@router.get("/users", response_model=List[Optional[UserOut]], status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_super_user)])
async def fetch_all_users(
        skip: int = 0, limit: int = 100,
        db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=Optional[UserOut], status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_super_user)])
async def fetch_user_by_id(
        user_id: int = Path(..., description='The id of the user'),
        db: Session = Depends(get_db)):
    user = get_user_by_id(db=db, user_id=user_id)
    return user


@router.get("/username/{username}", response_model=Optional[UserOut], status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_super_user)])
async def fetch_user_by_username(
        username: str = Path(..., description='The username of the user'),
        db: Session = Depends(get_db)):
    user = get_user_by_username(db=db, username=username)
    return user


@router.get("/email/{email}", response_model=Optional[UserOut], status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_super_user)])
async def fetch_user_by_email(
        email: str = Path(..., description='The email of the user'),
        db: Session = Depends(get_db)):
    user = get_user_by_email(db=db, email=email)
    return user


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(get_current_super_user)])
async def create_new_user(
        user_create: UserCreate,
        db: Session = Depends(get_db)):
    return create_user(db=db, user_create=user_create)


@router.delete('/delete-user/{user_id}', status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_super_user)])
async def delete_one_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_super_user)):
    return delete_user(db, user_id, current_user)


@router.put('/update-user/{user_id}', status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_super_user)])
async def update_one_user(
        user_id: int,
        user_update: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_super_user)):
    user = get_user_by_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with {user_id} not found'
        )
    try:
        user = update_user(db, user_update, current_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Something went wrong. Error: {str(e)}'
        )
    return user


@router.put('/update-my-data', status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)],
            response_model=UserOut)
async def update_my_data(new_data: UserUpdateMyData, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    update_my_own_data(db, new_data, current_user)
    return current_user


@router.patch('/update-my-password', status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)],
              response_model=UserOut)
async def update_my_password(new_password_data: UserUpdatePassword, db: Session = Depends(get_db),
                             current_user: User = Depends(get_current_user)):
    try:
        update_my_owm_password(db, new_password_data, current_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Something went wrong. Error - {str(e)}'
        )
    return current_user
