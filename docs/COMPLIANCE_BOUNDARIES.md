# Cashrail Compliance Boundaries

This document records operating boundaries for the Cashrail tenant. It is a product/runtime constraint document, not legal advice.

## Commercial email

Before any provider dispatch, the application should enforce a shared outbound compliance layer rather than relying on individual model prompts.

At minimum, the send path should support:

- truthful sender/header information;
- non-deceptive subject lines;
- sender/business identification appropriate to the message;
- a valid postal address where required;
- a clear opt-out path;
- a suppression list checked before every send;
- prompt honoring of unsubscribe/stop requests;
- provider message ids and status events retained in the ledger.

The FTC's CAN-SPAM guidance applies to commercial email and does not provide a general B2B exemption. See: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business

## Partner revenue and payment routing

For third-party offers sold through the Partner Revenue Engine:

```text
customer -> partner's checkout/invoice -> partner receives cleared funds
partner -> Cashrail commission under signed attribution terms
```

Cashrail should not receive customer settlement proceeds for goods/services actually provided by a third party and then forward those funds onward. This avoids turning Cashrail into an undisclosed payment facilitator or aggregator.

Stripe's current restricted-business guidance includes payment facilitation/aggregation and receiving settlement proceeds for goods or services the Stripe user did not provide on behalf of third-party sellers as restricted/prohibited activity depending on the arrangement. See: https://stripe.com/legal/restricted-businesses

## B2B invoice collection

`third_party_invoice_collection` / historical L7A is **paused_compliance**.

Cashrail does not currently have an approved canonical workflow for acting as a third-party collector of overdue invoices. The active recovery product is stalled-proposal recovery, where the client keeps its customer relationship and receives its own payment.

Stripe lists debt collection agencies among prohibited business categories. That does not by itself determine whether every AR-support workflow is a collection agency, but it is sufficient reason not to let a model silently choose the boundary. See: https://stripe.com/legal/restricted-businesses

## Real estate

Real estate is disabled in the Cashrail runtime.

`handover/UNLICENSED_RULES.txt` is a stay-out/compliance boundary. It is not an authorization to perform brokerage work under another label.

South Carolina law restricts licensed activity and limits what unlicensed personnel may discuss, negotiate, or explain in real-estate transactions. Relevant statutory references include S.C. Code §40-57-135 and §40-57-710: https://www.scstatehouse.gov/code/t40c057.php

## Regulated professional fee sharing

Do not create percentage-based partner arrangements involving legal fees, medical referrals, regulated financial services, or another profession with fee-sharing restrictions unless that specific arrangement has been separately reviewed for the relevant jurisdiction and profession.

## Source and privacy boundaries

Allowed research should use public information, provider-authorized data, or client-supplied records the client is entitled to provide.

Do not use:

- leaked databases;
- hacked/private records;
- credential sharing as a substitute for delegated access;
- scraped personal contact data obtained in violation of provider or legal restrictions;
- fabricated evidence when a live source is unavailable.

If evidence cannot be verified, the opportunity should remain blocked or unverified.

## Owner approval and automation

A provider-backed automation may execute only the class of action the owner has authorized. The event ledger must still retain provider evidence.

High-consequence actions such as signing agreements, spending money, changing payment routing, or changing compliance policy remain explicit human decisions unless a future written operating contract deliberately changes that boundary.