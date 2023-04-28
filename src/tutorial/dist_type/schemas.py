from pydantic import BaseModel, Field


class DistTypeCodeScheme(BaseModel):
    code: int = Field(ge=0)


class GetTutorialDistributionTypeScheme(
    DistTypeCodeScheme
):
    value: str = Field(min_length=1, max_length=256, example="Free")
