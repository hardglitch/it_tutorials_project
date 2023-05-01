from dataclasses import dataclass
from fastapi import HTTPException
from starlette import status


@dataclass()
class TutorialExceptions:
    TUTORIAL_NOT_FOUND = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Tutorial not found",
    )
