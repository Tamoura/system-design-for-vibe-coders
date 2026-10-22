"""Hidden checks for lab m10: do the four pieces work *together* once they are merged?

Each piece can pass its own tests and still fail here: a lost import, a dropped branch of the
command dispatch, a usage note that lists only one command, an old command that stopped working.
"""


def test_a_support_session_uses_every_command_in_one_database(cli, tmp_path, clock):
    env = {"REMIT_DB": str(tmp_path / "remit.db")}
    assert cli("customer", "add", "--id", "C001", "--name", "Aisha Rahman", "--kyc", "T2", environ=env, clock=clock)[0] == 0
    code, out, _ = cli("send", "--customer", "C001", "QAR", "500", "INR", "--recipient", "Ravi Kumar", environ=env, clock=clock)
    assert code == 0 and "sent TRF-" in out
    code, out, _ = cli("corridors", environ=env, clock=clock)
    assert code == 0 and len(out.splitlines()) == 4
    code, out, _ = cli("limits", "--customer", "C001", environ=env, clock=clock)
    assert code == 0 and "today 500.00 of 10000.00 QAR used (9500.00 left)" in out
    code, out, _ = cli("history", "--customer", "C001", environ=env, clock=clock)
    assert code == 0 and "QAR-INR  500.00 QAR  fee 12.00 QAR  -> 11286.00 INR  to Ravi Kumar" in out
    code, out, _ = cli("customer", "list", environ=env, clock=clock)
    assert code == 0 and out.strip() == "C001  Aisha Rahman  T2  none  en"


def test_the_commands_that_were_already_there_print_what_they_always_printed(cli, clock):
    code, out, err = cli("quote", "QAR", "500", "INR", environ={}, clock=clock)
    assert (code, err) == (0, "")
    assert out.splitlines() == [
        "Corridor:  QAR -> INR",
        "Send:      500.00 QAR",
        "Fee:       12.00 QAR",
        "Total:     512.00 QAR",
        "Rate:      22.5720 (valid for 60 s)",
        "Receive:   11286.00 INR",
        "Delivery:  bank_deposit",
    ]
    assert cli("quote", "QAR", "5", "INR", environ={}, clock=clock)[0] == 1
    assert cli("send", "QAR", "5", environ={}, clock=clock)[0] == 2


def test_the_help_lists_both_new_commands(cli, clock, capsys):
    cli("--help", environ={}, clock=clock)
    shown = capsys.readouterr().out
    assert "corridors" in shown and "limits" in shown
    assert all(old in shown for old in ("customer", "quote", "send", "history"))


def test_the_usage_note_at_the_top_of_cli_py_lists_both_new_commands():
    import remit.cli

    note = remit.cli.__doc__ or ""
    assert "python -m remit corridors" in note
    assert "python -m remit limits --customer" in note
    assert "python -m remit history --customer" in note


def test_a_new_command_never_falls_through_into_the_transfer_code(cli, tmp_path, clock):
    # `quote` and `send` read args.amount; the new commands have no such argument.
    env = {"REMIT_DB": str(tmp_path / "remit.db")}
    cli("customer", "add", "--id", "C001", "--name", "Aisha Rahman", "--kyc", "T2", environ=env, clock=clock)
    for argv in (("corridors",), ("corridors", "QAR-INR"), ("limits", "--customer", "C001")):
        code, out, err = cli(*argv, environ=env, clock=clock)
        assert code == 0 and out and "Traceback" not in err, argv
