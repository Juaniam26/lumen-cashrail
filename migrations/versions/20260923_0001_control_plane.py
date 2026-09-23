"""Initial Cashrail takeover control-plane schema."""
import sqlalchemy as sa
from alembic import op

revision = "20260923_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "attempts",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("bot_id", sa.String(16), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("deadline", sa.DateTime(timezone=True)),
        sa.Column("readiness_manifest", sa.Text()),
    )
    op.create_index("ix_attempts_bot_id", "attempts", ["bot_id"])
    op.create_table(
        "idempotency_records",
        sa.Column("key", sa.String(255), primary_key=True),
        sa.Column("scope", sa.String(80), nullable=False),
        sa.Column("resource_id", sa.String(36), nullable=False),
        sa.Column("request_hash", sa.String(64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("scope", "resource_id"),
    )
    op.create_table(
        "provider_events",
        sa.Column("provider", sa.String(32), primary_key=True),
        sa.Column("event_id", sa.String(255), primary_key=True),
        sa.Column("event_type", sa.String(120), nullable=False),
        sa.Column("received_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload_hash", sa.String(64), nullable=False),
        sa.Column("credited_cleared_cash", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("processed", sa.Boolean(), nullable=False, server_default=sa.true()),
    )


def downgrade() -> None:
    op.drop_table("provider_events")
    op.drop_table("idempotency_records")
    op.drop_index("ix_attempts_bot_id", table_name="attempts")
    op.drop_table("attempts")
