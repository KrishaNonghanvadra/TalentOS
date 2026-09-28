from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.student_profile import StudentProfile

from app.schemas.github import GitHubAnalysisResponse

from app.services.github_service import analyze_github


router = APIRouter(
    prefix="/github",
    tags=["GitHub"]
)


@router.get(
    "/analyze",
    response_model=GitHubAnalysisResponse
)
def analyze_student_github(
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

    if not student_profile.github_url:
        raise HTTPException(
            status_code=400,
            detail="GitHub URL is not added to the student profile"
        )

    try:
        return analyze_github(
            student_profile.github_url
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Unable to fetch GitHub profile"
        )