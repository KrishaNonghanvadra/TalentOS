from sqlalchemy.orm import Session

from app.models.skill import Skill
from app.models.student_profile import StudentSkill


def calculate_github_proficiency(repository_count: int) -> float:
    """
    Estimate proficiency based on the number of public
    repositories using a programming language.

    This is only a heuristic.
    """

    if repository_count <= 0:
        return 0

    if repository_count == 1:
        return 3

    if repository_count == 2:
        return 4

    if repository_count <= 4:
        return 6

    if repository_count <= 7:
        return 8

    return 10


def update_student_skills_from_github(
    db: Session,
    student_profile_id: int,
    github_analysis: dict
):
    languages = github_analysis.get("languages", {})

    added_skills = []
    updated_skills = []
    ignored_languages = []

    for language, repository_count in languages.items():

        skill = (
            db.query(Skill)
            .filter(Skill.name.ilike(language))
            .first()
        )

        if not skill:
            ignored_languages.append(language)
            continue

        github_proficiency = calculate_github_proficiency(
            repository_count
        )

        existing_skill = (
            db.query(StudentSkill)
            .filter(
                StudentSkill.student_profile_id == student_profile_id,
                StudentSkill.skill_id == skill.id
            )
            .first()
        )

        if existing_skill:

            if github_proficiency > existing_skill.proficiency:
                existing_skill.proficiency = github_proficiency
                updated_skills.append(skill.name)

        else:

            student_skill = StudentSkill(
                student_profile_id=student_profile_id,
                skill_id=skill.id,
                proficiency=github_proficiency,
                experience_months=None
            )

            db.add(student_skill)
            added_skills.append(skill.name)

    db.commit()

    return {
        "added_skills": added_skills,
        "updated_skills": updated_skills,
        "ignored_languages": ignored_languages
    }