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

    FAILED_TO_CREATE_TOKEN = {
        "response": "Failed to create token"
    }


class DatabaseExceptions:
    COMMON_EXCEPTION = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database error",
    )

