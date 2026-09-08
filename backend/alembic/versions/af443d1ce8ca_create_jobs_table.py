"""Create jobs table

Revision ID: af443d1ce8ca
Revises: 41e4886de0e0
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "af443d1ce8ca"
down_revision: Union[str, Sequence[str], None] = "41e4886de0e0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("company", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("location", sa.String(length=200), nullable=True),
        sa.Column("job_type", sa.String(length=50), nullable=True),
        sa.Column("minimum_cgpa", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_jobs_id"),
        "jobs",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_jobs_id"), table_name="jobs")
    op.drop_table("jobs")