from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.student_profile import StudentProfile
from app.models.job import Job

from app.schemas.roadmap import LearningRoadmapResponse

from app.services.roadmap_service import generate_learning_roadmap


router = APIRouter(
    prefix="/roadmap",
    tags=["Learning Roadmap"]
)


@router.get(
    "/jobs/{job_id}",
    response_model=LearningRoadmapResponse
)
def get_learning_roadmap(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    student_profile = (
        db.query(StudentProfile)
        .filter(
            StudentProfile.user_id == current_user.id
        )
        .first()
    )

    if not student_profile:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )

    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return generate_learning_roadmap(
        db,
        student_profile,
        job
    )