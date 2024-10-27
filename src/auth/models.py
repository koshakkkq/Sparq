from pydantic import BaseModel, Field


class TestModel(BaseModel):
    id: int
    value: str = Field(min_length=1, max_length=120)

    class Config:
        from_attributes = True


class TestModelPayload(BaseModel):
    value: str = Field(min_length=1, max_length=120)
