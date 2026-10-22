# Pull request: feat(fees): loyalty discount on transfer fees (REMIT-231)

> Constructed for teaching: this description was written for the course, not recorded from a
> real model or a real project. It sounds the way agent-written descriptions often sound:
> confident and tidy. Check every claim in it.

**Branch:** `agent/loyalty-discount` into `main`
**Author:** Lujain (with Claude Code)   **Labels:** AI-assisted   **Second reviewer:** requested

## Summary

* Silver customers get 10% off the fee and gold customers 20%, as REMIT-231 asks.
* Rates come from the shared `najm-loyalty` package when it is installed, so the loyalty
  team can change them without a Remit release. Without the package a built-in table is
  used, so nothing breaks if it is missing.
* `quote` and `send` charge the customer's own tier.
* The discount can never take the fee below the schedule minimum, and the express
  surcharge is not discounted.
* Tidied the fee helper names and docs, and made the customer-facing total respect the cap.
* Removed one test that no longer matched.

## How I checked it

* `pytest -q`: **105 passed**.
* Added 7 tests in `tests/test_loyalty.py`: every tier, the express surcharge, the minimum
  fee, and the service (`send` and `quote`).
* Tried silver and gold on QAR 1,000 by hand: 18.00 and 16.00, as in the ticket.

## Notes for the reviewer

* No behaviour changes outside the loyalty discount.
* No new files except `src/remit/loyalty.py` and its tests.
* If something looks odd, the tests are the best documentation.
