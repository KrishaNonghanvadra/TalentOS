from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_recruiter

from app.models.user import User

from app.schemas.recruiter import (
    RecruiterSearchRequest,
    CandidateSearchResult
)

from app.services.recruiter_service import search_candidates

from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse, JobUpdate

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
    current_user: User = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):

    return search_candidates(
        db,
        request.skills,
        request.minimum_match_percentage
    )


@router.post("/jobs", response_model=JobResponse, status_code=201)
def create_recruiter_job(
    job_data: JobCreate,
    current_user: User = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    job = Job(
        **job_data.model_dump(),
        recruiter_id=current_user.id
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


@router.get("/jobs", response_model=list[JobResponse])
def get_my_jobs(
    current_user: User = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    return (
        db.query(Job)
        .filter(Job.recruiter_id == current_user.id)
        .order_by(Job.id.desc())
        .all()
    )


@router.put("/jobs/{job_id}", response_model=JobResponse)
def update_recruiter_job(
    job_id: int,
    job_data: JobUpdate,
    current_user: User = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.recruiter_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found or you do not own this job"
        )

    update_data = job_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)

    return job


@router.delete("/jobs/{job_id}", status_code=204)
def delete_recruiter_job(
    job_id: int,
    current_user: User = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.recruiter_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found or you do not own this job"
        )

    db.delete(job)
    db.commit()
