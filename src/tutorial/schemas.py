from pydantic import BaseModel, Field


class TutorialScheme(BaseModel):
    title: str = Field(min_length=1, max_length=1024)
    type: int
    theme: int
    description: str = Field(min_length=1, max_length=10000)
    language: int
    source_link: str = Field(min_length=1, max_length=1024)
    share_type: int
    who_added: int | None = None


class DecryptedTutorialScheme(TutorialScheme):
    type: str = Field(min_length=1, max_length=256)
    theme: str = Field(min_length=1, max_length=256)
    language: str = Field(min_length=1, max_length=100)
    share_type: str = Field(min_length=1, max_length=100)
    who_added: str = Field(min_length=1, max_length=256)
