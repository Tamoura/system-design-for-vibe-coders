"""Lab m14, hidden acceptance tests, part 4: the Bangladesh wording, in English and Arabic.

The expected sentences below are the ticket's approved wording with the values filled in by hand.
"""
from decimal import Decimal

import pytest

from remit.money import Money

EN_EXPECTED = (
    "Hi Aisha Rahman, your transfer TRF-000001 to Bangladesh was sent. "
    "Rahim Uddin received 16,437.25 BDT at a rate of 1 QAR = 32.8745 BDT. "
    "You paid 500.00 QAR plus a fee of 14.50 QAR. "
    "Please keep this message as your receipt."
)
AR_EXPECTED = (
    "مرحباً Mariam Saleh، تم إرسال تحويلك TRF-000001 إلى بنغلاديش. "
    "تم استلام مبلغ ٣٩٤٬٤٩٤٫٠٠ تاكا بنغلاديشية من قبل Rahim Uddin بسعر صرف ١ ريال قطري مقابل ٣٢٫٨٧٤٥ تاكا. "
    "المبلغ المرسل: ١٢٬٠٠٠٫٠٠ ريال قطري، والرسوم: ١٣٠٫٠٠ ريال قطري. "
    "يرجى الاحتفاظ بهذه الرسالة كإيصال لك."
)


def values(**override):
    base = dict(
        name="Aisha Rahman",
        transfer_id="TRF-000001",
        recipient="Rahim Uddin",
        receive_amount=Money("16437.25", "BDT"),
        send_amount=Money("500", "QAR"),
        fee=Money("14.50", "QAR"),
        rate=Decimal("32.8745"),
    )
    base.update(override)
    return base


def test_the_english_wording_is_the_approved_text():
    from remit.notify import render

    assert render("transfer_sent_bdt", "en", **values()) == EN_EXPECTED


def test_the_arabic_wording_is_the_approved_text_with_arabic_digits_everywhere():
    from remit.notify import render

    text = render(
        "transfer_sent_bdt",
        "ar",
        **values(
            name="Mariam Saleh",
            receive_amount=Money("394494.00", "BDT"),
            send_amount=Money("12000", "QAR"),
            fee=Money("130.00", "QAR"),
        ),
    )
    assert text == AR_EXPECTED
    assert not any(ch in text.split("TRF-000001")[1].split("Rahim Uddin")[0] for ch in "0123456789")
    assert not any(ch in text.split("Rahim Uddin")[1] for ch in "0123456789")  # amounts, rate and the "1 QAR"


def test_the_template_exists_in_both_languages_and_needs_the_rate():
    from remit.errors import MissingTemplateVariable
    from remit.models import LANGUAGES
    from remit.notify import TEMPLATES, render

    assert set(TEMPLATES["transfer_sent_bdt"]) == set(LANGUAGES)
    without_rate = {k: v for k, v in values().items() if k != "rate"}
    with pytest.raises(MissingTemplateVariable, match="rate"):
        render("transfer_sent_bdt", "en", **without_rate)


def test_the_existing_templates_are_word_for_word_what_they_were():
    from remit.notify import render

    sent = dict(
        name="Aisha",
        transfer_id="TRF-000001",
        recipient="Ravi Kumar",
        receive_amount=Money("11286.00", "INR"),
        send_amount=Money("500", "QAR"),
        fee=Money("12.00", "QAR"),
    )
    assert render("transfer_sent", "en", **sent) == (
        "Hi Aisha, your transfer TRF-000001 was sent. Ravi Kumar received 11,286.00 INR. "
        "You paid 500.00 QAR plus a fee of 12.00 QAR."
    )
    assert render("transfer_sent", "ar", **sent).startswith("مرحباً Aisha، تم إرسال تحويلك TRF-000001.")
