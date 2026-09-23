from datetime import UTC, datetime, timedelta

from cashrail_runtime.controller import (
    ActionContext,
    JevInputs,
    StandingPolicy,
    evaluate_action,
    evaluate_jev,
)


def viable_inputs(**overrides: object) -> JevInputs:
    values: dict[str, object] = {
        "opportunity_id": "opp-1",
        "collection_probability": 0.82,
        "expected_verified_profit": 1_500_000,
        "remaining_action_hours": 24.0,
        "delivery_capacity": True,
        "reviewer_capacity": True,
        "approved_deposit": False,
        "evidence_complete": True,
        "policy_version": "cashrail-v1",
        "economics_version": "economics-v1",
    }
    values.update(overrides)
    return JevInputs(**values)  # type: ignore[arg-type]


def test_jev_routes_viable_opportunity_without_a_model_or_human() -> None:
    now = datetime.now(UTC)
    result = evaluate_jev(viable_inputs(), now=now)

    assert result.selected_action == "PURSUE"
    assert result.valid_until == now + timedelta(hours=4)
    assert result.profit_per_remaining_hour == 62_500
    assert result.input_hash


def test_jev_fails_closed_on_unknown_or_bad_economics() -> None:
    assert evaluate_jev(viable_inputs(collection_probability=None)).selected_action == "DEEP_REVIEW"
    assert evaluate_jev(viable_inputs(remaining_action_hours=None)).selected_action == "STOP"
    assert evaluate_jev(viable_inputs(expected_verified_profit=999_999)).selected_action == "STOP"
    assert evaluate_jev(viable_inputs(delivery_capacity=False)).selected_action == "STOP"


def test_controller_approves_only_standing_policy_actions() -> None:
    policy = StandingPolicy(
        version="cashrail-v1",
        allowed_actions=frozenset({"PUBLIC_RESEARCH", "INTERNAL_SCORING", "DRAFT_PROPOSAL"}),
    )
    jev = evaluate_jev(viable_inputs())
    context = ActionContext(
        action="DRAFT_PROPOSAL",
        gates={key: True for key in "ABCDEF"},
        suppression_clear=True,
        authority_verified=True,
        evidence_fresh=True,
        security_clear=True,
        jev=jev,
    )

    assert evaluate_action(policy, context).disposition == "APPROVED"


def test_controller_stops_instead_of_escalating_to_user() -> None:
    policy = StandingPolicy(
        version="cashrail-v1",
        allowed_actions=frozenset({"PUBLIC_RESEARCH"}),
    )
    jev = evaluate_jev(viable_inputs())
    context = ActionContext(
        action="SEND_OUTREACH",
        gates={key: True for key in "ABCDEF"},
        suppression_clear=True,
        authority_verified=True,
        evidence_fresh=True,
        security_clear=True,
        jev=jev,
    )

    decision = evaluate_action(policy, context)
    assert decision.disposition == "STOPPED"
    assert decision.escalation_target is None
    assert decision.reason_code == "OUTSIDE_STANDING_POLICY"


def test_controller_freezes_on_missing_gate_or_jev_stop() -> None:
    policy = StandingPolicy(
        version="cashrail-v1",
        allowed_actions=frozenset({"PUBLIC_RESEARCH"}),
    )
    context = ActionContext(
        action="PUBLIC_RESEARCH",
        gates={key: key != "C" for key in "ABCDEF"},
        suppression_clear=True,
        authority_verified=True,
        evidence_fresh=True,
        security_clear=True,
        jev=evaluate_jev(viable_inputs(expected_verified_profit=0)),
    )

    assert evaluate_action(policy, context).disposition == "FROZEN"
