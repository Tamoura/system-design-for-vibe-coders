"""Helpers that only lab m03 uses (kept out of ``checks.py``, which belongs to the kit): the spec reader and the checks
behind lesson 3.2, "turn three vague tickets into specs an agent can build from".

What the lab asks for
---------------------
Three vague tickets (``lab-assets/tickets/T1.md`` to ``T3.md``) become three specs (``specs/T1.md`` to ``T3.md``), each
written on ``specs/TEMPLATE.md``: Goal, Context, Behaviour, Acceptance criteria, Constraints, Non-goals, Decisions and
open questions, Risks, Test plan and Plan. Nothing is built: a spec lab that ends with an edited ``src/`` has failed.

How a spec is read
------------------
No model reads it. The grader is a set of mechanical questions, each of which a reviewer could also ask:

* Are the sections there, and is there something under each of them?                    (``section_problems``)
* Are the placeholders gone, and is there no filler?                                      (``placeholder_problems``, ``filler_problems``)
* Does Behaviour show worked examples with exact numbers or instants?                     (``example_problems``)
* Is every acceptance criterion *checkable*: does it hold a value, a code name or a quoted text a test could compare,
  and is it free of "works properly"?                                                      (``criteria_problems``)
* Do the files it names exist (or are they marked new)? Does it name real code and real tests?  (``file_problems``)
* Is each ticket's list of **hidden ambiguities** resolved?                              (``resolution``)
* Do the decisions agree with the house rules in CONTRIBUTING.md?                         (``rule_problems``)
* Is the plan a short numbered list of small steps, test first, with a check and a rollback?     (``plan_size_problems``, ``plan_shape_problems``)

Resolving an ambiguity, as the grader sees it
---------------------------------------------
Every ticket hides a handful of questions (rounding, a boundary, a currency, a time zone, Arabic wording ...). For each,
the kit holds one or more *parts*: a few groups of alternative keywords, written to be tolerant of wording. A part is met
by a **segment** of the spec: one list item, table row, paragraph or code line (long paragraphs also give two-sentence
windows), with its questions removed (a question is not a decision), at least five words long, in which every group has a
keyword. One segment can resolve only one part of the lab: a line of keywords cannot resolve everything, and the
ambiguity must be *answered*, not asked. Nothing here checks that the answer is a good one; the lesson says so.

What the grader cannot tell
---------------------------
Whether a decision is right for the bank, whether the Arabic is good Arabic, whether the examples are correct, whether you
understood any of it, or who wrote the file. It checks the shape of a spec an agent can build from and the facts that can be
checked against the repository. Usefulness is what the group session and the optional "ambiguity audit" are for.
"""
from __future__ import annotations

import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

from ailab import checks
from ailab.framework import Check

# ---------------------------------------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------------------------------------
TICKETS = ("T1", "T2", "T3")
SPEC_DIR = "specs"
TEMPLATE_FILE = f"{SPEC_DIR}/TEMPLATE.md"
LOG_FILE = "agent-log.md"
ALLOWED_FILES = (f"{SPEC_DIR}/**", LOG_FILE)

MIN_SEGMENT_WORDS = 5
WINDOW_AFTER_WORDS = 45  # a paragraph longer than this also yields two-sentence windows
MIN_CRITERIA = 4
MIN_EXAMPLES = 3
MIN_CONSTRAINTS = 3
MIN_NONGOALS = 2
MIN_DECISIONS = 3
MIN_STEPS = 4
MAX_STEPS = 10
MAX_STEP_WORDS = 45
MAX_STEP_FILES = 3

# Check names (the tests refer to them, so they are constants).
N_SCOPE = "Only specs and the agent log changed"
N_TESTS = "The repository's tests still pass"
N_EXIST = "All three specs exist"
N_SECTIONS = "Required sections are present"
N_PLACEHOLDERS = "No placeholders are left"
N_FILLER = "No filler"
N_EXAMPLES = "Behaviour has worked examples"
N_CRITERIA = "Acceptance criteria are checkable"
N_LISTS = "Constraints, non-goals, decisions are lists"
N_FILES = "Named files exist"
N_RULES = "Decisions follow the house rules"
N_REVIEW = "Money-logic specs name a second reviewer"
N_PLAN_SIZE = "Plans are small numbered steps"
N_PLAN_SHAPE = "Plans go test first, run pytest, roll back"
N_DISTINCT = "The specs are not copies"
N_RISKS = "Each spec names its risks"
N_LOG = "Your agent log has an entry (optional)"
N_COMMITS = "Commit messages follow CONTRIBUTING.md"
N_CLEAN = "Everything is committed (nothing left over)"


def n_ambiguities(ticket: str) -> str:
    return f"{ticket}: hidden questions answered"


WAITING = "waiting for {}"


def _waiting(missing: Sequence[str]) -> str:
    return "no specs yet" if len(missing) == len(TICKETS) else WAITING.format(_short(missing))

# ---------------------------------------------------------------------------------------------------------
# small text tools
# ---------------------------------------------------------------------------------------------------------
_WORD = re.compile(r"\S+")
_ARABIC_WORD = re.compile(r"[\u0621-\u064a\u064b-\u0652\u0671-\u06d3]{2,}")
_QUESTION = re.compile(r"[?\u061f]")
# A sentence ends at . ! ? (or the Arabic question mark), optionally followed by a closing quote or bracket, then a space.
_SENTENCE_END = re.compile(r"(?<=[.!?\u061f])[\"')\]\u201d\u2019]*\s+")


def split_sentences(text: str) -> list[str]:
    """Sentences of a block; emphasis marks are removed first, so that "**Rounding?** Half up." splits after the question."""
    return [part for part in _SENTENCE_END.split(text.replace("*", "")) if part]
