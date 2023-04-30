from pydantic import BaseModel, Field

class LangCodeScheme(BaseModel):
    lang_code: int = Field(ge=0)

class LangValueScheme(BaseModel):
    value: str = Field(min_length=1, max_length=100, example="english")

class LangAbbrScheme(BaseModel):
    abbreviation: str = Field(min_length=3, max_length=3, example="eng")

class IsUILangScheme(BaseModel):
    is_ui_lang: bool = Field(default=False)


class LanguageScheme(
    LangValueScheme,
    LangAbbrScheme,
    IsUILangScheme
):
    pass


class EditLanguageScheme(
    LanguageScheme,
    LangCodeScheme
):
    pass
