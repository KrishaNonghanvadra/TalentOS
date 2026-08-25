from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.base import Base


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)

    college = Column(String(200), nullable=True)
    degree = Column(String(100), nullable=True)
    branch = Column(String(100), nullable=True)

    semester = Column(Integer, nullable=True)
    cgpa = Column(Float, nullable=True)
    graduation_year = Column(Integer, nullable=True)

    github_url = Column(String(255), nullable=True)
    linkedin_url = Column(String(255), nullable=True)

    bio = Column(Text, nullable=True)

    user = relationship(
        "User",
        back_populates="student_profile"
    )

    skills = relationship(
        "StudentSkill",
        back_populates="student_profile",
        cascade="all, delete-orphan"
    )

from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.core.base import Base


class StudentSkill(Base):
    __tablename__ = "student_skills"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_profile_id = Column(
        Integer,
        ForeignKey("student_profiles.id"),
        nullable=False
    )

    skill_id = Column(
        Integer,
        ForeignKey("skills.id"),
        nullable=False
    )

    proficiency = Column(
        Float,
        nullable=False,
        default=0
    )

    experience_months = Column(
        Integer,
        nullable=True
    )

    student_profile = relationship(
        "StudentProfile",
        back_populates="skills"
    )

    skill = relationship(
        "Skill"
    )