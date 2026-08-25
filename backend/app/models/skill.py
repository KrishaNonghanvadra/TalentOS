from sqlalchemy import Column, Integer, String, Text

from app.core.base import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        unique=True,
        nullable=False
    )

    category = Column(
        String(100),
        nullable=True
    )

    description = Column(
        Text,
        nullable=True
    )