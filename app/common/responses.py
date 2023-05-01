from dataclasses import dataclass
from typing import Annotated
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
