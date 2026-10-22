"""A pytest plugin that breaks the limit warning in one deliberate way, chosen by AILAB_M04_MUTANT.

Used only by the m04 grader (``ailab/checks_m04.py``), in a subprocess, on a throw-away copy of the learner's
repository. It never changes a file: it patches the *running* program at its public edges (what
``render`` returns, what the notifier delivers, the daily limits), so it works on any sound implementation
whatever its internal structure. The learner's new tests are then run: a mutant is "killed" when at least
one of them fails.

    control            nothing is changed (proves the plugin itself loads and the tests pass with it)
    drop               the warning is never delivered
    blank              the warning text keeps no numbers
    percent_plus_one   the percentage shown is one too high (as if it were rounded up)
    english_only       Arabic customers get the English text
    western_digits     Arabic text shows Western digits
    line_up            the 80% line sits a little too high (daily limits 1% larger)
    line_down          the 80% line sits a little too low (daily limits 1% smaller)
"""
from __future__ import annotations

import os
import re
from decimal import Decimal

MUTANT = os.environ.get("AILAB_M04_MUTANT", "control")
WARNING = "limit_warning"
ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"
WESTERN_DIGITS = "0123456789"


def _percent_plus_one(text: str) -> str:
    """Add one to the first whole number that is followed by a percent sign (Western or Arabic digits)."""

    def bump(match: re.Match[str]) -> str:
        digits = match.group(1)
        arabic = digits[0] in ARABIC_DIGITS
        value = int(digits.translate(str.maketrans(ARABIC_DIGITS, WESTERN_DIGITS))) + 1
        shown = str(value)
        return (shown.translate(str.maketrans(WESTERN_DIGITS, ARABIC_DIGITS)) if arabic else shown) + match.group(2)

    return re.sub(r"([0-9٠-٩]+)(\s?[%٪])", bump, text, count=1)


def _patch_render(mutant: str) -> None:
    from remit import notify
    from remit.errors import NotificationError

    original = notify.render

    def render(template_id, lang, **values):
        if template_id != WARNING:
            return original(template_id, lang, **values)
        if mutant == "drop":
            raise NotificationError("the warning could not be delivered")
        if mutant == "english_only":
            return original(template_id, "en", **values)
        text = original(template_id, lang, **values)
        if mutant == "blank":
            return "Please check your daily limit."
        if mutant == "percent_plus_one":
            return _percent_plus_one(text)
        if mutant == "western_digits" and lang == "ar":
            return text.translate(str.maketrans(ARABIC_DIGITS, WESTERN_DIGITS))
        return text

    notify.render = render


def _patch_limits(factor: Decimal) -> None:
    from remit import limits

    for tier, tier_limits in list(limits.LIMITS.items()):
        limits.LIMITS[tier] = limits.TierLimits(daily=tier_limits.daily * factor, monthly=tier_limits.monthly)


def apply(mutant: str) -> None:
    if mutant in ("drop", "blank", "percent_plus_one", "english_only", "western_digits"):
        _patch_render(mutant)
    elif mutant == "line_up":
        _patch_limits(Decimal("1.01"))
    elif mutant == "line_down":
        _patch_limits(Decimal("0.99"))
    elif mutant != "control":
        raise RuntimeError(f"unknown mutant {mutant!r}")


apply(MUTANT)
