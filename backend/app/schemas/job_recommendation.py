from typing import List
from pydantic import BaseModel

from app.schemas.job_matching import SkillMatch, SkillGap


class JobRecommendationResponse(BaseModel):
    job_id: int
    job_title: str
    company: str
    match_percentage: float
    skill_readiness: float
    matched_skills: List[SkillMatch]
    skill_gaps: List[SkillGap]