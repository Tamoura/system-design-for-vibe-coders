# Najm Remit

Najm Remit is the service that lets the fictional **Najm Bank**'s expatriate customers in
Qatar send money home. It quotes a transfer, prices the fee, applies an exchange rate,
checks sending limits and sanctions screening, posts the ledger entries, stores the
transfer and tells the customer, in English or Arabic.

This is a **small teaching version** of the real thing. Everything in it is fictional:
the bank, the customers, the rates, the fees and the limits. It uses only the Python
standard library (plus `pytest` for the tests) and needs no network.

## Run the tests

```bash
python -m pip install pytest      # once
pytest -q
```

Python 3.11 or newer. The tests are deterministic: they inject a fixed clock and
sequential ids, so they never depend on today's date.

## Try it

```bash
export PYTHONPATH=src                          # or: python -m pip install -e .
python -m remit quote QAR 500 INR              # price a transfer, nothing is saved
python -m remit customer add --id C001 --name "Aisha Rahman" --kyc T2
python -m remit send --customer C001 QAR 500 INR --recipient "Ravi Kumar"
python -m remit history --customer C001
```

Settings come from environment variables; see `.env.example`.

## Layout

```
src/remit/        the service
  money.py          Money: an amount of one currency, on Decimal
  corridors.py      which routes we support, and their limits per transfer
  fees.py           tiered fee schedules
  fx.py             exchange rates, margins, 60-second quotes
  limits.py         daily and monthly limits by KYC tier (Qatar local time)
  screening.py      name screening against the watchlist       (old code, no dedicated tests)
  ledger.py         double-entry postings: class Ledger        (characterization tests)
  store.py          SQLite storage
  notify.py         notification templates, English and Arabic
  service.py        RemitService: quote() and send()
  cli.py            python -m remit
  config.py  models.py  errors.py
src/najmkit/      Najm Bank's internal helper library (vendored): ids, clock, audit
tests/            pytest suite
docs/             ARCHITECTURE.md, TOUR.md, najmkit.md
CONTRIBUTING.md   how we work here: read it before your first commit
```

`screening.py` has no dedicated tests: only `send()` exercises it (`tests/test_service.py`).

New to the repository? Read `docs/TOUR.md` first.
