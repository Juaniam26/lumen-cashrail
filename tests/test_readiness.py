from datetime import UTC, datetime, timedelta

import pytest

from cashrail_runtime.readiness import ManifestSigner


def complete_manifest() -> dict[str, object]:
    return {
        "attempt_id": "attempt-1",
        "bot_id": "bot_1",
        "gates": {key: True for key in "ABCDEF"},
        "blockers": [],
        "policy_version": "cashrail-v1",
        "clock_ready": True,
    }


def test_controller_signs_and_verifies_complete_manifest() -> None:
    now = datetime.now(UTC)
    signer = ManifestSigner("test-controller-token-32-characters")
    signed = signer.sign(complete_manifest(), now=now)

    assert signer.verify(signed, now=now)
    assert signed["signed_by"] == "cashrail-autonomous-controller"


def test_controller_refuses_incomplete_or_blocked_manifest() -> None:
    signer = ManifestSigner("test-controller-token-32-characters")
    with pytest.raises(ValueError, match="all pass"):
        signer.sign(complete_manifest() | {"gates": {"A": True}})
    with pytest.raises(ValueError, match="blockers"):
        signer.sign(complete_manifest() | {"blockers": ["B01"]})


def test_manifest_signature_rejects_tampering_and_expiry() -> None:
    now = datetime.now(UTC)
    signer = ManifestSigner("test-controller-token-32-characters")
    signed = signer.sign(complete_manifest(), now=now, ttl=timedelta(minutes=5))

    assert not signer.verify(signed | {"clock_ready": False}, now=now)
    assert not signer.verify(signed, now=now + timedelta(minutes=6))
