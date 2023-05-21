from dataclasses import dataclass
from fastapi import HTTPException, status


@dataclass()
class DatabaseExceptions(BaseException):
    COMMON_EXCEPTION = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database error",
    )

    DUPLICATED_ENTRY = HTTPException(
        status_code=status.HTTP_304_NOT_MODIFIED,
        detail="There is already an entry with the same parameters",
    )


@dataclass()
class CommonExceptions(BaseException):
    INVALID_PARAMETERS = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Invalid request parameters",
    )

    NOTHING_FOUND = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Nothing found",
    )


class LocaleExceptions(BaseException):
    LOCALE_NOT_FOUND = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="A Locale not found",
    )

    WRONG_LOCALE = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="A Wrong Locale",
    )
