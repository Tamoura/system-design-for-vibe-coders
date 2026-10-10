"""Najm Transfers: the sample system under test for the testing course.

Everything here is fictional: the bank, the limits, the fees and the rules.
Some bugs can be switched on on purpose, so you can practise catching them:

    NAJM_BUGS="limit_off_by_one,float_fee" pytest

Known bug names: limit_off_by_one, float_fee, tz_cutoff, no_idempotency, bola.
"""
from __future__ import annotations

import os
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from decimal import ROUND_HALF_UP, Decimal
from zoneinfo import ZoneInfo


def bugs() -> set[str]:
    """The bugs switched on right now (read on every call, so tests can change them)."""
    return {b.strip() for b in os.environ.get("NAJM_BUGS", "").split(",") if b.strip()}


MINOR_UNITS = {"QAR": 2, "AED": 2, "EUR": 2, "USD": 2, "KWD": 3, "BHD": 3, "OMR": 3, "JPY": 0}
MIN_TRANSFER = Decimal("1")
MAX_PER_TRANSFER = {"QAR": Decimal("25000"), "AED": Decimal("25000"), "EUR": Decimal("5000")}
DAILY_LIMIT = {"QAR": Decimal("50000"), "AED": Decimal("50000"), "EUR": Decimal("10000")}
KINDS = ("own", "domestic", "international")
CUTOFF = time(15, 0)       # local time in Qatar
WEEKEND = {4, 5}           # Friday and Saturday (Monday is 0)


class TransferRejected(Exception):
    """A business rule said no. `code` is stable and safe to assert on."""

    def __init__(self, code: str, message: str = ""):
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code


def quantize(amount, currency: str) -> Decimal:
    """Round half up to the currency's minor units (2 for QAR, 3 for KWD, 0 for JPY)."""
    if currency not in MINOR_UNITS:
        raise ValueError(f"unknown currency: {currency}")
    return Decimal(str(amount)).quantize(Decimal(1).scaleb(-MINOR_UNITS[currency]), rounding=ROUND_HALF_UP)


def fee(amount, currency: str, kind: str) -> Decimal:
    """Own-account: free. Domestic: free up to 1,000, otherwise a flat 2.00.
    International: 0.35 % of the amount, at least 10.00 and at most 100.00."""
    if kind not in KINDS:
        raise ValueError(f"unknown kind: {kind}")
    amount = Decimal(str(amount))
    if kind == "own":
        return quantize(0, currency)
    if kind == "domestic":
        return quantize(0 if amount <= 1000 else 2, currency)
    if "float_fee" in bugs():  # bug: binary floats and round() for money
        return quantize(round(max(10.0, min(100.0, float(amount) * 0.0035)), 2), currency)
    return quantize(max(Decimal("10"), min(Decimal("100"), amount * Decimal("0.0035"))), currency)


@dataclass(frozen=True)
class Decision:
    fee: Decimal
    total: Decimal


def check_transfer(amount, currency: str, kind: str, sent_today=Decimal("0")) -> Decision:
    """Apply the rules to one transfer. Raises TransferRejected, or returns the fee and total."""
    if currency not in DAILY_LIMIT:
        raise TransferRejected("unsupported_currency", currency)
    if kind not in KINDS:
        raise TransferRejected("unsupported_kind", kind)
    amount = Decimal(str(amount))
    if amount != quantize(amount, currency):
        raise TransferRejected("too_many_decimals")
    if amount < MIN_TRANSFER:
        raise TransferRejected("below_minimum")
    if amount > MAX_PER_TRANSFER[currency]:
        raise TransferRejected("above_per_transfer_max")
    projected = Decimal(str(sent_today)) + amount
    limit = DAILY_LIMIT[currency]
    if (projected >= limit) if "limit_off_by_one" in bugs() else (projected > limit):
        raise TransferRejected("daily_limit_exceeded")
    f = fee(amount, currency, kind)
    return Decision(fee=f, total=amount + f)


