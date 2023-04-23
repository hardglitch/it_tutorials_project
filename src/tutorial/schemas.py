from pydantic import BaseModel, Field


class TutorialScheme(BaseModel):
    title: str = Field(min_length=1, max_length=1024)
    type: int = Field(gt=-1)
    theme: int = Field(gt=-1)
    description: str = Field(min_length=1, max_length=10000)
    language: int = Field(gt=-1)
    source_link: str = Field(min_length=1, max_length=1024)
    share_type: int = Field(gt=-1)
    who_added: int | None = Field(gt=-1, default=None)


class DecryptedTutorialScheme(TutorialScheme):
    type: str = Field(min_length=1, max_length=256)
    theme: str = Field(min_length=1, max_length=256)
    language: str = Field(min_length=1, max_length=100)
    share_type: str = Field(min_length=1, max_length=100)
    who_added: str = Field(min_length=1, max_length=256)
