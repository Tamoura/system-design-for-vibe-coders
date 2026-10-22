"""Corridors: the send-currency to receive-currency routes Remit supports.

A corridor says what may be sent (minimum and maximum per transfer, in the send
currency), how it can be delivered, and which fee schedule (see fees.py) prices it.
All corridors start in QAR, because customers send from Qatar.

Adding a corridor means adding one entry to ``_DEFINITIONS`` *and* making sure its
fee schedule (fees.SCHEDULES), exchange rate and margin (fx.py) exist. All the
numbers are fictional.
"""
from __future__ import annotations

from dataclasses import dataclass

from remit.errors import AmountOutOfRange, CurrencyMismatch, UnknownCorridor, UnsupportedDeliveryMethod
from remit.money import Money

DELIVERY_METHODS = ("bank_deposit", "cash_pickup", "wallet")


@dataclass(frozen=True)
class Corridor:
    send_currency: str
    receive_currency: str
    min_send: Money
    max_send: Money
    delivery_methods: tuple[str, ...]
    fee_schedule: str  # a key of fees.SCHEDULES

    @property
    def code(self) -> str:
        """``"QAR-INR"``: the key used everywhere (rates, margins, logs)."""
        return f"{self.send_currency}-{self.receive_currency}"

    @property
    def default_delivery(self) -> str:
        return self.delivery_methods[0]


def _qar(amount: str) -> Money:
    return Money(amount, "QAR")


_DEFINITIONS: tuple[Corridor, ...] = (
    Corridor("QAR", "INR", _qar("50.00"), _qar("25000.00"), ("bank_deposit", "wallet"), "STD-A"),
    Corridor("QAR", "PHP", _qar("50.00"), _qar("20000.00"), ("bank_deposit", "cash_pickup", "wallet"), "STD-A"),
    Corridor("QAR", "EGP", _qar("100.00"), _qar("15000.00"), ("bank_deposit", "wallet"), "STD-B"),
    Corridor("QAR", "PKR", _qar("100.00"), _qar("15000.00"), ("bank_deposit", "cash_pickup"), "STD-B"),
)

CORRIDORS: dict[str, Corridor] = {c.code: c for c in _DEFINITIONS}


def get_corridor(send_currency: str, receive_currency: str) -> Corridor:
    """Look up a corridor by currencies. Raises UnknownCorridor when unsupported."""
    code = f"{send_currency}-{receive_currency}"
    try:
        return CORRIDORS[code]
    except KeyError:
        raise UnknownCorridor(f"no corridor {send_currency} -> {receive_currency}") from None


def corridor_for_code(code: str) -> Corridor:
    """Look up a corridor by its code, e.g. ``"QAR-INR"``."""
    try:
        return CORRIDORS[code]
    except KeyError:
        raise UnknownCorridor(f"no corridor {code}") from None


def all_corridors() -> list[Corridor]:
    """All corridors, sorted by code."""
    return [CORRIDORS[code] for code in sorted(CORRIDORS)]


def validate_send(corridor: Corridor, amount: Money, delivery_method: str | None = None) -> str:
    """Check an amount and delivery method against a corridor; return the method to use.

    The amount must be in the corridor's send currency and between ``min_send`` and
    ``max_send`` *inclusive*. ``delivery_method=None`` selects the corridor's default.
    """
    if amount.currency != corridor.send_currency:
        raise CurrencyMismatch(f"{corridor.code} takes {corridor.send_currency}, got {amount.currency}")
    if amount < corridor.min_send or amount > corridor.max_send:
        raise AmountOutOfRange(
            f"{corridor.code}: amount must be between {corridor.min_send} and {corridor.max_send}"
        )
    method = delivery_method or corridor.default_delivery
    if method not in corridor.delivery_methods:
        raise UnsupportedDeliveryMethod(f"{corridor.code} does not support {method!r}")
    return method
