"""Hidden acceptance tests for lab m00 (the learner never sees this file in their work directory).

They check *behaviour* through the public interface the ticket names: the rendered messages.
Because they only call ``remit.notify.render`` (and read the source tree), they accept any sound
fix: editing the template by hand, with an agent, or by another route. They do not care how the
fix was made, only that the customer-visible text is right and nothing else about it changed.
"""
from pathlib import Path

import remit
from remit.money import Money
from remit.notify import render

SENT = dict(
    name="Aisha",
    transfer_id="TRF-000001",
    recipient="Ravi Kumar",
    send_amount=Money("500.00", "QAR"),
    fee=Money("12.00", "QAR"),
    receive_amount=Money("11286.00", "INR"),
)
FAILED = dict(name="Aisha", recipient="Ravi Kumar", send_amount=Money("2500", "QAR"), reason="R.")


def test_english_transfer_sent_spells_received_correctly():
    text = render("transfer_sent", "en", **SENT)
    assert "received" in text
    assert "recieved" not in text


def test_english_transfer_sent_is_otherwise_unchanged():
    assert render("transfer_sent", "en", **SENT) == (
        "Hi Aisha, your transfer TRF-000001 was sent. "
        "Ravi Kumar received 11,286.00 INR. "
        "You paid 500.00 QAR plus a fee of 12.00 QAR."
    )


def test_arabic_transfer_sent_is_unchanged():
    assert render("transfer_sent", "ar", **SENT) == (
        "مرحباً Aisha، تم إرسال تحويلك TRF-000001. "
        "تم استلام مبلغ ١١٬٢٨٦٫٠٠ روبية هندية من قبل Ravi Kumar. "
        "المبلغ المرسل: ٥٠٠٫٠٠ ريال قطري، والرسوم: ١٢٫٠٠ ريال قطري."
    )


def test_transfer_failed_messages_are_unchanged():
    assert render("transfer_failed", "en", **FAILED) == (
        "Hi Aisha, your transfer of 2,500.00 QAR to Ravi Kumar could not be completed. "
        "R. No money has been taken from your account."
    )
    assert render("transfer_failed", "ar", **FAILED).startswith("مرحباً Aisha، تعذّر إتمام تحويلك بمبلغ ٢٬٥٠٠٫٠٠ ريال قطري")


def test_the_misspelling_is_gone_from_the_whole_source_tree():
    # Catches a "fix" that patches the output (for example with .replace) instead of the template.
    package = Path(remit.__file__).resolve().parent
    offenders = [p.name for p in package.rglob("*.py") if "recieve" in p.read_text(encoding="utf-8").lower()]
    assert offenders == []
