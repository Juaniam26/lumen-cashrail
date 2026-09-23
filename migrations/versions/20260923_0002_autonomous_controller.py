"""autonomous controller decisions

Revision ID: 20260923_0002
Revises: 20260923_0001
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260923_0002"
down_revision: str | None = "20260923_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "controller_decisions",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("opportunity_id", sa.String(length=255), nullable=False),
        sa.Column("action", sa.String(length=80), nullable=False),
        sa.Column("disposition", sa.String(length=24), nullable=False),
        sa.Column("reason_code", sa.String(length=120), nullable=False),
        sa.Column("jev_action", sa.String(length=24), nullable=False),
        sa.Column("jev_input_hash", sa.String(length=64), nullable=False),
        sa.Column("policy_version", sa.String(length=80), nullable=False),
        sa.Column("economics_version", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("valid_until", sa.DateTime(timezone=True), nullable=False),
        sa.Column("response_json", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_controller_decisions_opportunity_id",
        "controller_decisions",
        ["opportunity_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_controller_decisions_opportunity_id", table_name="controller_decisions")
    op.drop_table("controller_decisions")
