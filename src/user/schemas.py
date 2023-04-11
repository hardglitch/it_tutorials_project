# Pydantic models

from pydantic import BaseModel, EmailStr, Field
from src.models import Credential


class UserScheme(BaseModel):
    name: str = Field(min_length=1, max_length=1024)
    email: EmailStr
    credential: int = Field(default=Credential.user)
    is_active: bool = True
    rating: int = Field(gt=-1, default=0)

    class Config:
        orm_mode = True


class UserCreateScheme(UserScheme):
    password: str = Field(min_length=10, max_length=100)


class UserReadScheme(UserScheme):
    pass


class UserFullReadScheme(UserReadScheme):
    id: int
    hashed_password: str = Field(max_length=1024)


class UserUpdate(UserScheme):
    pass


class UserDelete(UserScheme):
    pass
