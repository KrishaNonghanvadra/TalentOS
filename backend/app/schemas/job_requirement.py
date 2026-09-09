from pydantic import BaseModel, Field


class JobRequirementCreate(BaseModel):
    skill_id: int = Field(gt=0)

    required_proficiency: float = Field(
        ge=0,
        le=10
    )


class JobRequirementUpdate(BaseModel):
    required_proficiency: float = Field(
        ge=0,
        le=10
    )


class JobRequirementResponse(BaseModel):
    id: int
    job_id: int
    skill_id: int
    required_proficiency: float

    class Config:
        from_attributes = True