from pydantic import BaseModel, Field, HttpUrl


class TutorialScheme(BaseModel):
    title: str = Field(min_length=1, max_length=1024)
    type: int = Field(ge=0)
    theme: int = Field(ge=0)
    description: str = Field(min_length=1, max_length=10000)
    language: int = Field(ge=0)
    source_link: HttpUrl
    share_type: int = Field(ge=0)
    who_added: int | None = Field(ge=0, default=None)


class DecryptedTutorialScheme(TutorialScheme):
    type: str = Field(min_length=1, max_length=256)
    theme: str = Field(min_length=1, max_length=256)
    language: str = Field(min_length=1, max_length=100)
    share_type: str = Field(min_length=1, max_length=100)
    who_added: str = Field(min_length=1, max_length=256)
