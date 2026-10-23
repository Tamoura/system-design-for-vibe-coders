# Najm Remit

Money-transfer service of the fictional Najm Bank: customers in Qatar send money home. Python 3.11, standard library only, pytest for tests. All data is fictional.

## Commands
- Tests, from the repository root: `pytest -q`. Nothing to install but pytest; `pyproject.toml` sets the import path.
- One file or one test: `pytest -q tests/test_fees.py` or `pytest -q tests/test_fees.py::test_minimum_fee_applies_to_small_amounts`.
- Command line: `PYTHONPATH=src python -m remit quote QAR 500 INR`. The tests do not need `PYTHONPATH`; `python -m remit` does.
- There is no linter, formatter, Makefile or build step. Do not invent one.

## Read first
- `docs/TOUR.md` for what is where, then `CONTRIBUTING.md` for the team's rules. Both apply to you as to a person.
- `docs/najmkit.md` before you touch ids, time or audit events.
- A transfer is `RemitService.send` in `src/remit/service.py`; follow its numbered step comments.
- `docs/ARCHITECTURE.md` is partly out of date (module names, the limits section). When a doc and the code disagree, the code wins.

## Conventions that differ from the defaults
- IMPORTANT: money is `Decimal`, never `float`. Use `Money` from `src/remit/money.py`: it rounds half up and raises `TypeError` on a float.
- `najmkit` is Najm's own library and is in no model's training data. Ids, time and audit events come only from it (`ids`, `clock`, `audit`). Read `docs/najmkit.md` for the exact names; do not guess them. Log ids, never names.
- Tests: pytest, one file per module in `tests/` (`tests/test_fees.py` covers `src/remit/fees.py`). Use the fixtures in `tests/conftest.py` (`service`, `store`, `customers`, `clock`): they give a fixed clock and sequential ids. New behaviour comes with a test. No network, no sleeping.
- Commits are `type(scope): subject`. Types: feat, fix, docs, test, refactor, perf, chore, ci, build, revert. The scope is required and lower case. Imperative subject, no full stop, header at most 72 characters. Example: `test(fees): cover the exact tier boundary`.
- Money logic (money, fees, fx, limits, ledger, service) needs a second human reviewer. Label AI-assisted pull requests `AI-assisted`.
- Every message to a customer exists in English and Arabic (`TEMPLATES` in `src/remit/notify.py`); change both.

## Gotchas
- `src/remit/ledger.py` and `src/remit/screening.py` are legacy and have no tests. Their module docstrings list known quirks: read them before any change.
- Settings are environment variables only; `.env.example` lists the names. Remit never loads a `.env` file.

## Never
- Never use `float` for money, or turn a `Money` into one.
- Never weaken, skip or delete an existing test to get green. If a test looks wrong, stop and say so. A task may ask you to change one: then say why in the commit body.
- Never put secrets, tokens or real customer data in code, tests, logs, fixtures or commit messages.
- Never add a dependency, or call `uuid.uuid4()` or `datetime.now()` in service code.
- Never tell a customer that a name matched a sanctions list; screening hits say only that we need to review.
- Do not change `ledger.py` or `screening.py` as a side effect of another task.
- Never push or open a pull request unless asked. Commit only when the task asks for it, and in small steps.
