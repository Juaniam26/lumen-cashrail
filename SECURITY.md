# Security Policy

## Supported release

The `1.x` Cashrail takeover control plane is supported. Live execution remains disabled until deployment-specific readiness evidence is approved.

## Reporting

Do not open a public issue containing credentials, customer data, payment data, exploit details, or provider receipts. Report privately to the repository owner through GitHub's private vulnerability reporting when enabled.

## Security invariants

- Never commit `.env`, controller tokens, Stripe secrets, OAuth tokens, or customer evidence.
- Use vault-managed, environment-specific secrets and a restricted Stripe key when a reconciliation worker is added.
- Keep `CASHRAIL_ENABLE_LIVE_EXECUTION=false` through build, migration, smoke testing, and rollback validation.
- Treat unknown financial inputs as blockers; they are never zero.
- Verify Stripe signatures, deduplicate provider events, and reconcile provider state before crediting cleared cash.
- Never retry an uncertain external mutation until provider state proves the first attempt did not complete.
