"""Helpers that only lab m12 uses (kept out of ``checks.py``, which belongs to the kit): the playbook lint.

What "lint" means here
----------------------
A team playbook is prose, so nothing compiles it. This module reads ``playbook.md`` the way a sceptical
tech lead would and asks a fixed list of questions, each with a mechanical answer:

* Is it complete?                    ten sections (found by a key word in the heading), each with real content, no template
                                     text left (a TODO or TBD that is only talked about is not template text)
* Are the rules rules?               bullets that start with MUST / MUST NOT and end with ``Check:`` and a mechanism anyone
                                     could run or inspect (a command, a CI job, a report, an audit that compares or lists ...);
                                     a person alone, a bare "a CI job" or one check pasted onto many rules is not one; no weasel
                                     words; spread over the areas that need them
* Are the review norms concrete?     the label, a diff limit in lines, the second human for the six money modules
                                     CONTRIBUTING.md names, a response time, what the author explains (read from the review
                                     section; "tests come with the change" may also be said in the verification section)
* Are the metrics measurable?        one ``###`` block per metric with six fields; three DORA-style delivery metrics; a guard metric
                                     whose threshold has a number and a response; definitions that name what is counted or timed,
                                     between which events and over which period; baselines taken from the facts file
                                     (``assets/team-context.md``) in its unit or an equivalent one, or "to be measured"
* Is it honest?                      no vanity metrics anywhere in the file, no unsourced productivity claims (source in the same
                                     sentence), no files that do not exist unless the words next to them call them new, nothing
                                     that loosens the bank's rules or CONTRIBUTING.md (no exceptions or AI stand-in for the
                                     second human reviewer)

What the lint cannot tell: whether the policy is *wise*, whether the team will follow it, or whether the numbers
suit your team. It checks the shape of a good playbook, not the judgement behind it. The lesson says so.

The facts it compares with (the money modules, the baseline figures) are read from the kit's own copies, so
editing ``lab-assets/team-context.md`` or ``CONTRIBUTING.md`` cannot move the goalposts (and counts as an
out-of-scope change).
"""
from __future__ import annotations

import os
import re
from collections import Counter
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from ailab import checks, framework
from ailab.framework import Check

# ---------------------------------------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------------------------------------
PLAYBOOK_FILE = "playbook.md"
ALLOWED_FILES = (PLAYBOOK_FILE,)  # the only file this lab may change
LAB_DIR = Path(__file__).resolve().parent / "labs" / "m12_playbook"
FACTS_PATH = LAB_DIR / "assets" / "team-context.md"
CONTRIBUTING_PATH = framework.BASE_REPO / "CONTRIBUTING.md"

MIN_SECTION_WORDS = 40
MIN_WORDS, MAX_WORDS = 700, 4500
MIN_RULES = 12
MIN_DELIVERY, MIN_GUARD = 3, 1
DIFF_LIMIT_RANGE = (10, 800)  # a "small diff" limit, in changed lines

FALLBACK_MONEY_MODULES = ("money.py", "fees.py", "fx.py", "limits.py", "ledger.py", "service.py")

# Check names (the tests refer to them, so they are constants).
N_EXISTS = "playbook.md exists"
N_SECTIONS = "All ten sections are there, with substance"
N_PLACEHOLDERS = "No template text is left"
N_LENGTH = "A length people will read"
N_RULE_COUNT = "At least twelve rules in the MUST / MUST NOT shape"
N_RULE_COVER = "Rules in every area that needs them"
N_RULE_CHECK = "Every rule says how it is checked"
N_RULE_VAGUE = "No weasel words in the rules"
N_TOOLS = "Tools and environments are specific"
N_DATA = "Data rules name the classes, the test data and the accounts"
N_CONTEXT = "Context and memory have a file, an owner and an update trigger"
N_CONTEXT_SIZE = "The memory file has a size limit"
N_REV_LABEL = "Review: the AI-assisted label is named"
N_REV_SIZE = "Review: a largest diff, in lines"
N_REV_MONEY = "Review: a second human for every money module"
N_REV_AUTHOR = "Review: the author explains and shows evidence"
N_REV_SPEED = "Review: a response time"
N_REV_TESTS = "Review: tests come with the change"
N_REV_SPEC = "Spec: what a ticket needs before an agent starts"
N_VERIFY = "Verification: the test command, Decimal and the tests' integrity"
N_VER_FAIL = "Verification: a new test must be seen to fail first"
N_SECURITY = "Security baseline covers the essentials"
N_AUTOMATION = "Automation says what is never automated, and limits unattended runs"
N_INCIDENT = "Incident handling covers the first day"
N_ONBOARDING = "Onboarding covers juniors and skill"
N_MET_BLOCKS = "Metrics: every metric block has all six fields"
N_MET_DELIVERY = "Metrics: three DORA-style delivery metrics"
N_MET_GUARD = "Metrics: a guard with a threshold and a response"
N_MET_DEFINED = "Metrics: every definition is measurable"
N_MET_BASELINE = "Metrics: baselines come from the facts"
N_MET_VANITY = "Metrics: no vanity measures"
N_MET_SPLIT = "Metrics: AI-assisted changes are compared with the rest"
N_CONTRADICT = "Nothing contradicts the bank's rules or CONTRIBUTING.md"
N_PROD = "Agents never touch production"
N_PATHS = "Every file it points to exists"
N_CLAIMS = "No unsourced claims about productivity"
N_DISTINCT = "The sections are not copies of each other"
N_SCOPE = "Only playbook.md changed"
N_SECRETS = "No secrets in the change"
N_COMMITS = "Commit messages follow CONTRIBUTING.md"
N_CLEAN = "Everything is committed (nothing left over)"

ALL_NAMES = [
    N_EXISTS, N_SECTIONS, N_PLACEHOLDERS, N_LENGTH, N_RULE_COUNT, N_RULE_COVER, N_RULE_CHECK, N_RULE_VAGUE,
    N_TOOLS, N_DATA, N_CONTEXT, N_CONTEXT_SIZE, N_REV_LABEL, N_REV_SIZE, N_REV_MONEY, N_REV_AUTHOR, N_REV_SPEED,
    N_REV_TESTS, N_REV_SPEC, N_VERIFY, N_VER_FAIL, N_SECURITY, N_AUTOMATION, N_INCIDENT, N_ONBOARDING,
    N_MET_BLOCKS, N_MET_DELIVERY, N_MET_GUARD, N_MET_DEFINED, N_MET_BASELINE, N_MET_VANITY, N_MET_SPLIT,
    N_CONTRADICT, N_PROD, N_PATHS, N_CLAIMS, N_DISTINCT, N_SCOPE, N_SECRETS, N_COMMITS, N_CLEAN,
]
ADVISORY = {N_CONTEXT_SIZE, N_REV_TESTS, N_REV_SPEC, N_VER_FAIL, N_MET_SPLIT, N_DISTINCT}

NEGATION = re.compile(
    r"\b(never|not|no|nobody|none|don'?t|do not|avoid\w*|reject\w*|refus\w*|forbid\w*|forbidden|ban\w*|prohibit\w*|"
    r"instead of|without|must not|neither|nor|cannot|can'?t|disabl\w*|den(?:y|ies|ied)|block\w*)\b",
    re.I,
)
VAGUE = re.compile(
    r"\b(responsibl[ey]\w*|careful\w*|cautious\w*|mindful\w*|as appropriate|where appropriate|when appropriate|"
    r"appropriate\w*|if possible|where possible|when possible|as needed|as necessary|try to|best effort|reasonabl[ey]|"
    r"properly|good judge?ment|common sense|should consider|ideally|generally|typically|usually|wherever feasible|"
    r"as far as possible|when in doubt|use your judge?ment|"
    r"regularly|periodically|promptly|timely|adequate\w*|sufficient\w*|sensibl[ey]|as soon as possible|asap|"
    r"whenever convenient|when convenient|aim to|strive to|endeavou?r\w*|where it makes sense|if it makes sense|"
    r"if feasible|when feasible|where feasible|if practical|where practical|whenever practical|to the extent possible|"
    r"if needed|when needed|if necessary|when necessary|quickly|swiftly|suitabl[ey]|in good faith|"
    r"as much as (?:is )?(?:practical|possible|reasonable)|as far as (?:is )?practical|in good time|in due course|from time to time|"
    r"as and when|to a reasonable extent|as (?:often|soon) as)\b",
    re.I,
)

# Unfinished text. Only the skeleton's <<prompts>> and markers used as markers count: a TODO or TBD that is *talked
# about* ("MUST NOT leave a TODO in merged code", "the TBD column") or sits in backticks is ordinary prose.
_CODE_SPAN = re.compile(r"`[^`\n]*`")
_MARK = r"(?:TODO|TBD|FIXME)"
_UNFINISHED = re.compile(
    rf"^[\s>*_+#|\-]*(?:\d+[.)]\s*)?{_MARK}\b"      # the line, item or value starts with the marker
    rf"|\b{_MARK}\s*:"                                 # "TODO: write this"
    rf"|[(\[]\s*{_MARK}\s*[)\]]"                       # "(TBD)", "[TODO]"
    rf"|:\s*[*_]*{_MARK}[*_]*\W*$"                     # "Baseline: TBD"
    rf"|\|\s*{_MARK}\s*\|"                             # a table cell that holds only the marker
)


def has_placeholder(text: str) -> bool:
    """Is there skeleton prompt or an unfinished-text marker in ``text`` (inline code is ignored)?"""
    plain = _CODE_SPAN.sub(" ", text)
    if "<<" in plain or ">>" in plain:
        return True
    if re.search(r"lorem ipsum|\bfill (?:this|it) in\b|\bxxx+\b", plain, re.I):
        return True
    return bool(_UNFINISHED.search(plain))


# ---------------------------------------------------------------------------------------------------------
# the facts (read from the kit's own copies)
# ---------------------------------------------------------------------------------------------------------
def money_modules() -> tuple[str, ...]:
    """The modules CONTRIBUTING.md says need a second reviewer, read from the kit's copy of the base repo."""
    try:
        text = CONTRIBUTING_PATH.read_text(encoding="utf-8")
        match = re.search(r"Money logic needs a second reviewer\.\*\*(.*?)(?:\n\*|\n\n|\Z)", text, flags=re.S)
        names = tuple(dict.fromkeys(re.findall(r"`(\w+\.py)`", match.group(1)))) if match else ()
    except OSError:
        names = ()
    return names if len(names) >= 3 else FALLBACK_MONEY_MODULES


def fact_numbers() -> set[str]:
    """Every number in the baseline table of ``assets/team-context.md`` (and the 13 weeks in its heading)."""
    try:
        text = FACTS_PATH.read_text(encoding="utf-8")
    except OSError:
        return set()
    start = text.find("## Last quarter in numbers")
    return set(re.findall(r"\d+(?:\.\d+)?", text[start:])) if start >= 0 else set()


@dataclass(frozen=True)
class Fact:
    """One row of the facts file's table, as the figures a baseline may quote for it."""

    key: str
    pattern: re.Pattern[str]          # matched on the metric's name (first match wins), then on its definition
    ints: frozenset[str]              # whole numbers that may stand alone ("3 of 30", "30 in 13 weeks")
    hours: float | None = None        # a duration, quoted in any unit within 10% ("52 hours", "about 2 days")
    percents: tuple[float, ...] = ()  # a percentage, quoted to within half a point ("10%", "13.3%")
    decimals: tuple[tuple[float, float], ...] = ()  # a bare decimal that is the same figure ("2.3 a week")


