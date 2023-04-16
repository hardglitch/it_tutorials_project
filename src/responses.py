from dataclasses import dataclass
from fastapi import HTTPException, status


@dataclass()
class UserResponses:

    USER_CREATED = HTTPException(
        status_code=status.HTTP_201_CREATED,
        detail="User registered",
    )

    USER_NOT_CREATED = {
         "response": "User not created"
    }

    USER_ALREADY_EXISTS = {
        "response": "User with the same name or email already exists"
    }

    SUCCESS = {
        "response": "Success"
    }

    USER_NOT_FOUND = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )

    ACCESS_DENIED = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied",
    )

    USER_UPDATED = HTTPException(
        status_code=status.HTTP_200_OK,
        detail="User updated",
    )

    USER_NOT_UPDATED = HTTPException(
        status_code=status.HTTP_304_NOT_MODIFIED,
        detail="User not updated",
    )


@dataclass()
class TutorialResponses:
    TUTORIAL_ALREADY_EXISTS = {
        "response": "A tutorial with the same parameters already exists"
    }

    TUTORIAL_CREATED = HTTPException(
        status_code=status.HTTP_201_CREATED,
        detail="Your tutorial added",
    )

    TUTORIAL_NOT_FOUND = {
        "response": "A tutorial not found"
    }
