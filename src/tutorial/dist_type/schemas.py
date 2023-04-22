from pydantic import BaseModel


class TutorialDistributionTypeScheme(BaseModel):
    code: int
    word_code: int
