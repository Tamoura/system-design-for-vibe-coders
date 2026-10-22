"""T04: does ANSWER.md say what happens to the ledger postings when saving the transfer fails?"""
import pathlib
import re
import sys

answer = pathlib.Path("ANSWER.md").read_text(encoding="utf-8").lower()
wanted = [
    ("says the ledger postings were already made", "ledger" in answer and re.search(r"already|before|earlier", answer) is not None),
    ("says they are not reversed", re.search(r"not (be )?(reversed|undone|rolled back)|nothing undoes|stay|remain|still posted", answer) is not None),
    ("names the failing step (store or save_transfer)", "save_transfer" in answer or "store" in answer),
]
missing = [what for what, ok in wanted if not ok]
if missing:
    sys.exit("the answer does not say: " + "; ".join(missing))
