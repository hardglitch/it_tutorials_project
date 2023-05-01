from dataclasses import dataclass
from starlette import status
from app.common.responses import ResponseScheme


@dataclass()
class TutorialResponses:
    TUTORIAL_ADDED = ResponseScheme(
        status_code=status.HTTP_201_CREATED,
        content="Your tutorial has been added",
    )
