from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.job_requirement import JobRequirement
from app.models.student_profile import StudentProfile

def get_gap_priority(gap: float) -> str:
    if gap >= 3:
        return "High"

    if gap >= 1:
        return "Medium"

    return "Low"


def calculate_job_match(
    db: Session,
    student_profile: StudentProfile,
    job: Job
):
    requirements = db.query(
        JobRequirement
    ).filter(
        JobRequirement.job_id == job.id
    ).all()

    matched_skills = []
    skill_gaps = []

    for requirement in requirements:

        student_skill = next(
            (
                skill
                for skill in student_profile.skills
                if skill.skill_id == requirement.skill_id
            ),
            None
        )

        if student_skill:
            student_proficiency = student_skill.proficiency
        else:
            student_proficiency = 0

        required_proficiency = (
            requirement.required_proficiency
        )

        skill_name = requirement.skill.name

        if student_proficiency >= required_proficiency:

            matched_skills.append({
                "skill": skill_name,
                "student_proficiency": student_proficiency,
                "required_proficiency": required_proficiency
            })

        else:
            gap = required_proficiency - student_proficiency
            priority = get_gap_priority(gap)

            skill_gaps.append({
                "skill": skill_name,
                "student_proficiency": student_proficiency,
                "required_proficiency": required_proficiency,
                "gap": gap,
                "priority": priority
            })

    skill_gaps.sort(key=lambda x: x["gap"], reverse=True)

    total_requirements = len(requirements)

    if total_requirements == 0:
        match_percentage = 0
    else:
        match_percentage = (
            len(matched_skills)
            / total_requirements
        ) * 100

    return {
        "job_id": job.id,
        "job_title": job.title,
        "company": job.company,
        "match_percentage": round(match_percentage, 2),
        "matched_skills": matched_skills,
        "skill_gaps": skill_gaps
    }