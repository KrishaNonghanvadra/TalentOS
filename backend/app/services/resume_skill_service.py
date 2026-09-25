import re

from sqlalchemy.orm import Session

from app.models.skill import Skill
from app.models.student_profile import StudentSkill


def extract_skills_from_resume(
    db: Session,
    student_profile_id: int,
    resume_text: str
):
    skills = db.query(Skill).all()

    extracted_skills = []

    text = resume_text.lower()

    for skill in skills:
        skill_name = skill.name.lower()

        pattern = r"\b" + re.escape(skill_name) + r"\b"

        if re.search(pattern, text):
            extracted_skills.append(skill)

    return extracted_skills