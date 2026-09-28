from app.services.resume_section_service import parse_resume_sections


def estimate_skill_proficiency(
    skill_name: str,
    resume_text: str
) -> float:

    sections = parse_resume_sections(
        resume_text
    )

    skill = skill_name.lower()

    score = 0

    # Skill explicitly listed
    if skill in sections["skills"].lower():
        score = 3

    # Skill used in projects
    if skill in sections["projects"].lower():
        score += 2

    # Skill used in experience
    if skill in sections["experience"].lower():
        score += 3

    # Skill mentioned in certifications
    if skill in sections["certifications"].lower():
        score += 1

    return min(score, 10)