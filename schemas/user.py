from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: str
    is_active: bool = True


class UserCreate(UserBase):
    email: EmailStr
    password: str
    is_superuser: bool = False


class UserUpdate(UserBase):
    password: Optional[str] = None
    is_superuser: bool = False


class UserOut(UserBase):
    user_id: int
    is_active: bool

# class UserInDatabase(UserBase):
#     hashed_password: str
#     is_superuser: bool = False
