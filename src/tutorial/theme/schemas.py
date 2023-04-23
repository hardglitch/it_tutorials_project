from pydantic import BaseModel, Field


class TutorialThemeScheme(BaseModel):
    code: int = Field(gt=-1)
    word_code: int = Field(gt=-1)
    type_code: int = Field(gt=-1)
