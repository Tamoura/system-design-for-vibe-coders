"""Helpers for lab m11 (lesson 11.2): checks that trace what a document CLAIMS back to its SOURCE.

A new file next to the shared helpers, used only by ``labs/m11_lifecycle``. Nothing here changes the kit's
framework or ``checks.py``. The idea of the lab is the idea of the code: a grader cannot judge whether prose
is *good*, but it can find prose that is *false*, because every claim in the three documents points at a
thing that can be looked up:

* an ADR points at the repository (paths, ``module.name`` symbols, constants);
* the najmkit page points at the library's code (names, signatures, examples that can be run);
* the postmortem points at the incident record (event ids, times, counts, severity).

Everything is deterministic, offline and standard library only. Learner code is only ever run in a
subprocess with a timeout, on a throw-away copy (``run_doc_examples``).

Layout: (1) text and Markdown helpers, (2) a code index of ``src/``, (3) a small rule engine for
"this sentence contradicts the code", (4) ADR checks, (5) najmkit page checks, (6) postmortem checks.
"""
from __future__ import annotations

import ast
import json
import re
import tempfile
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from ailab import checks, runner

# =================================================================================
# 1. text and Markdown helpers
# =================================================================================
_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_FENCE_LINE = re.compile(r"^\s*(```|~~~)")

NEGATION = re.compile(
    r"\b(no|not|never|none|nothing|without|cannot|unlike|rather than|instead of|instead|than|unknown|unclear|"
    r"unconfirmed|whether|if)\b|n't",
    re.I,
)
DOCSTRING_TALK = re.compile(r"docstring|comment|\bsays\b|\bclaims?\b|stale|outdated|wrong|incorrect|misleading", re.I)


def snippet(text: str, limit: int = 110) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def code_blocks(text: str) -> list[tuple[str, str]]:
    """(language, body) of every fenced code block."""
    blocks: list[tuple[str, str]] = []
    lang, body, marker = "", [], None
    for line in text.splitlines():
        m = _FENCE_LINE.match(line)
        if m and marker is None:
            marker, lang, body = m.group(1), line.strip()[3:].strip().split(" ")[0].lower(), []
        elif m and marker == m.group(1):
            blocks.append((lang, "\n".join(body)))
            marker = None
        elif marker is not None:
            body.append(line)
    return blocks


def prose_only(text: str) -> str:
    """The text with fenced code blocks removed (lines blanked, so line numbers survive)."""
    out, marker = [], None
    for line in text.splitlines():
        m = _FENCE_LINE.match(line)
        if m and marker is None:
            marker = m.group(1)
            out.append("")
        elif m and marker == m.group(1):
            marker = None
            out.append("")
        else:
            out.append("" if marker else line)
    return "\n".join(out)


def units(text: str) -> list[str]:
    """Sentences, with hard-wrapped lines joined: the grain at which rules look for a contradiction.

    A new block starts at a blank line, a heading, a list item or a table row; other lines continue the block above.
    """
    blocks: list[str] = []
    current: list[str] = []

    def flush() -> None:
        if current:
            blocks.append(" ".join(current))
            current.clear()

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            flush()
            continue
        if _BULLET.match(line) or stripped.startswith(("|", "#", ">")):
            flush()
        current.append(stripped)
        if stripped.startswith(("|", "#")):
            flush()
    flush()
    found: list[str] = []
    for block in blocks:
        for part in re.split(r"(?<=[.!?])\s+(?=[A-Z`\"'(\[])", block):
            if part.strip():
                found.append(part.strip())
    return found


@dataclass
class Sec:
    level: int
    title: str
    body: str  # up to the next heading of any level
    full: str  # including deeper sub-sections


def outline(text: str) -> list[Sec]:
    lines = text.splitlines()
    heads: list[tuple[int, int, str]] = []
    marker = None
    for i, line in enumerate(lines):
        m = _FENCE_LINE.match(line)
        if m and marker is None:
            marker = m.group(1)
            continue
        if m and marker == m.group(1):
            marker = None
            continue
        if marker:
            continue
        h = _HEADING.match(line)
        if h:
            heads.append((i, len(h.group(1)), h.group(2).strip()))
    sections: list[Sec] = []
    for n, (i, level, title) in enumerate(heads):
        nxt = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
        end_full = next((j for j, lvl, _ in heads[n + 1:] if lvl <= level), len(lines))
        sections.append(Sec(level, re.sub(r"[`*_]", "", title), "\n".join(lines[i + 1:nxt]).strip(),
                            "\n".join(lines[i + 1:end_full]).strip()))
    return sections


def find_section(sections: Sequence[Sec], pattern: str, *, min_level: int = 2) -> Sec | None:
    rx = re.compile(pattern, re.I)
    return next((s for s in sections if s.level >= min_level and rx.search(s.title)), None)


_BULLET = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")


def list_items(text: str) -> list[str]:
    """The top-level items of a section: bullets or numbered items (with their nested lines), else the rows
    of a table, else sub-headings, else bold-led paragraphs, else plain paragraphs."""
    lines = text.splitlines()
    bullets = [(i, len(m.group(1).expandtabs(4)), m) for i, ln in enumerate(lines) if (m := _BULLET.match(ln))]
    if bullets:
        top = min(ind for _, ind, _ in bullets)
        starts = [i for i, ind, _ in bullets if ind == top]
        items = []
        for n, s in enumerate(starts):
            e = starts[n + 1] if n + 1 < len(starts) else len(lines)
            items.append(" ".join(x.strip() for x in lines[s:e] if x.strip()))
        return items
    rows = [ln for ln in lines if ln.strip().startswith("|")]
    rows = [r for r in rows if not re.fullmatch(r"\s*\|?[\s:|-]+\|?\s*", r)]
    if len(rows) >= 2:
        return rows[1:]  # the first row is the header
    heads = [i for i, ln in enumerate(lines) if _HEADING.match(ln)]
    if heads:
        items = []
        for n, s in enumerate(heads):
            e = heads[n + 1] if n + 1 < len(heads) else len(lines)
            items.append(" ".join(x.strip() for x in lines[s:e] if x.strip()))
        return items
    paragraphs = [" ".join(p.split()) for p in re.split(r"\n\s*\n", text) if p.strip()]
    return paragraphs


# =================================================================================
# 2. a code index of src/
# =================================================================================
@dataclass
class Param:
    name: str
    kind: str  # "pos" (positional or keyword), "posonly", "kwonly", "var" (*args), "varkw" (**kwargs)
    required: bool = True


@dataclass
class ModuleInfo:
    name: str  # "remit.limits"
    short: str  # "limits"
    path: str  # "src/remit/limits.py"
    names: set[str] = field(default_factory=set)  # top-level names, public and private
    classes: dict[str, set[str]] = field(default_factory=dict)  # class -> its members
    sigs: dict[str, list[Param]] = field(default_factory=dict)  # "new_id", "FixedClock" (its __init__), "FixedClock.advance"
    lines: int = 0
    text: str = ""

    def has_member_anywhere(self, name: str) -> bool:
        return any(name in members for members in self.classes.values())


