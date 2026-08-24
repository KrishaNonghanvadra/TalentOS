from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers import users
from app.routers import profiles

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