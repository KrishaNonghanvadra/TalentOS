from sqlalchemy.orm import Session

from app.models.student_profile import StudentProfile
from app.models.student_profile import StudentSkill
from app.models.skill import Skill


def search_candidates(
    db: Session,
    required_skills,
    minimum_match_percentage: float = 0
):
    students = db.query(StudentProfile).all()

    results = []

    for student in students:

        matched_skills = []
        total_score = 0

        for requirement in required_skills:

            student_skill = (
                db.query(StudentSkill)
                .filter(
                    StudentSkill.student_profile_id == student.id,
                    StudentSkill.skill_id == requirement.skill_id
                )
                .first()
            )

            skill = (
                db.query(Skill)
                .filter(
                    Skill.id == requirement.skill_id
                )
                .first()
            )

            if not skill:
                continue

            if student_skill:
                student_proficiency = student_skill.proficiency
            else:
                student_proficiency = 0

            required_proficiency = (
                requirement.required_proficiency
            )

            if required_proficiency > 0:
                score = min(
                    student_proficiency /
                    required_proficiency,
                    1
                )
            else:
                score = 1

            total_score += score

            matched_skills.append({
                "skill_id": skill.id,
                "skill_name": skill.name,
                "student_proficiency": student_proficiency,
                "required_proficiency": required_proficiency,
                "score": round(score * 100, 2)
            })

        if not required_skills:
            continue

        match_percentage = (
            total_score /
            len(required_skills)
        ) * 100

        if match_percentage < minimum_match_percentage:
            continue

        results.append({
            "student_profile_id": student.id,
            "full_name": student.full_name,
            "college": student.college,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "github_url": student.github_url,
            "match_percentage": round(
                match_percentage,
                2
            ),
            "matched_skills": matched_skills
        })

    results.sort(
        key=lambda x: x["match_percentage"],
        reverse=True
    )

    return results