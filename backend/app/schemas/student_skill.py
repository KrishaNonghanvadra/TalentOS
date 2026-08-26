from pydantic import BaseModel, Field


class StudentSkillCreate(BaseModel):
    skill_id: int = Field(
        gt=0
    )

    proficiency: float = Field(
        ge=0,
        le=10
    )

    experience_months: int | None = Field(
        default=None,
        ge=0
    )


class StudentSkillUpdate(BaseModel):
    proficiency: float | None = Field(
        default=None,
        ge=0,
        le=10
    )

    experience_months: int | None = Field(
        default=None,
        ge=0
    )


class StudentSkillResponse(BaseModel):
    id: int
    student_profile_id: int
    skill_id: int
    proficiency: float
    experience_months: int | None

    class Config:
        from_attributes = True