from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, fields
from datetime import UTC, datetime
from typing import Any


class UnknownEconomics(ValueError):
    """A required accounting term is unknown; unknown never becomes zero."""


@dataclass(frozen=True, slots=True)
class Economics:
    cleared_collected_cash: int | None
    refunds: int | None
    disputes: int | None
    payment_fees: int | None
    tax_reserve: int | None
    chargeback_reserve: int | None
    paid_variable_cost: int | None
    accrued_fulfillment_cost: int | None
    unearned_customer_obligations: int | None
    reinvestment_spent: int | None

    @property
    def verified_net_profit(self) -> int:
        values: dict[str, int] = {}
        for item in fields(self):
            value = getattr(self, item.name)
            if value is None:
                raise UnknownEconomics(f"required economics field is unknown: {item.name}")
            if value < 0:
                raise ValueError(f"economics field cannot be negative: {item.name}")
            values[item.name] = value
        return values["cleared_collected_cash"] - sum(
            value for name, value in values.items() if name != "cleared_collected_cash"
        )


@dataclass(frozen=True, slots=True)
class DecisionEnvelope:
    opportunity_id: str
    input_hash: str
    policy_version: str
    economics_version: str
    approved_actions: frozenset[str]


def validate_jev_decision(
    envelope: DecisionEnvelope,
    decision: Mapping[str, Any],
    *,
    now: datetime | None = None,
) -> None:
    now = now or datetime.now(UTC)
    for key, expected in {
        "opportunity_id": envelope.opportunity_id,
        "input_hash": envelope.input_hash,
        "policy_version": envelope.policy_version,
        "economics_version": envelope.economics_version,
    }.items():
        if decision.get(key) != expected:
            raise ValueError(f"Jev decision {key} mismatch")
    if decision.get("selected_action") not in envelope.approved_actions:
        raise ValueError("Jev decision action is not approved")
    valid_until = decision.get("valid_until")
    if not isinstance(valid_until, datetime) or valid_until <= now:
        raise ValueError("Jev decision is expired or missing expiry")
