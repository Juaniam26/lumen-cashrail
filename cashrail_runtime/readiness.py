from __future__ import annotations

import hashlib
import hmac
import json
from datetime import UTC, datetime, timedelta
from typing import Any


class ManifestSigner:
    """Domain-separated, tamper-evident readiness signatures for the Controller."""

    def __init__(self, controller_secret: str) -> None:
        self._key = hashlib.sha256(f"cashrail-manifest-v1:{controller_secret}".encode()).digest()

    def sign(
        self,
        manifest: dict[str, Any],
        *,
        now: datetime | None = None,
        ttl: timedelta = timedelta(hours=4),
    ) -> dict[str, Any]:
        gates = manifest.get("gates")
        if not isinstance(gates, dict) or set(gates) != set("ABCDEF") or not all(gates.values()):
            raise ValueError("readiness gates A-F must all pass before signing")
        blockers = manifest.get("blockers")
        if not isinstance(blockers, list) or blockers:
            raise ValueError("readiness blockers must be empty before signing")
        if manifest.get("clock_ready") is not True:
            raise ValueError("clock_ready must be true before signing")

        now = now or datetime.now(UTC)
        payload = manifest | {
            "signed_by": "cashrail-autonomous-controller",
            "signed_at": now.isoformat(),
            "valid_until": (now + ttl).isoformat(),
        }
        return payload | {"signature": self._signature(payload)}

    def verify(self, signed: dict[str, Any], *, now: datetime | None = None) -> bool:
        signature = signed.get("signature")
        if not isinstance(signature, str):
            return False
        payload = {key: value for key, value in signed.items() if key != "signature"}
        if not hmac.compare_digest(signature, self._signature(payload)):
            return False
        try:
            valid_until = datetime.fromisoformat(str(payload["valid_until"]))
        except (KeyError, ValueError):
            return False
        now = now or datetime.now(UTC)
        return valid_until > now

    def _signature(self, payload: dict[str, Any]) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return hmac.new(self._key, canonical, hashlib.sha256).hexdigest()
