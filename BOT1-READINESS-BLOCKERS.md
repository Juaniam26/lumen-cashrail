# Bot 1 Readiness Blocker Register

This register distinguishes implemented controls from real-world evidence that does not yet exist. A code path is not marked as a live business capability merely because its tests pass.

| ID | Status | Current evidence | What remains |
|---|---|---|---|
| B01 Controller signing path | **FIXED** | Controller signs only complete A–F manifests with zero blockers; signatures are tamper-evident, expiring, durable, and idempotent. | None in code. |
| B02 Delivery owner | **FIXED FOR SYSTEM ROUTING** | `cashrail-delivery-orchestrator` is the named service owner. | A customer-specific human delivery owner is still required when the offer demands one. |
| B03 Security reviewer/capacity | **OPEN** | Review queue is named; capacity defaults to zero so availability cannot be fabricated. | Assign and verify a qualified reviewer before live work. |
| B04 Independent security/privacy review | **PARTIAL** | Runtime code receives static security and dependency checks in CI. | Customer evidence handling and each live deliverable still need an independent qualified review. |
| B05 Measured unit economics | **OPEN** | Unknown values fail closed. | Obtain measured reviewer time, delivery cost, fees, reserves, and collection data. |
| B06 Offer variants unsigned | **OPEN** | Draft variants remain drafts. | Controller may approve only after B03 and B05 produce evidence. |
| B07 Bot 1 payment path | **PARTIAL** | Stripe webhook signature, deduplication, and synthetic no-false-cash tests pass. | Authenticate the correct Cashrail Stripe account and complete a provider read-back test. |
| B08 Suppression/CRM runtime | **PARTIAL** | Durable hashed suppression registry now overrides caller assertions for external actions. | Connect an authoritative CRM/contact source and reconcile it before live sends. |
| B09 Qualified opportunity | **OPEN** | No candidate presently meets the evidence threshold. | A real deal blocker, owner, deadline, and evidence permission must be verified. |
| B10 First-wave approvals | **OPEN** | No messages have been approved or sent. | Requires an authorized standing policy for the exact first-wave class. |
| B11 Manifest unsigned | **CORRECTLY BLOCKED** | Signing endpoint refuses failed gates or non-empty blockers. | Clears automatically only when B01–B10/B12 are resolved and A–F pass. |
| B12 External-execution authority | **OPEN** | External execution remains disabled. | Explicit standing authorization is required before outreach, payment requests, contracts, charges, or spend. |

## Current determination

**NOT READY.** Bot 1 remains `STAGED`; `clock_ready = false`. This is a correct safety outcome, not a runtime failure.
