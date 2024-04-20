from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    email: EmailStr
    hashed_password: str
    is_superuser: bool = False
    is_active: bool = True


class UserUpdate(UserBase):
    username: Optional[str] = None
    hashed_password: Optional[str] = None
    is_superuser: bool = False


class UserUpdateMyData(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserUpdatePassword(BaseModel):
    current_password: str
    new_password: str


class UserOut(UserBase):
    user_id: int
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
