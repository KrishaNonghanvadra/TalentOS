from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.job import Job
from app.models.student_profile import StudentProfile
from app.models.user import User
from app.schemas.job_matching import JobMatchResponse
from app.services.job_matching_service import calculate_job_match
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/jobs",
    tags=["Job Matching"]
)

@router.get(
    "/{job_id}/match",
    response_model=JobMatchResponse
)
def match_student_with_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    student_profile = db.query(
        StudentProfile
    ).filter(
        StudentProfile.user_id == current_user.id
    ).first()

    if not student_profile:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )

    result = calculate_job_match(
        db,
        student_profile,
        job
    )

    return result