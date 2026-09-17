# Cashrail Event Ledger Contract

Cashrail may recommend actions, generate drafts, and track operator intent, but those activities are not proof that an external action occurred. The future Lumen runtime should persist revenue operations as append-only events and derive current status from those events.

## Core rule

**Assertion is not evidence.**

- A copied draft is not a send.
- A clicked `Mark sent` button is not a send.
- A manually entered dollar amount is not cash.
- A model statement that it searched the web is not source provenance.

The canonical schema is `schemas/revenue-event.schema.json`.

## Canonical progression

```text
opportunity.discovered
  -> evidence.verified
  -> message.drafted
  -> message.approved
  -> message.provider_accepted
  -> message.delivered
  -> message.replied
  -> lead.qualified
  -> agreement.signed
  -> payment.pending
  -> payment.verified
```

This is a common path, not a requirement that every opportunity emit every event. Failures and reversals remain explicit events:

- `message.failed`
- `message.unsubscribed`
- `payment.refunded`
- `cost.recorded`
- `opportunity.killed`

Never rewrite or delete a prior event merely to make a dashboard look current.

## Source evidence

A verified opportunity claim should retain the best available source evidence:

```json
{
  "source_url": "https://example.com/public-source",
  "source_record_id": null,
  "retrieved_at": "2026-09-17T12:00:00Z",
  "observed_fact": "Company posted a public opening notice."
}
```

When a provider record is the authoritative source, use its immutable record id. When live evidence cannot be obtained, mark the opportunity `blocked_no_live_source` rather than asking a model to fill the gap.

## Outbound evidence

`message.provider_accepted` is the earliest event that can substantiate a verified send attempt. It must include:

- provider name;
- provider message id;
- recipient;
- provider acceptance timestamp;
- opportunity id;
- campaign id when applicable.

Provider acceptance does not mean delivery. `message.delivered`, `message.failed`, `message.replied`, and `message.unsubscribed` are separate events.

Provider adapters should translate provider-native statuses into this canonical vocabulary and preserve raw provider metadata for diagnosis.

## Payment evidence

`payment.verified` requires immutable external evidence such as a processor transaction id, partner remittance id, bank settlement reference, or equivalent record.

At minimum record:

- settlement/payment provider;
- transaction id;
- gross amount;
- currency;
- opportunity/workstream attribution;
- verification time.

When known, also record fees, refunds, and net amount.

Manual cash entries may be useful operator notes, but they remain `unverified` and must not increase verified collected-cash totals.

## Costs and net contribution

Record directly attributable costs as events rather than hiding them in a static margin assumption.

Canonical calculation:

```text
net contribution
= verified gross cash
- partner payouts
- payment fees
- attributable data/outbound/model costs
- refunds
- other directly attributable costs
```

Do not create a universal percentage margin prior and call it observed Cashrail performance.

## Funnel diagnosis

Use observed stage counts to diagnose an experiment.

- Delivered, no replies: inspect list quality, sender health, channel, and message.
- Replies, no qualified conversations: inspect targeting and offer fit.
- Qualified, no signed agreement: inspect proof, economics, trust, and agreement friction.
- Signed, no verified cash: inspect close, attribution, fulfillment, and payment path.

The historical `zero replies after 18 hours = kill` rule is deprecated. Time still matters, but sample size and stage evidence determine what failed.

## Idempotency and duplicate prevention

The future application service should use stable event ids and provider transaction/message ids as idempotency keys. Replayed provider webhooks must not create duplicate cash or send events.

## Storage boundary

This repository defines the contract only. It does not contain the Lumen application's persistent event store. The event ledger must be implemented in the actual application repository with transactional server-side persistence before it can be considered operational.