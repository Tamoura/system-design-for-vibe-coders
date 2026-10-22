"""T08: did the review of review/PR-482.diff find the two real problems?"""
import pathlib
import re
import sys

review = pathlib.Path("REVIEW.md").read_text(encoding="utf-8").lower()
wanted = [
    ("the limit boundary: reaching the limit exactly must stay allowed",
     re.search(r"exactly|equal to|boundary|off-by-one|>=|inclusive|reaches? the limit", review) is not None),
    ("a customer's name written to the audit trail",
     re.search(r"personal data|\bpii\b|customer_name|customer's name|full name|privacy", review) is not None),
]
missing = [what for what, ok in wanted if not ok]
if missing:
    sys.exit("the review does not mention: " + "; ".join(missing))
