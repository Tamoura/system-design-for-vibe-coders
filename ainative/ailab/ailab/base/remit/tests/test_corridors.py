import pytest

from remit.corridors import DELIVERY_METHODS, all_corridors, corridor_for_code, get_corridor, validate_send
from remit.errors import AmountOutOfRange, CurrencyMismatch, UnknownCorridor, UnsupportedDeliveryMethod
from remit.fees import SCHEDULES
from remit.money import Money


def test_the_supported_corridors_start_in_qar():
    codes = [c.code for c in all_corridors()]
    assert {"QAR-INR", "QAR-PHP", "QAR-EGP", "QAR-PKR"} <= set(codes)
    assert all(c.send_currency == "QAR" for c in all_corridors())
    assert codes == sorted(codes)


def test_every_corridor_points_at_a_real_fee_schedule_and_known_methods():
    for corridor in all_corridors():
        assert corridor.fee_schedule in SCHEDULES
        assert set(corridor.delivery_methods) <= set(DELIVERY_METHODS)
        assert corridor.min_send < corridor.max_send


def test_lookup_by_currencies_and_by_code_and_unsupported_pairs_raise():
    assert get_corridor("QAR", "INR") is corridor_for_code("QAR-INR")
    with pytest.raises(UnknownCorridor):
        get_corridor("INR", "QAR")  # we only send out of Qatar
    with pytest.raises(UnknownCorridor):
        get_corridor("QAR", "USD")
    with pytest.raises(UnknownCorridor):
        corridor_for_code("nope")


def test_min_and_max_are_inclusive():
    inr = get_corridor("QAR", "INR")
    assert validate_send(inr, inr.min_send) == "bank_deposit"
    assert validate_send(inr, inr.max_send) == "bank_deposit"
    with pytest.raises(AmountOutOfRange):
        validate_send(inr, Money("49.99", "QAR"))
    with pytest.raises(AmountOutOfRange):
        validate_send(inr, Money("25000.01", "QAR"))


def test_delivery_method_defaults_to_the_first_and_must_be_supported():
    pkr = get_corridor("QAR", "PKR")
    assert validate_send(pkr, Money("500", "QAR")) == pkr.default_delivery
    assert validate_send(pkr, Money("500", "QAR"), "cash_pickup") == "cash_pickup"
    with pytest.raises(UnsupportedDeliveryMethod):
        validate_send(pkr, Money("500", "QAR"), "wallet")


def test_amount_must_be_in_the_send_currency():
    with pytest.raises(CurrencyMismatch):
        validate_send(get_corridor("QAR", "INR"), Money("500", "INR"))
