from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.skill import Skill
from app.schemas.skill import SkillCreate, SkillResponse


router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)

@router.post(
    "",
    response_model=SkillResponse,
    status_code=201
)
def create_skill(
    skill_data: SkillCreate,
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
        name=skill_data.name,
        category=skill_data.category,
        description=skill_data.description
    )

    db.add(skill)
    db.commit()
    db.refresh(skill)

    return skill

@router.get(
    "",
    response_model=list[SkillResponse]
)
def get_skills(
    db: Session = Depends(get_db)
):
    return (
        db.query(Skill)
        .order_by(Skill.name)
        .all()
    )