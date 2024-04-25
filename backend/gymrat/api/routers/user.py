from fastapi import Path, Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from gymrat.db.models.user import User
from gymrat.api.dependencies import get_current_super_user, get_current_user
from gymrat.crud.user import user_crud

from gymrat.db.db_setup import get_db
from gymrat.schemas.user import UserOut, UserCreate, UserUpdate, UserUpdatePassword, UserUpdateMyData
from security import verify_password, get_hashed_password

router = APIRouter()


@router.get("/all", response_model=List[Optional[UserOut]], status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_super_user)])
def fetch_all_users(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100):
    return user_crud.get_many(db, skip=skip, limit=limit)


@router.get("/all/{user_id}", response_model=Optional[UserOut], status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_super_user)])
def fetch_user_by_id(
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
def fetch_user_by_username(
        username: str = Path(..., description='The username of the user'),
        db: Session = Depends(get_db)):
    user = user_crud.get_user_by_username(db=db, username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with '{username}' username not found",
        )
    return user


@router.get("/email/{email}", response_model=Optional[UserOut], status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_super_user)])
def fetch_user_by_email(
        email: str = Path(..., description='The email of the user'),
        db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with '{email}' email not found",
        )
    return user


@router.post("/create", response_model=Optional[UserOut], status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(get_current_super_user)])
def create_new_user(
        user_create: UserCreate,
        db: Session = Depends(get_db)):
    user_username = user_crud.get_user_by_username(db, username=user_create.username)
    user_email = user_crud.get_user_by_email(db, email=user_create.email)
    if user_username is not None or user_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with this email or username already exists'
        )
    try:
        user_create.hashed_password = get_hashed_password(user_create.hashed_password)
        user = user_crud.create(db, user_create)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Can`t delete this user, {str(e)}'
        )
    return user


@router.delete('/delete/{user_id}', status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
def delete_one_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    user = user_crud.get_one(db, User.user_id == user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found")
    elif user_id != current_user.user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don`t have permission to delete this user")
    elif user == current_user and current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Super users can`t delete themselves'
        )
    try:
        user_crud.delete(db, user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Can`t delete this user, {str(e)}'
        )
    return {f'User with id {user_id} deleted'}


@router.put('/update/{user_id}', status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_super_user)])
def update_one_user(
        user_id: int,
        user_update: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_super_user)):
    user = user_crud.get_one(db, User.user_id == user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with {user_id} not found'
        )
    if user_update.hashed_password is not None:
        user_password = user_update.hashed_password
        current_user.hashed_password = get_hashed_password(user_password)
    try:
        user = user_crud.update(db, user, user_update)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Something went wrong. Error: {str(e)}'
        )
    return user


@router.get('/me', status_code=status.HTTP_200_OK)
def fetch_user_me(
        current_user: User = Depends(get_current_user)):
    return current_user


@router.put('/update-my-data', status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)],
            response_model=UserOut)
def update_my_data(
        new_data: UserUpdateMyData, db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    user_username = user_crud.get_user_by_username(db, username=new_data.username)
    user_email = user_crud.get_user_by_email(db, email=new_data.email)
    if user_username is not None or user_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with this email or username already exists'
        )
    if new_data.username is not None:
        current_user.username = new_data.username
    if new_data.email is not None:
        current_user.email = new_data.email
    try:
        user_crud.update(db, current_user, new_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Something went wrong. Error - {str(e)}'
        )
    return current_user


@router.patch('/update-my-password', status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)],
              response_model=UserOut)
def update_my_password(
        new_password_data: UserUpdatePassword, db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    if not verify_password(new_password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Incorrect password'
        )
    if new_password_data.current_password == new_password_data.new_password:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='New password cannot be the same as the current one'
        )
    try:
        hashed_password = get_hashed_password(new_password_data.new_password)
        current_user.hashed_password = hashed_password
        user_crud.update(db, current_user, new_password_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Something went wrong. Error - {str(e)}'
        )
    return current_user