FACTS: tuple[Fact, ...] = (
    Fact("lead time", re.compile(r"lead time|cycle time|commit to (?:production|prod|deploy)", re.I), frozenset({"52"}), hours=52),
    Fact("deployment frequency", re.compile(
        r"(deploy\w*|release)\s+(frequency|rate|cadence)|frequency of (deploy|release)|how often we (deploy|release)|"
        r"(?:deploy\w*|releases?)\s+(?:per|a|each|every)\s+(?:day|week|month)", re.I),
        frozenset({"30", "2"}), decimals=((2.2, 2.4),)),
    Fact("recovery time", re.compile(r"recover|restor|mttr|resolv|repair|time to (?:fix|remediat)", re.I), frozenset({"3"}), hours=3),
    Fact("change failure rate", re.compile(r"change fail\w*|failure rate|fail\w* (change|deployment|release)s?\s*(rate|percent)", re.I),
         frozenset({"3", "30", "10"}), percents=(10.0,)),
    Fact("rework rate", re.compile(r"rework|unplanned", re.I), frozenset({"4", "30", "13"}), percents=(13.33,)),
    Fact("review turnaround", re.compile(
        r"review (?:turnaround|time|latency|wait|speed)|turnaround|time to (?:first )?review|first (?:human )?review", re.I),
        frozenset({"9"}), hours=9),
    Fact("incidents", re.compile(r"incident", re.I), frozenset({"0", "1"})),
    Fact("AI-assisted share", re.compile(r"adoption|share|AI[- ]assisted", re.I), frozenset({"60"}), percents=(60.0,)),
)
# Kept for the tests and for anyone reading this file: the whole numbers each metric may quote.
BASELINES: tuple[tuple[re.Pattern[str], frozenset[str]], ...] = tuple((fact.pattern, fact.ints) for fact in FACTS)
QUARTER_WEEKS = "13"  # "13 weeks" (the length of the quarter) may be quoted for any metric, with its unit only


def baseline_fact(name: str, definition: str = "") -> Fact | None:
    """The row of the facts table a metric belongs to: by its name, else by what its definition says."""
    for text in (name, definition):
        for fact in FACTS:
            if fact.pattern.search(text):
                return fact
    return None


def baseline_figures(name: str, definition: str = "") -> frozenset[str]:
    """The whole numbers a baseline may quote for this metric, without the quarter's 13 weeks."""
    fact = baseline_fact(name, definition)
    return fact.ints if fact else frozenset()


_QTY = re.compile(
    r"(?<![\w.])(\d+(?:\.\d+)?)(?:[\s\-–]*(%|percent\b|hours?\b|hrs?\b|h\b|minutes?\b|mins?\b|days?\b|weeks?\b|wks?\b|months?\b))?",
    re.I,
)
_HOURS_PER = {"h": 1.0, "hr": 1.0, "hrs": 1.0, "hour": 1.0, "hours": 1.0, "min": 1 / 60, "mins": 1 / 60, "minute": 1 / 60,
              "minutes": 1 / 60, "day": 24.0, "days": 24.0, "week": 168.0, "weeks": 168.0, "wk": 168.0, "wks": 168.0}


def quantity_ok(fact: Fact | None, number: float, unit: str) -> bool:
    """May a baseline quote ``number`` (with ``unit``, possibly empty) for a metric of this row of the facts?"""
    unit = unit.lower()
    if unit in ("%", "percent"):
        return fact is not None and any(abs(number - p) <= 0.5 for p in fact.percents)
    if unit.startswith(("week", "wk")) and number == float(QUARTER_WEEKS):
        return True
    if unit:  # a duration in some unit: compare in hours
        factor = _HOURS_PER.get(unit)
        return bool(fact and fact.hours and factor and abs(number * factor - fact.hours) <= 0.1 * fact.hours)
    if fact is None:
        return False
    if number.is_integer() and str(int(number)) in fact.ints:
        return True
    return any(low <= number <= high for low, high in fact.decimals)


def baseline_problem(metric: "Metric") -> str | None:
    """Why this metric's Baseline is not a figure the facts give for it (None when it is fine)."""
    base = metric.fields.get("Baseline", "")
    fact = baseline_fact(metric.name, metric.fields.get("Definition", ""))
    quoted = [(float(hit.group(1)), (hit.group(2) or ""), hit.group(0).strip()) for hit in _QTY.finditer(base)]
    wrong = [text for number, unit, text in quoted if not quantity_ok(fact, number, unit)]
    if wrong:
        shown = _short(wrong, 3)
        if fact is None:
            return (f'"{metric.name}" quotes {shown}, but no row of the facts table matches this metric\'s name, '
                    f'so the honest baseline is "to be measured"')
        return f'"{metric.name}" quotes {shown}, which the facts file does not give for this metric'
    if not quoted and not re.search(
            r"to be measured|not (?:yet )?measured|unknown|no baseline|will be measured|measure (?:it )?first|not tracked|do not (?:yet )?(?:know|measure)",
            base, re.I):
        return f'"{metric.name}": say a figure from the facts or "to be measured"'
    return None


# ---------------------------------------------------------------------------------------------------------
# reading the document
# ---------------------------------------------------------------------------------------------------------
@dataclass
class Heading:
    level: int
    title: str
    norm: str
    line: int  # 0-based index into Doc.lines


@dataclass
class Doc:
    lines: list[str]
    fenced: list[bool]  # True for a line inside a code fence (the fence markers included)
    headings: list[Heading]

    def prose(self, start: int = 0, end: int | None = None) -> list[tuple[int, str]]:
        """(index, line) for every line outside a code fence, in [start, end)."""
        stop = len(self.lines) if end is None else end
        return [(i, self.lines[i]) for i in range(start, stop) if not self.fenced[i]]

    def logical(self, start: int = 0, end: int | None = None) -> list[tuple[int, str]]:
        """(index of the first physical line, text) with soft-wrapped lines joined: a sentence wrapped at 100
        columns is still one sentence. A heading, a list item, a table row or a blank line starts a new one."""
        stop = len(self.lines) if end is None else end
        out: list[tuple[int, str]] = []
        current: list[str] = []
        first = start

        def flush() -> None:
            if current:
                out.append((first, " ".join(current)))
                current.clear()

        for i in range(start, stop):
            if self.fenced[i]:
                flush()
                continue
            line = self.lines[i]
            if not line.strip():
                flush()
                continue
            is_heading = bool(_HEADING.match(line))
            starts_new = bool(is_heading or _ITEM.match(line) or line.lstrip().startswith(("|", ">")))
            if starts_new or not current:
                flush()
                first = i
            current.append(line.strip())
            if is_heading:
                flush()  # a heading is a line of its own
        flush()
        return out


@dataclass
class Section:
    key: str
    heading: Heading
    start: int  # first body line
    end: int  # one past the last body line
    doc: Doc = field(repr=False, default=None)  # type: ignore[assignment]

    def lines(self) -> list[tuple[int, str]]:
        return self.doc.prose(self.start, self.end)

    def text(self) -> str:
        """The body as plain prose: no code fences, no <<placeholders>>, no quoted prompts."""
        kept = [strip_placeholders(line) for _, line in self.doc.logical(self.start, self.end) if not line.startswith(">")]
        return "\n".join(kept)

    def words(self) -> int:
        return len(re.findall(r"[A-Za-z0-9_']+", self.text()))


_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_PLACEHOLDER_SPAN = re.compile(r"<<[^>\n]*>>")


def strip_placeholders(line: str) -> str:
    return _PLACEHOLDER_SPAN.sub(" ", line)


def norm_title(title: str) -> str:
    text = re.sub(r"[`*_]", "", title).lower()
    text = re.sub(r"^\s*(?:section\s+)?\d+[.):]?\s*", "", text)
    return re.sub(r"\s+", " ", text).strip(" .:-")


def parse(text: str) -> Doc:
    lines = text.splitlines()
    fenced: list[bool] = []
    headings: list[Heading] = []
    marker: str | None = None
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        fence = re.match(r"(```+|~~~+)", stripped)
        if marker is None and fence:
            marker = fence.group(1)[:3]
            fenced.append(True)
            continue
        if marker is not None:
            fenced.append(True)
            if stripped.startswith(marker):
                marker = None
            continue
        fenced.append(False)
        match = _HEADING.match(line)
        if match:
            title = match.group(2).strip()
            headings.append(Heading(len(match.group(1)), title, norm_title(title), i))
    return Doc(lines, fenced, headings)


SECTION_DEFS: tuple[tuple[str, str, re.Pattern[str]], ...] = (
    ("tools", "tools and environments", re.compile(r"\b(tools?|tooling|environments?)\b")),
    ("data", "data rules", re.compile(r"\bdata\b")),
    ("context", "context and memory", re.compile(r"\b(context|memory)\b")),
    ("review", "spec and review norms", re.compile(r"\b(reviews?|specs?|specifications?)\b")),
    ("verification", "verification standard", re.compile(r"\bverif\w*")),
    ("security", "security baseline", re.compile(r"\bsecur\w*")),
    ("automation", "automation", re.compile(r"\bautomat\w*")),
    ("metrics", "metrics plan", re.compile(r"\bmetrics?\b")),
    ("incident", "incident handling", re.compile(r"\bincidents?\b")),
    ("onboarding", "onboarding", re.compile(r"\b(?:onboard\w*|joiners?|new hires?|juniors?)\b")),
)
TITLES = {key: title for key, title, _ in SECTION_DEFS}


def find_sections(doc: Doc) -> dict[str, Section]:
    """The ten sections, found by heading words. The heading level is whichever (2, 1, 3) matches the most."""
    best: dict[str, Section] = {}
    for level in (2, 1, 3):
        found: dict[str, Section] = {}
        for key, _, pattern in SECTION_DEFS:
            for idx, heading in enumerate(doc.headings):
                if heading.level != level or not pattern.search(heading.norm):
                    continue
                end = len(doc.lines)
                for later in doc.headings[idx + 1:]:
                    if later.level <= level:
                        end = later.line
                        break
                found[key] = Section(key, heading, heading.line + 1, end, doc)
                break
        if len(found) > len(best):
            best = found
    return best


def section_of(sections: dict[str, Section], index: int) -> str | None:
    for key, section in sections.items():
        if section.start - 1 <= index < section.end:
            return key
    return None


