from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None
    is_superuser: bool = False


class UserOut(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime


class User(UserBase):
    hashed_password: str
    is_superuser: bool = False
    model_config = ConfigDict(from_attributes=True)
