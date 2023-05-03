from dataclasses import dataclass
from typing import Annotated
from pydantic import Field
from starlette import status
from starlette.responses import JSONResponse


class ResponseSchema(JSONResponse):
    status_code: Annotated[int, status]
    content: str | None = Field(max_length=256, default=None, example="This is the response description")


@dataclass()
class CommonResponses:
    SUCCESS = ResponseSchema(
        status_code=status.HTTP_200_OK,
        content="Successful",
    )
    CREATED = ResponseSchema(
        status_code=status.HTTP_201_CREATED,
        content="Successful",
    )
