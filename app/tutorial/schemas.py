from typing import Annotated
from pydantic import BaseModel, HttpUrl, validator
from app.dictionary.schemas import DictValue
from app.language.schemas import LangCode, LangValue
from app.tools import remove_dup_spaces
from app.tutorial.dist_type.schemas import DistTypeCode
from app.tutorial.theme.schemas import ThemeCode
from app.tutorial.type.schemas import TypeCode
from app.user.schemas import UserID, UserName


class TutorialIDSchema(BaseModel):
    id: int | None = None

TutorialID = Annotated[int, TutorialIDSchema]


class TitleSchema(BaseModel):
    title: str | None = None

class ValidTitleSchema(BaseModel):
    title: str | None = None

    @validator("title")
    def check_value(cls, value: str):
        return value if 1 < len(value := remove_dup_spaces(value)) <= 1024 else None

Title = Annotated[str, TitleSchema]
ValidTitle = Annotated[str, ValidTitleSchema]


class DescriptionSchema(BaseModel):
    description: str | None = None

class ValidDescriptionSchema(BaseModel):
    description: str | None = None

    @validator("description")
    def check_value(cls, value: str):
        return value if 1 < len(value := remove_dup_spaces(value)) <= 10000 else None

Description = Annotated[str, DescriptionSchema]
ValidDescription = Annotated[str, ValidDescriptionSchema]


class TutorialSchema(
    TutorialIDSchema,
    TitleSchema,
    DescriptionSchema,
):
    type_code: TypeCode
    theme_code: ThemeCode
    lang_code: LangCode
    dist_type_code: DistTypeCode
    source_link: HttpUrl
    who_added_id: UserID | None = None


class DecodedTutorialSchema(
    TitleSchema,
    DescriptionSchema,
):
    type: DictValue
    theme: DictValue
    language: LangValue
    dist_type: DictValue
    source_link: HttpUrl
    who_added: UserName
