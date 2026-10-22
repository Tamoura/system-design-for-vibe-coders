from decimal import Decimal

import pytest

from remit.errors import MissingTemplateVariable, UnknownTemplate, UnsupportedLanguage
from remit.models import Customer
from remit.money import Money
from remit.notify import (
    InMemoryNotifier,
    failure_reason,
    format_money,
    format_number,
    localize_digits,
    render,
)

SENT = dict(
    name="Aisha",
    transfer_id="TRF-000001",
    recipient="Ravi Kumar",
    send_amount=Money("500.00", "QAR"),
    fee=Money("12.00", "QAR"),
    receive_amount=Money("11286.00", "INR"),
)


def test_transfer_sent_in_english():
    assert render("transfer_sent", "en", **SENT) == (
        "Hi Aisha, your transfer TRF-000001 was sent. "
        "Ravi Kumar received 11,286.00 INR. "
        "You paid 500.00 QAR plus a fee of 12.00 QAR."
    )


def test_transfer_sent_in_arabic_uses_arabic_indic_digits():
    text = render("transfer_sent", "ar", **SENT)
    assert text == (
        "مرحباً Aisha، تم إرسال تحويلك TRF-000001. "
        "تم استلام مبلغ ١١٬٢٨٦٫٠٠ روبية هندية من قبل Ravi Kumar. "
        "المبلغ المرسل: ٥٠٠٫٠٠ ريال قطري، والرسوم: ١٢٫٠٠ ريال قطري."
    )
    amounts = text.split("TRF-000001")[1]
    assert not any(ch in amounts for ch in "0123456789")  # no Western digits in the amounts


def test_transfer_failed_in_both_languages():
    values = dict(name="Aisha", recipient="Ravi Kumar", send_amount=Money("2500", "QAR"))
    en = render("transfer_failed", "en", reason=failure_reason("limit_exceeded", "en"), **values)
    assert en == (
        "Hi Aisha, your transfer of 2,500.00 QAR to Ravi Kumar could not be completed. "
        "It would take you over your sending limit. No money has been taken from your account."
    )
    ar = render("transfer_failed", "ar", reason=failure_reason("needs_review", "ar"), **values)
    assert "٢٬٥٠٠٫٠٠ ريال قطري" in ar and ar.startswith("مرحباً Aisha")


def test_every_template_exists_in_every_supported_language():
    from remit.notify import TEMPLATES
    from remit.models import LANGUAGES

    for template_id, by_lang in TEMPLATES.items():
        assert set(by_lang) == set(LANGUAGES), template_id


def test_format_money_english_and_arabic():
    assert format_money(Money("1234.5", "QAR"), "en") == "1,234.50 QAR"
    assert format_money(Money("1234.5", "QAR"), "ar") == "١٬٢٣٤٫٥٠ ريال قطري"
    assert format_money(Money("0.07", "PHP"), "ar") == "٠٫٠٧ بيزو فلبيني"
    assert format_money(Money("1", "BDT"), "ar").endswith("تاكا بنغلاديشية")


def test_numbers_and_digits_follow_the_language():
    assert format_number(Decimal("22.5720"), "en") == "22.5720"
    assert format_number(Decimal("22.5720"), "ar") == "٢٢٫٥٧٢٠"
    assert localize_digits("TRF 2026", "en") == "TRF 2026"
    assert localize_digits("TRF 2026", "ar") == "TRF ٢٠٢٦"


def test_missing_variables_are_reported_by_name_and_extras_are_ignored():
    values = {k: v for k, v in SENT.items() if k != "fee"}
    with pytest.raises(MissingTemplateVariable, match="fee"):
        render("transfer_sent", "en", **values)
    assert render("transfer_sent", "en", extra="unused", **SENT) == render("transfer_sent", "en", **SENT)


def test_unknown_template_and_language():
    with pytest.raises(UnknownTemplate):
        render("no_such_template", "en", **SENT)
    with pytest.raises(UnsupportedLanguage):
        render("transfer_sent", "fr", **SENT)
    with pytest.raises(UnknownTemplate):
        failure_reason("nope", "en")


def test_in_memory_notifier_renders_in_the_customers_language():
    notifier = InMemoryNotifier()
    values = {k: v for k, v in SENT.items() if k != "name"}
    notifier.notify(Customer("C1", "Aisha", "T1", language="en"), "transfer_sent", **values)
    notifier.notify(Customer("C3", "مريم", "T3", language="ar"), "transfer_sent", **values)
    english, arabic = notifier.sent
    assert english.lang == "en" and english.text.startswith("Hi Aisha")
    assert arabic.lang == "ar" and arabic.text.startswith("مرحباً مريم") and arabic.customer_id == "C3"
