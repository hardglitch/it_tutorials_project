from pydantic import BaseModel, Field


class TypeCodeScheme(BaseModel):
    type_code: int = Field(ge=0)

class ValueScheme(BaseModel):
    value: str = Field(min_length=1, max_length=256, example="New type")


class ReadTutorialTypeScheme(
    TypeCodeScheme,
    ValueScheme
):
    pass
