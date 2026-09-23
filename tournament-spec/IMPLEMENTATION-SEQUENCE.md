# Implementation Sequence — No-Live-Execution Build

1. Freeze scope and verify this package's checksums and reconstruction notes.
2. Assign Controller, backup, domain reviewers, payment owner, credential owner, incident owner, and delivery owners.
3. Implement canonical durable state, event hash chain, idempotency, checkpoints, and provider-reconciliation adapters in a non-production environment.
4. Complete Gate 0A synthetic capability tests for every tool; document costs, authority, rate limits, retries, and fallbacks.
5. Complete independent security/privacy review (0B); remediate critical/high issues and preserve evidence.
6. Measure each bot's fulfillment/reviewer capacity and unit economics; approve offer variants, prices, deposits, terms, reserves, and stop thresholds (0C).
7. Build evidence-backed public-first opportunity pools; deduplicate, score, and audit the first wave without contacting prospects (0D).
8. Approve rendered messages/actions individually and verify identity, jurisdiction, consent/suppression, claims, offer, and destination (0E).
9. Sign each bot's readiness manifest and `clock_ready` predicate (0F). Keep bots staged.
10. Test Jev connectivity and data handling, then synthetic/historical shadow mode. Do not grant live influence until exit criteria pass.
11. Run a full no-send/no-charge rehearsal: restart recovery, provider timeout, duplicate prevention, suppression, incident freeze, deadline closure, terminal report, and bot handoff.
12. Separately obtain explicit live authorization. Controller activates only Bot 1, records the immutable deadline, and keeps Bots 2–6 staged.
13. During any later authorized attempt, reconcile provider truth continuously; at terminal state, close obligations before considering the next bot.

This package completes steps 1's artifact portion only. It does not assert that steps 2–13 are complete.
