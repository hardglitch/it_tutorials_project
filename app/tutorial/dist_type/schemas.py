from typing import Annotated
from pydantic import BaseModel
from ...dictionary.schemas import DictionarySchema


class DistTypeCodeSchema(BaseModel):
    dist_type_code: int | None = None

DistTypeCode = Annotated[int, DistTypeCodeSchema]


class DistTypeSchema(
    DistTypeCodeSchema,
    DictionarySchema
):
    pass