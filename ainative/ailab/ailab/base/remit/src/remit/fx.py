"""Foreign exchange: turning QAR into the receive currency.

A *rate provider* gives the mid-market rate for a pair at a moment in time. Remit
then takes the corridor's margin off that rate (the customer rate is lower than
the mid rate) and rounds the customer rate to 4 decimal places, half up. The
receive amount is the send amount times the customer rate, rounded half up to the
receive currency's 2 decimal places.

A quote is valid for 60 seconds (QUOTE_TTL): it is usable while ``now`` is strictly
before ``expires_at`` and expired from ``expires_at`` onwards.

The rates and margins below are fictional. ``StaticRateProvider`` is the only
provider; it never touches the network.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal
from typing import Protocol

from remit.corridors import Corridor
from remit.errors import CurrencyMismatch, RateUnavailable
from remit.money import Money

QUOTE_TTL = timedelta(seconds=60)
RATE_PLACES = Decimal("0.0001")

# Fictional mid-market rates: how many units of the receive currency one QAR buys.
DEFAULT_MID_RATES: dict[str, Decimal] = {
    "QAR-INR": Decimal("22.80"),
    "QAR-PHP": Decimal("15.40"),
    "QAR-EGP": Decimal("13.20"),
    "QAR-PKR": Decimal("77.00"),
}

# Fictional margins taken off the mid rate, per corridor (0.0100 is 1.00%).
CORRIDOR_MARGINS: dict[str, Decimal] = {
    "QAR-INR": Decimal("0.0100"),
    "QAR-PHP": Decimal("0.0125"),
    "QAR-EGP": Decimal("0.0150"),
    "QAR-PKR": Decimal("0.0150"),
}


class RateProvider(Protocol):
    """Anything that can say what one unit of ``send_currency`` is worth at ``at``."""

    def get_rate(self, send_currency: str, receive_currency: str, at: datetime) -> Decimal: ...


class StaticRateProvider:
    """Fixed fictional rates (ignores ``at``). Pass your own mapping to override."""

    def __init__(self, rates: Mapping[str, Decimal] | None = None) -> None:
        self._rates: dict[str, Decimal] = dict(DEFAULT_MID_RATES if rates is None else rates)

    def get_rate(self, send_currency: str, receive_currency: str, at: datetime) -> Decimal:
        code = f"{send_currency}-{receive_currency}"
        try:
            return self._rates[code]
        except KeyError:
            raise RateUnavailable(f"no rate for {code}") from None


@dataclass(frozen=True)
class FxQuote:
    rate: Decimal  # the customer rate, 4 dp
    receive: Money  # what the recipient gets, in the receive currency
    expires_at: datetime  # aware, UTC

    def is_expired(self, now: datetime) -> bool:
        """True from ``expires_at`` onwards (the quote is valid while now < expires_at)."""
        return now >= self.expires_at


def margin_for(corridor: Corridor) -> Decimal:
    try:
        return CORRIDOR_MARGINS[corridor.code]
    except KeyError:
        raise RateUnavailable(f"no margin configured for {corridor.code}") from None


def customer_rate(mid_rate: Decimal, margin: Decimal) -> Decimal:
    """``mid_rate`` less ``margin``, rounded half up to 4 decimal places."""
    return (mid_rate * (1 - margin)).quantize(RATE_PLACES, rounding=ROUND_HALF_UP)


def fx_quote(send: Money, corridor: Corridor, provider: RateProvider, now: datetime) -> FxQuote:
    """Quote the receive amount for ``send`` (QAR) on ``corridor`` at time ``now``.

    ``now`` must be timezone-aware. The quote expires ``QUOTE_TTL`` after ``now``.
    """
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must be timezone-aware")
    if send.currency != corridor.send_currency:
        raise CurrencyMismatch(f"{corridor.code} sends {corridor.send_currency}, got {send.currency}")
    mid = provider.get_rate(corridor.send_currency, corridor.receive_currency, now)
    rate = customer_rate(mid, margin_for(corridor))
    receive = Money(send.amount * rate, corridor.receive_currency)
    return FxQuote(rate=rate, receive=receive, expires_at=now + QUOTE_TTL)
