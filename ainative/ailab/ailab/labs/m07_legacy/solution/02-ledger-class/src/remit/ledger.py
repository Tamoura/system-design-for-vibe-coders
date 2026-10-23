"""LEGACY: Remit's double-entry ledger (a "shadow ledger" of Remit's own postings).

Every sent transfer is posted as one debit and two or three credits that add up:

    D  CUSTOMER:<id>       send_amount + fee
    C  PAYOUT_CLEARING     send_amount
    C  FEE_INCOME          fee - partner_share
    C  PARTNER_PAYABLE     partner_share          (30% of the fee, see Q-LED-1)

The customer's real balance lives in core banking, so a customer account here can go
negative: it only records what Remit has posted. A balance is credits minus debits.

STEP 1 OF 3 (refactoring): the books now live in the ``Ledger`` class. The module-level
functions below are thin wrappers around one shared default instance, so every caller
still works. They go away in step 3.

Known quirks (documented here, on purpose)
------------------------------------------
Q-LED-1  The partner's 30% share of the fee is rounded half-even (banker's rounding),
         while everything else in Remit rounds half-up. For a fee of 10.15 the partner
         share is 3.04 (half-up would give 3.05) and FEE_INCOME gets the remainder, 7.11.
Q-LED-2  ``balance(account)`` creates the account with a zero balance when it does not
         exist, so merely asking about an account makes ``accounts()`` list it.
Q-LED-3  All state (balances and the journal) is module-level and shared by everyone in
         the process. Entry ids and timestamps come from najmkit's global generator and
         global clock, not from anything passed in. ``reset()`` clears the state.
Q-LED-4  Balances are bare Decimals with no currency; everything is assumed to be QAR.
"""
from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal
from typing import Any

from najmkit import clock, ids
from remit.errors import CurrencyMismatch, DuplicatePosting, InvalidAmount
from remit.money import Money

ACCOUNT_PAYOUT = "PAYOUT_CLEARING"
ACCOUNT_FEE_INCOME = "FEE_INCOME"
ACCOUNT_PARTNER = "PARTNER_PAYABLE"
PARTNER_SHARE = Decimal("0.30")

_CENT = Decimal("0.01")


def customer_account(customer_id: str) -> str:
    return f"CUSTOMER:{customer_id}"


class Ledger:
    """One set of books: balances and a journal."""

    def __init__(self) -> None:
        self._balances: dict[str, Decimal] = {}  # account -> credits minus debits
        self._journal: list[dict[str, Any]] = []  # every posted entry, oldest first

    def _post(self, transfer_id: str, account: str, side: str, amount: Decimal) -> dict[str, Any]:
        entry = {
            "entry_id": ids.new_id("JNL"),
            "transfer_id": transfer_id,
            "account": account,
            "side": side,  # "D" or "C"
            "amount": amount,
            "posted_at": clock.now().isoformat(),
        }
        self._journal.append(entry)
        sign = 1 if side == "C" else -1
        self._balances[account] = self._balances.get(account, Decimal("0")) + sign * amount
        return entry

    def post_transfer(self, transfer_id: str, customer_id: str, send_amount: Money, fee: Money) -> list[dict[str, Any]]:
        """Post a sent transfer and return its entries (debit first, then credits).

        Raises DuplicatePosting if ``transfer_id`` was already posted to this ledger.
        Zero-amount legs are not posted.
        """
        if send_amount.currency != "QAR" or fee.currency != "QAR":
            raise CurrencyMismatch("the ledger posts QAR only")
        if send_amount <= Money.zero("QAR") or fee.is_negative():
            raise InvalidAmount("send amount must be positive and fee must not be negative")
        if any(e["transfer_id"] == transfer_id for e in self._journal):
            raise DuplicatePosting(f"transfer {transfer_id} is already posted")

        partner = (fee.amount * PARTNER_SHARE).quantize(_CENT, rounding=ROUND_HALF_EVEN)  # Q-LED-1
        income = fee.amount - partner

        entries = [self._post(transfer_id, customer_account(customer_id), "D", send_amount.amount + fee.amount)]
        entries.append(self._post(transfer_id, ACCOUNT_PAYOUT, "C", send_amount.amount))
        if income:
            entries.append(self._post(transfer_id, ACCOUNT_FEE_INCOME, "C", income))
        if partner:
            entries.append(self._post(transfer_id, ACCOUNT_PARTNER, "C", partner))
        return entries

    def balance(self, account: str) -> Decimal:
        """Credits minus debits for ``account`` (zero if it has never been used: Q-LED-2)."""
        if account not in self._balances:
            self._balances[account] = Decimal("0")
        return self._balances[account]

    def accounts(self) -> list[str]:
        """Names of all known accounts, sorted."""
        return sorted(self._balances)

    def journal(self) -> list[dict[str, Any]]:
        """A copy of the journal list (the entry dicts themselves are shared)."""
        return list(self._journal)


# -- the old module-level API: wrappers around one shared instance (removed in step 3) ------------
_DEFAULT = Ledger()


def post_transfer(transfer_id: str, customer_id: str, send_amount: Money, fee: Money) -> list[dict[str, Any]]:
    return _DEFAULT.post_transfer(transfer_id, customer_id, send_amount, fee)


def balance(account: str) -> Decimal:
    return _DEFAULT.balance(account)


def accounts() -> list[str]:
    return _DEFAULT.accounts()


def journal() -> list[dict[str, Any]]:
    return _DEFAULT.journal()


def reset() -> None:
    """Forget everything. Tests call this before and after each test."""
    global _DEFAULT
    _DEFAULT = Ledger()
