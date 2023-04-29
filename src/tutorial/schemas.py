from typing import Annotated
from pydantic import BaseModel, Field, HttpUrl
from src.language.schemas import LangCodeScheme, LangValueScheme
from src.tutorial.dist_type.schemas import DistTypeCodeScheme, DistTypeValueScheme
from src.tutorial.theme.schemas import ThemeCodeScheme, ThemeValueScheme
from src.tutorial.type.schemas import TypeCodeScheme, TypeValueScheme
from src.user.schemas import UserIDScheme, UserNameScheme


class TutorialIDScheme(BaseModel):
    id: int = Field(ge=0)


class EditTutorialScheme(BaseModel):
    title: str = Field(min_length=1, max_length=1024, example="New Title")
    type: Annotated[int, TypeCodeScheme]
    theme: Annotated[int, ThemeCodeScheme]
    language: Annotated[int, LangCodeScheme]
    description: str = Field(min_length=1, max_length=10000, example="This tutorial is great!")
    dist_type: Annotated[int, DistTypeCodeScheme]
    source_link: HttpUrl = Field(example="https://greattutor.com/777")


class AddTutorialScheme(EditTutorialScheme):
    who_added: Annotated[int, UserIDScheme]


class GetTutorialScheme(AddTutorialScheme):
    type: Annotated[str, TypeValueScheme]
    theme: Annotated[str, ThemeValueScheme]
    language: Annotated[str, LangValueScheme]
    dist_type: Annotated[str, DistTypeValueScheme]
    who_added: Annotated[str, UserNameScheme]
