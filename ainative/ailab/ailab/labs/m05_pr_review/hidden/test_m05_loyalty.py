"""Hidden acceptance tests for lab m05 (REMIT-231, the loyalty discount).

They are written from the ticket and go through the public interface only: ``quote_fee``,
``explain_fee``, ``RemitService.quote`` and ``RemitService.send``. They never import the
agent's helper names, so any sound implementation passes.

The expected values come from a small Decimal reference written straight from the ticket:
discount = base fee x rate, rounded half up to 2 dp; the customer pays base - discount, but
never less than the schedule minimum; the express surcharge is added afterwards.
"""
from decimal import ROUND_HALF_UP, Decimal

import pytest

from remit import ledger
from remit.corridors import get_corridor
from remit.errors import UnknownCustomer
from remit.fees import explain_fee, get_schedule, quote_fee
from remit.money import Money

INR = get_corridor("QAR", "INR")  # STD-A: minimum 5.00, cap 150.00, express 15.00
PKR = get_corridor("QAR", "PKR")  # STD-B: minimum 6.00, cap 120.00, express 20.00
RATES = {"none": Decimal("0"), "silver": Decimal("0.10"), "gold": Decimal("0.20")}


def qar(value):
    return Money(value, "QAR")


def reference_fee(amount, corridor, tier, express=False):
    """The ticket, as arithmetic on Decimals."""
    schedule = get_schedule(corridor.fee_schedule)
    base = explain_fee(amount, corridor).base.amount  # the undiscounted base fee (after minimum and cap)
    discount = (base * RATES[tier]).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    discounted = max(base - discount, schedule.minimum)
    return discounted + (schedule.express_surcharge if express else Decimal("0"))


# -- the ticket's own examples --------------------------------------------------------------------
@pytest.mark.parametrize(
    "amount, express, silver, gold",
    [
        ("100.00", False, "5.00", "5.00"),
        ("670.00", False, "13.54", "12.04"),
        ("1000.00", False, "18.00", "16.00"),
        ("1000.00", True, "33.00", "31.00"),
    ],
)
def test_the_examples_in_the_ticket(amount, express, silver, gold):
    assert quote_fee(qar(amount), INR, express=express, loyalty_tier="silver") == qar(silver)
    assert quote_fee(qar(amount), INR, express=express, loyalty_tier="gold") == qar(gold)


def test_a_customer_without_a_tier_pays_what_they_paid_before():
    for amount in ("100.00", "670.00", "1000.00", "20000.00"):
        assert quote_fee(qar(amount), INR) == quote_fee(qar(amount), INR, loyalty_tier="none")
    assert quote_fee(qar("1000.00"), INR, loyalty_tier="none") == qar("20.00")


# -- rounding and the minimum ---------------------------------------------------------------------
def test_the_silver_discount_rounds_half_up_to_the_cent():
    # QAR 192.50 -> base fee 5.85; the discount is 0.585, which rounds UP to 0.59: the customer pays 5.26
    assert quote_fee(qar("192.50"), INR, loyalty_tier="silver") == qar("5.26")


def test_the_discount_never_takes_the_fee_below_the_schedule_minimum():
    assert quote_fee(qar("192.50"), INR, loyalty_tier="gold") == qar("5.00")  # 5.85 less 1.17 would be 4.68
    assert quote_fee(qar("100.00"), PKR, loyalty_tier="gold") == qar("6.00")  # STD-B minimum


def test_every_amount_matches_the_decimal_reference():
    """A sweep like the repository's own monotonic-fee test: both schedules, both tiers, express or not."""
    checked = 0
    for corridor in (INR, PKR):
        for cents in range(5000, 2_600_000, 797):
            amount = Money(Decimal(cents) / 100, "QAR")
            for tier in ("silver", "gold"):
                for express in (False, True):
                    got = quote_fee(amount, corridor, express=express, loyalty_tier=tier)
                    assert got.amount == reference_fee(amount, corridor, tier, express), (corridor.code, amount, tier, express)
                    checked += 1
    assert checked > 5000


