"""Hidden acceptance tests for lab m06 (the learner never sees this file in their work directory).

They check *behaviour* through the public interface the ticket names: ``check_limits``, ``day_window``,
``month_window``, ``to_local`` and ``RemitService.send``. They accept any sound fix: restoring the
conversion, inlining ``astimezone(QATAR_TZ)``, adding a helper. They compare instants, so they do not care
which tzinfo object a window carries. The reference for "what is right" is written here independently of the
code under test: a fixed UTC+3 offset (Qatar has no daylight saving).
"""
from datetime import datetime, time, timedelta, timezone
from decimal import Decimal

import pytest

from remit.errors import LimitExceeded
from remit.limits import DAILY_EXCEEDED, LIMITS, MONTHLY_EXCEEDED, check_limits, day_window, month_window, to_local
from remit.models import Transfer
from remit.money import Money

QATAR = timezone(timedelta(hours=3))
UTC = timezone.utc
DAY = timedelta(days=1)


def utc(*parts):
    return datetime(*parts, tzinfo=UTC)


def qar(value):
    return Money(value, "QAR")


def past(amount, when):
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


# -- the boundary tests the tidy-up removed ---------------------------------------------------------------------
def test_the_day_ends_at_midnight_in_qatar_not_in_utc():
    just_before = utc(2026, 3, 2, 20, 59, 59)  # 23:59:59 in Qatar: still Monday 2 March
    just_after = utc(2026, 3, 2, 21, 0, 0)  # 00:00:00 on Tuesday 3 March in Qatar
    history = [past("2000.00", just_before)]
    assert not check_limits("T1", history, qar("1"), just_before).allowed
    assert check_limits("T1", history, qar("1"), just_after).allowed


def test_a_transfer_after_qatar_midnight_but_before_utc_midnight_belongs_to_the_new_day():
    early_tuesday = utc(2026, 3, 2, 22, 30)  # 01:30 on Tuesday 3 March in Qatar
    history = [past("2000.00", early_tuesday)]
    assert check_limits("T1", history, qar("1"), utc(2026, 3, 2, 9, 0)).daily_used == qar("0")
    assert check_limits("T1", history, qar("1"), early_tuesday + timedelta(hours=1)).daily_used == qar("2000.00")


def test_the_month_changes_at_midnight_in_qatar():
    history = [past("7000.00", utc(2026, 2, 28, 20, 59))]  # 23:59 on 28 February in Qatar
    march_first = utc(2026, 2, 28, 21, 0)  # 00:00 on 1 March in Qatar
    assert check_limits("T1", history, qar("2000"), march_first).allowed
    assert not check_limits("T1", history, qar("2000"), march_first - timedelta(minutes=2)).allowed


def test_windows_are_qatar_calendar_windows():
    now = utc(2026, 3, 2, 9, 0)
    start, end = day_window(now)
    assert start == datetime(2026, 3, 2, tzinfo=QATAR) and end == datetime(2026, 3, 3, tzinfo=QATAR)
    assert start.astimezone(UTC) == utc(2026, 3, 1, 21, 0)
    start, end = month_window(now)
    assert start == datetime(2026, 3, 1, tzinfo=QATAR) and end == datetime(2026, 4, 1, tzinfo=QATAR)
    assert month_window(utc(2026, 12, 15))[1] == datetime(2027, 1, 1, tzinfo=QATAR)
    assert to_local(now).hour == 12


# -- the same rules, tested over a whole week of instants so that no special case can hide ------------------------
def instants(start, days, step_minutes):
    moment = start
    while moment < start + timedelta(days=days):
        yield moment
        moment += timedelta(minutes=step_minutes)


def test_every_instant_is_inside_a_qatar_day_window_that_starts_at_qatar_midnight():
    for now in instants(utc(2026, 2, 25), 8, 17):
        start, end = day_window(now)
        assert start <= now < end
        assert end - start == DAY
        local_start = start.astimezone(QATAR)
        assert local_start.time() == time(0, 0), f"the day containing {now.isoformat()} does not start at Qatar midnight"


def test_every_instant_is_inside_a_qatar_month_window_that_starts_on_the_first():
    for now in instants(utc(2026, 2, 25), 8, 17):
        start, end = month_window(now)
        assert start <= now < end
        local_start, local_end = start.astimezone(QATAR), end.astimezone(QATAR)
        assert local_start.day == 1 and local_start.time() == time(0, 0)
        assert local_end.day == 1 and local_end.time() == time(0, 0)
        assert (local_end.year, local_end.month) == (local_start.year + (local_start.month == 12), local_start.month % 12 + 1)


