# Cashrail Canonical Runtime Design

## Purpose

This repository is the canonical operating contract for the Cashrail revenue tenant inside the broader Lumen platform. It is not the Lumen application source tree, a settlement engine, a real-estate operation, or proof that any external provider action occurred.

The upgrade has four goals:

1. make one machine-readable file authoritative for what is active, paused, experimental, or disabled;
2. separate internal lane history from the customer-facing commercial services Lumen actually offers;
3. require external evidence before a send, payment, or source claim is treated as verified;
4. prevent stale handover documents from reactivating deprecated strategies.

## Verified Repository Boundary

The current repository contains a README plus handover text files, bot packets, and one-page agreements. It does not contain the TanStack Lumen application, `sovereign_bridge.py`, a database implementation, Stripe webhook code, or a provider-backed outbound service. Therefore this repository can define contracts and operating state, but it cannot honestly claim to implement those runtime services.

## Product Boundary

- **Lumen** is the platform/control plane: evidence, workflow state, provider integrations, revenue accounting, allocation, and operator UI.
- **Cashrail** is one revenue tenant/operating kit running inside Lumen.
- Internal lane numbers are historical implementation labels. They are not the primary customer-facing product architecture.

Customer-facing commercial surfaces map to internal workstreams as follows:

| Customer surface | Internal workstream | Historical lane source |
| --- | --- | --- |
| Signal Intelligence | Commercial-trigger intelligence | L3 |
| Account Mapping | Cross-cutting research/enrichment | shared |
| Outbound Distribution | Owned-offer distribution first | L5 |
| Revenue Leakage Review + B2B Recovery | Stalled-proposal recovery | L7B |
| Opportunity Windows + Close Support | Partner Revenue Engine | merged L1 + L8 |
| AI workflow install | Narrow, demonstrable automation install | L9 |

## Canonical Operating State

The authoritative state is `config/revenue-runtime.json`.

- Active: Signal Intelligence / L3, Partner Revenue / merged L1+L8, Stalled Proposal Recovery / L7B.
- Build: L9 automation install, demo-gated.
- Support: L5 distribution, prioritizing Lumen-owned offers before third-party products.
- Experimental: L2 Waste Share.
- Opportunistic: L4 bounties.
- Paused for compliance design: L7A third-party invoice collection.
- Disabled: L6 real estate.

The operating spend policy remains zero out-of-pocket until verified profit unless the owner explicitly changes that policy.

## Truth Model

Lumen must distinguish **operator assertions** from **provider-verified facts**.

### Source evidence

Every material opportunity claim should preserve:

- source URL or provider record id;
- retrieval timestamp;
- observed fact;
- verification status;
- the workstream and opportunity that consumed it.

If a live source cannot be verified, the correct state is `blocked_no_live_source`, not an invented fact.

### Outbound evidence

A message is not verified as sent merely because a draft was copied or an operator clicked a local button.

Verified outbound requires at minimum:

- provider name;
- provider message id;
- recipient identity;
- provider acceptance timestamp;
- associated opportunity/campaign id.

Delivery, bounce, reply, and unsubscribe are later events, not aliases for `sent`.

### Cash evidence

A payment is not verified revenue because an operator entered a number manually.

Verified cash requires:

- payment provider or settlement source;
- transaction id or equivalent immutable evidence;
- gross amount;
- fees/refunds when known;
- associated offer/workstream/opportunity;
- verification timestamp.

Manual entries may exist as unverified notes, never as verified cash.

## Event Ledger Contract

The desired platform flow is append-only:

`opportunity.discovered` → `evidence.verified` → `message.drafted` → `message.approved` → `message.provider_accepted` → `message.delivered` → `message.replied` → `lead.qualified` → `agreement.signed` → `payment.pending` → `payment.verified`

Failure/reversal events such as `message.failed`, `payment.refunded`, `cost.recorded`, and `opportunity.killed` are also append-only. Current truth is derived from events rather than overwriting history.

The exact schema is documented in `docs/EVENT_LEDGER_CONTRACT.md` and `schemas/revenue-event.schema.json`.

## Payment Boundary

For partner-sold offers, the customer pays the partner. Cashrail receives its agreed commission from the partner after attributable customer funds clear. Cashrail must not act as an undisclosed pass-through settlement account for goods or services it did not provide.

