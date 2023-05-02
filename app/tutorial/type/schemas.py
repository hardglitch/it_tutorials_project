from pydantic import BaseModel, Field


class TypeCodeSchema(BaseModel):
    type_code: int = Field(ge=0)

class TypeValueSchema(BaseModel):
    value: str = Field(min_length=1, max_length=256, example="New type")


class GetTutorialTypeSchema(
    TypeCodeSchema,
    TypeValueSchema
):
    pass
