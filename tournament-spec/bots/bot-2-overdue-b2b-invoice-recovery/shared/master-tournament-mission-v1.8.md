# Grok Six-Bot Revenue Tournament — Master Mission v1.8 (Reconstructed)

## Status and authority

This is a production-ready control specification assembled from documented project context after the previously referenced source ZIP was found absent. It preserves the documented current architecture and marks unverified operating inputs rather than inventing them. It is a package for controlled preparation and later execution; it is not authorization to launch.

The Tournament Controller is the final authority for readiness, gates, freezes, bot activation/elimination, provider reconciliation, payment truth, and PASS/FAIL. Jev is advisory. Bots propose and execute only inside approved policy. Provider records are authoritative for sends, signatures, payments, refunds, disputes, and delivery evidence.

## Fixed tournament objective

- Six distinct bots run sequentially, beginning with Bot 1 when and only when all readiness gates pass.
- Each activated bot receives one immutable 72-hour wall-clock acquisition attempt. The clock never resets because a model, browser, or service restarts.
- Current documented target: at least **$10,000 verified net profit** within the active attempt.
- Zero user-provided capital; no borrowing, anticipated earnings, reimbursement assumptions, or cross-bot funds unless an explicit recorded tournament transfer policy allows it.
- Failure does not erase lawful customer obligations, delivery, support, refunds, or collections. It freezes new acquisition and triggers a terminal report and controlled transition.

## Accounting truth

Only provider-confirmed cleared cash can enter the profit ledger. A lead, reply, call, appointment, proposal, signature, invoice, funded intent, projected contract value, annualized savings, gross revenue, or pending payment is not verified profit.

```text
verified_net_profit =
  cleared_collected_cash
  - refunds
  - disputes
  - payment_fees
  - tax_reserve
  - chargeback_reserve
  - paid_variable_cost
  - accrued_fulfillment_cost
  - unearned_customer_obligations
  - reinvestment_spent
```

Every term must point to evidence IDs and an authoritative owner. Unknown is `null`, never zero. Assumptions may support planning but cannot authorize live execution or prove PASS.

## Pre-clock readiness gates

The 72-hour clock starts only when `clock_ready = true` and all gates have signed evidence:

1. **0A Shared-system preflight:** authenticated tools, provider read/write tests, canonical IDs, webhook/idempotency behavior, suppression controls, retention paths, outage fallbacks, and cost paths.
2. **0B Security and privacy:** independent review; critical findings block customer work; least privilege, secret handling, data minimization, and incident path verified.
3. **0C Economics and capacity:** measured fulfillment/reviewer time, approved prices and deposits, processor fees, reserves, delivery capacity, and no negative-margin variant.
4. **0D Qualified opportunity pool:** public-first qualification, evidence-backed signals, deduplication, and manually audited first wave. Enrichment tools are bounded gap-fillers only after public qualification and authenticated cost verification.
5. **0E Launch authority:** named Controller and backups; each first-wave destination, role, jurisdiction, suppression state, claim, offer, and final rendered message individually approved.
6. **0F Readiness manifest:** all preceding evidence current, hashes recorded, unresolved blockers zero, clock owner named, and manifest signed.

No fixed gate-completion date or named human is fabricated in this package. Those fields remain explicit launch blockers until supplied and verified.

## Activation, promotion, pause, and elimination

- `STAGED`: packet exists but live action is forbidden.
- `READY`: all bot-specific prerequisites pass but the bot is not active.
- `ACTIVE`: Controller records activation time, immutable deadline, approved variants, budget source, and live authorities.
- `FROZEN`: new external activity stops because a critical gate, provider contradiction, safety/security incident, authorization lapse, or accounting uncertainty occurred.
- `PASS`: authoritative ledger shows target met by deadline and obligations/reserves are accounted for.
- `FAIL`: deadline closes below target, an unrecoverable hard-stop condition occurs, or required evidence cannot be established. New acquisition stops; obligations continue.
- `PROMOTE`: Controller may expand only an already approved variant after real cleared-profit, quality, capacity, and complaint thresholds remain healthy.

## Non-negotiable conduct

No deception, impersonation, credential misuse, unauthorized access, fabricated proof, fake urgency, legal/compliance guarantees, harassment, spam, unlawful collection pressure, evasion of provider controls, or hidden subcontracting. Respect opt-outs and suppression globally. Never make a customer commitment that capacity, evidence, authority, and approved terms do not support.

## Tournament sequence

Bots remain staged in order 1–6. A terminal Bot does not silently activate the next. The Controller reconciles state, closes or transfers obligations, records learnings without customer data leakage, verifies the next bot's fresh readiness manifest, and then explicitly activates it. A passed bot may continue only under a separately recorded post-tournament authority; PASS is not blanket permission.

## Present package boundary

This package authorizes document assembly, testing, and readiness design only. It does not authorize outreach, account creation, contracting, invoicing, charging, spending, prospect contact, or launch. The explicit live authorization token and all gates would still be required outside this deliverable task.
