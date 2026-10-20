# labs/m06/check_notes.py
"""Check that discovery notes quote their sources.   python labs/m06/check_notes.py docs/discovery-notes.md
A citation is [Y-10 "call-back"]: a turn id, then two or more words copied from that turn. Every REQ, RISK, CON or Q line needs one, on that same line.
Exit 0 = clean. It checks that a quote is REAL; it cannot check that your reading of it is right."""
import re
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "labkit/data"
TURN = re.compile(r"^\[([HYA]-\d+)\]\s*(.*)$")                   # a source line:  [Y-10] text
CITE = re.compile(r'\[([HYA]-\d+)\s+"([^"]+)"\]')                # a citation:     [Y-10 "text"]
ITEM = re.compile(r"^\s*(?:[-*]\s*)?\*{0,2}(?:REQ|RISK|CON|Q)-\d+")   # a line you must defend, bullet or not


def norm(s: str) -> str:
    return " ".join(re.sub(r"\W+", " ", s.lower()).split())      # ignore case, punctuation and spacing


def load_turns() -> dict[str, str]:
    """{turn id: text} from the three source files."""
    names = ("m06_interview_hind.md", "m06_interview_yara.md", "m06_as_is_process.md")
    return {m[1]: m[2] for n in names for x in (DATA / n).read_text(encoding="utf-8").splitlines() if (m := TURN.match(x))}


def check(notes: str, turns: dict[str, str]) -> list[str]:
    found = []
    for n, line in enumerate(notes.splitlines(), 1):
        cites = CITE.findall(line)
        if ITEM.match(line) and not cites:
            found.append(f"line {n}: no citation (source it, or turn it into a question)")
        for tid, quote in cites:
            q = norm(quote)
            if tid not in turns:
                found.append(f"line {n}: there is no turn {tid}")
            elif " " not in q or f" {q} " not in f" {norm(turns[tid])} ":          # whole words, at least two
                found.append(f"line {n}: {tid} does not say \"{quote}\" (two or more whole words)")
    return found


if __name__ == "__main__":
    text, turns = Path(sys.argv[1]).read_text(encoding="utf-8"), load_turns()
    problems = check(text, turns)
    print("\n".join(problems) or "every citation checks out")
    cited = {t for t, _ in CITE.findall(text)}
    print("not cited yet, read again:", *(t for t, x in turns.items() if t not in cited and not x.startswith("**You:**")))
    sys.exit(1 if problems else 0)
