from pydantic import BaseModel


class TutorialThemeScheme(BaseModel):
    code: int
    word_code: int