def _params(fn: ast.FunctionDef | ast.AsyncFunctionDef, *, drop_first: bool) -> list[Param]:
    a = fn.args
    pos = [*a.posonlyargs, *a.args]
    defaults = len(a.defaults)
    out: list[Param] = []
    for n, arg in enumerate(pos):
        required = n < len(pos) - defaults
        out.append(Param(arg.arg, "posonly" if n < len(a.posonlyargs) else "pos", required))
    if drop_first and out:
        out = out[1:]
    if a.vararg:
        out.append(Param(a.vararg.arg, "var", False))
    for arg, default in zip(a.kwonlyargs, a.kw_defaults):
        out.append(Param(arg.arg, "kwonly", default is None))
    if a.kwarg:
        out.append(Param(a.kwarg.arg, "varkw", False))
    return out


def _targets(node: ast.stmt) -> Iterable[str]:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            for n in ast.walk(t):
                if isinstance(n, ast.Name):
                    yield n.id
    elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        yield node.target.id


class CodeIndex:
    """What ``src/`` defines, found by reading the code (nothing is imported)."""

    def __init__(self, work: Path | str) -> None:
        self.work = Path(work)
        self.modules: dict[str, ModuleInfo] = {}
        self.by_short: dict[str, ModuleInfo] = {}
        self.class_homes: dict[str, list[ModuleInfo]] = {}
        for path in sorted((self.work / "src").rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            text = read(path)
            if text is None:
                continue
            try:
                tree = ast.parse(text)
            except SyntaxError:
                continue
            package = path.parent.name
            info = ModuleInfo(f"{package}.{path.stem}", path.stem, path.relative_to(self.work).as_posix(),
                              lines=len(text.splitlines()), text=text)
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    info.names.add(node.name)
                    info.sigs[node.name] = _params(node, drop_first=False)
                elif isinstance(node, ast.ClassDef):
                    info.names.add(node.name)
                    members: set[str] = set()
                    for member in node.body:
                        if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            members.add(member.name)
                            info.sigs[f"{node.name}.{member.name}"] = _params(member, drop_first=True)
                            if member.name == "__init__":
                                info.sigs[node.name] = _params(member, drop_first=True)
                        else:
                            members.update(_targets(member))
                    info.classes[node.name] = members
                    info.sigs.setdefault(node.name, [])
                    self.class_homes.setdefault(node.name, []).append(info)
                else:
                    info.names.update(_targets(node))
            self.modules[info.name] = info
            if path.stem != "__init__":
                self.by_short[path.stem] = info

    # -- references ---------------------------------------------------------------------------
    def resolve_path(self, token: str) -> bool | None:
        """True/False if ``token`` is a path that should exist (or not); None when it is not a repository reference."""
        m = re.fullmatch(r"(?:\./)?((?:[\w.-]+/)*[\w.-]+\.(\w+))(?::(\d+|[A-Za-z_][\w.]*))?", token)
        if not m:
            return None
        path, ext, suffix = m.group(1), m.group(2).lower(), m.group(3)
        roots = ("src", "tests", "docs", "lab-assets", ".github")
        is_ref = ext == "py" or path.split("/")[0] in roots
        target = self.work / path
        found: Path | None = target if target.is_file() else None
        if found is None and "/" not in path:
            hits = [*(self.work / "src").rglob(path), self.work / "tests" / path, self.work / "docs" / path, self.work / path]
            found = next((h for h in hits if h.is_file()), None)
            is_ref = is_ref or found is not None
        if not is_ref:
            return None
        if found is None:
            return False
        if suffix:
            body = read(found) or ""
            if suffix.isdigit():
                return int(suffix) <= max(1, len(body.splitlines()))
            return all(re.search(rf"\b{re.escape(part)}\b", body) for part in suffix.split("."))
        return True

    def resolve_symbol(self, token: str) -> bool | None:
        """True/False for ``module.name`` and ``Class.member`` references; None when it is not clearly one."""
        token = re.sub(r"\(.*$", "", token.strip())
        if not re.fullmatch(r"[A-Za-z_]\w*(\.[A-Za-z_]\w*)+", token):
            return None
        parts = token.split(".")
        if parts[0] in ("remit", "najmkit"):
            module = self.modules.get(".".join(parts[:2]))
            if module is None:
                return False
            rest = parts[2:]
        elif parts[0] in self.by_short:
            module, rest = self.by_short[parts[0]], parts[1:]
        elif parts[0][:1].isupper() and parts[0] in self.class_homes:
            homes = self.class_homes[parts[0]]
            return any(parts[1] in m.classes[parts[0]] for m in homes)
        else:
            return None
        if not rest:
            return True
        first = rest[0]
        if first in module.names:
            if len(rest) > 1 and first in module.classes:
                return rest[1] in module.classes[first]
            return True
        return module.has_member_anywhere(first)  # `clock.advance`: an instance named after its module


def read_facts(work: Path | str) -> dict[str, str]:
    """Version facts read from the code itself: najmkit's ``__version__`` and ``API_VERSION``."""
    text = read(Path(work) / "src" / "najmkit" / "__init__.py") or ""
    version = re.search(r'__version__\s*=\s*"([^"]+)"', text)
    api = re.search(r'API_VERSION\s*=\s*"([^"]+)"', text)
    return {"version": version.group(1) if version else "", "api": api.group(1) if api else ""}


# =================================================================================
# 3. a small rule engine: "this sentence contradicts the code"
# =================================================================================
@dataclass(frozen=True)
class Rule:
    id: str
    pattern: re.Pattern[str]
    message: str
    expect: Callable[[re.Match[str]], bool] | None = None  # when given: the claim is fine if it returns True
    exempt: re.Pattern[str] | None = None  # a sentence that matches this is left alone (negation, quoting a stale doc ...)


def apply_rules(text: str, rules: Sequence[Rule]) -> list[str]:
    """One problem per offending sentence and rule: ``<what is wrong>: "<the sentence>"``.

    A rule whose exemption is a negation ("no", "not", "never", "whether" ...) only looks at the 70 characters before
    the claim and the claim itself: "customers sent it again after seeing no message" must not be excused by the "no"
    that comes after. Other exemptions (quoting a stale document, contrasting with an alternative) read the whole sentence.
    """
    problems: list[str] = []
    for unit in units(text):
        for rule in rules:
            local = rule.exempt is not None and NEGATION.pattern in rule.exempt.pattern
            for m in rule.pattern.finditer(unit):
                if rule.exempt is not None and rule.exempt.search(unit[max(0, m.start() - 70):m.end()] if local else unit):
                    continue
                if rule.expect is not None and rule.expect(m):
                    continue
                problem = f'{rule.message}: "{snippet(unit)}"'
                if problem not in problems:
                    problems.append(problem)
                break
    return problems


def _rx(pattern: str, flags: int = re.I) -> re.Pattern[str]:
    return re.compile(pattern, flags)


def _int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value.replace(",", ""))
    except ValueError:
        return None


