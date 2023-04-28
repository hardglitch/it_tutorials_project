from pydantic import BaseModel, Field
from src.language.schemas import LangCodeScheme


class WordCodeScheme(BaseModel):
    word_code: int = Field(ge=0)

class ValueScheme(BaseModel):
    value: str = Field(min_length=1, max_length=256, example="new word")


class AddWordToDictionaryScheme(
    LangCodeScheme,
    ValueScheme
):
    pass


class EditDictionaryScheme(
    WordCodeScheme,
    LangCodeScheme,
    ValueScheme
):
    pass