# ---------------------------------------------------------------------------------------------------------
# rules
# ---------------------------------------------------------------------------------------------------------
_ITEM = re.compile(r"^(\s*)(?:[-*+]|\d+[.)])\s+(.*)$")
# A rule starts with MUST or MUST NOT, after an optional label such as "R1.", "**D-2**", "Data rule 3 -" or "R1 (data):"
_RULE_START = re.compile(
    r"^[\s*_`]*(?:[^\n]{0,40}?[:.)\u2014\u2013-][\s*_`]*)?(MUST NOT|MUST)\b"
)
_CHECK = re.compile(r"\b(?:Checks?|Checked by|Verified by|Verification)[*_]*\s*:\s*[*_]*\s*(.+)$", re.I | re.S)
# What counts as a mechanism after "Check:": something that runs, or leaves a record someone can open. The ticket lists
# the kinds. A person or a feeling alone ("the team lead reviews it", "everyone knows") is not one.
MECHANISM = re.compile(
    "|".join([
        # things that run
        r"\bCI\b", r"\bpipelines?\b", r"\bworkflows?\b", r"\bGitHub Actions?\b", r"\bhooks?\b", r"pre-?commit", r"pre-?push",
        r"pre-?merge", r"\bbranch protection\b", r"\bprotected branch\w*", r"\brulesets?\b", r"\bcode ?owners?\b",
        r"\bCODEOWNERS\b", r"\bpytest\b", r"\btests?\b", r"\bscan\w*", r"\blint\w*", r"\bscripts?\b", r"\bcommands?\b",
        r"\bquer(?:y|ies)\b", r"\bbots?\b", r"\balerts?\b", r"\bmonitor\w*", r"\bdashboards?\b", r"\bgates?\b",
        # gating phrases
        r"\bstatus checks?\b", r"\brequired (?:checks?|reviewers?|reviews?|status)\b", r"\bturns? red\b", r"\bmerge (?:button|queue|gate)\b",
        r"\b(?:build|job|check|pipeline|CI|step|test)s?\s+(?:fails?|breaks?|is blocked|stays? (?:red|blocked))\b",
        r"\bfails? the (?:build|job|check|merge|pipeline)\b", r"\bblocks? the (?:merge|release|deploy\w*)\b", r"\bmerge is blocked\b",
        # records and settings
        r"\breport\w*", r"\blogs?\b", r"\btickets?\b", r"\brecord(?:s|ed)?\b", r"\bregisters?\b", r"\blists?\b", r"\blisted\b",
        r"\broster\b", r"\binventory\b", r"\btimestamps?\b", r"\bfields?\b", r"\bcolumns?\b", r"\btemplates?\b",
        r"\bchecklists?\b", r"\blabels?\b", r"\bdiffs?\b", r"\bgrep\b", r"\bgit (?:log|diff|grep|blame)\b", r"\bsettings\b",
        r"\bdeny rules?\b", r"\bpermissions?\b", r"\bmetrics?\b", r"\bon-call\b", r"\bapprov\w*", r"\bsign-?offs?\b",
        r"`[^`]+`",
        # inspections that compare or list named things
        r"\baudit\w*", r"\baccess reviews?\b", r"\bcompar\w+", r"\breconcil\w+", r"\bcross-?check\w*", r"\bcount(?:s|ed|ing)?\b",
        r"\bsampl\w+", r"\bspot[- ]checks?\b", r"\bretros?\b", r"\bretrospectives?\b", r"\bpostmortems?\b",
    ]),
    re.I,
)
_STOPWORDS = frozenset(
    "a an the of in on at for to and or is are be was were runs run running every each any all this that these those it its "
    "with by from as so also then than when if per via".split())
# words that name a kind of mechanism without saying what it looks at ("a CI job", "a monthly audit")
_GENERIC = frozenset(
    "ci cd job jobs step steps check checks checked hook hooks script scripts test tests audit audits review reviews reviewer "
    "reviewers report reports scan scans template templates label labels pipeline workflow tool tools process team lead manager "
    "someone person people we our us monthly weekly daily quarterly yearly annual annually regular".split())


def check_problem(check: str | None) -> str | None:
    """Why a rule's ``Check:`` clause does not say how the rule is verified (None when it does)."""
    if check is None:
        return "no Check: clause"
    if len(re.findall(r"\w+", check)) < 3 or not MECHANISM.search(check):
        return "the check names no mechanism"
    specific = [word for word in re.findall(r"[a-z0-9][\w-]*", _CODE_SPAN.sub(" x ", check.lower()))
                if word not in _STOPWORDS and word not in _GENERIC]
    if not specific:
        return "the check names only a kind of mechanism, not what it looks at"
    return None


@dataclass
class Rule:
    line: int  # 0-based index of the first line
    text: str  # the whole item, one line
    body: str  # before "Check:"
    check: str | None  # after "Check:", None when absent
    section: str | None

    @property
    def label(self) -> str:
        words = re.sub(r"[*_`]", "", self.body).split()
        return " ".join(words[:7]) + (" ..." if len(words) > 7 else "")


def extract_rules(doc: Doc, sections: dict[str, Section]) -> list[Rule]:
    rules: list[Rule] = []
    i, n = 0, len(doc.lines)
    while i < n:
        line = doc.lines[i]
        match = None if doc.fenced[i] else _ITEM.match(line)
        if not match:
            i += 1
            continue
        parts = [match.group(2)]
        j = i + 1
        while j < n and not doc.fenced[j] and doc.lines[j].strip() and not _ITEM.match(doc.lines[j]) \
                and not _HEADING.match(doc.lines[j]) and not doc.lines[j].lstrip().startswith(("|", ">")):
            parts.append(doc.lines[j].strip())
            j += 1
        indent = len(match.group(1))
        while j < n and not doc.fenced[j]:  # nested items (a "Check:" on its own sub-bullet) belong to the rule
            child = _ITEM.match(doc.lines[j])
            if not child or len(child.group(1)) <= indent:
                break
            parts.append(child.group(2))
            j += 1
            while j < n and not doc.fenced[j] and doc.lines[j].strip() and not _ITEM.match(doc.lines[j]) \
                    and not _HEADING.match(doc.lines[j]):
                parts.append(doc.lines[j].strip())
                j += 1
        text = " ".join(parts)
        if _RULE_START.match(text):
            found = _CHECK.search(text)
            body = text[:found.start()] if found else text
            rules.append(Rule(i, text, body.strip(), found.group(1).strip() if found else None, section_of(sections, i)))
            i = j  # a rule swallows its continuation lines and its sub-bullets
        else:
            i += 1  # any other item: look at its sub-bullets one by one
    return rules


# ---------------------------------------------------------------------------------------------------------
# metrics
# ---------------------------------------------------------------------------------------------------------
FIELDS = ("Kind", "Definition", "Source", "Cadence", "Baseline", "Threshold")
_FIELD = re.compile(
    r"^\s*(?:[-*+]\s+)?(?:\*\*|__)?\s*(Kind|Definition|Source|Cadence|Baseline|Threshold|Target|Trigger)\s*(?:\*\*|__)?"
    r"\s*:\s*(?:\*\*|__)?\s*(.*)$",
    re.I,
)


@dataclass
class Metric:
    name: str
    line: int  # 0-based index of the block's heading
    fields: dict[str, str]
    end: int = 0  # one past the block's last line

    @property
    def kind(self) -> str:
        """``delivery`` or ``guard``: whichever of the two words comes first in the Kind field ("DORA delivery metric" is delivery)."""
        value = self.fields.get("Kind", "")
        words = [] if has_placeholder(value) else re.findall(r"delivery|guard", value.lower())
        return words[0] if words else "other"


def metric_blocks(doc: Doc, section: Section) -> list[Metric]:
    """Every sub-heading of the metrics section that holds at least one of the six fields."""
    subs = [h for h in doc.headings if section.start <= h.line < section.end and h.level > section.heading.level]
    blocks: list[Metric] = []
    for idx, heading in enumerate(subs):
        stop = subs[idx + 1].line if idx + 1 < len(subs) else section.end
        # a deeper or later heading of any level ends the block
        for other in doc.headings:
            if heading.line < other.line < stop:
                stop = other.line
                break
        fields: dict[str, str] = {}
        current: str | None = None
        for i in range(heading.line + 1, stop):
            if doc.fenced[i]:
                continue
            line = doc.lines[i]
            match = _FIELD.match(line)
            if match:
                name = match.group(1).capitalize()
                name = "Threshold" if name in ("Target", "Trigger") else name
                current = name
                fields[name] = match.group(2).strip()
            elif current and line.strip() and not _ITEM.match(line):
                fields[current] = (fields[current] + " " + line.strip()).strip()
            elif not line.strip():
                current = None
        if fields:
            blocks.append(Metric(re.sub(r"[`*_]", "", heading.title).strip(), heading.line, fields, stop))
    return blocks


FAMILIES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("lead time", re.compile(r"lead time|cycle time|commit to (?:production|prod|deploy)", re.I)),
    ("deployment frequency", re.compile(
        r"(deploy\w*|release)\s+(frequency|rate|cadence)|frequency of (deploy|release)|how often we (deploy|release)|"
        r"(?:deploy\w*|releases?)\s+(?:per|a|each|every)\s+(?:day|week|month)", re.I)),
    ("change failure rate", re.compile(r"change fail\w*|fail\w* (change|deployment|release)s?\s*(rate|percent)|failure rate", re.I)),
    ("recovery time", re.compile(r"recover|restor|mttr|resolv|repair|time to (?:fix|remediat)", re.I)),
    ("rework rate", re.compile(r"rework", re.I)),
)


def family(name: str) -> str | None:
    return next((label for label, pattern in FAMILIES if pattern.search(name)), None)


_SUBJECTIVE = re.compile(r"\b(feel|feels|felt|perceiv\w*|sentiment|satisf\w*|happy|happiness|enjoy\w*|vibes?)\b", re.I)
_STAT = re.compile(r"\b(median|mean|average|p\d{2}|\d{2}(?:st|nd|rd|th) percentile|percentile)\b", re.I)
_FROM_TO = re.compile(r"\bfrom\b.{3,}?\b(?:to|until|till)\b|\bbetween\b.{3,}?\band\b|\bsince\b.{3,}?\b(?:until|till|to)\b|\bminus\b|→|->", re.I | re.S)
_RATIO = re.compile(r"divided by|÷|/|\bout of\b|\bof all\b|\bshare of\b|\bpercent(?:age)? of\b|\bratio of\b|\bproportion of\b|\bper\b|\bover\b", re.I)
_WINDOW = re.compile(r"\b(?:per|each|every|weekly|monthly|quarterly|daily|sprint|weeks?|months?|quarters?|days?|rolling)\b", re.I)
_PERIOD = re.compile(
    r"\b(?:per|a|an|each|every|in a|in the|in each|during a|during the)\s+(?:\w+\s+){0,2}(?:day|week|month|sprint|quarter)s?\b|"
    r"\b(?:daily|weekly|monthly|quarterly)\b", re.I)
_COUNTING = re.compile(r"\b(?:count|number|total|how many|deployments?|releases?|incidents?)\b", re.I)


