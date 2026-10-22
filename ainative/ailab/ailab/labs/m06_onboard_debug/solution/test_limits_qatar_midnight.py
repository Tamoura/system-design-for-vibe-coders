"""Regression tests for REMIT-231: the day and the month of the limits begin at midnight in Qatar (UTC+3).

The first test replays what happened to customer C2207 in prod.log, using the real moments from the log.
The rest pin the boundary on both sides, for the day and for the month, and the direction nobody had
noticed (a customer let through over the limit in the small hours).
"""
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from remit.limits import DAILY_EXCEEDED, MONTHLY_EXCEEDED, check_limits, day_window, month_window
from remit.models import Transfer
from remit.money import Money

QATAR = timezone(timedelta(hours=3))


def utc(*parts):
    return datetime(*parts, tzinfo=timezone.utc)


def qar(value):
    return Money(value, "QAR")


def sent(amount, when):
    return Transfer(
        id=f"TRF-{when:%Y%m%d%H%M%S}", customer_id="C2207", corridor="QAR-INR", send_amount=qar(amount), fee=qar("20.00"),
        receive_amount=Money("22572.00", "INR"), rate=Decimal("22.572"), recipient_name="R. Kumar",
        delivery_method="bank_deposit", created_at=when,
    )


def test_c2207_is_not_refused_just_after_qatar_midnight():
    # prod.log: sent 1,200 at 16:42 UTC on Friday 13 March, then tried 1,000 at 22:18 UTC the same UTC day.
    # 22:18 UTC is 01:18 on Saturday in Qatar: a new day, so the T1 daily limit of 2,000 is not in play.
    history = [sent("1200.00", utc(2026, 3, 13, 16, 42, 7))]
    result = check_limits("T1", history, qar("1000.00"), utc(2026, 3, 13, 22, 18, 9))
    assert result.allowed and result.reason is None
    assert result.daily_used == qar("0.00")


def test_the_last_second_before_qatar_midnight_still_counts_for_the_old_day():
    history = [sent("1500.00", utc(2026, 3, 13, 16, 0))]
    result = check_limits("T1", history, qar("600.00"), utc(2026, 3, 13, 20, 59, 59))
    assert not result.allowed and result.reason == DAILY_EXCEEDED


def test_the_first_second_after_qatar_midnight_is_a_new_day():
    history = [sent("1500.00", utc(2026, 3, 13, 16, 0))]
    result = check_limits("T1", history, qar("600.00"), utc(2026, 3, 13, 21, 0, 0))
    assert result.allowed and result.daily_used == qar("0.00")


def test_a_customer_cannot_spend_two_days_of_limit_in_one_qatar_day():
    # The other direction: 1,800 at 00:40 on Sunday in Qatar (21:40 UTC on Saturday), then 1,500 at 03:40 in Qatar
    # (00:40 UTC on Sunday). Same Qatar day, so 3,300 is over the T1 limit of 2,000. The old code allowed it.
    history = [sent("1800.00", utc(2026, 3, 14, 21, 40))]
    result = check_limits("T1", history, qar("1500.00"), utc(2026, 3, 15, 0, 40))
    assert not result.allowed and result.reason == DAILY_EXCEEDED
    assert result.daily_used == qar("1800.00")


def test_the_day_window_runs_from_qatar_midnight_to_qatar_midnight():
    start, end = day_window(utc(2026, 3, 13, 22, 18))
    assert start == datetime(2026, 3, 14, tzinfo=QATAR) and end == datetime(2026, 3, 15, tzinfo=QATAR)
    assert start.astimezone(timezone.utc) == utc(2026, 3, 13, 21, 0)


def test_the_month_changes_at_qatar_midnight_not_at_utc_midnight():
    # A T2 customer (daily 10,000, monthly 40,000) has sent 39,900 in March. 22:30 UTC on 31 March is 01:30 on
    # 1 April in Qatar, so the March spending no longer counts; two hours earlier it still does.
    history = [sent("9000.00", utc(2026, 3, day, 12, 0)) for day in (27, 28, 29, 30)] + [sent("3900.00", utc(2026, 3, 31, 12, 0))]
    april = utc(2026, 3, 31, 22, 30)
    assert check_limits("T2", history, qar("1000.00"), april).allowed
    assert check_limits("T2", history, qar("1000.00"), april - timedelta(hours=2)).reason == MONTHLY_EXCEEDED
    assert month_window(april)[0] == datetime(2026, 4, 1, tzinfo=QATAR)
