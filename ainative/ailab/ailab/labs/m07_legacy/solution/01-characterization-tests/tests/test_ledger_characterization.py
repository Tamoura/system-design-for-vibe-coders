"""Characterization tests for the ledger: they pin what it does today, quirks included.

Nothing here says what the ledger *should* do. Each test was written by running the code,
reading the result and asking "do we depend on this?". Q-LED-1 .. Q-LED-4 are the quirks the
module docstring lists. The tests reach the ledger only through tests/ledger_port.py, so the
same file runs before and after the refactor.
"""
from decimal import Decimal

import pytest

from ledger_port import ledger_of, make_ledger
from remit.errors import CurrencyMismatch, DuplicatePosting, InvalidAmount, LimitExceeded, ScreeningHit, StoreError
from remit.money import Money

QAR = "QAR"


def qar(value):
    return Money(value, QAR)


def post(ledger, transfer_id="TRF-1", customer="C001", send="500.00", fee="12.00"):
    return ledger.post_transfer(transfer_id, customer, qar(send), qar(fee))


def amounts(entries):
    return [(e["account"], e["side"], e["amount"]) for e in entries]


# -- what a posting looks like ----------------------------------------------------------------
def test_a_transfer_is_one_debit_then_three_credits_in_this_order():
    entries = post(make_ledger())
    assert amounts(entries) == [
        ("CUSTOMER:C001", "D", Decimal("512.00")),
        ("PAYOUT_CLEARING", "C", Decimal("500.00")),
        ("FEE_INCOME", "C", Decimal("8.40")),
        ("PARTNER_PAYABLE", "C", Decimal("3.60")),
    ]


def test_every_entry_has_exactly_these_fields_with_ids_and_the_posting_time():
    entries = post(make_ledger())
    assert [e["entry_id"] for e in entries] == ["JNL-000001", "JNL-000002", "JNL-000003", "JNL-000004"]
    for entry in entries:
        assert set(entry) == {"entry_id", "transfer_id", "account", "side", "amount", "posted_at"}
        assert entry["transfer_id"] == "TRF-1"
        assert entry["posted_at"] == "2026-03-02T09:00:00+00:00"
        assert isinstance(entry["amount"], Decimal)


def test_the_posting_time_comes_from_the_najmkit_clock(clock):
    ledger = make_ledger()
    clock.advance(hours=2)
    entries = post(ledger)
    assert {e["posted_at"] for e in entries} == {"2026-03-02T11:00:00+00:00"}


def test_the_customer_account_is_named_after_the_customer():
    entries = post(make_ledger(), customer="C777")
    assert entries[0]["account"] == "CUSTOMER:C777"


def test_balances_are_credits_minus_debits_so_the_customer_goes_negative():
    ledger = make_ledger()
    post(ledger)
    assert ledger.balance("CUSTOMER:C001") == Decimal("-512.00")
    assert ledger.balance("PAYOUT_CLEARING") == Decimal("500.00")
    assert ledger.balance("FEE_INCOME") == Decimal("8.40")
    assert ledger.balance("PARTNER_PAYABLE") == Decimal("3.60")


def test_balances_add_up_across_transfers_and_the_books_always_net_to_zero():
    ledger = make_ledger()
    post(ledger, "TRF-1", "C001", "500.00", "12.00")
    post(ledger, "TRF-2", "C002", "1000.00", "20.00")
    assert ledger.balance("PAYOUT_CLEARING") == Decimal("1500.00")
    assert ledger.balance("CUSTOMER:C001") == Decimal("-512.00")
    assert sum(ledger.balance(a) for a in ledger.accounts()) == Decimal("0")


