from typing import Annotated
from pydantic import BaseModel, Field, HttpUrl
from app.language.schemas import LangCodeScheme, LangValueScheme
from app.tutorial.dist_type.schemas import DistTypeCodeScheme, DistTypeValueScheme
from app.tutorial.theme.schemas import ThemeCodeScheme, ThemeValueScheme
from app.tutorial.type.schemas import TypeCodeScheme, TypeValueScheme
from app.user.schemas import UserIDScheme, UserNameScheme


class TutorialIDScheme(BaseModel):
    id: int = Field(ge=0)

class TitleScheme(BaseModel):
    title: str = Field(min_length=1, max_length=1024, example="New Title")

class DescriptionScheme(BaseModel):
    description: str = Field(min_length=1, max_length=10000, example="This tutorial is great!")

class SourseLinkScheme(BaseModel):
    source_link: HttpUrl = Field(example="https://greattutor.com/777")


class EditTutorialScheme(
    TitleScheme,
    DescriptionScheme,
    SourseLinkScheme
):
    type_code: Annotated[int, TypeCodeScheme]
    theme_code: Annotated[int, ThemeCodeScheme]
    lang_code: Annotated[int, LangCodeScheme]
    dist_type_code: Annotated[int, DistTypeCodeScheme]


class AddTutorialScheme(EditTutorialScheme):
    who_added_id: Annotated[int, UserIDScheme]


class GetDecodedTutorialScheme(
    TitleScheme,
    DescriptionScheme,
    SourseLinkScheme
):
    type: Annotated[str, TypeValueScheme]
    theme: Annotated[str, ThemeValueScheme]
    language: Annotated[str, LangValueScheme]
    dist_type: Annotated[str, DistTypeValueScheme]
    who_added: Annotated[str, UserNameScheme]
