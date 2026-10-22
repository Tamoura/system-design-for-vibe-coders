"""Hidden checks for lab m10, task D: the Customer Care runbook (docs/CARE.md).

They look for what the ticket asks for (headings, the commands, a real output line, the template
id and the English wording). They cannot tell whether the page is any good to a person on a call.
"""
import re
from pathlib import Path

import pytest

import remit

ROOT = Path(remit.__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs" / "CARE.md"
QAR_INR = "QAR-INR: 50.00 to 25000.00 QAR; delivery: bank_deposit (default), wallet; fees: STD-A"
ENGLISH = "is taking longer than expected"


def sections():
    """Level-2 sections of the runbook: {lower-case title: body}. Headings inside code fences are ignored."""
    if not RUNBOOK.is_file():
        pytest.fail("docs/CARE.md does not exist")
    found, current, fenced = {}, None, False
    for text in RUNBOOK.read_text(encoding="utf-8").splitlines():
        if text.lstrip().startswith("```"):
            fenced = not fenced
        match = None if fenced else re.match(r"##\s+(.*?)\s*$", text)
        if match and not text.startswith("###"):
            current = match.group(1).strip().lower()
            found[current] = ""
        elif current is not None:
            found[current] += text + "\n"
    return found


def test_the_runbook_has_its_title_and_the_three_sections():
    assert RUNBOOK.is_file(), "docs/CARE.md does not exist"
    text = RUNBOOK.read_text(encoding="utf-8")
    assert re.search(r"^#\s+Customer Care desk pack\s*$", text, re.M | re.I)
    assert {"corridors", "limits", "delay message"} <= set(sections())


def test_the_corridors_section_has_the_command_and_a_real_output_line():
    body = sections()["corridors"]
    assert "python -m remit corridors" in body
    assert "```" in body
    assert QAR_INR in body


def test_the_limits_section_has_the_command_and_an_example():
    body = sections()["limits"]
    assert "python -m remit limits --customer" in body
    assert "```" in body
    assert "QAR used" in body, "the example should be a line copied from the real output"


def test_the_delay_section_names_the_template_and_quotes_the_english_wording():
    body = sections()["delay message"]
    assert "transfer_delayed" in body
    assert ENGLISH in body
