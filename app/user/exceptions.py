from dataclasses import dataclass
from fastapi import HTTPException
from starlette import status


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


@dataclass()
class UserExceptions:
    ACCESS_DENIED = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Access denied",
    )