_EXAMPLE_TOKEN = re.compile(r"\d[\d,]*\.\d{2}\b|\b\d{1,2}:\d{2}\b|\d{4}-\d{2}-\d{2}|[\u0660-\u0669]{2,}")
_NUMBER = re.compile(r"\d|[\u0660-\u0669]")
_ANCHOR = re.compile(r"\d|[\u0660-\u0669]|`[^`\n]+`|\"[^\"\n]{3,}\"|\u201c[^\u201d\n]{3,}\u201d|\u00ab[^\u00bb\n]{3,}\u00bb|[\u0621-\u064a]{3,}")


def words(text: str) -> int:
    return len(_WORD.findall(text))


def arabic_words(text: str) -> int:
    return len(_ARABIC_WORD.findall(text))


def _norm_title(title: str) -> str:
    title = re.sub(r"[`*_]", "", title).strip().lower()
    return re.sub(r"^[^a-z]+", "", title)  # numbering, emoji and punctuation before the first letter


def _short(items: Sequence[str], limit: int = 3) -> str:
    return checks._short(list(items), limit)  # noqa: SLF001 - the kit's own formatter, same style as every check


def _fail(name: str, detail: str, hint: str, required: bool = True) -> Check:
    return Check(name, False, detail, hint, required)


def _ok(name: str, detail: str = "", required: bool = True) -> Check:
    return Check(name, True, detail, "", required)


# ---------------------------------------------------------------------------------------------------------
# blocks: the units the grader reads (list items, table rows, paragraphs, code lines)
# ---------------------------------------------------------------------------------------------------------
_FENCE = re.compile(r"^\s*(```+|~~~+)")
_HEADING = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
_LIST = re.compile(r"^(\s*)(?:[-*+]|\d+[.)])\s+(?:\[[ xX]\]\s+)?(\S.*)$")
_ROW = re.compile(r"^\s*\|(.*)\|\s*$")
_SEPARATOR = re.compile(r"^[\s:|-]+$")
_GWT = re.compile(r"^\s*(given|when|then|and|but)\b", re.I)
_GWT_CONTINUES = re.compile(r"^\s*(when|then|and|but)\b", re.I)


@dataclass
class Block:
    text: str
    kind: str  # "item" | "row" | "para" | "code"
    indent: int = 0


def blocks(text: str) -> list[Block]:
    """The blocks of a Markdown text. A heading of level 3 or deeper is glued to the block that follows it, so that a
    decision written as a sub-section ("### Express surcharge" and a paragraph) still reads as one statement."""
    lines = text.splitlines()
    out: list[Block] = []
    current: Block | None = None
    fence: str | None = None
    heading: str | None = None

    def flush() -> None:
        nonlocal current
        if current is not None:
            out.append(current)
            current = None

    def prefixed(body: str) -> str:
        nonlocal heading
        if heading:
            body, heading = f"{heading}: {body}", None
        return body

    for index, raw in enumerate(lines):
        line = raw.rstrip()
        fence_match = _FENCE.match(line)
        if fence_match:
            flush()
            marker = fence_match.group(1)[:3]
            fence = marker if fence is None else (None if line.strip().startswith(fence) else fence)
            continue
        if fence is not None:
            if line.strip():
                out.append(Block(prefixed(line.strip()), "code"))
            continue
        if not line.strip():
            flush()
            continue
        heading_match = _HEADING.match(line)
        if heading_match:
            flush()
            heading = heading_match.group(2) if len(heading_match.group(1)) >= 3 else None
            continue
        row = _ROW.match(line)
        if row:
            flush()
            if _SEPARATOR.match(row.group(1)):
                continue
            following = lines[index + 1].strip() if index + 1 < len(lines) else ""
            separator = _ROW.match(following)
            if separator and _SEPARATOR.match(separator.group(1)):
                continue  # the header row of a table is not a statement
            cells = [cell.strip() for cell in row.group(1).split("|")]
            out.append(Block(prefixed(" | ".join(cells)), "row"))
            continue
        item = _LIST.match(line)
        if item:
            flush()
            current = Block(prefixed(item.group(2).strip()), "item", len(item.group(1)))
            continue
        if current is not None:
            current.text += " " + line.strip()
        else:
            current = Block(prefixed(line.strip()), "para")
    flush()
    return out


def list_items(text: str) -> list[str]:
    """The items of a section: list items and table rows (Given / When / Then lines are joined into one item). A section
    written as plain paragraphs gives its sentences instead."""
    found = [b for b in blocks(text) if b.kind in ("item", "row")]
    items: list[str] = []
    for block in found:
        if items and _GWT_CONTINUES.match(block.text) and _GWT.match(items[-1]) and block.kind == "item":
            items[-1] += " " + block.text
        else:
            items.append(block.text)
    if items:
        return items
    sentences: list[str] = []
    for block in blocks(text):
        sentences += [s for s in split_sentences(block.text) if words(s) >= 4]
    return sentences


def statements(block: Block) -> str:
    """The block without its questions: a question is not a decision."""
    parts = block.text.split(" | ") if block.kind == "row" else [block.text]
    kept: list[str] = []
    for part in parts:
        kept += [s for s in split_sentences(part) if not _QUESTION.search(s)]
    return " ".join(kept)


# ---------------------------------------------------------------------------------------------------------
# the spec: sections
# ---------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class SectionRule:
    key: str
    pattern: re.Pattern[str]
    min_words: int
    required: bool = True


