"""Shared fixtures. Everything that could make a test flaky is injected here:

* the clock is a FixedClock (Monday 2 March 2026, 09:00 UTC = 12:00 in Qatar),
* ids are sequential (TRF-000001, TRF-000002, ...),
* environment variables that Remit or najmkit read are removed.
"""
from datetime import datetime, timezone

import pytest

from najmkit import audit, clock as najm_clock, ids
from remit.fx import StaticRateProvider
from remit.models import Customer
from remit.notify import InMemoryNotifier
from remit.service import RemitService
from remit.store import Store

NOW = datetime(2026, 3, 2, 9, 0, tzinfo=timezone.utc)


@pytest.fixture(autouse=True)
def isolated_world(monkeypatch):
    """Reset every piece of global state a test could touch."""
    for name in ("REMIT_ENV", "REMIT_DB", "REMIT_AUDIT_LOG", "REMIT_WATCHLIST", "REMIT_LANG", audit.ENV_VAR):
        monkeypatch.delenv(name, raising=False)
    ids.use_generator(ids.SequentialIds())
    najm_clock.set_clock(najm_clock.FixedClock(NOW))
    audit.configure(None)
    yield
    ids.use_generator(None)
    najm_clock.reset_clock()
    audit.configure(None)


@pytest.fixture
def now():
    return NOW


@pytest.fixture
def clock():
    """The process-wide FixedClock (also what najmkit.clock.now() returns)."""
    return najm_clock.get_clock()


@pytest.fixture
def store():
    with Store(":memory:") as db:
        yield db


@pytest.fixture
def customers(store):
    """Three customers: Aisha (T2, English), Bilal (T1, English), Mariam (T3, Arabic, gold)."""
    people = [
        Customer("C001", "Aisha Rahman", "T2", "none", "en"),
        Customer("C002", "Bilal Khan", "T1", "silver", "en"),
        Customer("C003", "Mariam Saleh", "T3", "gold", "ar"),
    ]
    for person in people:
        store.add_customer(person)
    return {person.id: person for person in people}


@pytest.fixture
def notifier():
    return InMemoryNotifier()


@pytest.fixture
def service(store, customers, clock, notifier):
    return RemitService(store, StaticRateProvider(), ["Test Sanctioned Person"], clock, notifier)
