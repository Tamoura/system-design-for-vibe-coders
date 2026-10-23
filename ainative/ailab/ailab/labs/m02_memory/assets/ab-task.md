# REMIT-252: machine-readable quotes (`quote --json`)

**From:** Hessa, Product Owner, Najm Remit
**To:** Payments Platform
**Priority:** Medium

The mobile team wants to read a quote from the command line without parsing our text layout. This ticket is the
task for the A/B experiment in REMIT-251: do it twice, once without project memory and once with it. Do it in the
throw-away copies, never in the directory you grade.

## What I need

1. `python -m remit quote QAR 500 INR --json` prints the quote as **one line of JSON** and nothing else, with
   these keys: `corridor` (for example `"QAR-INR"`), `delivery`, `express` (true or false), `send`, `fee`,
   `total`, `receive` and `rate`.
2. `send`, `fee`, `total` and `receive` are objects with an `amount` and a `currency`, and both are **strings**:
   `{"amount": "500.00", "currency": "QAR"}`. The `rate` is a string too, exactly as the text output shows it
   (`"22.5720"`). The mobile team must never receive a number that has been through a float.
3. Without `--json` the output is byte for byte what it is today. Errors still print `error [code]: message` on
   stderr, print nothing on stdout, and exit with status 1.
4. The new behaviour comes with tests, in the team's usual place and style.
5. Commit it, with a message that follows the team's rules.

## Out of scope

Only `quote` gets the flag. `send` and `history` stay as they are. No new dependencies.
