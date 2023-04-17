from pydantic import BaseModel, Field
from src.constants.constants import Language, ShareType


class TutorialScheme(BaseModel):
    title: str
    type: str
    theme: str
    description: str
    language: Language = Field(default=Language.rus, alias=Language.__name__)
    source_link: str
    share_type: ShareType = Field(default=ShareType.free, alias=ShareType.__name__)


class DecryptedTutorialScheme(BaseModel):
    title: str
    type: str
    theme: str
    description: str
    language: str
    source_link: str
    share_type: str
