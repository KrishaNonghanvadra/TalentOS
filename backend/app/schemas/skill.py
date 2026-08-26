from pydantic import BaseModel, Field
from typing import Optional


class SkillCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )

    category: Optional[str] = Field(
        default=None,
        max_length=100
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )


class SkillResponse(BaseModel):
    id: int
    name: str
    category: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True