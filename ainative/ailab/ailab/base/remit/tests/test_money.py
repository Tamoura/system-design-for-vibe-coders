import copy
import pickle
from decimal import Decimal

import pytest

from remit.errors import CurrencyMismatch, InvalidAmount, UnknownCurrency
from remit.money import CURRENCIES, Money, quantize


def test_amount_is_stored_as_decimal_with_two_places():
    m = Money("500", "QAR")
    assert m.amount == Decimal("500.00")
    assert str(m.amount) == "500.00"
    assert m.currency == "QAR"


def test_rounds_half_up():
    cases = {"2.345": "2.35", "2.344": "2.34", "2.355": "2.36", "0.125": "0.13", "-2.345": "-2.35"}
    for raw, expected in cases.items():  # half-even would give 0.12 for 0.125; "half up" is away from zero
        assert Money(raw, "QAR").amount == Decimal(expected), raw
    assert quantize(Decimal("1.005")) == Decimal("1.01")  # the helper behind Money
    assert quantize(Decimal("1.5"), places=0) == Decimal("2")


def test_supported_currencies_have_two_decimals():
    assert set(CURRENCIES) == {"QAR", "INR", "PHP", "EGP", "PKR", "BDT"}
    for currency, places in CURRENCIES.items():
        assert places == 2
        assert Money(1, currency).amount == Decimal("1.00")


def test_unknown_currency_is_rejected():
    with pytest.raises(UnknownCurrency):
        Money(1, "USD")
    with pytest.raises(UnknownCurrency):
        Money(1, "qar")


def test_float_is_rejected_everywhere():
    with pytest.raises(TypeError):
        Money(1.5, "QAR")
    with pytest.raises(TypeError):
        Money("1", "QAR") + 1.5
    with pytest.raises(TypeError):
        Money("1", "QAR") * 1.5
    with pytest.raises(TypeError):
        Money("1", "QAR") / 2.0
    with pytest.raises(TypeError):
        Money("1", "QAR") < 2.0


def test_bool_and_garbage_are_rejected():
    for bad in (True, None):
        with pytest.raises(TypeError):
            Money(bad, "QAR")
    for bad in ("twelve", "NaN", Decimal("Infinity")):
        with pytest.raises(InvalidAmount):
            Money(bad, "QAR")


def test_addition_and_subtraction_keep_the_currency():
    assert Money("10.10", "QAR") + Money("0.05", "QAR") == Money("10.15", "QAR")
    assert Money("10.10", "QAR") - Money("10.20", "QAR") == Money("-0.10", "QAR")


def test_mixing_currencies_raises():
    with pytest.raises(CurrencyMismatch):
        Money(1, "QAR") + Money(1, "INR")
    with pytest.raises(CurrencyMismatch):
        Money(1, "QAR") < Money(1, "INR")


def test_multiplication_rounds_half_up():
    assert Money("100.25", "QAR") * Decimal("0.02") == Money("2.01", "QAR")  # 2.005
    assert Decimal("3") * Money("1.10", "QAR") == Money("3.30", "QAR")
    with pytest.raises(TypeError):
        Money(1, "QAR") * Money(1, "QAR")


def test_division():
    assert Money("10.00", "QAR") / 3 == Money("3.33", "QAR")
    assert Money("10.00", "QAR") / Money("4.00", "QAR") == Decimal("2.5")
    with pytest.raises(ZeroDivisionError):
        Money("10.00", "QAR") / 0


def test_comparison_and_equality():
    assert Money("1.00", "QAR") < Money("1.01", "QAR")
    assert Money("2.00", "QAR") >= Money("2.00", "QAR")
    assert Money("1", "QAR") == Money("1.00", "QAR")
    assert Money("1", "QAR") != Money("1", "INR")  # equal numbers, different currency
    assert max(Money("1", "QAR"), Money("3", "QAR"), Money("2", "QAR")) == Money("3", "QAR")
    assert {Money("1", "QAR"): "a"}[Money("1.00", "QAR")] == "a"  # hashable


def test_zero_negative_abs_bool():
    assert not Money.zero("QAR")
    assert Money("0.01", "QAR")
    assert (-Money("5", "QAR")).is_negative()
    assert abs(Money("-5", "QAR")) == Money("5", "QAR")
    assert str(Money("-0.001", "QAR")) == "0.00 QAR"  # no negative zero


def test_sum_needs_a_start_value_and_text_forms():
    items = [Money("1.10", "QAR"), Money("2.20", "QAR")]
    assert sum(items, Money.zero("QAR")) == Money("3.30", "QAR")
    assert str(Money("1234.5", "QAR")) == "1234.50 QAR"
    assert repr(Money("1234.5", "QAR")) == "Money('1234.50', 'QAR')"


def test_money_is_immutable_and_copyable():
    m = Money(1, "QAR")
    with pytest.raises(AttributeError):
        m.amount = Decimal(2)  # type: ignore[misc]
    with pytest.raises(AttributeError):
        m._amount = Decimal(2)
    assert copy.deepcopy(m) == m
    assert pickle.loads(pickle.dumps(m)) == m
