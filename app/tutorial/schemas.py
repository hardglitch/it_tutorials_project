from typing import Annotated, List

from fastapi import Query
from pydantic import BaseModel, HttpUrl, validator
from ..dictionary.schemas import DictValue
from ..language.schemas import LangCode, LangValue
from ..tools import remove_dup_spaces
from ..tutorial.dist_type.schemas import DistTypeCode
from ..tutorial.theme.schemas import ThemeCode
from ..tutorial.type.schemas import TypeCode
from ..user.schemas import UserID, UserName


class TutorialIDSchema(BaseModel):
    id: int | None = None

TutorialID = Annotated[int, TutorialIDSchema]


class TitleSchema(BaseModel):
    title: str | None = None

class ValidTitleSchema(BaseModel):
    title: str | None = None

    @validator("title")
    def check_value(cls, value: str):
        return value if 1 < len(value := remove_dup_spaces(value)) <= 256 else None

Title = Annotated[str, TitleSchema]
ValidTitle = Annotated[str, ValidTitleSchema]


class DescriptionSchema(BaseModel):
    description: str | None = None

class ValidDescriptionSchema(BaseModel):
    description: str | None = None

    @validator("description")
    def check_value(cls, value: str):
        return value if 1 < len(value := remove_dup_spaces(value)) <= 1024 else None

Description = Annotated[str, DescriptionSchema]
ValidDescription = Annotated[str, ValidDescriptionSchema]


class PaginationSchema(BaseModel):
    page: int = 1

Pagination = Annotated[int, PaginationSchema]


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
    who_added_is_active: bool | None = None


class DecodedTutorialSchema(
    TutorialSchema
):
    type: DictValue
    theme: DictValue
    language: LangValue
    dist_type: DictValue
    who_added: UserName


class TutorialListSchema(BaseModel):
    tutorials: List[DecodedTutorialSchema]
    total_count: int
