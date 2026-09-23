from datetime import UTC, datetime, timedelta

import pytest

from cashrail_runtime.domain import (
    DecisionEnvelope,
    Economics,
    UnknownEconomics,
    validate_jev_decision,
)


def complete_economics(**overrides: int | None) -> Economics:
    values = {
        "cleared_collected_cash": 1_500_000,
        "refunds": 10_000,
        "disputes": 20_000,
        "payment_fees": 45_000,
        "tax_reserve": 150_000,
        "chargeback_reserve": 30_000,
        "paid_variable_cost": 50_000,
        "accrued_fulfillment_cost": 100_000,
        "unearned_customer_obligations": 25_000,
        "reinvestment_spent": 20_000,
    }
    values.update(overrides)
    return Economics(**values)


def test_verified_net_profit_uses_every_required_deduction() -> None:
    assert complete_economics().verified_net_profit == 1_050_000


def test_unknown_economics_fail_closed_instead_of_becoming_zero() -> None:
    with pytest.raises(UnknownEconomics):
        complete_economics(tax_reserve=None).verified_net_profit


def test_negative_economics_are_rejected() -> None:
    with pytest.raises(ValueError):
        complete_economics(refunds=-1).verified_net_profit


def test_jev_decision_must_match_opportunity_hash_versions_and_expiry() -> None:
    now = datetime.now(UTC)
    envelope = DecisionEnvelope(
        opportunity_id="opp-1",
        input_hash="abc",
        policy_version="v1.9",
        economics_version="v1.9",
        approved_actions=frozenset({"PURSUE", "STOP"}),
    )
    decision = {
        "opportunity_id": "opp-1",
        "input_hash": "abc",
        "policy_version": "v1.9",
        "economics_version": "v1.9",
        "selected_action": "PURSUE",
        "valid_until": now + timedelta(minutes=5),
    }
    validate_jev_decision(envelope, decision, now=now)

    for key, value in {
        "opportunity_id": "opp-2",
        "input_hash": "different",
        "policy_version": "v0",
        "economics_version": "v0",
        "selected_action": "REALLOCATE",
        "valid_until": now - timedelta(seconds=1),
    }.items():
        invalid = decision | {key: value}
        with pytest.raises(ValueError):
            validate_jev_decision(envelope, invalid, now=now)