def next_business_day(d: date) -> date:
    while d.weekday() in WEEKEND:
        d += timedelta(days=1)
    return d


def value_date(now: datetime, tz: str = "Asia/Qatar") -> date:
    """The day a transfer submitted at `now` (timezone-aware) is processed.
    Before 15:00 local time: today. At or after 15:00: the next day. Weekends are skipped."""
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    local = now.astimezone(ZoneInfo("UTC" if "tz_cutoff" in bugs() else tz))  # bug: cut-off read in UTC
    d = local.date() + (timedelta(days=1) if local.time() >= CUTOFF else timedelta(0))
    return next_business_day(d)


ACCOUNTS = {
    "acc-1": {"owner": "alice", "currency": "QAR", "balance": Decimal("12000.00")},
    "acc-2": {"owner": "bob", "currency": "QAR", "balance": Decimal("800.00")},
    "acc-3": {"owner": "alice", "currency": "EUR", "balance": Decimal("2500.00")},
}


class TransferService:
    """In-memory transfers with idempotency keys. One instance per test keeps tests isolated."""

    def __init__(self, accounts: dict | None = None):
        self.accounts = {k: dict(v) for k, v in (accounts or ACCOUNTS).items()}
        self._by_id: dict[str, dict] = {}
        self._by_key: dict[tuple[str, str], tuple[tuple, dict]] = {}
        self._sent_today: dict[tuple[str, str], Decimal] = defaultdict(Decimal)
        self._seq = 0

    def submit(self, user: str, req: dict, key: str, now: datetime | None = None) -> tuple[dict, bool]:
        """Create a transfer. Returns (transfer, created). A repeat of the same key and
        request returns the first result with created=False; the same key with a
        different request is rejected."""
        fingerprint = (req["from_account"], req["to_account"], str(req["amount"]), req["currency"], req["kind"])
        if "no_idempotency" not in bugs() and (user, key) in self._by_key:
            seen_fp, seen = self._by_key[(user, key)]
            if seen_fp != fingerprint:
                raise TransferRejected("idempotency_key_reuse")
            return seen, False
        src = self.accounts.get(req["from_account"])
        if src is None or src["owner"] != user:
            raise TransferRejected("not_owner")
        if req["to_account"] not in self.accounts:
            raise TransferRejected("unknown_recipient")
        if src["currency"] != req["currency"]:
            raise TransferRejected("currency_mismatch")
        decision = check_transfer(req["amount"], req["currency"], req["kind"], self._sent_today[(user, req["currency"])])
        if src["balance"] < decision.total:
            raise TransferRejected("insufficient_funds")
        src["balance"] -= decision.total
        self.accounts[req["to_account"]]["balance"] += Decimal(str(req["amount"]))
        self._sent_today[(user, req["currency"])] += Decimal(str(req["amount"]))
        self._seq += 1
        transfer = {
            "id": f"tr-{self._seq:04d}", "owner": user, "status": "accepted",
            "from_account": req["from_account"], "to_account": req["to_account"],
            "amount": str(Decimal(str(req["amount"]))), "currency": req["currency"],
            "fee": str(decision.fee), "value_date": value_date(now or datetime.now(ZoneInfo("UTC"))).isoformat(),
        }
        self._by_id[transfer["id"]] = transfer
        self._by_key[(user, key)] = (fingerprint, transfer)
        return transfer, True

    def get(self, user: str, transfer_id: str) -> dict:
        t = self._by_id.get(transfer_id)
        if t is None:
            raise TransferRejected("not_found")
        if t["owner"] != user and "bola" not in bugs():  # bug: any logged-in user can read any transfer
            raise TransferRejected("not_owner")
        return t

    def balance(self, user: str, account_id: str) -> dict:
        acc = self.accounts.get(account_id)
        if acc is None:
            raise TransferRejected("not_found")
        if acc["owner"] != user:
            raise TransferRejected("not_owner")
        return {"account": account_id, "balance": str(acc["balance"]), "currency": acc["currency"]}
