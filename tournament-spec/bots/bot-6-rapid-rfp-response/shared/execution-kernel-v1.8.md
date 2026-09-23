# Shared Execution Kernel v1.8

## Core invariants

1. Never fabricate a source, action, provider state, customer response, payment, cost, delivery, or result.
2. Keep distinct lifecycle states: `discovered → qualified → approved → queued → attempted → provider_accepted → delivered → replied → proposed → signed → invoiced → pending → cleared → fulfilled → reconciled`.
3. Provider-confirmed state wins over CRM or model memory. Contradictions freeze the affected action until reconciled.
4. Every external mutation uses an idempotency key, precondition snapshot, policy decision ID, and post-action provider receipt.
5. Every durable record includes bot/opportunity/customer IDs, timestamps, evidence IDs, source owner, freshness, policy/economics versions, actor, action, result, and immutable event hash.
6. No duplicate outreach, invoices, contracts, charges, refunds, or commitments after restart. Query provider state before retrying an uncertain mutation.
7. Suppression, security, identity, jurisdiction, capacity, economics, and authorization gates are fail-closed.
8. Customer obligations survive bot failure and tournament closure.

## Canonical durable state

Minimum entities: `Tournament`, `BotAttempt`, `Opportunity`, `Contact`, `ConsentSuppression`, `OfferVariant`, `Approval`, `ExternalAction`, `ProviderReceipt`, `Payment`, `Obligation`, `Evidence`, `JevDecision`, `Escalation`, and `Handoff`.

Each event stores `event_id`, `idempotency_key`, `entity_version`, `occurred_at`, `recorded_at`, `source_provider`, `source_record_id`, `input_hash`, `output_hash`, `policy_version`, `economics_version`, and `previous_event_hash`. Personally sensitive evidence is minimized, access-controlled, and retained only as required by approved policy.

## Execution loop

```text
START
→ recover durable state
→ reconcile uncertain provider actions
→ verify clock and active authority
→ verify tools, suppression, evidence freshness, capacity, economics
→ select one eligible action
→ obtain required gate decision
→ execute at most one external mutation
→ capture provider receipt
→ verify resulting state
→ update ledger and obligations
→ checkpoint
→ repeat or freeze/terminate
```

## Evidence classes

Label every statement as one of: sourced fact, assumption, calculation, configured state, synthetic test result, provider-confirmed action, externally verified state, collected revenue, or blocker. Evidence must be addressable by ID and include source, capture time, freshness limit, hash, and permitted use.

## Recovery and retries

- On context loss, read the last checkpoint and event log; never reconstruct state from conversational memory.
- On browser/service failure, mark the action `uncertain`, query provider state, and retry only when absence is proven and the same idempotency key is safe.
- Use bounded retries with jitter; after the configured limit, open a circuit, freeze the dependent workflow, and escalate.
- On expired login or missing credential, do not request secrets in chat or bypass access controls. Escalate through the approved credential owner.
- On automation blocking, stop automated attempts; use an approved manual/provider path or abandon the action.
- On unexpected prospect/customer response, pause templated follow-ups and route to the authorized response path.
- On low credits/capacity, stop before creating obligations; do not spend unverified or user funds.

## Checkpoint contents

Active bot and immutable deadline; canonical ledger totals; open obligations; uncertain actions; current opportunity rankings; suppression changes; capacity; tool health; Jev status; gate decisions; next safe action; escalation owner and deadline. A checkpoint is complete only after durable write and read-back verification.

## Handoff

Handoffs include only necessary data, lawful purpose, customer commitments, open risks, authoritative IDs, evidence, financial state, next deadline, and acceptance receipt from the receiving owner. No opportunity is double-owned, and no unresolved obligation is discarded.
