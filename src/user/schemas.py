# Pydantic models

from pydantic import BaseModel, EmailStr, Field
from src.user.models import Credential


class User(BaseModel):
    # id: int
    name: str = Field(min_length=1, max_length=1024)
    email: EmailStr
    credential: Credential
    is_active: bool = True
    rating: int = Field(gt=-1, default=0)

    class Config:
        orm_mode = True


class UserCreate(User):
    credential = Credential.user
    password: str = Field(min_length=10, max_length=1024)


class UserRead(User):
    pass


class UserUpdate(User):
    pass


class UserDelete(User):
    pass