# =================================================================================
# 4. ADR checks
# =================================================================================
def find_adr(work: Path | str) -> Path | None:
    """The lowest-numbered ADR: docs/adr/NNNN-something.md."""
    folder = Path(work) / "docs" / "adr"
    files = sorted(p for p in folder.glob("*.md") if re.match(r"^\d{4}-.+\.md$", p.name)) if folder.is_dir() else []
    return files[0] if files else None


_STATUS = re.compile(r"\b(proposed|accepted|deprecated|superseded)\b", re.I)
_DOWNSIDE = re.compile(
    r"\b(but|however|cost|costs|downside|downsides|risk|risks|trade-?off|negative|drawback|limitation|harder|"
    r"cannot|can't|must now|burden|worse|lose|loses|no longer|at the price)\b",
    re.I,
)


def adr_format_problems(text: str) -> list[str]:
    problems: list[str] = []
    secs = outline(text)
    if not any(s.level == 1 and s.title.strip() for s in secs):
        problems.append("there is no title (a line starting with '# ')")
    order = ["status", "context", "decision", "consequences"]
    found: dict[str, int | None] = {}
    for key in order:
        rx = re.compile(rf"^\s*{key}\b", re.I)
        found[key] = next((i for i, s in enumerate(secs) if s.level >= 2 and rx.search(s.title)), None)
    status_text = secs[found["status"]].full if found["status"] is not None else ""
    if found["status"] is None:  # Nygard's own ADRs use headings, but "Status: Accepted" on one line is common
        inline = re.search(r"(?im)^\W*status\W*[:\-]\s*(.+)$", text)
        if inline:
            status_text = inline.group(1)
            found["status"] = -1
    missing = [k.title() for k in order if found[k] is None]
    if missing:
        problems.append("missing section(s): " + ", ".join(missing))
    else:
        real = [found[k] for k in order if found[k] != -1]
        if real != sorted(real):
            problems.append("the sections are out of order (expected Status, Context, Decision, Consequences)")
    if found["status"] is not None and not _STATUS.search(status_text[:200]):
        problems.append("Status is not one of Proposed, Accepted, Deprecated, Superseded")
    minimum = {"context": 40, "decision": 12, "consequences": 40}
    for key, words in minimum.items():
        if found[key] is not None and len(secs[found[key]].full.split()) < words:
            problems.append(f"{key.title()} is too thin (under {words} words)")
    if found["consequences"] is not None and not _DOWNSIDE.search(secs[found["consequences"]].full):
        problems.append("Consequences name no downside (an ADR records what gets harder, not only what gets easier)")
    return problems


ADR_RULES: list[Rule] = [
    Rule("quote_ttl",
         _rx(r"\bquotes?\b[^.\n]{0,60}?\b(?:valid|expires?|expired|good|lasts?|lifetime|ttl)\b[^.\n]{0,40}?\b(\d+)\s*(seconds?|secs?|s|minutes?|mins?)\b"),
         "The quote lifetime disagrees with fx.QUOTE_TTL",
         expect=lambda m: (int(m.group(1)) * (60 if m.group(2).lower().startswith("m") else 1)) == 60),
    Rule("quote_ttl_adj",
         _rx(r"\b(\d+)[- ](second|minute)s?\b[^.\n]{0,20}\bquote"),
         "The quote lifetime disagrees with fx.QUOTE_TTL",
         expect=lambda m: (int(m.group(1)) * (60 if m.group(2).lower() == "minute" else 1)) == 60),
    Rule("qatar_offset",
         _rx(r"\bQatar\b[^.\n]{0,80}\b(?:UTC|GMT)\s*\+\s*(\d{1,2})\b|\b(?:UTC|GMT)\s*\+\s*(\d{1,2})\b[^.\n]{0,60}\bQatar\b"),
         "The Qatar offset disagrees with limits.QATAR_UTC_OFFSET",
         expect=lambda m: (_int(m.group(1) or m.group(2))) == 3),
    Rule("qatar_dst",
         _rx(r"\bQatar\b[^.\n]{0,80}\b(?:observes|uses|has|follows|applies)\b[^.\n]{0,30}\b(?:daylight|dst)\b"),
         "The code does not apply daylight saving to Qatar (limits.QATAR_TZ is a fixed offset)",
         exempt=NEGATION),
    Rule("stale_t1", _rx(r"\bT1\b[^.\n]{0,80}\b5,?000\b"),
         "The T1 figure disagrees with limits.LIMITS (docs/ARCHITECTURE.md is not a source: it has drifted)",
         exempt=_rx(r"stale|outdated|ARCHITECTURE|wrong|incorrect|drift|disagree|monthly|8,?000")),
    Rule("stale_t2", _rx(r"\bT2\b[^.\n]{0,80}\b25,?000\b"),
         "The T2 figure disagrees with limits.LIMITS (docs/ARCHITECTURE.md is not a source: it has drifted)",
         exempt=_rx(r"stale|outdated|ARCHITECTURE|wrong|incorrect|drift|disagree|corridor|max_send|QAR-INR|per transfer|per-transfer")),
    Rule("no_monthly", _rx(r"\bno monthly (?:limit|cap)s?\b|\bthere (?:is|are) no monthly\b"),
         "Check limits.LIMITS: this disagrees with it",
         exempt=_rx(r"stale|outdated|ARCHITECTURE|wrong|incorrect|drift|disagree|claims?|says")),
    Rule("two_tiers", _rx(r"\btwo (?:kyc )?tiers?\b"),
         "Check limits.LIMITS and models.KYC_TIERS: the number of tiers disagrees with them",
         exempt=_rx(r"stale|outdated|ARCHITECTURE|wrong|incorrect|drift|disagree|claims?|says")),
    Rule("marginal_fee", _rx(r"\b(?:marginal|progressive|bracket|slab)s?\b[^.\n]{0,60}\bfees?\b|\bfees?\b[^.\n]{0,60}\b(?:marginal|progressive|bracket|slab)"),
         "Check fees.FeeSchedule.tier_index: how the tier is chosen disagrees with this",
         exempt=NEGATION),
    Rule("express_before_cap", _rx(r"\bexpress\b[^.\n]{0,60}\bbefore the cap\b"),
         "Check fees.explain_fee: where the express surcharge is added disagrees with this", exempt=NEGATION),
    Rule("half_even", _rx(r"\b(?:half[- ]even|banker'?s?)\b"),
         "Check money.quantize and ledger.post_transfer: the rounding rule disagrees with this",
         exempt=_rx(r"ledger|partner|Q-LED|instead|rather|than|alternative|\bvs\b|versus|differs?|except|unlike|but\b|not\b", 0)),
    Rule("float_ok", _rx(r"\b(?:accepts?|allows?|supports?|takes)\b[^.\n]{0,40}\bfloats?\b"),
         "Check money.Money: what it does with floats disagrees with this",
         exempt=_rx(r"reject|refus|rais|TypeError|never|not\b|no\b|without|instead")),
    Rule("all_placeholders", _rx(r"\ball queries use placeholders\b|\bevery query (?:is )?parameteri[sz]ed\b|\bqueries use placeholders\b"),
         "Check every query in src/remit/store.py: this disagrees with it",
         exempt=_rx(r"except|apart|search_by_name|known smell|stale|outdated|ARCHITECTURE|wrong|claims?|says")),
]


