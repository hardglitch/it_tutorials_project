import re
from typing import Annotated
from pydantic import BaseModel, validator
from ..tools import remove_dup_spaces


class LangCodeSchema(BaseModel):
    lang_code: int | None = None

LangCode = Annotated[int, LangCodeSchema]


class LangValueSchema(BaseModel):
    lang_value: str | None = None

class ValidLangValueSchema(BaseModel):
    lang_value: str | None = None

    @validator("lang_value")
    def check_value(cls, value: str) -> str | None:
        return value[:100] if (value := remove_dup_spaces(value)) else None

LangValue = Annotated[str, LangValueSchema]
ValidLangValue = Annotated[str, ValidLangValueSchema]



class LangAbbrSchema(BaseModel):
    abbreviation: str | None = None

class ValidLangAbbrSchema(BaseModel):
    abbreviation: str | None = None

    @classmethod
    def clean_lang_abbr(cls, value: str) -> str:
        pattern = re.compile(r"^[a-z]{3}")
        return re.match(pattern, value)[0]

    @validator("abbreviation")
    def check_value(cls, value: str) -> str | None:
        return value if (value := cls.clean_lang_abbr(value)) else None

LangAbbr = Annotated[str, LangAbbrSchema]
ValidLangAbbr = Annotated[str, ValidLangAbbrSchema]


class IsUILangSchema(BaseModel):
    is_ui_lang: bool | None = None

IsUILang = Annotated[bool, IsUILangSchema]


class LanguageSchema(
    LangValueSchema,
    LangAbbrSchema,
    IsUILangSchema,
    LangCodeSchema,
):
    pass