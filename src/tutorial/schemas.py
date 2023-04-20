from pydantic import BaseModel, Field
from src.constants.constants import ShareType, UILanguage


class TutorialScheme(BaseModel):
    title: str = Field(min_length=1, max_length=1024)
    type: int   # from DB
    theme: int  # from DB
    description: str = Field(min_length=1, max_length=10000)
    language: int = Field(default=0)
    source_link: str = Field(min_length=1, max_length=1024)
    share_type: int = Field(default=ShareType.free)


class DecryptedTutorialScheme(TutorialScheme):
    type: str = Field(min_length=1, max_length=256)
    theme: str = Field(min_length=1, max_length=256)
    language: str = Field(min_length=1, max_length=100)
    share_type: str = Field(min_length=1, max_length=100)


# class TutorialThemeScheme(BaseModel):
#     eng = Field(min_length=1, max_length=256)
#     rus = Field(min_length=1, max_length=256)
#     ukr = Field(min_length=1, max_length=256)
