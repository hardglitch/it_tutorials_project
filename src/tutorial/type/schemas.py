from pydantic import BaseModel, Field


class TutorialTypeScheme(BaseModel):
    code: int = Field(gt=-1)
    word_code: int = Field(gt=-1)
