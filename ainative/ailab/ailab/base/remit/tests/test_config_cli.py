import io

import pytest

from najmkit import audit
from remit.cli import main
from remit.config import Config, load_config


def run(*argv, environ=None, clock=None):
    out, err = io.StringIO(), io.StringIO()
    code = main(list(argv), environ=environ, clock=clock, out=out, err=err)
    return code, out.getvalue(), err.getvalue()


def test_config_defaults_and_overrides():
    assert load_config({}) == Config()
    config = load_config({"REMIT_ENV": "test", "REMIT_DB": "/tmp/x.db", "REMIT_AUDIT_LOG": "a.jsonl", "REMIT_LANG": "ar"})
    assert (config.env, config.db_path, config.audit_log, config.language) == ("test", "/tmp/x.db", "a.jsonl", "ar")


def test_bad_config_values_are_rejected():
    for bad in ({"REMIT_ENV": "staging"}, {"REMIT_LANG": "fr"}):
        with pytest.raises(ValueError):
            load_config(bad)


def test_config_reads_the_real_environment_by_default(monkeypatch):
    monkeypatch.setenv("REMIT_DB", "elsewhere.db")
    assert load_config().db_path == "elsewhere.db"


def test_quote_command(clock):
    code, out, err = run("quote", "QAR", "500", "INR", environ={}, clock=clock)
    assert code == 0 and err == ""
    assert out.splitlines() == [
        "Corridor:  QAR -> INR",
        "Send:      500.00 QAR",
        "Fee:       12.00 QAR",
        "Total:     512.00 QAR",
        "Rate:      22.5720 (valid for 60 s)",
        "Receive:   11286.00 INR",
        "Delivery:  bank_deposit",
    ]


def test_quote_errors_exit_with_one_and_a_code(clock):
    code, out, err = run("quote", "QAR", "5", "INR", environ={}, clock=clock)
    assert code == 1 and out == "" and err.startswith("error [amount_out_of_range]")


def test_usage_errors_exit_with_two(clock):
    assert run("quote", environ={}, clock=clock)[0] == 2
    assert run("send", "QAR", "5", environ={}, clock=clock)[0] == 2
    assert run("quote", "QAR", "5", "INR", environ={"REMIT_ENV": "nope"}, clock=clock)[0] == 2
    code, _, err = run("quote", "QAR", "500", "INR", environ={"REMIT_WATCHLIST": "/no/such/file.txt"}, clock=clock)
    assert code == 2 and "cannot read the watchlist" in err


def test_customer_send_and_history_share_a_database_file(tmp_path, clock):
    env = {"REMIT_DB": str(tmp_path / "remit.db"), "REMIT_AUDIT_LOG": str(tmp_path / "audit.jsonl")}
    assert run("customer", "add", "--id", "C001", "--name", "Aisha Rahman", "--kyc", "T2", environ=env, clock=clock)[0] == 0
    code, out, _ = run("send", "--customer", "C001", "QAR", "500", "INR", "--recipient", "Ravi Kumar", environ=env, clock=clock)
    assert code == 0
    assert "Ravi Kumar received 11,286.00 INR" in out  # the console notification
    assert "sent TRF-" in out and "(fee 12.00 QAR)" in out
    code, out, _ = run("history", "--customer", "C001", environ=env, clock=clock)
    assert code == 0 and "QAR-INR  500.00 QAR  fee 12.00 QAR  -> 11286.00 INR  to Ravi Kumar" in out
    assert [e["event"] for e in audit.read_events()] == ["transfer.sent"]
    code, out, _ = run("customer", "list", environ=env, clock=clock)
    assert out.strip() == "C001  Aisha Rahman  T2  none  en"


def test_sending_for_an_unknown_customer_fails_cleanly(tmp_path, clock):
    env = {"REMIT_DB": str(tmp_path / "remit.db")}
    code, _, err = run("send", "--customer", "C404", "QAR", "500", "INR", "--recipient", "Ravi", environ=env, clock=clock)
    assert code == 1 and "unknown_customer" in err
