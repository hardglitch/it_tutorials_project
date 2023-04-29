from dataclasses import dataclass
from fastapi import HTTPException, status


@dataclass()
class AuthenticateExceptions:

    CREDENTIAL_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    INCORRECT_PARAMETERS = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    FAILED_TO_CREATE_TOKEN = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Failed to create a token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    TOKEN_NOT_FOUND = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token not found",
        headers={"WWW-Authenticate": "Bearer"},
    )

    TOKEN_EXPIRED = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )


class DatabaseExceptions:
    COMMON_EXCEPTION = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database error",
    )


class LanguageExceptions:
    FAILED_TO_ADD_LANGUAGE = HTTPException(
        status_code=status.HTTP_304_NOT_MODIFIED,
        detail="Failed to add language",
    )


class UserExceptions:
    ACCESS_DENIED = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Access denied",
    )


class TutorialExceptions:
    TUTORIAL_NOT_FOUND = HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Tutorial not found",
    )


class CommonExceptions:
    INVALID_PARAMETERS = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Invalid request parameters",
    )

    DUPLICATED_ENTRY = HTTPException(
        status_code=status.HTTP_304_NOT_MODIFIED,
        detail="There is already an entry with the same parameters",
    )

    NOTHING_FOUND = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Nothing found",
    )
