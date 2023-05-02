from pydantic import BaseModel, Field
from app.dictionary.schemas import WordCodeSchema, LangCodeSchema
from app.tutorial.type.schemas import TypeCodeSchema


class ThemeCodeSchema(BaseModel):
    theme_code: int = Field(ge=0)

class ThemeValueSchema(BaseModel):
    value: str = Field(min_length=1, max_length=256, example="New theme")


class AddTutorialThemeSchema(
    LangCodeSchema,
    ThemeValueSchema,
    TypeCodeSchema
):
    pass


class EditTutorialThemeSchema(
    ThemeValueSchema,
    TypeCodeSchema,
    ThemeCodeSchema,
    WordCodeSchema,
    LangCodeSchema
):
    pass


class GetTutorialThemeSchema(
    ThemeCodeSchema,
    ThemeValueSchema,
    TypeCodeSchema,
    WordCodeSchema
):
    pass
