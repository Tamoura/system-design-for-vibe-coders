"""Sending limits by KYC tier.

KYC ("know your customer") tiers say how well Najm has verified a customer:

* T1: identity document checked only (the lowest limits)
* T2: also address and employer verified
* T3: enhanced due diligence completed (the highest limits)

Each tier has a daily and a monthly limit in QAR (fictional numbers). A transfer is
allowed when what the customer has already sent in the window plus the new amount is
less than or equal to the limit (reaching the limit exactly is allowed).

"Day" and "month" are *Qatar calendar* days and months. Qatar is UTC+3 all year with
no daylight saving, so we use a fixed offset: the day runs from 00:00 to 24:00 at
UTC+3, which is 21:00 to 21:00 in UTC. Timestamps are stored in UTC, so everything
that decides which window a transfer falls into must convert with ``to_local`` first.
"""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Protocol

from remit.errors import CurrencyMismatch, InvalidAmount, UnknownKycTier
from remit.money import Money

QATAR_UTC_OFFSET = timedelta(hours=3)
QATAR_TZ = timezone(QATAR_UTC_OFFSET, "AST")

DAILY_EXCEEDED = "daily_limit_exceeded"
MONTHLY_EXCEEDED = "monthly_limit_exceeded"


@dataclass(frozen=True)
class TierLimits:
    daily: Money
    monthly: Money


# Fictional limits in QAR.
LIMITS: dict[str, TierLimits] = {
    "T1": TierLimits(daily=Money("2000.00", "QAR"), monthly=Money("8000.00", "QAR")),
    "T2": TierLimits(daily=Money("10000.00", "QAR"), monthly=Money("40000.00", "QAR")),
    "T3": TierLimits(daily=Money("30000.00", "QAR"), monthly=Money("120000.00", "QAR")),
}


class HistoryItem(Protocol):
    """What check_limits needs from a past transfer (remit.models.Transfer has both)."""

    created_at: datetime
    send_amount: Money


@dataclass(frozen=True)
class LimitResult:
    allowed: bool
    reason: str | None  # None, DAILY_EXCEEDED or MONTHLY_EXCEEDED
    tier: str
    daily_used: Money  # already sent today, NOT counting the amount being checked
    daily_limit: Money
    monthly_used: Money  # already sent this month, NOT counting the amount being checked
    monthly_limit: Money

    @property
    def daily_remaining(self) -> Money:
        return max(self.daily_limit - self.daily_used, Money.zero("QAR"))

    @property
    def monthly_remaining(self) -> Money:
        return max(self.monthly_limit - self.monthly_used, Money.zero("QAR"))


def limits_for(tier: str) -> TierLimits:
    try:
        return LIMITS[tier]
    except KeyError:
        raise UnknownKycTier(f"unknown KYC tier {tier!r}") from None


def _require_aware(moment: datetime) -> None:
    if moment.tzinfo is None or moment.utcoffset() is None:
        raise ValueError("datetimes must be timezone-aware")


def to_local(moment: datetime) -> datetime:
    """Convert an aware datetime to Qatar local time (UTC+3)."""
    _require_aware(moment)
    return moment.astimezone(QATAR_TZ)


def day_window(now: datetime) -> tuple[datetime, datetime]:
    """Start (inclusive) and end (exclusive) of the Qatar calendar day containing ``now``."""
    local = to_local(now)
    start = local.replace(hour=0, minute=0, second=0, microsecond=0)
    return start, start + timedelta(days=1)


def month_window(now: datetime) -> tuple[datetime, datetime]:
    """Start (inclusive) and end (exclusive) of the Qatar calendar month containing ``now``."""
    local = to_local(now)
    start = local.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if start.month == 12:
        end = start.replace(year=start.year + 1, month=1)
    else:
        end = start.replace(month=start.month + 1)
    return start, end


def check_limits(tier: str, history: Iterable[HistoryItem], amount: Money, now: datetime) -> LimitResult:
    """Can a customer of KYC ``tier`` send ``amount`` (QAR) at time ``now``?

    ``history`` is the customer's earlier transfers (each with ``created_at`` and
    ``send_amount``). The daily limit is checked first, so when both limits would be
    exceeded the reason is ``daily_limit_exceeded``.
    """
    limits = limits_for(tier)
    _require_aware(now)
    if amount.currency != "QAR":
        raise CurrencyMismatch(f"limits are in QAR, got {amount.currency}")
    if amount <= Money.zero("QAR"):
        raise InvalidAmount("amount must be greater than zero")

    day_start, day_end = day_window(now)
    month_start, month_end = month_window(now)
    daily_used = Money.zero("QAR")
    monthly_used = Money.zero("QAR")
    for item in history:
        _require_aware(item.created_at)
        if month_start <= item.created_at < month_end:
            monthly_used += item.send_amount
            if day_start <= item.created_at < day_end:
                daily_used += item.send_amount

    reason = None
    if daily_used + amount > limits.daily:
        reason = DAILY_EXCEEDED
    elif monthly_used + amount > limits.monthly:
        reason = MONTHLY_EXCEEDED
    return LimitResult(
        allowed=reason is None,
        reason=reason,
        tier=tier,
        daily_used=daily_used,
        daily_limit=limits.daily,
        monthly_used=monthly_used,
        monthly_limit=limits.monthly,
    )
