"""One place to ask "what time is it?" so that tests can control it.

All times in Najm services are timezone-aware and in UTC. ``utc_now()`` returns the current time from
whichever clock is installed (the system clock by default). Code that is handed a clock object (for
example ``RemitService``) calls ``now()`` on that object; code that has no clock handed to it calls
the module-level ``utc_now()``.
"""
from __future__ import annotations

import warnings
from datetime import datetime, timedelta, timezone
from typing import Protocol


class Clock(Protocol):
    def now(self) -> datetime: ...


def _parse(value: datetime | str) -> datetime:
    moment = datetime.fromisoformat(value) if isinstance(value, str) else value
    if moment.tzinfo is None or moment.utcoffset() is None:
        raise ValueError("clock times must be timezone-aware (e.g. 2026-03-02T09:00:00+00:00)")
    return moment.astimezone(timezone.utc)


class SystemClock:
    """The real time, in UTC."""

    def now(self) -> datetime:
        return datetime.now(timezone.utc)


class FixedClock:
    """A clock that only moves when you move it (for tests and demos)."""

    def __init__(self, start: datetime | str) -> None:
        self._now = _parse(start)

    def now(self) -> datetime:
        return self._now

    def set(self, moment: datetime | str) -> None:
        """Jump to ``moment`` (must be timezone-aware)."""
        self._now = _parse(moment)

    def advance(self, **delta: int) -> datetime:
        """Move forward by a ``timedelta(**delta)``, e.g. ``advance(seconds=61)``."""
        self._now = self._now + timedelta(**delta)
        return self._now


_installed: Clock = SystemClock()


def utc_now() -> datetime:
    """Current time (aware, UTC) from the installed clock."""
    return _installed.now()


def install(clock: Clock) -> None:
    """Install ``clock`` as the process-wide clock used by module-level ``utc_now()``."""
    global _installed
    _installed = clock


def current() -> Clock:
    """Return the installed clock."""
    return _installed


def restore() -> None:
    """Go back to the system clock."""
    install(SystemClock())


# ---- deprecated v1 names: removed in 3.0. Delete this section when nothing calls them. ----
def now() -> datetime:
    """Deprecated since 2.0: use utc_now."""
    warnings.warn("najmkit.clock.now is deprecated, use utc_now (removed in 3.0)", DeprecationWarning, stacklevel=2)
    return utc_now()


def set_clock(clock: Clock) -> None:
    """Deprecated since 2.0: use install."""
    warnings.warn("najmkit.clock.set_clock is deprecated, use install (removed in 3.0)", DeprecationWarning, stacklevel=2)
    install(clock)


def get_clock() -> Clock:
    """Deprecated since 2.0: use current."""
    warnings.warn("najmkit.clock.get_clock is deprecated, use current (removed in 3.0)", DeprecationWarning, stacklevel=2)
    return current()


def reset_clock() -> None:
    """Deprecated since 2.0: use restore."""
    warnings.warn("najmkit.clock.reset_clock is deprecated, use restore (removed in 3.0)", DeprecationWarning, stacklevel=2)
    restore()
