from pydantic import BaseModel, Field


class LanguageScheme(BaseModel):
    abbreviation: str = Field(min_length=3, max_length=3)
    value: str = Field(max_length=100)
    is_ui_lang: bool = Field(default=False)


class EditLanguageScheme(LanguageScheme):
    abbreviation: str | None = Field(min_length=3, max_length=3, default=None)
    value: str | None = Field(max_length=100, default=None)
    is_ui_lang: bool | None = Field(default=None)
