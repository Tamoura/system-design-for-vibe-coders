"""Mask personal data and secrets in a log before it goes into a prompt.

usage:  python redact_log.py < raw.log > safe.log      (what was masked is counted on stderr)

A safety net, not a guarantee: no regular expression recognises a name or a free-text note.
Read the result before you paste it.
"""
import re
import sys

CARD = re.compile(r"\b\d(?:[ -]?\d){12,18}\b")  # 13 to 19 digits; masked only if the Luhn check passes

RULES = [
    ("email", re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"), "<email>"),
    ("bearer", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{16,}"), "Bearer <token>"),
    ("key", re.compile(r"\b(?:sk|pk|rk)[-_](?:live|test)[-_][A-Za-z0-9_-]{12,}|\bAKIA[0-9A-Z]{16}\b"), "<key>"),
    ("iban", re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b"), "<iban>"),
    ("phone", re.compile(r"\+\d{1,3}[ -]?\d[\d -]{6,12}\d"), "<phone>"),
    ("national id", re.compile(r"\b[23]\d{10}\b"), "<national-id>"),
]


def luhn_ok(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        n = int(ch) * (2 if i % 2 else 1)
        total += n - 9 if n > 9 else n
    return total % 10 == 0


def redact(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    for name, pattern, mask in RULES:
        text, n = pattern.subn(mask, text)
        if n:
            counts[name] = n

    def card(match: re.Match) -> str:
        digits = re.sub(r"\D", "", match.group(0))
        if luhn_ok(digits):
            counts["card"] = counts.get("card", 0) + 1
            return "<card>"
        return match.group(0)

    return CARD.sub(card, text), counts


if __name__ == "__main__":
    safe, found = redact(sys.stdin.read())
    sys.stdout.write(safe)
    print("masked: " + (", ".join(f"{k} x{v}" for k, v in sorted(found.items())) or "nothing"), file=sys.stderr)
