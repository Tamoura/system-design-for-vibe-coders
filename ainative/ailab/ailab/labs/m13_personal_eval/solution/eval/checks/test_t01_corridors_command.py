"""T01: `python -m remit corridors` lists the corridors, one line each, and touches no database."""
import io

from remit.cli import main


def run(tmp_path, *argv):
    out, err = io.StringIO(), io.StringIO()
    database = tmp_path / "remit.db"
    code = main(list(argv), environ={"REMIT_DB": str(database)}, out=out, err=err)
    return code, out.getvalue(), database


def test_one_line_per_corridor_sorted_by_code(tmp_path):
    code, out, _ = run(tmp_path, "corridors")
    assert code == 0
    assert out.splitlines() == [
        "QAR-EGP  100.00 to 15000.00 QAR",
        "QAR-INR  50.00 to 25000.00 QAR",
        "QAR-PHP  50.00 to 20000.00 QAR",
        "QAR-PKR  100.00 to 15000.00 QAR",
    ]


def test_listing_corridors_does_not_create_a_database_file(tmp_path):
    _, _, database = run(tmp_path, "corridors")
    assert not database.exists()


def test_the_other_commands_still_work(tmp_path):
    code, out, _ = run(tmp_path, "quote", "QAR", "500", "INR")
    assert code == 0 and out.startswith("Corridor:  QAR -> INR")
