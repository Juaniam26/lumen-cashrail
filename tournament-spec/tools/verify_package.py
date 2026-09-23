#!/usr/bin/env python3
"""Structural verifier for the reconstructed six-bot control package.

This deliberately verifies archive integrity and control invariants only. It
does not connect to providers, send messages, charge money, or activate bots.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.json"
CHECKSUMS = ROOT / "INTEGRITY-SHA256.txt"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("source_status", "").startswith("reconstructed") is False:
        fail("manifest source status is not explicit about reconstruction")
    if manifest.get("live_execution_authorized") is not False:
        fail("live_execution_authorized must be false")

    entries = manifest.get("files", [])
    if manifest.get("file_count_excluding_manifest_and_checksum") != len(entries):
        fail("manifest file count does not match entries")

    for entry in entries:
        rel = entry["path"]
        path = ROOT / rel
        if not path.is_file():
            fail(f"manifest file missing: {rel}")
        actual = sha256(path)
        if actual != entry["sha256"]:
            fail(f"manifest hash mismatch: {rel}")
        if path.stat().st_size != entry["size_bytes"]:
            fail(f"manifest size mismatch: {rel}")

    required = [
        "README.md",
        "RECONSTRUCTION-NOTES.md",
        "AUDIT-DISPOSITIONS.md",
        "PRODUCTION-READINESS-AUDIT.md",
        "IMPLEMENTATION-BLOCKERS.md",
        "tools/verify_package.py",
    ]
    for rel in required:
        if not (ROOT / rel).is_file():
            fail(f"required control file missing: {rel}")

    master = (ROOT / "shared/master-tournament-mission-v1.8.md").read_text(encoding="utf-8")
    for phrase in ("72-hour", "10,000", "zero user-provided capital", "provider-confirmed cleared cash"):
        if phrase.lower() not in master.lower():
            fail(f"master mission lost invariant: {phrase}")

    print(f"PASS: {len(entries)} manifest entries verified")
    print("PASS: reconstruction and no-live-execution controls verified")
    print("PASS: core tournament invariants present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
