"""Hidden acceptance tests for lab m04 (REMIT-318, the daily-limit warning).

They test only what the ticket states, through the public interface it names: ``notify.TEMPLATES`` / ``render``,
``RemitService.send`` and the notifier that receives the messages. The expected texts are written out here from the
ticket's approved wording, and the expected percentages and remaining amounts are computed with plain Decimal
arithmetic, so a sound implementation passes however it is structured. They run inside a copy of the learner's
repository, so they use the repository's own fixtures (``service``, ``store``, ``customers``, ``clock``, ``notifier``).
"""
from __future__ import annotations

import dataclasses
import inspect
import io
import re
from decimal import Decimal

import pytest

from najmkit import audit
from remit import ledger
from remit.cli import main as cli_main
from remit.errors import LimitExceeded, NotificationError, ScreeningHit
from remit.fx import StaticRateProvider
from remit.models import Customer
from remit.money import Money
from remit.notify import TEMPLATES, InMemoryNotifier, render
from remit.service import RemitService, SendResult

EN = "Hi {name}, this transfer takes you to {percent}% of your daily sending limit. You can send {remaining} more today."
AR = "مرحباً {name}، بهذا التحويل وصلت إلى {percent}٪ من حد الإرسال اليومي. يمكنك اليوم إرسال مبلغ إضافي أقصاه {remaining}."
DAILY = {"T1": Decimal("2000.00"), "T2": Decimal("10000.00"), "T3": Decimal("30000.00")}
TO_ARABIC = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
NAME = "Layla Hassan"


def qar(value) -> Money:
    return Money(value, "QAR")


def english_money(amount: Decimal) -> str:
    return f"{amount:,.2f} QAR"


def arabic_money(amount: Decimal) -> str:
    number = f"{amount:,.2f}".translate(TO_ARABIC).replace(",", "٬").replace(".", "٫")
    return f"{number} ريال قطري"


def expected(lang: str, name: str, percent: int, remaining: Decimal) -> str:
    if lang == "en":
        return EN.format(name=name, percent=percent, remaining=english_money(remaining))
    return AR.format(name=name, percent=str(percent).translate(TO_ARABIC), remaining=arabic_money(remaining))


