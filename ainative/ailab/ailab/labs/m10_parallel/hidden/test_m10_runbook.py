"""Hidden checks for lab m10, task D: the Customer Care runbook (docs/CARE.md).

They look for what the ticket asks for (headings, the commands, example lines that are real output, the
template id and the English wording). Any real corridor line will do, but every corridor line on the page
must be a real one; a usage line must fit the form and add up. They cannot tell a hand-typed line that
happens to be right from a pasted one, nor whether the page is any good to a person on a call.
"""
import re
from decimal import Decimal
from pathlib import Path

import pytest

import remit

ROOT = Path(remit.__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs" / "CARE.md"
REAL_CORRIDOR_LINES = {
    "QAR-EGP: 100.00 to 15000.00 QAR; delivery: bank_deposit (default), wallet; fees: STD-B",
    "QAR-INR: 50.00 to 25000.00 QAR; delivery: bank_deposit (default), wallet; fees: STD-A",
    "QAR-PHP: 50.00 to 20000.00 QAR; delivery: bank_deposit (default), cash_pickup, wallet; fees: STD-A",
    "QAR-PKR: 100.00 to 15000.00 QAR; delivery: bank_deposit (default), cash_pickup; fees: STD-B",
}
USAGE_LINE = re.compile(
    r"^(T[123]): today (\d+\.\d\d) of (\d+\.\d\d) QAR used \((\d+\.\d\d) left\); "
    r"this month (\d+\.\d\d) of (\d+\.\d\d) QAR used \((\d+\.\d\d) left\)$"
)
ENGLISH = "is taking longer than expected"


def sections():
    """Level-2 sections of the runbook: {lower-case title: body}. Headings inside code fences are ignored."""
    if not RUNBOOK.is_file():
        pytest.fail("docs/CARE.md does not exist")
    found, current, fenced = {}, None, False
    for text in RUNBOOK.read_text(encoding="utf-8").splitlines():
        if text.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
        match = None if fenced else re.match(r"##\s+(.*?)\s*$", text)
        if match and not text.startswith("###"):
            current = match.group(1).strip().lower()
            found[current] = ""
        elif current is not None:
            found[current] += text + "\n"
    return found


def section(name):
    """The body of the level-2 section whose title is ``name`` or starts with it (``## Corridors command`` is fine)."""
    for title, body in sections().items():
        if title.startswith(name):
            return body
    pytest.fail(f"docs/CARE.md has no '## {name}' section")


def test_the_runbook_has_its_title_and_the_three_sections():
    assert RUNBOOK.is_file(), "docs/CARE.md does not exist"
    text = RUNBOOK.read_text(encoding="utf-8")
    assert re.search(r"^#\s+Customer Care desk pack\b", text, re.M | re.I)
    for name in ("corridors", "limits", "delay message"):
        section(name)


def has_code_block(body):
    """A fenced block (backticks or tildes) or an indented one."""
    return bool(re.search(r"^\s*(```|~~~)", body, re.M) or re.search(r"^( {4}|\t)\S", body, re.M))


def test_the_corridors_section_has_the_command_and_real_output():
    body = section("corridors")
    assert re.search(r"-m\s+remit\s+corridors", body), "the command is missing"
    assert has_code_block(body), "the example is not in a code block"
    shown = [line.strip() for line in body.splitlines() if re.match(r"\s*QAR-[A-Z]{3}: ", line)]
    assert shown, "no corridor line from the program's output"
    typed = [line for line in shown if line not in REAL_CORRIDOR_LINES]
    assert not typed, f"not what the program prints: {typed}"


def test_the_limits_section_has_the_command_and_a_real_usage_line():
    from remit.limits import limits_for

    body = section("limits")
    assert re.search(r"-m\s+remit\s+limits\s+--customer", body), "the command is missing"
    assert has_code_block(body), "the example is not in a code block"
    shown = [line.strip() for line in body.splitlines() if re.match(r"\s*T[0-9]:", line)]
    assert shown, "no usage line from the program's output"
    for line in shown:
        match = USAGE_LINE.match(line)
        assert match, f"not the form the program prints: {line}"
        tier, day_used, day_limit, day_left, month_used, month_limit, month_left = match.groups()
        limits = limits_for(tier)
        assert Decimal(day_limit) == limits.daily.amount and Decimal(month_limit) == limits.monthly.amount, line
        assert Decimal(day_left) == max(Decimal(day_limit) - Decimal(day_used), 0), line
        assert Decimal(month_left) == max(Decimal(month_limit) - Decimal(month_used), 0), line
        assert Decimal(day_used) <= Decimal(month_used), line


def test_the_delay_section_names_the_template_and_quotes_the_english_wording():
    body = section("delay message")
    assert "transfer_delayed" in body
    # the wording may be quoted (> ...) and wrapped anywhere
    flat = " ".join(re.sub(r"^\s*>\s?", "", line) for line in body.splitlines())
    assert ENGLISH in re.sub(r"\s+", " ", flat)
