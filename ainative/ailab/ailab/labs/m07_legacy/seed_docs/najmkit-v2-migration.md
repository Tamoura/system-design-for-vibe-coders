# najmkit 2.0: migration notes

**From:** Salem, Platform Engineering
**Applies to:** every service that vendors najmkit 1.x. This repository now carries najmkit **2.0.0** (API v2).

This release is the *expand* step of a two-step change. The v2 names exist next to the v1 names, and
each v1 name still works but raises a `DeprecationWarning`. Version 3.0 removes the v1 names, so move
your service before you take 3.0. (Your own copy, once nothing calls a v1 name, can drop the old names
earlier: that is the *contract* step.)

## Renamed (same behaviour)

| v1 | v2 | Notes |
|---|---|---|
| `ids.new_id(prefix)` | `ids.make_id(prefix)` | same format, same checks |
| `ids.use_generator(gen)` | `ids.use_source(source)` | `None` still means random tokens |
| `clock.now()` | `clock.utc_now()` | the **module-level** function only |
| `clock.set_clock(c)` | `clock.install(c)` | |
| `clock.get_clock()` | `clock.current()` | |
| `clock.reset_clock()` | `clock.restore()` | back to the system clock |
| `audit.log_event(event, **fields)` | `audit.emit(event, **fields)` | see "Behaviour change" below |

## Did not change

`ids.SequentialIds`, `clock.Clock`, `clock.SystemClock`, `clock.FixedClock` (including its `now()`,
`set()` and `advance()` methods: a clock *object* still has `.now()`), `audit.configure`,
`audit.current_path`, `audit.read_events` and `audit.ENV_VAR`.

## Behaviour change: `audit.emit` takes JSON values only

`audit.log_event` wrote any value it was given by calling `str()` on whatever JSON could not hold
(a `Money`, a `Decimal`, a `datetime`). `audit.emit` does not guess: it accepts `str`, `int`, `float`,
`bool`, `None`, and lists and dicts of those, and raises `TypeError` for anything else. Convert the
value yourself. The deprecated `log_event` wrapper keeps the old `str()` behaviour so that v1 callers
do not break during the migration.

Audit files are read by other teams. The fraud team's parser reads `send_amount` and `fee` as text
such as `"500.00 QAR"`. If your records change, their parser changes with them: keep the lines exactly
as they were unless you have agreed otherwise.

## Suggested order

1. Start with the shared test setup (`tests/conftest.py`): every test runs its fixtures, so one v1 call
   there fails every test under `-W error::DeprecationWarning`. Then move one module at a time and run
   your tests after each.
2. Run the tests with `-W error::DeprecationWarning`: with the shared setup migrated, every v1 call that
   is left raises at its call site. (Calls in code that no test reaches are not found this way: search
   for the old names too.)
3. When nothing calls a v1 name, delete the section marked "deprecated v1 names" in `ids.py`,
   `clock.py` and `audit.py` (the contract step), run the tests again, and update `docs/najmkit.md`,
   which still describes version 1.3.0, and the package docstring in `src/najmkit/__init__.py`. Leave
   `__version__` as it is: this is the same release with its deprecated names removed from your copy.

## Versions

2.0.0 is this release. 3.0 will remove the v1 names. There is no schedule for 3.0 yet.
