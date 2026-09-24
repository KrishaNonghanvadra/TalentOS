from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.core.base import Base
from app.models.skill import Skill


class JobRequirement(Base):
    __tablename__ = "job_requirements"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(
        Integer,
        ForeignKey("jobs.id"),
        nullable=False
    )

    skill_id = Column(
        Integer,
        ForeignKey("skills.id"),
        nullable=False
    )

    required_proficiency = Column(
        Float,
        nullable=False
    )

    job = relationship(
        "Job",
        back_populates="requirements"
    )

    skill = relationship("Skill")