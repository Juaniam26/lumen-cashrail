# Lumen Cashrail

Cashrail is the **revenue operating tenant / policy kit** for Lumen.

This repository is deliberately small. It contains operating rules, workstream packets, commercial one-pagers, and machine-readable contracts. It is **not** the full Lumen application source tree and must not be treated as proof that provider sends, payment reconciliation, database persistence, or UI features already exist.

## Canonical source of truth

Read these in order:

1. [`config/revenue-runtime.json`](config/revenue-runtime.json) — machine-readable active/paused/disabled state.
2. [`handover/00_START_HERE.txt`](handover/00_START_HERE.txt) — operator start path.
3. [`docs/EVENT_LEDGER_CONTRACT.md`](docs/EVENT_LEDGER_CONTRACT.md) — what counts as evidence for source, outbound, and cash.
4. [`docs/COMPLIANCE_BOUNDARIES.md`](docs/COMPLIANCE_BOUNDARIES.md) — hard operating boundaries.
5. [`docs/INTEGRATION_GAPS.md`](docs/INTEGRATION_GAPS.md) — capabilities that still belong in the actual Lumen application repository.

If a historical handover file conflicts with `config/revenue-runtime.json`, the runtime file wins.

## Current commercial portfolio

| Customer-facing route | Internal workstream | State |
| --- | --- | --- |
| Signal Intelligence | commercial-trigger intelligence / historical L3 | active |
| Account Mapping | shared research/enrichment layer | active support |
| Opportunity Windows + Close Support | Partner Revenue Engine / merged L1 + L8 | active |
| Revenue Leakage Review + B2B Recovery | stalled-proposal recovery / L7B | active |
| Outbound Distribution | owned-offer distribution / L5 | support |
| AI Workflow Install | narrow automation install / L9 | build, demo-gated |
| Waste Share | L2 | experimental |
| Bounties | L4 | opportunistic |
| Third-party invoice collection | L7A | paused for compliance design |
| Real estate | L6 | disabled |

## Truth rules

- A draft, copied message, or local `Mark sent` state is **not** a verified send.
- Verified outbound requires provider evidence such as a provider message id.
- A manually entered dollar amount is **not** verified cash.
- Verified cash requires immutable payment/settlement evidence.
- A model claiming it searched is **not** source provenance; preserve the source URL/provider record and retrieval time.
- Optimize for **net contribution**, not gross revenue or a theoretical split percentage.

## Payment boundary

For a partner's offer:

```text
customer -> partner checkout/invoice -> partner receives cleared funds
partner -> Cashrail commission under signed attribution terms
```

Cashrail does not use its payment account as a pass-through settlement account for another seller's goods or services.

## Spend policy

Default: **$0 out of pocket until verified profit** unless the owner explicitly changes the policy.

No paid ads, inventory, trading bankroll, fake proof, impersonation, leaked data, or selling a product that does not exist.

## Repository map

- `config/` — canonical runtime policy.
- `schemas/` — event/evidence contracts for future Lumen application integration.
- `docs/` — architecture, compliance, and integration boundaries.
- `handover/bots/` — compatibility packets for current workstreams.
- `handover/agreements/` — short commercial operating agreements.
- `handover/UNLICENSED_RULES.txt` — real-estate stay-out boundary; real estate remains disabled.
- `handover/THREE_LANES_START.txt` — retained only as a deprecated historical redirect.

## Integration state

Apollo can currently support research/prospecting through the connected workspace, but the audit found **no linked sending mailbox**, so Apollo outbound is not yet a verified send path. Payment reconciliation and the persistent event ledger are likewise not implemented in this repository.

See [`docs/INTEGRATION_GAPS.md`](docs/INTEGRATION_GAPS.md) before claiming an integration is live.
