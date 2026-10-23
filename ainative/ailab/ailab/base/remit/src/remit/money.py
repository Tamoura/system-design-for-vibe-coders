"""Money: an immutable amount of a single currency, built on Decimal.

The rules of the house (see CONTRIBUTING.md):

* Money is always ``Decimal`` under the hood, never ``float``. Passing a float to
  ``Money`` (or doing arithmetic with one) raises ``TypeError`` on purpose.
* Every amount is rounded to the currency's decimal places with ROUND_HALF_UP the
  moment it is created, so a ``Money`` never carries hidden fractions.
* You cannot mix currencies: adding QAR to INR raises ``CurrencyMismatch``.
"""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Any

from remit.errors import CurrencyMismatch, InvalidAmount, UnknownCurrency

# Supported currencies and their number of decimal places (all two, today).
CURRENCIES: dict[str, int] = {
    "QAR": 2,
    "INR": 2,
    "PHP": 2,
    "EGP": 2,
    "PKR": 2,
    "BDT": 2,
}

ROUNDING = ROUND_HALF_UP


def quantize(value: Decimal, places: int = 2) -> Decimal:
    """Round ``value`` to ``places`` decimal places, half up (2.345 -> 2.35)."""
    return value.quantize(Decimal(1).scaleb(-places), rounding=ROUNDING)


def _to_decimal(value: Any) -> Decimal:
    if isinstance(value, (bool, float)):
        raise TypeError(f"money amounts must be Decimal, int or str, not {type(value).__name__}")
    if isinstance(value, Decimal):
        number = value
    elif isinstance(value, int):
        number = Decimal(value)
    elif isinstance(value, str):
        try:
            number = Decimal(value.strip())
        except InvalidOperation:
            raise InvalidAmount(f"not a number: {value!r}") from None
    else:
        raise TypeError(f"money amounts must be Decimal, int or str, not {type(value).__name__}")
    if not number.is_finite():
        raise InvalidAmount(f"amount must be a finite number, got {value!r}")
    return number


def _factor(value: Any) -> Decimal:
    """A multiplier or divisor: Decimal or int. Never float, never Money."""
    if isinstance(value, (bool, float)) or not isinstance(value, (Decimal, int)):
        raise TypeError(f"expected a Decimal or int factor, not {type(value).__name__}")
    return Decimal(value)


class Money:
    """An amount in one currency. Immutable, hashable, comparable within a currency."""

    __slots__ = ("_amount", "_currency")

    def __init__(self, amount: Decimal | int | str, currency: str) -> None:
        if not isinstance(currency, str) or currency not in CURRENCIES:
            raise UnknownCurrency(f"unsupported currency: {currency!r}")
        rounded = quantize(_to_decimal(amount), CURRENCIES[currency])
        if rounded.is_zero():
            rounded = abs(rounded)  # never carry a negative zero ("-0.00")
        object.__setattr__(self, "_amount", rounded)
        object.__setattr__(self, "_currency", currency)

    # -- construction and access -------------------------------------------
    @classmethod
    def zero(cls, currency: str) -> Money:
        return cls(0, currency)

    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def currency(self) -> str:
        return self._currency

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("Money is immutable")

    def __delattr__(self, name: str) -> None:
        raise AttributeError("Money is immutable")

    def __reduce__(self) -> tuple[Any, ...]:  # copy.deepcopy / pickle support
        return (Money, (self._amount, self._currency))

    # -- helpers -------------------------------------------------------------
    def _same_currency(self, other: Money) -> None:
        if other._currency != self._currency:
            raise CurrencyMismatch(f"cannot combine {self._currency} with {other._currency}")

    def _with(self, amount: Decimal) -> Money:
        return Money(amount, self._currency)

    # -- arithmetic ----------------------------------------------------------
    def __add__(self, other: object) -> Money:
        if not isinstance(other, Money):
            return NotImplemented
        self._same_currency(other)
        return self._with(self._amount + other._amount)

    def __sub__(self, other: object) -> Money:
        if not isinstance(other, Money):
            return NotImplemented
        self._same_currency(other)
        return self._with(self._amount - other._amount)

    def __mul__(self, factor: object) -> Money:
        if isinstance(factor, Money):
            return NotImplemented
        return self._with(self._amount * _factor(factor))

    __rmul__ = __mul__

    def __truediv__(self, other: object) -> Money | Decimal:
        """Money / number -> Money (rounded half up); Money / Money -> Decimal ratio."""
        if isinstance(other, Money):
            self._same_currency(other)
            return self._amount / other._amount
        return self._with(self._amount / _factor(other))

    def __neg__(self) -> Money:
        return self._with(-self._amount)

    def __abs__(self) -> Money:
        return self._with(abs(self._amount))

    def __bool__(self) -> bool:
        return self._amount != 0

    def is_negative(self) -> bool:
        return self._amount < 0

    # -- comparison ------------------------------------------------------------
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self._currency == other._currency and self._amount == other._amount

    def __hash__(self) -> int:
        return hash((self._amount, self._currency))

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        self._same_currency(other)
        return self._amount < other._amount

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        self._same_currency(other)
        return self._amount <= other._amount

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        self._same_currency(other)
        return self._amount > other._amount

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        self._same_currency(other)
        return self._amount >= other._amount

    # -- text --------------------------------------------------------------------
    def __str__(self) -> str:
        return f"{self._amount:f} {self._currency}"

    def __repr__(self) -> str:
        return f"Money('{self._amount:f}', '{self._currency}')"
