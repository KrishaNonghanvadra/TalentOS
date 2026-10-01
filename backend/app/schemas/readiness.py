from pydantic import BaseModel

class CareerReadinessResponse(BaseModel):
    overall_score: float
    skill_score: float
    profile_score: float
    resume_score: float
    github_score: float