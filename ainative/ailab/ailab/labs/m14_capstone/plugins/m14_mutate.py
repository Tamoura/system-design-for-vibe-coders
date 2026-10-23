"""A pytest plugin for lab m14's advisory "your tests have teeth" check. It is not a test and not a lab.

The grader runs the learner's own new tests in a throw-away copy with ``-p m14_mutate`` and the environment
variable ``M14_MUTANT`` set to one of the ids below. The plugin then breaks ONE agreed number of the BDT corridor in
memory, after the modules are imported and before any test runs, so it works whatever the learner's code looks like
as long as it keeps the repository's own extension points (``CORRIDORS``, ``SCHEDULES``, ``DEFAULT_MID_RATES``,
``CORRIDOR_MARGINS``). If a mutant cannot be applied the run ends with exit code 97 ("not applied"), which the
grader counts as neither caught nor missed.
"""
from __future__ import annotations

import os
from dataclasses import replace
from decimal import Decimal

NOT_APPLIED = 97

# id -> what the mutant breaks, in words a learner can act on (shown when a mutant survives)
DESCRIPTIONS = {
    "max-send": "the maximum per transfer (one cent too high)",
    "tier-edge": "the first fee tier boundary (1,000.00 treated as tier 1)",
    "fee-cap": "the fee cap",
    "margin": "the margin on the rate",
    "express": "the express surcharge",
    "delivery": "the delivery methods (cash pickup allowed)",
}


def _mutate(mutant: str) -> None:
    from remit import corridors, fees, fx
    from remit.money import Money

    if mutant == "max-send":
        c = corridors.CORRIDORS["QAR-BDT"]
        corridors.CORRIDORS["QAR-BDT"] = replace(c, max_send=Money("12000.01", "QAR"))
    elif mutant == "tier-edge":
        s = fees.SCHEDULES["STD-C"]
        first, *rest = s.tiers
        fees.SCHEDULES["STD-C"] = replace(s, tiers=(replace(first, upto=Decimal("999.99")), *rest))
    elif mutant == "fee-cap":
        s = fees.SCHEDULES["STD-C"]
        fees.SCHEDULES["STD-C"] = replace(s, cap=s.cap + Decimal("1.00"))
    elif mutant == "margin":
        fx.CORRIDOR_MARGINS["QAR-BDT"] = fx.CORRIDOR_MARGINS["QAR-BDT"] + Decimal("0.0001")
    elif mutant == "express":
        s = fees.SCHEDULES["STD-C"]
        fees.SCHEDULES["STD-C"] = replace(s, express_surcharge=s.express_surcharge - Decimal("1.00"))
    elif mutant == "delivery":
        c = corridors.CORRIDORS["QAR-BDT"]
        corridors.CORRIDORS["QAR-BDT"] = replace(c, delivery_methods=(*c.delivery_methods, "cash_pickup"))
    else:  # pragma: no cover - the grader only passes known ids
        raise KeyError(mutant)


def pytest_configure(config):
    mutant = os.environ.get("M14_MUTANT", "")
    if not mutant:
        return
    try:
        _mutate(mutant)
    except Exception:  # the learner's structure is different: tell the grader instead of failing the tests
        import pytest

        pytest.exit(f"m14 mutant {mutant!r} could not be applied", returncode=NOT_APPLIED)
