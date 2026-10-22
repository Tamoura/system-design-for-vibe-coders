"""A light end-to-end test of RemitService with an in-memory store, a fixed clock and an
in-memory notifier. The ledger and the name screening run for real inside send()."""
from decimal import Decimal

import pytest

from najmkit import audit
from remit.errors import (
    AmountOutOfRange,
    InvalidRequest,
    LimitExceeded,
    NotificationError,
    QuoteExpired,
    QuoteMismatch,
    ScreeningHit,
    UnknownCorridor,
    UnknownCustomer,
    UnsupportedDeliveryMethod,
)
from remit.models import Customer
from remit.money import Money


def qar(value):
    return Money(value, "QAR")


def test_quote_prices_a_transfer_without_sending_it(service, store, now):
    quote = service.quote(qar("500"), "INR")
    assert quote.fee == qar("12.00") and quote.total == qar("512.00")
    assert quote.fx.rate == Decimal("22.5720") and quote.fx.receive == Money("11286.00", "INR")
    assert quote.fx.expires_at == now.replace(minute=1)  # 60 seconds after 09:00
    assert quote.delivery_method == "bank_deposit" and not quote.express
    assert store.count_transfers() == 0


def test_express_quote_adds_the_surcharge(service):
    assert service.quote(qar("500"), "INR", express=True).fee == qar("27.00")


def test_send_runs_the_whole_flow(service, store, notifier, now):
    result = service.send("C001", qar("500"), "INR", "  Ravi Kumar ")
    transfer = result.transfer
    assert transfer.id == "TRF-000001"
    assert (transfer.customer_id, transfer.corridor, transfer.recipient_name) == ("C001", "QAR-INR", "Ravi Kumar")
    assert (transfer.send_amount, transfer.fee) == (qar("500.00"), qar("12.00"))
    assert (transfer.receive_amount, transfer.rate) == (Money("11286.00", "INR"), Decimal("22.5720"))
    assert transfer.created_at == now and transfer.status == "completed"
    assert result.total_debited == qar("512.00") and result.notified
    assert result.limits.allowed and result.limits.daily_used == qar("0")
    assert store.get_transfer("TRF-000001") == transfer

    (note,) = notifier.sent
    assert note.template_id == "transfer_sent" and note.customer_id == "C001"
    assert note.text.startswith("Hi Aisha Rahman, your transfer TRF-000001 was sent.")


def test_an_arabic_speaking_customer_gets_an_arabic_notification(service, notifier):
    service.send("C003", qar("1000"), "PHP", "Maria Santos", delivery_method="cash_pickup")
    (note,) = notifier.sent
    assert note.lang == "ar" and note.text.startswith("مرحباً Mariam Saleh")
    assert "١٬٠٠٠٫٠٠ ريال قطري" in note.text  # the 1,000 QAR sent, in Arabic-Indic digits
    assert "١٥٬٢٠٧٫٥٠ بيزو فلبيني" in note.text  # 1,000 x 15.2075 received


def test_history_lists_transfers_oldest_first(service, clock):
    service.send("C001", qar("100"), "INR", "Ravi Kumar")
    clock.advance(hours=1)
    service.send("C001", qar("200"), "INR", "Ravi Kumar")
    assert [t.send_amount for t in service.history("C001")] == [qar("100"), qar("200")]


def test_invalid_requests_are_rejected_before_anything_is_saved(service, store, notifier):
    cases = [
        (dict(customer_id="C999"), UnknownCustomer),
        (dict(recipient="   "), InvalidRequest),
        (dict(amount="49.99"), AmountOutOfRange),
        (dict(receive="USD"), UnknownCorridor),
        (dict(delivery="cash_pickup"), UnsupportedDeliveryMethod),
    ]
    for kwargs, error in cases:
        args = dict(customer_id="C001", amount="500", receive="INR", recipient="Ravi Kumar", delivery=None)
        args.update(kwargs)
        with pytest.raises(error):
            service.send(
                args["customer_id"], qar(args["amount"]), args["receive"], args["recipient"], delivery_method=args["delivery"]
            )
    assert store.count_transfers() == 0 and notifier.sent == []


