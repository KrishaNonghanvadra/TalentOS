from pydantic import BaseModel, Field, HttpUrl
from typing import Optional


class StudentProfileCreate(BaseModel):
    full_name: str = Field(
        min_length=2,
        max_length=100
    )

    phone: Optional[str] = Field(
        default=None,
        max_length=20
    )

    college: Optional[str] = Field(
        default=None,
        max_length=200
    )

    degree: Optional[str] = Field(
        default=None,
        max_length=100
    )

    branch: Optional[str] = Field(
        default=None,
        max_length=100
    )

    semester: Optional[int] = Field(
        default=None,
        ge=1,
        le=12
    )

    cgpa: Optional[float] = Field(
        default=None,
        ge=0,
        le=10
    )

    graduation_year: Optional[int] = Field(
        default=None,
        ge=2000,
        le=2100
    )

    github_url: Optional[HttpUrl] = None

    linkedin_url: Optional[HttpUrl] = None

    bio: Optional[str] = Field(
        default=None,
        max_length=1000
    )

class StudentProfileResponse(BaseModel):
    id: int
    user_id: int

    full_name: str
    phone: Optional[str]

    college: Optional[str]
    degree: Optional[str]
    branch: Optional[str]

    semester: Optional[int]
    cgpa: Optional[float]
    graduation_year: Optional[int]

    github_url: Optional[HttpUrl]
    linkedin_url: Optional[HttpUrl]

    bio: Optional[str]

    class Config:
        from_attributes = True

class StudentProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    phone: Optional[str] = Field(
        default=None,
        max_length=20
    )

    college: Optional[str] = Field(
        default=None,
        max_length=200
    )

    degree: Optional[str] = Field(
        default=None,
        max_length=100
    )

    branch: Optional[str] = Field(
        default=None,
        max_length=100
    )

    semester: Optional[int] = Field(
        default=None,
        ge=1,
        le=12
    )

    cgpa: Optional[float] = Field(
        default=None,
        ge=0,
        le=10
    )

    graduation_year: Optional[int] = Field(
        default=None,
        ge=2000,
        le=2100
    )

    github_url: Optional[HttpUrl] = None

    linkedin_url: Optional[HttpUrl] = None

    bio: Optional[str] = Field(
        default=None,
        max_length=1000
    )