from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.student_profile import StudentProfile
from app.services.job_matching_service import calculate_job_match


def get_recommended_jobs(
    db: Session,
    student_profile: StudentProfile
):
    jobs = db.query(Job).all()

    recommendations = []

    for job in jobs:
        result = calculate_job_match(
            db,
            student_profile,
            job
        )

        recommendations.append(result)

    # Highest match first
    recommendations.sort(
        key=lambda x: x["match_percentage"],
        reverse=True
    )

    return recommendations