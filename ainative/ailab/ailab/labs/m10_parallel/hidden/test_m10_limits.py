"""Hidden checks for lab m10, task C: ``limits.usage_line`` and the ``limits`` command."""
from datetime import datetime, timezone
from decimal import Decimal

import pytest

from remit.models import Transfer
from remit.money import Money


def utc(text):
    return datetime.fromisoformat(text).replace(tzinfo=timezone.utc)


def past(amount, when):
    """A past transfer; only created_at and send_amount matter to the limits."""
    return Transfer(
        id=f"T-{when.isoformat()}-{amount}",
        customer_id="C001",
        corridor="QAR-INR",
        send_amount=Money(amount, "QAR"),
        fee=Money("5", "QAR"),
        receive_amount=Money("1.00", "INR"),
        rate=Decimal("1"),
        recipient_name="Ravi Kumar",
        delivery_method="bank_deposit",
        created_at=when,
    )


def line(tier, history, now):
    from remit.limits import usage_line

    return usage_line(tier, history, now)


def test_a_customer_with_no_history_has_everything_left():
    now = utc("2026-03-02T09:00:00")
    assert line("T1", [], now) == (
        "T1: today 0.00 of 2000.00 QAR used (2000.00 left); this month 0.00 of 8000.00 QAR used (8000.00 left)"
    )


def test_today_and_this_month_are_added_up_separately():
    now = utc("2026-03-02T09:00:00")
    history = [past("3000.00", utc("2026-03-02T05:00:00")), past("9000.00", utc("2026-03-01T10:00:00"))]
    assert line("T2", history, now) == (
        "T2: today 3000.00 of 10000.00 QAR used (7000.00 left); this month 12000.00 of 40000.00 QAR used (28000.00 left)"
    )


def test_last_months_transfers_do_not_count():
    now = utc("2026-03-02T09:00:00")
    history = [past("4000.00", utc("2026-02-27T10:00:00")), past("100.50", utc("2026-03-02T08:00:00"))]
    assert line("T3", history, now) == (
        "T3: today 100.50 of 30000.00 QAR used (29899.50 left); this month 100.50 of 120000.00 QAR used (119899.50 left)"
    )


def test_a_transfer_made_after_midnight_in_qatar_belongs_to_the_new_day():
    # 21:30 UTC on 2 March is 00:30 on 3 March in Qatar: the 20:00 UTC transfer belongs to "yesterday".
    now = utc("2026-03-02T21:30:00")
    history = [past("700.00", utc("2026-03-02T20:00:00")), past("300.00", utc("2026-03-02T21:10:00"))]
    assert line("T1", history, now) == (
        "T1: today 300.00 of 2000.00 QAR used (1700.00 left); this month 1000.00 of 8000.00 QAR used (7000.00 left)"
    )


def test_the_month_turns_over_at_midnight_in_qatar():
    # 21:30 UTC on 31 March is already 1 April in Qatar.
    now = utc("2026-03-31T21:30:00")
    history = [past("500.00", utc("2026-03-31T10:00:00")), past("250.00", utc("2026-03-31T21:10:00"))]
    assert line("T1", history, now) == (
        "T1: today 250.00 of 2000.00 QAR used (1750.00 left); this month 250.00 of 8000.00 QAR used (7750.00 left)"
    )


def test_what_is_left_is_never_negative():
    now = utc("2026-03-02T09:00:00")
    history = [past("2500.00", utc("2026-03-02T05:00:00"))]
    assert line("T1", history, now) == (
        "T1: today 2500.00 of 2000.00 QAR used (0.00 left); this month 2500.00 of 8000.00 QAR used (5500.00 left)"
    )


def test_cents_add_up_exactly():
    now = utc("2026-03-02T09:00:00")
    history = [past("0.10", utc("2026-03-02T05:00:00")), past("0.20", utc("2026-03-02T06:00:00")), past("33.33", utc("2026-03-02T07:00:00"))]
    assert line("T1", history, now).startswith("T1: today 33.63 of 2000.00 QAR used (1966.37 left)")


def test_an_unknown_tier_raises_the_usual_error():
    from remit.errors import UnknownKycTier

    with pytest.raises(UnknownKycTier):
        line("T9", [], utc("2026-03-02T09:00:00"))


def test_the_command_shows_a_customers_position_from_real_transfers(cli, tmp_path, clock):
    env = {"REMIT_DB": str(tmp_path / "remit.db")}
    assert cli("customer", "add", "--id", "C001", "--name", "Aisha Rahman", "--kyc", "T2", environ=env, clock=clock)[0] == 0
    code, out, err = cli("limits", "--customer", "C001", environ=env, clock=clock)
    assert (code, err) == (0, "")
    assert out.splitlines() == [
        "C001  Aisha Rahman",
        "T2: today 0.00 of 10000.00 QAR used (10000.00 left); this month 0.00 of 40000.00 QAR used (40000.00 left)",
    ]
    assert cli("send", "--customer", "C001", "QAR", "500", "INR", "--recipient", "Ravi Kumar", environ=env, clock=clock)[0] == 0
    code, out, err = cli("limits", "--customer", "C001", environ=env, clock=clock)
    assert (code, err) == (0, "")
    assert out.splitlines() == [
        "C001  Aisha Rahman",
        "T2: today 500.00 of 10000.00 QAR used (9500.00 left); this month 500.00 of 40000.00 QAR used (39500.00 left)",
    ]


def test_the_command_uses_the_clock_it_is_given(cli, tmp_path, clock):
    env = {"REMIT_DB": str(tmp_path / "remit.db")}
    cli("customer", "add", "--id", "C002", "--name", "Bilal Khan", "--kyc", "T1", environ=env, clock=clock)
    cli("send", "--customer", "C002", "QAR", "500", "INR", "--recipient", "Ravi Kumar", environ=env, clock=clock)
    clock.advance(hours=13)  # 22:00 UTC is already the next day in Qatar
    code, out, _ = cli("limits", "--customer", "C002", environ=env, clock=clock)
    assert code == 0
    assert out.splitlines()[1] == (
        "T1: today 0.00 of 2000.00 QAR used (2000.00 left); this month 500.00 of 8000.00 QAR used (7500.00 left)"
    )


def test_an_unknown_customer_exits_with_one_and_names_the_error(cli, tmp_path, clock):
    code, out, err = cli("limits", "--customer", "C404", environ={"REMIT_DB": str(tmp_path / "remit.db")}, clock=clock)
    assert code == 1 and out == ""
    assert err.startswith("error [")  # the CLI's own form, "error [code]: message"; the natural code is unknown_customer


def test_the_command_needs_a_customer(cli, tmp_path, clock):
    code, out, _ = cli("limits", environ={"REMIT_DB": str(tmp_path / "remit.db")}, clock=clock)
    assert code != 0 and out == ""  # bad usage (argparse gives 2) or a Remit error (1): never a silent success
