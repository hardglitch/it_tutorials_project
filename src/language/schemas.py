from pydantic import BaseModel, Field

class LangCodeScheme(BaseModel):
    code: int = Field(ge=0)


class LanguageScheme(BaseModel):
    abbreviation: str = Field(min_length=3, max_length=3, examples="eng")
    value: str = Field(min_length=1, max_length=100, example="english")
    is_ui_lang: bool = Field(default=False)


class EditLanguageScheme(
    LanguageScheme,
    LangCodeScheme
):
    pass
