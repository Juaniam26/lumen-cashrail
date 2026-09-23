# Runtime Implementation Blockers

This file prevents the archive from being mistaken for the missing application.

## Not supplied and therefore not verified

- Canonical source repository and revision.
- Executable API service and provider adapters.
- Database migrations, constraints, transaction boundaries, and backup/restore test.
- Dependency lockfile, container image digest, SBOM, vulnerability scan, and signed artifact.
- Authentication/authorization implementation and audit-log access controls.
- Provider-backed payment, CRM, enrichment, DocuSign, Jev, or Grok connectivity.
- Runtime tests, load tests, chaos/restart tests, and security test output.
- Monitoring configuration, alert routing, on-call ownership, and retention enforcement.

## Minimum runtime contract

The missing implementation must satisfy the existing `shared/runtime-contract-v1.8.md`, `shared/execution-kernel-v1.8.md`, and `shared/gate-control-kit-v1.8.md`. In addition, it must reject:

- any request with unknown required economics;
- any attempt whose active BotAttempt is absent, expired, or not Controller-authorized;
- any Jev decision with a different opportunity ID, input hash, policy/economics version, expiry, or approved action set;
- any duplicate mutation without provider reconciliation;
- any budget reservation that would cross the configured cap;
- any live action without an authenticated actor and durable idempotency key.

The first implementation milestone is a no-send/no-charge synthetic rehearsal. Passing this file's checklist is necessary but does not itself establish live readiness.
