"""KIT_NOTES.md must agree with the code: its generated tables are regenerated and compared."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

from ailab import framework, runner
from conftest import KIT_ROOT

NOTES = KIT_ROOT / "KIT_NOTES.md"
GENERATOR = Path(__file__).resolve().parent / "kit_notes_tables.py"


def test_generated_blocks_are_up_to_date(tmp_path):
    copy = tmp_path / "KIT_NOTES.md"
    shutil.copyfile(NOTES, copy)
    result = runner.run_python([GENERATOR, "--write", copy], cwd=KIT_ROOT,
                               pythonpath=[framework.BASE_REPO / "src", KIT_ROOT])
    assert result.ok, result.output
    assert "is up to date" in result.stdout, (
        "KIT_NOTES.md is out of date. From ainative/ailab run:\n"
        "  PYTHONPATH=ailab/base/remit/src:. python tests/kit_notes_tables.py --write KIT_NOTES.md"
    )


def test_the_generator_output_is_stable_across_hash_seeds(tmp_path):
    outputs = {
        runner.run_python([GENERATOR], cwd=KIT_ROOT, pythonpath=[framework.BASE_REPO / "src", KIT_ROOT],
                          extra_env={"PYTHONHASHSEED": seed}).stdout
        for seed in ("1", "2", "3")
    }
    assert len(outputs) == 1


def test_every_generated_block_is_present_once():
    text = NOTES.read_text(encoding="utf-8")
    for name in ("signatures", "constants", "kit_api"):
        assert text.count(f"<!-- BEGIN GENERATED: {name} -->") == 1 and text.count(f"<!-- END GENERATED: {name} -->") == 1


def test_the_notes_contain_no_machine_specific_paths_in_generated_text():
    text = NOTES.read_text(encoding="utf-8")
    generated = re.findall(r"<!-- BEGIN GENERATED: \w+ -->(.*?)<!-- END GENERATED: \w+ -->", text, re.S)
    assert generated and not any("/home/" in block or "/tmp/" in block for block in generated)


def test_every_quirk_id_in_the_code_is_in_the_notes_and_vice_versa():
    notes = NOTES.read_text(encoding="utf-8")
    base = framework.BASE_REPO
    code = "\n".join(p.read_text(encoding="utf-8") for p in (base / "src").rglob("*.py"))
    docs = "\n".join(p.read_text(encoding="utf-8") for p in (base / "docs").glob("*.md"))
    in_code = set(re.findall(r"\b[QS]-[A-Z]+-\d\b", code))
    assert in_code == {f"Q-LED-{i}" for i in range(1, 5)} | {f"Q-SCR-{i}" for i in range(1, 5)} | {"S-STORE-1"}
    for ident in in_code:
        assert f"**{ident}**" in notes, f"{ident} is in the code but not in the notes register"
    # ids the notes introduce for docs and gaps
    for ident in ("D-ARCH-1", "D-ARCH-2", "D-SVC-1", "G-BDT", "G-WARN", "G-LOYALTY", "G-V2", "G-ADR", "I-SVC-1", "I-SCR-1"):
        assert f"**{ident}**" in notes, ident
    assert "D-SVC-1" not in docs  # the doc states the limitation in prose, without kit ids
    assert not re.search(r"\b[QDGIS]-[A-Z]+-\d\b", docs), "kit ids must not leak into the learner-facing docs"


def test_every_public_kit_function_is_listed_in_the_notes():
    from ailab import checks, framework as fw, gitutil

    notes = NOTES.read_text(encoding="utf-8")
    for module in (checks, fw, gitutil):
        for name, value in vars(module).items():
            if not name.startswith("_") and callable(value) and getattr(value, "__module__", None) == module.__name__:
                assert re.search(rf"\b{name}\b", notes), f"{module.__name__}.{name} is not documented in KIT_NOTES.md"
