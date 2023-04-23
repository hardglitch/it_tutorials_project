from pydantic import BaseModel, Field


class DictionaryScheme(BaseModel):
    word_code: int | None = Field(gt=-1)
    lang_code: int = Field(gt=-1)
    value: str = Field(min_length=1, max_length=256)


class EditDictionaryScheme(DictionaryScheme):
    word_code: int | None = Field(gt=-1, default=None)
    lang_code: int | None = Field(gt=-1, default=None)
    value: str = Field(min_length=1, max_length=256)
