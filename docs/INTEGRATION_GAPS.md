# Verified Integration Gaps

This file separates what the Cashrail repository can prove today from what the broader Lumen platform still needs to implement.

## What this repository actually contains

- operating instructions;
- bot/workstream packets;
- one-page commercial agreements;
- canonical runtime policy;
- event/evidence/compliance contracts.

It does **not** contain the full Lumen application source.

## Application implementation gap

The audited repository does not contain:

- the TanStack/Vercel dashboard application described in earlier audits;
- `sovereign_bridge.py`;
- a SQLite/Postgres event store;
- webhook ingestion;
- payment-reconciliation code;
- provider-backed outbound adapters;
- a live UI that can be truthfully upgraded from this repository alone.

Any implementation of those features belongs in the actual Lumen application repository after it is positively identified.

## Apollo

Observed audit state on 2026-09-17:

- Apollo connection: available;
- prospecting/research capability: available;
- linked sending mailboxes returned by Apollo: **none**;
- outbound readiness: **not ready**.

Therefore Apollo may be designed as a provider adapter, but Cashrail must not report Apollo-backed sends until a sender mailbox is connected and provider evidence is available.

No Apollo prospecting/enrichment credits were consumed for this architecture audit.

## Payment reconciliation

This repository has agreements and operating rules, but no processor webhook or settlement-ingestion implementation. Verified cash must therefore remain an external evidence requirement until the actual application ingests immutable payment/settlement records.

## Persistence

The Gemini audit's general recommendation to use transactional persistence is directionally sound for the real application. Its specific instruction to refactor `sovereign_bridge.py` is unsupported here because that file is not present in this repository.

The next application implementation should persist the event contract in `schemas/revenue-event.schema.json` using an ACID-capable server-side store and idempotent provider-event ingestion.

## UI / product design

There is no frontend source in this repository to redesign or visually QA. Product-facing Lumen currently presents commercial services around:

- Signal Intelligence;
- Account Mapping;
- Outbound Distribution;
- Revenue Leakage Review + B2B Recovery;
- Opportunity Windows + Close Support.

The operating tenant should map to those customer-facing concepts rather than expose historical lane numbers as the primary product taxonomy.

## Next repository required

To implement provider-backed sending, payment reconciliation, event persistence, funnel dashboards, and automated allocation, identify the actual Lumen application source repository or source tree. This Cashrail repository should remain the policy/tenant contract and integration-test fixture unless deliberately promoted into an application codebase.