# A definition about software delivery names something from it. For the five DORA metrics the two ends are checked too.
_DOMAIN = re.compile(
    r"\b(?:commits?|pull requests?|PRs?|merg\w+|changes?|deploy\w*|releas\w*|production|prod|incidents?|tickets?|review\w*|"
    r"tests?|builds?|bugs?|defects?|roll ?backs?|hotfix\w*|revert\w*|rework\w*|failures?|failed|outages?|alerts?|sessions?|"
    r"prompts?|agents?|costs?|runs?|jobs?|pipelines?|CI|branch\w*|diffs?|lines?|files?|modules?|engineers?|developers?|"
    r"joiners?|hires?|onboarding|stor(?:y|ies)|tasks?|issues?|sprints?|customers?|transfers?|requests?|postmortems?|"
    r"code|work|fix\w*|labels?)\b",
    re.I,
)
FAMILY_ANCHORS: dict[str, tuple[tuple[str, re.Pattern[str]], ...]] = {
    "lead time": (
        ("the change it starts from (a commit, a pull request)", re.compile(r"commit|pull request|\bPRs?\b|merg\w+|change\w*|ticket|code|request|work|task|story|issue", re.I)),
        ("where it ends (production, deployed, live)", re.compile(r"production|\bprod\b|deploy\w*|releas\w*|\blive\b|ship\w*|customers?", re.I)),
    ),
    "deployment frequency": (
        ("what is counted (deployments, releases)", re.compile(r"deploy\w*|releas\w*|ship\w*|push\w*|go(?:es|ing)? live", re.I)),
    ),
    "change failure rate": (
        ("what is counted (deployments, releases, changes)", re.compile(r"deploy\w*|releas\w*|change\w*|ship\w*", re.I)),
        ("what counts as a failure (a hotfix, a rollback, an incident)", re.compile(r"fail\w*|hotfix\w*|roll ?back|revert\w*|incident|patch\w*|remediat\w*|degrad\w*|\bbug", re.I)),
    ),
    "recovery time": (
        ("where it starts (a failure declared or detected)", re.compile(r"fail\w*|incident|outage|declared|detect\w*|alert\w*|degrad\w*|down(?:time)?|broke\w*|\bbug|issue", re.I)),
        ("where it ends (service restored, fixed, rolled back)", re.compile(r"restor\w*|recover\w*|resol\w*|fix\w*|\bback\b|roll ?back|mitigat\w*|repair\w*|healthy|working again|normal", re.I)),
    ),
    "rework rate": (
        ("what counts as rework (unplanned fixes, hotfixes, reverts)", re.compile(r"unplanned|rework\w*|fix\w*|hotfix\w*|follow-?up|outside the plan|revert\w*|roll ?back|redo\w*|reopen\w*|patch\w*", re.I)),
    ),
}


def definition_problems(metric: Metric) -> list[str]:
    """Why a definition is not measurable; an empty list means it is."""
    text = metric.fields.get("Definition", "")
    name = metric.name.lower()
    problems: list[str] = []
    if len(re.findall(r"\w+", text)) < 4:
        return ["too short to define anything: say what is counted or timed, between which events, over which period"]
    if re.match(r"\s*how (?!many\b|much\b)", text, re.I) or _SUBJECTIVE.search(text):
        return ["it describes a feeling or a question, not a number: say what is counted or timed"]
    if re.search(r"\brate\b|\bratio\b|\bshare\b|\bpercent", name):
        if not _RATIO.search(text):
            problems.append("a rate needs a numerator and a denominator (A divided by B, A out of all B)")
        if not _WINDOW.search(text):
            problems.append("name the period it is computed over (a week, a month, a quarter)")
    elif re.search(r"\b(time|duration|turnaround|latency|age|delay|wait)\b", name):
        if not _STAT.search(text):
            problems.append("a duration needs a statistic: the median, the mean or a percentile")
        if not _FROM_TO.search(text):
            problems.append("name the start event and the end event (from ... until ...)")
    elif re.search(r"\b(frequency|count|number|volume|throughput|incidents?)\b", name):
        if not _PERIOD.search(text):
            problems.append("a count needs a period (per week, per quarter)")
        if not _COUNTING.search(text):
            problems.append("say what is counted")
    elif not (_STAT.search(text) or _RATIO.search(text) or _PERIOD.search(text)):
        problems.append("no unit, statistic or period: how would two people get the same number?")
    anchors = FAMILY_ANCHORS.get(family(metric.name) or "")
    if anchors:
        problems += [f"it should name {label}" for label, pattern in anchors if not pattern.search(text)]
        if not _DOMAIN.search(text):
            problems.append("it names nothing from software delivery (a commit, a deployment, an incident ...)")
    elif not _DOMAIN.search(text):
        problems.append("it names nothing from software delivery (a commit, a pull request, a deployment, an incident ...): what exactly is counted or timed?")
    return problems


_COMPARATOR = re.compile(
    r"[<>≥≤]|>=|<=|\b(above|below|exceeds?|more than|less than|over|under|at least|at most|no more than|no less than|"
    r"higher than|lower than|worse than|greater than|beyond|rises?|drops?|falls?|reach(?:es)?|up to|within)\b",
    re.I,
)
_ACTION = re.compile(
    r"\b(?:paus|stop|freez|halt|review|retro|escalat|investigat|reduc|roll ?back|revert|tighten|reopen|reset|lower|"
    r"suspend|requir|add|call|convene|discuss|revisit|trigger|ask|inspect|audit|alert|notif|flag|restrict|switch|"
    r"fall back|go back|ban|disabl|revok|rotat|cap|hold|slow|raise the|pull|meet)\w*",
    re.I,
)


_NUMBER_WORD = re.compile(
    r"\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|thirty|forty|fifty|sixty|"
    r"seventy|eighty|ninety|hundred|half)\b", re.I)


def threshold_problems(text: str) -> list[str]:
    problems = []
    if not (re.search(r"\d", text) or _NUMBER_WORD.search(text)):
        problems.append("no number")
    if not _COMPARATOR.search(text):
        problems.append("no comparison (above, below, more than, at least)")
    if not _ACTION.search(text):
        problems.append("no response (what do we do when it is crossed?)")
    return problems


_VANITY = re.compile(
    r"\blines? of code\b|\bLOC\b|\bkloc\b|\bsuggestions? accepted\b|\bsuggestion[- ]acceptance\b|\bacceptance (?:rate|ratio)\b|"
    r"\baccept(?:ed|ance) (?:rate|ratio)\b|\b(?:code|lines) (?:written|generated) by (?:AI|agents?|the agent|Copilot|Claude)\b|"
    r"\bAI[- ](?:written|generated) (?:code|lines|share|percent\w*|ratio)\b|\bpercent(?:age)? of (?:the )?(?:code|lines)\b|"
    r"\b(?:share|percent(?:age)?|ratio) of (?:the )?(?:code|lines) (?:that (?:is|are|was|were) )?(?:written|generated)\b|"
    r"\bnumber of prompts\b|\bprompts? per\b|"
    # the same ideas under other names: uptake, completions kept, lines an agent wrote, volume per person
    r"\buptake\b|\b(?:completions?|suggestions?)\s+(?:kept|accepted|taken|used|offered|shown|retained|rejected)\b|"
    r"\b(?:kept|accepted|taken|retained)\s+(?:completions?|suggestions?)\b|"
    r"\blines?\b[^.\n]{0,80}\b(?:written|generated|authored|produced|created)\s+by\s+(?:an?\s+|the\s+)?(?:AI|agents?|Claude|Copilot|assistants?|LLMs?)\b|"
    r"\b(?:lines?|commits?|pull requests?|PRs?|tickets?)\s+(?:\w+\s+){0,3}per\s+(?:engineer|developer|dev|person|head)\b",
    re.I,
)
_ADOPTION = re.compile(
    r"adoption|\busage\b|\bAI contribution\b|\bAI footprint\b|\bAI penetration\b|"
    r"\bAI[- ]assisted (?:share|percent\w*|ratio|rate|volume|pull requests|PRs)\b|\bAI share\b|"
    r"\b(?:share|percent\w*|ratio|proportion|number|count) of (?:merged )?(?:pull requests|PRs|changes|commits|code|lines)\b.*\bAI\b|"
    r"\bAI[- ](?:written|generated)\b",
    re.I,
)
_QUALITY = re.compile(r"fail|rework|incident|revert|roll ?back|defect|bug|escape|hotfix|review|lead time|recover|restor|\bpass", re.I)


def _negated_by_intro(lines: list[tuple[int, str]], index: int) -> bool:
    """A list item such as "- lines of code" is excused by "We do not measure:" just before the list."""
    if not _ITEM.match(lines[index][1]):
        return False
    for _, earlier in reversed(lines[max(0, index - 6):index]):
        if _ITEM.match(earlier):
            continue
        return bool(NEGATION.search(earlier))
    return False


def is_adoption(metric: Metric) -> bool:
    """A metric that merely counts how much the team uses AI (it is fine to report, wrong to set a target on)."""
    definition = metric.fields.get("Definition", "")
    about_use = _ADOPTION.search(metric.name) or re.search(r"\badoption\b", definition, re.I)
    return bool(about_use) and not _QUALITY.search(metric.name + " " + definition)


# ---------------------------------------------------------------------------------------------------------
# small tools for the checks
# ---------------------------------------------------------------------------------------------------------
def _short(items: Sequence[str], limit: int = 3) -> str:
    return checks._short(list(items), limit)  # noqa: SLF001 - the kit's own formatter, same style as every check


def _fail(name: str, detail: str, hint: str) -> Check:
    return Check(name, False, detail, hint, name not in ADVISORY)


def _ok(name: str, detail: str = "") -> Check:
    return Check(name, True, detail, "", name not in ADVISORY)


def _grade(name: str, problems: Sequence[str], hint: str, detail_ok: str = "") -> Check:
    return _fail(name, "; ".join(problems), hint) if problems else _ok(name, detail_ok)


def _line_has(text: str, *patterns: re.Pattern[str] | str, negated: bool = False) -> bool:
    """Is there one line of ``text`` matching every pattern (and, when ``negated``, a negation word too)?"""
    compiled = [re.compile(p, re.I) if isinstance(p, str) else p for p in patterns]
    for line in text.splitlines():
        if all(p.search(line) for p in compiled) and (not negated or NEGATION.search(line)):
            return True
    return False


Group = tuple[str, Callable[[str], bool]]


def _g(label: str, *patterns: str, negated: bool = False, flags: int = re.I) -> Group:
    """A coverage group: some line must match every pattern (one pattern: anywhere in the text)."""
    compiled = [re.compile(p, flags) for p in patterns]
    if len(compiled) == 1 and not negated:
        return label, lambda text: bool(compiled[0].search(text))
    return label, lambda text: _line_has(text, *compiled, negated=negated)


def _coverage(name: str, text: str, groups: Sequence[Group], need: int, hint: str) -> Check:
    missing = [label for label, test in groups if not test(text)]
    hit = len(groups) - len(missing)
    if hit >= need:
        return _ok(name)
    return _fail(name, f"missing: {_short(missing, 4)}", hint)