def floor_percent(total: Decimal, limit: Decimal) -> int:
    return int((total * 100) // limit)


@pytest.fixture
def make_customer(store):
    made: list[Customer] = []

    def make(tier: str = "T1", lang: str = "en", name: str = NAME) -> Customer:
        person = Customer(f"H{len(made) + 1:03d}", name, tier, "none", lang)
        store.add_customer(person)
        made.append(person)
        return person

    return make


def send(service, customer: Customer, amount, receive: str = "INR", **kwargs):
    return service.send(customer.id, qar(amount), receive, "Ravi Kumar", **kwargs)


def kinds(notifier, customer: Customer) -> list[str]:
    return [n.template_id for n in notifier.sent if n.customer_id == customer.id]


def warnings(notifier, customer: Customer) -> list:
    return [n for n in notifier.sent if n.customer_id == customer.id and n.template_id == "limit_warning"]


# ---------------------------------------------------------------------------------------------
# the template and its approved wording
# ---------------------------------------------------------------------------------------------
def test_the_limit_warning_template_exists_in_english_and_arabic():
    assert "limit_warning" in TEMPLATES
    assert set(TEMPLATES["limit_warning"]) == {"en", "ar"}


def test_the_english_wording_is_the_approved_wording():
    assert TEMPLATES["limit_warning"]["en"] == EN
    text = render("limit_warning", "en", name="Bilal Khan", percent=Decimal(85), remaining=Money("300.00", "QAR"))
    assert text == "Hi Bilal Khan, this transfer takes you to 85% of your daily sending limit. You can send 300.00 QAR more today."


def test_the_arabic_wording_is_the_approved_wording_with_arabic_digits():
    assert TEMPLATES["limit_warning"]["ar"] == AR
    text = render("limit_warning", "ar", name="Fatima Noor", percent=Decimal(85), remaining=Money("300.00", "QAR"))
    assert text == "مرحباً Fatima Noor، بهذا التحويل وصلت إلى ٨٥٪ من حد الإرسال اليومي. يمكنك اليوم إرسال مبلغ إضافي أقصاه ٣٠٠٫٠٠ ريال قطري."
    assert not any(ch in text for ch in "0123456789")


def test_the_existing_messages_did_not_change():
    sent = dict(name="Aisha", transfer_id="TRF-000001", recipient="Ravi Kumar", send_amount=Money("500.00", "QAR"),
                fee=Money("12.00", "QAR"), receive_amount=Money("11286.00", "INR"))
    assert render("transfer_sent", "en", **sent) == (
        "Hi Aisha, your transfer TRF-000001 was sent. Ravi Kumar received 11,286.00 INR. "
        "You paid 500.00 QAR plus a fee of 12.00 QAR."
    )
    assert render("transfer_sent", "ar", **sent).startswith("مرحباً Aisha، تم إرسال تحويلك TRF-000001.")
    failed = dict(name="Aisha", recipient="Ravi Kumar", send_amount=Money("2500", "QAR"), reason="It would take you over your sending limit.")
    assert render("transfer_failed", "en", **failed) == (
        "Hi Aisha, your transfer of 2,500.00 QAR to Ravi Kumar could not be completed. "
        "It would take you over your sending limit. No money has been taken from your account."
    )


# ---------------------------------------------------------------------------------------------
# when to warn: the 80% line, the rounding, the tiers
# ---------------------------------------------------------------------------------------------
LINE = [
    # tier, amount, warned?
    ("T1", "100.00", False), ("T1", "1000.00", False), ("T1", "1500.00", False), ("T1", "1599.99", False),
    ("T1", "1600.00", True), ("T1", "1600.01", True), ("T1", "1615.00", True), ("T1", "1666.67", True),
    ("T1", "1699.99", True), ("T1", "1700.00", True), ("T1", "1999.99", True), ("T1", "2000.00", True),
    ("T2", "5000.00", False), ("T2", "7999.99", False), ("T2", "8000.00", True), ("T2", "9999.99", True),
    ("T3", "20000.00", False), ("T3", "23999.99", False), ("T3", "24000.00", True), ("T3", "25000.00", True),
]


@pytest.mark.parametrize("tier,amount,warned", LINE)
def test_the_decision_and_the_numbers_match_the_rule_for_many_amounts(service, notifier, make_customer, tier, amount, warned):
    person = make_customer(tier)
    send(service, person, amount)
    got = warnings(notifier, person)
    total = Decimal(amount)
    assert (len(got) == 1) == (total * 5 >= DAILY[tier] * 4) == warned
    if warned:
        assert got[0].text == expected("en", NAME, floor_percent(total, DAILY[tier]), DAILY[tier] - total)
        assert kinds(notifier, person) == ["transfer_sent", "limit_warning"]
    else:
        assert kinds(notifier, person) == ["transfer_sent"]


def test_exactly_eighty_percent_is_warned_and_one_cent_less_is_not(service, notifier, make_customer):
    under, exact = make_customer("T1"), make_customer("T1")
    send(service, under, "1599.99")
    send(service, exact, "1600.00")
    assert warnings(notifier, under) == [] and len(warnings(notifier, exact)) == 1


def test_the_percentage_is_rounded_down_never_up(service, notifier, make_customer):
    near_the_top, just_over = make_customer("T1"), make_customer("T1")
    send(service, near_the_top, "1999.99")
    send(service, just_over, "1615.00")
    assert "99%" in warnings(notifier, near_the_top)[0].text and "100%" not in warnings(notifier, near_the_top)[0].text
    assert "80%" in warnings(notifier, just_over)[0].text and "81%" not in warnings(notifier, just_over)[0].text


def test_reaching_the_limit_exactly_is_allowed_and_warned_with_nothing_left(service, notifier, make_customer):
    person = make_customer("T1")
    send(service, person, "2000.00")
    (note,) = warnings(notifier, person)
    assert note.text == expected("en", NAME, 100, Decimal("0.00"))


def test_the_total_includes_what_was_already_sent_today(service, notifier, make_customer):
    person = make_customer("T1")
    send(service, person, "1000.00")
    assert warnings(notifier, person) == []
    send(service, person, "600.00")
    (note,) = warnings(notifier, person)
    assert note.text == expected("en", NAME, 80, Decimal("400.00"))


def test_every_transfer_past_the_line_is_warned_not_only_the_first(service, notifier, make_customer):
    person = make_customer("T1")
    for amount in ("1600.00", "100.00", "200.00", "100.00"):
        send(service, person, amount)
    texts = [n.text for n in warnings(notifier, person)]
    assert texts == [
        expected("en", NAME, 80, Decimal("400.00")),
        expected("en", NAME, 85, Decimal("300.00")),
        expected("en", NAME, 95, Decimal("100.00")),
        expected("en", NAME, 100, Decimal("0.00")),
    ]


def test_fees_do_not_count_towards_the_total(service, notifier, make_customer):
    person = make_customer("T1")
    result = send(service, person, "1590.00")  # 79.5% of the limit; with the fee it would be over 80%
    assert result.total_debited.amount > Decimal("1600.00")
    assert warnings(notifier, person) == []


def test_express_transfers_follow_the_same_rule(service, notifier, make_customer):
    person = make_customer("T1")
    send(service, person, "1600.00", express=True)
    assert len(warnings(notifier, person)) == 1


def test_the_total_spans_every_corridor(service, notifier, make_customer):
    person = make_customer("T1")
    send(service, person, "1000.00", "INR")
    send(service, person, "700.00", "PHP")
    assert len(warnings(notifier, person)) == 1


# ---------------------------------------------------------------------------------------------
# which limit, which day
# ---------------------------------------------------------------------------------------------
def test_only_the_daily_limit_matters_not_the_monthly_one(service, clock, notifier, make_customer):
    person = make_customer("T1")  # monthly limit 8,000.00
    for _ in range(5):
        send(service, person, "1500.00")  # 75% of the daily limit each day, 93.75% of the monthly one by day five
        clock.advance(days=1)
    assert warnings(notifier, person) == []
    assert kinds(notifier, person).count("transfer_sent") == 5


def test_yesterdays_transfers_do_not_count(service, clock, notifier, make_customer):
    person = make_customer("T1")
    send(service, person, "1000.00")
    clock.advance(days=1)
    send(service, person, "700.00")
    assert warnings(notifier, person) == []


def test_the_day_is_the_qatar_day_not_the_utc_day(service, clock, notifier, make_customer):
    across, within = make_customer("T1"), make_customer("T1")
    clock.set("2026-03-02T20:59:00+00:00")  # 23:59 in Qatar
    send(service, across, "1000.00")
    send(service, within, "1000.00")
    clock.set("2026-03-02T20:59:30+00:00")  # still the same Qatar day
    send(service, within, "700.00")
    clock.set("2026-03-02T21:00:00+00:00")  # 00:00 in Qatar: a new day
    send(service, across, "700.00")
    assert len(warnings(notifier, within)) == 1
    assert warnings(notifier, across) == []


# ---------------------------------------------------------------------------------------------
# language
# ---------------------------------------------------------------------------------------------
def test_an_arabic_customer_gets_the_arabic_warning_with_arabic_digits(service, notifier, make_customer):
    person = make_customer("T1", "ar", "Fatima Noor")
    send(service, person, "1700.00")
    (note,) = warnings(notifier, person)
    assert note.lang == "ar"
    assert note.text == expected("ar", "Fatima Noor", 85, Decimal("300.00"))
    assert not any(ch in note.text for ch in "0123456789")


def test_an_english_customer_gets_english_only(service, notifier, make_customer):
    person = make_customer("T1", "en")
    send(service, person, "1700.00")
    (note,) = warnings(notifier, person)
    assert note.lang == "en" and note.text == expected("en", NAME, 85, Decimal("300.00"))
    assert not re.search(r"[؀-ۿ]", note.text)


# ---------------------------------------------------------------------------------------------
# when not to warn, order, count
# ---------------------------------------------------------------------------------------------
def test_the_warning_comes_straight_after_transfer_sent_exactly_once(service, notifier, make_customer):
    person = make_customer("T1")
    send(service, person, "1700.00")
    assert kinds(notifier, person) == ["transfer_sent", "limit_warning"]
    assert len(notifier.sent) == 2


def test_a_refused_transfer_gets_no_warning(service, notifier, make_customer, store):
    refused, warned_then_refused = make_customer("T1"), make_customer("T1")
    send(service, refused, "1500.00")
    with pytest.raises(LimitExceeded):
        send(service, refused, "600.00")
    assert kinds(notifier, refused) == ["transfer_sent", "transfer_failed"]
    send(service, warned_then_refused, "1900.00")
    with pytest.raises(LimitExceeded):
        send(service, warned_then_refused, "200.00")
    assert kinds(notifier, warned_then_refused) == ["transfer_sent", "limit_warning", "transfer_failed"]
    assert store.count_transfers() == 2


def test_a_held_transfer_gets_no_warning(service, notifier, make_customer, store):
    person = make_customer("T1")
    send(service, person, "1700.00")
    with pytest.raises(ScreeningHit):
        service.send(person.id, qar("100.00"), "INR", "Test Sanctioned Person")
    assert kinds(notifier, person) == ["transfer_sent", "limit_warning", "transfer_failed"]
    assert store.count_transfers() == 1


def test_an_invalid_request_sends_nothing(service, notifier, make_customer):
    person = make_customer("T1")
    send(service, person, "1700.00")
    before = len(notifier.sent)
    with pytest.raises(Exception):
        service.send(person.id, qar("100.00"), "INR", "   ")
    assert len(notifier.sent) == before


# ---------------------------------------------------------------------------------------------
# best effort, interface, money
# ---------------------------------------------------------------------------------------------
class WarningFails(InMemoryNotifier):
    def notify(self, customer, template_id, **values):
        if template_id == "limit_warning":
            raise NotificationError("the gateway is down")
        return super().notify(customer, template_id, **values)


def test_a_warning_that_cannot_be_delivered_does_not_undo_the_transfer(store, customers, clock, tmp_path):
    audit.configure(tmp_path / "audit.jsonl")
    flaky = WarningFails()
    flaky_service = RemitService(store, StaticRateProvider(), ["Test Sanctioned Person"], clock, flaky)
    result = flaky_service.send("C002", qar("1700.00"), "INR", "Ravi Kumar")  # Bilal, T1
    assert result.notified is True and store.count_transfers() == 1
    assert [n.template_id for n in flaky.sent] == ["transfer_sent"]
    events = audit.read_events()
    failed = [e for e in events if e["event"] == "notification.failed"]
    assert [e["template"] for e in failed] == ["limit_warning"]
    assert any(e["event"] == "transfer.sent" for e in events)


def test_send_keeps_its_signature_and_its_result_keeps_its_fields():
    assert list(inspect.signature(RemitService.send).parameters) == [
        "self", "customer_id", "send_amount", "receive_currency", "recipient_name", "express", "delivery_method", "quote",
    ]
    assert [f.name for f in dataclasses.fields(SendResult)] == ["transfer", "total_debited", "limits", "notified"]


def test_the_result_still_reports_the_position_before_the_transfer(service, make_customer):
    person = make_customer("T1")
    first = send(service, person, "1000.00")
    second = send(service, person, "700.00")
    assert first.limits.daily_used == qar("0.00") and second.limits.daily_used == qar("1000.00")


def test_the_warning_does_not_touch_the_money(service, make_customer, store):
    person = make_customer("T1")
    quote = service.quote(qar("1600.00"), "INR")
    result = send(service, person, "1600.00")
    assert result.transfer.fee == quote.fee and result.total_debited == qar("1600.00") + quote.fee
    assert store.count_transfers() == 1
    assert ledger.balance("PAYOUT_CLEARING") == Decimal("1600.00")
    assert ledger.balance(ledger.customer_account(person.id)) == -(Decimal("1600.00") + quote.fee.amount)


def test_the_command_line_prints_the_warning_after_the_sent_message(clock, tmp_path):
    env = {"REMIT_DB": str(tmp_path / "remit.db")}

    def run(*argv):
        out, err = io.StringIO(), io.StringIO()
        code = cli_main(list(argv), environ=env, clock=clock, out=out, err=err)
        return code, out.getvalue().splitlines()

    assert run("customer", "add", "--id", "C001", "--name", "Bilal Khan", "--kyc", "T1")[0] == 0
    code, lines = run("send", "--customer", "C001", "QAR", "1700", "INR", "--recipient", "Ravi Kumar")
    assert code == 0 and len(lines) == 3
    assert lines[0].startswith("[notification to C001 (en)] Hi Bilal Khan, your transfer TRF-000001 was sent.")
    assert lines[1] == "[notification to C001 (en)] " + expected("en", "Bilal Khan", 85, Decimal("300.00"))
    assert lines[2].startswith("sent TRF-000001:")
