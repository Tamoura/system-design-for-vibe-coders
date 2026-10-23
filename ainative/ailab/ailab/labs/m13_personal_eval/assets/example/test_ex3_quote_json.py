"""Check for example task EX3: `python -m remit quote ... --json` prints one JSON object and nothing else."""
import io
import json
from datetime import datetime, timezone

from najmkit.clock import FixedClock
from remit.cli import main

NOW = FixedClock(datetime(2026, 3, 2, 9, 0, tzinfo=timezone.utc))


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    code = main(list(argv), out=out, err=err, clock=NOW)
    return code, out.getvalue(), err.getvalue()


def test_a_json_quote_has_the_agreed_keys_and_exact_decimals():
    code, out, _ = run("quote", "QAR", "500", "INR", "--json")
    data = json.loads(out)  # fails if there is anything but one JSON document on the output
    assert code == 0
    assert data["send_amount"] == "500.00"
    assert data["fee"] == "12.00"
    assert data["total"] == "512.00"
    assert data["rate"] == "22.5720"
    assert data["receive_amount"] == "11286.00"
    assert data["delivery_method"] == "bank_deposit"


def test_the_express_fee_and_the_delivery_method_follow_the_options():
    _, out, _ = run("quote", "QAR", "500", "INR", "--express", "--delivery", "wallet", "--json")
    data = json.loads(out)
    assert data["fee"] == "27.00" and data["delivery_method"] == "wallet"


def test_without_the_flag_the_output_is_unchanged():
    _, out, _ = run("quote", "QAR", "500", "INR")
    assert out.splitlines()[0] == "Corridor:  QAR -> INR"
    assert out.splitlines()[2] == "Fee:       12.00 QAR"
