from __future__ import annotations

import hashlib
import json
import secrets
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import stripe
from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .controller import (
    ActionContext,
    JevInputs,
    StandingPolicy,
    evaluate_action,
    evaluate_jev,
)
from .db import (
    Attempt,
    ControllerDecision,
    IdempotencyRecord,
    ProviderEvent,
    make_session_factory,
)
from .settings import Settings


class AttemptCreate(BaseModel):
    bot_id: str = Field(pattern=r"^bot_[1-6]$")


class ReadinessManifest(BaseModel):
    gates: dict[str, bool]


class JevInputBody(BaseModel):
    opportunity_id: str = Field(min_length=1, max_length=255)
    collection_probability: float | None = Field(default=None, ge=0, le=1)
    expected_verified_profit: int | None = Field(default=None, ge=0)
    remaining_action_hours: float | None = Field(default=None, ge=0)
    delivery_capacity: bool | None = None
    reviewer_capacity: bool | None = None
    approved_deposit: bool = False
    evidence_complete: bool = False
    policy_version: str = Field(min_length=1, max_length=80)
    economics_version: str = Field(min_length=1, max_length=80)


class ControllerEvaluationBody(BaseModel):
    action: str = Field(min_length=1, max_length=80)
    gates: dict[str, bool]
    suppression_clear: bool
    authority_verified: bool
    evidence_fresh: bool
    security_clear: bool
    jev_inputs: JevInputBody