# -- Q-LED-1: the partner's share is rounded half-even -----------------------------------------
@pytest.mark.parametrize(
    ("fee", "partner", "income"),
    [
        ("12.00", "3.60", "8.40"),  # no tie: 3.60 exactly
        ("10.15", "3.04", "7.11"),  # 3.045 -> 3.04 (half-up would say 3.05)
        ("5.15", "1.54", "3.61"),  # 1.545 -> 1.54
        ("0.15", "0.04", "0.11"),  # 0.045 -> 0.04
        ("10.35", "3.10", "7.25"),  # 3.105 -> 3.10
        ("10.25", "3.08", "7.17"),  # 3.075 -> 3.08 (the tie rounds to the even neighbour, which is up)
        ("0.25", "0.08", "0.17"),  # 0.075 -> 0.08
    ],
)
def test_the_partner_share_is_thirty_percent_rounded_half_even(fee, partner, income):
    ledger = make_ledger()
    post(ledger, fee=fee)
    assert ledger.balance("PARTNER_PAYABLE") == Decimal(partner)
    assert ledger.balance("FEE_INCOME") == Decimal(income)


def test_fee_income_is_whatever_is_left_so_the_two_credits_add_up_to_the_fee():
    for fee in ("10.15", "5.15", "0.15", "12.00", "7.77"):
        ledger = make_ledger()
        post(ledger, fee=fee)
        assert ledger.balance("PARTNER_PAYABLE") + ledger.balance("FEE_INCOME") == Decimal(fee)


# -- Q-LED-4: zero legs are not posted, QAR only, bare decimals ---------------------------------
def test_a_fee_too_small_for_a_partner_share_posts_no_partner_leg():
    entries = post(make_ledger(), fee="0.01")  # 0.003 rounds to 0.00
    assert [e["account"] for e in entries] == ["CUSTOMER:C001", "PAYOUT_CLEARING", "FEE_INCOME"]
    assert entries[2]["amount"] == Decimal("0.01")


def test_a_zero_fee_posts_only_the_debit_and_the_payout_and_creates_no_fee_accounts():
    ledger = make_ledger()
    entries = post(ledger, fee="0.00")
    assert amounts(entries) == [
        ("CUSTOMER:C001", "D", Decimal("500.00")),
        ("PAYOUT_CLEARING", "C", Decimal("500.00")),
    ]
    assert ledger.accounts() == ["CUSTOMER:C001", "PAYOUT_CLEARING"]


@pytest.mark.parametrize(
    ("send", "fee"),
    [(Money("500", "EGP"), Money("12", "QAR")), (Money("500", "QAR"), Money("12", "EGP")), (Money("500", "EGP"), Money("12", "EGP"))],
    ids=["send in EGP", "fee in EGP", "both in EGP"],
)
def test_only_qar_is_accepted(send, fee):
    ledger = make_ledger()
    with pytest.raises(CurrencyMismatch):
        ledger.post_transfer("TRF-1", "C001", send, fee)
    assert ledger.journal() == []


@pytest.mark.parametrize(("send", "fee"), [("0.00", "1.00"), ("-5.00", "1.00"), ("5.00", "-0.01")])
def test_a_zero_or_negative_send_amount_and_a_negative_fee_are_refused(send, fee):
    ledger = make_ledger()
    with pytest.raises(InvalidAmount):
        post(ledger, send=send, fee=fee)
    assert ledger.journal() == []


def test_the_currency_check_comes_before_the_amount_check():
    with pytest.raises(CurrencyMismatch):
        make_ledger().post_transfer("TRF-1", "C001", Money("0", "EGP"), qar("1"))


# -- Q-LED-3: duplicates, ids, and what a failed posting leaves behind ----------------------------
def test_posting_the_same_transfer_twice_is_refused_and_changes_nothing():
    ledger = make_ledger()
    post(ledger)
    before = ledger.journal()
    with pytest.raises(DuplicatePosting):
        post(ledger, customer="C002", send="10.00", fee="1.00")  # a different customer does not matter
    assert ledger.journal() == before
    assert ledger.balance("PAYOUT_CLEARING") == Decimal("500.00")


def test_the_amount_check_comes_before_the_duplicate_check():
    ledger = make_ledger()
    post(ledger)
    with pytest.raises(InvalidAmount):
        post(ledger, send="-1.00")


def test_a_refused_posting_does_not_use_up_entry_ids():
    ledger = make_ledger()
    with pytest.raises(InvalidAmount):
        post(ledger, send="0.00")
    entries = post(ledger)
    assert entries[0]["entry_id"] == "JNL-000001"


