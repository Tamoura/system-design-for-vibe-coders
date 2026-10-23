"""Lab m14, hidden acceptance tests, part 3: the BDT rate, the margin and the 60-second quote."""
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from remit.money import Money

NOW = datetime(2026, 3, 2, 9, 0, tzinfo=timezone.utc)


def qar(amount):
    return Money(amount, "QAR")


def corridor():
    from remit.corridors import get_corridor

    return get_corridor("QAR", "BDT")


def test_the_mid_rate_and_the_margin_are_the_agreed_numbers():
    from remit.fx import StaticRateProvider, margin_for

    assert StaticRateProvider().get_rate("QAR", "BDT", NOW) == Decimal("33.46")
    assert margin_for(corridor()) == Decimal("0.0175")


def test_the_customer_rate_rounds_half_up_to_four_places():
    from remit.fx import customer_rate

    # 33.46 x (1 - 0.0175) = 32.874450 exactly: half up gives 32.8745; half-even or a float would give 32.8744.
    assert customer_rate(Decimal("33.46"), Decimal("0.0175")) == Decimal("32.8745")


@pytest.mark.parametrize(
    "amount, receive",
    [
        ("100.00", "3287.45"),
        ("250.00", "8218.63"),  # 8218.625 exactly: half up
        ("500.00", "16437.25"),
        ("1000.01", "32874.83"),
        ("12000.00", "394494.00"),
    ],
)
def test_the_receive_amount_is_the_send_amount_times_the_customer_rate(amount, receive):
    from remit.fx import StaticRateProvider, fx_quote

    quote = fx_quote(qar(amount), corridor(), StaticRateProvider(), NOW)
    assert quote.rate == Decimal("32.8745")
    assert quote.receive == Money(receive, "BDT")
    assert quote.receive.currency == "BDT" and isinstance(quote.receive.amount, Decimal)


def test_the_quote_lives_for_sixty_seconds_like_every_other():
    from remit.fx import StaticRateProvider, fx_quote

    quote = fx_quote(qar("500"), corridor(), StaticRateProvider(), NOW)
    assert quote.expires_at == NOW + timedelta(seconds=60)
    assert not quote.is_expired(NOW + timedelta(seconds=59))
    assert quote.is_expired(NOW + timedelta(seconds=60))


def test_a_quote_needs_a_timezone_and_the_right_currency():
    from remit.errors import CurrencyMismatch
    from remit.fx import StaticRateProvider, fx_quote

    with pytest.raises(ValueError):
        fx_quote(qar("500"), corridor(), StaticRateProvider(), datetime(2026, 3, 2, 9, 0))
    with pytest.raises(CurrencyMismatch):
        fx_quote(Money("500", "INR"), corridor(), StaticRateProvider(), NOW)


@pytest.mark.parametrize(
    "code, rate, receive",
    [
        ("QAR-INR", "22.5720", "11286.00"),
        ("QAR-PHP", "15.2075", "7603.75"),
        ("QAR-EGP", "13.0020", "6501.00"),
        ("QAR-PKR", "75.8450", "37922.50"),
    ],
)
def test_the_other_corridors_quote_exactly_as_before(code, rate, receive):
    from remit.corridors import corridor_for_code
    from remit.fx import StaticRateProvider, fx_quote

    quote = fx_quote(qar("500.00"), corridor_for_code(code), StaticRateProvider(), NOW)
    assert quote.rate == Decimal(rate)
    assert quote.receive.amount == Decimal(receive)
