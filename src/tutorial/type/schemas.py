from pydantic import BaseModel


class TutorialTypeScheme(BaseModel):
    code: int
    word_code: int
