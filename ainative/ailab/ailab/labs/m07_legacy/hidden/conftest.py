"""Fixtures for the hidden m07 tests. They install their own fixed clock and sequential ids (using the
najmkit v2 names, which exist from the very first commit of the lab) and build their own service, so
they do not depend on how the learner changed tests/conftest.py."""
import pytest

from najmkit import audit, clock, ids
from remit.fx import StaticRateProvider
from remit.models import Customer
from remit.notify import InMemoryNotifier
from remit.service import RemitService
from remit.store import Store

NOW = "2026-03-02T09:00:00+00:00"
PEOPLE = (
    Customer("C001", "Aisha Rahman", "T2", "none", "en"),
    Customer("C002", "Bilal Khan", "T1", "silver", "en"),
    Customer("C003", "Mariam Saleh", "T3", "gold", "ar"),
)


@pytest.fixture(autouse=True)
def hx_world(monkeypatch):
    monkeypatch.delenv(audit.ENV_VAR, raising=False)
    ids.use_source(ids.SequentialIds())
    clock.install(clock.FixedClock(NOW))
    audit.configure(None)
    yield
    ids.use_source(None)
    clock.restore()
    audit.configure(None)


@pytest.fixture
def hx_clock():
    return clock.current()


@pytest.fixture
def hx_new_ledger():
    """A function that makes a Ledger, failing the test with a plain message while the class does not exist."""

    def make():
        from remit import ledger as module

        ledger_class = getattr(module, "Ledger", None)
        if ledger_class is None:
            pytest.fail("remit.ledger has no class Ledger yet")
        return ledger_class()

    return make


@pytest.fixture
def hx_build():
    """A function that builds a RemitService over a fresh in-memory store, with the three demo customers."""
    stores = []

    def build(**kwargs):
        store = Store(":memory:")
        stores.append(store)
        for person in PEOPLE:
            store.add_customer(person)
        service = RemitService(store, StaticRateProvider(), ["Test Sanctioned Person"], clock.current(), InMemoryNotifier(), **kwargs)
        return service

    yield build
    for store in stores:
        store.close()
