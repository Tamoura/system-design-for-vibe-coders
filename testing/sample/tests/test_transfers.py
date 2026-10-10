"""A small starter suite for najm.transfers. It is good, but not complete: the course asks you to find the gaps."""
from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

import pytest

from najm.transfers import TransferRejected, TransferService, check_transfer, fee, quantize, value_date


def test_quantize_rounds_half_up():
    assert quantize("2.675", "QAR") == Decimal("2.68")


def test_quantize_uses_the_currency_minor_units():
    assert quantize("1.2345", "KWD") == Decimal("1.235")
    assert quantize("10.5", "JPY") == Decimal("11")


def test_own_account_transfers_are_free():
    assert fee("500", "QAR", "own") == Decimal("0.00")


def test_domestic_fee_is_flat_above_1000():
    assert fee("5000", "QAR", "domestic") == Decimal("2.00")


def test_international_fee_has_a_minimum():
    assert fee("100", "QAR", "international") == Decimal("10.00")


def test_international_fee_is_capped():
    assert fee("100000", "QAR", "international") == Decimal("100.00")


def test_a_normal_transfer_is_accepted_with_its_fee():
    decision = check_transfer("5000", "QAR", "domestic")
    assert decision.fee == Decimal("2.00")
    assert decision.total == Decimal("5002.00")


def test_a_transfer_over_the_daily_limit_is_rejected():
    with pytest.raises(TransferRejected) as e:
        check_transfer("5000", "QAR", "domestic", sent_today="49000")
    assert e.value.code == "daily_limit_exceeded"


def test_unsupported_currency_is_rejected():
    with pytest.raises(TransferRejected) as e:
        check_transfer("10", "USD", "domestic")
    assert e.value.code == "unsupported_currency"


def test_cutoff_before_3pm_is_processed_today():
    now = datetime(2026, 10, 5, 10, 0, tzinfo=ZoneInfo("Asia/Qatar"))  # a Monday
    assert value_date(now).isoformat() == "2026-10-05"


def test_the_same_idempotency_key_creates_one_transfer():
    svc = TransferService()
    req = {"from_account": "acc-1", "to_account": "acc-2", "amount": "100.00", "currency": "QAR", "kind": "domestic"}
    first, created1 = svc.submit("alice", req, "key-1")
    second, created2 = svc.submit("alice", req, "key-1")
    assert (created1, created2) == (True, False)
    assert first["id"] == second["id"]
    assert svc.accounts["acc-1"]["balance"] == Decimal("11900.00")


def test_a_user_cannot_read_someone_elses_transfer():
    svc = TransferService()
    req = {"from_account": "acc-1", "to_account": "acc-2", "amount": "10.00", "currency": "QAR", "kind": "domestic"}
    t, _ = svc.submit("alice", req, "k")
    with pytest.raises(TransferRejected) as e:
        svc.get("bob", t["id"])
    assert e.value.code == "not_owner"
