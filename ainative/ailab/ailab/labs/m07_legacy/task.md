# REMIT-372: make the ledger safe to change, then move Remit to najmkit 2

**From:** Tariq, Engineering Lead, Payments Platform (Hessa's business reason is at the end)
**To:** You, and your AI coding tool if you use one
**Priority:** Normal. Money logic: a second human reviews it before it merges.

`src/remit/ledger.py` is Remit's oldest code and has no tests. Its books live in module-level
variables, so a process can have exactly one set of books. Finance's reconciliation job needs two
`RemitService` objects in one process, each with its own ledger. And najmkit 3 will remove najmkit 1.

Three parts. Do Part 1 first and commit it before you change anything under `src/`; commit every
later step separately. **Behaviour must not change anywhere**, quirks included, except where this
ticket says so. Read the docstring of `ledger.py` first.

### Part 1: pin what the ledger does now

1. Copy `lab-assets/ledger_port.py` to `tests/ledger_port.py`: a seam with `make_ledger()` (a fresh
   ledger) and `ledger_of(service)` (the ledger a service posts to), working before and after Part 2.
2. Write characterization tests in **new files named `tests/test_ledger_*.py`**, importing the seam as
   `from ledger_port import ledger_of, make_ledger` (`tests.ledger_port` fails under `pytest -q`, which
   CI runs). They say what the code does today, quirks included (values, order, error types and
   messages), not what you think it should do. Reach the ledger only through the seam. Part 2 changes
   Q-LED-3's shared books on purpose: pin the rest of it.
3. They must pass on the code as it is now and, unchanged, after Part 2. The grader runs them on the
   original and on broken copies of it, so test behaviour, never the source text: it wants at least ten
   tests that catch at least 13 of 16 breaks, and ignores your edits to `tests/conftest.py`.
   `python lab-assets/try_mutation.py` runs your tests on the original; given a file, a text and a
   replacement, it breaks the original there and says whether they noticed.

### Part 2: remove the module-level state

After the refactor the interface is exactly this:

    # src/remit/ledger.py
    class Ledger:
        def __init__(self) -> None: ...                       # no arguments needed
        def post_transfer(self, transfer_id: str, customer_id: str, send_amount: Money, fee: Money) -> list[dict]: ...
        def balance(self, account: str) -> Decimal: ...
        def accounts(self) -> list[str]: ...
        def journal(self) -> list[dict]: ...

    # src/remit/service.py
    class RemitService:
        def __init__(self, store, rates, watchlist, clock, notifier, ledger: Ledger | None = None) -> None: ...
        # self.ledger is the Ledger in use; ledger=None means a fresh Ledger() for this service

- State belongs to the instance: no changing module-level variables, no mutable class attributes,
  no module-level default instance.
- The module functions `post_transfer`, `balance`, `accounts`, `journal` and `reset` are removed.
  The constants and `customer_account()` stay.
- Entry ids and times still come from najmkit as today, so two ledgers in one process share one id
  sequence. `tests/conftest.py` stops calling `ledger.reset()`.
- The one deliberate change: two `Ledger` objects no longer share their books.

### Part 3: najmkit 1 to 2

The vendored najmkit is 2.0.0. `docs/najmkit-v2-migration.md` lists the renames and one change in
behaviour; the old names still work but warn.

- Move every use of an old name in `src/remit` and `tests` to the new one. Remit's audit files are
  read by the fraud team's parser: the lines must come out byte for byte as today.
- Then delete the deprecated names from `src/najmkit` and update the documents that are now untrue:
  `docs/najmkit.md` (still version 1) and any that call the ledger untested or module-level.

### Rules

- Commits follow `CONTRIBUTING.md`: at least three that change something, each leaving `pytest -q`
  green; the one that adds your ledger tests changes nothing under `src/`. Never mix a refactor and a
  migration in one commit (your reviewer checks that). Commit everything.
- Edit an existing test only to follow a rename or the removed `reset()`. This ticket asks for those
  edits and for commits, which `CLAUDE.md` allows when a task asks: tell your AI tool, and say why in
  the commit body.
- Touch only `ledger.py`, `service.py`, `store.py` and `cli.py` in `src/remit`, `src/najmkit`, `tests`,
  `docs`, `scripts`, `README.md`, `CLAUDE.md`, `AGENTS.md`, `.claude`, and `pyproject.toml` or
  `.github/workflows` if you make warnings-as-errors permanent.
- Recommended: fill in `lab-assets/refactoring-plan-template.md` as `docs/refactoring-plan.md` first.
- Use any help you like, an AI coding tool included. You are accountable for every line.

**Why now (Hessa):** the nightly reconciliation compares two sets of books, and the audit lines feed
the fraud team's dashboard. Neither can change on the day we ship.

When you think you are done, from the `ailab` folder of the course repository:
`python -m ailab grade m07 --dir <this directory>`
