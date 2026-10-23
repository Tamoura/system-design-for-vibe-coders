from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from remit.errors import CurrencyMismatch, InvalidAmount, UnknownKycTier
from remit.limits import (
    DAILY_EXCEEDED,
    LIMITS,
    MONTHLY_EXCEEDED,
    QATAR_TZ,
    check_limits,
    day_window,
    month_window,
    to_local,
)
from remit.models import Transfer
from remit.money import Money

# Monday 2 March 2026, 12:00 in Qatar (09:00 UTC).
NOW = datetime(2026, 3, 2, 9, 0, tzinfo=timezone.utc)


def qar(value):
    return Money(value, "QAR")


def past(amount, when):
    """A past transfer; only created_at and send_amount matter to the limits."""
    return Transfer(
        id=f"T-{when.isoformat()}-{amount}",
        customer_id="C001",
        corridor="QAR-INR",
        send_amount=qar(amount),
        fee=qar("5"),
        receive_amount=Money("1.00", "INR"),
        rate=Decimal("1"),
        recipient_name="Ravi Kumar",
        delivery_method="bank_deposit",
        created_at=when,
    )


def test_an_empty_history_allows_anything_up_to_the_daily_limit():
    documented = {"T1": ("2000", "8000"), "T2": ("10000", "40000"), "T3": ("30000", "120000")}
    assert {t: (str(v.daily.amount), str(v.monthly.amount)) for t, v in LIMITS.items()} == {
        t: (f"{d}.00", f"{m}.00") for t, (d, m) in documented.items()
    }
    result = check_limits("T1", [], qar("2000.00"), NOW)
    assert result.allowed and result.reason is None
    assert result.daily_used == qar("0") and result.daily_remaining == qar("2000.00")


def test_reaching_the_limit_exactly_is_allowed_and_one_cent_over_is_not():
    history = [past("1500.00", NOW - timedelta(hours=1))]
    assert check_limits("T1", history, qar("500.00"), NOW).allowed
    over = check_limits("T1", history, qar("500.01"), NOW)
    assert not over.allowed and over.reason == DAILY_EXCEEDED


def test_the_result_reports_the_position_before_the_new_transfer():
    history = [past("700.00", NOW - timedelta(hours=2)), past("300.00", NOW - timedelta(hours=1))]
    result = check_limits("T1", history, qar("100"), NOW)
    assert result.daily_used == qar("1000.00") and result.daily_remaining == qar("1000.00")
    assert result.monthly_used == qar("1000.00") and result.monthly_remaining == qar("7000.00")
    assert result.tier == "T1" and result.daily_limit == qar("2000")


def test_monthly_limit():
    # Five transfers of 1,600 yesterday: 8,000 used this month, none today.
    history = [past("1600.00", datetime(2026, 3, 1, 9 + i, 0, tzinfo=timezone.utc)) for i in range(5)]
    result = check_limits("T1", history, qar("100"), NOW)
    assert not result.allowed and result.reason == MONTHLY_EXCEEDED
    assert result.daily_used == qar("0") and result.monthly_used == qar("8000.00")
    assert check_limits("T2", history, qar("100"), NOW).allowed  # T2 has room


def test_daily_is_reported_before_monthly_when_both_are_exceeded():
    history = [past("1900.00", NOW - timedelta(hours=1))] + [
        past("1600.00", datetime(2026, 3, 1, 9 + i, 0, tzinfo=timezone.utc)) for i in range(4)
    ]
    assert check_limits("T1", history, qar("200"), NOW).reason == DAILY_EXCEEDED


def test_old_months_do_not_count():
    history = [past("7900.00", datetime(2026, 2, 28, 9, 0, tzinfo=timezone.utc))]
    result = check_limits("T1", history, qar("1000"), NOW)
    assert result.allowed and result.monthly_used == qar("0")


def test_the_day_ends_at_midnight_in_qatar_not_in_utc():
    # 20:59:59 UTC is 23:59:59 in Qatar: still Monday 2 March.
    just_before = datetime(2026, 3, 2, 20, 59, 59, tzinfo=timezone.utc)
    # 21:00:00 UTC is 00:00:00 on Tuesday 3 March in Qatar.
    just_after = datetime(2026, 3, 2, 21, 0, 0, tzinfo=timezone.utc)
    history = [past("2000.00", just_before)]
    assert not check_limits("T1", history, qar("1"), just_before).allowed  # same Qatar day
    assert check_limits("T1", history, qar("1"), just_after).allowed  # a new Qatar day


def test_a_transfer_after_qatar_midnight_but_before_utc_midnight_belongs_to_the_new_day():
    # 22:30 UTC on 2 March is 01:30 on 3 March in Qatar.
    early_tuesday = datetime(2026, 3, 2, 22, 30, tzinfo=timezone.utc)
    history = [past("2000.00", early_tuesday)]
    monday_noon = NOW
    assert check_limits("T1", history, qar("1"), monday_noon).daily_used == qar("0")
    assert check_limits("T1", history, qar("1"), early_tuesday + timedelta(hours=1)).daily_used == qar("2000.00")


def test_the_month_changes_at_midnight_in_qatar():
    # 21:00 UTC on 28 February is 00:00 on 1 March in Qatar.
    history = [past("7000.00", datetime(2026, 2, 28, 20, 59, tzinfo=timezone.utc))]
    march_1_local = datetime(2026, 2, 28, 21, 0, tzinfo=timezone.utc)
    assert check_limits("T1", history, qar("2000"), march_1_local).allowed  # February is gone
    assert not check_limits("T1", history, qar("2000"), march_1_local - timedelta(minutes=2)).allowed


def test_windows_are_local_calendar_windows():
    start, end = day_window(NOW)
    assert (start, end) == (datetime(2026, 3, 2, tzinfo=QATAR_TZ), datetime(2026, 3, 3, tzinfo=QATAR_TZ))
    assert start.astimezone(timezone.utc) == datetime(2026, 3, 1, 21, 0, tzinfo=timezone.utc)
    start, end = month_window(NOW)
    assert (start, end) == (datetime(2026, 3, 1, tzinfo=QATAR_TZ), datetime(2026, 4, 1, tzinfo=QATAR_TZ))
    assert month_window(datetime(2026, 12, 15, tzinfo=timezone.utc))[1] == datetime(2027, 1, 1, tzinfo=QATAR_TZ)
    assert to_local(NOW).hour == 12


def test_bad_inputs():
    with pytest.raises(UnknownKycTier):
        check_limits("T9", [], qar("10"), NOW)
    with pytest.raises(CurrencyMismatch):
        check_limits("T1", [], Money("10", "INR"), NOW)
    with pytest.raises(InvalidAmount):
        check_limits("T1", [], qar("0"), NOW)
    with pytest.raises(ValueError):
        check_limits("T1", [], qar("10"), datetime(2026, 3, 2, 9, 0))
