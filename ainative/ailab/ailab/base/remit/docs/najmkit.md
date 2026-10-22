# najmkit (API v1)

`najmkit` is Najm Bank's internal helper library. Every Najm service vendors a copy of it
(this repository's copy is in `src/najmkit/`, version 1.3.0, API `v1`). It is internal:
it is not on PyPI and it is not in any model's training data, so check this page, not your
memory, for what it offers.

It has three modules. Import them as `from najmkit import ids, clock, audit`.

## `najmkit.ids`

Readable, prefixed identifiers.

```python
ids.new_id(prefix: str) -> str
```

Returns `"<PREFIX>-<TOKEN>"`, for example `"TRF-9F3A1C7B2D40"`. `prefix` is 2 to 5 upper-case
ASCII letters, otherwise `ValueError`. Prefixes used in Remit: `TRF` (transfer), `CUS`
(customer), `JNL` (ledger journal entry).

Tests control the token part:

```python
ids.use_generator(ids.SequentialIds())      # TRF-000001, CUS-000002, ...
ids.SequentialIds(start=40)                  # starts at 000040
ids.use_generator(None)                      # back to random tokens
```

## `najmkit.clock`

One place to ask for the time. Times are always timezone-aware and in UTC.

```python
clock.now() -> datetime                      # from the installed clock
clock.SystemClock().now()                    # the real time
clock.FixedClock(start)                      # start: aware datetime or ISO string
    .now() / .set(moment) / .advance(**timedelta_kwargs)
clock.set_clock(clock) / clock.get_clock() / clock.reset_clock()
```

`FixedClock("2026-03-02T09:00:00+00:00")` never moves by itself; `advance(seconds=61)`
moves it. A naive datetime raises `ValueError`. `RemitService` takes a clock object and
calls `clock.now()` on it; `ledger.py` has no clock handed to it and calls the
module-level `clock.now()`, which is why tests install a global fixed clock.

## `najmkit.audit`

An append-only JSON-lines audit trail.

```python
audit.log_event(event: str, **fields) -> dict
audit.configure(path | None) -> None
audit.current_path() -> Path | None
audit.read_events(path=None) -> list[dict]
```

`log_event("transfer.sent", transfer_id="TRF-1")` builds
`{"ts": <clock.now() as ISO text>, "event": "transfer.sent", "transfer_id": "TRF-1"}`,
appends it as one line (keys sorted) to the audit file and returns it.

* `event` is a dotted lower-case name (`transfer.sent`, `notification.failed`); anything
  else raises `ValueError`. The field names `ts` and `event` are reserved.
* The file is `audit.configure(path)` if set, otherwise the `NAJMKIT_AUDIT_LOG`
  environment variable, otherwise nothing is written (the record is still returned).
  The Remit CLI calls `configure()` with `REMIT_AUDIT_LOG`.
* Values that are not JSON types (Decimal, Money, datetime) are written with `str()`.
* Log identifiers only. Never log names, document numbers, phone numbers or secrets.
* I/O errors propagate: a failed audit write is a failure.

## Where Remit uses it

| Call | Where |
|---|---|
| `ids.new_id("TRF")` | `service.py`, when a transfer is sent |
| `ids.new_id("CUS")` | `store.py`, `Store.create_customer` |
| `ids.new_id("JNL")` | `ledger.py`, every journal entry |
| `clock.now()` | `ledger.py`, the posting time |
| `clock.SystemClock()` | `cli.py`, the real clock |
| `audit.log_event(...)` | `service.py`: `transfer.sent`, `transfer.rejected`, `notification.failed` |
| `audit.configure(...)` | `cli.py` |
