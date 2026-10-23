# A tour of the Najm Remit repository

You are new to the Payments Platform team. This tour tells you what is where, in the
order you are likely to need it. Run `pytest -q` first: everything you see should pass
on a fresh checkout (unless a task you were given says otherwise).

## Start here

| File | Why |
|---|---|
| `README.md` | What Remit is, how to run the tests, the layout |
| `CONTRIBUTING.md` | The team's working agreements: commit format, pull requests, money rules |
| `docs/ARCHITECTURE.md` | The design in one page. Documents drift: when it disagrees with the code, the code wins, and the document needs a fix |
| `docs/najmkit.md` | The internal helper library. You cannot guess it; read it |

## `src/remit/`: the service

Read these in the order of a transfer's life.

* **`models.py`**: the two dataclasses everything passes around, `Customer` (id, name,
  KYC tier, loyalty tier, language) and `Transfer`.
* **`money.py`**: `Money`. Money is `Decimal`, never `float`; it rounds half up; it
  refuses to mix currencies. Almost every other module imports it.
* **`corridors.py`**: which routes exist, the minimum and maximum per transfer, the
  delivery methods and which fee schedule applies.
* **`fees.py`**: tiered fee schedules. `quote_fee(amount, corridor, express=False)`.
* **`fx.py`**: exchange rates (`StaticRateProvider`), the margin on each corridor and
  the 60-second `FxQuote`.
* **`limits.py`**: daily and monthly limits by KYC tier. "Day" means a Qatar calendar day.
* **`screening.py`**: name screening against a watchlist. Old code, written before the
  team had tests. **No dedicated tests**: only `send()` exercises it. Read it before you
  trust it.
* **`ledger.py`**: double-entry postings in a `Ledger` class. Old code whose quirks are
  pinned by `tests/test_ledger_characterization.py`; each `RemitService` owns one.
* **`store.py`**: SQLite storage. One query is built differently from all the others;
  see if you can spot which.
* **`notify.py`**: notification templates in English and Arabic, and the notifiers.
* **`service.py`**: `RemitService`. This is where the pieces meet: `quote()` and
  `send()`. If you only read one file, read this one.
* **`cli.py`**, **`config.py`**, **`errors.py`**: the command line, environment
  settings, and the error classes (all derive from `RemitError`).

## `src/najmkit/`: the vendored library

`ids.py`, `clock.py` and `audit.py`. Services use it for ids, time and the audit trail,
so tests can control all three. Look for the calls: `grep -rn "najmkit\|ids\.\|clock\.\|audit\." src/remit`.

## `tests/`

One test file per module, plus `conftest.py` with the fixtures that make everything
deterministic: a fixed clock (Monday 2 March 2026, 09:00 UTC), sequential ids, a fresh
in-memory store and an in-memory notifier. There is no test file for
`screening.py`; `tests/test_service.py` exercises it through `send()`.

## Where to look when...

| You need to... | Look in |
|---|---|
| change what a customer is charged | `fees.py`, then `tests/test_fees.py` |
| change a notification's wording | `notify.py` (`TEMPLATES`), then `tests/test_notify.py` |
| change a sending limit | `limits.py` (`LIMITS`), then `tests/test_limits.py` |
| add a currency corridor | `corridors.py`, `fees.py`, `fx.py`, and the tests for each |
| see everything that happens on `send` | `service.py` |
| find out what the team expects of a commit | `CONTRIBUTING.md` |
