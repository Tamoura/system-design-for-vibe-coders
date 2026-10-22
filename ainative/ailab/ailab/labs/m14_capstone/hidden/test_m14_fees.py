"""Lab m14, hidden acceptance tests, part 2: the STD-C fee schedule.

The tier is chosen by the whole amount with the upper bound included; the minimum and the cap apply; the express
surcharge is added after the cap; everything is Decimal, rounded half up.
"""
from decimal import Decimal

import pytest

from remit.money import Money


def qar(amount):
    return Money(amount, "QAR")


def corridor():
    from remit.corridors import get_corridor

    return get_corridor("QAR", "BDT")


@pytest.mark.parametrize(
    "amount, fee",
    [
        ("100.00", "7.00"),  # 5.70 raw: the minimum applies
        ("159.09", "7.00"),
        ("250.00", "9.00"),
        ("500.00", "14.50"),
        ("1000.00", "25.50"),  # the last amount of tier 0
        ("1000.01", "28.00"),  # the first amount of tier 1, priced on the whole amount
        ("2500.00", "52.00"),
        ("5000.00", "92.00"),  # the last amount of tier 1
        ("5000.01", "100.00"),  # the first amount of tier 2
        ("8000.00", "130.00"),
        ("10000.00", "130.00"),  # raw 155.00: the cap applies
        ("12000.00", "130.00"),
    ],
)
def test_the_standard_fee_for_these_amounts(amount, fee):
    from remit.fees import quote_fee

    assert quote_fee(qar(amount), corridor()) == qar(fee)


@pytest.mark.parametrize(
    "amount, fee",
    [("100.00", "25.00"), ("500.00", "32.50"), ("1000.01", "46.00"), ("12000.00", "148.00")],
)
def test_the_express_surcharge_is_added_after_the_cap(amount, fee):
    from remit.fees import quote_fee

    assert quote_fee(qar(amount), corridor(), express=True) == qar(fee)


def test_a_fee_that_is_exactly_half_a_cent_rounds_up_not_to_even():
    from remit.fees import explain_fee, quote_fee

    # 167.50 x 2.20% + 3.50 = 7.1850 exactly. Half up gives 7.19; round-half-even or a float would give 7.18.
    assert quote_fee(qar("167.50"), corridor()) == qar("7.19")
    assert explain_fee(qar("167.50"), corridor()).raw == qar("7.19")


def test_the_breakdown_names_the_tier_and_says_which_limit_applied():
    from remit.fees import explain_fee

    low = explain_fee(qar("100.00"), corridor())
    assert (low.schedule_id, low.tier_index, low.minimum_applied, low.cap_applied) == ("STD-C", 0, True, False)
    assert (low.raw, low.base, low.total) == (qar("5.70"), qar("7.00"), qar("7.00"))
    mid = explain_fee(qar("1000.01"), corridor())
    assert (mid.tier_index, mid.minimum_applied, mid.cap_applied) == (1, False, False)
    top = explain_fee(qar("12000.00"), corridor(), express=True)
    assert (top.tier_index, top.cap_applied, top.raw, top.base) == (2, True, qar("177.00"), qar("130.00"))
    assert (top.surcharge, top.total) == (qar("18.00"), qar("148.00"))


def test_the_schedule_object_carries_the_agreed_minimum_cap_and_surcharge():
    from remit.fees import get_schedule

    schedule = get_schedule("STD-C")
    assert (schedule.minimum, schedule.cap, schedule.express_surcharge) == (Decimal("7.00"), Decimal("130.00"), Decimal("18.00"))
    assert len(schedule.tiers) == 3
    assert [t.upto for t in schedule.tiers] == [Decimal("1000.00"), Decimal("5000.00"), None]
    assert [t.percent for t in schedule.tiers] == [Decimal("0.022"), Decimal("0.016"), Decimal("0.011")]
    assert [t.flat for t in schedule.tiers] == [Decimal("3.50"), Decimal("12.00"), Decimal("45.00")]


def test_a_larger_amount_never_costs_less_across_the_whole_range():
    from remit.fees import quote_fee

    c = corridor()
    previous = Decimal("0")
    amounts = [Decimal(n) / 100 for n in range(10000, 1200001, 997)]  # a sweep over the range
    amounts += [Decimal("1000.00") + Decimal(n) / 100 for n in range(-5, 6)]  # a cent either side of 1,000
    amounts += [Decimal("5000.00") + Decimal(n) / 100 for n in range(-5, 6)]  # and of 5,000
    amounts += [Decimal("7727.27") + Decimal(n) / 100 for n in range(-5, 6)]  # and where the cap takes over
    for amount in sorted(set(amounts)):
        fee = quote_fee(Money(amount, "QAR"), c).amount
        assert fee >= previous, f"the fee fell at {amount}"
        assert Decimal("7.00") <= fee <= Decimal("130.00")
        previous = fee


def test_fees_are_money_in_qar_never_a_float():
    from remit.fees import quote_fee

    fee = quote_fee(qar("500.00"), corridor())
    assert isinstance(fee, Money) and fee.currency == "QAR" and isinstance(fee.amount, Decimal)


@pytest.mark.parametrize(
    "code, amount, fee",
    [
        ("QAR-INR", "500.00", "12.00"),
        ("QAR-INR", "500.01", "12.50"),
        ("QAR-INR", "20000.00", "150.00"),
        ("QAR-PHP", "2000.01", "40.00"),
        ("QAR-EGP", "1000.00", "28.00"),
        ("QAR-PKR", "500.00", "15.50"),
        ("QAR-PKR", "100.00", "6.00"),
    ],
)
def test_the_other_corridors_are_priced_exactly_as_before(code, amount, fee):
    from remit.corridors import corridor_for_code
    from remit.fees import quote_fee

    assert quote_fee(qar(amount), corridor_for_code(code)) == qar(fee)


def test_the_existing_schedules_are_untouched():
    from remit.fees import get_schedule

    a, b = get_schedule("STD-A"), get_schedule("STD-B")
    assert (a.minimum, a.cap, a.express_surcharge) == (Decimal("5.00"), Decimal("150.00"), Decimal("15.00"))
    assert (b.minimum, b.cap, b.express_surcharge) == (Decimal("6.00"), Decimal("120.00"), Decimal("20.00"))
    assert len(a.tiers) == 4 and len(b.tiers) == 3
