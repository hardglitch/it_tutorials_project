from pydantic import BaseModel, Field

class LangCodeSchema(BaseModel):
    lang_code: int = Field(ge=0)

class LangValueSchema(BaseModel):
    value: str = Field(min_length=1, max_length=100, example="english")

class LangAbbrSchema(BaseModel):
    abbreviation: str = Field(min_length=3, max_length=3, example="eng")

class IsUILangSchema(BaseModel):
    is_ui_lang: bool = Field(default=False)


class LanguageSchema(
    LangValueSchema,
    LangAbbrSchema,
    IsUILangSchema
):
    pass


class EditLanguageSchema(
    LanguageSchema,
    LangCodeSchema
):
    pass
