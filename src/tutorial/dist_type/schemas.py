from pydantic import BaseModel, Field


class GetTutorialDistributionTypeScheme(BaseModel):
    code: int = Field(ge=0)
    value: str = Field(min_length=1, max_length=256, example="Free")
