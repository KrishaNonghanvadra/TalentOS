from sqlalchemy.orm import Session

from app.models.student_profile import StudentProfile
from app.models.resume import Resume
from app.models.student_profile import StudentSkill

def calculate_skill_score(student_profile: StudentProfile) -> float:
    skills = student_profile.skills

    if not skills:
        return 0

    total = 0

    for student_skill in skills:
        total += student_skill.proficiency

    average = total / len(skills)

    return round((average / 10) * 100, 2)


def calculate_profile_score(student_profile: StudentProfile) -> float:
    fields = [
        student_profile.full_name,
        student_profile.phone,
        student_profile.college,
        student_profile.degree,
        student_profile.branch,
        student_profile.semester,
        student_profile.cgpa,
        student_profile.graduation_year,
        student_profile.github_url,
        student_profile.linkedin_url,
        student_profile.bio,
    ]

    completed_fields = 0

    for field in fields:
        if field is not None and field != "":
            completed_fields += 1

    score = (completed_fields / len(fields)) * 100

    return round(score, 2)


def calculate_resume_score(student_profile: StudentProfile) -> float:
    if not student_profile.resume:
        return 0

    resume = student_profile.resume

    if not resume.extracted_text:
        return 50

    if len(resume.extracted_text.strip()) < 100:
        return 50

    return 100


def calculate_github_score(student_profile: StudentProfile) -> float:
    skills = student_profile.skills

    if not skills:
        return 0

    github_skill_count = 0

    for skill in skills:
        if skill.proficiency > 0:
            github_skill_count += 1

    if github_skill_count == 0:
        return 0

    score = min(github_skill_count * 20, 100)

    return score


def calculate_career_readiness(
    db: Session,
    student_profile: StudentProfile
):
    skill_score = calculate_skill_score(student_profile)

    profile_score = calculate_profile_score(student_profile)

    resume_score = calculate_resume_score(student_profile)

    github_score = calculate_github_score(student_profile)

    overall_score = (
        skill_score * 0.40
        + profile_score * 0.20
        + resume_score * 0.20
        + github_score * 0.20
    )

    return {
        "overall_score": round(overall_score, 2),
        "skill_score": skill_score,
        "profile_score": profile_score,
        "resume_score": resume_score,
        "github_score": github_score,
    }