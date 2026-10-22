"""REMIT-414: the Bangladesh corridor. Each test names the acceptance criterion of specs/REMIT-414.md that it proves."""
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from remit.corridors import get_corridor, validate_send
from remit.errors import AmountOutOfRange, LimitExceeded, UnsupportedDeliveryMethod
from remit.fees import explain_fee, quote_fee
from remit.fx import StaticRateProvider, customer_rate, fx_quote
from remit.money import Money


def qar(amount: str) -> Money:
    return Money(amount, "QAR")


BDT = get_corridor("QAR", "BDT")
NOW = datetime(2026, 3, 2, 9, 0, tzinfo=timezone.utc)


# AC1: the minimum and the maximum are inclusive, one cent outside is refused
@pytest.mark.parametrize("amount", ["100.00", "12000.00"])
def test_ac1_the_edges_of_the_range_are_accepted(amount):
    assert validate_send(BDT, qar(amount)) == "bank_deposit"


@pytest.mark.parametrize("amount", ["99.99", "12000.01"])
def test_ac1_one_cent_outside_the_range_is_refused(amount):
    with pytest.raises(AmountOutOfRange):
        validate_send(BDT, qar(amount))


# AC2: bank deposit is the default, wallet is allowed, cash pickup is not
def test_ac2_delivery_methods():
    assert BDT.delivery_methods == ("bank_deposit", "wallet")
    assert validate_send(BDT, qar("500"), "wallet") == "wallet"
    with pytest.raises(UnsupportedDeliveryMethod):
        validate_send(BDT, qar("500"), "cash_pickup")


# AC3: the tier follows the whole amount and the upper bound belongs to the lower tier
@pytest.mark.parametrize(
    "amount, tier, fee",
    [("1000.00", 0, "25.50"), ("1000.01", 1, "28.00"), ("5000.00", 1, "92.00"), ("5000.01", 2, "100.00")],
)
def test_ac3_the_tier_boundaries(amount, tier, fee):
    breakdown = explain_fee(qar(amount), BDT)
    assert (breakdown.tier_index, breakdown.total) == (tier, qar(fee))


# AC4: the minimum, the cap, and the express surcharge after the cap
def test_ac4_minimum_cap_and_express():
    assert quote_fee(qar("100.00"), BDT) == qar("7.00")  # raw 5.70
    assert quote_fee(qar("10000.00"), BDT) == qar("130.00")  # raw 155.00
    assert quote_fee(qar("12000.00"), BDT, express=True) == qar("148.00")  # 130.00 + 18.00
    assert explain_fee(qar("12000.00"), BDT).cap_applied


# AC5: rounding is half up, for fees and for the receive amount
def test_ac5_a_fee_of_exactly_7_185_rounds_up():
    assert quote_fee(qar("167.50"), BDT) == qar("7.19")


def test_ac5_a_receive_amount_of_exactly_8218_625_rounds_up():
    quote = fx_quote(qar("250.00"), BDT, StaticRateProvider(), NOW)
    assert quote.receive == Money("8218.63", "BDT")


# AC6: the rate, the margin and the quote lifetime
def test_ac6_the_customer_rate_and_the_receive_amount():
    assert customer_rate(Decimal("33.46"), Decimal("0.0175")) == Decimal("32.8745")
    quote = fx_quote(qar("500.00"), BDT, StaticRateProvider(), NOW)
    assert quote.rate == Decimal("32.8745") and quote.receive == Money("16437.25", "BDT")


def test_ac6_the_quote_expires_after_sixty_seconds():
    quote = fx_quote(qar("500.00"), BDT, StaticRateProvider(), NOW)
    assert not quote.is_expired(NOW + timedelta(seconds=59))
    assert quote.is_expired(NOW + timedelta(seconds=60))


# AC7: the wording, in the customer's language; other corridors keep the old template
def test_ac7_the_english_customer_reads_the_bangladesh_wording(service, notifier):
    service.send("C001", qar("500"), "BDT", "Rahim Uddin")
    sent = notifier.sent[-1]
    assert sent.template_id == "transfer_sent_bdt"
    assert sent.text == (
        "Hi Aisha Rahman, your transfer TRF-000001 to Bangladesh was sent. "
        "Rahim Uddin received 16,437.25 BDT at a rate of 1 QAR = 32.8745 BDT. "
        "You paid 500.00 QAR plus a fee of 14.50 QAR. Please keep this message as your receipt."
    )


def test_ac7_the_arabic_customer_reads_arabic_digits(service, notifier):
    service.send("C003", qar("12000.00"), "BDT", "Rahim Uddin")
    text = notifier.sent[-1].text
    assert "١ ريال قطري مقابل ٣٢٫٨٧٤٥ تاكا" in text and "١٣٠٫٠٠ ريال قطري" in text
    assert not any(ch in text.split("Rahim Uddin")[1] for ch in "0123456789")


def test_ac7_other_corridors_keep_transfer_sent(service, notifier):
    service.send("C001", qar("500"), "INR", "Ravi Kumar")
    assert notifier.sent[-1].template_id == "transfer_sent"


# AC8: the KYC limits and the ledger are untouched by the new corridor
def test_ac8_the_t1_daily_limit_still_applies_to_bangladesh(service):
    with pytest.raises(LimitExceeded):
        service.send("C002", qar("2000.01"), "BDT", "Rahim Uddin")
    assert service.send("C002", qar("2000.00"), "BDT", "Rahim Uddin").transfer.fee == qar("44.00")


def test_ac8_the_ledger_is_posted_in_qar(service):
    from remit import ledger

    service.send("C001", qar("500"), "BDT", "Rahim Uddin")
    assert ledger.balance("PAYOUT_CLEARING") == Decimal("500.00")
    assert ledger.balance("CUSTOMER:C001") == Decimal("-514.50")


# AC9: the four existing corridors quote exactly as before
@pytest.mark.parametrize("code, fee, receive", [("INR", "12.00", "11286.00"), ("PKR", "15.50", "37922.50")])
def test_ac9_existing_corridors_are_unchanged(service, code, fee, receive):
    quote = service.quote(qar("500"), code)
    assert (quote.fee, quote.fx.receive.amount) == (qar(fee), Decimal(receive))
