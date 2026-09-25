import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.student_profile import StudentProfile
from app.models.resume import Resume

from app.schemas.resume import ResumeResponse

from app.services.resume_service import extract_text_from_pdf
from app.services.resume_skill_service import extract_skills_from_resume

from app.models.student_profile import StudentSkill

router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"]
)


UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get(
    "/me",
    response_model=ResumeResponse
)
def get_my_resume(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    student_profile = (
        db.query(StudentProfile)
        .filter(
            StudentProfile.user_id == current_user.id
        )
        .first()
    )

    if not student_profile:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )

    resume = (
        db.query(Resume)
        .filter(
            Resume.student_profile_id == student_profile.id
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    return resume

@router.post(
    "/upload",
    response_model=ResumeResponse
)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    student_profile = (
        db.query(StudentProfile)
        .filter(
            StudentProfile.user_id == current_user.id
        )
        .first()
    )

    if not student_profile:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )

    existing_resume = (
        db.query(Resume)
        .filter(
            Resume.student_profile_id == student_profile.id
        )
        .first()
    )

    if existing_resume:
        raise HTTPException(
            status_code=400,
            detail="Resume already exists. Delete the existing resume before uploading a new one."
        )

    file_name = f"{uuid.uuid4()}.pdf"

    file_path = os.path.join(
        UPLOAD_DIR,
        file_name
    )

    contents = await file.read()

    with open(file_path, "wb") as resume_file:
        resume_file.write(contents)

    extracted_text = extract_text_from_pdf(
        file_path
    )

    resume = Resume(
        student_profile_id=student_profile.id,
        file_name=file_name,
        file_path=file_path,
        extracted_text=extracted_text
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume

@router.post("/extract-skills")
def extract_resume_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student_profile = (
        db.query(StudentProfile)
        .filter(StudentProfile.user_id == current_user.id)
        .first()
    )

    if not student_profile:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )

    resume = (
        db.query(Resume)
        .filter(Resume.student_profile_id == student_profile.id)
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    extracted_skills = extract_skills_from_resume(
        db,
        student_profile.id,
        resume.extracted_text or ""
    )

    added_skills = []
    already_existing = []

    for skill in extracted_skills:

        existing_skill = (
            db.query(StudentSkill)
            .filter(
                StudentSkill.student_profile_id == student_profile.id,
                StudentSkill.skill_id == skill.id
            )
            .first()
        )

        if existing_skill:
            already_existing.append(skill.name)
            continue

        student_skill = StudentSkill(
            student_profile_id=student_profile.id,
            skill_id=skill.id,
            proficiency=0,
            experience_months=None
        )

        db.add(student_skill)
        added_skills.append(skill.name)

    db.commit()

    return {
        "message": "Resume skills extracted successfully",
        "skills": added_skills,
        "already_existing": already_existing
    }