def test_entry_ids_keep_counting_across_transfers():
    ledger = make_ledger()
    post(ledger, "TRF-1")
    entries = post(ledger, "TRF-2")
    assert [e["entry_id"] for e in entries] == ["JNL-000005", "JNL-000006", "JNL-000007", "JNL-000008"]


# -- Q-LED-2: reading an account creates it ------------------------------------------------------
def test_asking_for_an_unknown_account_returns_zero_and_creates_it():
    ledger = make_ledger()
    assert ledger.accounts() == []
    assert ledger.balance("NOPE") == Decimal("0")
    assert ledger.accounts() == ["NOPE"]


def test_asking_for_a_known_account_changes_nothing():
    ledger = make_ledger()
    post(ledger)
    before = ledger.accounts()
    ledger.balance("FEE_INCOME")
    assert ledger.accounts() == before


# -- the readers ---------------------------------------------------------------------------------
def test_accounts_are_listed_in_alphabetical_order_not_in_posting_order():
    ledger = make_ledger()
    post(ledger)
    assert ledger.accounts() == ["CUSTOMER:C001", "FEE_INCOME", "PARTNER_PAYABLE", "PAYOUT_CLEARING"]


def test_the_journal_is_a_copy_of_the_list_in_posting_order():
    ledger = make_ledger()
    entries = post(ledger)
    journal = ledger.journal()
    assert [e["entry_id"] for e in journal] == [e["entry_id"] for e in entries]
    journal.clear()
    assert len(ledger.journal()) == 4


# -- through the service: what send() does to the books ----------------------------------------------
def test_send_posts_the_transfer_to_the_ledger_with_the_fee_and_the_customer(service):
    service.send("C001", qar("500"), "INR", "Ravi Kumar")
    ledger = ledger_of(service)
    assert ledger.balance("CUSTOMER:C001") == Decimal("-512.00")
    assert ledger.balance("PAYOUT_CLEARING") == Decimal("500.00")
    assert ledger.balance("PARTNER_PAYABLE") == Decimal("3.60")


def test_send_numbers_the_transfer_first_and_then_its_journal_entries(service):
    service.send("C001", qar("500"), "INR", "Ravi Kumar")
    journal = ledger_of(service).journal()
    assert {e["transfer_id"] for e in journal} == {"TRF-000001"}
    assert [e["entry_id"] for e in journal] == ["JNL-000002", "JNL-000003", "JNL-000004", "JNL-000005"]


def test_an_express_transfer_posts_the_surcharge_as_part_of_the_fee(service):
    service.send("C001", qar("500"), "INR", "Ravi Kumar", express=True)  # fee 27.00
    ledger = ledger_of(service)
    assert ledger.balance("CUSTOMER:C001") == Decimal("-527.00")
    assert ledger.balance("PARTNER_PAYABLE") == Decimal("8.10")
    assert ledger.balance("FEE_INCOME") == Decimal("18.90")


def test_a_tie_in_a_real_fee_goes_to_the_even_cent(service):
    service.send("C001", qar("157.25"), "INR", "Ravi Kumar")  # fee 5.15, partner 1.545
    assert ledger_of(service).balance("PARTNER_PAYABLE") == Decimal("1.54")


def test_a_transfer_refused_for_the_limit_posts_nothing(service):
    service.send("C002", qar("1500"), "INR", "Ravi Kumar")  # Bilal is T1: 2,000 a day
    before = ledger_of(service).journal()
    with pytest.raises(LimitExceeded):
        service.send("C002", qar("600"), "INR", "Ravi Kumar")
    assert ledger_of(service).journal() == before


def test_a_transfer_held_by_screening_posts_nothing(service):
    with pytest.raises(ScreeningHit):
        service.send("C001", qar("500"), "INR", "Test Sanctioned Person")
    assert ledger_of(service).journal() == []


def test_if_the_store_fails_after_the_ledger_the_postings_stay(service, monkeypatch):
    def broken(transfer):
        raise StoreError("disk full")

    monkeypatch.setattr(service.store, "save_transfer", broken)
    with pytest.raises(StoreError):
        service.send("C001", qar("500"), "INR", "Ravi Kumar")
    assert len(ledger_of(service).journal()) == 4  # documented limitation D-SVC-1
