from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.student_profile import StudentProfile

from app.schemas.job_recommendation import JobRecommendationResponse

from app.services.job_recommendation_service import get_recommended_jobs


router = APIRouter(
    prefix="/jobs",
    tags=["Job Recommendations"]
)


@router.get(
    "/recommended",
    response_model=list[JobRecommendationResponse]
)
def recommend_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student_profile = (
        db.query(StudentProfile)
        .filter(StudentProfile.user_id == current_user.id)
        .first()
    )

    if not student_profile:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )

    return get_recommended_jobs(
        db,
        student_profile
    )