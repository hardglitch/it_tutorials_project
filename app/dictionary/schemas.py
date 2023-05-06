from typing import Annotated
from pydantic import BaseModel, validator
from app.language.schemas import LangCodeSchema
from app.tools import remove_dup_spaces


class WordCodeSchema(BaseModel):
    word_code: int | None = None

DictWordCode = Annotated[int, WordCodeSchema]


class DictValueSchema(BaseModel):
    dict_value: str | None = None

class ValidDictValueSchema(BaseModel):
    dict_value: str | None = None

    @validator("dict_value")
    def check_value(cls, value: str) -> str | None:
        return value[:256] if remove_dup_spaces(value) else None

DictValue = Annotated[str, DictValueSchema]
ValidDictValue = Annotated[str, ValidDictValueSchema]


class DictionarySchema(
    WordCodeSchema,
    LangCodeSchema,
    DictValueSchema
):
    pass
