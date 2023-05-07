from typing import Annotated
from pydantic import BaseModel
from ...dictionary.schemas import DictionarySchema
from ...tutorial.type.schemas import TypeCodeSchema


class ThemeCodeSchema(BaseModel):
    theme_code: int | None = None

ThemeCode = Annotated[int, ThemeCodeSchema]


class ThemeSchema(
    ThemeCodeSchema,
    TypeCodeSchema,
    DictionarySchema,
):
    pass
