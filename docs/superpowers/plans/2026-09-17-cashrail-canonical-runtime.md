# Cashrail Canonical Runtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the Cashrail handover repository into one internally consistent, evidence-bound operating contract for the current Lumen revenue tenant.

**Architecture:** Keep this repository documentation/configuration-first because the actual Lumen application source is not present here. Establish `config/revenue-runtime.json` as the policy source of truth, define provider/payment/event contracts in docs/schema, and update legacy bot packets and agreements so they cannot contradict the canonical state.

**Tech Stack:** Markdown, plain-text operating packets, JSON, JSON Schema, GitHub review branch.

**Spec:** `docs/superpowers/specs/2026-09-17-cashrail-canonical-runtime-design.md`

## Global Constraints

- Do not invent application code that is not present in this repository.
- Spend policy remains zero out-of-pocket until verified profit unless explicitly changed by the owner.
- Verified send requires provider evidence; a manual status change is not proof.
- Verified cash requires transaction evidence; a manual number is not proof.
- L7A third-party invoice collection is paused pending compliance design.
- L6 real estate is disabled.
- Partner-offer customer payments go to the partner; Cashrail receives its commission separately.
- Preserve historical files when practical; mark stale instructions deprecated rather than silently deleting history.

---

### Task 1: Canonical runtime and event contracts

**Files:**
- Create: `config/revenue-runtime.json`
- Create: `schemas/revenue-event.schema.json`
- Create: `docs/EVENT_LEDGER_CONTRACT.md`
- Create: `docs/COMPLIANCE_BOUNDARIES.md`
- Create: `docs/INTEGRATION_GAPS.md`

**Interfaces:**
- Consumes: policy decisions in the design spec.
- Produces: canonical workstream statuses; event names/required evidence; integration readiness states used by every handover packet.

- [ ] **Step 1: Create a machine-readable runtime policy**

Define Lumen as platform, Cashrail as tenant, active/build/support/experimental/paused/disabled workstreams, zero-spend policy, provider-verification requirements, and payment-routing rules.

- [ ] **Step 2: Validate the runtime JSON**

Parse the exact file content with a JSON parser. Expected: exit success and no duplicate/invalid syntax.

- [ ] **Step 3: Create the event JSON Schema**

Require `event_id`, `event_type`, `occurred_at`, `tenant`, `workstream`, `opportunity_id`, `verification`, and event-specific evidence payloads while allowing provider-specific metadata.

- [ ] **Step 4: Validate the schema JSON**

Parse the exact schema file with a JSON parser. Expected: exit success.

- [ ] **Step 5: Document ledger and compliance semantics**

Define append-only event progression, source/outbound/payment evidence, net contribution, CAN-SPAM middleware, payment-provider boundaries, paused collections, and disabled real estate.

- [ ] **Step 6: Document integration gaps**

State explicitly that this repository lacks the Lumen application, persistence implementation, outbound adapter, and payment reconciliation code; record Apollo as research-capable/send-not-ready until a mailbox is linked.

- [ ] **Step 7: Commit and read back the created files**

Expected: all five files exist on the review branch and match the intended policy.

### Task 2: Repair repository entry points

**Files:**
- Create: `.gitignore`
- Modify: `README.md`
- Modify: `handover/00_START_HERE.txt`
- Modify: `handover/THREE_LANES_START.txt`

**Interfaces:**
- Consumes: `config/revenue-runtime.json`.
- Produces: one human-readable entry path that agrees with the machine-readable state.

- [ ] **Step 1: Add secret-safe ignore rules**

Ignore `.am_key`, environment files, private-key formats, secret directories, local build/dependency artifacts, and macOS metadata.

- [ ] **Step 2: Rewrite README around the verified repository boundary**

State that this repo is the Cashrail operating contract, not the full Lumen app. Remove references to missing tracker/playbook/script files as if they exist. Link canonical config/contracts and current handover packets.

- [ ] **Step 3: Replace stale start instructions**

Activate L3, merged L1/L8, and L7B; set L5 support, L9 build-demo, L2 experimental, L4 opportunistic, L7A paused, L6 disabled. Remove the old six-bot/L6 startup flow.

- [ ] **Step 4: Deprecate Three-Lanes instructions in place**

Preserve the file for history but make the first line unambiguously state that it is deprecated and redirect readers to `config/revenue-runtime.json` and `handover/00_START_HERE.txt`.

- [ ] **Step 5: Read back all entry-point files**

Expected: no active instruction tells the operator to enable real estate, invoice collection, or the obsolete five-lane default.

### Task 3: Align active bot packets with the canonical portfolio

**Files:**
- Modify: `handover/bots/00_REVENUE_DESK.txt`
- Modify: `handover/bots/03_DATA_MILL.txt`
- Modify: `handover/bots/05_DISTRO_SPLIT.txt`
- Modify: `handover/bots/07_CASH_RECOVERY.txt`
- Modify: `handover/bots/08_SPLIT_CLOSER.txt`
- Modify: `handover/bots/09_INSTALL_SELLER.txt`

**Interfaces:**
- Consumes: canonical runtime status, event truth model, payment boundary.
- Produces: executable human/agent instructions that cannot elevate drafts/manual statuses into verified sends or cash.

- [ ] **Step 1: Rewrite Revenue Desk coordinator**

