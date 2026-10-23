# TODO: Najm Remit, notes for coding agents

TODO: two sentences: what Remit is, which language, and that every number in it is fictional. Copy this file to CLAUDE.md (or AGENTS.md) at the repository root and keep it between 15 and 150 lines: the grader counts them.

## Commands
- TODO: the test command, `pytest -q`, and when to run it.
- TODO: a command that runs one test file.
- TODO: a command that prices a transfer, such as `PYTHONPATH=src python -m remit quote QAR 500 INR`. The grader runs the `python -m remit quote ...` commands you write, so they must work.

## Rules that differ from the defaults
- TODO: money is Decimal, never float, and rounds half up.
- TODO: commits are `type(scope): subject`, as CONTRIBUTING.md says.
- TODO: time, ids and audit events come from najmkit; where to read about it.
- TODO: which files are money files that need a second human reviewer.

## Adding a corridor
TODO: a numbered checklist in the order you will work, naming `corridors.py`, `fees.py`, `fx.py` and the other files a corridor touches.

## Never
- TODO: at least three bullets, each with "never", "do not" or "must not": tests, dependencies, secrets, pushing, deleting.

## Where things are
TODO: the files to read first. A path in backticks must exist (or the same line must say it does not); `docs/ARCHITECTURE.md` can be stale, so say which text wins.
