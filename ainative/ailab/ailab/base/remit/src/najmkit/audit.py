"""Append-only audit trail: one JSON object per line.

``log_event("transfer.sent", transfer_id="TRF-1", amount="500.00")`` appends

    {"amount": "500.00", "event": "transfer.sent", "transfer_id": "TRF-1", "ts": "2026-03-02T09:00:00+00:00"}

to the audit file. The file is chosen, in this order, by

1. ``configure(path)`` (what the Remit CLI does with ``REMIT_AUDIT_LOG``), then
2. the ``NAJMKIT_AUDIT_LOG`` environment variable,
3. otherwise nothing is written (the record is still returned).

Rules of the house: log identifiers, never names, document numbers or secrets.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from najmkit import clock

ENV_VAR = "NAJMKIT_AUDIT_LOG"
_EVENT = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$")
_RESERVED = ("ts", "event")

_configured: Path | None = None


def configure(path: str | os.PathLike[str] | None) -> None:
    """Set (or with ``None`` clear) the audit file for this process."""
    global _configured
    _configured = Path(path) if path else None


def current_path() -> Path | None:
    """The audit file in effect, or None when auditing to disk is off."""
    if _configured is not None:
        return _configured
    env = os.environ.get(ENV_VAR)
    return Path(env) if env else None


def log_event(event: str, **fields: Any) -> dict[str, Any]:
    """Record ``event`` with ``fields`` and return the record.

    ``event`` is a dotted lower-case name such as ``transfer.sent``. The field
    names ``ts`` and ``event`` are reserved. Values that are not JSON types
    (Decimal, Money, datetime) are written with ``str()``. I/O errors propagate.
    """
    if not _EVENT.match(event):
        raise ValueError(f"event must look like 'transfer.sent', got {event!r}")
    for key in _RESERVED:
        if key in fields:
            raise ValueError(f"{key!r} is reserved and set by log_event")
    record: dict[str, Any] = {"ts": clock.now().isoformat(), "event": event, **fields}
    path = current_path()
    if path is not None:
        line = json.dumps(record, sort_keys=True, default=str, ensure_ascii=False)
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    return record


def read_events(path: str | os.PathLike[str] | None = None) -> list[dict[str, Any]]:
    """Read an audit file back (the configured one by default). Missing file -> []."""
    target = Path(path) if path else current_path()
    if target is None or not target.exists():
        return []
    with open(target, encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]
