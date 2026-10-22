"""Hidden checks for lab m10, task A: the ``transfer_delayed`` notification (English and Arabic)."""
import pytest

from remit.errors import MissingTemplateVariable
from remit.money import Money
from remit.notify import TEMPLATES, render

VALUES = dict(name="Aisha", transfer_id="TRF-000007", recipient="Ravi Kumar")

EN = (
    "Hi Aisha, your transfer TRF-000007 to Ravi Kumar is taking longer than expected. "
    "We are working on it and will message you as soon as it arrives. "
    "We are sorry for the wait."
)
AR = (
    "مرحباً Aisha، تأخّر وصول تحويلك TRF-000007 إلى Ravi Kumar عن الموعد المتوقع. "
    "نعمل على إتمامه وسنراسلك فور وصوله. "
    "نعتذر عن الانتظار."
)


def test_the_template_exists_in_english_and_arabic():
    assert set(TEMPLATES["transfer_delayed"]) == {"en", "ar"}


def test_the_english_wording_is_the_approved_text():
    assert render("transfer_delayed", "en", **VALUES) == EN


def test_the_arabic_wording_is_the_approved_text():
    assert render("transfer_delayed", "ar", **VALUES) == AR


def test_it_reaches_each_customer_in_their_own_language(customers, notifier):
    english = notifier.notify(customers["C001"], "transfer_delayed", transfer_id="TRF-000007", recipient="Ravi Kumar")
    arabic = notifier.notify(customers["C003"], "transfer_delayed", transfer_id="TRF-000008", recipient="Ravi Kumar")
    assert english.lang == "en" and english.text.startswith("Hi Aisha Rahman, your transfer TRF-000007")
    assert arabic.lang == "ar" and arabic.text.startswith("مرحباً Mariam Saleh، تأخّر وصول تحويلك TRF-000008")
    assert [n.template_id for n in notifier.sent] == ["transfer_delayed", "transfer_delayed"]


def test_a_missing_value_is_refused_like_every_other_template():
    with pytest.raises(MissingTemplateVariable):
        render("transfer_delayed", "en", name="Aisha", transfer_id="TRF-000007")


def test_the_existing_messages_are_untouched():
    sent = dict(
        name="Aisha",
        transfer_id="TRF-000001",
        recipient="Ravi Kumar",
        send_amount=Money("500.00", "QAR"),
        fee=Money("12.00", "QAR"),
        receive_amount=Money("11286.00", "INR"),
    )
    assert render("transfer_sent", "en", **sent) == (
        "Hi Aisha, your transfer TRF-000001 was sent. Ravi Kumar received 11,286.00 INR. "
        "You paid 500.00 QAR plus a fee of 12.00 QAR."
    )
    assert render("transfer_failed", "en", name="Aisha", recipient="Ravi Kumar", send_amount=Money("2500", "QAR"), reason="R.") == (
        "Hi Aisha, your transfer of 2,500.00 QAR to Ravi Kumar could not be completed. "
        "R. No money has been taken from your account."
    )