def _norm_text(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[`*_>#|-]", " ", text)).strip().lower()


# ---------------------------------------------------------------------------------------------------------
# the checks
# ---------------------------------------------------------------------------------------------------------
def load(work: Path) -> tuple[Doc, dict[str, Section]] | None:
    try:
        text = (Path(work) / PLAYBOOK_FILE).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    doc = parse(text)
    return doc, find_sections(doc)


def sections_check(doc: Doc, sections: dict[str, Section]) -> Check:
    missing = [TITLES[key] for key, _, _ in SECTION_DEFS if key not in sections]
    thin = [TITLES[key] for key, section in sections.items() if section.words() < MIN_SECTION_WORDS]
    problems = ([f"missing a heading for: {_short(missing, 4)}"] if missing else []) \
        + ([f"too thin (under {MIN_SECTION_WORDS} words of your own): {_short(thin, 4)}"] if thin else [])
    hint = ("Use the ten headings of the skeleton and write real content under each; a prompt in <<double angle brackets>> does not count.")
    if missing:
        hint = ("Each section is found by a key word in its heading: tools, data, context or memory, spec or review, verification, "
                "security, automation, metrics, incident, onboarding. Keep the key word when you rename a heading.")
    return _grade(N_SECTIONS, problems, hint)


def placeholders_check(doc: Doc) -> Check:
    hits = [f"line {number + 1}" for number, line in doc.logical() if has_placeholder(line)]
    if hits:
        return _fail(N_PLACEHOLDERS, f"template or unfinished text at {_short(hits, 4)}",
                     "Replace every <<prompt>> with your own text, and finish any TODO or TBD. "
                     "(A TODO or TBD that you write about, or put in backticks, is fine.)")
    return _ok(N_PLACEHOLDERS)


def length_check(doc: Doc) -> Check:
    words = len(re.findall(r"[A-Za-z0-9_']+", "\n".join(strip_placeholders(line) for _, line in doc.prose())))
    if words < MIN_WORDS:
        return _fail(N_LENGTH, f"{words} words; a playbook that covers ten areas needs at least {MIN_WORDS}",
                     "Say enough for each section that a new joiner could act on it (700 to 4,500 words in all).")
    if words > MAX_WORDS:
        return _fail(N_LENGTH, f"{words} words; nobody reads more than {MAX_WORDS} words of policy",
                     "Cut it to 4,500 words or fewer. Prefer a short rule with a check to a long explanation.")
    return _ok(N_LENGTH, f"{words} words")


AREAS = ("data", "review", "verification", "security", "automation", "incident")


def rule_checks(rules: list[Rule]) -> list[Check]:
    out: list[Check] = []
    # count
    if len(rules) < MIN_RULES:
        out.append(_fail(N_RULE_COUNT, f"found {len(rules)} rule(s); the ticket asks for at least {MIN_RULES}",
                         "A rule is a list item that starts with MUST or MUST NOT (capitals) and ends with Check: and how to verify it."))
    else:
        out.append(_ok(N_RULE_COUNT, f"{len(rules)} rules"))
    # coverage
    have = {rule.section for rule in rules}
    missing = [TITLES[a] for a in AREAS if a not in have]
    out.append(_grade(N_RULE_COVER, [f"no rule under: {_short(missing, 6)}"] if missing else [],
                      "Put at least one MUST / MUST NOT rule inside each of those sections."))
    if not rules:
        waiting = "waiting for rules in the MUST / MUST NOT shape"
        out.append(_fail(N_RULE_CHECK, waiting, "Write the rules first."))
        out.append(_fail(N_RULE_VAGUE, waiting, "Write the rules first."))
        return out
    # a check clause with a mechanism
    bad = []
    for rule in rules:
        problem = check_problem(rule.check)
        if problem:
            bad.append(f'"{rule.label}": {problem}')
    problems = [_short(bad, 2) + (f" ({len(bad)} rules in all)" if len(bad) > 2 else "")] if bad else []
    # one check text pasted onto many rules is not a check for each of them
    same = Counter(re.sub(r"\W+", " ", rule.check.lower()).strip() for rule in rules if rule.check)
    if same:
        text, count = same.most_common(1)[0]
        if count >= 4 and count >= 0.4 * len(rules):
            problems.append(f"{count} of {len(rules)} rules end with the same check text; a check says how this rule is verified")
    out.append(_grade(N_RULE_CHECK, problems,
                      "End the rule with Check: and something that runs or leaves a record: a command, a CI job or status check, a hook, a script, "
                      "a scan, a report or log, a checklist item, a label, a branch-protection setting, or an audit that compares or lists named things. "
                      "A person's name alone is not one."))
    # weasel words
    weasel = []
    for rule in rules:
        found = VAGUE.search(rule.text)
        if found:
            weasel.append(f'"{rule.label}" says "{found.group(0)}"')
    out.append(_grade(N_RULE_VAGUE, [_short(weasel, 2)] if weasel else [],
                      "Replace the soft word with something a reviewer could test: a number, a name, a command."))
    return out


def tools_check(section: Section | None) -> Check:
    if section is None:
        return _fail(N_TOOLS, "the tools and environments section is missing", "Add the section from the skeleton.")
    groups = [
        _g("an approved-tools list", r"approved", r"\b(list|register|catalogue|allow-?list)\b"),
        _g("who keeps the list", r"\b(Salem|platform engineering|owner|owned|maintain\w*|keeps?|kept)\b"),
        _g("where agents may run", r"\b(branch|worktree|container|sandbox|laptop|workstation|CI|runner|dev ?container)\b"),
        _g("how a new tool gets approved", r"\b(request|approval|approve|apply)\b", r"\b(new|another|additional|other|unlisted|unapproved)\b"),
    ]
    return _coverage(N_TOOLS, section.text(), groups, 3,
                     "Say which tools are approved and who keeps the list, where agents run, and how someone asks for a new tool.")


def data_check(section: Section | None) -> Check:
    if section is None:
        return _fail(N_DATA, "the data rules section is missing", "Add the section from the skeleton.")
    text = section.text()
    groups = [
        ("the Confidential and Restricted classes", lambda t: "Confidential" in t and "Restricted" in t),
        ("that they never go into a prompt", lambda t: _line_has(t, r"Confidential|Restricted", negated=True)),
        _g("customer data", r"\b(customers?|personal data|account numbers?|PII)\b"),
        _g("synthetic test data", r"\b(synthetic|fictional|fake|anonymi[sz]ed|masked|made-up|dummy)\b"),
        _g("which accounts may be used", r"\b(personal accounts?|company[- ]managed|enterprise (?:account|plan)|SSO|free tiers?|the bank'?s? (?:own )?account)\b"),
    ]
    return _coverage(N_DATA, text, groups, 4,
                     "Name the data classes, say what never goes into a prompt, what test data is allowed and which accounts are.")


def context_checks(section: Section | None) -> list[Check]:
    if section is None:
        miss = "the context and memory section is missing"
        return [_fail(N_CONTEXT, miss, "Add the section from the skeleton."), _fail(N_CONTEXT_SIZE, miss, "Add the section.")]
    text = section.text()
    groups = [
        ("the memory file (CLAUDE.md or AGENTS.md)", lambda t: bool(re.search(r"\b(CLAUDE\.md|AGENTS\.md)\b", t))),
        _g("an owner", r"\b(owner|owned|owns|maintain\w*|responsible|Tariq|Nada|Salem|Noura|lead)\b"),
        _g("what makes us add a line", r"\b(twice|two times|second time|again|repeat\w*|recurr\w*|mistake|correction|incident|retro\w*|whenever|every time)\b"),
    ]
    size = _line_has(text, r"\b\d+\s*lines?\b|\b(?:under|below|at most|no more than|up to|maximum|max)\s+\d+\b")
    return [
        _coverage(N_CONTEXT, text, groups, 3, "Name the memory file (CLAUDE.md or AGENTS.md; it does not exist yet, so say it is new), its owner, and the event that makes someone add a line to it."),
        _ok(N_CONTEXT_SIZE) if size else _fail(N_CONTEXT_SIZE, "no limit on its size",
                                               "A memory file that grows without limit stops being followed: give it a size."),
    ]


def review_checks(section: Section | None, verification: Section | None = None) -> list[Check]:
    names = [N_REV_LABEL, N_REV_SIZE, N_REV_MONEY, N_REV_AUTHOR, N_REV_SPEED, N_REV_TESTS, N_REV_SPEC]
    if section is None:
        return [_fail(n, "the spec and review norms section is missing", "Add the section from the skeleton.") for n in names]
    text = section.text()
    out: list[Check] = []
    out.append(_ok(N_REV_LABEL) if "AI-assisted" in text else
               _fail(N_REV_LABEL, "the label `AI-assisted` is not named", "Name the label exactly as CONTRIBUTING.md spells it."))
    # a diff limit
    lo, hi = DIFF_LIMIT_RANGE
    limits = []
    for line in text.splitlines():
        if re.search(r"\blines?\b|\bLOC\b", line, re.I):
            limits += [int(n.replace(",", "")) for n in re.findall(r"\b\d[\d,]*\b", line)]
    if any(lo <= n <= hi for n in limits):
        out.append(_ok(N_REV_SIZE))
    else:
        out.append(_fail(N_REV_SIZE, "no maximum diff size in lines" if not limits else f"found {_short([str(n) for n in limits])}, which is not a small diff",
                         f"Say how many changed lines a pull request may have, from {lo} to {hi}: a number a reviewer can read carefully in one sitting."))
    # the second human for money logic
    modules = money_modules()
    missing = [m for m in modules if not re.search(rf"\b{re.escape(m)}\b", text)]
    second = (re.search(r"\b(second|2nd|two|another|different|independent)\b[^.\n]{0,40}\b(human|reviewers?|reviews?|approvals?|approver|person|people|pair of eyes|set of eyes)", text, re.I)
              or re.search(r"\b(human|reviewer|approv\w*)\b[^.\n]{0,40}\b(second|in addition|besides|other than|apart from|not the author)\b", text, re.I)
              or re.search(r"\b(?:besides|other than|in addition to|apart from) the author\b|four[- ]eyes", text, re.I))
    problems = ([f"modules not named: {_short(missing, 6)}"] if missing else []) + ([] if second else ["no second human reviewer"])
    out.append(_grade(N_REV_MONEY, problems, "CONTRIBUTING.md says which modules need a second human besides the author: name every one of them."))
    # the author explains and shows evidence
    explains = re.search(r"\bexplain\w*\b", text, re.I)
    evidence = re.search(r"\b(descri\w+|evidence|proof|results?|pasted?|pastes|output|ran|commands? (?:you |they |that |which )?(?:were |was )?(?:run|executed)|"
                         r"what (?:was|you|they) (?:run|ran))\b", text, re.I)
    out.append(_grade(N_REV_AUTHOR, ([] if explains else ["the author is not required to explain the change"]) + ([] if evidence else ["no evidence in the description (commands run, results)"]),
                      "Say what the author must explain and what the pull request description must show."))
    # a response time
    speed = re.search(r"\b(\d+|one|two|three|four)\s*(working |business )?(hours?|days?)\b|\bsame[- ]day\b|\bnext (working |business )?day\b|\bwithin a (working )?day\b|\b\d+\s?h\b", text, re.I)
    out.append(_ok(N_REV_SPEED) if speed else _fail(N_REV_SPEED, "no response time", "Say how long a pull request may wait for its first review, in hours or working days."))
    # advisory: tests come with the change
    # "tests come with the change" may be said in the review norms or in the verification standard
    both = text + ("\n" + verification.text() if verification is not None else "")
    tests = _line_has(both, r"\btests?\b", r"\b(first|before|with the change|alongside|come with|comes with|arrive|accompany|included|must include|new behaviou?r|"
                      r"every change|each change|every pull request|each pull request|with every|with each|together|same pull request|same PR)\b")
    out.append(_ok(N_REV_TESTS) if tests else _fail(N_REV_TESTS, "nothing says tests arrive with the change", "Say when the tests arrive: in the same pull request, or ahead of it."))
    spec = re.search(r"acceptance criteria|non-?goals?|out of scope|definition of done|done means|do not touch", text, re.I)
    out.append(_ok(N_REV_SPEC) if spec else _fail(N_REV_SPEC, "nothing says what a ticket must contain before an agent starts",
                                                  "Acceptance criteria and non-goals are what an agent builds from."))
    return out


# "never modify / change / alter / touch / loosen a test": a verb straight in front of the test (not any "change")
_TEST_TAMPERING = re.compile(
    r"\b(?:chang|modif|alter|tamper|loosen|touch|overwrit|water)\w*\s+(?:with\s+|down\s+)?(?:(?:an?|the|any|all|existing|old|your|their|its)\s+)*"
    r"(?:tests?|test suite|suite|assertions?|expected values?)\b",
    re.I,
)


def verification_checks(section: Section | None) -> list[Check]:
    if section is None:
        return [_fail(N_VERIFY, "the verification standard section is missing", "Add the section from the skeleton."),
                _fail(N_VER_FAIL, "the verification standard section is missing", "Add the section.")]
    text = section.text()
    groups = [
        _g("the test command", r"\bpytest\b"),
        _g("Decimal for money", r"\bDecimal\b"),
        ("that tests are not edited, deleted or skipped to pass", lambda t: _line_has(
            t, r"\b(edit|delet|skip|weaken|disabl|remov|comment(?:ing)? out|rewrit)\w*\b", r"\btests?\b", negated=True)
         or _line_has(t, _TEST_TAMPERING, negated=True)),
    ]
    fail_first = _line_has(text, r"\bfail\w*\b", r"\b(without|before|revert\w*|stash\w*|original|starter|old code|removed|absent)\b")
    return [
        _coverage(N_VERIFY, text, groups, 3, "Name the test command, the rule for money, and what an agent may never do to a test."),
        _ok(N_VER_FAIL) if fail_first else _fail(N_VER_FAIL, "nothing asks to see the new test fail without the change",
                                                  "A test that passes without the change proves nothing: say how the author shows it can fail."),
    ]


def security_check(section: Section | None) -> Check:
    if section is None:
        return _fail(N_SECURITY, "the security baseline section is missing", "Add the section from the skeleton.")
    groups = [
        _g("secrets", r"\b(secrets?|credentials?|api keys?|\.env)\b"),
        _g("production", r"\bproduction\b", negated=True),
        _g("permissions and least privilege", r"\b(least privilege|permissions?|deny rules?|manual mode|default mode|plan mode|acceptEdits|bypass\w*|dangerously\w*)\b"),
        _g("dependencies and invented package names", r"\b(dependenc\w+|packages?|slopsquat\w*|lockfiles?|pip install)\b"),
        _g("untrusted content and prompt injection", r"\b(prompt injection|injection|untrusted|issue text|web pages?|fetched|external content)\b"),
        _g("MCP servers and plugins", r"\b(MCP|connectors?|plugins?|servers?)\b"),
    ]
    return _coverage(N_SECURITY, section.text(), groups, 5,
                     "Cover secrets, production, permissions, dependencies, untrusted content and MCP servers; you may skip one.")


def automation_check(section: Section | None) -> Check:
    if section is None:
        return _fail(N_AUTOMATION, "the automation section is missing", "Add the section from the skeleton.")
    groups = [
        _g("how it is automated (hooks, CI, headless runs)", r"\b(hooks?|CI|pipeline|headless|claude -p|scheduled|pre-?commit|GitHub Actions|workflow|cron)\b"),
        _g("what is never automated", r"\b(never|not|no|must not|without a human|only a human|by hand)\b",
           r"\b(merg\w*|deploy\w*|releas\w*|production|money|credentials|auto-?merge)\b"),
        _g("limits on unattended runs", r"\b(unattended|headless|scheduled|background|claude -p|automated runs?|cron)\b",
           r"\b(max-turns|max-budget|budget|timeouts?|time limit|caps?|limit\w*|ceiling)\b"),
    ]
    return _coverage(N_AUTOMATION, section.text(), groups, 3,
                     "Say how work is automated, what is never automated, and what caps an unattended run (turns, money or minutes).")


def incident_check(section: Section | None) -> Check:
    if section is None:
        return _fail(N_INCIDENT, "the incident handling section is missing", "Add the section from the skeleton.")
    groups = [
        _g("containment (stop it, revoke, revert)", r"\b(contain\w*|stop\w* the agent|revoke\w*|rotate\w*|disabl\w*|kill|revert\w*|roll ?back|isolat\w*|disconnect\w*)\b"),
        _g("keeping the evidence", r"\b(preserve\w*|transcripts?|agent logs?|evidence|keep the|save the)\b"),
        _g("who is called", r"\b(Maha|on-call|SRE|incident (?:commander|lead|manager))\b"),
        _g("a time limit", r"\b(?:\d+|an?|one|two|three|four|five|six|eight|ten|twelve|twenty|thirty|forty|the first)[\s-]*(?:working |business )?(?:minutes?|hours?|days?)\b|\bsame[- ]day\b|\bnext (?:working |business )?day\b"),
        _g("a blameless review", r"\bblameless\b"),
        ("a change to a control afterwards", lambda t: bool(re.search(r"postmortem|post-mortem|follow-?up", t, re.I))
         and bool(re.search(r"\b(hook|rules?|permissions?|memory|CLAUDE\.md|tests?|checklist|playbook|guard|control)\b", t, re.I))),
    ]
    return _coverage(N_INCIDENT, section.text(), groups, 5,
                     "Cover containing it, keeping the evidence, who is called, a deadline, a blameless review and the control you change afterwards.")


def onboarding_check(section: Section | None) -> Check:
    if section is None:
        return _fail(N_ONBOARDING, "the onboarding section is missing", "Add the section from the skeleton.")
    groups = [
        _g("a mentor or pairing", r"\b(mentor\w*|buddy|pair\w*|senior)\b"),
        _g("explaining back", r"\bexplain\w*\b"),
        _g("work done without AI", r"\b(without (?:AI|an? (?:agent|assistant|AI)|the agent|agents?)|no-AI|by hand|AI-free|manual(?:ly)?)\b"),
        _g("a cadence", r"\b(?:\d+|one|two|three|four|six|every|each|weekly|monthly|per|once)\b", r"\b(weeks?|days?|sprints?|months?|quarters?)\b"),
        _g("reading before writing", r"\b(CONTRIBUTING|TOUR|docs/|code reading|read(?:ing)? (?:the )?(?:code|module))\b"),
    ]
    return _coverage(N_ONBOARDING, section.text(), groups, 4,
                     "Say who pairs with a new joiner, what they explain back, when they work without AI, and on what schedule.")


def metric_checks(doc: Doc, section: Section | None) -> list[Check]:
    names = [N_MET_BLOCKS, N_MET_DELIVERY, N_MET_GUARD, N_MET_DEFINED, N_MET_BASELINE, N_MET_VANITY, N_MET_SPLIT]
    if section is None:
        return [_fail(n, "the metrics plan section is missing", "Add the section from the skeleton.") for n in names]
    blocks = metric_blocks(doc, section)
    out: list[Check] = []
    # 1. blocks and fields
    problems = []
    if not blocks:
        problems.append("no metric blocks: use one ### heading per metric with the six fields underneath")
    for block in blocks:
        absent = [f for f in FIELDS if not block.fields.get(f, "").strip()]
        stray = [f for f in FIELDS if has_placeholder(block.fields.get(f, ""))]
        if absent:
            problems.append(f'"{block.name}" lacks {_short(absent, 3)}')
        elif stray:
            problems.append(f'"{block.name}" still has template text in {_short(stray, 2)}')
        elif block.kind == "other":
            problems.append(f'"{block.name}": Kind must be delivery or guard')
    out.append(_grade(N_MET_BLOCKS, [_short(problems, 2)] if problems else [],
                      "Each metric: a ### heading, then Kind, Definition, Source, Cadence, Baseline and Threshold."))
    # 2. delivery
    delivery = [b for b in blocks if b.kind == "delivery"]
    fams = {family(b.name) for b in delivery} - {None}
    out.append(_ok(N_MET_DELIVERY, ", ".join(sorted(fams))) if len(fams) >= MIN_DELIVERY else
               _fail(N_MET_DELIVERY, f"{len(delivery)} delivery block(s), {len(fams)} recognised: {_short(sorted(fams), 4) or 'none'}",
                     "Name at least three of DORA's: lead time, deployment frequency, change failure rate, recovery time, rework rate."))
    # 3. guard
    guards = [b for b in blocks if b.kind == "guard"]
    gp = []
    if len(guards) < MIN_GUARD:
        gp.append("no guard metric")
    for block in guards:
        found = threshold_problems(block.fields.get("Threshold", ""))
        if found:
            gp.append(f'"{block.name}": {_short(found, 3)}')
    out.append(_grade(N_MET_GUARD, gp, "A guard's Threshold needs a number, a comparison and what we do when it is crossed."))
    real = [b for b in blocks if not any(has_placeholder(v) for v in b.fields.values())]
    if not real:
        waiting = "waiting for a filled-in metric block"
        hint = "Write the metric blocks first."
        out += [_fail(N_MET_DEFINED, waiting, hint), _fail(N_MET_BASELINE, waiting, hint), _fail(N_MET_VANITY, waiting, hint)]
        out.append(_fail(N_MET_SPLIT, waiting, hint))
        return out
    # 4. definitions
    dp = []
    for block in blocks:
        found = definition_problems(block)
        if found:
            dp.append(f'"{block.name}": {found[0]}')
    out.append(_grade(N_MET_DEFINED, [_short(dp, 2) + (f" ({len(dp)} metrics in all)" if len(dp) > 2 else "")] if dp else [],
                      "Two people with the same data must get the same number: say what is counted or timed, between which events, over which period."))
    # 5. baselines
    bp = [problem for problem in (baseline_problem(block) for block in blocks) if problem]
    out.append(_grade(N_MET_BASELINE, [_short(bp, 2)] if bp else [],
                      "Use only the figures in lab-assets/team-context.md, in the same unit or an equivalent one (52 hours, about 2 days); "
                      "for any metric the table does not cover, write \"to be measured\"."))
    # 6. vanity
    vp = []
    flagged: list[tuple[int, int]] = []  # the line ranges of blocks already named, so their lines are not listed again
    for block in blocks:
        blob = block.name + " " + block.fields.get("Definition", "")
        if _VANITY.search(blob):
            vp.append(f'"{block.name}"')
            flagged.append((block.line, block.end))
        elif is_adoption(block) and not NEGATION.search(block.fields.get("Threshold", "")):
            vp.append(f'"{block.name}" puts a target on adoption')
            flagged.append((block.line, block.end))
    lines = doc.logical()
    for index, (number, line) in enumerate(lines):
        if line.startswith("#") or any(a <= number < b for a, b in flagged):
            continue
        if any(_VANITY.search(sentence) and not NEGATION.search(sentence) for sentence in sentences(line)) \
                and not _negated_by_intro(lines, index):
            vp.append(f"line {number + 1}")
    out.append(_grade(N_MET_VANITY, [_short(list(dict.fromkeys(vp)), 3)] if vp else [],
                      "Lines of code, suggestion acceptance and the share of AI-written code reward volume, wherever they appear in the playbook. "
                      "Measure what reaches production and what it costs."))
    # 7. advisory: compare AI-assisted with the rest
    text = section.text()
    split = re.search(r"AI-assisted", text) and re.search(r"\b(compar\w+|split|segment\w*|versus|vs\.?|against|separately|break ?down|by label|other pull requests|non-AI|not labelled)\b", text, re.I)
    out.append(_ok(N_MET_SPLIT) if split else _fail(N_MET_SPLIT, "no metric is looked at separately for AI-assisted changes",
                                                    "The label is also a way to measure: compare AI-assisted pull requests with the others, without a target on the share."))
    return out


_AI = r"(?:AI|agents?|bots?|Copilot|Claude|LLMs?|automated)"
_CONTRADICTIONS: tuple[tuple[str, re.Pattern[str], bool], ...] = (
    # (what it says, pattern, True when a negation or restriction on the same line excuses it)
    ("float is fine for money", re.compile(r"\b(use|uses|using|may use|can use|allowed|acceptable|fine|ok|okay|permitted)\b[^.\n]{0,40}\bfloats?\b", re.I), True),
    ("bypass mode is allowed everywhere", re.compile(r"dangerously-skip-permissions|bypassPermissions|bypass (?:mode|permissions)", re.I), True),
    ("the label is optional", re.compile(r"\blabel\w*\b[^.\n]{0,60}\boptional\b|\boptional\b[^.\n]{0,60}\blabel", re.I), False),
    ("the second reviewer is optional", re.compile(r"second (?:human )?review\w*[^.\n]{0,60}\b(optional|not required|only if|unless)\b|\b(optional|skip|waive\w*)\b[^.\n]{0,40}second (?:human )?review", re.I), False),
    ("tests are optional", re.compile(r"\b(?:tests?|test coverage)\b[^.\n]{0,30}\b(?:optional|not required|can be skipped|may be skipped|may be omitted)\b", re.I), False),
    ("authors may approve their own change", re.compile(r"\bself[- ](?:approv|merg)\w*|\b(?:approve|merge) (?:their|your|his|her|its) own\b", re.I), True),
    ("the author can be the second reviewer", re.compile(
        r"\bsame person (?:who|that|as)\b[^.\n]{0,30}\b(?:wrote|authored|opened|prompted|made)\b|"
        r"\b(?:author|submitter|developer)\b[^.\n]{0,20}\b(?:may|can|could)\s+(?:also\s+)?(?:be|act as|serve as|count as)\b[^.\n]{0,20}\b(?:review\w*|approv\w*)|"
        r"\breviewer\b[^.\n]{0,20}\b(?:may|can|could)\s+be\s+the\s+(?:author|same)|\bself-review\w*\s+(?:is|are|counts?)\b", re.I), True),
    ("an AI review can replace the human one", re.compile(
        rf"\b{_AI}\b[^.\n]{{0,40}}\b(?:can|may|will) (?:replace|substitute|count as|serve as|stand in for)\b[^.\n]{{0,40}}\b(?:second|human|reviewer)|"
        rf"\b(?:second|2nd|other|additional)\s+(?:human\s+)?(?:review\w*|approv\w*|look|pair of eyes)\b[^.\n]{{0,60}}\b(?:may|can|could|might|is allowed to)\s+be\s+(?:an?\s+)?{_AI}\b|"
        rf"\b{_AI}\s+(?:code\s+)?(?:review\w*|approv\w*)\s+(?:also\s+|still\s+)?(?:counts?|is\s+(?:enough|sufficient|fine|acceptable|allowed|ok(?:ay)?)|satisf\w+|suffices?|qualif\w+)\b|"
        rf"\b(?:or|including|even|such as)\s+(?:by\s+)?an?\s+{_AI}\b[^.\n]{{0,25}}\b(?:review\w*|approv\w*|reviewer)\b|"
        rf"\b{_AI}\b[^.\n]{{0,60}}\b(?:counts?|serves?|stands?|acts?|qualif\w+)\s+(?:as|in for)\s+(?:the\s+)?(?:second|human)\b", re.I), True),
    ("AI-written code needs less review", re.compile(
        rf"\bAI[- ](?:written|generated|assisted)\b[^.\n]{{0,40}}\b(?:needs?|requires?|gets?|receives?)\s+(?:less|lighter|fewer|no)\s+(?:review|scrutiny|checks?)\b|"
        rf"\b(?:skip|waive|bypass)\w*\s+(?:the\s+)?review\b[^.\n]{{0,30}}\bAI\b", re.I), True),
    ("personal accounts are allowed", re.compile(
        r"\b(?:personal|free[- ]tier|private)\s+(?:accounts?|subscriptions?|licen[cs]es?|plans?|tiers?)\b[^.\n]{0,40}\b(?:are|is|may be|can be|allowed|fine|ok|okay|acceptable|permitted|welcome)\b", re.I), True),
    ("Confidential or Restricted data may go into prompts", re.compile(
        r"\b(?:Confidential|Restricted)\b[^.\n]{0,60}\b(?:may|can|is allowed|are allowed|is fine|is ok|is acceptable|is permitted)\b[^.\n]{0,40}\b(?:prompts?|pasted?|shared?|sent|agents?|contexts?|tools?)\b", re.I), True),
    ("dependencies need no ticket", re.compile(
        r"\bdependenc\w+[^.\n]{0,40}\b(?:freely|at will|without (?:a )?(?:ticket|review|approval|second reviewer)|no (?:ticket|approval) (?:is )?needed)\b", re.I), True),
    ("agents may use production", re.compile(r"\bagents?\b[^.\n]{0,40}\b(?:may|can|are allowed to|is allowed to|have access to)\b[^.\n]{0,50}\bproduction\b", re.I), True),
)
_RESTRICTION = re.compile(r"isolat|container|sandbox|\bVMs?\b|throw-?away|without credentials|no network", re.I)
_NOT_OPTIONAL = re.compile(r"\b(?:not|never|isn'?t|aren'?t)\s+optional\b|\bnon-?optional\b|\bmandatory\b", re.I)

# The second human reviewer for money logic has no exceptions and no discretion (CONTRIBUTING.md, the bank's fifth rule).
_MONEY_REF = re.compile(r"money logic|money modules?|money code|\b(?:money|fees|fx|limits|ledger|service)\.py\b|\bsix (?:money )?modules\b|\bthe six\b", re.I)
_REVIEW_REF = re.compile(r"\breview\w*|\bapprov\w*|\bsecond\b|\bsign-?off\b|\bsecond look\b", re.I)
_AUTHOR_OK = re.compile(r"\b(?:except|other than|apart from|besides|but not)\s+(?:for\s+)?(?:the\s+)?(?:author|submitter|committer)\b", re.I)
_EXEMPT = re.compile(
    r"\bunless\b|\bexcept\b|\bexempt\w*|\b(?:waiv|skip)\w*\b[^.;]{0,25}\b(?:review\w*|approv\w*|second)\b|"
    r"\b(?:review\w*|approv\w*|second)\b[^.;]{0,25}\b(?:waiv|skip)\w*|\boptional\b|\bnot required\b|\bonly if\b|\bonly when\b|"
    r"\b(?:from|by) (?:no one|nobody)\b|\bno (?:second )?(?:review\w*|approval)\b[^.\n]{0,20}\b(?:needed|required)\b|"
    r"\bat the (?:author|reviewer|team)'?s? discretion\b|"
    r"\b(?:if|when|whenever)\s+(?:the\s+)?(?:author|developer|engineer|submitter|owner)\s+(?:thinks|feels|believes|decides|judges|considers|wants|chooses)\b|"
    r"\b(?:if|when|where)\s+(?:the change|it|they)\s+(?:is|are|looks?)\s+(?:small|tiny|trivial|minor|low[- ]risk|urgent|risky|safe|simple)\b|"
    r"\b(?:when|if|where|for|unless)\b[^.;]{0,40}\b(?:under|below|fewer than|less than)\s+\d+\s+(?:changed\s+)?lines?\b",
    re.I,
)


def sentences(text: str) -> list[str]:
    """Split prose into sentences (a rule's "MUST ... Check: ..." is two); abbreviations such as e.g. do not split."""
    protected = re.sub(r"\b(e\.g|i\.e|etc|vs|et al|approx|incl)\.", lambda hit: hit.group(0).replace(".", "\u2024"), text, flags=re.I)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z`(\[*\"'])", protected)
    return [part.replace("\u2024", ".").strip() for part in parts if part.strip()]


def contradiction_check(doc: Doc) -> Check:
    hits = []
    for number, line in doc.logical():
        for sentence in sentences(line):  # one sentence at a time: a negation elsewhere in the paragraph excuses nothing
            for label, pattern, excusable in _CONTRADICTIONS:
                if pattern.search(sentence):
                    if excusable and (NEGATION.search(sentence) or _RESTRICTION.search(sentence)):
                        continue
                    if "optional" in label and _NOT_OPTIONAL.search(sentence):
                        continue
                    hits.append(f"line {number + 1} ({label})")
            plain = _AUTHOR_OK.sub(" ", sentence)
            if _MONEY_REF.search(plain) and _REVIEW_REF.search(plain) and _EXEMPT.search(plain) \
                    and not _NOT_OPTIONAL.search(plain):
                hits.append(f"line {number + 1} (the second human reviewer for money logic has an exception)")
    return _grade(N_CONTRADICT, [_short(list(dict.fromkeys(hits)), 3)] if hits else [],
                  "The playbook sits under the bank's six rules and CONTRIBUTING.md. It can be stricter, never looser: "
                  "no exceptions or discretion for the second human reviewer, no AI review in its place.")


def production_check(doc: Doc) -> Check:
    for _, line in doc.logical():
        if re.search(r"\bproduction\b", line, re.I) and NEGATION.search(line) and re.search(r"\b(agents?|AI|tools?|assistants?|Claude|Copilot)\b", line, re.I):
            return _ok(N_PROD)
    return _fail(N_PROD, "nothing says agents never touch production",
                 "The bank's fourth rule: say it in your own words, and say how the team stops an agent getting production credentials.")


_BACKTICK = re.compile(r"`([^`\n]+)`")
_FILE_EXTENSIONS = (".py", ".md", ".yml", ".yaml", ".json", ".toml", ".txt", ".cfg", ".ini", ".sh", ".lock")
_BARE_FILENAMES = frozenset({"CODEOWNERS", "Makefile", "Dockerfile", "LICENSE", "CHANGELOG"})
_KNOWN_FOLDERS = frozenset({"src", "tests", "docs", "lab-assets", "scripts", ".github", ".claude", "tools", "hooks", "bin", "config", "ci"})
_LOCAL_ONLY = re.compile(r"^\.env(?:\.[\w-]+)?$")  # a developer's own .env file: git ignores it, and a deny rule may name it
# "a new `CODEOWNERS` file", "we create `scripts/check.py`", "proposed": the sentence that names a file says it does not exist yet
_NEW = re.compile(
    r"\b(?:new|creat\w+|propos\w+|introduc\w+|to build|to be (?:built|created|added|written|made)|yet to be|"
    r"(?:does|do|did) not (?:yet )?exist|doesn'?t exist|not yet (?:exist\w*|built|created|written))\b",
    re.I,
)


_PRONOUN_START = re.compile(r"\s*(?:It|This|That|They|These|Those|Both)\b")


def _repo_names(work: Path) -> tuple[set[str], set[str]]:
    """Every file and folder of the repository (relative, with '/'), and every bare file name."""
    paths: set[str] = set()
    names: set[str] = set()
    for root, dirs, files in os.walk(work):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", ".pytest_cache")]
        relative = Path(root).relative_to(work).as_posix()
        for name in dirs + files:
            paths.add(name if relative == "." else f"{relative}/{name}")
            names.add(name)
    return paths, names


def _file_token(token: str) -> str | None:
    """The path a backticked token names, or None when it is not a file or folder name."""
    token = token.strip().rstrip(".,;:)").lstrip("@")
    if token.startswith("./"):
        token = token[2:]
    if not token or re.search(r"[*<>{}$\u2026\s()]|\.\.\.|://", token) or not re.fullmatch(r"[\w.\-/]+", token):
        return None
    if not re.search(r"[A-Za-z]", token):
        return None
    name = token.rstrip("/")
    if "/" in name:
        first = name.split("/", 1)[0]
        if token.endswith("/") or name.lower().endswith(_FILE_EXTENSIONS) or first in _KNOWN_FOLDERS:
            return name
        return None
    if name.lower().endswith(_FILE_EXTENSIONS) or name in _BARE_FILENAMES or (name.startswith(".") and len(name) > 1):
        return name
    return None


# a path written without backticks still counts when it has folders and a file extension: docs/SECURITY.md, src/remit/risk.py
_PLAIN_PATH = re.compile(r"(?<![\w/.@:-])((?:\.?[\w-]+/)+[\w.-]*[\w-]\.(?:py|md|yml|yaml|json|toml|txt|cfg|ini|sh))(?![\w/-])")
_URL = re.compile(r"https?://\S+")
_NEAR = 60  # a "new" or "proposed" counts when it stands within this many characters of the path


def _path_mentions(sentence: str) -> list[tuple[str, int, int]]:
    """(path, start, end) of every file or folder a sentence names: in backticks, or as a plain folder/file path."""
    found: list[tuple[str, int, int]] = []
    for hit in _BACKTICK.finditer(sentence):
        path = _file_token(hit.group(1))
        if path is not None and not _LOCAL_ONLY.match(path):
            found.append((path, hit.start(), hit.end()))
    plain = _BACKTICK.sub(lambda hit: " " * len(hit.group(0)), _URL.sub(lambda hit: " " * len(hit.group(0)), sentence))
    for hit in _PLAIN_PATH.finditer(plain):
        path = _file_token(hit.group(1))
        if path is not None and not _LOCAL_ONLY.match(path):
            found.append((path, hit.start(1), hit.end(1)))
    return found


def paths_check(work: Path, doc: Doc) -> Check:
    """Every file or folder the playbook names exists, or the words around it call it new or proposed."""
    paths, names = _repo_names(Path(work))
    mentions: list[tuple[str, int]] = []   # (path, line) in reading order
    declared: set[str] = set()
    for number, line in doc.logical():
        parts = sentences(line)
        for index, sentence in enumerate(parts):
            # "The memory file is `CLAUDE.md`. It does not exist yet." : a sentence that starts with "It" or "This" speaks about the one before
            follow = parts[index + 1] if index + 1 < len(parts) else ""
            spoken_after = bool(_PRONOUN_START.match(follow) and _NEW.search(follow))
            for path, start, end in _path_mentions(sentence):
                mentions.append((path, number + 1))
                if spoken_after or _NEW.search(sentence[max(0, start - _NEAR):end + _NEAR]):
                    declared.add(path)
    missing: list[str] = []
    for path, number in mentions:
        exists = path in paths or ("/" not in path and path in names)
        if not exists and path not in declared:
            missing.append(f"`{path}` (line {number})")
    return _grade(N_PATHS, [_short(list(dict.fromkeys(missing)), 3)] if missing else [],
                  "Look in the repository (docs/ARCHITECTURE.md is partly out of date, and an assistant will happily repeat it); "
                  "lab-assets/team-context.md says what exists today. A file that does not exist yet is fine when the words next to it "
                  "call it new or proposed, for example \"a new `CODEOWNERS` file\".")


_CLAIM = re.compile(
    r"\b(?:studies|research|surveys?|experts?|analysts?|benchmarks?)\s+(?:shows?|proves?|found|finds?|suggests?|indicates?|says?|confirms?|demonstrates?|reveals?)\b|"
    r"\baccording to (?:a|an|the|recent|several|multiple|one|some)(?:\s+[\w-]+){0,3}\s+(?:study|studies|survey|surveys|research|analysis|white ?paper|trial|"
    r"(?:industry|analyst|vendor|market|research|survey|annual) reports?)\b|"
    r"\b\d+\s?[x\u00d7]\s+(?:faster|more productive|productivity)\b|\b\d{2,3}\s?%\s+(?:faster|more productive|productivity|increase in productivity|gains?)\b|"
    r"\bindustry (?:average|standard|benchmark)s?\b|\b(?:10|ten)x\b|"
    # the same claims in other words: doubling, "far faster", hours saved, an AI verb with a quantity
    r"\b(?:double[sd]?|doubling|triple[sd]?|tripling|halve[sd]?|quadruple[sd]?)\b[^.\n]{0,60}\b(?:productiv\w*|output|velocity|throughput|speed|ship\w*|deliver\w*|faster|code)\b|"
    r"\b(?:much|far|significantly|dramatically|substantially|vastly|considerably)\s+(?:faster|more productive|more efficient|quicker)\b|"
    r"\bsav(?:e|es|ing)\s+(?:\w+\s+){0,3}(?:hours?|days?|minutes?)\s+(?:a|per|each|every)\s+(?:day|week|developer|engineer)\b|"
    r"\b(?:AI|assistants?|agents?|Copilot|Claude|LLMs?|the tools|these tools)\b[^.\n]{0,60}\b(?:makes?|made|speeds?|boosts?|cuts?|reduces?|saves?|increases?|improves?|raises?|multipl\w+)\b"
    r"[^.\n]{0,60}(?:\d+\s?%|\d+\s?[x\u00d7]|\b(?:two|three|four|five|ten)\s+times\b|\btwice as\b|\bhalf the\b|"
    r"\b(?:a|one)\s+(?:third|quarter|half|fifth)\b|\b(?:two|three)[- ](?:thirds|quarters)\b)",
    re.I,
)
# A source in the same sentence: a link, "et al", a named study, or a named organisation together with a year or a report.
_SOURCE = re.compile(
    r"https?://|\bet al\b|\b(?:METR|DORA|Accelerate|Stack Overflow|arXiv|SSRN)\b|"
    r"\b(?:Google|Microsoft|GitHub|Anthropic|Meta|McKinsey|Gartner|Forrester|IDC|Atlassian|JetBrains|Accenture|GitClear|Uplevel|Cui)\b"
    r"[^.\n]{0,60}\b(?:20\d\d|(?i:study|studies|survey|trial|report|paper|experiment))\b|"
    r"\b(?:20\d\d)\b[^.\n]{0,40}\b(?i:study|survey|trial|report|paper)\b",
)


def claims_check(doc: Doc) -> Check:
    hits = []
    for number, line in doc.logical():
        for sentence in sentences(line):
            if _CLAIM.search(sentence) and not re.search(_SOURCE, sentence):
                hits.append(f"line {number + 1}")
                break
    return _grade(N_CLAIMS, [f"claim without a source at {_short(hits, 3)}"] if hits else [],
                  "A playbook is policy, not evidence. Delete the claim, or name the study (and its limits) in the same sentence.")


def distinct_check(sections: dict[str, Section]) -> Check:
    seen: dict[str, str] = {}
    dupes = []
    for key, section in sections.items():
        body = _norm_text(section.text())
        if len(body.split()) < 15:
            continue
        if body in seen:
            dupes.append(f"{TITLES[key]} = {TITLES[seen[body]]}")
        seen[body] = key
    return _grade(N_DISTINCT, [_short(dupes, 2)] if dupes else [], "Each section answers a different question.")


# ---------------------------------------------------------------------------------------------------------
# putting it together
# ---------------------------------------------------------------------------------------------------------
def playbook_checks(work: Path) -> list[Check]:
    """Every check about ``playbook.md`` itself, in a stable order. Without the file each one waits."""
    loaded = load(work)
    if loaded is None:
        waiting = "waiting for playbook.md"
        out = [_fail(N_EXISTS, "there is no playbook.md in the repository root", "Copy the skeleton's idea: one file, playbook.md, at the root.")]
        out += [_fail(n, waiting, "Write playbook.md first.") for n in ALL_NAMES if n in _FILE_CHECKS and n != N_EXISTS]
        return out
    doc, sections = loaded
    rules = extract_rules(doc, sections)
    pick = sections.get
    results: list[Check] = [_ok(N_EXISTS)]
    results += [sections_check(doc, sections), placeholders_check(doc), length_check(doc)]
    results += rule_checks(rules)
    results += [tools_check(pick("tools")), data_check(pick("data"))]
    results += context_checks(pick("context"))
    results += review_checks(pick("review"), pick("verification"))
    results += verification_checks(pick("verification"))
    results += [security_check(pick("security")), automation_check(pick("automation")), incident_check(pick("incident")),
                onboarding_check(pick("onboarding"))]
    results += metric_checks(doc, pick("metrics"))
    results += [contradiction_check(doc), production_check(doc), paths_check(work, doc), claims_check(doc), distinct_check(sections)]
    order = {name: i for i, name in enumerate(ALL_NAMES)}
    return sorted(results, key=lambda c: order[c.name])


_FILE_CHECKS = set(ALL_NAMES) - {N_SCOPE, N_SECRETS, N_COMMITS, N_CLEAN}


def repository_checks(work: Path) -> list[Check]:
    """Scope, secrets and commit hygiene, the same in every lab."""
    return [
        checks.files_changed_within(
            work, ALLOWED_FILES, name=N_SCOPE,
            hint="This lab changes playbook.md only. Do not edit CONTRIBUTING.md, the tests or lab-assets/ to fit your playbook: "
                 "the playbook sits under them.",
        ),
        checks.no_secrets(work, name=N_SECRETS),
        _commit_hint(checks.conventional_commits(work, name=N_COMMITS)),
        checks.all_committed(work, name=N_CLEAN),
    ]


def _commit_hint(check: Check) -> Check:
    """"Commit your change" is wrong advice for a learner who did commit, but on another branch; "amend" fixes only the last commit."""
    if check.ok:
        return check
    if "found 0 commits" in check.detail:
        check.hint = ("The grader counts the commits on the branch that is checked out in this directory, since the lab-start tag. "
                      "Commit playbook.md here (git add playbook.md, then git commit -m \"docs(playbook): ...\"), "
                      "or switch to the branch where you committed (git switch <branch>).")
    else:
        check.hint = ("Every commit since the start is checked. Format: type(scope): subject, a lower-case scope, at most 72 characters, no full stop. "
                      "Reword the last commit with git commit --amend; to fix older ones, undo them with git reset --soft lab-start and commit again.")
    return check


def all_checks(work: Path) -> list[Check]:
    return playbook_checks(work) + repository_checks(work)
