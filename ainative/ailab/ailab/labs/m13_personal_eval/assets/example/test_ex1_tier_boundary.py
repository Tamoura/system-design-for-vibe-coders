"""Check for example task EX1: is the fee tier chosen with an inclusive upper bound?

A check lives outside the repository the tool works in and is copied in only when the run is scored.
It tests the behaviour a customer sees, not the line a fix happens to change.
"""
from remit.corridors import get_corridor
from remit.fees import explain_fee, get_schedule, quote_fee
from remit.money import Money

INR = get_corridor("QAR", "INR")  # fee schedule STD-A: tiers end at 500, 2000 and 10000 QAR


def qar(value):
    return Money(value, "QAR")


def test_exactly_500_is_still_in_the_first_tier():
    assert explain_fee(qar("500.00"), INR).tier_index == 0
    assert quote_fee(qar("500.00"), INR) == qar("12.00")


def test_one_cent_over_moves_to_the_next_tier():
    assert explain_fee(qar("500.01"), INR).tier_index == 1


def test_every_upper_bound_belongs_to_its_own_tier():
    tiers = get_schedule(INR.fee_schedule).tiers
    for index, tier in enumerate(tiers[:-1]):
        assert explain_fee(Money(tier.upto, "QAR"), INR).tier_index == index
