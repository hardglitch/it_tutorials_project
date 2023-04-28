from pydantic import BaseModel, Field
from src.dictionary.schemas import WordCodeScheme, LangCodeScheme
from src.tutorial.type.schemas import TypeCodeScheme


class ThemeCodeScheme(BaseModel):
    theme_code: int = Field(ge=0)

class ValueScheme(BaseModel):
    value: str = Field(min_length=1, max_length=256, example="New theme")


class AddTutorialThemeScheme(
    LangCodeScheme,
    ValueScheme,
    TypeCodeScheme
):
    pass


class EditTutorialThemeScheme(
    ValueScheme,
    TypeCodeScheme,
    ThemeCodeScheme,
    WordCodeScheme,
    LangCodeScheme
):
    pass


class GetTutorialThemeScheme(
    ThemeCodeScheme,
    ValueScheme,
    TypeCodeScheme,
    WordCodeScheme
):
    pass
