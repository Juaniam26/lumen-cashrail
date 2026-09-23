from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta


@dataclass(frozen=True, slots=True)
class JevInputs:
    opportunity_id: str
    collection_probability: float | None
    expected_verified_profit: int | None
    remaining_action_hours: float | None
    delivery_capacity: bool | None
    reviewer_capacity: bool | None
    approved_deposit: bool
    evidence_complete: bool
    policy_version: str
    economics_version: str


@dataclass(frozen=True, slots=True)
class JevRecommendation:
    decision_id: str
    opportunity_id: str
    input_hash: str
    policy_version: str
    economics_version: str
    selected_action: str
    reason_code: str
    profit_per_remaining_hour: int | None
    created_at: datetime
    valid_until: datetime


@dataclass(frozen=True, slots=True)
class StandingPolicy:
    version: str
    allowed_actions: frozenset[str]


@dataclass(frozen=True, slots=True)
class ActionContext:
    action: str
    gates: dict[str, bool]
    suppression_clear: bool
    authority_verified: bool
    evidence_fresh: bool
    security_clear: bool
    jev: JevRecommendation


@dataclass(frozen=True, slots=True)
class ControllerDisposition:
    disposition: str
    reason_code: str
    escalation_target: None = None


def evaluate_jev(inputs: JevInputs, *, now: datetime | None = None) -> JevRecommendation:
    """Apply the documented Jev thresholds without an LLM or external provider."""
    now = now or datetime.now(UTC)
    canonical = json.dumps(asdict(inputs), sort_keys=True, separators=(",", ":"))
    input_hash = hashlib.sha256(canonical.encode()).hexdigest()
    action, reason, hourly = _route_jev(inputs)
    decision_seed = f"{input_hash}:{action}:{now.isoformat()}"
    decision_id = hashlib.sha256(decision_seed.encode()).hexdigest()
    return JevRecommendation(
        decision_id=decision_id,
        opportunity_id=inputs.opportunity_id,
        input_hash=input_hash,
        policy_version=inputs.policy_version,
        economics_version=inputs.economics_version,
        selected_action=action,
        reason_code=reason,
        profit_per_remaining_hour=hourly,
        created_at=now,
        valid_until=now + timedelta(hours=4),
    )


def _route_jev(inputs: JevInputs) -> tuple[str, str, int | None]:
    if inputs.remaining_action_hours is None or inputs.remaining_action_hours <= 0:
        return "STOP", "NO_REMAINING_ACTION_TIME", None
    if (
        inputs.collection_probability is None
        or inputs.expected_verified_profit is None
        or inputs.delivery_capacity is None
        or inputs.reviewer_capacity is None
        or not inputs.evidence_complete
    ):
        return "DEEP_REVIEW", "REQUIRED_INPUT_UNKNOWN", None
    if not 0 <= inputs.collection_probability <= 1:
        return "STOP", "INVALID_COLLECTION_PROBABILITY", None
    hourly = int(inputs.expected_verified_profit / inputs.remaining_action_hours)
    if not inputs.delivery_capacity or not inputs.reviewer_capacity:
        return "STOP", "CAPACITY_UNAVAILABLE", hourly
    if inputs.expected_verified_profit < 1_000_000 or hourly <= 0:
        return "STOP", "PROFIT_THRESHOLD_NOT_MET", hourly
    if inputs.collection_probability < 0.70 and not inputs.approved_deposit:
        return "DEEP_REVIEW", "COLLECTION_THRESHOLD_REQUIRES_DEPOSIT", hourly
    return "PURSUE", "ALL_PROFIT_GATES_PASS", hourly


def evaluate_action(
    policy: StandingPolicy, context: ActionContext
) -> ControllerDisposition:
    """Make a final controller decision; out-of-policy work stops with no user escalation."""
    required_gates = set("ABCDEF")
    if set(context.gates) != required_gates or not all(context.gates.values()):
        return ControllerDisposition("FROZEN", "READINESS_GATE_FAILED")
    if context.action not in policy.allowed_actions:
        return ControllerDisposition("STOPPED", "OUTSIDE_STANDING_POLICY")
    if not all(
        (
            context.suppression_clear,
            context.authority_verified,
            context.evidence_fresh,
            context.security_clear,
        )
    ):
        return ControllerDisposition("FROZEN", "ACTION_SAFETY_GATE_FAILED")
    if context.jev.policy_version != policy.version:
        return ControllerDisposition("FROZEN", "POLICY_VERSION_MISMATCH")
    if context.jev.selected_action != "PURSUE":
        return ControllerDisposition("STOPPED", f"JEV_{context.jev.reason_code}")
    return ControllerDisposition("APPROVED", "STANDING_POLICY_AND_JEV_PASS")
