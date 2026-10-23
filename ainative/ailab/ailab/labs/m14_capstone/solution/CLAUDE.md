# Najm Remit: notes for coding agents

Najm Remit prices and sends money from Qatar (QAR) to family abroad. The bank and every number in it are fictional. Python 3.11, standard library only.

## Commands
- All tests, before every commit: `pytest -q`
- One file: `pytest -q tests/test_fees.py`
- Price a transfer without saving anything: `PYTHONPATH=src python -m remit quote QAR 500 BDT`

## Rules that differ from the defaults
- Money is `Decimal` through `Money`, never `float`. Round half up. The old `ledger.py` rounds the partner share half-even on purpose: leave it.
- Commits are `type(scope): subject`, as `CONTRIBUTING.md` says: scope required and lower case, header at most 72 characters, no full stop.
- Time, ids and audit events come from `najmkit`. Read `docs/najmkit.md` first: you cannot guess it. Do not call `uuid.uuid4()` or `datetime.now()` in service code.
- Money files need a second human reviewer: `money.py`, `fees.py`, `fx.py`, `limits.py`, `ledger.py`, `service.py`. Say which in the review notes.
- Label AI-assisted work `AI-assisted` in the pull request.

## Adding a corridor
A corridor is data in three places, and words when the wording differs. Tests first, then one commit per step, in this order:
1. `fees.py`: a schedule in `SCHEDULES` when the corridor needs its own tiers.
2. `fx.py`: the mid rate in `DEFAULT_MID_RATES` and the margin in `CORRIDOR_MARGINS`.
3. `corridors.py`: the entry in `_DEFINITIONS`, last, because it points at the first two.
4. `notify.py` and `service.py` only when the customer wording differs (`SENT_TEMPLATES`).
5. `docs/corridors.md`, and the lines of `docs/ARCHITECTURE.md` that the change makes untrue.

Limits per KYC tier live in `limits.py` and belong to the customer, not to a corridor: do not add per-corridor limits.

## Never
- Never edit, skip or delete an existing test to make a change pass.
- Never add a dependency, a network call or a new library.
- Never read, print or commit `.env` files or any secret.
- Never push, force anything, or run `rm -rf`.
- Never fix `ledger.py` or `screening.py` inside another change: they are legacy and have no tests.

## Where things are
Start with `docs/TOUR.md`. `docs/ARCHITECTURE.md` can be stale: when it disagrees with the code, the code wins.
