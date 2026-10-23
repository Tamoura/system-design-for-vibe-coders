"""REMIT-318: the limit warning. The approved wording."""
from decimal import Decimal

from remit.money import Money
from remit.notify import TEMPLATES, render


def qar(value):
    return Money(value, "QAR")


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
