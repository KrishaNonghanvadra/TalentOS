from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.student_profile import StudentProfile

from app.schemas.github import GitHubAnalysisResponse

from app.services.github_service import analyze_github
from app.services.github_skill_service import update_student_skills_from_github

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


@router.post("/sync-skills")
def sync_github_skills(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
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

    if not student_profile.github_url:
        raise HTTPException(
            status_code=400,
            detail="GitHub URL is not added to the student profile"
        )

    try:
        github_analysis = analyze_github(
            student_profile.github_url
        )

        result = update_student_skills_from_github(
            db,
            student_profile.id,
            github_analysis
        )

        return {
            "message": "GitHub skills synchronized successfully",
            "github_analysis": github_analysis,
            "skill_sync": result
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Unable to synchronize GitHub skills"
        )