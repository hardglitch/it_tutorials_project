from pydantic import BaseModel, Field


class DistTypeCodeScheme(BaseModel):
    dist_type_code: int = Field(ge=0)

class DistTypeValueScheme(BaseModel):
    dist_type_value: str = Field(min_length=1, max_length=256, example="Free")


class GetTutorialDistTypeScheme(
    DistTypeCodeScheme,
    DistTypeValueScheme
):
    pass