from fastapi.testclient import TestClient

from cashrail_runtime.api import create_app
from cashrail_runtime.settings import Settings


def client(tmp_path, *, live: bool = False) -> TestClient:
    settings = Settings(
        database_url=f"sqlite:///{tmp_path / 'test.db'}",
        controller_token="test-controller-token-32-characters",
        enable_live_execution=live,
        stripe_webhook_secret="whsec_test",
    )
    return TestClient(create_app(settings))


def auth() -> dict[str, str]:
    return {"Authorization": "Bearer test-controller-token-32-characters"}


def test_health_is_public_but_does_not_leak_secrets(tmp_path) -> None:
    response = client(tmp_path).get("/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "live_execution": False}
    assert "token" not in response.text.lower()


def test_controller_status_names_cashrail_and_excludes_user_from_runtime(tmp_path) -> None:
    response = client(tmp_path).get("/v1/controller/status")
    assert response.status_code == 200
    assert response.json() == {
        "controller": "cashrail-autonomous-controller",
        "jev": "deterministic-profit-router",
        "user_in_runtime_chain": False,
        "out_of_policy_behavior": "STOP",
        "external_execution_enabled": False,
    }


def test_control_room_is_served_and_snapshot_leaks_no_secrets(tmp_path) -> None:
    api = client(tmp_path)
    page = api.get("/control-room/")
    snapshot = api.get("/v1/control-room/snapshot")

    assert page.status_code == 200
    assert "Cashrail Control Room" in page.text
    assert snapshot.status_code == 200
    assert snapshot.json()["controller"]["name"] == "Cashrail Autonomous Controller"
    assert snapshot.json()["controller"]["user_in_runtime_chain"] is False
    assert "token" not in snapshot.text.lower()
    assert "secret" not in snapshot.text.lower()


def test_control_room_can_rerun_a_safe_readiness_check(tmp_path) -> None:
    api = client(tmp_path)
    page = api.get("/control-room/")
    check = api.post("/v1/control-room/readiness-check")

    assert page.status_code == 200
    assert 'id="rerun-readiness"' in page.text
    assert "Run readiness check again" in page.text
    assert check.status_code == 200
    assert check.json()["clock_started"] is False
    assert check.json()["external_actions_performed"] is False
    assert check.json()["result"] == "NOT_READY"
    assert set(check.json()["gates"]) == set("ABCDEF")


def test_controller_endpoints_require_authentication(tmp_path) -> None:
    response = client(tmp_path).post("/v1/attempts", json={"bot_id": "bot_1"})
    assert response.status_code == 401


def test_attempt_creation_is_idempotent_and_immutable_72_hours(tmp_path) -> None:
    headers = auth() | {"Idempotency-Key": "attempt-bot-1-2026-09-23"}
    first = client(tmp_path).post("/v1/attempts", headers=headers, json={"bot_id": "bot_1"})
    second = client(tmp_path).post("/v1/attempts", headers=headers, json={"bot_id": "bot_1"})
    assert first.status_code == 201
    assert second.status_code == 200
    assert first.json()["attempt_id"] == second.json()["attempt_id"]
    assert first.json()["deadline"] == second.json()["deadline"]
    assert first.json()["status"] == "STAGED"


def test_live_activation_fails_closed_when_runtime_flag_is_off(tmp_path) -> None:
    api = client(tmp_path)
    created = api.post(
        "/v1/attempts",
        headers=auth() | {"Idempotency-Key": "attempt-activate-off"},
        json={"bot_id": "bot_1"},
    ).json()
    response = api.post(
        f"/v1/attempts/{created['attempt_id']}/activate",
        headers=auth(),
        json={"gates": {key: True for key in "ABCDEF"}},
    )
    assert response.status_code == 423


def test_incomplete_readiness_manifest_cannot_activate(tmp_path) -> None:
    api = client(tmp_path, live=True)
    created = api.post(
        "/v1/attempts",
        headers=auth() | {"Idempotency-Key": "attempt-missing-gates"},
        json={"bot_id": "bot_1"},
    ).json()
    response = api.post(
        f"/v1/attempts/{created['attempt_id']}/activate",
        headers=auth(),
        json={"gates": {"A": True}},
    )
    assert response.status_code == 409


def test_activation_sets_one_immutable_72_hour_deadline(tmp_path) -> None:
    api = client(tmp_path, live=True)
    created = api.post(
        "/v1/attempts",
        headers=auth() | {"Idempotency-Key": "attempt-complete-gates"},
        json={"bot_id": "bot_1"},
    ).json()
    payload = {"gates": {key: True for key in "ABCDEF"}}
    first = api.post(
        f"/v1/attempts/{created['attempt_id']}/activate", headers=auth(), json=payload
    )
    second = api.post(
        f"/v1/attempts/{created['attempt_id']}/activate", headers=auth(), json=payload
    )
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["deadline"] == second.json()["deadline"]
    assert first.json()["status"] == "ACTIVE"


def test_reusing_idempotency_key_with_different_payload_is_rejected(tmp_path) -> None:
    api = client(tmp_path)
    headers = auth() | {"Idempotency-Key": "attempt-payload-binding"}
    assert api.post("/v1/attempts", headers=headers, json={"bot_id": "bot_1"}).status_code == 201
    assert api.post("/v1/attempts", headers=headers, json={"bot_id": "bot_2"}).status_code == 409


def test_checkout_completed_is_not_credited_as_cleared_cash(tmp_path, monkeypatch) -> None:
    from cashrail_runtime import api as api_module

    monkeypatch.setattr(
        api_module.stripe.Webhook,
        "construct_event",
        lambda payload, signature, secret: {
            "id": "evt_1",
            "type": "checkout.session.completed",
            "data": {"object": {"id": "cs_1", "amount_total": 100_000}},
        },
    )
    api = client(tmp_path)
    response = api.post(
        "/v1/webhooks/stripe",
        content=b"{}",
        headers={"Stripe-Signature": "valid-test-signature"},
    )
    assert response.status_code == 202
    assert response.json()["credited_cleared_cash"] == 0


def test_autonomous_controller_evaluates_and_persists_decision(tmp_path) -> None:
    api = client(tmp_path)
    payload = {
        "action": "DRAFT_PROPOSAL",
        "gates": {key: True for key in "ABCDEF"},
        "suppression_clear": True,
        "authority_verified": True,
        "evidence_fresh": True,
        "security_clear": True,
        "jev_inputs": {
            "opportunity_id": "opp-1",
            "collection_probability": 0.9,
            "expected_verified_profit": 1_500_000,
            "remaining_action_hours": 10,
            "delivery_capacity": True,
            "reviewer_capacity": True,
            "approved_deposit": False,
            "evidence_complete": True,
            "policy_version": "cashrail-v1",
            "economics_version": "economics-v1",
        },
    }

    response = api.post(
        "/v1/controller/evaluate",
        headers=auth() | {"Idempotency-Key": "controller-decision-opp-1"},
        json=payload,
    )
    replay = api.post(
        "/v1/controller/evaluate",
        headers=auth() | {"Idempotency-Key": "controller-decision-opp-1"},
        json=payload,
    )

    assert response.status_code == 201
    assert response.json()["disposition"] == "APPROVED"
    assert response.json()["jev_action"] == "PURSUE"
    assert response.json()["escalation_target"] is None
    assert replay.status_code == 200
    assert replay.json()["decision_id"] == response.json()["decision_id"]


def test_autonomous_controller_stops_out_of_policy_without_user_escalation(tmp_path) -> None:
    api = client(tmp_path)
    payload = {
        "action": "SEND_OUTREACH",
        "gates": {key: True for key in "ABCDEF"},
        "suppression_clear": True,
        "authority_verified": True,
        "evidence_fresh": True,
        "security_clear": True,
        "jev_inputs": {
            "opportunity_id": "opp-2",
            "collection_probability": 0.9,
            "expected_verified_profit": 1_500_000,
            "remaining_action_hours": 10,
            "delivery_capacity": True,
            "reviewer_capacity": True,
            "approved_deposit": False,
            "evidence_complete": True,
            "policy_version": "cashrail-v1",
            "economics_version": "economics-v1",
        },
    }

    response = api.post(
        "/v1/controller/evaluate",
        headers=auth() | {"Idempotency-Key": "controller-decision-opp-2"},
        json=payload,
    )

    assert response.status_code == 201
    assert response.json()["disposition"] == "STOPPED"
    assert response.json()["escalation_target"] is None


def test_external_action_cannot_bypass_server_suppression_registry(tmp_path) -> None:
    api = client(tmp_path)
    contact_hash = "a" * 64
    suppress = api.post(
        "/v1/suppressions",
        headers=auth() | {"Idempotency-Key": "suppress-contact-1"},
        json={"contact_hash": contact_hash, "reason": "do-not-contact"},
    )
    assert suppress.status_code == 201

    settings = api.app.state.settings
    settings.controller_allowed_actions += ",SEND_OUTREACH"
    payload = {
        "action": "SEND_OUTREACH",
        "contact_hash": contact_hash,
        "gates": {key: True for key in "ABCDEF"},
        "suppression_clear": True,
        "authority_verified": True,
        "evidence_fresh": True,
        "security_clear": True,
        "jev_inputs": {
            "opportunity_id": "opp-suppressed",
            "collection_probability": 0.9,
            "expected_verified_profit": 1_500_000,
            "remaining_action_hours": 10,
            "delivery_capacity": True,
            "reviewer_capacity": True,
            "approved_deposit": False,
            "evidence_complete": True,
            "policy_version": "cashrail-v1",
            "economics_version": "economics-v1",
        },
    }
    decision = api.post(
        "/v1/controller/evaluate",
        headers=auth() | {"Idempotency-Key": "suppressed-decision-1"},
        json=payload,
    )
    assert decision.status_code == 201
    assert decision.json()["disposition"] == "FROZEN"
    assert decision.json()["reason_code"] == "ACTION_SAFETY_GATE_FAILED"


def test_controller_signing_endpoint_refuses_failed_gates(tmp_path) -> None:
    api = client(tmp_path)
    created = api.post(
        "/v1/attempts",
        headers=auth() | {"Idempotency-Key": "attempt-for-failed-signature"},
        json={"bot_id": "bot_1"},
    ).json()
    response = api.post(
        "/v1/readiness/sign",
        headers=auth() | {"Idempotency-Key": "failed-manifest-signature"},
        json={
            "attempt_id": created["attempt_id"],
            "bot_id": "bot_1",
            "gates": {key: False for key in "ABCDEF"},
            "blockers": ["B01"],
            "policy_version": "cashrail-v1",
            "clock_ready": False,
        },
    )
    assert response.status_code == 409


def test_suppression_duplicate_contact_is_safe_with_a_new_key(tmp_path) -> None:
    api = client(tmp_path)
    payload = {"contact_hash": "a" * 64, "reason": "opt-out"}
    first = api.post(
        "/v1/suppressions",
        headers=auth() | {"Idempotency-Key": "suppression-first-key"},
        json=payload,
    )
    second = api.post(
        "/v1/suppressions",
        headers=auth() | {"Idempotency-Key": "suppression-second-key"},
        json=payload | {"reason": "do-not-contact"},
    )

    assert first.status_code == 201
    assert second.status_code == 200
    mismatch = api.post(
        "/v1/suppressions",
        headers=auth() | {"Idempotency-Key": "suppression-second-key"},
        json={"contact_hash": "b" * 64, "reason": "different"},
    )
    assert mismatch.status_code == 409


def test_controller_refuses_manifest_for_stale_policy(tmp_path) -> None:
    api = client(tmp_path)
    created = api.post(
        "/v1/attempts",
        headers=auth() | {"Idempotency-Key": "attempt-for-stale-policy"},
        json={"bot_id": "bot_1"},
    ).json()
    response = api.post(
        "/v1/readiness/sign",
        headers=auth() | {"Idempotency-Key": "stale-policy-signature"},
        json={
            "attempt_id": created["attempt_id"],
            "bot_id": "bot_1",
            "gates": {key: True for key in "ABCDEF"},
            "blockers": [],
            "policy_version": "cashrail-old",
            "clock_ready": True,
        },
    )

    assert response.status_code == 409


def test_controller_signs_complete_manifest_durably_and_idempotently(tmp_path) -> None:
    api = client(tmp_path)
    created = api.post(
        "/v1/attempts",
        headers=auth() | {"Idempotency-Key": "attempt-for-signature"},
        json={"bot_id": "bot_1"},
    ).json()
    payload = {
        "attempt_id": created["attempt_id"],
        "bot_id": "bot_1",
        "gates": {key: True for key in "ABCDEF"},
        "blockers": [],
        "policy_version": "cashrail-v1",
        "clock_ready": True,
    }
    headers = auth() | {"Idempotency-Key": "complete-manifest-signature"}
    first = api.post("/v1/readiness/sign", headers=headers, json=payload)
    replay = api.post("/v1/readiness/sign", headers=headers, json=payload)

    assert first.status_code == 201
    assert replay.status_code == 200
    assert first.json()["signature"] == replay.json()["signature"]
