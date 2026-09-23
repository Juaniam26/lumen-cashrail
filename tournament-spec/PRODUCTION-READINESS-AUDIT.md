# Production-Hardening Audit — v1.9 controlled deliverable

## Scope and evidence boundary

This audit covers the supplied `grok-six-bot-revenue-tournament-integrated-verified.zip`, `Pasted text.txt`, and `Pasted text (2).txt`. The ZIP contains Markdown and JSON control material only; it does not contain the Python service, SQL schema, Docker files, dependency lockfile, migrations, tests, dashboards, or provider adapters described in the pasted transcript. Therefore runtime claims in the pasted transcript are treated as unverified source claims, not as inspected implementation evidence.

The package is hardened as a production-controlled specification and archive. It is not a verified production service and is not launch authorization.

## Findings converted to controls or blockers

| ID | Severity | Evidence | Finding | Disposition |
|---|---|---|---|---|
| AUD-001 | Critical | Pasted text, `JevClient.call_jev` | Budget query filters `is_paused=False` and then checks whether the returned row is paused. The pause branch is unreachable; spend can continue past the safety threshold. | Blocker recorded. A real implementation must atomically reserve budget before the call and fail closed at the cap. |
| AUD-002 | Critical | Pasted text, `_call_jev_internal` | The claimed Jev integration is a local ratio simulation. It does not authenticate to Jev, enforce timeout/retry/redaction/schema validation, or prove REST/MCP compatibility. | Blocker recorded. Only an authenticated synthetic/dry-run test may establish compatibility. |
| AUD-003 | Critical | Pasted text, `create_opportunity` | `expected_profit` is `cleared_cash - variable_cost`; it omits fees, refunds/disputes, reserves, fulfillment obligations, tax reserve, and reinvestment. It also accepts cleared cash from the request rather than a provider-backed receipt. | Blocker recorded. The canonical ledger formula in v1.8 remains authoritative; runtime implementation must calculate from evidence-owned fields. |
| AUD-004 | High | Pasted text, `DeterministicRouter` | `required_economics_version` is declared but only `policy_version` is checked. A stale economics policy can pass the router. | Blocker recorded. Add a test that mismatched policy or economics versions never return `PURSUE`. |
| AUD-005 | Critical | Pasted text, `/act` | The disposition endpoint does not prove that the Jev decision belongs to the requested opportunity, matches the current envelope hash, is unexpired, is in the approved action set, or was authorized by an authenticated Controller. | Blocker recorded. Require opportunity binding, hash/version checks, expiry checks, idempotency, and Controller authorization. |
| AUD-006 | High | Pasted text, `attempt_id = uuid4()` in opportunity creation | Each opportunity receives a new attempt ID, which conflicts with one immutable 72-hour attempt per activated bot. | Blocker recorded. Attempt identity must come from the active durable BotAttempt, never from opportunity creation. |
| AUD-007 | High | Pasted deployment claims | The transcript claims “ready for production” and “50+ tests,” but no executable service, dependency lock, test output, migration evidence, image digest, or deployment receipt was supplied. | Corrected in package status. The verifier reports archive/spec readiness only. |
| AUD-008 | High | Pasted text, defaults/logging | Default database credentials, optional API key, URL logging, no demonstrated authentication/rate limiting, and `create_all` startup schema creation are not acceptable production defaults. | Blocker recorded. Require secret references, redacted logs, authenticated API access, migrations, and least-privilege database roles. |
| AUD-009 | High | Shared v1.8 controls | The package describes durable state, event hashes, reconciliation, and observability but supplies no executable schemas, event-chain verifier, idempotency store, or synthetic replay harness. | Fixed at deliverable level by adding the package verifier and an explicit implementation blocker register; runtime remains pending. |
| AUD-010 | Medium | Jev architecture and pasted evaluation text | Jev promotion thresholds differ across the supplied material (for example, 10/30-day evidence versus 25+ lift evidence). | Fixed by declaring the v1.8 Jev architecture and shared controls authoritative; conflicting pasted thresholds are non-authoritative pending an approved policy version. |

## Required acceptance tests before any live authority

1. Verify the ZIP and extracted package against the generated SHA-256 manifest.
2. Run the package verifier with zero structural failures.
3. Build a real non-production service from a canonical repository with a locked dependency graph and migrations.
4. Prove fail-closed economics with provider-backed synthetic receipts, including every deduction and `null != 0` behavior.
5. Prove atomic idempotency and uncertain-mutation reconciliation under timeout, restart, duplicate request, and provider contradiction.
6. Prove authorization, suppression, evidence freshness, offer approval, and Controller-only activation with negative tests.
7. Prove Jev authenticated REST/MCP compatibility in shadow mode, including malformed/injection responses, cost caps, timeout, redaction, and fallback.
8. Produce independent security/quality evidence, backup restore evidence, observability alerts, and a signed readiness manifest.

No external outreach, charge, invoice, contract, signature, spend, publication, or bot activation is authorized by this audit.
