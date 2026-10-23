from decimal import Decimal

import pytest

from remit.corridors import get_corridor
from remit.errors import CurrencyMismatch, InvalidAmount, UnknownFeeSchedule
from remit.fees import FeeSchedule, FeeTier, explain_fee, get_schedule, quote_fee
from remit.money import Money

INR = get_corridor("QAR", "INR")  # schedule STD-A
PKR = get_corridor("QAR", "PKR")  # schedule STD-B


def qar(value):
    return Money(value, "QAR")


def test_std_a_tiers():
    expected = {
        "200.00": "6.00",  # tier 1: 2% + 2.00
        "500.00": "12.00",  # the last riyal of tier 1
        "600.00": "14.00",  # tier 2: 1.5% + 5.00
        "2000.00": "35.00",
        "5000.00": "70.00",  # tier 3: 1% + 20.00
        "10000.00": "120.00",
        "12000.00": "140.00",  # tier 4: 0.75% + 50.00
    }
    for amount, fee in expected.items():
        assert quote_fee(qar(amount), INR) == qar(fee), amount


def test_the_tier_is_chosen_by_the_whole_amount_and_the_boundary_is_inclusive():
    assert explain_fee(qar("500.00"), INR).tier_index == 0
    assert explain_fee(qar("500.01"), INR).tier_index == 1
    assert explain_fee(qar("2000.00"), INR).tier_index == 1
    assert explain_fee(qar("2000.01"), INR).tier_index == 2
    assert explain_fee(qar("10000.00"), INR).tier_index == 2
    assert explain_fee(qar("10000.01"), INR).tier_index == 3


def test_a_higher_amount_never_costs_less():
    previous = Decimal(0)
    for cents in range(5000, 2_500_001, 997):
        fee = quote_fee(Money(Decimal(cents) / 100, "QAR"), INR).amount
        assert fee >= previous
        previous = fee


def test_minimum_fee_applies_to_small_amounts():
    breakdown = explain_fee(qar("50.00"), INR)  # 2% + 2.00 = 3.00
    assert breakdown.raw == qar("3.00")
    assert breakdown.minimum_applied and not breakdown.cap_applied
    assert breakdown.total == qar("5.00")
    assert not explain_fee(qar("150.00"), INR).minimum_applied  # 5.00 exactly is not "applied"


def test_cap_applies_to_large_amounts():
    breakdown = explain_fee(qar("20000.00"), INR)  # 0.75% + 50 = 200.00
    assert breakdown.raw == qar("200.00")
    assert breakdown.cap_applied
    assert breakdown.total == qar("150.00")


def test_express_surcharge_is_added_after_the_cap():
    assert quote_fee(qar("500.00"), INR, express=True) == qar("27.00")  # 12 + 15
    capped = explain_fee(qar("20000.00"), INR, express=True)
    assert capped.base == qar("150.00") and capped.surcharge == qar("15.00")
    assert capped.total == qar("165.00")  # above the 150 cap, by design


def test_the_fee_is_rounded_half_up_once():
    # 150.25 * 2% = 3.005; + 2.00 = 5.005 -> 5.01 (half-even would give 5.00)
    assert quote_fee(qar("150.25"), INR) == qar("5.01")


def test_std_b_schedule_for_egp_and_pkr():
    assert quote_fee(qar("500.00"), PKR) == qar("15.50")  # 2.5% + 3
    assert quote_fee(qar("100.00"), PKR) == qar("6.00")  # minimum 6.00
    assert quote_fee(qar("3000.00"), PKR) == qar("64.00")  # 1.8% + 10
    assert quote_fee(qar("15000.00"), PKR) == qar("120.00")  # capped
    assert quote_fee(qar("100.00"), PKR, express=True) == qar("26.00")


def test_corridors_share_a_schedule_where_the_registry_says_so():
    php = get_corridor("QAR", "PHP")
    assert quote_fee(qar("1000.00"), php) == quote_fee(qar("1000.00"), INR)
    fee = quote_fee(qar("500"), INR)
    assert isinstance(fee, Money) and fee.currency == "QAR"


def test_bad_inputs():
    with pytest.raises(CurrencyMismatch):
        quote_fee(Money("500", "INR"), INR)
    with pytest.raises(InvalidAmount):
        quote_fee(qar("0"), INR)
    with pytest.raises(InvalidAmount):
        quote_fee(qar("-5"), INR)


def test_schedule_lookup_and_validation():
    assert get_schedule("STD-A").express_surcharge == Decimal("15.00")
    with pytest.raises(UnknownFeeSchedule):
        get_schedule("NOPE")
    with pytest.raises(ValueError):  # tiers out of order
        FeeSchedule("X", (FeeTier(Decimal(10), Decimal("0.1"), Decimal(0)), FeeTier(Decimal(5), Decimal("0.1"), Decimal(0)),
                          FeeTier(None, Decimal("0.1"), Decimal(0))), Decimal(1), Decimal(9), Decimal(1))
