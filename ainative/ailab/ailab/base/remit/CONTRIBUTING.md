# Contributing to Najm Remit

These are the working agreements of the Payments Platform team. They apply to everyone,
and to every AI coding tool that works in this repository.

## Run the tests

```bash
pytest -q
```

All tests must pass before you commit and before you open a pull request. CI runs the
same command.

## Commits: Conventional Commits with a scope

Write every commit message header as

```
type(scope): subject
```

* `type` is one of `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`, `ci`,
  `build`, `revert`.
* `scope` is the module or area you touched, in lower case: `notify`, `fees`, `fx`,
  `limits`, `ledger`, `screening`, `store`, `service`, `cli`, `docs`, `ci`. A scope is
  required.
* `subject` says what the change does, in the imperative ("correct the spelling of
  received"), with no full stop at the end.
* The whole header is at most 72 characters. Add `!` before the colon for a breaking
  change: `feat(fees)!: charge fees on the receive side`.
* Use the body (after a blank line) for the why, not the what.

Examples: `fix(limits): count transfers made just after midnight`,
`test(fees): cover the exact tier boundary`, `docs(architecture): describe the ledger`.

## Pull requests

* **Keep them small.** One logical change per pull request and per commit. If the diff
  needs a long explanation, split it.
* **Money logic needs a second reviewer.** Anything that touches `money.py`, `fees.py`,
  `fx.py`, `limits.py`, `ledger.py` or `service.py` needs approval from a second human
  reviewer, in addition to the author.
* **Label AI-assisted changes.** If an AI tool wrote or substantially shaped any part of
  the change, put the label `AI-assisted` on the pull request. The author is still
  accountable: you must be able to explain and defend every line.
* Describe what you ran to check the change.

## Code rules

* **Money is always `Decimal`, never `float`.** Use the `Money` class. Round half up.
* New behaviour comes with a test. Keep tests deterministic: inject the clock and ids,
  no network, no sleeping.
* **No secrets** in code, tests, fixtures, logs or commit history. Settings come from
  environment variables; add the name (never the value) to `.env.example`.
* Standard library only. Do not add a dependency without a ticket and a second
  reviewer.
* Use `najmkit` for ids, time and audit events (see `docs/najmkit.md`); do not call
  `uuid.uuid4()` or `datetime.now()` directly in service code.
