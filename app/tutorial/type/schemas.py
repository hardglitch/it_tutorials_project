from typing import Annotated
from pydantic import BaseModel
from ...dictionary.schemas import DictionarySchema


class TypeCodeSchema(BaseModel):
    type_code: int | None = None

TypeCode = Annotated[int, TypeCodeSchema]


class TypeSchema(
    TypeCodeSchema,
    DictionarySchema
):
    pass
