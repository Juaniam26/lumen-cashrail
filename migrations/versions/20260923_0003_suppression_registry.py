"""suppression registry

Revision ID: 20260923_0003
Revises: 20260923_0002
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260923_0003"
down_revision: str | None = "20260923_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("idempotency_records") as batch_op:
        batch_op.alter_column(
            "resource_id",
            existing_type=sa.String(length=36),
            type_=sa.String(length=255),
            existing_nullable=False,
        )
    op.create_table(
        "suppression_records",
        sa.Column("contact_hash", sa.String(length=64), nullable=False),
        sa.Column("reason", sa.String(length=120), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("contact_hash"),
    )
    op.create_table(
        "readiness_manifests",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("attempt_id", sa.String(length=36), nullable=False),
        sa.Column("bot_id", sa.String(length=16), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.Column("signature", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("valid_until", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("signature"),
    )
    op.create_index(
        "ix_readiness_manifests_attempt_id",
        "readiness_manifests",
        ["attempt_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_readiness_manifests_attempt_id", table_name="readiness_manifests")
    op.drop_table("readiness_manifests")
    op.drop_table("suppression_records")
    with op.batch_alter_table("idempotency_records") as batch_op:
        batch_op.alter_column(
            "resource_id",
            existing_type=sa.String(length=255),
            type_=sa.String(length=36),
            existing_nullable=False,
        )
