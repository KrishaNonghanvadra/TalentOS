from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.recruiter import (
    RecruiterSearchRequest,
    CandidateSearchResult
)

from app.services.recruiter_service import search_candidates


router = APIRouter(
    prefix="/recruiter",
    tags=["Recruiter"]
)


@router.post(
    "/search",
    response_model=list[CandidateSearchResult]
)
def recruiter_search(
    request: RecruiterSearchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return search_candidates(
        db,
        request.skills
    )