from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse, JobUpdate


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

@router.post(
    "",
    response_model=JobResponse,
    status_code=201
)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db)
):
    job = Job(
        title=job_data.title,
        company=job_data.company,
        description=job_data.description,
        location=job_data.location,
        job_type=job_data.job_type,
        minimum_cgpa=job_data.minimum_cgpa
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job

@router.get(
    "",
    response_model=list[JobResponse]
)
def get_jobs(
    db: Session = Depends(get_db)
):
    jobs = db.query(Job).all()

    return jobs

@router.get(
    "/{job_id}",
    response_model=JobResponse
)
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job

@router.put(
    "/{job_id}",
    response_model=JobResponse
)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    update_data = job_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(job, key, value)

    db.commit()
    db.refresh(job)

    return job

@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    db.delete(job)
    db.commit()

    return {
        "message": "Job deleted successfully"
    }