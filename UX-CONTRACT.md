# Cashrail Control Room UX Contract

## Purpose

The control room is a read-only explanation and status surface. It never starts a bot, sends outreach, approves a charge, signs a contract, spends money, or changes Controller policy.

## Authoritative sources

| Concern | Source |
|---|---|
| Bot lifecycle and 72-hour clock | `tournament-spec/shared/master-tournament-mission-v1.8.md` |
| Controller and Jev authority | `AUTONOMOUS-OPERATING-POLICY.md` |
| Runtime status | `GET /v1/control-room/snapshot` |
| Verified money | Provider-confirmed ledger values only |

## Observable behavior

- Initial load reserves the final layout and shows “Checking Cashrail…” in the status region.
- Successful refresh labels the view “Live read-only snapshot” and shows the update time.
- Failed refresh keeps the explanatory Bot 1 readiness report visible, labels it “Last known report,” and offers a real Retry button.
- “Run readiness check again” recomputes the six gates without activating a bot, starting its clock, or performing an external action. It reports the fresh gate count and preserves the prior report if the check fails.
- “Show me how it works” starts a clearly labeled sample walkthrough. It never changes runtime state.
- The six bot stations remain in sequence. Only one may be described as active.
- Money remains $0 until the snapshot reports provider-confirmed cleared cash.
- Keyboard focus is visible, reduced motion disables transitions, and narrow screens use a vertical rail.
