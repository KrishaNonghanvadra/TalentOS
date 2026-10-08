from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_admin

from app.models.user import User
from app.models.skill import Skill

from app.schemas.skill import (
    SkillCreate,
    SkillResponse
)
from app.models.job_requirement import JobRequirement
from app.models.student_profile import StudentSkill


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.post(
    "/skills",
    response_model=SkillResponse,
    status_code=201
)
def create_skill(
    skill_data: SkillCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):

    existing_skill = (
        db.query(Skill)
        .filter(
            Skill.name.ilike(skill_data.name)
        )
        .first()
    )

    if existing_skill:
        raise HTTPException(
            status_code=400,
            detail="Skill already exists"
        )

    skill = Skill(
        name=skill_data.name.strip(),
        category=skill_data.category,
        description=skill_data.description
    )

    db.add(skill)
    db.commit()
    db.refresh(skill)

    return skill

@router.get(
    "/skills",
    response_model=list[SkillResponse]
)
def get_all_skills(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):

    return (
        db.query(Skill)
        .order_by(Skill.name)
        .all()
    )

@router.put(
    "/skills/{skill_id}",
    response_model=SkillResponse
)
def update_skill(
    skill_id: int,
    skill_data: SkillCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):

    skill = (
        db.query(Skill)
        .filter(Skill.id == skill_id)
        .first()
    )

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    existing_skill = (
        db.query(Skill)
        .filter(
            Skill.name.ilike(skill_data.name),
            Skill.id != skill_id
        )
        .first()
    )

    if existing_skill:
        raise HTTPException(
            status_code=400,
            detail="Another skill with this name already exists"
        )

    skill.name = skill_data.name.strip()
    skill.category = skill_data.category
    skill.description = skill_data.description

    db.commit()
    db.refresh(skill)

    return skill

@router.delete(
    "/skills/{skill_id}"
)
def delete_skill(
    skill_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):

    skill = (
        db.query(Skill)
        .filter(Skill.id == skill_id)
        .first()
    )

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    student_skill_exists = (
        db.query(StudentSkill)
        .filter(
            StudentSkill.skill_id == skill_id
        )
        .first()
    )

    if student_skill_exists:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete skill because students are using it"
        )

    job_requirement_exists = (
        db.query(JobRequirement)
        .filter(
            JobRequirement.skill_id == skill_id
        )
        .first()
    )

    if job_requirement_exists:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete skill because jobs are using it"
        )

    db.delete(skill)
    db.commit()

    return {
        "message": "Skill deleted successfully"
    }