# Order matters: "Test plan" must claim its heading before "Plan" looks for one.
SECTION_RULES: tuple[SectionRule, ...] = (
    SectionRule("Test plan", re.compile(r"^(test plan|tests?|verification)\b"), 12),
    SectionRule("Plan", re.compile(r"^(plan|implementation plan)\b"), 25),
    SectionRule("Goal", re.compile(r"^(goal|objective|outcome|purpose)\b"), 8),
    SectionRule("Context", re.compile(r"^(context|background)\b"), 15),
    SectionRule("Behaviour", re.compile(r"^(behaviou?r|examples?|scenarios?|worked examples?)\b"), 30),
    SectionRule("Acceptance criteria", re.compile(r"^acceptance\b"), 30),
    SectionRule("Constraints", re.compile(r"^constraints?\b"), 15),
    SectionRule("Non-goals", re.compile(r"^(non[- ]?goals?|out of scope|not in scope)\b"), 6),
    SectionRule("Decisions", re.compile(r"^(decisions?|open questions?|assumptions?|questions?)\b"), 40),
    SectionRule("Risks", re.compile(r"^risks?\b"), 8, required=False),
)
DISPLAY_ORDER = ("Goal", "Context", "Behaviour", "Acceptance criteria", "Constraints", "Non-goals", "Decisions", "Risks",
                 "Test plan", "Plan")


class Spec:
    """One spec file, read once: its text, its sections (with their sub-sections) and its blocks."""

    def __init__(self, ticket: str, rel: str, text: str) -> None:
        self.ticket = ticket
        self.rel = rel
        self.text = text.lstrip("\ufeff")
        self.outline = checks.markdown_outline(self.text)
        self.sections: dict[str, str] = {}
        claimed: dict[int, str] = {}
        for rule in SECTION_RULES:
            for index, section in enumerate(self.outline):
                if index not in claimed and rule.pattern.match(_norm_title(section.title)):
                    claimed[index] = rule.key
                    break
        for index, key in claimed.items():
            self.sections[key] = self._full_body(index, claimed)

    def _full_body(self, index: int, claimed: dict[int, str]) -> str:
        """The section's own text plus its sub-sections. A heading that is not one of the ten sections and follows it, at
        its own level or deeper (a "Steps" and a "Rollback" under "Plan"), belongs to it."""
        level = self.outline[index].level
        parts = [self.outline[index].body]
        for later_index in range(index + 1, len(self.outline)):
            later = self.outline[later_index]
            if later.level < level or later_index in claimed:
                break
            parts.append(f"{'#' * later.level} {later.title}\n{later.body}")
        return "\n\n".join(parts)

    def blocks(self) -> list[Block]:
        return blocks(self.text)

    def segments(self) -> list[str]:
        """What an ambiguity can be resolved by (see the module docstring)."""
        found: list[str] = []
        for block in self.blocks():
            text = statements(block)
            if words(text) >= MIN_SEGMENT_WORDS or arabic_words(text) >= 4:
                found.append(text)
            if words(text) > WINDOW_AFTER_WORDS:
                sentences = split_sentences(text)
                for first, second in zip(sentences, sentences[1:]):
                    window = f"{first} {second}"
                    if words(window) >= MIN_SEGMENT_WORDS:
                        found.append(window)
        return found

    def sentences(self) -> list[str]:
        out: list[str] = []
        for block in self.blocks():
            out += split_sentences(block.text)
        return out


def load_specs(work: Path) -> dict[str, Spec | None]:
    specs: dict[str, Spec | None] = {}
    for ticket in TICKETS:
        path = Path(work) / SPEC_DIR / f"{ticket}.md"
        try:
            specs[ticket] = Spec(ticket, f"{SPEC_DIR}/{ticket}.md", path.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            specs[ticket] = None
    return specs


# ---------------------------------------------------------------------------------------------------------
# sections, placeholders, filler
# ---------------------------------------------------------------------------------------------------------
def section_problems(spec: Spec) -> list[str]:
    missing, thin = [], []
    for rule in SECTION_RULES:
        if not rule.required:
            continue
        body = spec.sections.get(rule.key)
        if body is None:
            missing.append(rule.key)
        elif words(body) < rule.min_words:
            thin.append(f"{rule.key} ({words(body)} words, at least {rule.min_words})")
    problems = []
    if missing:
        missing.sort(key=DISPLAY_ORDER.index)
        problems.append("missing " + _short(missing))
    if thin:
        problems.append("too short: " + ", ".join(thin))
    return problems


PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME|XXX)\b|lorem ipsum|\bto be decided\b|\bto be determined\b|\u2026{2,}|\.{4,}")


def placeholder_problems(spec: Spec) -> list[str]:
    found = []
    for number, line in enumerate(spec.text.splitlines(), start=1):
        match = PLACEHOLDER.search(line)
        if match:
            found.append(f"line {number}: {match.group(0)}")
    return found


FILLER = (
    ("a vague quality word",
     re.compile(r"\b(user[- ]friendly|intuitive|seamless(?:ly)?|robust|scalable|world[- ]class|state[- ]of[- ]the[- ]art|best[- ]practices?|"
                r"clean code|production[- ]ready|high[- ]quality|easy to use|performant|enterprise[- ]grade|cutting[- ]edge)\b", re.I)),
    ("'works properly' or 'as expected'",
     re.compile(r"\b(?:works?|behaves?|calculated|handled|processed|displayed|shown|rounded)\s+(?:correctly|properly|as expected|appropriately|accurately)\b|"
                r"\bas expected\b|\bproperly\b|\bappropriately\b", re.I)),
    ("'etc.' or 'and so on'", re.compile(r"\betc\b\.?|\band so on\b|\band the like\b|\band more\b", re.I)),
    ("'the system shall'", re.compile(r"\bthe system (?:shall|should be able to|must be able to)\b", re.I)),
    ("consultant words", re.compile(r"\b(leverag\w+|utili[sz]e[sd]?|synerg\w+|holistic|paradigm|streamlin\w+|empower\w*)\b", re.I)),
    ("'handle edge cases'", re.compile(r"\b(?:handle|cover|consider|account for)\s+(?:all |any |the )?edge cases\b|\bedge cases? (?:are|will be) (?:handled|covered)\b", re.I)),
    ("'ensure it works'", re.compile(r"\bensure (?:that )?(?:it|everything|the feature|the system) works\b", re.I)),
)


