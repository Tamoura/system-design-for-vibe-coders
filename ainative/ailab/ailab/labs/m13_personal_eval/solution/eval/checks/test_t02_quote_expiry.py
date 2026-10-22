"""T02: a quote is valid for 60 seconds and expired from the moment it is 60 seconds old."""
from datetime import datetime, timedelta, timezone

from remit.corridors import get_corridor
from remit.fx import QUOTE_TTL, StaticRateProvider, fx_quote
from remit.money import Money

NOW = datetime(2026, 3, 2, 9, 0, tzinfo=timezone.utc)


def a_quote():
    return fx_quote(Money("500.00", "QAR"), get_corridor("QAR", "INR"), StaticRateProvider(), NOW)


def test_a_quote_is_valid_until_its_last_instant():
    quote = a_quote()
    assert not quote.is_expired(NOW)
    assert not quote.is_expired(quote.expires_at - timedelta(microseconds=1))


def test_a_quote_is_expired_from_the_moment_it_is_sixty_seconds_old():
    quote = a_quote()
    assert QUOTE_TTL == timedelta(seconds=60)
    assert quote.is_expired(NOW + QUOTE_TTL)
    assert quote.is_expired(NOW + QUOTE_TTL + timedelta(seconds=1))
