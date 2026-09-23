# Jev Supervisory and Profit-Routing Architecture v1.8

## Mission and boundary

Jev is a shared advisory profit-routing and loss-avoidance layer, not a seventh bot. It cannot browse for source truth, execute tools, authorize external actions, mark money collected, declare profit, override gates, extend the clock, create prices/terms, or activate/eliminate a bot.

```text
authoritative provider/evidence state
→ deterministic economics and capacity engine
→ Jev bounded routing recommendation
→ Grok execution proposal
→ Controller policy/gate decision
→ provider action if authorized
→ provider reconciliation and durable outcome
```

## Optimization order

Cleared cash; verified net profit after all deductions/obligations; probability of collection inside the deadline; profit per remaining action hour; safe capacity; then speed where it improves the preceding measures. Lead count, replies, proposals, gross value, annualized savings, activity, and Jev confidence are not success measures.

## Deterministic input envelope

Required: opportunity/bot IDs, evidence IDs/freshness, approved variants, `expected_collected_revenue`, `probability_of_collection`, `probability_of_collection_by_deadline`, `time_to_collection`, `fixed_variable_cost`, `payment_fee`, `refund_dispute_reserve`, `tax_reserve`, `customer_obligation`, `reinvestment_spent_for_this_opportunity`, `available_capacity`, `reviewer_capacity`, `estimated_fulfillment_hours`, `estimated_remaining_action_hours`, `hours_remaining`, `current_cleared_cash`, and `current_verified_net_profit`.

```text
expected_cleared_cash = expected_collected_revenue × probability_of_collection_by_deadline
expected_verified_profit = expected_cleared_cash - payment_fee - refund_dispute_reserve
  - tax_reserve - fixed_variable_cost - customer_obligation
  - reinvestment_spent_for_this_opportunity
profit_per_remaining_hour = expected_verified_profit /
  max(estimated_remaining_action_hours, minimum_time_denominator)
```

The engine calculates; Jev never infers missing economics from prose. If collection-by-deadline, expected profit, capacity, or reviewer capacity is null, route to `DEEP_REVIEW` without Jev. If hours remaining is null, `STOP`. Unknown secondary fields remain null.

## Allowed recommendations

`PURSUE`, `PURSUE_WITH_SMALLER_SCOPE`, `REQUIRE_APPROVED_DEPOSIT`, `SELECT_APPROVED_OFFER_VARIANT`, `RAISE_TO_APPROVED_PRICE_VARIANT`, `DEEP_REVIEW`, `STOP`, `REALLOCATE`.

For active pursuit, documented minimums are: collection-by-deadline probability ≥ 0.70; expected verified profit ≥ $10,000; positive profit per remaining hour; sufficient delivery and reviewer capacity. Controller may tighten. If profit meets target but collection probability is below 0.70, require an approved deposit or deep review. If the current opportunity is non-positive and another eligible one is positive, reallocate. If none qualifies, stop.

## Decision record and expiry

Retain decision ID, bot/opportunity, input hash, evidence IDs, policy/economics versions, alternatives, recommendation, signals/confidence, reason codes, timestamp/expiry, provider response ID/hash, Controller disposition, provider result, realized cash/cost/obligation/profit.

A decision expires on material evidence/payment/capacity/suppression/offer/policy/economics change, infeasible remaining time, attempt closure, or four hours—whichever is first. Expiry halts the dependent action and requires recomputation. If unavailable, deterministic hard gates and ranking govern; never invent a Jev result.

## Rollout and proof

Jev compatibility remains unverified until authenticated REST/MCP connectivity, schema, cost, rate-limit, retry, timeout, redaction, data handling, malformed-response, injection, and fallback tests pass. Start in shadow mode on historical/synthetic opportunities. Exit only after at least 10 completed opportunities or 30 days, whichever comes first, with: no worse false-positive pursuit rate than baseline; false-negative stop rate no more than baseline +5 percentage points; API cost below expected profit improvement per decision; and zero schema violations or unauthorized/unapproved recommendations. Only then may the Controller authorize bounded routing influence.