def filler_problems(spec: Spec) -> list[str]:
    found: dict[str, int] = {}
    for number, line in enumerate(spec.text.splitlines(), start=1):
        for label, pattern in FILLER:
            if label not in found and pattern.search(line):
                found[label] = number
    return [f"{label} (line {number})" for label, number in found.items()]


# ---------------------------------------------------------------------------------------------------------
# behaviour examples and acceptance criteria
# ---------------------------------------------------------------------------------------------------------
def example_problems(spec: Spec) -> list[str]:
    body = spec.sections.get("Behaviour")
    if body is None:
        return ["no Behaviour section"]
    lines = {ln.strip() for ln in body.splitlines() if _EXAMPLE_TOKEN.search(ln) and not ln.strip().startswith("#")}
    if len(lines) < MIN_EXAMPLES:
        return [f"{len(lines)} line(s) with an exact amount, time or date; at least {MIN_EXAMPLES}"]
    return []


_VAGUE = re.compile(
    r"\b(?:works?|behaves?|looks?|feels?|performs?|handled?)\s+(?:well|fine|good|nicely|correctly|properly|as expected)\b|"
    r"\b(?:user[- ]friendly|intuitive|easy to use|easily|fast|quick(?:ly)?|seamless|robust|nice|reasonable|appropriate|good|better|"
    r"correct(?:ly)?|proper(?:ly)?|works?|as (?:required|specified|intended|needed))\b", re.I)
_STRONG = re.compile(r"\d[\d,]*\.\d{2}\b|\b\d{1,2}:\d{2}\b|\d{4}-\d{2}-\d{2}|[\u0660-\u0669]|`[^`\n]+`|\"[^\"\n]{3,}\"|\u201c[^\u201d\n]{3,}\u201d|\u00ab[^\u00bb\n]{3,}\u00bb|[\u0621-\u064a]{3,}")
_OBSERVABLE = re.compile(
    r"\b(?:contains?|ends? with|starts? with|equals?|identical|byte for byte|exactly|unchanged|raises?|returns?|prints?|refus\w+|"
    r"rejects?|rejected|accepted|allowed|matches|is the same as)\b", re.I)


def checkable(item: str) -> bool:
    """An acceptance criterion a test or a command could prove or refute: it holds a value, a code name or a quoted text
    (or says exactly what is compared), is more than a few words, and is not just a vague adjective."""
    if words(item) < 5:
        return False
    if _VAGUE.search(item):
        return bool(_STRONG.search(item))
    return bool(_ANCHOR.search(item) or _OBSERVABLE.search(item))


def criteria_problems(spec: Spec) -> list[str]:
    body = spec.sections.get("Acceptance criteria")
    if body is None:
        return ["no Acceptance criteria section"]
    items = list_items(body)
    problems = []
    if len(items) < MIN_CRITERIA:
        problems.append(f"{len(items)} criteria; at least {MIN_CRITERIA}, one per bullet")
    weak = [item for item in items if not checkable(item)]
    if weak:
        shown = weak[0] if len(weak[0]) <= 70 else weak[0][:67] + "..."
        problems.append(f"{len(weak)} not checkable, for example \"{shown}\"")
    strong = [item for item in items if _EXAMPLE_TOKEN.search(item)]
    if items and len(strong) < 2:
        problems.append("fewer than two criteria carry an exact amount, time or date")
    return problems


def list_problems(spec: Spec) -> list[str]:
    problems = []
    for key, minimum in (("Constraints", MIN_CONSTRAINTS), ("Non-goals", MIN_NONGOALS), ("Decisions", MIN_DECISIONS)):
        body = spec.sections.get(key)
        if body is None:
            problems.append(f"no {key} section")
        elif len(list_items(body)) < minimum:
            problems.append(f"{key}: {len(list_items(body))} item(s); at least {minimum}")
    return problems


# ---------------------------------------------------------------------------------------------------------
# files that the spec names
# ---------------------------------------------------------------------------------------------------------
_PATHISH = re.compile(
    r"(?<![\w/.@~-])(?P<path>(?:src|tests|docs|specs|lab-assets|\.github)/[\w./-]*[\w-]\.(?:py|md|toml|ya?ml|json|txt|cfg|ini))\b|"
    r"(?<![\w/.@~-])(?P<bare>[\w-]+\.(?:py|md|toml|ya?ml|json|txt|cfg|ini))\b")
_CREATION = re.compile(r"\b(new|creat\w*|add(?:s|ed|ing)?|introduc\w*|writ(?:e|es|ing|ten)|start(?:s|ing)? a)\b", re.I)
_GONE = re.compile(r"\b(?:does not|doesn'?t|do not|no longer|not) exist|\bno longer\b|\bstale\b|\bout of date\b|\boutdated\b|\bgone\b|\bremoved\b|\bmissing\b|\bdoes not match\b|\bthere is no\b|\bhas no\b|\bhave no\b", re.I)
_SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".claude", "node_modules"}


def repo_files(work: Path) -> set[str]:
    """Every file in the work directory as a posix path relative to it (no .git, no caches)."""
    found = set()
    for path in Path(work).rglob("*"):
        if path.is_file() and not (_SKIP_DIRS & set(path.relative_to(work).parts)):
            found.add(path.relative_to(work).as_posix())
    return found