def adr_fact_problems(text: str) -> list[str]:
    return apply_rules(prose_only(text), ADR_RULES)


def adr_references(text: str, index: CodeIndex) -> tuple[list[str], int, int]:
    """(unresolved references, number resolved, number resolved that point into src/)."""
    unresolved: list[str] = []
    resolved = in_src = 0
    seen: set[str] = set()
    for token in re.findall(r"`([^`\n]+)`", prose_only(text)):
        token = token.strip()
        if token in seen:
            continue
        seen.add(token)
        verdict = index.resolve_path(token)
        kind = "path"
        if verdict is None:
            verdict = index.resolve_symbol(token)
            kind = "symbol"
        if verdict is None:
            continue
        if verdict:
            resolved += 1
            if kind == "symbol" or token.lstrip("./").startswith("src/") or re.match(r"[\w.-]+\.py", token):
                in_src += 1
        else:
            unresolved.append(token)
    return unresolved, resolved, in_src


CRITIC_HEAD = r"critic|objection|challenge|steelman|devil"
RESPONSE_CUE = re.compile(
    r"\b(respon(?:se|d|ded|ds)|answer(?:ed)?|repl(?:y|ied)|decision|disposition|resolution|outcome|accept(?:ed)?|"
    r"reject(?:ed)?|address(?:ed)?|kept|keep|chose|changed|added|follow[- ]up|mitigat\w+|deferred|rebuttal|"
    r"we (?:will|did|do)|still|because)\b",
    re.I,
)


def sub_sections(secs: Sequence[Sec], parent: Sec) -> list[Sec]:
    """The sections nested directly or indirectly under ``parent`` (the outline is in document order)."""
    start = next(i for i, s in enumerate(secs) if s is parent)
    nested = []
    for s in secs[start + 1:]:
        if s.level <= parent.level:
            break
        nested.append(s)
    return nested


def adr_critic_problems(text: str) -> list[str]:
    secs = outline(text)
    sec = find_section(secs, CRITIC_HEAD)
    if sec is None:
        return ["there is no section for the critic's objections (a heading with 'Critic' or 'Objections' in it)"]
    nested = sub_sections(secs, sec)
    if len(nested) >= 3:  # one sub-heading per objection
        items = [f"{n.title} {n.full}" for n in nested if len((n.title + " " + n.full).split()) >= 8]
    else:
        items = [i for i in list_items(sec.full) if len(i.split()) >= 8]
    table_rows = [ln for ln in sec.full.splitlines() if ln.strip().startswith("|")]
    header = table_rows[0] if table_rows else ""
    if len(items) < 3:
        return [f"found {len(items)} objection(s); the task asks for at least 3"]
    if table_rows and re.search(r"respon|answer|decision|disposition|outcome|repl|resolution|action", header, re.I):
        answered = len(items)
    else:
        answered = sum(1 for i in items if RESPONSE_CUE.search(i))
    if answered < 3:
        return [f"only {answered} objection(s) say what you did about them (accepted, rejected with a reason, deferred)"]
    return []


# =================================================================================
# 5. najmkit page checks
# =================================================================================
FILE_EXTENSIONS = {"py", "md", "json", "jsonl", "log", "txt", "toml", "yml", "yaml", "cfg", "ini", "csv", "lock"}
NAJMKIT_MODULES = ("ids", "clock", "audit")
_QUAL = re.compile(r"(?<![\w.])(?:najmkit\.)?(ids|clock|audit)\.([A-Za-z_]\w*)(?:\.([A-Za-z_]\w*))?")
_IMPORT = re.compile(r"^\s*from\s+najmkit(?:\.(\w+))?\s+import\s+([^\n#]+)", re.M)
_PLAIN_IMPORT = re.compile(r"^\s*import\s+najmkit(?:\.(\w+))?", re.M)
COVERAGE_EXCLUDE = {"Clock"}  # a Protocol: documenting FixedClock and SystemClock covers it


def _module(index: CodeIndex, short: str) -> ModuleInfo | None:
    return index.modules.get(f"najmkit.{short}")


def docs_name_problems(text: str, index: CodeIndex) -> list[str]:
    problems: list[str] = []
    for m in _QUAL.finditer(text):
        short, name, member = m.group(1), m.group(2), m.group(3)
        if name in FILE_EXTENSIONS:
            continue
        module = _module(index, short)
        if module is None:
            continue
        claim = f"{short}.{name}" + (f".{member}" if member else "")
        if name not in module.names:
            if not module.has_member_anywhere(name):
                problems.append(f"`{claim}` does not exist in najmkit.{short}")
            continue
        if member and name in module.classes and member not in module.classes[name]:
            problems.append(f"`{claim}` does not exist ({name} has no '{member}')")
    for m in _IMPORT.finditer(text):
        short = m.group(1)
        names = [n.strip().split(" as ")[0].strip("() ") for n in m.group(2).split(",") if n.strip()]
        if short is None:
            for n in names:
                if n and f"najmkit.{n}" not in index.modules and n != "*":
                    problems.append(f"`from najmkit import {n}`: najmkit has no module '{n}'")
        else:
            module = _module(index, short)
            if module is None:
                problems.append(f"`from najmkit.{short} import ...`: najmkit has no module '{short}'")
                continue
            for n in names:
                if n and n != "*" and n not in module.names:
                    problems.append(f"`from najmkit.{short} import {n}`: najmkit.{short} defines no '{n}'")
    for m in _PLAIN_IMPORT.finditer(text):
        if m.group(1) and f"najmkit.{m.group(1)}" not in index.modules:
            problems.append(f"`import najmkit.{m.group(1)}`: najmkit has no module '{m.group(1)}'")
    return list(dict.fromkeys(problems))


