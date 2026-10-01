from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.student_profile import StudentProfile

from app.schemas.readiness import CareerReadinessResponse

from app.services.readiness_service import calculate_career_readiness


router = APIRouter(
    prefix="/readiness",
    tags=["Career Readiness"]
)


@router.get(
    "/me",
    response_model=CareerReadinessResponse
)
def get_career_readiness(
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

    return calculate_career_readiness(
        db,
        student_profile
    )