def named_files(spec: Spec, files: set[str]) -> tuple[set[str], list[str]]:
    """(the existing files the spec names, the problems: files named as if they existed that do not)."""
    basenames: dict[str, list[str]] = {}
    for rel in files:
        basenames.setdefault(rel.rsplit("/", 1)[-1], []).append(rel)
    real: set[str] = set()
    problems: list[str] = []
    for line in spec.text.splitlines():
        for match in _PATHISH.finditer(line):
            token = match.group("path") or match.group("bare")
            if any(ch in token for ch in "*<>{}"):
                continue
            if match.group("path"):
                found = [token] if token in files else []
            else:
                found = basenames.get(token, [])
            if found:
                real.update(found)
            elif not _CREATION.search(line) and not _GONE.search(line):
                problems.append(token)
    return real, list(dict.fromkeys(problems))


def file_problems(spec: Spec, files: set[str]) -> list[str]:
    real, missing = named_files(spec, files)
    problems = []
    if missing:
        problems.append("names files that do not exist: " + _short(missing, 2))
    if not any(f.startswith("src/") for f in real) or not any(f.startswith("tests/") for f in real):
        problems.append("it must name the real code it will change (src/) and the real tests (tests/)")
    return problems


# ---------------------------------------------------------------------------------------------------------
# the hidden ambiguities
# ---------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Part:
    """One thing a segment must say: every group of alternatives must have a keyword in it. ``arabic`` asks for that many
    Arabic words instead (an Arabic sentence)."""

    groups: tuple[re.Pattern[str], ...] = ()
    arabic: int = 0

    def met_by(self, segment: str) -> bool:
        if self.arabic and arabic_words(segment) < self.arabic:
            return False
        return all(group.search(segment) for group in self.groups)


@dataclass(frozen=True)
class Ambiguity:
    id: str
    family: str  # the family of the lesson's hunting list: only this is ever shown to the learner
    part: Part


def _part(*groups: str, arabic: int = 0) -> Part:
    return Part(tuple(re.compile(g, re.I) for g in groups), arabic)


FEE_PARTS, ROUNDING, BOUNDARIES = "fee parts", "rounding", "boundaries"
CURRENCY, TIME, ARABIC = "currency and corridors", "time and zones", "Arabic"

_DISCOUNT = r"discount|15 ?%|0\.85|0\.15|\boff\b|reduc|saving|waive|offer|promo|rebate|markdown"

AMBIGUITIES: dict[str, tuple[Ambiguity, ...]] = {
    "T1": (
        Ambiguity("express", FEE_PARTS, _part(r"express|surcharge", _DISCOUNT)),
        Ambiguity("minimum", FEE_PARTS, _part(r"minimum|\bmin\b|floor|6\.00|lowest fee|smallest fee", _DISCOUNT)),
        Ambiguity("rounding", ROUNDING, _part(
            r"round|quantize|ROUND_",
            r"half[- ]?up|ROUND_HALF|nearest|0\.01|2 (?:dp|decimal)|two decimal|cents?\b|fils|dirham|\bup\b|\bdown\b|\beven\b",
            r"discount|fee|saving|15 ?%|0\.85")),
        Ambiguity("corridor", CURRENCY, _part(
            r"QAR-EGP|\bEGP\b|Egypt",
            r"\bonly\b|\bjust\b|exclusively|solely|nothing else|other corridors?|\bPKR\b|Pakistan|STD-B|schedule|\bINR\b|\bPHP\b|unchanged|exclud|not apply|every corridor|all corridors|no other")),
    ),
    "T2": (
        Ambiguity("currency", CURRENCY, _part(
            r"\bINR\b|\bPHP\b|\bEGP\b|\bPKR\b|receive currency|receiving currency|recipient'?s? currency|family'?s? currency|destination currency|target currency|payout currency|local currency|rupee|peso|pound",
            r"\bQAR\b|\bdebit|send(?:ing)? currency|customer pays|pays? in|paid in")),
        Ambiguity("direction", ROUNDING, _part(
            r"round|ceil|ROUND_|quantize|next (?:cent|0\.01|fils)|smallest|lowest|search|overshoot|slightly (?:more|less)|a (?:little|bit) (?:more|less)",
            r"\bup\b|ceil|at least|or more|never (?:less|short|below)|no less|not less|more than|rather than|\bdown\b|half[- ]?up|nearest|exact|too much|too little|slightly (?:more|less)|a (?:little|bit) (?:more|less)",
            r"send|QAR|amount|receive|target|family|recipient")),
        Ambiguity("tier", BOUNDARIES, _part(
            r"tier|fees? (?:is |are |will be )?(?:calculated|computed|priced|charged|based|worked out)|priced on|charged on",
            r"boundar|upto|inclusive|whole amount|derived|calculated|500\.0\d|1,?000\.0\d|2,?000\.0\d|5,?000\.0\d|10,?000\.0\d|exactly|edge|crosses?|next tier|jump")),
        Ambiguity("limits", BOUNDARIES, _part(
            r"min_send|max_send|minimum|maximum|\blimit|AmountOutOfRange|out of range|within|outside",
            r"derived|calculated|computed|converted|conversion|QAR (?:send )?amount|send amount|resulting|needs?|requires?|would (?:need|take)")),
    ),
    "T3": (
        Ambiguity("zone", TIME, _part(
            r"Qatar|\bAST\b|UTC ?\+ ?3|\+03:?00|Asia/Qatar|QATAR_TZ|to_local|local time|Manila|Karachi|UTC ?\+ ?[58]|\bPHT\b|\bPKT\b|time ?zone|partner'?s? (?:local )?time",
            r"cut-?off|18:00|6 ?(?:pm|p\.m\.)|6:00|evening|after|before|clock")),
        Ambiguity("boundary", BOUNDARIES, _part(
            r"cut-?off|18:00|6 ?(?:pm|p\.m\.)|6:00",
            r"exactly|inclusive|exclusive|at or after|on or after|up to and including|strictly|17:59|18:00:00|18:00:01|\bsharp\b|boundary|one second|second before|second after|before 18|after 18|from 18")),
        Ambiguity("day", TIME, _part(
            r"tomorrow|next (?:working |business |calendar )?day|following day|next morning",
            r"Friday|Saturday|weekend|working day|business day|calendar day|midnight|same (?:time ?)?zone|Qatar|\blocal\b|\bdate\b|holiday")),
        Ambiguity("scope", CURRENCY, _part(
            r"cash_pickup|cash pickup|pick-?up",
            r"\bonly\b|\bjust\b|exclusively|solely|bank_deposit|bank deposit|wallet|QAR-PHP|QAR-PKR|\bPHP\b|\bPKR\b|\bINR\b|\bEGP\b|not (?:apply|applies|affect)|unchanged|other (?:delivery|methods?|deliver\w+)|no other")),
        Ambiguity("ar-wording", ARABIC, _part(arabic=4)),
        Ambiguity("ar-digits", ARABIC, _part(
            r"Arabic-Indic|Eastern Arabic|localize_digits|format_money|format_number|digits|numerals?|[\u0660-\u0669]",
            r"time|\b6\b|18|cut-?off|message|text|numbers?|name|Latin|unchanged|Western|ASCII|sentence")),
    ),
}


