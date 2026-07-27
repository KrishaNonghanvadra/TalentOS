from fastapi import FastAPI

app = FastAPI(title="TalentOS API")

@app.get("/")
def root():
    return {
        "message": "TalentOS API is running"
    }