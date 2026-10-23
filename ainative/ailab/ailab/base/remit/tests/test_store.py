from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from remit.errors import StoreError, UnknownCustomer
from remit.models import Customer, Transfer
from remit.money import Money
from remit.store import Store

NOW = datetime(2026, 3, 2, 9, 0, tzinfo=timezone.utc)


def make_transfer(transfer_id="TRF-1", customer_id="C001", created_at=NOW, **overrides):
    values = dict(
        id=transfer_id,
        customer_id=customer_id,
        corridor="QAR-INR",
        send_amount=Money("500.00", "QAR"),
        fee=Money("12.00", "QAR"),
        receive_amount=Money("11286.00", "INR"),
        rate=Decimal("22.5720"),
        recipient_name="Ravi Kumar",
        delivery_method="bank_deposit",
        created_at=created_at,
    )
    values.update(overrides)
    return Transfer(**values)


def test_customers_round_trip(store, customers):
    assert store.get_customer("C003") == customers["C003"]
    assert store.get_customer("nope") is None
    assert [c.id for c in store.list_customers()] == ["C001", "C002", "C003"]


def test_unknown_and_duplicate_customers_are_errors(store, customers):
    assert store.require_customer("C001").name == "Aisha Rahman"
    with pytest.raises(UnknownCustomer):
        store.require_customer("C999")
    with pytest.raises(StoreError):  # a duplicate id
        store.add_customer(customers["C001"])


def test_create_customer_uses_a_najmkit_id(store):
    customer = store.create_customer("Omar Farooq", kyc_tier="T2", language="ar")
    assert customer.id == "CUS-000001" and store.get_customer("CUS-000001") == customer


def test_customer_values_are_validated():
    with pytest.raises(ValueError):
        Customer("C1", "X", "T9")
    with pytest.raises(ValueError):
        Customer("C1", "X", "T1", loyalty_tier="platinum")
    with pytest.raises(ValueError):
        Customer("C1", "X", "T1", language="fr")


def test_transfers_round_trip_without_losing_a_digit(store, customers):
    transfer = make_transfer(express=True)
    store.save_transfer(transfer)
    assert store.get_transfer("TRF-1") == transfer
    assert store.get_transfer("TRF-1").rate == Decimal("22.5720")  # trailing zero kept
    assert store.get_transfer("missing") is None


def test_a_transfer_needs_an_existing_customer_and_a_new_id(store, customers):
    with pytest.raises(StoreError):
        store.save_transfer(make_transfer(customer_id="C999"))
    store.save_transfer(make_transfer())
    with pytest.raises(StoreError):
        store.save_transfer(make_transfer())


def test_list_transfers_is_per_customer_oldest_first_and_can_start_from_a_time(store, customers):
    store.save_transfer(make_transfer("TRF-2", created_at=NOW + timedelta(hours=1)))
    store.save_transfer(make_transfer("TRF-1", created_at=NOW))
    store.save_transfer(make_transfer("TRF-3", customer_id="C002", created_at=NOW))
    assert [t.id for t in store.list_transfers("C001")] == ["TRF-1", "TRF-2"]
    assert [t.id for t in store.list_transfers("C001", since=NOW + timedelta(minutes=1))] == ["TRF-2"]
    assert [t.id for t in store.list_transfers("C001", since=NOW)] == ["TRF-1", "TRF-2"]  # inclusive
    assert store.count_transfers() == 3
    with pytest.raises(ValueError):  # times must be timezone-aware
        store.list_transfers("C001", since=datetime(2026, 3, 2, 9, 0))
    with pytest.raises(ValueError):
        store.save_transfer(make_transfer("TRF-9", created_at=datetime(2026, 3, 2, 9, 0)))


def test_search_by_name(store, customers):
    assert [c.id for c in store.search_by_name("rahman")] == ["C001"]
    assert [c.id for c in store.search_by_name("a")] == ["C001", "C002", "C003"]
    assert store.search_by_name("zzz") == []


def test_a_database_file_keeps_its_data(tmp_path):
    path = tmp_path / "remit.db"
    with Store(path) as db:
        db.add_customer(Customer("C1", "Aisha", "T1"))
    with Store(path) as db:
        assert db.get_customer("C1").name == "Aisha"
