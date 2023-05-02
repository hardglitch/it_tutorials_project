from pydantic import BaseModel, Field
from app.language.schemas import LangCodeSchema


class WordCodeSchema(BaseModel):
    word_code: int = Field(ge=0)

class ValueSchema(BaseModel):
    value: str = Field(min_length=1, max_length=256, example="new word")


class AddWordToDictionarySchema(
    LangCodeSchema,
    ValueSchema
):
    pass


class EditDictionarySchema(
    WordCodeSchema,
    LangCodeSchema,
    ValueSchema
):
    pass
