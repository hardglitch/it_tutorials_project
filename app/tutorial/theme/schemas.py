from typing import Annotated
from pydantic import BaseModel
from app.dictionary.schemas import DictionarySchema
from app.tutorial.type.schemas import TypeCodeSchema


class ThemeCodeSchema(BaseModel):
    theme_code: int | None = None

ThemeCode = Annotated[int, ThemeCodeSchema]


class ThemeSchema(
    ThemeCodeSchema,
    TypeCodeSchema,
    DictionarySchema,
):
    pass