def _balanced(text: str, start: int) -> str | None:
    depth = 0
    for i in range(start, min(len(text), start + 400)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return " ".join(text[start + 1:i].split())
    return None


def claimed_params(inside: str) -> tuple[str, list[Param], int, list[str], bool] | None:
    """Read the text between the parentheses of a claimed signature or call.

    Returns (form, params, positional count, keyword names, declares): ``form`` is "signature"
    (``prefix: str, **fields``) or "call" (``"TRF", length=3``). ``declares`` is True when the text can only be a
    declaration (annotations, defaults, stars): bare names such as ``(fixed)`` could be variables in a call, so
    their names are not held against the real parameters. None when the text is neither
    (``path | None = None`` and the like).
    """
    try:
        fn = ast.parse(f"def _({inside}): pass").body[0]
        assert isinstance(fn, ast.FunctionDef)
        a = fn.args
        params = _params(fn, drop_first=False)
        declares = bool(a.defaults or a.kw_defaults or a.vararg or a.kwarg or a.kwonlyargs
                        or any(x.annotation for x in [*a.posonlyargs, *a.args]))
        # a parameter with a default may be a keyword argument in a call (`seconds=61`), so it is not counted as positional
        return "signature", params, sum(1 for p in params if p.kind in ("pos", "posonly") and p.required), [], declares
    except (SyntaxError, AssertionError, IndexError):
        pass
    try:
        call = ast.parse(f"_({inside})", mode="eval").body
        assert isinstance(call, ast.Call)
        positional = sum(1 for a in call.args if not isinstance(a, ast.Starred))
        return "call", [], positional, [k.arg for k in call.keywords if k.arg], True
    except (SyntaxError, AssertionError):
        return None


def signature_problem(label: str, inside: str, real: list[Param]) -> str | None:
    if not inside.strip():
        return None  # `ids.new_id()` is shorthand for "the function", not a claim about its arguments
    claim = claimed_params(inside)
    if claim is None:
        return None
    form, params, positional, keywords, declares = claim
    names = {p.name for p in real}
    varkw = next((p.name for p in real if p.kind == "varkw"), None)
    has_var = any(p.kind == "var" for p in real)
    capacity = sum(1 for p in real if p.kind in ("pos", "posonly"))
    if positional > capacity and not has_var:
        return f"`{label}({inside})`: the real function takes at most {capacity} positional argument(s)"
    if not declares:
        return None
    claimed = [(p.name, p.kind) for p in params] if form == "signature" else [(k, "kwonly") for k in keywords]
    for name, kind in claimed:
        if kind in ("var", "varkw"):
            continue
        if name in names and name != varkw:
            continue
        if varkw is not None:
            if name == varkw and form == "signature":
                return f"`{label}({inside})`: '{name}' is the **{name} catch-all, not a parameter called '{name}'"
            continue
        return f"`{label}({inside})`: '{name}' is not a parameter of {label.split('.')[-1]}"
    return None


def docs_signature_problems(text: str, index: CodeIndex) -> list[str]:
    problems: list[str] = []
    flat = text.replace("\n", " ")
    public: dict[str, tuple[ModuleInfo, str]] = {}
    for short in NAJMKIT_MODULES:
        module = _module(index, short)
        if module is None:
            continue
        for key in module.sigs:
            public.setdefault(key, (module, key))
    checked: set[tuple[str, str]] = set()
    for m in _QUAL.finditer(flat):
        short, name, member = m.group(1), m.group(2), m.group(3)
        end = m.end()
        if flat[end:end + 1] != "(" or name in FILE_EXTENSIONS:
            continue
        module = _module(index, short)
        if module is None:
            continue
        key = f"{name}.{member}" if member else name
        if key not in module.sigs:
            continue
        inside = _balanced(flat, end)
        if inside is None or (key, inside) in checked:
            continue
        checked.add((key, inside))
        problem = signature_problem(f"{short}.{key}", inside, module.sigs[key])
        if problem:
            problems.append(problem)
    names_unqualified = {key: mod for key, (mod, _) in public.items() if "." not in key and key != "now"}
    for m in re.finditer(r"(?<![\w.])([A-Za-z_]\w*)\s*(?=\()", flat):
        key = m.group(1)
        if key not in names_unqualified:
            continue
        inside = _balanced(flat, m.end())
        if inside is None or (key, inside) in checked:
            continue
        checked.add((key, inside))
        problem = signature_problem(key, inside, names_unqualified[key].sigs[key])
        if problem:
            problems.append(problem)
    return list(dict.fromkeys(problems))


def public_names(work: Path | str) -> list[str]:
    """Top-level public names of najmkit's modules, read with ``checks.public_api`` (functions and classes)."""
    api = checks.public_api(work, "src")
    found = []
    for dotted in api:
        parts = dotted.split(".")
        if len(parts) == 3 and parts[0] == "najmkit" and parts[2] not in COVERAGE_EXCLUDE:
            found.append(parts[2])
    return sorted(set(found))


def docs_coverage(text: str, work: Path | str) -> tuple[int, int, list[str]]:
    names = public_names(work)
    missing = [n for n in names if not re.search(rf"(?<![A-Za-z_]){re.escape(n)}(?![A-Za-z_])", text)]
    return len(names) - len(missing), len(names), missing


def docs_rules(facts: dict[str, str]) -> list[Rule]:
    version, api = facts.get("version", ""), facts.get("api", "")
    other = _rx(r"python|migrat|future|planned|upgrade|will |later|next ")
    return [
        Rule("version", _rx(r"\bversion\s+`?v?(\d+\.\d+\.\d+)`?"), "The version disagrees with __version__ in src/najmkit/__init__.py",
             expect=lambda m: m.group(1) == version, exempt=other),
        Rule("api", _rx(r"\bAPI\s+`?(v\d+)`?"), "The API version disagrees with API_VERSION in src/najmkit/__init__.py",
             expect=lambda m: m.group(1).lower() == api.lower(), exempt=other),
        Rule("prefix_range", _rx(r"\bprefix[^.\n]{0,100}?\b(\d)\s*(?:to|-|–|—|and)\s*(\d)\b[^.\n]{0,20}(?:upper|capital|letters|characters|chars)"),
             "The prefix rule disagrees with the check in ids.new_id",
             expect=lambda m: (int(m.group(1)), int(m.group(2))) == (2, 5)),
        Rule("prefix_range2", _rx(r"\b(\d)\s*(?:to|-|–|—)\s*(\d)\s*(?:upper-?case|capital)"),
             "The prefix rule disagrees with the check in ids.new_id",
             expect=lambda m: (int(m.group(1)), int(m.group(2))) == (2, 5)),
        Rule("prefix_case", _rx(r"\bprefix[^.\n]{0,80}\b(?:lower-?case|mixed[- ]case|any case|case[- ]insensitive)\b"),
             "The prefix rule disagrees with the check in ids.new_id", exempt=NEGATION),
        Rule("random_token", _rx(r"\brandom[^.\n]{0,40}?\b(\d+)[- ](?:hex(?:adecimal)?|character|char)s?\b|\b(\d+)[- ](?:hex(?:adecimal)?|character|char)s?\b[^.\n]{0,20}\brandom"),
             "The token length disagrees with ids.new_id",
             expect=lambda m: _int(m.group(1) or m.group(2)) == 12),
        Rule("sequential_digits", _rx(r"\bsequential[^.\n]{0,80}?\b(\d+)[- ]digit|\b(\d+)[- ]digit[^.\n]{0,40}\bsequential"),
             "The width of a sequential token disagrees with ids.SequentialIds",
             expect=lambda m: _int(m.group(1) or m.group(2)) == 6),
        Rule("reserved_fields", _rx(r"^(?=.*\breserved\b)(?=.*`(?:timestamp|level|message|time|id|type|source|name|severity)`)", re.I | re.S),
             "The reserved field names disagree with audit.log_event", exempt=NEGATION),
        Rule("event_format", _rx(r"\bevent\b[^.\n]{0,60}\b(?:snake_case|camel ?case|upper-?case|any string|free[- ]form|arbitrary)\b"),
             "The event-name rule disagrees with the check in audit.log_event", exempt=NEGATION),
        Rule("naive_ok", _rx(r"\bnaive\b[^.\n]{0,80}\b(?:accepted|allowed|assumed|treated as|converted|interpreted)\b"),
             "What the clock does with a naive datetime disagrees with najmkit.clock", exempt=NEGATION),
        Rule("local_time", _rx(r"\bnow\(\)[^.\n]{0,80}\b(?:local time|machine'?s? time ?zone|naive)\b"),
             "What clock.now() returns disagrees with najmkit.clock", exempt=NEGATION),
        Rule("audit_default", _rx(r"(?:default(?:s)? to|falls? back to|writes? to|goe?s? to|prints? to|printed to|sent to|logged to|written to)[^.\n]{0,50}\b(?:stdout|stderr|console|audit\.log|syslog|a default file)\b"),
             "What happens with no audit path disagrees with audit.current_path and audit.log_event", exempt=NEGATION),
        Rule("read_events_raises",
             _rx(r"^(?=.*(?:read_events|missing|does not exist|doesn't exist|nonexistent|non-existent|no such file))(?!.*\blog_event\b).*\bFileNotFoundError\b", re.I | re.S),
             "What audit.read_events does with a missing file disagrees with running it (try it)",
             exempt=re.compile(NEGATION.pattern + "|" + DOCSTRING_TALK.pattern, re.I)),
        Rule("thread_safe", _rx(r"\bthread[- ]?safe\b"), "Nothing in the code supports a thread-safety claim", exempt=NEGATION),
        Rule("async", _rx(r"\basync(?:io|hronous(?:ly)?)?\b|\bawait\b|\bcoroutines?\b"), "Nothing in the code supports an async claim", exempt=NEGATION),
        Rule("pypi", _rx(r"\bpip install\b[^\n]*\bnajmkit\b|\bnajmkit\b[^.\n]{0,60}\b(?:on|from|via) PyPI\b"),
             "Check how najmkit is distributed (see src/najmkit/__init__.py)", exempt=NEGATION),
        Rule("audit_extras", _rx(r"\b(?:log_event|audit)\b[^.\n]{0,100}\b(?:retries|retry|retried|rotates|rotation|compress\w*|batch\w*|buffer\w*|flush\w*|encrypt\w*|signs|signed|hash chain)\b"),
             "Nothing in audit.log_event does this: read it", exempt=NEGATION),
    ]


def docs_fact_problems(text: str, facts: dict[str, str]) -> list[str]:
    return apply_rules(prose_only(text), docs_rules(facts))


_RUNNER = r'''
import contextlib, io, json, sys
statements = json.load(open(sys.argv[1], encoding="utf-8"))
namespace = {"__name__": "doc_example"}
results = []
for i, source in enumerate(statements):
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(source, "<docs statement %d>" % i, "exec"), namespace)
        results.append({"i": i, "ok": True})
    except BaseException as exc:
        results.append({"i": i, "ok": False, "type": type(exc).__name__, "msg": str(exc)[:300]})
print("@@RESULT@@" + json.dumps(results))
'''
_KNOWN_CALLABLES = {"new_id", "use_generator", "SequentialIds", "SystemClock", "FixedClock", "now", "set_clock", "get_clock",
                    "reset_clock", "configure", "current_path", "log_event", "read_events", "advance", "set", "__init__"}
_KNOWN_CLASSES = ("SequentialIds", "SystemClock", "FixedClock", "Clock")


_IMPORT_LINE = re.compile(r"\bfrom\s+najmkit(?:\.\w+)?\s+import\s+[\w, ]+|\bimport\s+najmkit(?:\.\w+)?")


def doc_statements(text: str) -> list[str]:
    """Every top-level statement of every Python block that parses (blocks of signatures do not).

    An import that the page shows only in prose ("import them as `from najmkit import ids, clock, audit`") is
    put in front, so a page may state its import once.
    """
    statements: list[str] = []
    for lang, body in code_blocks(text):
        if lang not in ("python", "py", "python3"):
            continue
        try:
            tree = ast.parse(body)
        except SyntaxError:
            continue
        for node in tree.body:
            segment = ast.get_source_segment(body, node)
            if segment:
                statements.append(segment)
    preamble = [m.group(0).strip() for m in _IMPORT_LINE.finditer(prose_only(text))]
    return [*dict.fromkeys(preamble), *statements] if statements else []


def example_failure(result: dict) -> str | None:
    """A statement failed because of najmkit's API (not because of a placeholder): the failure text, else None."""
    kind, msg = result.get("type", ""), result.get("msg", "")
    if kind == "AttributeError" and ("najmkit" in msg or any(c in msg for c in _KNOWN_CLASSES)):
        return f"AttributeError: {msg}"
    if kind in ("ImportError", "ModuleNotFoundError") and "najmkit" in msg:
        return f"{kind}: {msg}"
    if kind == "TypeError":
        m = re.match(r"^(?:\w+\.)*(?P<fn>\w+)\(\) (?:got an unexpected keyword argument|takes|missing)", msg)
        if m and m.group("fn") in _KNOWN_CALLABLES:
            return f"TypeError: {msg}"
    return None


def run_doc_examples(work: Path | str, text: str, *, timeout: float = 15.0) -> tuple[list[str], dict[str, int], int]:
    """Run the docs' Python statements against the learner's code, in a subprocess on a throw-away copy.

    Returns (API failures, successful statements per najmkit module, statements tried).
    """
    statements = doc_statements(text)
    ok_by_module = {m: 0 for m in NAJMKIT_MODULES}
    if not statements:
        return [], ok_by_module, 0
    with tempfile.TemporaryDirectory(prefix="ailab-m11-") as scratch, checks.work_copy(work) as root:
        payload = Path(scratch) / "statements.json"
        payload.write_text(json.dumps(statements), encoding="utf-8")
        run = runner.run_python(["-c", _RUNNER, str(payload)], cwd=root, pythonpath=[root / "src"], timeout=timeout,
                                extra_env={"HOME": scratch})
    marker = "@@RESULT@@"
    if run.timed_out or marker not in run.stdout:
        return ["the examples did not finish (an endless loop, or a crash while importing najmkit)"], ok_by_module, len(statements)
    results = json.loads(run.stdout.split(marker, 1)[1].strip().splitlines()[0])
    failures: list[str] = []
    for result in results:
        source = statements[result["i"]]
        if result["ok"]:
            for module in NAJMKIT_MODULES:
                if re.search(rf"\b{module}\.", source):
                    ok_by_module[module] += 1
            continue
        why = example_failure(result)
        if why:
            failures.append(f"`{snippet(source, 70)}` -> {why}")
    return failures, ok_by_module, len(statements)


# =================================================================================
# 6. postmortem checks
# =================================================================================
CAST = ("Tariq", "Lujain", "Hessa", "Nada", "Noura", "Maha", "Layla", "Hamad", "Sara", "Salem")
SECTION_ORDER = ("timeline", "summary", "impact", "actions", "unknowns", "inferences", "facts")
SECTION_PATTERNS = {
    "summary": r"summary|overview|tl;?dr",
    "impact": r"impact",
    "timeline": r"timeline",
    "facts": r"what we know|facts|established|confirmed|known\b",
    "inferences": r"infer|hypothes|likely|probable|suspect",
    "unknowns": r"unknown|do not know|don'?t know|not (?:yet )?(?:known|established)|open questions|gaps|cannot say|can'?t say",
    "actions": r"action|follow[- ]?up|next steps|remediation",
}
SECTION_LABELS = {
    "summary": "Summary", "impact": "Impact", "timeline": "Timeline", "facts": "What we know",
    "inferences": "What we infer", "unknowns": "What we do not know", "actions": "Action items",
}


class Record:
    """The incident record (the kit's pristine copy, never the learner's) and what can be derived from it."""

    def __init__(self, data: dict) -> None:
        self.data = data
        self.id: str = data["id"]
        self.severity: str = data["severity"]
        self.date: str = data["date"]
        self.version: str = data["service_version"]
        self.events: dict[str, dict] = {e["id"]: e for e in data["timeline"]}
        self.times: set[str] = {e["time"][:5] for e in data["timeline"]}
        self.people: set[str] = {data.get("incident_commander", "")} - {""}
        self.dates: set[str] = {self.date}
        for key in ("baseline", "last_deploy"):
            for value in _strings(data.get(key)):
                self.dates.update(re.findall(r"\d{4}-\d{2}-\d{2}", value))
        for value in _strings(data.get("counts")):
            self.dates.update(re.findall(r"\d{4}-\d{2}-\d{2}", value))
        self.count_numbers, self.minute_numbers = self._numbers()

    def _numbers(self) -> tuple[set[int], set[int]]:
        """Numbers a postmortem may use: counts (the record's, and a few meaningful differences) and minutes (differences of times)."""

        def flatten(node: object, prefix: str = "") -> dict[str, int]:
            flat: dict[str, int] = {}
            if isinstance(node, bool):
                return flat
            if isinstance(node, (int, float)):
                flat[prefix] = int(node)
            elif isinstance(node, dict):
                for key, value in node.items():
                    flat.update(flatten(value, f"{prefix}.{key}" if prefix else key))
            return flat

        counts, baseline = flatten(self.data.get("counts")), flatten(self.data.get("baseline"))
        numbers = set(counts.values()) | set(baseline.values())
        for path, value in counts.items():  # this week against last week, same measure
            if path in baseline:
                numbers.add(abs(value - baseline[path]))
        for section in (counts, baseline):  # sends minus what failed or was rejected
            sent = section.get("transfer.sent")
            if sent is not None:
                numbers.update(abs(sent - v) for k, v in section.items() if k != "transfer.sent")
            groups: dict[str, int] = {}
            for path, value in section.items():
                parent = path.rsplit(".", 1)[0] if "." in path else ""
                groups[parent] = groups.get(parent, 0) + value
            numbers.update(v for k, v in groups.items() if k and k.count(".") >= 1 or k in ("transfer.rejected", "notification.failed"))
        minutes = sorted(int(e["time"][:2]) * 60 + int(e["time"][3:5]) for e in self.data["timeline"])
        in_minutes = {abs(a - b) for a in minutes for b in minutes}
        scrub = re.compile(r"\d{1,2}:\d{2}(?::\d{2})?|\d{4}-\d{2}-\d{2}|\b[A-Za-z]+-?\d+\b")
        from_text: set[int] = set()
        for value in [self.data["title"], *[e["text"] for e in self.data["timeline"]]]:
            from_text.update(int(n.replace(",", "")) for n in re.findall(r"\d[\d,]*", scrub.sub(" ", value)) if n.strip(","))
        return numbers | from_text, in_minutes | from_text


def _strings(node: object) -> Iterable[str]:
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from _strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from _strings(v)


def load_record(path: Path) -> Record:
    return Record(json.loads(path.read_text(encoding="utf-8")))


def postmortem_sections(text: str) -> dict[str, Sec]:
    """Map each required part to the first heading that matches it (more specific parts are tried first)."""
    secs = [s for s in outline(text) if s.level >= 2]
    found: dict[str, Sec] = {}
    for sec in secs:
        for key in SECTION_ORDER:
            if key not in found and re.search(SECTION_PATTERNS[key], sec.title, re.I):
                found[key] = sec
                break
    return found


def postmortem_section_problems(sections: dict[str, Sec]) -> list[str]:
    problems = [f"no '{SECTION_LABELS[k]}' section" for k in SECTION_PATTERNS if k not in sections]
    for key, minimum in (("summary", 12), ("impact", 8), ("timeline", 12), ("facts", 8), ("inferences", 8), ("unknowns", 8), ("actions", 8)):
        sec = sections.get(key)
        if sec is not None and len(sec.full.split()) < minimum:
            problems.append(f"'{SECTION_LABELS[key]}' is nearly empty")
    return problems


_ROW = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+|\|\s*)?\**\s*(?:\d{4}-\d{2}-\d{2}[ T]+)?(\d{1,2}):(\d{2})(?::\d{2})?")


