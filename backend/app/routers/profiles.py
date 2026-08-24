from dataclasses import field

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth_service import get_current_user
from app.models.user import User
from app.models.student_profile import StudentProfile

from app.schemas.student_profile import (
    StudentProfileCreate,
    StudentProfileResponse,
    StudentProfileUpdate,
)


router = APIRouter(
    prefix="/profiles",
    tags=["Student Profiles"]
)

@router.post(
    "",
    response_model=StudentProfileResponse,
    status_code=201
)
def create_profile(
    profile_data: StudentProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing_profile = (
    db.query(StudentProfile)
    .filter(
        StudentProfile.user_id == current_user.id
    )
    .first()
    )

    if existing_profile:
        raise HTTPException(
            status_code=400,
            detail="Student profile already exists"
        )

    new_profile = StudentProfile(
    user_id=current_user.id,
    full_name=profile_data.full_name,
    phone=profile_data.phone,
    college=profile_data.college,
    degree=profile_data.degree,
    branch=profile_data.branch,
    semester=profile_data.semester,
    cgpa=profile_data.cgpa,
    graduation_year=profile_data.graduation_year,
    github_url=str(profile_data.github_url)
        if profile_data.github_url
        else None,
    linkedin_url=str(profile_data.linkedin_url)
        if profile_data.linkedin_url
        else None,
    bio=profile_data.bio,
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile

@router.get(
    "/me",
    response_model=StudentProfileResponse
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = (
        db.query(StudentProfile)
        .filter(
            StudentProfile.user_id == current_user.id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )

    return profile

@router.put(
    "/me",
    response_model=StudentProfileResponse
)
def update_my_profile(
    profile_data: StudentProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = (
        db.query(StudentProfile)
        .filter(
            StudentProfile.user_id == current_user.id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )

    update_data = profile_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():

        if field in ["github_url", "linkedin_url"] and value:
            value = str(value)

        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return profile

@router.delete(
    "/me",
    status_code=204
)
def delete_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = (
        db.query(StudentProfile)
        .filter(
            StudentProfile.user_id == current_user.id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )

    db.delete(profile)
    db.commit()