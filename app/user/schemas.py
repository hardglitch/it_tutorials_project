from typing import Annotated
from pydantic import BaseModel, EmailStr, SecretStr, validator
from app.common.constants import Credential, DecodedCredential
from app.tools import hard_clean_text, remove_dup_spaces


class IDSchema(BaseModel):
    id: int | None = None

    @validator("id")
    def check_value(cls, value: int):
        return value if value >= 0 else None


UserID = Annotated[int, IDSchema]


class UserNameSchema(BaseModel):
    name: str | None = None

    @validator("name")
    def check_value(cls, value: str):
        return hard_clean_text(value[:100]) if remove_dup_spaces(value) else None


UserName = Annotated[str, UserNameSchema]


class PasswordSchema(BaseModel):
    password: SecretStr | None = None

    @validator("password")
    def check_value(cls, value: SecretStr):
        return value if 10 <= len(value) <= 100 else None


Password = Annotated[SecretStr, PasswordSchema]


class RatingSchema(BaseModel):
    rating: int | None = None

    @validator("rating")
    def check_value(cls, value: int):
        return value if value >= 0 else None


Rating = Annotated[int, RatingSchema]


class EmailSchema(BaseModel):
    email: EmailStr | None = None

    @validator("email")
    def check_value(cls, value: EmailStr):
        return value[:320] if value else None


EMail = Annotated[EmailStr, EmailSchema]


class UserSchema(
    IDSchema,
    UserNameSchema,
    PasswordSchema,
    RatingSchema
):

    email: EmailStr | None = None
    credential: Credential | None = None
    decoded_credential: DecodedCredential | None = None
    token: str | None = None