def resolution(ticket: str, spec: Spec) -> dict[str, bool]:
    """Which hidden ambiguities of ``ticket`` the spec resolves: a maximum matching between ambiguities and segments, so
    that one segment resolves at most one of them."""
    ambiguities = AMBIGUITIES[ticket]
    segments = spec.segments()
    candidates = [[i for i, seg in enumerate(segments) if amb.part.met_by(seg)] for amb in ambiguities]
    owner: dict[int, int] = {}

    def assign(a: int, seen: set[int]) -> bool:
        for s in candidates[a]:
            if s in seen:
                continue
            seen.add(s)
            if s not in owner or assign(owner[s], seen):
                owner[s] = a
                return True
        return False

    for a in range(len(ambiguities)):
        assign(a, set())
    matched = set(owner.values())
    return {amb.id: i in matched for i, amb in enumerate(ambiguities)}


def ambiguity_problems(ticket: str, spec: Spec) -> tuple[int, list[str]]:
    """(how many are resolved, the families of those that are not)."""
    solved = resolution(ticket, spec)
    open_families = [amb.family for amb in AMBIGUITIES[ticket] if not solved[amb.id]]
    return sum(solved.values()), open_families


# ---------------------------------------------------------------------------------------------------------
# house rules (CONTRIBUTING.md) and reviewers
# ---------------------------------------------------------------------------------------------------------
_NEGATION = re.compile(
    r"\b(never|not|no|none|don'?t|do not|doesn'?t|without|instead of|avoid|forbid\w*|reject\w*|raises?|TypeError|rather than|must not|"
    r"stdlib|standard library|banned|prohibit\w*)\b", re.I)
_LEDGER = re.compile(r"\bledger\b|\bQ-LED|\bpartner share\b", re.I)
HOUSE_RULES: tuple[tuple[str, re.Pattern[str], str], ...] = (
    ("float money", re.compile(r"\bfloats?\b|\bfloating[- ]point\b|\bround\(", re.I), "Money is Decimal, never float (CONTRIBUTING.md)"),
    ("banker's rounding", re.compile(r"half[- ]even|banker'?s|ROUND_HALF_EVEN", re.I), "Remit rounds half up (CONTRIBUTING.md); the ledger's half-even is a known quirk, not a rule"),
    ("a direct clock or id call", re.compile(r"\bdatetime\.(?:utc)?now\s*\(|\bdate\.today\s*\(|\btime\.time\s*\(|\buuid4?\b|\buuid\.uuid4", re.I),
     "Time and ids come from najmkit and the injected clock (CONTRIBUTING.md)"),
    ("a new dependency", re.compile(r"\bpip install\b|\bpoetry add\b|\buv add\b|\bpytz\b|\bbabel\b|\bdateutil\b|\bpendulum\b|\bpandas\b|\bnumpy\b|"
                                    r"\bimport requests\b|\brequests (?:library|package|module)\b|\bpython-bidi\b|\barabic[-_]reshaper\b|\bforex-python\b", re.I),
     "Standard library only; no new dependency without a ticket (CONTRIBUTING.md)"),
)


def rule_problems(spec: Spec) -> list[tuple[str, str]]:
    found: dict[str, str] = {}
    for sentence in spec.sentences():
        if _NEGATION.search(sentence) or _LEDGER.search(sentence):
            continue
        for label, pattern, hint in HOUSE_RULES:
            if label not in found and pattern.search(sentence):
                found[label] = hint
    return list(found.items())


MONEY_LOGIC = ("money.py", "fees.py", "fx.py", "limits.py", "ledger.py", "service.py")
_SECOND_REVIEWER = re.compile(r"second (?:human )?(?:reviewer|review|approver|person|engineer|pair)|two (?:human )?reviewers|another (?:human )?(?:reviewer|engineer|person)|"
    r"(?:independent|different|additional) (?:human )?(?:reviewer|engineer|person|approver)|four[- ]eyes|(?:other than|besides|in addition to) the author", re.I)


