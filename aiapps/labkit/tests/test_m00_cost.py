"""Module 0, lesson 0.2: cost is arithmetic on usage and a price you copy from the price page."""
import os
import subprocess
import sys
from pathlib import Path

import pytest

from labs.m00.cost import call_cost, conversation_tokens

COST = Path(__file__).resolve().parents[1] / "labs" / "m00" / "cost.py"


def test_call_cost_is_tokens_times_price_per_million():
    assert call_cost(1_000_000, 0, 2.0, 10.0) == pytest.approx(2.0)
    assert call_cost(0, 1_000_000, 2.0, 10.0) == pytest.approx(10.0)
    assert call_cost(2_500, 400, 1.0, 5.0) == pytest.approx((2_500 * 1 + 400 * 5) / 1_000_000)


def test_one_turn_is_system_plus_one_user_message():
    assert conversation_tokens(system=1500, user=60, answer=250, turns=1) == (1560, 250)


def test_history_is_resent_so_input_grows_every_turn():
    # call 1: 1500+60 = 1560; call 2: 1500+120+250 = 1870; call 3: 1500+180+500 = 2180
    assert conversation_tokens(1500, 60, 250, 3) == (1560 + 1870 + 2180, 750)


def test_doubling_the_turns_more_than_doubles_the_input_bill():
    short, _ = conversation_tokens(1500, 60, 250, 6)
    long, _ = conversation_tokens(1500, 60, 250, 12)
    assert long > 2 * short


def run(**env):
    clean = {k: v for k, v in os.environ.items() if not k.startswith("PRICE_")}
    clean.update(env)
    return subprocess.run([sys.executable, str(COST), "--turns", "6", "--conversations", "10", "--weeks", "2"],
                          env=clean, capture_output=True, text=True, timeout=60)


def test_cli_prints_tokens_without_prices_and_asks_for_them():
    r = run()
    assert r.returncode == 0 and "in=14010 out=1500" in r.stdout and "PRICE_IN_PER_MTOK" in r.stdout


def test_cli_prints_money_when_prices_are_set():
    r = run(PRICE_IN_PER_MTOK="1", PRICE_OUT_PER_MTOK="5")
    assert r.returncode == 0 and "per conversation" in r.stdout and "budget at x2" in r.stdout
