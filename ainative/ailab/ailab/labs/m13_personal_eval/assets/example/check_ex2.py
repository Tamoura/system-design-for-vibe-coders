# ailab/labs/m13_personal_eval/assets/example/check_ex2.py
"""Example EX2: does ANSWER.md say what the code does? Until the tool writes it, reading the file fails."""
import pathlib
import re
import sys

answer = pathlib.Path("ANSWER.md").read_text(encoding="utf-8").lower()
wanted = [
    ("names the express surcharge", "express" in answer and "surcharge" in answer),
    ("says it is added after the cap", re.search(r"after the cap|after[^.]{0,25}\bcap(?:ped|ping)\b|on top of the cap|beyond the cap", answer) is not None),
    ("says the fee can pass the cap", re.search(r"exceed|above the cap|over the cap|past the cap|higher than the cap|more than the cap", answer) is not None),
]
missing = [what for what, ok in wanted if not ok]
if missing:
    sys.exit("the answer does not say: " + "; ".join(missing))