def review_problems(spec: Spec, files: set[str]) -> list[str]:
    real, _ = named_files(spec, files)
    touched = sorted(f for f in real if f.rsplit("/", 1)[-1] in MONEY_LOGIC and f.startswith("src/"))
    if touched and not _SECOND_REVIEWER.search(spec.text):
        return [f"it names {touched[0].rsplit('/', 1)[-1]} but no second human reviewer"]
    return []


# ---------------------------------------------------------------------------------------------------------
# the plan
# ---------------------------------------------------------------------------------------------------------
_STEP = re.compile(r"^\s*(?:\d+[.)]|step\s*\d+\s*[:.)-]|[-*+]\s*\[[ xX]\])\s*(?P<body>\S.*)$", re.I)
_ROLLBACK = re.compile(r"roll ?back|\brevert\b|git restore|git reset|git switch|git checkout|git branch -D|\bundo\b|switch(?:ed)? (?:it )?off|delete the branch", re.I)
_TEST = re.compile(r"\btests?\b|pytest|test_", re.I)
_TEST_WRITE = re.compile(r"\b(?:add|write|create|extend|draft|new|failing|cover|assert|pin)\b", re.I)
_CODE_EDIT = re.compile(r"\b(?:add|change|edit|implement|write|create|update|modify|replace|introduce|extend|wire|refactor|fix|expose|print|raise|apply)\b", re.I)
_READ_ONLY = re.compile(r"^\s*(?:read|open|run|check|review|look|inspect|list|grep|explore|record|create the branch|start a branch|branch)\b", re.I)


def plan_steps(spec: Spec) -> list[str]:
    body = spec.sections.get("Plan", "")
    steps: list[str] = []
    for line in body.splitlines():
        match = _STEP.match(line)
        if match:
            steps.append(match.group("body").strip())
        elif steps and line.startswith("  ") and line.strip() and not _STEP.match(line):
            steps[-1] += " " + line.strip()
    return steps


def _files_in(text: str) -> set[str]:
    return {m.group("path") or m.group("bare") for m in _PATHISH.finditer(text)}


def plan_size_problems(spec: Spec) -> list[str]:
    steps = plan_steps(spec)
    problems = []
    if not MIN_STEPS <= len(steps) <= MAX_STEPS:
        problems.append(f"{len(steps)} numbered steps; between {MIN_STEPS} and {MAX_STEPS} are expected")
    long_steps = [i for i, step in enumerate(steps, start=1) if words(step) > MAX_STEP_WORDS]
    if long_steps:
        problems.append(f"step {long_steps[0]} is {words(steps[long_steps[0] - 1])} words; at most {MAX_STEP_WORDS}")
    broad = [i for i, step in enumerate(steps, start=1) if len(_files_in(step)) > MAX_STEP_FILES]
    if broad:
        problems.append(f"step {broad[0]} touches more than {MAX_STEP_FILES} files")
    vague = [i for i, step in enumerate(steps, start=1) if not (re.search(r"`[^`]+`", step) or _files_in(step) or "pytest" in step)]
    if vague:
        problems.append(f"step {vague[0]} names no file, test or command")
    return problems


def plan_shape_problems(spec: Spec) -> list[str]:
    steps = plan_steps(spec)
    body = spec.sections.get("Plan", "")
    problems = []
    first_test = next((i for i, s in enumerate(steps) if _TEST.search(s) and _TEST_WRITE.search(s)
                       and (re.search(r"tests/|test_", s))), None)
    first_code = next((i for i, s in enumerate(steps)
                       if re.search(r"src/", s) and _CODE_EDIT.search(s) and not _READ_ONLY.search(s)), None)
    if first_test is None:
        problems.append("no step writes a test")
    elif first_code is not None and first_code < first_test:
        problems.append(f"step {first_code + 1} changes the code before step {first_test + 1} writes the test")
    if not any("pytest" in s for s in steps):
        problems.append("no step runs pytest")
    if not _ROLLBACK.search(body):
        problems.append("no rollback")
    return problems


# ---------------------------------------------------------------------------------------------------------
# advisory checks
# ---------------------------------------------------------------------------------------------------------
def _shingles(text: str, size: int = 4) -> set[tuple[str, ...]]:
    tokens = re.findall(r"\w+", text.lower())
    return {tuple(tokens[i:i + size]) for i in range(max(0, len(tokens) - size + 1))}


def similarity(a: str, b: str) -> float:
    sa, sb = _shingles(a), _shingles(b)
    return len(sa & sb) / len(sa | sb) if sa and sb else 0.0


def risk_problems(spec: Spec) -> list[str]:
    body = spec.sections.get("Risks")
    if body is None or words(body) < 8 or "TODO" in body:
        return ["no Risks section with content"]
    return []


_LOG_FIELDS = ("entry", "prompt", "what the agent did", "what i corrected", "what i checked", "minutes", "would i delegate")


def log_check(work: Path) -> Check:
    path = Path(work) / LOG_FILE
    if not path.is_file():
        return _fail(N_LOG, f"{LOG_FILE} is missing", "Optional: restore the template from the starting commit and add one entry.", required=False)
    text = path.read_text(encoding="utf-8", errors="replace")
    if re.search(r"no agent used", text, re.I):
        return _ok(N_LOG, "no agent used, and said so", required=False)
    filled = 0
    for line in text.splitlines():
        label, colon, value = line.partition(":")
        if colon and any(label.strip().lower().startswith(f) for f in _LOG_FIELDS) and len(value.strip()) >= 3:
            filled += 1
    if filled >= 5:
        return _ok(N_LOG, required=False)
    return _fail(N_LOG, f"{filled} of 7 fields filled", "Optional: fill the entry in the lesson 0.1 format, or write 'no agent used' and why.", required=False)


