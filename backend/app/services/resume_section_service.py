import re


SECTION_NAMES = {
    "skills": [
        "skills",
        "technical skills",
        "technical skill",
        "skill set"
    ],
    "projects": [
        "projects",
        "personal projects",
        "academic projects",
        "project work"
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "internship",
        "internships"
    ],
    "education": [
        "education",
        "academic background"
    ],
    "certifications": [
        "certifications",
        "certificates"
    ]
}


def detect_section_heading(line: str):
    cleaned = line.strip().lower()

    cleaned = re.sub(
        r"[^a-zA-Z\s]",
        "",
        cleaned
    )

    cleaned = " ".join(cleaned.split())

    for section, headings in SECTION_NAMES.items():
        if cleaned in headings:
            return section

    return None


def parse_resume_sections(text: str):
    sections = {
        "skills": "",
        "projects": "",
        "experience": "",
        "education": "",
        "certifications": "",
        "other": ""
    }

    current_section = "other"

    for line in text.splitlines():

        section = detect_section_heading(line)

        if section:
            current_section = section
            continue

        sections[current_section] += line + "\n"

    return sections