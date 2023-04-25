from pydantic import BaseModel, Field
from src.dictionary.schemas import DictionaryScheme


class AddTutorialThemeScheme(DictionaryScheme):
    type_code: int = Field(ge=0)


class EditTutorialThemeScheme(DictionaryScheme):
    code: int = Field(ge=0)
    type_code: int | None = Field(ge=0)


class ReadTutorialThemeScheme(BaseModel):
    code: int = Field(ge=0)
    value: str = Field(min_length=1, max_length=256)
    type_code: int = Field(ge=0)
