# Pydantic models

from pydantic import BaseModel, EmailStr, Field
from src.models import Credential


class User(BaseModel):
    name: str = Field(min_length=1, max_length=1024)
    email: EmailStr
    credential: int = Field(default=Credential.user)
    is_active: bool = True
    rating: int = Field(gt=-1, default=0)

    class Config:
        orm_mode = True


class UserCreate(User):
    password: str = Field(min_length=10, max_length=100)


class UserRead(User):
    pass


class UserFullRead(UserRead):
    id: int
    hashed_password: str = Field(max_length=1024)


class UserUpdate(User):
    pass


class UserDelete(User):
    pass
