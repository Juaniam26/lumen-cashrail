# Runtime Contract v1.8

## Startup contract

The runner must load and verify the signed readiness manifest, policy/economics versions, active Bot ID, activation timestamp, immutable deadline, provider health, credentials by opaque reference, current suppression set, canonical ledger, open obligations, outstanding uncertain actions, approved offer variants, and capacity. If any required item is missing or stale, enter `FROZEN`, not `ACTIVE`.

## State machine

`BOOT → RECOVER → RECONCILE → PREFLIGHT → READY → ACTIVE_LOOP → CHECKPOINT`, with exits to `FROZEN`, `PASS_CANDIDATE`, `FAIL_CANDIDATE`, or `TERMINAL`. Only the Controller converts a candidate to PASS/FAIL after provider reconciliation and obligation accounting.

## Active-loop contract

One durable decision and at most one external mutation per transaction boundary. Before mutation: re-read entity version, clock, suppression, approval, economics, capacity, and idempotency status. After mutation: capture provider receipt, read provider state, append event, update obligation and ledger projections, checkpoint, and only then plan the next action.

## Time and terminal behavior

Use a monotonic elapsed-time record plus wall-clock UTC timestamps. Restart does not extend the deadline. At deadline: stop new acquisition and new commitments, reconcile actions already accepted by providers, preserve delivery/support/refund duties, compute the candidate result, generate a terminal report, and wait for Controller disposition.

## Failure-mode table

| Condition | Required behavior |
|---|---|
| Model/context loss | Recover only from durable state and verify hash chain |
| Browser crash | Mark current action uncertain; reconcile before retry |
| Login/session expiry | Freeze dependent action; route to credential owner |
| Site blocks automation | Stop automation; no evasion; use approved alternative |
| Provider timeout/rate limit | Bounded retry, circuit breaker, deterministic fallback |
| Unexpected reply | Cancel queued templates for that party; classify and route |
| Data contradiction | Provider owner wins after reconciliation; freeze meanwhile |
| Low credits/cash/capacity | Stop before spend or obligation; re-scope only to approved variant |
| Jev unavailable/malformed/expired | Deterministic gates/ranking; no invented decision |
| Critical safety/security issue | Immediate freeze and incident escalation |

## Observability

Record health heartbeats, queue depth, provider latency/errors, uncertain mutations, suppression events, bounce/complaint/refund/dispute rates, cleared cash, reserves, costs, obligations, capacity, and clock. Alerts require an owner, severity, acknowledgment deadline, and closure evidence.

## Resume acceptance test

A resumed runner must prove: same attempt ID/deadline; no duplicate provider mutation; complete open-obligation list; ledger matches authoritative providers; suppression is current; policy and economics versions match; last checkpoint hash verifies. Otherwise it remains frozen.