# ---------------------------------------------------------------------------------------------------------
# the checks
# ---------------------------------------------------------------------------------------------------------
def _per_ticket(specs: dict[str, Spec | None], name: str, finder: Callable[[Spec], Sequence[str]], hint: str,
                required: bool = True) -> Check:
    """One check over the specs that exist: their problems are listed ticket by ticket; with no problem in the ones that
    exist, a missing spec still keeps the check from passing (it waits for it)."""
    missing = [f"{SPEC_DIR}/{t}.md" for t, s in specs.items() if s is None]
    problems = []
    for ticket, spec in specs.items():
        if spec is None:
            continue
        found = list(finder(spec))
        if found:
            problems.append(f"{ticket}: " + "; ".join(found[:2]))
    if problems:
        return _fail(name, " | ".join(problems[:3]) + (f" (+{len(problems) - 3} more)" if len(problems) > 3 else ""), hint, required)
    if missing:
        return _fail(name, _waiting(missing), "", required)
    return _ok(name, required=required)


def spec_checks(work: Path) -> list[Check]:
    work = Path(work)
    specs = load_specs(work)
    files = repo_files(work)
    out: list[Check] = []

    missing = [f"{SPEC_DIR}/{t}.md" for t, s in specs.items() if s is None]
    out.append(_fail(N_EXIST, "missing: " + _short(missing), "Write one spec per ticket, on specs/TEMPLATE.md, in specs/T1.md, specs/T2.md and specs/T3.md.")
               if missing else _ok(N_EXIST))
    out.append(_per_ticket(specs, N_SECTIONS, section_problems,
                           "Keep the headings of specs/TEMPLATE.md and write something under each one."))
    out.append(_per_ticket(specs, N_PLACEHOLDERS, placeholder_problems,
                           "Replace every TODO of the template with your own text, and decide what is still TBD."))
    out.append(_per_ticket(specs, N_FILLER, filler_problems,
                           "Say it with a number, an example or a name from the code; delete it if you cannot."))
    out.append(_per_ticket(specs, N_EXAMPLES, example_problems,
                           "Behaviour needs worked examples: exact inputs and outputs, as a table or Given / When / Then, "
                           "including the edges (the smallest amount, the exact boundary, one cent or one second either side)."))
    out.append(_per_ticket(specs, N_CRITERIA, criteria_problems,
                           "One bullet per criterion; each must name a value, a code name or a text that a test could compare. "
                           "\"Works properly\" is not a criterion."))
    out.append(_per_ticket(specs, N_LISTS, list_problems,
                           "List constraints, non-goals and decisions as bullets, one per line: what must stay true, what you "
                           "will not build, and every question the ticket left open, answered."))
    out.append(_per_ticket(specs, N_FILES, lambda s: file_problems(s, files),
                           "Open the files you name. If a document disagrees with the code, the code wins; name a file you "
                           "will create as new, on a line that says so."))

    for ticket in TICKETS:
        spec = specs[ticket]
        name = n_ambiguities(ticket)
        if spec is None:
            out.append(_fail(name, WAITING.format(f"{SPEC_DIR}/{ticket}.md"), ""))
            continue
        total = len(AMBIGUITIES[ticket])
        solved, open_families = ambiguity_problems(ticket, spec)
        if open_families:
            counted = {f: open_families.count(f) for f in dict.fromkeys(open_families)}
            shown = ", ".join(f if n == 1 else f"{f} x{n}" for f, n in counted.items())
            out.append(_fail(name, f"{solved} of {total} resolved; still open: {shown}",
                             "Read the ticket as a sceptic: which words can mean two things? Find what the code does, then write "
                             "each answer as one complete sentence that names its subject (a question is not an answer). "
                             "If only Hessa can know, decide, say it is an assumption and who confirms it."))
        else:
            out.append(_ok(name, f"{solved} of {total} resolved"))

    broken: list[str] = []
    hints: list[str] = []
    for ticket, spec in specs.items():
        if spec is None:
            continue
        for label, hint in rule_problems(spec):
            broken.append(f"{ticket}: {label}")
            hints.append(hint)
    if broken:
        out.append(_fail(N_RULES, _short(broken, 2), hints[0] + ". When the code and your idea disagree, change the idea."))
    elif missing:
        out.append(_fail(N_RULES, _waiting(missing), ""))
    else:
        out.append(_ok(N_RULES))
    out.append(_per_ticket(specs, N_REVIEW, lambda s: review_problems(s, files),
                           "CONTRIBUTING.md: anything that touches money.py, fees.py, fx.py, limits.py, ledger.py or service.py "
                           "needs a second human reviewer. Say so in Constraints or in the Plan."))
    out.append(_per_ticket(specs, N_PLAN_SIZE, plan_size_problems,
                           "Number the steps; keep each to one commit and one reading of the diff, naming the file, test or "
                           "command. If the plan is longer, slice the work and plan the first slice."))
    out.append(_per_ticket(specs, N_PLAN_SHAPE, plan_shape_problems,
                           "Write the failing test before the code it covers, run pytest, and say how to undo the change."))

    present = [s for s in specs.values() if s is not None]
    if len(present) == len(TICKETS):
        pairs = [(a.ticket, b.ticket) for i, a in enumerate(present) for b in present[i + 1:] if similarity(a.text, b.text) > 0.5]
        out.append(_fail(N_DISTINCT, "too similar: " + ", ".join(f"{a} and {b}" for a, b in pairs),
                         "Each ticket has its own numbers, files and decisions. A copy with the names changed is a template, not a spec.",
                         required=False) if pairs else _ok(N_DISTINCT, required=False))
    else:
        out.append(_fail(N_DISTINCT, "no specs yet", "", required=False))
    out.append(_per_ticket(specs, N_RISKS, risk_problems,
                           "Name what could go wrong in production and how you would notice.", required=False))
    out.append(log_check(work))
    return out