def timeline_rows(section_text: str) -> list[tuple[str, str]]:
    rows = []
    for line in section_text.splitlines():
        m = _ROW.match(line)
        if m:
            rows.append((f"{int(m.group(1)):02d}:{m.group(2)}", line))
    return rows


def timeline_problems(section_text: str, record: Record, key: dict) -> tuple[list[str], set[str], int]:
    """Check each row against the record. Returns (problems, event ids covered, number of rows)."""
    problems: list[str] = []
    covered: set[str] = set()
    rows = timeline_rows(section_text)
    for hhmm, line in rows:
        ids = re.findall(r"\bE(\d+)\b", line)
        ids = [f"E{i}" for i in ids]
        unknown = [i for i in ids if i not in record.events]
        if unknown:
            problems.append(f"row {hhmm}: the record has no event {', '.join(unknown)}")
            continue
        candidates = [i for i in ids if record.events[i]["time"][:5] == hhmm] if ids else \
            [i for i, e in record.events.items() if e["time"][:5] == hhmm]
        if not candidates:
            if ids:
                problems.append(f"row {hhmm}: {', '.join(ids)} is not at that time in the record")
            else:
                problems.append(f"row {hhmm}: the record has no event at that time")
            continue
        lowered = line.lower()
        matched = [i for i in candidates if re.search(key["events"][i]["anchors"], lowered)]
        if not matched:
            problems.append(f"row {hhmm}: the text does not describe {', '.join(candidates)} as the record does")
            continue
        covered.update(matched)
    return problems, covered, len(rows)


