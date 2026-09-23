# Gate-Control Kit v1.8

## Authority matrix

| Action | Bot may prepare | Controller may approve | Human/specialist required | Default |
|---|---:|---:|---:|---|
| Public research and internal scoring | Yes | Policy preapproval | No | Allowed internally |
| Enrichment lookup | Yes | Auth/cost/scope verified | Privacy review if novel | Fail closed |
| Draft outreach/proposal/contract/invoice | Yes | Yes | Legal/specialist for novel terms | Draft only |
| Send outreach or customer message | No | Yes | First wave/novel class approval | Blocked |
| Change approved price/scope/deposit | No | Select approved variant only | New policy owner for novel variant | Blocked |
| Sign/accept terms or create commitments | No | Within explicit authority only | Authorized signer/legal as required | Blocked |
| Create/send invoice or payment request | No | Yes after payment/economics gates | Finance if novel method | Blocked |
| Charge/refund/move payout destination | No | Bounded approved workflow | Authorized payment owner | Blocked |
| Spend/reinvest cleared bot funds | No | Within recorded ceiling | User for out-of-policy spend | Blocked |
| Handle credentials/secrets | No | Route only | Credential owner/security | Never in model context |
| Activate/eliminate bot or declare PASS | No | Controller only | Audit evidence required | Blocked |

## Mandatory gate order for an external action

`ACTIVE AUTHORITY → CLOCK → IDENTITY → JURISDICTION/CONSENT → SUPPRESSION → EVIDENCE FRESHNESS → OFFER/POLICY → ECONOMICS → CAPACITY → SECURITY/QUALITY → ACTION APPROVAL → PROVIDER EXECUTION → RECEIPT/RECONCILIATION`.

Any `false`, `null`, stale, contradictory, or missing required field blocks the action. The Controller may tighten but never weaken thresholds during an attempt.

## Freeze triggers

Critical security/privacy finding; uncertain duplicate mutation; provider/CRM disagreement about payment or send; suppression breach; unauthorized commitment; unverified payout change; negative or unknown unit economics; insufficient fulfillment/reviewer capacity; evidence tampering; complaint spike; material legal/jurisdiction ambiguity; Jev recommending an unapproved action; clock uncertainty.

Freeze means: stop new external activity, preserve evidence, protect customers, reconcile provider state, record scope and owner, continue only necessary lawful obligations, and require a documented unfreeze decision.

## Escalation tiers

- Tier 1 Controller: ordinary gate conflict, tool outage, stale evidence, capacity reallocation.
- Tier 2 Specialist: security, privacy, quality, accessibility, legal, collections, cloud, telephony, or RFP review beyond approved checklist.
- Tier 3 User/policy owner: new policy, capital spend, payout destination, identity/legal ambiguity beyond specialist authority, or agreement outside approved variants.
- Emergency: security incident, suspected fraud, unauthorized charge/contact, or material customer harm—freeze immediately and invoke incident response.

Routine lead, message, price, dashboard, and ordinary approved-variant decisions do not go to the user.
