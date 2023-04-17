# Pydantic models

from pydantic import BaseModel, EmailStr, Field
from src.models import Credential


class UserScheme(BaseModel):
    name: str = Field(min_length=1, max_length=1024)
    credential: Credential = Field(default=Credential.user)
    is_active: bool = True
    rating: int = Field(gt=-1, default=0)

    class Config:
        orm_mode = True


class UserCreateScheme(UserScheme):
    email: EmailStr
    password: str = Field(min_length=10, max_length=100)


class UserReadScheme(UserScheme):
    # tutorial: List[TutorialScheme] | None
    pass


class DecryptedUserReadScheme(UserReadScheme):
    credential: str      # TODO: make a stronger check


class UserFullReadScheme(UserReadScheme):
    id: int
    hashed_password: str = Field(max_length=1024)


class UserUpdateScheme(BaseModel):
    name: str | None = Field(min_length=1, max_length=1024, default=None)
    email: EmailStr | None = None
    password: str | None = Field(min_length=10, max_length=100, default=None)
    credential: Credential | None = None


class UserDeleteScheme(UserScheme):
    pass
