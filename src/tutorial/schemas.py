from pydantic import BaseModel
from src.db_const import Language, ShareType


class TutorialScheme(BaseModel):
    title: str
    type: str
    theme: str
    description: str
    language: int
    source_link: str
    share_type: int


class DecryptedTutorialScheme(BaseModel):
    title: str
    type: str
    theme: str
    description: str
    language: str
    source_link: str
    share_type: str
