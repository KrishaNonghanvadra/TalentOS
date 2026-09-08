from pydantic import BaseModel, Field
from typing import Optional


class JobCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    company: str = Field(min_length=2, max_length=200)
    description: Optional[str] = None
    location: Optional[str] = Field(default=None, max_length=200)
    job_type: Optional[str] = Field(default=None, max_length=50)
    minimum_cgpa: Optional[float] = Field(
        default=None,
        ge=0,
        le=10
    )


class JobUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=200
    )
    company: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=200
    )
    description: Optional[str] = None
    location: Optional[str] = Field(
        default=None,
        max_length=200
    )
    job_type: Optional[str] = Field(
        default=None,
        max_length=50
    )
    minimum_cgpa: Optional[float] = Field(
        default=None,
        ge=0,
        le=10
    )


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    description: Optional[str]
    location: Optional[str]
    job_type: Optional[str]
    minimum_cgpa: Optional[float]

    class Config:
        from_attributes = True