_UNITS = (r"minutes?|mins?|seconds?|secs?|hours?|hrs?|customers?|transfers?|events?|calls?|callers?|tickets?|rejections?|messages?|"
          r"notifications?|failures?|users?|accounts?|requests?|alerts?|errors?|QAR")
_NUMBER_UNIT = re.compile(rf"(?<![\w:.,/-])(\d{{1,3}}(?:,\d{{3}})+|\d+)(?:\.\d+)?(?:\s|-)?(?:{_UNITS})\b", re.I)
_MONTH_NAMES = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                "November", "December")
_MONTH_RX = "|".join(f"{m}|{m[:3]}" for m in _MONTH_NAMES)
_DAY_MONTH = re.compile(rf"\b(\d{{1,2}})(?:st|nd|rd|th)?\s+({_MONTH_RX})\b")
_MONTH_DAY = re.compile(rf"\b({_MONTH_RX})\s+(\d{{1,2}})(?:st|nd|rd|th)?\b")


def _month_number(name: str) -> int:
    return next(i for i, m in enumerate(_MONTH_NAMES, start=1) if m.startswith(name[:3]))


def invented_facts(text: str, record: Record) -> list[str]:
    """Numbers with units, clock times, dates, ids, severity and versions that are not in the record."""
    problems: list[str] = []
    body = re.sub(r"\bINC-\d+\b", " ", text)
    for m in _NUMBER_UNIT.finditer(body):
        value = int(m.group(1).replace(",", ""))
        unit = m.group(0)[len(m.group(1)):]
        if re.search(r"hours?|hrs?", unit, re.I):
            allowed = value <= 2
        elif re.search(r"seconds?|secs?", unit, re.I):
            allowed = value <= 59
        elif re.search(r"minutes?|mins?", unit, re.I):
            allowed = value in record.minute_numbers
        else:
            allowed = value in record.count_numbers
        if not allowed:
            problems.append(f"the number {m.group(1)} ('{snippet(m.group(0), 30)}') is not in the record and is not a difference of times or counts in it")
    for hh, mm in re.findall(r"(?<![\d:.-])(\d{1,2}):(\d{2})(?::\d{2})?(?![\d:])", body):
        if f"{int(hh):02d}:{mm}" not in record.times:
            problems.append(f"the time {hh}:{mm} is not the time of any event in the record")
    allowed = {(int(d[5:7]), int(d[8:10])) for d in record.dates}
    for iso in re.findall(r"\b\d{4}-\d{2}-\d{2}\b", body):
        if iso not in record.dates:
            problems.append(f"the date {iso} is not in the record")
    spoken = [(_month_number(mo), int(d)) for d, mo in _DAY_MONTH.findall(body)] + \
             [(_month_number(mo), int(d)) for mo, d in _MONTH_DAY.findall(body)]
    for month, day in dict.fromkeys(spoken):
        if (month, day) not in allowed:
            problems.append(f"the date '{day} {_MONTH_NAMES[month - 1]}' is not in the record")
    for year in dict.fromkeys(re.findall(r"\b(20\d{2})\b", body)):
        if year != record.date[:4]:
            problems.append(f"the year {year} is not in the record")
    for inc in dict.fromkeys(re.findall(r"\bINC-\d+\b", text)):
        if inc != record.id:
            problems.append(f"{inc} is not the incident in the record ({record.id})")
    for sev in dict.fromkeys(re.findall(r"\bSEV\s?-?(\d)\b", text, re.I)):
        if f"SEV{sev}" != record.severity:
            problems.append(f"SEV{sev} is not the severity in the record")
    for version in dict.fromkeys(re.findall(r"(?:\bv|\bversion\s+|\bRemit\s+)(\d+\.\d+\.\d+)\b", text)):
        if version != record.version:
            problems.append(f"version {version} is not the service version in the record")
    return list(dict.fromkeys(problems))


