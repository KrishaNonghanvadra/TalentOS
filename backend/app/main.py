from fastapi import FastAPI

app = FastAPI(
    title="TalentOS API",
    description="AI-Powered Career Intelligence & Placement Platform",
    version="0.1.0"
)


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