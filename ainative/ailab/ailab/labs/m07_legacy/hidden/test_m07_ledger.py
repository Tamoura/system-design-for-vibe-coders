"""Hidden characterization suite for lab m07: the Ledger class must behave exactly like the legacy
module did (Q-LED-1 to Q-LED-4 and the details around them), with its state on the instance."""
import inspect
from decimal import Decimal

import pytest

from remit.errors import CurrencyMismatch, DuplicatePosting, InvalidAmount
from remit.money import Money


def qar(value):
    return Money(value, "QAR")


def post(ledger, transfer_id="TRF-1", customer="C001", send="500.00", fee="12.00"):
    return ledger.post_transfer(transfer_id, customer, qar(send), qar(fee))


def shape(entries):
    return [(e["account"], e["side"], e["amount"]) for e in entries]


# -- the interface the ticket fixes -----------------------------------------------------------
def test_a_ledger_is_created_with_no_arguments_and_starts_empty(hx_new_ledger):
    ledger = hx_new_ledger()
    assert ledger.accounts() == [] and ledger.journal() == []


def test_the_four_methods_take_the_documented_positional_arguments(hx_new_ledger):
    from remit.ledger import Ledger

    ledger = hx_new_ledger()
    assert list(inspect.signature(Ledger.post_transfer).parameters)[1:5] == ["transfer_id", "customer_id", "send_amount", "fee"]
    assert ledger.post_transfer("TRF-1", "C001", qar("100"), qar("5")) and ledger.balance("PAYOUT_CLEARING") == Decimal("100")


# -- what a posting looks like -----------------------------------------------------------------
def test_a_posting_is_a_debit_then_three_credits_in_a_fixed_order(hx_new_ledger):
    entries = post(hx_new_ledger())
    assert shape(entries) == [
        ("CUSTOMER:C001", "D", Decimal("512.00")),
        ("PAYOUT_CLEARING", "C", Decimal("500.00")),
        ("FEE_INCOME", "C", Decimal("8.40")),
        ("PARTNER_PAYABLE", "C", Decimal("3.60")),
    ]


def test_entries_have_exactly_the_documented_fields(hx_new_ledger):
    entries = post(hx_new_ledger())
    for entry in entries:
        assert set(entry) == {"entry_id", "transfer_id", "account", "side", "amount", "posted_at"}
        assert entry["transfer_id"] == "TRF-1" and isinstance(entry["amount"], Decimal)
        assert entry["posted_at"] == "2026-03-02T09:00:00+00:00"
    assert [e["entry_id"] for e in entries] == ["JNL-000001", "JNL-000002", "JNL-000003", "JNL-000004"]


def test_the_journal_lists_what_was_posted_in_order(hx_new_ledger):
    ledger = hx_new_ledger()
    first = post(ledger, "TRF-1")
    second = post(ledger, "TRF-2", "C002", "100.00", "5.00")
    assert ledger.journal() == first + second


def test_balances_are_credits_minus_debits(hx_new_ledger):
    ledger = hx_new_ledger()
    post(ledger)
    assert ledger.balance("CUSTOMER:C001") == Decimal("-512.00")
    assert ledger.balance("PAYOUT_CLEARING") == Decimal("500.00")
    assert ledger.balance("FEE_INCOME") + ledger.balance("PARTNER_PAYABLE") == Decimal("12.00")
    assert isinstance(ledger.balance("PAYOUT_CLEARING"), Decimal)


# -- Q-LED-1 -----------------------------------------------------------------------------------
@pytest.mark.parametrize(
    ("fee", "partner"),
    [("12.00", "3.60"), ("10.15", "3.04"), ("5.15", "1.54"), ("0.15", "0.04"), ("10.35", "3.10"), ("10.25", "3.08"), ("0.25", "0.08"), ("33.33", "10.00")],
    ids=[f"fee-{n}" for n in range(1, 9)],
)
def test_the_partner_share_is_rounded_half_even_and_income_is_the_remainder(hx_new_ledger, fee, partner):
    ledger = hx_new_ledger()
    post(ledger, fee=fee)
    assert ledger.balance("PARTNER_PAYABLE") == Decimal(partner)
    assert ledger.balance("FEE_INCOME") == Decimal(fee) - Decimal(partner)


def test_a_tiny_fee_has_no_partner_leg_and_a_zero_fee_has_no_fee_legs(hx_new_ledger):
    tiny = post(hx_new_ledger(), fee="0.01")
    assert [e["account"] for e in tiny] == ["CUSTOMER:C001", "PAYOUT_CLEARING", "FEE_INCOME"]
    ledger = hx_new_ledger()
    zero = post(ledger, fee="0.00")
    assert shape(zero) == [("CUSTOMER:C001", "D", Decimal("500.00")), ("PAYOUT_CLEARING", "C", Decimal("500.00"))]
    assert ledger.accounts() == ["CUSTOMER:C001", "PAYOUT_CLEARING"]


# -- Q-LED-4 and the checks before posting -------------------------------------------------------
@pytest.mark.parametrize(
    ("send", "fee"),
    [(Money("5", "EGP"), qar("1")), (qar("5"), Money("1", "EGP")), (Money("0", "EGP"), Money("0", "EGP"))],
    ids=["send", "fee", "both"],
)
def test_only_qar_is_accepted(hx_new_ledger, send, fee):
    ledger = hx_new_ledger()
    with pytest.raises(CurrencyMismatch):
        ledger.post_transfer("TRF-1", "C001", send, fee)
    assert ledger.journal() == [] and ledger.accounts() == []


