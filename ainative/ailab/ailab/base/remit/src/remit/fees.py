"""Fees: what Najm charges to send money.

A fee schedule is a table of tiers. The tier is chosen by the *whole* send amount
(it is not marginal): the first tier whose ``upto`` is greater than or equal to the
amount applies, so exactly 500.00 is in the first tier of STD-A and 500.01 is in
the second. The fee is then

    raw      = amount * tier.percent + tier.flat        (rounded half up to 2 dp)
    base     = min(max(raw, schedule.minimum), schedule.cap)
    total    = base + schedule.express_surcharge        (only when express=True)

so the express surcharge is added *after* the cap. All numbers are fictional and are
in QAR, the send currency of every corridor today.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from remit.corridors import Corridor
from remit.errors import CurrencyMismatch, InvalidAmount, UnknownFeeSchedule
from remit.money import Money


@dataclass(frozen=True)
class FeeTier:
    upto: Decimal | None  # inclusive upper bound in QAR; None = no upper bound
    percent: Decimal  # a fraction: Decimal("0.02") is 2%
    flat: Decimal  # QAR added on top of the percentage


@dataclass(frozen=True)
class FeeSchedule:
    id: str
    tiers: tuple[FeeTier, ...]
    minimum: Decimal  # QAR; the fee is never lower than this
    cap: Decimal  # QAR; the fee (before express) is never higher than this
    express_surcharge: Decimal  # QAR flat, added after the cap

    def __post_init__(self) -> None:
        bounds = [t.upto for t in self.tiers[:-1]]
        if not self.tiers or self.tiers[-1].upto is not None or None in bounds:
            raise ValueError(f"{self.id}: only the last tier may be unbounded")
        if bounds != sorted(bounds):
            raise ValueError(f"{self.id}: tiers must be in ascending order")
        if self.minimum > self.cap:
            raise ValueError(f"{self.id}: minimum is above cap")

    def tier_index(self, amount: Decimal) -> int:
        for index, tier in enumerate(self.tiers):
            if tier.upto is None or amount <= tier.upto:
                return index
        raise AssertionError("unreachable: the last tier is unbounded")  # pragma: no cover


def _D(value: str) -> Decimal:
    return Decimal(value)


# Fictional numbers. STD-A prices the QAR->INR and QAR->PHP corridors.
STD_A = FeeSchedule(
    id="STD-A",
    tiers=(
        FeeTier(_D("500.00"), _D("0.0200"), _D("2.00")),
        FeeTier(_D("2000.00"), _D("0.0150"), _D("5.00")),
        FeeTier(_D("10000.00"), _D("0.0100"), _D("20.00")),
        FeeTier(None, _D("0.0075"), _D("50.00")),
    ),
    minimum=_D("5.00"),
    cap=_D("150.00"),
    express_surcharge=_D("15.00"),
)

# STD-B prices the QAR->EGP and QAR->PKR corridors.
STD_B = FeeSchedule(
    id="STD-B",
    tiers=(
        FeeTier(_D("1000.00"), _D("0.0250"), _D("3.00")),
        FeeTier(_D("5000.00"), _D("0.0180"), _D("10.00")),
        FeeTier(None, _D("0.0120"), _D("40.00")),
    ),
    minimum=_D("6.00"),
    cap=_D("120.00"),
    express_surcharge=_D("20.00"),
)

SCHEDULES: dict[str, FeeSchedule] = {s.id: s for s in (STD_A, STD_B)}


@dataclass(frozen=True)
class FeeBreakdown:
    """How a fee was built (for explaining a quote to a customer or a reviewer)."""

    schedule_id: str
    tier_index: int  # 0-based
    raw: Money  # percentage + flat, before minimum and cap
    minimum_applied: bool
    cap_applied: bool
    base: Money  # after minimum and cap
    surcharge: Money  # zero unless express
    total: Money  # base + surcharge


def get_schedule(schedule_id: str) -> FeeSchedule:
    try:
        return SCHEDULES[schedule_id]
    except KeyError:
        raise UnknownFeeSchedule(f"no fee schedule {schedule_id!r}") from None


def explain_fee(amount: Money, corridor: Corridor, *, express: bool = False) -> FeeBreakdown:
    """Price ``amount`` on ``corridor`` and show the working."""
    if amount.currency != corridor.send_currency:
        raise CurrencyMismatch(f"{corridor.code} fees are in {corridor.send_currency}, got {amount.currency}")
    if amount <= Money.zero(amount.currency):
        raise InvalidAmount("amount must be greater than zero")
    schedule = get_schedule(corridor.fee_schedule)
    index = schedule.tier_index(amount.amount)
    tier = schedule.tiers[index]
    cur = amount.currency
    raw = Money(amount.amount * tier.percent + tier.flat, cur)
    minimum, cap = Money(schedule.minimum, cur), Money(schedule.cap, cur)
    base = min(max(raw, minimum), cap)
    surcharge = Money(schedule.express_surcharge, cur) if express else Money.zero(cur)
    return FeeBreakdown(
        schedule_id=schedule.id,
        tier_index=index,
        raw=raw,
        minimum_applied=raw < minimum,
        cap_applied=raw > cap,
        base=base,
        surcharge=surcharge,
        total=base + surcharge,
    )


def quote_fee(amount: Money, corridor: Corridor, *, express: bool = False) -> Money:
    """The fee (a Money in the send currency) to send ``amount`` on ``corridor``."""
    return explain_fee(amount, corridor, express=express).total