Use customer-facing workstreams, funnel evidence, append-only state terminology, and provider/payment proof requirements. Remove the `18 hours = kill` rule.

- [ ] **Step 2: Upgrade L3 to commercial-trigger intelligence**

Require source URL, observed event, buyer consequence, relevant vendor/buyer category, and verification status. Keep low-ticket starter products but design toward repeatable recurring feeds.

- [ ] **Step 3: Reposition L5 as a distribution layer**

Prioritize Lumen/Cashrail-owned offers. Allow third-party distribution only under signed attribution terms. Never route third-party customer settlement through Cashrail.

- [ ] **Step 4: Split L7 behavior**

Make stalled-proposal recovery the active product. Mark third-party invoice recovery paused pending compliance review. Do not give live collection instructions.

- [ ] **Step 5: Merge L1/L8 into Partner Revenue Engine**

Retain the `08_SPLIT_CLOSER.txt` path for compatibility, but state that it is the canonical merged engine. Require proven offer, attribution, partner-owned checkout, and commission paid after cleared funds.

- [ ] **Step 6: Keep L9 demo-gated**

Require one narrow job, a three-minute live/recorded demo, week-one deliverable, scoreboard, and explicit send/spend approval policy before outreach.

- [ ] **Step 7: Cross-read all packets**

Expected: packet statuses and payment/outbound truth rules agree with `config/revenue-runtime.json`.

### Task 4: Align commercial agreements

**Files:**
- Modify: `handover/agreements/SPLIT_CLOSE_AGREEMENT.txt`
- Modify: `handover/agreements/CASH_RECOVERY_AGREEMENT.txt`
- Modify: `handover/agreements/DISTRO_SPLIT_AGREEMENT.txt`
- Modify: `handover/agreements/INSTALL_AGREEMENT.txt`

**Interfaces:**
- Consumes: payment boundary and active workstream scope.
- Produces: one-page operating agreements that do not imply pass-through settlement or active third-party debt collection.

- [ ] **Step 1: Convert Split Close to Partner Revenue Agreement**

State that the partner contracts/invoices the buyer and receives buyer funds. Cashrail invoices/is paid its sourced-revenue share separately after cleared funds.

- [ ] **Step 2: Narrow Cash Recovery Agreement to stalled proposals**

Remove active past-due-invoice collection scope. Keep client-owned checkout/payment path and compensation tied to attributable first payments.

- [ ] **Step 3: Update Distribution Agreement**

Make owned-offer distribution the default internal model; for third-party offers, require unique attribution and owner/platform-owned checkout.

- [ ] **Step 4: Tighten Install Agreement**

Require the specific demonstrated job and measurable week-one output. Keep revenue guarantees explicitly excluded.

- [ ] **Step 5: Read back all modified agreements**

Expected: no agreement instructs Cashrail to receive and forward third-party customer settlement proceeds.

### Task 5: Repository verification and review handoff

**Files:**
- Verify all changed files on `audit/canonical-runtime-2026-09-17`.

**Interfaces:**
- Consumes: Tasks 1–4.
- Produces: reviewable pull request and evidence of internal consistency.

- [ ] **Step 1: Fetch every changed file from the branch**

Expected: connector returns the new branch version for each path.

- [ ] **Step 2: Parse JSON documents independently**

Expected: both runtime config and event schema parse cleanly.

- [ ] **Step 3: Search the branch for forbidden/stale active concepts**

Check active instructions for `L6`, `real estate`, `18 hours`, `customer -> Cashrail -> partner`, and any claim that Apollo sending is live. Historical/deprecation references are allowed only when clearly labeled.

- [ ] **Step 4: Compare branch against main**

Expected: only intended docs/config/handover files change; no unrelated files are removed.

- [ ] **Step 5: Open a pull request**

Summarize verified findings, the intentionally unimplemented runtime gap, and the next required integration into the actual Lumen application repository.

### Task 6: Rewrite and verify the Google Drive forensic audit

**Files:**
- Update in place: `Lumen Canonical Integration - Forensic Audit & Architecture Upgrade`

**Interfaces:**
- Consumes: verified repo state, completed review branch, official current compliance sources, observed Apollo readiness.
- Produces: a forensic audit that describes the real architecture, separates verified facts from recommendations, and points to the concrete repo upgrade.

- [ ] **Step 1: Replace unsupported architecture claims**

Remove `sovereign_bridge.py`, current 10DLC decay, Joint Escrow Instructions, title/escrow settlement, and $100k/week feasibility as asserted facts.

- [ ] **Step 2: Document correct platform/tenant boundary**

Lumen = platform/control plane; Cashrail = revenue tenant/operating kit.

- [ ] **Step 3: Document canonical commercial portfolio and truth model**

Include active/support/build/experimental/paused/disabled states and provider/payment evidence requirements.

- [ ] **Step 4: Add source-backed compliance boundaries**

Use official FTC, Stripe, and South Carolina sources; label legal/business-process recommendations as boundaries, not legal determinations.

- [ ] **Step 5: Link the review branch/pull request**

Record the concrete repository upgrade rather than a hypothetical blueprint.

- [ ] **Step 6: Read back the edited Google Doc**

Expected: the document no longer claims nonexistent code or real-estate settlement infrastructure, and its canonical state matches the repository.