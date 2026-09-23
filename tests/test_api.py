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
