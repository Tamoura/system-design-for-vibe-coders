"""Hidden tests for lab m07: RemitService owns a ledger (or is given one) and send() keeps doing
exactly what it did to the books."""
import inspect
from decimal import Decimal

import pytest

from remit.errors import LimitExceeded, NotificationError, ScreeningHit, StoreError
from remit.money import Money
from remit.service import RemitService


def qar(value):
    return Money(value, "QAR")


def test_the_service_takes_an_optional_ledger_and_defaults_to_none():
    parameter = inspect.signature(RemitService.__init__).parameters["ledger"]
    assert parameter.default is None


def test_a_service_without_a_ledger_gets_its_own_fresh_one(hx_build):
    from remit.ledger import Ledger

    one, two = hx_build(), hx_build()
    assert isinstance(one.ledger, Ledger) and isinstance(two.ledger, Ledger)
    assert one.ledger is not two.ledger
    assert one.ledger.journal() == []


def test_services_with_their_own_ledgers_do_not_see_each_others_postings(hx_build):
    one, two = hx_build(), hx_build()
    one.send("C001", qar("500"), "INR", "Ravi Kumar")
    assert one.ledger.balance("PAYOUT_CLEARING") == Decimal("500.00")
    assert two.ledger.accounts() == [] and two.ledger.journal() == []


def test_a_ledger_that_is_passed_in_is_the_one_that_is_used(hx_build, hx_new_ledger):
    mine = hx_new_ledger()
    service = hx_build(ledger=mine)
    assert service.ledger is mine
    service.send("C001", qar("500"), "INR", "Ravi Kumar")
    assert mine.balance("PAYOUT_CLEARING") == Decimal("500.00")


def test_two_services_can_share_one_ledger_on_purpose(hx_build, hx_new_ledger):
    shared = hx_new_ledger()
    one, two = hx_build(ledger=shared), hx_build(ledger=shared)
    one.send("C001", qar("500"), "INR", "Ravi Kumar")
    two.send("C002", qar("100"), "INR", "Ravi Kumar")
    assert shared.balance("PAYOUT_CLEARING") == Decimal("600.00")


def test_send_posts_the_fee_and_the_surcharge_to_the_books(hx_build):
    service = hx_build()
    service.send("C001", qar("500"), "INR", "Ravi Kumar", express=True)  # fee 27.00
    book = service.ledger
    assert book.balance("CUSTOMER:C001") == Decimal("-527.00")
    assert book.balance("PARTNER_PAYABLE") == Decimal("8.10") and book.balance("FEE_INCOME") == Decimal("18.90")


def test_send_keeps_the_half_even_share_on_a_real_fee(hx_build):
    service = hx_build()
    service.send("C001", qar("157.25"), "INR", "Ravi Kumar")  # fee 5.15
    assert service.ledger.balance("PARTNER_PAYABLE") == Decimal("1.54")
    assert service.ledger.balance("FEE_INCOME") == Decimal("3.61")


def test_the_transfer_gets_its_id_before_the_journal_entries(hx_build):
    service = hx_build()
    result = service.send("C001", qar("500"), "INR", "Ravi Kumar")
    assert result.transfer.id == "TRF-000001"
    assert [e["entry_id"] for e in service.ledger.journal()] == ["JNL-000002", "JNL-000003", "JNL-000004", "JNL-000005"]
    assert {e["transfer_id"] for e in service.ledger.journal()} == {"TRF-000001"}


def test_a_quoted_transfer_posts_the_quoted_fee(hx_build):
    service = hx_build()
    quote = service.quote(qar("500"), "INR")
    service.send("C001", qar("500"), "INR", "Ravi Kumar", quote=quote)
    assert service.ledger.balance("CUSTOMER:C001") == -(quote.total.amount)


def test_transfers_that_are_refused_post_nothing(hx_build):
    service = hx_build()
    service.send("C002", qar("1500"), "INR", "Ravi Kumar")
    before = service.ledger.journal()
    with pytest.raises(LimitExceeded):
        service.send("C002", qar("600"), "INR", "Ravi Kumar")
    with pytest.raises(ScreeningHit):
        service.send("C001", qar("500"), "INR", "Test Sanctioned Person")
    assert service.ledger.journal() == before


def test_a_store_failure_after_the_ledger_leaves_the_postings_in_place(hx_build, monkeypatch):
    service = hx_build()

    def broken(transfer):
        raise StoreError("disk full")

    monkeypatch.setattr(service.store, "save_transfer", broken)
    with pytest.raises(StoreError):
        service.send("C001", qar("500"), "INR", "Ravi Kumar")
    assert len(service.ledger.journal()) == 4 and service.ledger.balance("PAYOUT_CLEARING") == Decimal("500.00")


def test_a_failed_notification_does_not_undo_the_postings(hx_build):
    class Broken:
        def notify(self, customer, template_id, **values):
            raise NotificationError("gateway down")

    service = hx_build()
    service.notifier = Broken()
    result = service.send("C001", qar("500"), "INR", "Ravi Kumar")
    assert result.notified is False and len(service.ledger.journal()) == 4


def test_the_command_line_still_sends_and_posts(tmp_path, hx_clock, capsys):
    import io

    from remit.cli import main

    env = {"REMIT_DB": str(tmp_path / "remit.db")}
    out = io.StringIO()
    assert main(["customer", "add", "--id", "C001", "--name", "Aisha Rahman", "--kyc", "T2"], environ=env, clock=hx_clock, out=out) == 0
    code = main(["send", "--customer", "C001", "QAR", "500", "INR", "--recipient", "Ravi Kumar"], environ=env, clock=hx_clock, out=out)
    assert code == 0 and "sent TRF-000001" in out.getvalue()
