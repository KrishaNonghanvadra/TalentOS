from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers import users
from app.routers import profiles

from app.routers import skills
from app.routers import student_skills

app = FastAPI(
    title="TalentOS API",
    description="AI-Powered Career Intelligence & Placement Platform",
    version="0.1.0"
)


app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "TalentOS API is running",
        "version": "0.1.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

app.include_router(users.router)
app.include_router(profiles.router)

app.include_router(skills.router)
app.include_router(student_skills.router)