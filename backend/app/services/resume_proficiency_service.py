import re


def estimate_skill_proficiency(
    skill_name: str,
    resume_text: str
) -> float:

    text = resume_text.lower()
    skill = skill_name.lower()

    if skill not in text:
        return 0

    score = 2

    project_keywords = [
        "project",
        "developed",
        "built",
        "created",
        "application",
        "app",
    ]

    experience_keywords = [
        "experience",
        "internship",
        "worked",
        "developer",
        "engineer",
    ]

    advanced_keywords = [
        "architecture",
        "deployment",
        "optimization",
        "production",
        "api",
        "scalable",
        "microservices",
    ]

    for keyword in project_keywords:
        if keyword in text:
            score += 1

    for keyword in experience_keywords:
        if keyword in text:
            score += 1

    for keyword in advanced_keywords:
        if keyword in text:
            score += 1

    return min(score, 10)