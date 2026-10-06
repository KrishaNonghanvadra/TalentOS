from typing import List
from pydantic import BaseModel, Field


class RecruiterSkillRequirement(BaseModel):
    skill_id: int = Field(gt=0)
    required_proficiency: float = Field(
        ge=0,
        le=10
    )


class RecruiterSearchRequest(BaseModel):
    skills: List[RecruiterSkillRequirement]


class CandidateSkillMatch(BaseModel):
    skill_id: int
    skill_name: str
    student_proficiency: float
    required_proficiency: float
    score: float


class CandidateSearchResult(BaseModel):
    student_profile_id: int
    full_name: str | None
    college: str | None
    branch: str | None
    cgpa: float | None
    github_url: str | None
    match_percentage: float
    matched_skills: List[CandidateSkillMatch]