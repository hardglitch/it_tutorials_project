# Pydantic models

from pydantic import BaseModel, EmailStr, Field
from src.constants.constants import Credential


class UserScheme(BaseModel):
    name: str = Field(min_length=1, max_length=1024)
    credential: int = Field(gt=Credential.user-1, lt=Credential.admin+1, default=Credential.user)
    is_active: bool = True
    rating: int = Field(ge=0, default=0)


class UserCreateScheme(UserScheme):
    email: EmailStr
    password: str = Field(min_length=10, max_length=100)


class UserReadScheme(UserScheme):
    # added_tutorials: List[TutorialScheme]
    pass


class DecryptedUserReadScheme(UserReadScheme):
    credential: str


class UserFullReadScheme(UserReadScheme):
    id: int = Field(ge=0)
    hashed_password: str = Field(max_length=1024)


class UserUpdateScheme(BaseModel):
    id: int | None = Field(ge=0)
    name: str | None = Field(min_length=1, max_length=1024, default=None)
    email: EmailStr | None = None
    password: str | None = Field(min_length=10, max_length=100, default=None)