def test_limits_are_enforced_and_the_customer_is_told(service, store, notifier, tmp_path):
    audit.configure(tmp_path / "audit.jsonl")
    service.send("C002", qar("1500"), "INR", "Ravi Kumar")  # Bilal is T1: 2,000 a day
    with pytest.raises(LimitExceeded) as caught:
        service.send("C002", qar("600"), "INR", "Ravi Kumar")
    assert caught.value.result.reason == "daily_limit_exceeded"
    assert store.count_transfers() == 1
    assert [n.template_id for n in notifier.sent] == ["transfer_sent", "transfer_failed"]
    assert "over your sending limit" in notifier.sent[1].text
    rejected = [e for e in audit.read_events() if e["event"] == "transfer.rejected"]
    assert rejected[0]["reason"] == "limit_exceeded" and rejected[0]["customer_id"] == "C002"


def test_a_watchlist_hit_on_the_recipient_holds_the_transfer(service, store, notifier):
    with pytest.raises(ScreeningHit) as caught:
        service.send("C001", qar("500"), "INR", "Test Sanctioned Person")
    assert caught.value.matches[0].entry == "Test Sanctioned Person"
    assert store.count_transfers() == 0
    (note,) = notifier.sent
    assert note.template_id == "transfer_failed"
    assert "review" in note.text
    wording = note.text.replace("Test Sanctioned Person", "").lower()
    assert "sanction" not in wording and "watchlist" not in wording  # never tip off


def test_a_watchlist_hit_on_the_sender_holds_the_transfer(service, store):
    store.add_customer(Customer("C100", "Test Sanctioned Person", "T1"))
    with pytest.raises(ScreeningHit):
        service.send("C100", qar("500"), "INR", "Ravi Kumar")


def test_a_quote_can_be_used_for_the_send_within_60_seconds(service, clock):
    quote = service.quote(qar("500"), "INR")
    clock.advance(seconds=59)
    result = service.send("C001", qar("500"), "INR", "Ravi Kumar", quote=quote)
    assert result.transfer.rate == quote.fx.rate and result.transfer.fee == quote.fee


def test_an_expired_quote_is_refused(service, clock, store):
    quote = service.quote(qar("500"), "INR")
    clock.advance(seconds=60)
    with pytest.raises(QuoteExpired):
        service.send("C001", qar("500"), "INR", "Ravi Kumar", quote=quote)
    assert store.count_transfers() == 0


def test_a_quote_for_something_else_is_refused(service):
    quote = service.quote(qar("500"), "INR")
    with pytest.raises(QuoteMismatch):
        service.send("C001", qar("600"), "INR", "Ravi Kumar", quote=quote)
    with pytest.raises(QuoteMismatch):
        service.send("C001", qar("500"), "INR", "Ravi Kumar", express=True, quote=quote)


def test_a_failed_notification_does_not_undo_the_transfer(service, store, tmp_path):
    class Broken:
        def notify(self, customer, template_id, **values):
            raise NotificationError("gateway down")

    audit.configure(tmp_path / "audit.jsonl")
    service.notifier = Broken()
    result = service.send("C001", qar("500"), "INR", "Ravi Kumar")
    assert result.notified is False
    assert store.count_transfers() == 1
    assert [e["event"] for e in audit.read_events()] == ["notification.failed", "transfer.sent"]


def test_sending_writes_an_audit_event_without_personal_data(service, tmp_path):
    audit.configure(tmp_path / "audit.jsonl")
    service.send("C001", qar("500"), "INR", "Ravi Kumar", express=True)
    (event,) = audit.read_events()
    assert event == {
        "ts": "2026-03-02T09:00:00+00:00",
        "event": "transfer.sent",
        "transfer_id": "TRF-000001",
        "customer_id": "C001",
        "corridor": "QAR-INR",
        "send_amount": "500.00 QAR",
        "fee": "27.00 QAR",
        "express": True,
    }