def invented_people(text: str, record: Record) -> list[str]:
    return [f"{name} is not named in the record" for name in CAST
            if name not in record.people and re.search(rf"\b{name}\b", text)]


def forbidden_problems(text: str, key: dict) -> list[str]:
    rules = [
        Rule(r["id"], re.compile(r["pattern"], re.I), r["message"],
             exempt=re.compile(NEGATION.pattern + (("|" + r["exempt"]) if r.get("exempt") else ""), re.I))
        for r in key["forbidden"]
    ]
    return apply_rules(text, rules)


_CONFIDENCE = re.compile(r"\b(low|medium|high|unconfirmed|not confirmed|probable|plausible|possible|likely|uncertain|tentative|confidence)\b", re.I)
_VERIFY = re.compile(r"\b(confirm|verify|check|would show|would tell|refute|test|ask|query|compare|look at)\b", re.I)


def inference_problems(sec: Sec | None) -> list[str]:
    if sec is None:
        return []
    items = [i for i in list_items(sec.full) if len(i.split()) >= 6]
    if len(items) < 2:
        return [f"found {len(items)} inference(s); a postmortem that infers nothing is rarely complete (expected at least 2)"]
    problems = []
    unlabelled = [i for i in items if not _CONFIDENCE.search(i)]
    if unlabelled:
        problems.append(f"{len(unlabelled)} inference(s) say nothing about how confident you are")
    if not any(re.search(r"\bE\d+\b", i) for i in items):
        problems.append("no inference cites the event id it rests on")
    if not any(_VERIFY.search(i) for i in items):
        problems.append("no inference says what would confirm or refute it")
    return problems


def unknown_problems(sec: Sec | None, key: dict) -> list[str]:
    if sec is None:
        return []
    items = [i for i in list_items(sec.full) if len(i.split()) >= 4]
    problems = []
    if len(items) < 2:
        problems.append(f"found {len(items)} open question(s); the record leaves several (expected at least 2)")
    hits = sum(1 for pattern in key["gaps"] if re.search(pattern, sec.full, re.I))
    if hits < key["min_gaps"]:
        problems.append(f"the open questions name {hits} of the real gaps in the record (at least {key['min_gaps']} expected)")
    return problems


BLAME = re.compile(r"\b(blame|blamed|fault of|careless|negligen\w*|forgot|incompeten\w*|sloppy|human error|operator error|engineer error)\b", re.I)


def blame_problems(text: str) -> list[str]:
    return [f'"{snippet(u)}"' for u in units(text) if BLAME.search(u) and not NEGATION.search(u)]


def preamble(text: str) -> str:
    """The title and the lines before the first '## ' heading (severity, service, version, date ...)."""
    lines = text.splitlines()
    end = next((i for i, ln in enumerate(lines) if ln.startswith("## ")), len(lines))
    return "\n".join(lines[:end])


def section_texts(sections: dict[str, Sec], keys: Iterable[str]) -> str:
    return "\n".join(sections[k].full for k in keys if k in sections)


def action_item_count(sec: Sec | None) -> int:
    return 0 if sec is None else len([i for i in list_items(sec.full) if len(i.split()) >= 5])
