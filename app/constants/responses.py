from dataclasses import dataclass
from typing import Annotated
from fastapi import HTTPException
from pydantic import Field
from starlette import status
from starlette.responses import Response


class ResponseScheme(Response):
    status_code: Annotated[int, status]
    content: str | None = Field(max_length=256, default=None, example="This is the response description")


@dataclass()
class CommonResponses:
    SUCCESS = ResponseScheme(
        status_code=status.HTTP_200_OK,
        content="Successful",
    )
    CREATED = ResponseScheme(
        status_code=status.HTTP_201_CREATED,
        content="Successful",
    )


@dataclass()
class UserResponses:

    USER_CREATED = "User registered"
    USER_NOT_CREATED = "User not created"
    USER_ALREADY_EXISTS = "User with the same name or email already exists"
    THIS_USER_HAS_BEEN_DELETED = "This user has been deleted"
    USER_NOT_FOUND = "User not found"
    USER_UPDATED = "User updated"
    USER_NOT_UPDATED = "User not updated"

    ACCESS_DENIED = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Access denied",
    )


@dataclass()
class TutorialResponses:
    TUTORIAL_ALREADY_EXISTS = "A tutorial with the same parameters already exists"
    TUTORIAL_ADDED = ResponseScheme(
        status_code=status.HTTP_200_OK,
        content="Your tutorial has been added",
    )
    PARAMETER_ERRORS = "Error(s) in parameter(s)"


@dataclass()
class LanguageResponses:
    FAILED_TO_ADD_LANGUAGE = "Failed to add language"