def test_silver_ties_are_rounded_half_up_everywhere():
    """Base fees that end in 5 cents are exactly the ones where a float gets the cent wrong."""
    ties = []
    for cents in range(5000, 200_000, 7):
        amount = Money(Decimal(cents) / 100, "QAR")
        base = explain_fee(amount, INR).base.amount
        if base * 100 % 10 == 5:
            ties.append(amount)
    assert len(ties) > 100
    for amount in ties:
        assert quote_fee(amount, INR, loyalty_tier="silver").amount == reference_fee(amount, INR, "silver"), amount


# -- the express surcharge and the cap (the discount must not change either) -------------------------
def test_the_express_surcharge_is_never_discounted():
    for tier in ("none", "silver", "gold"):
        plain = quote_fee(qar("1000.00"), INR, loyalty_tier=tier)
        rushed = quote_fee(qar("1000.00"), INR, express=True, loyalty_tier=tier)
        assert rushed == plain + qar("15.00"), tier


def test_the_express_surcharge_is_still_added_after_the_cap():
    # nothing in REMIT-231 changes how the cap works
    assert quote_fee(qar("20000.00"), INR, express=True) == qar("165.00")
    assert quote_fee(qar("20000.00"), INR, express=True, loyalty_tier="none") == qar("165.00")
    assert quote_fee(qar("15000.00"), PKR, express=True) == qar("140.00")
    capped = explain_fee(qar("20000.00"), INR, express=True)
    assert capped.total == capped.base + capped.surcharge


def test_the_discount_comes_off_the_capped_base_fee():
    assert quote_fee(qar("20000.00"), INR, loyalty_tier="gold") == qar("120.00")  # 150.00 less 30.00
    assert quote_fee(qar("20000.00"), INR, express=True, loyalty_tier="gold") == qar("135.00")


# -- bad input --------------------------------------------------------------------------------------
@pytest.mark.parametrize("tier", ["platinum", "Gold", "GOLD", "", "bronze"])
def test_an_unknown_tier_is_an_error_not_a_quiet_full_price(tier):
    with pytest.raises(ValueError):
        quote_fee(qar("1000.00"), INR, loyalty_tier=tier)
    with pytest.raises(ValueError):
        explain_fee(qar("1000.00"), INR, express=True, loyalty_tier=tier)


def test_fees_are_money_and_money_stays_strict():
    assert isinstance(quote_fee(qar("670.00"), INR, loyalty_tier="silver"), Money)
    with pytest.raises(TypeError):
        Money(13.54, "QAR")


# -- the service ------------------------------------------------------------------------------------
def test_send_charges_each_customer_their_own_tier(service, store):
    standard = service.send("C001", qar("1000"), "INR", "Ravi Kumar")  # Aisha: none
    silver = service.send("C002", qar("1000"), "INR", "Ravi Kumar")  # Bilal: silver
    gold = service.send("C003", qar("1000"), "PHP", "Maria Santos")  # Mariam: gold
    assert standard.transfer.fee == qar("20.00") and standard.total_debited == qar("1020.00")
    assert silver.transfer.fee == qar("18.00") and silver.total_debited == qar("1018.00")
    assert gold.transfer.fee == qar("16.00") and gold.total_debited == qar("1016.00")
    assert store.get_transfer(silver.transfer.id).fee == qar("18.00")


def test_an_express_send_adds_the_surcharge_after_the_discount(service):
    result = service.send("C003", qar("1000"), "INR", "Ravi Kumar", express=True)
    assert result.transfer.fee == qar("31.00")


def test_the_discounted_fee_reaches_the_ledger_and_the_customer(service, notifier):
    result = service.send("C002", qar("1000"), "INR", "Ravi Kumar")
    assert ledger.balance(ledger.customer_account("C002")) == Decimal("-1018.00")
    (note,) = notifier.sent
    assert "a fee of 18.00 QAR" in note.text
    assert result.notified


def test_a_quote_for_a_customer_uses_their_tier(service):
    assert service.quote(qar("1000"), "INR", customer_id="C002").fee == qar("18.00")
    assert service.quote(qar("1000"), "INR", customer_id="C003", express=True).fee == qar("31.00")
    assert service.quote(qar("1000"), "INR", customer_id="C001").total == qar("1020.00")
    assert service.quote(qar("1000"), "INR").fee == qar("20.00")  # no customer: the standard fee


def test_a_quote_for_an_unknown_customer_is_refused(service):
    with pytest.raises(UnknownCustomer):
        service.quote(qar("1000"), "INR", customer_id="C999")
