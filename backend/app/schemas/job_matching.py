from pydantic import BaseModel
from typing import List


class SkillMatch(BaseModel):
    skill: str
    student_proficiency: float
    required_proficiency: float


class SkillGap(BaseModel):
    skill: str
    student_proficiency: float
    required_proficiency: float
    gap: float
    priority: str


class JobMatchResponse(BaseModel):
    job_id: int
    job_title: str
    company: str

    match_percentage: float
    skill_readliness: float

    matched_skills: List[SkillMatch]
    skill_gaps: List[SkillGap]
    