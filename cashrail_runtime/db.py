from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, UniqueConstraint, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class Attempt(Base):
    __tablename__ = "attempts"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    bot_id: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="STAGED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    readiness_manifest: Mapped[str | None] = mapped_column(Text)


class IdempotencyRecord(Base):
    __tablename__ = "idempotency_records"
    key: Mapped[str] = mapped_column(String(255), primary_key=True)
    scope: Mapped[str] = mapped_column(String(80), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(36), nullable=False)
    request_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    __table_args__ = (UniqueConstraint("scope", "resource_id"),)


class ProviderEvent(Base):
    __tablename__ = "provider_events"
    provider: Mapped[str] = mapped_column(String(32), primary_key=True)
    event_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    event_type: Mapped[str] = mapped_column(String(120), nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    payload_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    credited_cleared_cash: Mapped[int] = mapped_column(default=0, nullable=False)
    processed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


def make_session_factory(
    database_url: str, *, initialize_schema: bool
) -> tuple[sessionmaker[Session], Engine]:
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite:") else {}
    engine = create_engine(database_url, pool_pre_ping=True, connect_args=connect_args)
    if initialize_schema:
        Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, expire_on_commit=False), engine
