from pydantic import BaseModel, Field
from app.dictionary.schemas import WordCodeScheme, LangCodeScheme
from app.tutorial.type.schemas import TypeCodeScheme


class ThemeCodeScheme(BaseModel):
    theme_code: int = Field(ge=0)

class ThemeValueScheme(BaseModel):
    value: str = Field(min_length=1, max_length=256, example="New theme")


class AddTutorialThemeScheme(
    LangCodeScheme,
    ThemeValueScheme,
    TypeCodeScheme
):
    pass


class EditTutorialThemeScheme(
    ThemeValueScheme,
    TypeCodeScheme,
    ThemeCodeScheme,
    WordCodeScheme,
    LangCodeScheme
):
    pass


class GetTutorialThemeScheme(
    ThemeCodeScheme,
    ThemeValueScheme,
    TypeCodeScheme,
    WordCodeScheme
):
    pass
