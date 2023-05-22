from typing import Annotated
from pydantic import BaseModel, EmailStr, SecretStr, validator
from ..common.constants import Credential, DecodedCredential
from ..tools import hard_clean_text


class IDSchema(BaseModel):
    id: int | None = None

UserID = Annotated[int, IDSchema]


class UserNameSchema(BaseModel):
    name: str | None = None

class ValidUserNameSchema(BaseModel):
    name: str | None = None

    @validator("name")
    def check_value(cls, value: str):
        return value if 1 < len(value := hard_clean_text(value)) <= 100 else None

UserName = Annotated[str, UserNameSchema]
ValidUserName = Annotated[str, ValidUserNameSchema]


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

EMail = Annotated[EmailStr, EmailSchema]


class UserSchema(
    IDSchema,
    UserNameSchema,
    PasswordSchema,
    EmailSchema,
    RatingSchema,
):

    credential: Credential | None = None
    decoded_credential: DecodedCredential | None = None
    is_active: bool | None = None


class TokenDataSchema(
    IDSchema,
    UserNameSchema,
):
    pass
