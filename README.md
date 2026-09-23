# Cashrail Grok Six-Bot Revenue Tournament

**Production control-plane release:** the Grok six-bot tournament now takes over the Cashrail desk in this repository. The former handover material remains under `handover/` for provenance; the executable runtime is under `cashrail_runtime/`.

The complete six-bot mission, execution kernel, gate-control kit, Jev routing architecture, audit, checksums, and structural verifier are preserved under `tournament-spec/`.

The **Cashrail Autonomous Controller service** is the Controller. The product owner is not
in the runtime approval or escalation chain. Out-of-policy work stops automatically. Jev is
a deterministic, local, time-bounded profit router and does not require an AI-provider key.
See `AUTONOMOUS-OPERATING-POLICY.md`.

The read-only Control Room is available at `/control-room/`. It explains the six-bot sequence,
current readiness state, blockers, Controller/Jev roles, and provider-confirmed money in plain
language. It exposes no Controller mutation controls or credentials. “Refresh status” updates the
display; “Run readiness check again” safely recomputes the six gates without activating a bot,
starting its clock, or performing an external action.

The `production-gates` GitHub workflow enforces tests, at least 90% coverage, lint, strict type checking, static security analysis, dependency auditing, specification integrity, and a clean distributable build.

The runtime is deliberately fail-closed. It is production-ready with external execution disabled by default. It cannot send outreach, sign contracts, spend, create charges, or activate a bot until an operator supplies production secrets, applies migrations, explicitly enables live execution, and submits a complete A–F readiness manifest.

## Verified controls

- One durable 72-hour attempt per activation; restart does not reset the deadline.
- Complete verified-net-profit formula; unknown accounting fields block rather than become zero.
- Controller bearer authentication and payload-bound idempotency keys.
- Jev decision validation binds opportunity, input hash, policy/economics versions, approved action, and expiry.
- Autonomous Controller decisions are persisted and idempotent; no decision escalates to the product owner.
- Stripe webhook signature verification and event deduplication. Checkout completion is recorded but never credited as cleared cash.
- Production rejects SQLite and uses PostgreSQL with explicit migrations.
- Container runs as a non-root user with dropped capabilities, read-only filesystem, and live execution off.

## Run and verify

```bash
python -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/pytest -q
.venv/bin/ruff check .
.venv/bin/mypy cashrail_runtime
.venv/bin/bandit -q -r cashrail_runtime
.venv/bin/pip-audit
python3 tournament-spec/tools/verify_package.py
alembic upgrade head
uv build
```

For deployment, copy `.env.example` to the deployment secret system, run `alembic upgrade head`, and start the API. Never commit `.env` or Stripe/controller secrets. Use a restricted Stripe key when a later reconciliation worker is enabled; this release does not create Checkout Sessions, charges, invoices, refunds, or payouts.

## Existing Cashrail handover

Private operating kit for **this** desk — Nash Calder / Cashrail — built in the Grok chat with Jay Money.

This is **not**:

- [lumen.grok.me](https://lumen.grok.me) — that is a separate Codex focus / GTD app
- [Juaniam26/lumen-revenue-desk](https://github.com/Juaniam26/lumen-revenue-desk) — empty shell, different origin, do not mix

## What this repo is

The 72-hour $0-capital Revenue Desk handover:

| Path | What it is |
| --- | --- |
| `handover/00_START_HERE.txt` | Ten-minute setup |
| `handover/playbook.md` | Full manual |
| `handover/bots/00`–`09` | Paste-as-message-1 packets |
| `handover/agreements/` | One-pagers after a real YES |
| `handover/scripts/` | First-touch copy |
| `handover/UNLICENSED_RULES.txt` | SC real-estate stay-out rules |
| `handover/THREE_LANES_START.txt` | L7 / L8 / L9 add-on |

## Load

Jay is out of the loop on send-approvals for this desk.

- Hot: Desk + L3 mill + L5 distro + L7 recovery + L8 closer
- Lists: L1 / L2
- Lottery: L4
- Parked: L9 until there is a one-sentence demo
- Real estate: out
- $0 spend
- Stretch $30k is a target, not a forecast
- Geography: Spartanburg / Upstate SC

## Rules that beat every other instruction

- No ads, inventory, trading bankroll, fake proof, impersonation
- No consumer debt collection, no sheriff theater
- No pitching a product that is not live
- Cash is $0 unless Stripe says otherwise
- Ping Jay only on emergency or $500+

## Owner

Jay Money · Juaniam26
