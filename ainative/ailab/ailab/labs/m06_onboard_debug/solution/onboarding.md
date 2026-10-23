# A tour of Najm Remit for the next new engineer

Everything below was checked against the code on the day it was written, by opening the files. Where
a document and the code disagree, the code wins and the tour says so.

## What Remit is

Najm Remit lets the bank's customers in Qatar send money home. It prices a transfer (fee and exchange
rate), checks the customer's sending limits, screens the sender and the recipient against a watchlist, posts
the ledger entries, stores the transfer and tells the customer in English or Arabic. It is a small Python 3.11
service that uses only the standard library (SQLite through `sqlite3`) plus `pytest` for tests. Everything in
it, the bank, the customers and the numbers, is fictional.

## Entry points

- **The command line:** `python -m remit` (`src/remit/__main__.py` calls `main()` in `src/remit/cli.py`). It needs
  `PYTHONPATH=src` or `pip install -e .`. Commands: `customer add|list`, `quote`, `send`, `history`.
- **The library:** `RemitService` in `src/remit/service.py`. `quote()` prices a transfer without sending it;
  `send()` runs the whole flow. If you read one file, read this one.
- **Settings** come from environment variables read by `src/remit/config.py` (`REMIT_DB`, `REMIT_AUDIT_LOG`,
  `REMIT_WATCHLIST`, `REMIT_LANG`, `REMIT_ENV`); `.env.example` lists them. There is no `.env` loader.

## Data flow

`RemitService.send()` runs these steps in this order and stops at the first failure:

1. **validate**: the customer exists, the recipient is named, the corridor, amount and delivery method are allowed.
2. **limits**: `check_limits` in `limits.py` compares what the customer has already sent today and this month with
   the limits of their KYC tier. Over the limit raises `LimitExceeded`.
3. **screening**: `screening.py` checks the sender's and the recipient's names. A hit raises `ScreeningHit`.
4. **fee**: `fees.py` prices the transfer.
5. **fx**: `fx.py` gives the customer rate; a quote is good for 60 seconds.
6. **ledger**: `ledger.py` posts the double entries.
7. **store**: `store.py` saves the transfer in SQLite.
8. **notify**: `notify.py` sends "transfer sent" in the customer's language. This step is best effort: a failure
   is audited, and the transfer still stands.

Time comes from an injected clock and ids and audit events from `najmkit` (`docs/najmkit.md`), never from
`datetime.now()` or `uuid` in service code.

## Tests

Run `pytest -q` from the repository root (`pyproject.toml` puts `src` on the path). There is one test file per
module in `tests/`. `tests/conftest.py` makes everything deterministic: a fixed clock (Monday 2 March 2026, 09:00 UTC),
sequential ids, an in-memory store, three customers and a notifier, and it wipes the ledger's global state.
The money, fees, fx, limits and notify modules are tested thoroughly. The service is tested lightly.
**`ledger.py` and `screening.py` have no tests of their own**; they are only exercised through `send()`.

## Risks and gaps

- `ledger.py` and `screening.py` are legacy, untested modules. The ledger keeps its state in module-level
  variables, and its partner share rounds half-even while the rest of Remit rounds half-up. Do not change either
  without characterization tests first.
- Money is always `Decimal`, never `float`, through the `Money` class. Money logic (`money.py`, `fees.py`, `fx.py`,
  `limits.py`, `ledger.py`, `service.py`) needs a second human reviewer (`CONTRIBUTING.md`).
- `Store.search_by_name` builds its SQL by string formatting, unlike every other query; a known smell.
- After the ledger, `send()` is not atomic: if saving fails, the ledger posting stays.
- `docs/ARCHITECTURE.md` is stale in two places. It describes a `risk.py` module that does not exist (limits are in
  `limits.py` and screening in `screening.py`), and it says T1 may send 5,000 a day with no monthly limit, which is
  outdated: the code has three KYC tiers (T1 2,000 a day and 8,000 a month) and monthly limits.
- A "day" and a "month" in `limits.py` are Qatar calendar days and months (UTC+3). Timestamps are stored in UTC, so
  everything that decides which window a moment belongs to has to convert first.

## Open questions

- I have not run the command line against a real database file; I only read `cli.py`.
- I could not tell from the code who owns the watchlist: `screening.py` has a 2022 TODO about moving it to a
  vendor feed, and nobody on the team has told me what happened to that.
