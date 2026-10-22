"""Lab m14, hidden acceptance tests, part 1: the QAR-BDT corridor (code, minimum, maximum, delivery).

Imports happen inside the tests so that one broken module fails only the checks that need it.
"""
import pytest

from remit.money import Money


def qar(amount):
    return Money(amount, "QAR")


def test_the_corridor_exists_and_corridors_are_listed_in_code_order():
    from remit.corridors import all_corridors, corridor_for_code, get_corridor

    corridor = get_corridor("QAR", "BDT")
    assert corridor is corridor_for_code("QAR-BDT")
    assert (corridor.send_currency, corridor.receive_currency, corridor.code) == ("QAR", "BDT", "QAR-BDT")
    assert [c.code for c in all_corridors()] == ["QAR-BDT", "QAR-EGP", "QAR-INR", "QAR-PHP", "QAR-PKR"]


def test_the_corridor_has_a_fee_schedule_of_its_own_called_std_c():
    from remit.corridors import get_corridor
    from remit.fees import SCHEDULES

    corridor = get_corridor("QAR", "BDT")
    assert corridor.fee_schedule == "STD-C"
    assert "STD-C" in SCHEDULES and {"STD-A", "STD-B"} <= set(SCHEDULES)


def test_the_minimum_and_the_maximum_per_transfer_are_the_agreed_amounts():
    from remit.corridors import get_corridor

    corridor = get_corridor("QAR", "BDT")
    assert corridor.min_send == qar("100.00")
    assert corridor.max_send == qar("12000.00")


@pytest.mark.parametrize("amount", ["100.00", "100.01", "5000.00", "11999.99", "12000.00"])
def test_amounts_from_the_minimum_to_the_maximum_inclusive_are_accepted(amount):
    from remit.corridors import get_corridor, validate_send

    assert validate_send(get_corridor("QAR", "BDT"), qar(amount)) == "bank_deposit"


@pytest.mark.parametrize("amount", ["0.01", "99.99", "12000.01", "12000.02", "50000.00"])
def test_one_cent_outside_the_minimum_or_the_maximum_is_refused(amount):
    from remit.corridors import get_corridor, validate_send
    from remit.errors import AmountOutOfRange

    with pytest.raises(AmountOutOfRange):
        validate_send(get_corridor("QAR", "BDT"), qar(amount))


def test_delivery_is_bank_deposit_by_default_and_wallet_is_allowed():
    from remit.corridors import get_corridor, validate_send

    corridor = get_corridor("QAR", "BDT")
    assert corridor.delivery_methods == ("bank_deposit", "wallet")
    assert corridor.default_delivery == "bank_deposit"
    assert validate_send(corridor, qar("500"), "wallet") == "wallet"
    assert validate_send(corridor, qar("12000.00"), "wallet") == "wallet"


def test_cash_pickup_is_not_offered_to_bangladesh():
    from remit.corridors import get_corridor, validate_send
    from remit.errors import UnsupportedDeliveryMethod

    with pytest.raises(UnsupportedDeliveryMethod):
        validate_send(get_corridor("QAR", "BDT"), qar("500"), "cash_pickup")


def test_the_corridor_takes_qar_only_and_only_one_way():
    from remit.corridors import get_corridor, validate_send
    from remit.errors import CurrencyMismatch, UnknownCorridor

    with pytest.raises(CurrencyMismatch):
        validate_send(get_corridor("QAR", "BDT"), Money("500", "BDT"))
    with pytest.raises(UnknownCorridor):
        get_corridor("BDT", "QAR")
    with pytest.raises(UnknownCorridor):
        get_corridor("INR", "BDT")


@pytest.mark.parametrize(
    "code, low, high, methods, schedule",
    [
        ("QAR-INR", "50.00", "25000.00", ("bank_deposit", "wallet"), "STD-A"),
        ("QAR-PHP", "50.00", "20000.00", ("bank_deposit", "cash_pickup", "wallet"), "STD-A"),
        ("QAR-EGP", "100.00", "15000.00", ("bank_deposit", "wallet"), "STD-B"),
        ("QAR-PKR", "100.00", "15000.00", ("bank_deposit", "cash_pickup"), "STD-B"),
    ],
)
def test_the_four_existing_corridors_are_exactly_as_they_were(code, low, high, methods, schedule):
    from remit.corridors import corridor_for_code

    corridor = corridor_for_code(code)
    assert (corridor.min_send, corridor.max_send) == (qar(low), qar(high))
    assert corridor.delivery_methods == methods
    assert corridor.fee_schedule == schedule
