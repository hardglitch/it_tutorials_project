from typing import Annotated
from pydantic import BaseModel, Field, HttpUrl
from app.language.schemas import LangCodeSchema, LangValueSchema
from app.tutorial.dist_type.schemas import DistTypeCodeSchema, DistTypeValueSchema
from app.tutorial.theme.schemas import ThemeCodeSchema, ThemeValueSchema
from app.tutorial.type.schemas import TypeCodeSchema, TypeValueSchema
from app.user.schemas import UserIDSchema, UserNameSchema


class TutorialIDSchema(BaseModel):
    id: int = Field(ge=0)

class TitleSchema(BaseModel):
    title: str = Field(min_length=1, max_length=1024, example="New Title")

class DescriptionSchema(BaseModel):
    description: str = Field(min_length=1, max_length=10000, example="This tutorial is great!")

class SourseLinkSchema(BaseModel):
    source_link: HttpUrl = Field(example="https://greattutor.com/777")


class EditTutorialSchema(
    TitleSchema,
    DescriptionSchema,
    SourseLinkSchema
):
    type_code: Annotated[int, TypeCodeSchema]
    theme_code: Annotated[int, ThemeCodeSchema]
    lang_code: Annotated[int, LangCodeSchema]
    dist_type_code: Annotated[int, DistTypeCodeSchema]


class AddTutorialSchema(EditTutorialSchema):
    who_added_id: Annotated[int, UserIDSchema]


class GetDecodedTutorialSchema(
    TitleSchema,
    DescriptionSchema,
    SourseLinkSchema
):
    type: Annotated[str, TypeValueSchema]
    theme: Annotated[str, ThemeValueSchema]
    language: Annotated[str, LangValueSchema]
    dist_type: Annotated[str, DistTypeValueSchema]
    who_added: Annotated[str, UserNameSchema]
