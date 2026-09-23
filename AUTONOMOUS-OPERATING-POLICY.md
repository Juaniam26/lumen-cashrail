# Cashrail Autonomous Operating Policy

## Runtime authority

The **Cashrail Autonomous Controller service** is the Tournament Controller. The product
owner is not a runtime operator, approval queue, fallback reviewer, or escalation target.
Bots never hold Controller authority. Jev is advisory and cannot execute actions.

## Out-of-policy behavior

An action that is missing evidence, has an unknown required value, fails a readiness or
safety gate, contradicts provider state, or falls outside the standing policy is stopped or
frozen automatically. It is not escalated to the product owner.

The default standing policy permits public research, internal scoring, and drafting only.
It does not permit outreach, contracts, charges, refunds, spending, payout changes, or live
provider mutations. Those actions require a separately deployed, versioned standing policy
and explicit external-execution authorization. Absence of that authorization means STOP.

## Jev

Jev is implemented as a deterministic local profit router. It uses complete structured
economics and the documented thresholds; it does not infer missing values from prose and
does not require an LLM or provider credential. Every recommendation is input-hashed,
version-bound, time-limited to four hours, persisted with the Controller disposition, and
recomputed after material change or expiry.

## Precedence

This policy governs runtime ownership and replaces references in reconstructed historical
mission material that route ordinary or exceptional operating decisions to the user. If a
qualified specialist or legally authorized signer is required but unavailable, the
opportunity stops. Cashrail does not transfer that duty to the product owner.