def create_app(settings: Settings) -> FastAPI:
    session_factory, engine = make_session_factory(
        settings.database_url, initialize_schema=settings.auto_create_schema
    )
    app = FastAPI(title="Cashrail Grok Six-Bot Controller", version="1.0.0")
    app.state.settings = settings
    app.state.session_factory = session_factory
    app.state.engine = engine

    def db_session() -> Iterator[Session]:
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    def require_controller(authorization: str | None = Header(default=None)) -> None:
        expected = f"Bearer {settings.controller_token.get_secret_value()}"
        if not authorization or not secrets.compare_digest(authorization, expected):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")

    @app.get("/v1/health")
    def health() -> dict[str, object]:
        return {"status": "ok", "live_execution": settings.enable_live_execution}

    @app.get("/v1/controller/status")
    def controller_status() -> dict[str, object]:
        return {
            "controller": "cashrail-autonomous-controller",
            "jev": "deterministic-profit-router",
            "user_in_runtime_chain": False,
            "out_of_policy_behavior": "STOP",
            "external_execution_enabled": settings.enable_live_execution,
        }

    @app.post("/v1/attempts", dependencies=[Depends(require_controller)])
    def create_attempt(
        body: AttemptCreate,
        idempotency_key: str = Header(min_length=8, max_length=255, alias="Idempotency-Key"),
        db: Session = Depends(db_session),
    ) -> object:
        request_hash = hashlib.sha256(body.model_dump_json().encode()).hexdigest()
        existing = db.get(IdempotencyRecord, idempotency_key)
        if existing:
            if existing.request_hash != request_hash:
                raise HTTPException(status_code=409, detail="idempotency key payload mismatch")
            attempt = db.get(Attempt, existing.resource_id)
            return _attempt_response(attempt, 200)

        now = datetime.now(UTC)
        attempt = Attempt(id=str(uuid4()), bot_id=body.bot_id, status="STAGED", created_at=now)
        db.add(attempt)
        db.add(
            IdempotencyRecord(
                key=idempotency_key,
                scope="attempt:create",
                resource_id=attempt.id,
                request_hash=request_hash,
                created_at=now,
            )
        )
        db.commit()
        return _attempt_response(attempt, 201)

    @app.post("/v1/attempts/{attempt_id}/activate", dependencies=[Depends(require_controller)])
    def activate_attempt(
        attempt_id: str,
        body: ReadinessManifest,
        db: Session = Depends(db_session),
    ) -> dict[str, str | None]:
        if not settings.enable_live_execution:
            raise HTTPException(status_code=423, detail="live execution is disabled")
        attempt = db.get(Attempt, attempt_id)
        if not attempt:
            raise HTTPException(status_code=404, detail="attempt not found")
        required = set("ABCDEF")
        if set(body.gates) != required or not all(body.gates.values()):
            raise HTTPException(status_code=409, detail="readiness gates A-F must all pass")
        if attempt.started_at is None:
            attempt.started_at = datetime.now(UTC)
            attempt.deadline = attempt.started_at + timedelta(hours=72)
        attempt.status = "ACTIVE"
        attempt.readiness_manifest = json.dumps(body.gates, sort_keys=True)
        db.commit()
        return _attempt_payload(attempt)

    @app.post("/v1/controller/evaluate", dependencies=[Depends(require_controller)])
    def controller_evaluate(
        body: ControllerEvaluationBody,
        idempotency_key: str = Header(min_length=8, max_length=255, alias="Idempotency-Key"),
        db: Session = Depends(db_session),
    ) -> object:
        request_hash = hashlib.sha256(body.model_dump_json().encode()).hexdigest()
        existing = db.get(IdempotencyRecord, idempotency_key)
        if existing:
            if existing.request_hash != request_hash:
                raise HTTPException(status_code=409, detail="idempotency key payload mismatch")
            saved = db.get(ControllerDecision, existing.resource_id)
            if saved is None:
                raise HTTPException(status_code=500, detail="controller decision record is corrupt")
            return JSONResponse(status_code=200, content=json.loads(saved.response_json))

        jev_inputs = JevInputs(**body.jev_inputs.model_dump())
        jev = evaluate_jev(jev_inputs)
        policy = StandingPolicy(
            version=settings.controller_policy_version,
            allowed_actions=settings.allowed_controller_actions,
        )
        disposition = evaluate_action(
            policy,
            ActionContext(
                action=body.action,
                gates=body.gates,
                suppression_clear=body.suppression_clear,
                authority_verified=body.authority_verified,
                evidence_fresh=body.evidence_fresh,
                security_clear=body.security_clear,
                jev=jev,
            ),
        )
        response = {
            "decision_id": jev.decision_id,
            "opportunity_id": jev.opportunity_id,
            "action": body.action,
            "disposition": disposition.disposition,
            "reason_code": disposition.reason_code,
            "escalation_target": disposition.escalation_target,
            "jev_action": jev.selected_action,
            "jev_reason_code": jev.reason_code,
            "jev_input_hash": jev.input_hash,
            "profit_per_remaining_hour": jev.profit_per_remaining_hour,
            "policy_version": jev.policy_version,
            "economics_version": jev.economics_version,
            "valid_until": jev.valid_until.isoformat(),
        }
        db.add(
            ControllerDecision(
                id=jev.decision_id,
                opportunity_id=jev.opportunity_id,
                action=body.action,
                disposition=disposition.disposition,
                reason_code=disposition.reason_code,
                jev_action=jev.selected_action,
                jev_input_hash=jev.input_hash,
                policy_version=jev.policy_version,
                economics_version=jev.economics_version,
                created_at=jev.created_at,
                valid_until=jev.valid_until,
                response_json=json.dumps(response, sort_keys=True),
            )
        )
        db.add(
            IdempotencyRecord(
                key=idempotency_key,
                scope="controller:evaluate",
                resource_id=jev.decision_id,
                request_hash=request_hash,
                created_at=jev.created_at,
            )
        )
        db.commit()
        return JSONResponse(status_code=201, content=response)

    @app.post("/v1/webhooks/stripe", status_code=202)
    async def stripe_webhook(
        request: Request,
        stripe_signature: str | None = Header(default=None, alias="Stripe-Signature"),
        db: Session = Depends(db_session),
    ) -> dict[str, bool | int]:
        if not stripe_signature:
            raise HTTPException(status_code=400, detail="missing Stripe signature")
        payload = await request.body()
        try:
            event = stripe.Webhook.construct_event(
                payload,
                stripe_signature,
                settings.stripe_webhook_secret.get_secret_value(),
            )
        except (ValueError, stripe.SignatureVerificationError):
            raise HTTPException(status_code=400, detail="invalid Stripe webhook") from None
        event_id, event_type = str(event["id"]), str(event["type"])
        record = ProviderEvent(
            provider="stripe",
            event_id=event_id,
            event_type=event_type,
            received_at=datetime.now(UTC),
            payload_hash=hashlib.sha256(payload).hexdigest(),
            credited_cleared_cash=0,
            processed=True,
        )
        db.add(record)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
        return {"accepted": True, "credited_cleared_cash": 0}

    return app


def _attempt_response(attempt: Attempt | None, status_code: int) -> JSONResponse:
    if attempt is None:
        raise HTTPException(status_code=500, detail="idempotency record is corrupt")
    return JSONResponse(
        status_code=status_code,
        content=_attempt_payload(attempt),
    )


def _attempt_payload(attempt: Attempt) -> dict[str, str | None]:
    return {
        "attempt_id": attempt.id,
        "bot_id": attempt.bot_id,
        "status": attempt.status,
        "started_at": _iso_utc(attempt.started_at),
        "deadline": _iso_utc(attempt.deadline),
    }


def _iso_utc(value: datetime | None) -> str | None:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).isoformat()


def app_from_environment() -> FastAPI:
    return create_app(Settings())