For Lumen-owned products/services, Lumen may use its own supported payment processor subject to that processor's business rules.

## Unit Economics

Revenue decisions optimize **net contribution**, not gross collected cash or theoretical split percentage.

`net contribution = gross cash - partner payouts - payment fees - attributable data/outbound/model costs - refunds - other directly attributable costs`

The allocator should eventually compare workstreams using observed data such as:

- net contribution per 100 verified deliveries;
- net contribution per operator hour;
- net contribution per dollar of attributable compute/data spend;
- median days to verified cash;
- delivered → replied → qualified → signed → paid conversion.

No conversion prior should be presented as empirical Lumen performance until enough actual observations exist.

## Experiment Kill Logic

The historical `zero replies after 18 hours` rule is deprecated. Kill/repair decisions should be based on funnel evidence and sample size.

Examples:

- delivered but no replies: inspect list quality, message, sender health, and channel;
- replies but no qualified conversations: inspect targeting/offer fit;
- qualified conversations but no signed economics: inspect trust, pricing, proof, and agreement friction;
- signed economics but no cash: inspect closing, attribution, fulfillment, or payment path.

Time still matters, but time alone is not a diagnosis.

## Compliance Boundaries

- Commercial email must pass suppression/opt-out and sender-identity checks in code before provider dispatch.
- L7A invoice collection remains paused until the operating model is confirmed not to create prohibited or licensed collection activity in the relevant jurisdictions and payment-provider rules are satisfied.
- Real estate remains disabled in Cashrail. `handover/UNLICENSED_RULES.txt` is a stay-out boundary, not a workaround guide.
- Law-firm fee-sharing and other regulated professional-fee arrangements are out unless separately reviewed for the relevant jurisdiction and fee structure.

## Apollo Integration State

Apollo is a valid provider candidate for research, enrichment, sequences, and provider-verifiable outbound. At audit time the connected Apollo workspace had no linked sending mailbox. Therefore the canonical state is **research-capable, send-not-ready** until a mailbox is linked and verified. No Apollo credits should be consumed merely to prove architecture.

## Implementation Phases

### Phase 0 — Canonicalize the operating kit

- add machine-readable runtime state;
- update handover packets to the current portfolio;
- mark stale Three-Lanes instructions deprecated;
- add secret-ignore rules;
- make payment/outbound/evidence boundaries explicit.

### Phase 1 — Evidence and event ledger in the actual Lumen app

Once the real application source repository is identified, implement the event schema server-side and persist immutable provider/payment evidence.

### Phase 2 — Provider-backed outbound

Add provider adapters that translate accepted/delivered/replied/bounced/unsubscribed states into ledger events. Apollo may be one adapter after sender setup is complete.

### Phase 3 — Payment reconciliation

Ingest processor/webhook or partner-settlement evidence, bind it to opportunities, and compute net contribution. Manual values stay unverified.

### Phase 4 — Allocation engine

Allocate effort from observed economics and funnel behavior rather than lane loyalty or fixed clocks.

### Phase 5 — Productize L9

Ship one narrow, demonstrable automation job with a three-minute run, week-one deliverable, scoreboard, and explicit send/spend approval rules before selling broader automation installs.

## Non-Goals

This repository upgrade does not:

- invent the missing Lumen application code;
- create `sovereign_bridge.py`;
- implement title/escrow or real-estate settlement;
- assert a $100k/week forecast;
- claim 10DLC/carrier costs that Cashrail is not currently incurring;
- claim Apollo can send before a sending mailbox is linked;
- claim cash unless external payment evidence exists.

## Acceptance Criteria

1. `config/revenue-runtime.json` is the single runtime-policy source of truth and parses as JSON.
2. Every active bot packet agrees with that runtime state.
3. Real estate is disabled everywhere active instructions are read.
4. L7A is visibly paused and L7B remains an active recovery product.
5. Partner revenue uses customer → partner → Cashrail commission, not customer → Cashrail pass-through settlement.
6. Verified outbound requires provider evidence.
7. Verified cash requires transaction evidence.
8. The README accurately states that this repo is an operating contract/handover kit rather than the full Lumen application.
9. Deprecated strategy files cannot reasonably be mistaken for current operating instructions.
10. The Google Drive forensic audit is rewritten to describe this verified architecture and the remaining implementation gap.