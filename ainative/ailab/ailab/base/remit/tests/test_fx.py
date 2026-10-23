from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from remit.corridors import get_corridor
from remit.errors import CurrencyMismatch, RateUnavailable
from remit.fx import QUOTE_TTL, StaticRateProvider, customer_rate, fx_quote
from remit.money import Money

NOW = datetime(2026, 3, 2, 9, 0, tzinfo=timezone.utc)
INR = get_corridor("QAR", "INR")
PHP = get_corridor("QAR", "PHP")


def test_customer_rate_takes_the_margin_off_the_mid_rate_and_rounds_half_up():
    assert customer_rate(Decimal("22.80"), Decimal("0.0100")) == Decimal("22.5720")
    assert customer_rate(Decimal("15.40"), Decimal("0.0125")) == Decimal("15.2075")
    assert customer_rate(Decimal("1.00005"), Decimal("0")) == Decimal("1.0001")  # 4 decimal places


def test_quote_applies_rate_and_returns_receive_money():
    quote = fx_quote(Money("500.00", "QAR"), INR, StaticRateProvider(), NOW)
    assert quote.rate == Decimal("22.5720")
    assert quote.receive == Money("11286.00", "INR")


def test_receive_amount_is_rounded_half_up_to_two_places():
    provider = StaticRateProvider({"QAR-INR": Decimal("20.10")})
    quote = fx_quote(Money("55.00", "QAR"), INR, provider, NOW)
    assert quote.rate == Decimal("19.8990")
    assert quote.receive == Money("1094.45", "INR")  # 55 * 19.8990 = 1094.4450 (half-even: 1094.44)


def test_each_corridor_uses_its_own_margin():
    provider = StaticRateProvider()
    assert fx_quote(Money("100", "QAR"), PHP, provider, NOW).rate == Decimal("15.2075")


def test_quote_is_valid_for_60_seconds():
    quote = fx_quote(Money("500", "QAR"), INR, StaticRateProvider(), NOW)
    assert QUOTE_TTL == timedelta(seconds=60)
    assert quote.expires_at == NOW + timedelta(seconds=60)
    assert not quote.is_expired(NOW)
    assert not quote.is_expired(NOW + timedelta(seconds=59, microseconds=999999))
    assert quote.is_expired(NOW + timedelta(seconds=60))
    assert quote.is_expired(NOW + timedelta(minutes=5))
    later = NOW + timedelta(hours=3)  # the time is an argument, not a global
    assert fx_quote(Money("500", "QAR"), INR, StaticRateProvider(), later).expires_at == later + QUOTE_TTL


def test_provider_without_a_rate_raises():
    with pytest.raises(RateUnavailable):
        fx_quote(Money("500", "QAR"), INR, StaticRateProvider({}), NOW)
    with pytest.raises(RateUnavailable):
        StaticRateProvider().get_rate("QAR", "USD", NOW)


def test_bad_inputs_are_rejected():
    with pytest.raises(CurrencyMismatch):  # the send amount must be in the corridor's send currency
        fx_quote(Money("500", "INR"), INR, StaticRateProvider(), NOW)
    with pytest.raises(ValueError):  # the time must be timezone-aware
        fx_quote(Money("500", "QAR"), INR, StaticRateProvider(), datetime(2026, 3, 2, 9, 0))


def test_a_custom_provider_only_needs_get_rate():
    class Fixed:
        def get_rate(self, send_currency, receive_currency, at):
            return Decimal("20")

    assert fx_quote(Money("10", "QAR"), INR, Fixed(), NOW).rate == Decimal("19.8000")
