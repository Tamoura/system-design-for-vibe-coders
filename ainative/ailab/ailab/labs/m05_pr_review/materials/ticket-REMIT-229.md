# REMIT-229: loyalty discount on transfer fees

**From:** Hessa, Product Owner, Najm Remit
**To:** Payments Platform
**Priority:** Normal

> Constructed for teaching: this ticket was written for the course. Najm Bank, Remit and every number in it are fictional.

Our silver and gold customers should pay less in fees. `Customer.loyalty_tier` already
exists (`none`, `silver`, `gold`) but nothing uses it yet.

## Rules

1. Silver customers get **10%** off the fee. Gold customers get **20%** off. Customers with
   tier `none` pay exactly what they pay today.
2. The discount applies to the **base fee**, that is the fee after the schedule's minimum
   and cap. The **express surcharge is never discounted**.
3. The discount amount is the base fee times the rate, **rounded half up to 2 decimals**,
   like every amount in Remit. The customer pays the base fee minus the discount.
4. The discount can never take the base fee **below the schedule's minimum**. If it would,
   charge the minimum.
5. An **unknown tier is an error** (`ValueError`), not "no discount": a typo must never
   silently charge full price.
6. Nothing else about fees changes.

## Examples (QAR-INR, schedule STD-A, minimum fee 5.00)

| Send amount | Base fee | Silver pays | Gold pays | Why |
|---|---:|---:|---:|---|
| 100.00 | 5.00 | 5.00 | 5.00 | already the minimum |
| 670.00 | 15.05 | 13.54 | 12.04 | the silver discount, 1.505, rounds up to 1.51 |
| 1,000.00 | 20.00 | 18.00 | 16.00 | |
| 1,000.00 express | 20.00 | 33.00 | 31.00 | 18.00 + 15.00 and 16.00 + 15.00 |

## Where

* `fees.quote_fee` and `fees.explain_fee` take a keyword `loyalty_tier` (default `"none"`).
* `RemitService.send` charges the customer's own tier. `RemitService.quote` takes an
  optional `customer_id` and prices that customer's tier.
* The transfer's fee, the ledger postings and the customer's notification all use the
  discounted fee.

## Definition of done

* A test for every rule above.
* Money is `Decimal`; no new dependencies; no secrets (see `CONTRIBUTING.md`).
* Money logic: a second human reviewer. AI-assisted changes carry the `AI-assisted` label.
