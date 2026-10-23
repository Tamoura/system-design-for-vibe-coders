# najmkit

`najmkit` is Najm Bank's internal helper library. This repository vendors a copy of it in `src/najmkit/` (version 1.3.0, API `v1`). It is internal: it is not on PyPI, and no AI model has seen it in training, so read this page and the code, not your memory.

It has three modules, imported together like this:

```python
from najmkit import ids, clock, audit
```

## najmkit.ids

Readable, prefixed identifiers.

| Name | Signature | What it does |
|---|---|---|
| `ids.new_id` | `new_id(prefix)` | Returns `PREFIX-TOKEN`, for example `TRF-9F3A1C7B2D40`. |
| `ids.SequentialIds` | `SequentialIds(start=1)` | A token source for tests: 000001, 000002, and so on. |
| `ids.use_generator` | `use_generator(generator)` | Installs a token source; `None` goes back to random tokens. |

The prefix must be 2 to 5 upper-case ASCII letters, otherwise `ValueError`. Remit uses `TRF` (transfer), `CUS` (customer) and `JNL` (journal entry). The random token is 12 hex characters, upper-case.

```python
from najmkit import ids

ids.use_generator(ids.SequentialIds())
print(ids.new_id("TRF"))  # TRF-000001
print(ids.new_id("CUS"))  # CUS-000002
ids.use_generator(None)   # random tokens again
```

## najmkit.clock

One place to ask for the time. Times are timezone-aware and in UTC; a naive datetime raises `ValueError`.

| Name | Signature | What it does |
|---|---|---|
| `clock.now` | `now()` | The current time from the installed clock. |
| `clock.SystemClock` | `SystemClock()` | The real time. It is the default. |
| `clock.FixedClock` | `FixedClock(start)` | A clock that only moves when told. `start` is an aware datetime or an ISO string. |
| `clock.FixedClock.set` | `set(moment)` | Jump to `moment`. |
| `clock.FixedClock.advance` | `advance(**delta)` | Move forward by a `timedelta`; returns the new time. |
| `clock.set_clock` | `set_clock(clock)` | Install a clock for the whole process. |
| `clock.get_clock` | `get_clock()` | The installed clock. |
| `clock.reset_clock` | `reset_clock()` | Back to the system clock. |

```python
from najmkit import clock

fixed = clock.FixedClock("2026-03-02T09:00:00+00:00")
clock.set_clock(fixed)
fixed.advance(seconds=61)
print(clock.now())  # 2026-03-02 09:01:01+00:00
clock.reset_clock()
```

`RemitService` is handed a clock object and calls `.now()` on it. `ledger.py` is handed nothing and calls the module-level `clock.now()`, which is why the tests install a global fixed clock.

## najmkit.audit

An append-only JSON-lines audit trail.

| Name | Signature | What it does |
|---|---|---|
| `audit.log_event` | `log_event(event, **fields)` | Builds a record, appends it to the audit file if there is one, and returns the record. |
| `audit.configure` | `configure(path)` | Choose the audit file; `None` clears it. |
| `audit.current_path` | `current_path()` | The audit file in effect, or `None`. |
| `audit.read_events` | `read_events(path=None)` | Read an audit file back as a list of dicts. |

`log_event("transfer.sent", transfer_id="TRF-1")` returns `{"ts": ..., "event": "transfer.sent", "transfer_id": "TRF-1"}`. The event name is dotted lower-case; `ts` and `event` are reserved field names. The file is the one given to `configure`, otherwise the one named by the environment variable `NAJMKIT_AUDIT_LOG`; with neither, nothing is written (the record is still returned). Values that are not JSON types are written with `str()`. A failed write raises, so an audit failure is a failure. Log identifiers only, never names or secrets.

```python
from najmkit import audit

audit.configure("audit.jsonl")
record = audit.log_event("transfer.sent", transfer_id="TRF-1")
print(audit.read_events())  # [{'event': 'transfer.sent', 'transfer_id': 'TRF-1', 'ts': '...'}]
audit.configure(None)
```

## Where Remit uses it

| Call | Where |
|---|---|
| `ids.new_id("TRF")` | `service.py`, when a transfer is sent |
| `ids.new_id("CUS")` | `store.py`, `Store.create_customer` |
| `ids.new_id("JNL")` | `ledger.py`, every journal entry |
| `clock.now()` | `ledger.py`, the posting time |
| `audit.log_event(...)` | `service.py`: `transfer.sent`, `transfer.rejected`, `notification.failed` |

## Known problems

- The docstring of `audit.read_events` in `src/najmkit/audit.py` says a missing file raises an error. I ran `audit.read_events("nope.jsonl")` and it returned an empty list, which is what the tests expect. The docstring should be corrected in a separate change.
