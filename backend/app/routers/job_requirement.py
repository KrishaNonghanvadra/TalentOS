from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.job import Job
from app.models.job_requirement import JobRequirement
from app.models.skill import Skill
from app.schemas.job_requirement import (
    JobRequirementCreate,
    JobRequirementUpdate,
    JobRequirementResponse
)


router = APIRouter(
    prefix="/jobs",
    tags=["Job Requirements"]
)

@router.post(
    "/{job_id}/requirements",
    response_model=JobRequirementResponse,
    status_code=201
)
def create_job_requirement(
    job_id: int,
    requirement_data: JobRequirementCreate,
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

    skill = db.query(Skill).filter(
        Skill.id == requirement_data.skill_id
    ).first()

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    existing_requirement = db.query(
        JobRequirement
    ).filter(
        JobRequirement.job_id == job_id,
        JobRequirement.skill_id == requirement_data.skill_id
    ).first()

    if existing_requirement:
        raise HTTPException(
            status_code=400,
            detail="This skill is already required for this job"
        )

    requirement = JobRequirement(
        job_id=job_id,
        skill_id=requirement_data.skill_id,
        required_proficiency=requirement_data.required_proficiency
    )

    db.add(requirement)
    db.commit()
    db.refresh(requirement)

    return requirement

@router.get(
    "/{job_id}/requirements",
    response_model=list[JobRequirementResponse]
)
def get_job_requirements(
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

    requirements = db.query(
        JobRequirement
    ).filter(
        JobRequirement.job_id == job_id
    ).all()

    return requirements

@router.put(
    "/requirements/{requirement_id}",
    response_model=JobRequirementResponse
)
def update_job_requirement(
    requirement_id: int,
    requirement_data: JobRequirementUpdate,
    db: Session = Depends(get_db)
):
    requirement = db.query(
        JobRequirement
    ).filter(
        JobRequirement.id == requirement_id
    ).first()

    if not requirement:
        raise HTTPException(
            status_code=404,
            detail="Job requirement not found"
        )

    requirement.required_proficiency = (
        requirement_data.required_proficiency
    )

    db.commit()
    db.refresh(requirement)

    return requirement

@router.delete(
    "/requirements/{requirement_id}"
)
def delete_job_requirement(
    requirement_id: int,
    db: Session = Depends(get_db)
):
    requirement = db.query(
        JobRequirement
    ).filter(
        JobRequirement.id == requirement_id
    ).first()

    if not requirement:
        raise HTTPException(
            status_code=404,
            detail="Job requirement not found"
        )

    db.delete(requirement)
    db.commit()

    return {
        "message": "Job requirement deleted successfully"
    }