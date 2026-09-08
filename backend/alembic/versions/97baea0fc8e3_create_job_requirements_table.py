"""Create job requirements table

Revision ID: 97baea0fc8e3
Revises: af443d1ce8ca
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "97baea0fc8e3"
down_revision: Union[str, Sequence[str], None] = "af443d1ce8ca"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "job_requirements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("job_id", sa.Integer(), nullable=False),
        sa.Column("skill_id", sa.Integer(), nullable=False),
        sa.Column("required_proficiency", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["job_id"],
            ["jobs.id"],
        ),
        sa.ForeignKeyConstraint(
            ["skill_id"],
            ["skills.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_job_requirements_id"),
        "job_requirements",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_job_requirements_id"),
        table_name="job_requirements",
    )
    op.drop_table("job_requirements")