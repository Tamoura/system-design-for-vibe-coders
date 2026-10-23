"""REMIT-318: the limit warning. The approved wording, and when the service sends it."""
from decimal import Decimal

import pytest

from remit.money import Money
from remit.notify import TEMPLATES, render

# Bilal (C002) is T1: daily limit 2,000.00 QAR, so the 80% line is 1,600.00. Mariam (C003) is T3 and Arabic: 30,000.00.


def qar(value):
    return Money(value, "QAR")


def warnings(notifier):
    return [n for n in notifier.sent if n.template_id == "limit_warning"]


# -- the wording --------------------------------------------------------------------------------------------
def test_the_template_exists_in_both_languages():
    assert set(TEMPLATES["limit_warning"]) == {"en", "ar"}


def test_the_english_wording():
    text = render("limit_warning", "en", name="Bilal Khan", percent=Decimal(85), remaining=qar("300.00"))
    assert text == "Hi Bilal Khan, this transfer takes you to 85% of your daily sending limit. You can send 300.00 QAR more today."


def test_the_arabic_wording_has_arabic_digits_only():
    text = render("limit_warning", "ar", name="Fatima Noor", percent=Decimal(85), remaining=qar("300.00"))
    assert text == "مرحباً Fatima Noor، بهذا التحويل وصلت إلى ٨٥٪ من حد الإرسال اليومي. يمكنك اليوم إرسال مبلغ إضافي أقصاه ٣٠٠٫٠٠ ريال قطري."
    assert not any(ch in text for ch in "0123456789")


# -- the 80% line ---------------------------------------------------------------------------------------------
def test_no_warning_one_cent_under_the_line(service, notifier):
    service.send("C002", qar("1599.99"), "INR", "Ravi Kumar")
    assert [n.template_id for n in notifier.sent] == ["transfer_sent"]


def test_a_warning_exactly_on_the_line_straight_after_transfer_sent(service, notifier):
    service.send("C002", qar("1600.00"), "INR", "Ravi Kumar")
    assert [n.template_id for n in notifier.sent] == ["transfer_sent", "limit_warning"]
    assert notifier.sent[1].text == (
        "Hi Bilal Khan, this transfer takes you to 80% of your daily sending limit. You can send 400.00 QAR more today."
    )


@pytest.mark.parametrize("amount,shown,left", [("1615.00", "80%", "385.00"), ("1999.99", "99%", "0.01"), ("2000.00", "100%", "0.00")])
def test_the_percentage_is_rounded_down(service, notifier, amount, shown, left):
    service.send("C002", qar(amount), "INR", "Ravi Kumar")
    (note,) = warnings(notifier)
    assert f"to {shown} of your daily" in note.text and f"send {left} QAR more" in note.text


def test_the_total_includes_what_was_sent_earlier_today(service, notifier):
    service.send("C002", qar("1000.00"), "INR", "Ravi Kumar")
    assert warnings(notifier) == []
    service.send("C002", qar("600.00"), "INR", "Ravi Kumar")
    assert len(warnings(notifier)) == 1


def test_every_later_transfer_past_the_line_is_warned_too(service, notifier):
    for amount in ("1600.00", "100.00"):
        service.send("C002", qar(amount), "INR", "Ravi Kumar")
    assert ["80%" in n.text for n in warnings(notifier)] == [True, False]
    assert "85%" in warnings(notifier)[1].text


def test_fees_do_not_count_and_yesterday_does_not_count(service, notifier, clock):
    service.send("C002", qar("1590.00"), "INR", "Ravi Kumar")  # 79.5%; with the fee it would be over 80%
    clock.advance(days=1)
    service.send("C002", qar("100.00"), "INR", "Ravi Kumar")
    assert warnings(notifier) == []
