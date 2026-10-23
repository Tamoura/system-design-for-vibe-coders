"""Hidden checks for lab m10, task B: ``corridors.describe`` and the ``corridors`` command."""
from remit.money import Money

LINES = {
    "QAR-EGP": "QAR-EGP: 100.00 to 15000.00 QAR; delivery: bank_deposit (default), wallet; fees: STD-B",
    "QAR-INR": "QAR-INR: 50.00 to 25000.00 QAR; delivery: bank_deposit (default), wallet; fees: STD-A",
    "QAR-PHP": "QAR-PHP: 50.00 to 20000.00 QAR; delivery: bank_deposit (default), cash_pickup, wallet; fees: STD-A",
    "QAR-PKR": "QAR-PKR: 100.00 to 15000.00 QAR; delivery: bank_deposit (default), cash_pickup; fees: STD-B",
}


def test_describe_writes_the_agreed_line_for_every_corridor():
    from remit.corridors import CORRIDORS, describe

    assert {code: describe(corridor) for code, corridor in CORRIDORS.items()} == LINES


def test_describe_works_for_any_corridor_not_only_the_shipped_ones():
    from remit.corridors import Corridor, describe

    other = Corridor("QAR", "LKR", Money("75", "QAR"), Money("12000.5", "QAR"), ("wallet",), "STD-B")
    assert describe(other) == "QAR-LKR: 75.00 to 12000.50 QAR; delivery: wallet (default); fees: STD-B"
    reordered = Corridor("QAR", "NPR", Money("20", "QAR"), Money("900", "QAR"), ("cash_pickup", "wallet", "bank_deposit"), "STD-A")
    assert describe(reordered) == "QAR-NPR: 20.00 to 900.00 QAR; delivery: cash_pickup (default), wallet, bank_deposit; fees: STD-A"


def test_the_command_lists_every_corridor_in_code_order(cli, tmp_path, clock):
    code, out, err = cli("corridors", environ={"REMIT_DB": str(tmp_path / "remit.db")}, clock=clock)
    assert (code, err) == (0, "")
    assert out.splitlines() == [LINES[c] for c in sorted(LINES)]


def test_the_command_prints_one_corridor_when_given_its_code(cli, tmp_path, clock):
    code, out, err = cli("corridors", "QAR-PKR", environ={"REMIT_DB": str(tmp_path / "remit.db")}, clock=clock)
    assert (code, err) == (0, "")
    assert out.splitlines() == [LINES["QAR-PKR"]]


def test_an_unknown_code_exits_with_one_and_names_the_error(cli, tmp_path, clock):
    code, out, err = cli("corridors", "QAR-XYZ", environ={"REMIT_DB": str(tmp_path / "remit.db")}, clock=clock)
    assert code == 1 and out == ""
    assert err.startswith("error [")  # the CLI's own form, "error [code]: message"; the natural code is unknown_corridor


def test_the_command_reads_no_data_so_it_creates_no_database_file(cli, tmp_path, clock):
    database = tmp_path / "remit.db"
    cli("corridors", environ={"REMIT_DB": str(database)}, clock=clock)
    cli("corridors", "QAR-INR", environ={"REMIT_DB": str(database)}, clock=clock)
    assert not database.exists()
