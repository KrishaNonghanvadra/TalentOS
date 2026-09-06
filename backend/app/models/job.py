from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.orm import relationship

from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)

    company = Column(String(200), nullable=False)

    description = Column(Text, nullable=True)

    location = Column(String(200), nullable=True)

    job_type = Column(String(50), nullable=True)

    minimum_cgpa = Column(Float, nullable=True)

    requirements = relationship(
        "JobRequirement",
        back_populates="job",
        cascade="all, delete-orphan"
    )