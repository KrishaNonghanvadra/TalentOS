from typing import List
from pydantic import BaseModel


class LearningTask(BaseModel):
    skill: str
    priority: str
    topic: str
    description: str


class LearningRoadmapResponse(BaseModel):
    job_id: int
    job_title: str
    company: str
    tasks: List[LearningTask]