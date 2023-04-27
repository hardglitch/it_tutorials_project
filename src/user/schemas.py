# Pydantic models

from pydantic import BaseModel, EmailStr, Field
from src.constants.constants import Credential


class UserIDScheme(BaseModel):
    id: int = Field(ge=0)

class NameScheme(BaseModel):
    name: str = Field(min_length=1, max_length=1024, example="new user")

class CredentialScheme(BaseModel):
    credential: int = Field(ge=Credential.user.value, le=Credential.admin.value, default=Credential.user)

class DecodedCredentialScheme(BaseModel):
    decoded_credential: str = Field(example="user")

class RatingScheme(BaseModel):
    rating: int = Field(ge=0, default=0)

class EmailScheme(BaseModel):
    email: EmailStr = Field(example="newuser@email.com")

class PasswordScheme(BaseModel):
    password: str = Field(min_length=10, max_length=100, example="1234567890")

class HashedPasswordScheme(BaseModel):
    hashed_password: str = Field(max_length=1024)


class AddUserScheme(
    NameScheme,
    CredentialScheme,
    EmailScheme,
    PasswordScheme
):
    pass


class GetUserScheme(
    NameScheme,
    DecodedCredentialScheme,
    RatingScheme
):
    pass


class EditUserScheme(
    NameScheme,
    EmailScheme,
    PasswordScheme
):
    pass


class AuthUserScheme(
    UserIDScheme,
    NameScheme,
    HashedPasswordScheme
):
    pass
