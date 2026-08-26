from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.skill import Skill
from app.models.student_profile import StudentSkill
from app.models.student_profile import StudentProfile

from app.schemas.student_skill import (
    StudentSkillCreate,
    StudentSkillUpdate,
    StudentSkillResponse
)
from app.schemas import skill
from app.schemas import student_skill


router = APIRouter(
    prefix="/profiles/me/skills",
    tags=["Student Skills"]
)

@router.post(
    "",
    response_model=StudentSkillResponse,
    status_code=201
)
def add_student_skill(
    skill_data: StudentSkillCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = (
        db.query(StudentProfile)
        .filter(
            StudentProfile.user_id == current_user.id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )

    skill = (
        db.query(Skill)
        .filter(
            Skill.id == skill_data.skill_id
        )
        .first()
    )

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    existing = (
        db.query(StudentSkill)
        .filter(
            StudentSkill.student_profile_id == profile.id,
            StudentSkill.skill_id == skill_data.skill_id
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Student already has this skill"
        )

    student_skill = StudentSkill(
        student_profile_id=profile.id,
        skill_id=skill_data.skill_id,
        proficiency=skill_data.proficiency,
        experience_months=skill_data.experience_months
    )

    db.add(student_skill)
    db.commit()
    db.refresh(student_skill)

    return student_skill

@router.post(
    "",
    response_model=StudentSkillResponse,
    status_code=201
)
def add_student_skill(
    skill_data: StudentSkillCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = (
        db.query(StudentProfile)
        .filter(
            StudentProfile.user_id == current_user.id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )

    skill = (
        db.query(Skill)
        .filter(
            Skill.id == skill_data.skill_id
        )
        .first()
    )

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    existing = (
        db.query(StudentSkill)
        .filter(
            StudentSkill.student_profile_id == profile.id,
            StudentSkill.skill_id == skill_data.skill_id
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Student already has this skill"
        )

    student_skill = StudentSkill(
        student_profile_id=profile.id,
        skill_id=skill_data.skill_id,
        proficiency=skill_data.proficiency,
        experience_months=skill_data.experience_months
    )

    db.add(student_skill)
    db.commit()
    db.refresh(student_skill)

    return student_skill

@router.get(
    "",
    response_model=list[StudentSkillResponse]
)
def get_my_skills(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = (
        db.query(StudentProfile)
        .filter(
            StudentProfile.user_id == current_user.id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )

    return (
        db.query(StudentSkill)
        .filter(
            StudentSkill.student_profile_id == profile.id
        )
        .all()
    )

@router.put(
    "/{skill_id}",
    response_model=StudentSkillResponse
)
def update_student_skill(
    skill_id: int,
    skill_data: StudentSkillUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = (
        db.query(StudentProfile)
        .filter(
            StudentProfile.user_id == current_user.id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )

        student_skill = (
        db.query(StudentSkill)
        .filter(
            StudentSkill.id == skill_id,
            StudentSkill.student_profile_id == profile.id
        )
        .first()
    )

    if not student_skill:
        raise HTTPException(
            status_code=404,
            detail="Student skill not found"
        )

        update_data = skill_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(student_skill, field, value)

    db.commit()
    db.refresh(student_skill)

    return student_skill

@router.delete(
    "/{skill_id}",
    status_code=204
)
def delete_student_skill(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = (
        db.query(StudentProfile)
        .filter(
            StudentProfile.user_id == current_user.id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )

    student_skill = (
        db.query(StudentSkill)
        .filter(
            StudentSkill.id == skill_id,
            StudentSkill.student_profile_id == profile.id
        )
        .first()
    )

    if not student_skill:
        raise HTTPException(
            status_code=404,
            detail="Student skill not found"
        )

    db.delete(student_skill)
    db.commit()