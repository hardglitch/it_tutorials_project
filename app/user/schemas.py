from pydantic import BaseModel, EmailStr, Field
from app.common.constants import Credential


class UserIDSchema(BaseModel):
    id: int = Field(ge=0)

class UserNameSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100, example="New User")

class CredentialSchema(BaseModel):
    credential: int = Field(ge=Credential.user.value, le=Credential.admin.value, default=Credential.user)

class DecodedCredentialSchema(BaseModel):
    decoded_credential: str = Field(example="user")

class RatingSchema(BaseModel):
    rating: int = Field(ge=0, default=0)

class EmailSchema(BaseModel):
    email: EmailStr = Field(example="newuser@email.com")

class PasswordSchema(BaseModel):
    password: str = Field(min_length=10, max_length=100, example="1234567890")


class AddUserSchema(
    UserNameSchema,
    CredentialSchema,
    EmailSchema,
    PasswordSchema
):
    pass


class GetUserSchema(
    UserIDSchema,
    UserNameSchema,
    DecodedCredentialSchema,
    RatingSchema
):
    pass


class EditUserSchema(
    UserNameSchema,
    EmailSchema,
    PasswordSchema
):
    pass


class AuthUserSchema(
    UserIDSchema,
    UserNameSchema,
):
    pass
