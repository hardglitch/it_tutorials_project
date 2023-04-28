from dataclasses import dataclass
from fastapi import HTTPException
from starlette import status


@dataclass()
class CommonResponses:
    SUCCESS = HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Successful",
    )
    FAILED = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Failed",
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
    TUTORIAL_ADDED = "Your tutorial has been added"
    TUTORIAL_NOT_FOUND = "A tutorial not found"
    PARAMETER_ERRORS = "Error(s) in parameter(s)"


@dataclass()
class LanguageResponses:
    FAILED_TO_ADD_LANGUAGE = "Failed to add language"

