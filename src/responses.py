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
