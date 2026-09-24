from pydantic import BaseModel


class ResumeResponse(BaseModel):
    id: int
    student_profile_id: int
    file_name: str
    file_path: str
    extracted_text: str | None = None

    class Config:
        from_attributes = True