@pytest.mark.parametrize(("send", "fee"), [("0.00", "1.00"), ("-5.00", "1.00"), ("5.00", "-0.01")], ids=["zero", "negative", "fee"])
def test_amounts_that_make_no_sense_are_refused(hx_new_ledger, send, fee):
    ledger = hx_new_ledger()
    with pytest.raises(InvalidAmount):
        post(ledger, send=send, fee=fee)
    assert ledger.journal() == []


def test_checks_run_in_a_fixed_order_currency_then_amount_then_duplicate(hx_new_ledger):
    ledger = hx_new_ledger()
    post(ledger, "TRF-1")
    with pytest.raises(CurrencyMismatch):
        ledger.post_transfer("TRF-1", "C001", Money("0", "EGP"), qar("1"))
    with pytest.raises(InvalidAmount):
        post(ledger, "TRF-1", send="0.00")
    with pytest.raises(DuplicatePosting):
        post(ledger, "TRF-1")


def test_a_refused_posting_changes_nothing_and_uses_no_ids(hx_new_ledger):
    ledger = hx_new_ledger()
    post(ledger, "TRF-1")
    snapshot = (ledger.journal(), ledger.accounts(), ledger.balance("PAYOUT_CLEARING"))
    for bad in (lambda: post(ledger, "TRF-1"), lambda: post(ledger, "TRF-2", send="0.00")):
        with pytest.raises((DuplicatePosting, InvalidAmount)):
            bad()
    assert (ledger.journal(), ledger.accounts(), ledger.balance("PAYOUT_CLEARING")) == snapshot
    assert post(ledger, "TRF-3")[0]["entry_id"] == "JNL-000005"


def test_the_same_transfer_id_is_refused_even_for_another_customer(hx_new_ledger):
    ledger = hx_new_ledger()
    post(ledger, "TRF-1", "C001")
    with pytest.raises(DuplicatePosting):
        post(ledger, "TRF-1", "C002")


# -- Q-LED-2 and the readers ---------------------------------------------------------------------
def test_asking_for_an_unknown_account_creates_it_with_a_zero_balance(hx_new_ledger):
    ledger = hx_new_ledger()
    assert ledger.balance("NOPE") == Decimal("0") and isinstance(ledger.balance("NOPE"), Decimal)
    assert ledger.accounts() == ["NOPE"]


def test_asking_about_a_known_account_changes_nothing(hx_new_ledger):
    ledger = hx_new_ledger()
    post(ledger)
    before = (ledger.accounts(), ledger.journal())
    ledger.balance("PAYOUT_CLEARING")
    assert (ledger.accounts(), ledger.journal()) == before


def test_accounts_come_back_sorted_by_name(hx_new_ledger):
    ledger = hx_new_ledger()
    post(ledger)
    ledger.balance("AAA")
    assert ledger.accounts() == ["AAA", "CUSTOMER:C001", "FEE_INCOME", "PARTNER_PAYABLE", "PAYOUT_CLEARING"]


def test_the_journal_call_hands_out_a_copy_of_the_list(hx_new_ledger):
    ledger = hx_new_ledger()
    post(ledger)
    journal = ledger.journal()
    assert journal is not ledger.journal()
    journal.append({"junk": True})
    assert len(ledger.journal()) == 4


# -- Q-LED-3: ids and time come from najmkit; the books belong to the instance ----------------------
def test_entries_are_stamped_with_the_najmkit_clock_at_posting_time(hx_new_ledger, hx_clock):
    ledger = hx_new_ledger()
    post(ledger, "TRF-1")
    hx_clock.advance(minutes=90)
    later = post(ledger, "TRF-2")
    assert {e["posted_at"] for e in later} == {"2026-03-02T10:30:00+00:00"}
    assert {e["posted_at"] for e in ledger.journal()[:4]} == {"2026-03-02T09:00:00+00:00"}


def test_two_ledgers_keep_separate_books(hx_new_ledger):
    one, two = hx_new_ledger(), hx_new_ledger()
    post(one, "TRF-1")
    assert two.accounts() == [] and two.journal() == []
    post(two, "TRF-1")  # the same transfer id is fine in a different ledger
    assert one.balance("PAYOUT_CLEARING") == two.balance("PAYOUT_CLEARING") == Decimal("500.00")
    post(two, "TRF-2")
    assert one.balance("PAYOUT_CLEARING") == Decimal("500.00") and two.balance("PAYOUT_CLEARING") == Decimal("1000.00")


def test_entry_ids_still_come_from_one_process_wide_sequence(hx_new_ledger):
    one, two = hx_new_ledger(), hx_new_ledger()
    assert post(one, "TRF-1")[0]["entry_id"] == "JNL-000001"
    assert post(two, "TRF-2")[0]["entry_id"] == "JNL-000005"
    assert post(one, "TRF-3")[0]["entry_id"] == "JNL-000009"


def test_creating_a_ledger_does_not_use_up_ids(hx_new_ledger):
    for _ in range(3):
        hx_new_ledger()
    assert post(hx_new_ledger())[0]["entry_id"] == "JNL-000001"


# -- the module itself -----------------------------------------------------------------------------
def test_the_old_module_level_functions_are_gone():
    from remit import ledger as module

    for name in ("reset", "post_transfer", "balance", "accounts", "journal"):
        assert not hasattr(module, name), f"remit.ledger.{name} should not exist any more"


def test_the_constants_and_the_account_helper_stay_where_they_were():
    from remit import ledger as module

    assert module.ACCOUNT_PAYOUT == "PAYOUT_CLEARING" and module.ACCOUNT_FEE_INCOME == "FEE_INCOME"
    assert module.ACCOUNT_PARTNER == "PARTNER_PAYABLE" and module.PARTNER_SHARE == Decimal("0.30")
    assert module.customer_account("C9") == "CUSTOMER:C9"