@pytest.mark.parametrize("year, month", [(2026, 1), (2026, 2), (2026, 3), (2026, 8), (2026, 12), (2028, 2)])
def test_each_month_starts_at_qatar_midnight_on_the_first(year, month):
    first_midnight = datetime(year, month, 1, tzinfo=QATAR)
    for offset in (timedelta(0), timedelta(hours=11, minutes=59), timedelta(days=14, hours=3)):
        start, _ = month_window(first_midnight + offset)
        assert start == first_midnight
    start, _ = month_window(first_midnight - timedelta(seconds=1))
    assert start != first_midnight  # the last second of the previous month


def test_windows_accept_any_time_zone_for_the_input():
    in_qatar = datetime(2026, 3, 3, 0, 30, tzinfo=QATAR)  # Tuesday 3 March, 30 minutes after midnight in Qatar
    in_london = in_qatar.astimezone(timezone(timedelta(hours=0)))
    in_tokyo = in_qatar.astimezone(timezone(timedelta(hours=9)))
    expected = (datetime(2026, 3, 3, tzinfo=QATAR), datetime(2026, 3, 4, tzinfo=QATAR))
    assert day_window(in_qatar) == day_window(in_london) == day_window(in_tokyo) == expected


# -- the behaviour the fix must leave alone ----------------------------------------------------------------------
def test_reaching_a_limit_exactly_is_still_allowed_and_one_cent_over_is_not():
    history = [past("1500.00", utc(2026, 3, 2, 8, 0))]
    now = utc(2026, 3, 2, 9, 0)
    assert check_limits("T1", history, qar("500.00"), now).allowed
    over = check_limits("T1", history, qar("500.01"), now)
    assert not over.allowed and over.reason == DAILY_EXCEEDED


def test_daily_is_reported_before_monthly_and_the_monthly_limit_still_works():
    now = utc(2026, 3, 2, 9, 0)
    five_days = [past("1600.00", utc(2026, 3, 1, 9 + i, 0)) for i in range(5)]  # 8,000 yesterday: the T1 month is full
    result = check_limits("T1", five_days, qar("100"), now)
    assert not result.allowed and result.reason == MONTHLY_EXCEEDED
    assert result.daily_used == qar("0") and result.monthly_used == qar("8000.00")
    both = five_days + [past("1900.00", utc(2026, 3, 2, 8, 0))]
    assert check_limits("T1", both, qar("200"), now).reason == DAILY_EXCEEDED
    assert LIMITS["T1"].daily == qar("2000.00") and LIMITS["T1"].monthly == qar("8000.00")


def test_the_result_still_reports_the_position_before_the_new_transfer():
    now = utc(2026, 3, 2, 9, 0)
    history = [past("700.00", now - timedelta(hours=2)), past("300.00", now - timedelta(hours=1))]
    result = check_limits("T1", history, qar("100"), now)
    assert result.daily_used == qar("1000.00") and result.daily_remaining == qar("1000.00")
    assert result.monthly_used == qar("1000.00") and result.monthly_remaining == qar("7000.00")


# -- the customer's view: through the service ---------------------------------------------------------------------
def test_a_customer_is_not_refused_after_qatar_midnight(service, clock, customers):
    clock.set(utc(2026, 3, 2, 17, 0))  # 20:00 on Monday in Qatar
    service.send("C002", qar("1500.00"), "INR", "Ravi Kumar")
    clock.set(utc(2026, 3, 2, 22, 30))  # 01:30 on Tuesday in Qatar: a new day
    result = service.send("C002", qar("1000.00"), "INR", "Ravi Kumar")
    assert result.limits.daily_used == qar("0")


def test_a_customer_is_still_refused_before_qatar_midnight(service, clock, customers):
    clock.set(utc(2026, 3, 2, 17, 0))
    service.send("C002", qar("1500.00"), "INR", "Ravi Kumar")
    clock.set(utc(2026, 3, 2, 20, 59, 59))  # 23:59:59 on Monday in Qatar
    with pytest.raises(LimitExceeded):
        service.send("C002", qar("600.00"), "INR", "Ravi Kumar")


def test_a_customer_cannot_use_two_days_of_limit_in_one_qatar_day(service, clock, customers):
    clock.set(utc(2026, 3, 2, 21, 30))  # 00:30 on Tuesday in Qatar
    service.send("C002", qar("1800.00"), "INR", "Ravi Kumar")
    clock.set(utc(2026, 3, 3, 0, 40))  # 03:40 on Tuesday in Qatar, but already Tuesday in UTC
    with pytest.raises(LimitExceeded):
        service.send("C002", qar("1500.00"), "INR", "Ravi Kumar")
