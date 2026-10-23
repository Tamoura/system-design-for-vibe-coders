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
import doctest
import json
import re
import tempfile
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from ailab import checks, gitutil, runner

# =================================================================================
# 1. text and Markdown helpers
# =================================================================================
_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_FENCE_LINE = re.compile(r"^\s*(```|~~~)")

NEGATION = re.compile(
    r"\b(no|not|never|none|nobody|no one|neither|nor|nothing|without|cannot|unlike|rather than|instead of|instead|than|unknown|unclear|"
    r"unconfirmed|whether|if)\b|n't",
    re.I,
)
DOCSTRING_TALK = re.compile(r"docstring|comment|\bsays\b|\bclaims?\b|stale|outdated|wrong|incorrect|misleading", re.I)
# File extensions: `audit.jsonl` is a file name, not the attribute `jsonl` of the module `audit`.
FILE_EXTENSIONS = {"py", "md", "json", "jsonl", "log", "txt", "toml", "yml", "yaml", "cfg", "ini", "csv", "lock"}
# A sentence that says the thing it names is not there. Quoting a wrong name in order to refute it is not a wrong claim.
REFUTES = re.compile(
    r"\b(?:does(?:n't| not)|do(?:n't| not)|did(?:n't| not)|will not|never) exist|no longer exists?|no such\b|non-?existent|"
    r"never existed|(?:has|had) been (?:removed|deleted)|was (?:removed|deleted)|is gone|there is no\b|not a real\b|"
    r"is not (?:a|an) (?:real|valid|public)\b|is not defined|(?:defines|has) no\b",
    re.I,
)


def snippet(text: str, limit: int = 110) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def around(text: str, start: int, end: int, *, margin: int = 24, limit: int = 110) -> str:
    """The words at ``text[start:end]`` with a little context on each side (whole words), so a message quotes the phrase that caused it."""
    left, right = max(0, start - margin), min(len(text), end + margin)
    while 0 < left < start and not text[left - 1].isspace():
        left += 1
    while end < right < len(text) and not text[right].isspace():
        right -= 1
    cut = " ".join(text[left:right].split())
    if len(cut) > limit:
        cut = cut[: limit - 3].rsplit(" ", 1)[0] + "..."
    return ("..." if left else "") + cut + ("..." if right < len(text) else "")


_ONES = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
         "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
         "seventeen": 17, "eighteen": 18, "nineteen": 19}
_TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
_SCALES = {"hundred": 100, "thousand": 1000}
_SINGLE = "|".join(w for w in _ONES if w != "zero")
_SPOKEN_NUMBER = re.compile(
    rf"\b(?:(?P<tens>{'|'.join(_TENS)})(?:[- ](?P<ones>{_SINGLE}))?|(?P<small>{'|'.join(_ONES)})|(?P<article>a))"
    rf"(?:\s+(?P<scale>hundred|thousand))?\b",
    re.I,
)
_ARTICLE_UNIT = re.compile(r"\ban?\s+(?=(?:second|minute|hour)s?\b)", re.I)


def words_to_numbers(text: str, *, minimum: int = 0) -> str:
    """Spoken numbers as digits ("five minutes" -> "5 minutes", "two thousand" -> "2000"), so a rule written for
    digits also reads a figure that was typed in words. Only numbers of at least ``minimum`` are changed."""

    def convert(m: re.Match[str]) -> str:
        scale = m.group("scale")
        if m.group("article"):  # "a hundred", "a thousand"; a bare "a" is left alone
            value = _SCALES[scale.lower()] if scale else None
        elif m.group("tens"):
            value = _TENS[m.group("tens").lower()] + (_ONES[m.group("ones").lower()] if m.group("ones") else 0)
        else:
            value = _ONES[m.group("small").lower()]
        if value is None:
            return m.group(0)
        if scale and not m.group("article"):
            value *= _SCALES[scale.lower()]
        return str(value) if value >= minimum else m.group(0)

    out = _SPOKEN_NUMBER.sub(convert, text)
    return _ARTICLE_UNIT.sub("1 ", out) if minimum <= 1 else out


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


def blocks(text: str) -> list[str]:
    """Paragraphs, with hard-wrapped lines joined. A new block starts at a blank line, a heading, a list item or a table row;
    other lines continue the block above."""
    found: list[str] = []
    current: list[str] = []

    def flush() -> None:
        if current:
            found.append(" ".join(current))
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
    return found


def units(text: str) -> list[str]:
    """Sentences, with hard-wrapped lines joined: the grain at which rules look for a contradiction."""
    found: list[str] = []
    for block in blocks(text):
        for part in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9`\"'(\[])", block):
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
    default: str | None = None  # the source text of the default, when there is one
    annotation: str | None = None  # the source text of the type, when there is one


@dataclass
class ModuleInfo:
    name: str  # "remit.limits"
    short: str  # "limits"
    path: str  # "src/remit/limits.py"
    names: set[str] = field(default_factory=set)  # top-level names, public and private
    classes: dict[str, set[str]] = field(default_factory=dict)  # class -> its members
    sigs: dict[str, list[Param]] = field(default_factory=dict)  # "new_id", "FixedClock" (its __init__), "FixedClock.advance"
    returns: dict[str, str | None] = field(default_factory=dict)  # "new_id" -> "str" (the return type, when written)
    lines: int = 0
    text: str = ""

    def has_member_anywhere(self, name: str) -> bool:
        return any(name in members for members in self.classes.values())


def _src(node: ast.AST | None) -> str | None:
    return None if node is None else ast.unparse(node)


def _params(fn: ast.FunctionDef | ast.AsyncFunctionDef, *, drop_first: bool) -> list[Param]:
    a = fn.args
    pos = [*a.posonlyargs, *a.args]
    defaults: list[ast.expr | None] = [None] * (len(pos) - len(a.defaults)) + list(a.defaults)
    out: list[Param] = []
    for n, (arg, default) in enumerate(zip(pos, defaults, strict=True)):
        out.append(Param(arg.arg, "posonly" if n < len(a.posonlyargs) else "pos", default is None, _src(default),
                         _src(arg.annotation)))
    if drop_first and out:
        out = out[1:]
    if a.vararg:
        out.append(Param(a.vararg.arg, "var", False, None, _src(a.vararg.annotation)))
    for arg, default in zip(a.kwonlyargs, a.kw_defaults, strict=True):
        out.append(Param(arg.arg, "kwonly", default is None, _src(default), _src(arg.annotation)))
    if a.kwarg:
        out.append(Param(a.kwarg.arg, "varkw", False, None, _src(a.kwarg.annotation)))
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
                    info.returns[node.name] = _src(node.returns)
                elif isinstance(node, ast.ClassDef):
                    info.names.add(node.name)
                    members: set[str] = set()
                    for member in node.body:
                        if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            members.add(member.name)
                            info.sigs[f"{node.name}.{member.name}"] = _params(member, drop_first=True)
                            info.returns[f"{node.name}.{member.name}"] = _src(member.returns)
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
        if rest[-1].lower() in FILE_EXTENSIONS and not module.has_member_anywhere(rest[-1]) and rest[-1] not in module.names:
            return None  # `audit.jsonl` is a file name, not a name in the module `audit`
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
    """One problem per offending sentence and rule: ``<what is wrong>: "<the words that caused it>"``.

    A rule whose exemption is a negation ("no", "not", "never", "whether" ...) only looks at the 70 characters before
    the claim and the claim itself: "customers sent it again after seeing no message" must not be excused by the "no"
    that comes after. Other exemptions (quoting a stale document, contrasting with an alternative) read the whole sentence.
    A figure written in words ("five minutes") is read as well as the same figure in digits.
    """
    problems: list[str] = []
    for unit in units(text):
        spoken = words_to_numbers(unit)
        variants = [unit] if spoken == unit else [unit, spoken]
        for rule in rules:
            local = rule.exempt is not None and NEGATION.pattern in rule.exempt.pattern
            hit: tuple[str, re.Match[str]] | None = None
            for variant in variants:
                for m in rule.pattern.finditer(variant):
                    if rule.exempt is not None and rule.exempt.search(variant[max(0, m.start() - 70):m.end()] if local else variant):
                        continue
                    if rule.expect is not None and rule.expect(m):
                        continue
                    hit = (variant, m)
                    break
                if hit:
                    break
            if hit:
                problem = f'{rule.message}: "{around(hit[0], hit[1].start(), hit[1].end())}"'
                if problem not in problems:
                    problems.append(problem)
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


_ADR_PARTS = ("status", "context", "decision", "consequences")
ADR_MINIMUM_WORDS = {"context": 25, "decision": 8, "consequences": 20}  # task.md says "a few sentences" for each
_ADR_LABEL = re.compile(r"^\s*(?:[-*+]\s+)?\**\s*(status|context|decision|consequences)\s*\**\s*[:\u2013\u2014-]\s*(\S.*)?$", re.I)


def adr_parts(text: str) -> dict[str, tuple[int, str]]:
    """The four parts of an ADR -> (line where it starts, its text).

    A part starts at a heading ("## Context") or at a label ("Context: ..." or "**Context:** ..."); it runs to the
    next heading or label. Both layouts are accepted, because Nygard's parts matter, not the markup.
    """
    lines = text.splitlines()
    parts: dict[str, list] = {}
    current: str | None = None
    for i, line in enumerate(lines):
        heading = _HEADING.match(line)
        if heading:
            title = re.sub(r"[`*_]", "", heading.group(2)).strip()
            name = next((p for p in _ADR_PARTS if re.match(rf"{p}\b", title, re.I)), None)
            if len(heading.group(1)) >= 2 and name and name not in parts:
                parts[name] = [i, []]
                current = name
            else:
                current = None
            continue
        label = _ADR_LABEL.match(line)
        if label and label.group(1).lower() not in parts:
            current = label.group(1).lower()
            parts[current] = [i, [label.group(2) or ""]]
            continue
        if current:
            parts[current][1].append(line)
    return {k: (v[0], "\n".join(v[1]).strip()) for k, v in parts.items()}


def adr_format_problems(text: str) -> list[str]:
    problems: list[str] = []
    if not any(s.level == 1 and s.title.strip() for s in outline(text)):
        problems.append("there is no title (a line starting with '# ')")
    parts = adr_parts(text)
    missing = [k.title() for k in _ADR_PARTS if k not in parts]
    if missing:
        problems.append("missing section(s): " + ", ".join(missing))
    else:
        starts = [parts[k][0] for k in _ADR_PARTS]
        if starts != sorted(starts):
            problems.append("the sections are out of order (expected Status, Context, Decision, Consequences)")
    if "status" in parts and not _STATUS.search(parts["status"][1][:200]):
        problems.append("Status is not one of Proposed, Accepted, Deprecated, Superseded")
    for key, words in ADR_MINIMUM_WORDS.items():
        if key in parts and len(parts[key][1].split()) < words:
            problems.append(f"{key.title()} is too thin (a few sentences, at least {words} words)")
    if "consequences" in parts and not _DOWNSIDE.search(parts["consequences"][1]):
        problems.append("Consequences name no downside (an ADR records what gets harder, not only what gets easier)")
    return problems


ADR_RULES: list[Rule] = [
    Rule("quote_ttl",
         _rx(r"\bquotes?\b[^.\n]{0,60}?\b(?:valid|expires?|expired|good|lasts?|lifetime|ttl)\b[^.\n]{0,40}?\b(\d+)\s*(seconds?|secs?|s|minutes?|mins?)\b"),
         "The quote lifetime disagrees with fx.QUOTE_TTL",
         expect=lambda m: (int(m.group(1)) * (60 if m.group(2).lower().startswith("m") else 1)) == 60,
         exempt=_rx(r"could|would|might|alternative|instead|longer|shorter|\bif\b|rather|option|propos|\bsay\b|e\.g\.|suppose|imagine")),
    Rule("quote_ttl_adj",
         _rx(r"\b(\d+)[- ](second|minute)s?\b[^.\n]{0,20}\bquote"),
         "The quote lifetime disagrees with fx.QUOTE_TTL",
         expect=lambda m: (int(m.group(1)) * (60 if m.group(2).lower() == "minute" else 1)) == 60,
         exempt=_rx(r"could|would|might|alternative|instead|longer|shorter|\bif\b|rather|option|propos|\bsay\b|e\.g\.|suppose|imagine")),
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
    Rule("express_before_cap", _rx(r"\bexpress\b[^.\n]{0,60}\bbefore the cap\b"),
         "Check fees.explain_fee: where the express surcharge is added disagrees with this",
         exempt=_rx(r"could|would|might|alternative|instead|\bif\b|rather|option|propos|should|\bnot\b|n't")),
    Rule("half_even", _rx(r"\b(?:Money|Remit|we|our|fees?|rounding)\b[^.\n]{0,60}\b(?:round\w*|use\w*)\b[^.\n]{0,30}\b(?:half[- ]even|banker'?s?)\b"),
         "Check money.quantize and ledger.post_transfer: the rounding rule disagrees with this",
         exempt=_rx(r"ledger|partner|Q-LED|default|python|decimal module|instead|rather|than|alternative|\bvs\b|versus|differs?|except|unlike|but\b|not\b|never|could|would")),
    Rule("float_ok", _rx(r"\b(?:accepts?|allows?|supports?|takes)\b[^.\n]{0,40}\bfloats?\b"),
         "Check money.Money: what it does with floats disagrees with this",
         exempt=_rx(r"reject|refus|rais|TypeError|never|not\b|no\b|without|instead")),
    Rule("all_placeholders", _rx(r"\ball queries use placeholders\b|\bevery query (?:is )?parameteri[sz]ed\b|\bqueries use placeholders\b"),
         "Check every query in src/remit/store.py: this disagrees with it",
         exempt=_rx(r"except|apart|search_by_name|known smell|stale|outdated|ARCHITECTURE|wrong|claims?|says")),
    Rule("notify_retries",
         _rx(r"\b(?:_notify|notif\w*|notifier)\b[^.\n]{0,80}\b(?:retr(?:y|ies|ied|ying)|back-?off|re-?sen[dt]s?|re-?queue[sd]?|outbox|dead[- ]letter)\b"),
         "Check RemitService._notify in src/remit/service.py: it catches the error and carries on; nothing there retries, queues or backs off",
         exempt=_rx(r"\b(?:no|not|never|nothing|none|nor|without|cannot|unlike|than|whether|if)\b|n't|could|would|might|alternative|"
                    r"instead|option|propos|should|rather|recommend|future|follow-up|ticket|deferred|steelman|consider|better|worth")),
]


def adr_fact_problems(text: str) -> list[str]:
    return apply_rules(prose_only(text), ADR_RULES)


def adr_references(text: str, index: CodeIndex) -> tuple[list[str], int, int]:
    """(unresolved references, number resolved, number resolved that point into src/).

    A reference to something that is not there is fine when its own sentence says so ("the old page names `risk.py`,
    which does not exist"): that is a true claim, not a pointer to nothing.
    """
    unresolved: list[str] = []
    resolved = in_src = 0
    seen: set[str] = set()
    for unit in units(prose_only(text)):
        refuted = bool(REFUTES.search(unit))
        for token in re.findall(r"`([^`\n]+)`", unit):
            token = token.strip()
            if token in seen:
                continue
            verdict = index.resolve_path(token)
            kind = "path"
            if verdict is None:
                verdict = index.resolve_symbol(token)
                kind = "symbol"
            if verdict is None:
                continue
            if not verdict and refuted:
                continue
            seen.add(token)
            if verdict:
                resolved += 1
                if kind == "symbol" or token.lstrip("./").startswith("src/") or re.match(r"[\w.-]+\.py", token):
                    in_src += 1
            else:
                unresolved.append(token)
    return unresolved, resolved, in_src


CRITIC_HEAD = r"critic|objection|challenge|steelman|devil"
OBJECTION_WORDS = 8  # an objection with its response is a sentence or two, not a label
# What you did about an objection. "Noted" and "see above" are not decisions.
RESPONSE_CUE = re.compile(
    r"\b(accept(?:ed|s)?|reject(?:ed|s)?|defer(?:red|s)?|postpon\w+|declin\w+|dismiss\w+|agree[ds]?|disagree[ds]?|adopt\w+|upheld|"
    r"overrul\w+|concede[ds]?|address(?:ed)?|mitigat\w+|keep|kept|retain\w*|stay with|stand by|chose|changed|added|rewrote|"
    r"incorporated|revised|updated|follow[- ]up|ticket|out of scope|no change|not changing|won'?t fix|"
    r"we (?:will|did|do|decided)|i (?:will|did|decided))\b",
    re.I,
)
_RESPONSE_HEAD = re.compile(r"respon|answer|decision|disposition|outcome|repl|resolution|action", re.I)


def sub_sections(secs: Sequence[Sec], parent: Sec) -> list[Sec]:
    """The sections nested directly or indirectly under ``parent`` (the outline is in document order)."""
    start = next(i for i, s in enumerate(secs) if s is parent)
    nested = []
    for s in secs[start + 1:]:
        if s.level <= parent.level:
            break
        nested.append(s)
    return nested


def _table_cells(row: str) -> list[str]:
    return [c.strip() for c in row.strip().strip("|").split("|")]


# "Critic's objections:" on a line of its own works like a heading, as "Status:" and "Context:" do for the other parts
_CRITIC_LABEL = re.compile(r"^[ \t]*(?:[-*+][ \t]+)?\**[ \t]*((?:the[ \t]+)?(?:critic|objections?)[^\n:]{0,40}?)[ \t]*\**[ \t]*:[ \t]*\**[ \t]*(.*)$",
                           re.I | re.M)


def adr_critic_problems(text: str) -> list[str]:
    secs = outline(text)
    sec = find_section(secs, CRITIC_HEAD)
    if sec is None:
        label = _CRITIC_LABEL.search(text)
        if label:
            body = (label.group(2) + "\n" + text[label.end():]).strip()
            sec = Sec(2, label.group(1).strip(), body, body)
    if sec is None:
        return ["there is no section for the critic's objections (a heading, or a line like \"Critic's objections:\")"]
    nested = sub_sections(secs, sec) if sec in secs else []
    if len(nested) >= 3:  # one sub-heading per objection
        candidates = [f"{n.title} {n.full}" for n in nested]
    else:
        candidates = list_items(sec.full)
    table_rows = [ln for ln in sec.full.splitlines() if ln.strip().startswith("|")]
    response_column = None
    if table_rows:
        heads = _table_cells(table_rows[0])
        response_column = next((i for i, h in enumerate(heads) if _RESPONSE_HEAD.search(h)), None)
    items = [c for c in candidates if len(c.split()) >= OBJECTION_WORDS]
    if len(items) < 3:
        short = len(candidates) - len(items)
        why = (f" ({short} more are too short to count: write a full sentence and what you did, at least "
               f"{OBJECTION_WORDS} words)") if short else ""
        return [f"found {len(items)} objection(s); the task asks for at least 3" + why]

    def response_of(item: str) -> str:
        if response_column is not None and item.strip().startswith("|"):
            cells = _table_cells(item)
            if len(cells) > response_column:
                return cells[response_column]
        return item

    answered = sum(1 for i in items if RESPONSE_CUE.search(response_of(i)))
    if answered < 3:
        return [f"only {answered} objection(s) say what you did about them (accepted, rejected with a reason, deferred)"]
    return []


# =================================================================================
# 5. najmkit page checks
# =================================================================================
NAJMKIT_MODULES = ("ids", "clock", "audit")
_QUAL = re.compile(r"(?<![\w.])(?:najmkit\.)?(ids|clock|audit)\.([A-Za-z_]\w*)(?:\.([A-Za-z_]\w*))?")
_IMPORT = re.compile(r"^\s*from\s+najmkit(?:\.(\w+))?\s+import\s+([^\n#]+)", re.M)
_PLAIN_IMPORT = re.compile(r"^\s*import\s+najmkit(?:\.(\w+))?", re.M)
COVERAGE_EXCLUDE = {"Clock"}  # a Protocol: documenting FixedClock and SystemClock covers it


def _module(index: CodeIndex, short: str) -> ModuleInfo | None:
    return index.modules.get(f"najmkit.{short}")


def docs_name_problems(text: str, index: CodeIndex) -> list[str]:
    problems: list[str] = []

    def refuted(position: int) -> bool:
        """The line holding ``position`` says the name is not there ("`ids.generate` does not exist")."""
        start = text.rfind("\n", 0, position) + 1
        end = text.find("\n", position)
        return bool(REFUTES.search(text[start:end if end != -1 else len(text)]))

    for m in _QUAL.finditer(text):
        short, name, member = m.group(1), m.group(2), m.group(3)
        if name in FILE_EXTENSIONS:
            continue
        module = _module(index, short)
        if module is None:
            continue
        claim = f"{short}.{name}" + (f".{member}" if member else "")
        if name not in module.names:
            if not module.has_member_anywhere(name) and not refuted(m.start()):
                problems.append(f"`{claim}` does not exist in najmkit.{short}")
            continue
        if member and name in module.classes and member not in module.classes[name] and not refuted(m.start()):
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


def _balanced_end(text: str, start: int) -> int | None:
    """The index of the ``)`` that closes the ``(`` at ``text[start]``."""
    depth = 0
    for i in range(start, min(len(text), start + 400)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return i
    return None


def _balanced(text: str, start: int) -> str | None:
    end = _balanced_end(text, start)
    return None if end is None else " ".join(text[start + 1:end].split())


def read_annotation(tail: str) -> str | None:
    """The return type written after a closing parenthesis (``-> str``, ``-> dict[str, Any] | None``), else None."""
    arrow = re.match(r"\s*->\s*", tail)
    if not arrow:
        return None
    i, n, parts = arrow.end(), len(tail), []
    while True:
        ident = re.match(r"[A-Za-z_][\w.]*", tail[i:])
        if not ident:
            break
        j = i + ident.end()
        if j < n and tail[j] == "[":
            depth, k = 0, j
            while k < n:
                depth += (tail[k] == "[") - (tail[k] == "]")
                if depth == 0:
                    break
                k += 1
            if depth != 0:
                return None
            j = k + 1
        parts.append(tail[i:j])
        union = re.match(r"\s*\|\s*", tail[j:])
        if not union:
            break
        i = j + union.end()
    return " | ".join(parts) if parts else None


def annotation_tokens(source: str) -> frozenset[str]:
    """The type names in an annotation, in a form that ignores spelling: ``Optional[str]`` and ``str | None`` agree."""
    try:
        tree = ast.parse(source, mode="eval")
    except SyntaxError:
        return frozenset()
    inner = {id(n.value) for n in ast.walk(tree) if isinstance(n, ast.Attribute)}  # `os` in `os.PathLike`
    tokens: set[str] = set()
    for node in ast.walk(tree):
        if id(node) in inner:
            continue
        if isinstance(node, ast.Name):
            tokens.add(node.id)
        elif isinstance(node, ast.Attribute):
            tokens.add(node.attr)
        elif isinstance(node, ast.Constant):
            if node.value is None:
                tokens.add("None")
            elif isinstance(node.value, str):
                tokens |= annotation_tokens(node.value)
    if "Optional" in tokens:
        tokens.add("None")
    return frozenset(tokens - {"Optional", "Union"})


@dataclass
class Claim:
    """What the text between the parentheses of a claimed signature or call says."""
    form: str  # "signature" (``prefix: str, **fields``) or "call" (``"TRF", length=3``)
    params: list[Param]
    positional: int  # required positional parameters (signature) or positional arguments (call)
    keywords: list[str]
    declares: bool  # True when it can only be a declaration (annotations, defaults, stars)
    annotated: bool  # True when a type is written: only a signature does that


def read_claim(inside: str) -> Claim | None:
    """None when the text is neither (``path | None = None`` and the like)."""
    try:
        fn = ast.parse(f"def _({inside}): pass").body[0]
        assert isinstance(fn, ast.FunctionDef)
        a = fn.args
        params = _params(fn, drop_first=False)
        annotated = any(x.annotation for x in [*a.posonlyargs, *a.args, *a.kwonlyargs, a.vararg, a.kwarg] if x)
        declares = bool(a.defaults or a.kw_defaults or a.vararg or a.kwarg or a.kwonlyargs or annotated)
        # a parameter with a default may be a keyword argument in a call (`seconds=61`), so it is not counted as positional
        return Claim("signature", params, sum(1 for p in params if p.kind in ("pos", "posonly") and p.required), [],
                     declares, annotated)
    except (SyntaxError, AssertionError, IndexError):
        pass
    try:
        call = ast.parse(f"_({inside})", mode="eval").body
        assert isinstance(call, ast.Call)
        positional = sum(1 for a in call.args if not isinstance(a, ast.Starred))
        return Claim("call", [], positional, [k.arg for k in call.keywords if k.arg], True, False)
    except (SyntaxError, AssertionError):
        return None


def claimed_params(inside: str) -> tuple[str, list[Param], int, list[str], bool] | None:
    claim = read_claim(inside)
    return None if claim is None else (claim.form, claim.params, claim.positional, claim.keywords, claim.declares)


def _same_default(a: str, b: str) -> bool:
    def norm(source: str) -> str:
        try:
            return ast.unparse(ast.parse(source, mode="eval"))
        except SyntaxError:
            return source.strip()

    return norm(a) == norm(b)


def signature_problem(label: str, inside: str, real: list[Param], *, claimed_return: str | None = None,
                      real_return: str | None = None, method: bool = False) -> str | None:
    """Does the claimed signature fit the real one?

    A claim that looks like a call (``seconds=61``, bare names) is only held to the real function's capacity: no more
    positional arguments than it takes, no keyword it does not have. A claim that can only be a signature (a type is
    written, or ``-> type`` follows) is held to the def line: every parameter, in order, with the right default and types.
    A method's ``self`` may be written or left out.
    """
    if not inside.strip() and claimed_return is None:
        return None  # `ids.new_id()` is shorthand for "the function", not a claim about its arguments
    claim = read_claim(inside)
    if claim is None:
        return None
    form, params, positional, keywords, declares = claim.form, list(claim.params), claim.positional, claim.keywords, claim.declares
    if method and form == "signature" and params and params[0].name in ("self", "cls") and params[0].kind in ("pos", "posonly"):
        params, positional = params[1:], max(0, positional - 1)
    strict = form == "signature" and (claim.annotated or claimed_return is not None)
    shown = f"`{label}({inside})" + (f" -> {claimed_return}" if claimed_return else "") + "`"
    names = {p.name for p in real}
    varkw = next((p.name for p in real if p.kind == "varkw"), None)
    has_var = any(p.kind == "var" for p in real)
    capacity = sum(1 for p in real if p.kind in ("pos", "posonly"))
    if positional > capacity and not has_var:
        return f"{shown}: the real function takes at most {capacity} positional argument(s)"
    if not declares and not strict:
        return None
    claimed = [(p.name, p.kind) for p in params] if form == "signature" else [(k, "kwonly") for k in keywords]
    for name, kind in claimed:
        if kind in ("var", "varkw"):
            continue
        if name in names and name != varkw:
            continue
        if varkw is not None:
            if name == varkw and form == "signature":
                return f"{shown}: '{name}' is the **{name} catch-all, not a parameter called '{name}'"
            continue
        return f"{shown}: '{name}' is not a parameter of {label.split('.')[-1]}"
    if not strict:
        return None
    claimed_names, claimed_kinds = {p.name for p in params}, {p.kind for p in params}
    for p in real:
        if p.name not in claimed_names and not (p.kind in ("var", "varkw") and p.kind in claimed_kinds):  # `**kwargs` is as good as `**fields`
            return f"{shown}: the signature leaves out '{p.name}'"
    order = [p.name for p in real if p.kind in ("pos", "posonly")]
    if [p.name for p in params if p.kind in ("pos", "posonly") and p.name in order] != order:
        return f"{shown}: the parameters are not in the order of the def line"
    by_name = {p.name: p for p in real}
    for p in params:
        r = by_name.get(p.name)
        if r is None:
            continue
        if p.default is not None and r.default is not None and not _same_default(p.default, r.default):
            return f"{shown}: the default of '{p.name}' disagrees with the def line"
        if p.default is not None and r.default is None:
            return f"{shown}: '{p.name}' has no default in the code"
        if p.default is None and r.default is not None and p.kind in ("pos", "posonly", "kwonly"):
            return f"{shown}: '{p.name}' is optional in the code: show its default"
        if p.annotation and r.annotation and not annotation_tokens(p.annotation) <= annotation_tokens(r.annotation):
            return f"{shown}: the type of '{p.name}' disagrees with the def line"
    if claimed_return and real_return and not annotation_tokens(claimed_return) <= annotation_tokens(real_return):
        return f"{shown}: the return type disagrees with the def line"
    return None


def _fenced_defs(text: str) -> list[tuple[str | None, str, str, str | None]]:
    """(class, name, text between the parentheses, return type) of every ``def`` line inside a fenced code block."""
    found = []
    for _, body in code_blocks(text):
        classes = [(len(m.group(1).expandtabs(4)), m.start(), m.group(2)) for m in re.finditer(r"^([ \t]*)class\s+(\w+)", body, re.M)]
        for m in re.finditer(r"^([ \t]*)(?:async\s+)?def\s+(\w+)\s*\(", body, re.M):
            end = _balanced_end(body, m.end() - 1)
            if end is None:
                continue
            indent = len(m.group(1).expandtabs(4))
            owner = next((name for ind, pos, name in reversed(classes) if pos < m.start() and ind < indent), None)
            tail = body[end + 1:end + 200].split("\n", 1)[0]
            found.append((owner, m.group(2), " ".join(body[m.end():end].split()), read_annotation(tail)))
    return found


def docs_signature_problems(text: str, index: CodeIndex) -> list[str]:
    """Every signature the page writes down (inline, in a table, in a heading, or as a ``def`` line in a code block)."""
    problems: list[str] = []
    text = text.replace("\\|", " |")  # a pipe inside a table cell is written \| (same length, so positions agree)
    flat = text.replace("\n", " ")  # same length as ``text``, so positions agree
    public: dict[str, tuple[ModuleInfo, str]] = {}
    for short in NAJMKIT_MODULES:
        module = _module(index, short)
        if module is None:
            continue
        for key in module.sigs:
            public.setdefault(key, (module, key))
    checked: set[tuple[str, str, str | None]] = set()

    def check(label: str, key: str, module: ModuleInfo, inside: str, ret: str | None) -> None:
        if (key, inside, ret) in checked:
            return
        checked.add((key, inside, ret))
        method = "." in key or key in module.classes
        problem = signature_problem(label, inside, module.sigs[key], claimed_return=ret,
                                    real_return=None if key in module.classes else module.returns.get(key), method=method)
        if problem:
            problems.append(problem)

    def tail_of(close: int) -> str | None:
        return read_annotation(text[close + 1:close + 200].split("\n", 1)[0])

    for m in _QUAL.finditer(flat):
        short, name, member = m.group(1), m.group(2), m.group(3)
        end = m.end()
        if flat[end:end + 1] != "(" or name in FILE_EXTENSIONS:
            continue
        module = _module(index, short)
        key = f"{name}.{member}" if member else name
        if module is None or key not in module.sigs:
            continue
        close = _balanced_end(flat, end)
        if close is None:
            continue
        check(f"{short}.{key}", key, module, " ".join(flat[end + 1:close].split()), tail_of(close))
    classes = {c for mod, _ in public.values() for c in mod.classes}
    for m in re.finditer(r"(?<![\w.])([A-Z]\w*)\.([A-Za-z_]\w*)(?=\()", flat):  # `FixedClock.set(...)`
        cls, member = m.group(1), m.group(2)
        key = f"{cls}.{member}"
        if cls in classes and key in public:
            module = public[key][0]
            close = _balanced_end(flat, m.end())
            if close is not None:
                check(key, key, module, " ".join(flat[m.end() + 1:close].split()), tail_of(close))
    names_unqualified = {key: mod for key, (mod, _) in public.items() if "." not in key and key != "now"}
    for m in re.finditer(r"(?<![\w.])([A-Za-z_]\w*)\s*(?=\()", flat):
        key = m.group(1)
        if key not in names_unqualified:
            continue
        close = _balanced_end(flat, m.end())
        if close is None:
            continue
        check(key, key, names_unqualified[key], " ".join(flat[m.end() + 1:close].split()), tail_of(close))
    for line in text.splitlines():  # a bare `name()` that opens a table row, heading or list item is meant as the signature
        if not (line.lstrip().startswith(("|", "#", "- ", "* ", "+ ")) or re.match(r"\s*\d+[.)]\s", line)):
            continue
        spans = [sp.strip() for sp in re.findall(r"`([^`\n]+)`", line)]
        bare = re.fullmatch(r"(?:najmkit\.)?(?:(ids|clock|audit)\.)?([A-Za-z_]\w*)(?:\.([A-Za-z_]\w*))?\(\)", spans[0]) if spans else None
        if not bare:
            continue
        short, name, member = bare.groups()
        key = f"{name}.{member}" if member else name
        module = _module(index, short) if short else (public[key][0] if key in public else None)
        if module is None or key not in module.sigs:
            continue
        last = member or name
        if any(re.match(rf"(?:[\w.]*\.)?{re.escape(last)}\(\s*\S", sp) for sp in spans[1:]):
            continue  # the same row also writes the function with its parameters
        required = [p for p in module.sigs[key] if p.required and p.kind in ("pos", "posonly", "kwonly")]
        if required:
            problems.append(f"`{spans[0]}`: the signature leaves out '{required[0].name}' (write the parameters, as on the def line)")
    for owner, name, inside, ret in _fenced_defs(text):  # a `def` line copied into a code block is a signature too
        key = f"{owner}.{name}" if owner else name
        if key in public and (owner or not inside.startswith(("self", "cls"))):
            check(key, key, public[key][0], inside, ret)
    return list(dict.fromkeys(problems))


def prose_word_count(text: str) -> int:
    """Words of explanation: the page without its code blocks and without its inline code."""
    prose = re.sub(r"`[^`\n]*`", " ", prose_only(text))
    return len(re.findall(r"[A-Za-z][A-Za-z'-]*", prose))


PAGE_MIN_WORDS, PAGE_MIN_PROSE = 60, 40  # a page that is only a list of signatures does not say what anything does


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
    """(names covered, public names, the ones missing). A name is covered when the page writes it with its signature
    (``name(...)``); a bare mention in a list is not documentation."""
    names = public_names(work)
    missing = [n for n in names if not re.search(rf"(?<![A-Za-z_]){re.escape(n)}\s*\(|\bclass\s+{re.escape(n)}\b", text)]
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
        Rule("token_length", _rx(r"\btokens?\b[^\n]{0,40}?\b(\d+)[- ](?:hex(?:adecimal)?[- ])?(?:characters?|chars?|digits?|symbols?)\b"),
             "The token length disagrees with ids.new_id (random tokens) or ids.SequentialIds",
             expect=lambda m: _int(m.group(1)) in (12, 6), exempt=NEGATION),
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
        Rule("locking", _rx(r"\b(?:log_event|read_events|audit|new_id|najmkit)\b[^.\n]{0,80}\b(?:locks?|locked|locking|mutex|semaphore|fsync|atomic(?:ally)?)\b"),
             "Nothing in najmkit takes a lock, syncs to disk or writes atomically: read the code", exempt=NEGATION),
        Rule("audit_extras", _rx(r"\b(?:log_event|audit)\b[^.\n]{0,100}\b(?:retries|retry|retried|rotates|rotation|compress\w*|batch\w*|buffer\w*|flush\w*|encrypt\w*|signs|signed|hash chain)\b"),
             "Nothing in audit.log_event does this: read it", exempt=NEGATION),
    ]


def docs_fact_problems(text: str, facts: dict[str, str]) -> list[str]:
    return apply_rules(prose_only(text), docs_rules(facts))


def known_problems_problems(text: str) -> list[str]:
    """The ticket sends a comment that disagrees with the code to a 'Known problems' section (and says to leave the code alone).

    Checked loosely: such a section exists, says something, and names the function whose comment is wrong (found by
    reading the code, not given away here).
    """
    sec = find_section(outline(text), r"known (?:problems|issues)|discrepanc|doc(?:string)? (?:problems|issues)|errata")
    if sec is None:
        return ["there is no 'Known problems' section"]
    if len(sec.full.split()) < 12:
        return ["'Known problems' is nearly empty"]
    if not re.search(r"read_events", sec.full):
        return ["'Known problems' does not report the comment that the running code contradicts (call the functions the docstrings make promises about)"]
    return []


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
# What each module offers, for crediting an example to a module when it is imported by name
# (`from najmkit.ids import new_id`), as well as when it is called as `ids.new_id(...)`.
_MODULE_CALLABLES = {
    "ids": ("new_id", "SequentialIds", "use_generator"),
    "clock": ("SystemClock", "FixedClock", "now", "set_clock", "get_clock", "reset_clock"),
    "audit": ("configure", "current_path", "log_event", "read_events"),
}


def modules_used(source: str) -> set[str]:
    """The najmkit modules a statement really uses: `ids.x`, `najmkit.ids.x`, or a call to one of their functions or
    classes by its bare name. Read from the syntax tree, so a word inside a string (`"audit.jsonl"`) does not count."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    used: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            base = node.value
            if isinstance(base, ast.Name) and base.id in NAJMKIT_MODULES:
                used.add(base.id)
            elif (isinstance(base, ast.Attribute) and isinstance(base.value, ast.Name)
                  and base.value.id == "najmkit" and base.attr in NAJMKIT_MODULES):
                used.add(base.attr)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            used.update(mod for mod, names in _MODULE_CALLABLES.items() if node.func.id in names)
    return used


_IMPORT_LINE = re.compile(r"\bfrom\s+najmkit(?:\.\w+)?\s+import\s+[\w, ]+|\bimport\s+najmkit(?:\.\w+)?")


def doc_statements(text: str) -> list[str]:
    """Every top-level statement of every Python block that parses (blocks of signatures do not).

    An import that the page shows only in prose ("import them as `from najmkit import ids, clock, audit`") is
    put in front, so a page may state its import once.
    """
    statements: list[str] = []
    for lang, body in code_blocks(text):
        if lang not in ("python", "py", "python3", "pycon"):
            continue
        if ">>> " in body:  # a doctest-style session: the lines after each prompt are the statements
            statements.extend(ex.source.rstrip("\n") for ex in doctest.DocTestParser().get_examples(body))
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
            for module in modules_used(source):
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
        self.event_minutes: dict[str, int] = {e["id"]: int(e["time"][:2]) * 60 + int(e["time"][3:5]) for e in data["timeline"]}
        self.count_numbers, self.minute_numbers, self.written_numbers = self._numbers()
        self.diff_minutes: set[int] = {abs(a - b) for a in self.event_minutes.values() for b in self.event_minutes.values()}
        self.written_minutes: set[int] = {int(n) for v in _strings(data) for n in re.findall(r"(\d+)\s*(?:minutes?|mins?)\b", v)}
        self.percentages: set[int] = {int(float(n)) for v in _strings(data) for n in re.findall(r"(\d+(?:\.\d+)?)\s?%", v)}
        self.words: set[str] = {w.lower() for v in _strings(data) for w in re.findall(r"[A-Za-z][A-Za-z'-]{2,}", v)}

    def _numbers(self) -> tuple[set[int], set[int], set[int]]:
        """Numbers a postmortem may use: counts (the record's, and a few meaningful differences), minutes (differences of
        times) and the numbers the record itself writes in its titles and event texts."""

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
        entries = {len(self.data["timeline"]), len(self.data.get("responders", []))}  # "the record has 13 events"
        return numbers | from_text | entries, in_minutes | from_text, from_text


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
    for key, minimum in (("summary", 10), ("impact", 5), ("timeline", 12), ("facts", 6), ("inferences", 6), ("unknowns", 6), ("actions", 6)):
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
_PERCENT = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)\s?(?:%|percent\b|per ?cent\b)", re.I)
_CLOCK = re.compile(r"(?<![\d:.-])(\d{1,2}):(\d{2})(?::\d{2})?(?![\d:])")
_MONTH_NAMES = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                "November", "December")
_MONTH_RX = "|".join(f"{m}|{m[:3]}" for m in _MONTH_NAMES)
_DAY_MONTH = re.compile(rf"\b(\d{{1,2}})(?:st|nd|rd|th)?\s+({_MONTH_RX})\b")
_MONTH_DAY = re.compile(rf"\b({_MONTH_RX})\s+(\d{{1,2}})(?:st|nd|rd|th)?\b")


def _month_number(name: str) -> int:
    return next(i for i, m in enumerate(_MONTH_NAMES, start=1) if m.startswith(name[:3]))


def _anchor_minutes(block: str, record: Record) -> set[int]:
    """The times (in minutes) of the events a paragraph, bullet or table row cites, by id (E4) or by clock time (10:19)."""
    found = {record.event_minutes[f"E{n}"] for n in re.findall(r"\bE(\d+)\b", block) if f"E{n}" in record.event_minutes}
    found.update(int(hh) * 60 + int(mm) for hh, mm in _CLOCK.findall(block))
    return found


def invented_facts(text: str, record: Record) -> list[str]:
    """Numbers with units, percentages, clock times, dates, ids, severity and versions that are not in the record.

    A duration that the record does not write down itself ("52 minutes" is in its title) must be tied to the events it spans:
    the paragraph, bullet or table row must cite an event (E1) or a time (09:58) that is that many minutes from another event.
    """
    problems: list[str] = []
    spoken = words_to_numbers(text, minimum=4)  # "thirteen minutes", "two thousand customers"
    for block in blocks(re.sub(r"\bINC-\d+\b", " ", spoken)):
        for m in _NUMBER_UNIT.finditer(block):
            value = int(m.group(1).replace(",", ""))
            unit = m.group(0)[len(m.group(1)):]
            if re.search(r"hours?|hrs?", unit, re.I):
                allowed = value <= 2
            elif re.search(r"seconds?|secs?", unit, re.I):
                allowed = value <= 59
            elif re.search(r"minutes?|mins?", unit, re.I):
                if value in record.written_minutes:  # "52 minutes" is in the record's own title
                    allowed = True
                elif value in record.diff_minutes:
                    anchors = _anchor_minutes(block, record)
                    spans = {abs(a - b) for a in anchors for b in record.event_minutes.values()}
                    allowed = value in spans
                    if not allowed:
                        problems.append(f"{value} minutes is the gap between some two events in the record, but this text does not cite "
                                        "events that are that far apart: name the two events it spans (for example E1 and E2)")
                        continue
                else:
                    allowed = False
            else:
                allowed = value in record.count_numbers
            if not allowed:
                problems.append(f"the number {m.group(1)} ('{snippet(m.group(0), 30)}') is not in the record and is not a difference of times or counts in it")
        for m in _PERCENT.finditer(block):
            if int(float(m.group(1))) not in record.percentages:
                problems.append(f"the percentage {m.group(1)}% is not in the record: give the counts it comes from (for example 171 of 188)")
    body = re.sub(r"\bINC-\d+\b", " ", text)
    for hh, mm in _CLOCK.findall(body):
        if f"{int(hh):02d}:{mm}" not in record.times:
            problems.append(f"the time {hh}:{mm} is not the time of any event in the record")
    allowed_dates = {(int(d[5:7]), int(d[8:10])) for d in record.dates}
    for iso in re.findall(r"\b\d{4}-\d{2}-\d{2}\b", body):
        if iso not in record.dates:
            problems.append(f"the date {iso} is not in the record")
    spoken = [(_month_number(mo), int(d)) for d, mo in _DAY_MONTH.findall(body)] + \
             [(_month_number(mo), int(d)) for mo, d in _MONTH_DAY.findall(body)]
    for month, day in dict.fromkeys(spoken):
        if (month, day) not in allowed_dates:
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


_BASELINE_MARKER = re.compile(
    r"week (?:earlier|before)|last week|a week|one week|previous week|baseline|4 March|2026-03-04|same window|compared|against|"
    r"versus|\bvs\b|\bthan\b|usual|normal|typical|before|earlier|previous|prior|\bago\b|the week|last wednesday",
    re.I,
)


def _leaf_values(node: object) -> list[int]:
    if isinstance(node, bool):
        return []
    if isinstance(node, (int, float)):
        return [int(node)]
    if isinstance(node, dict):
        return [v for child in node.values() for v in _leaf_values(child)]
    return []


def misassigned_counts(text: str, record: Record, key: dict) -> list[str]:
    """A number that is in the record but belongs to another measure ("176 transfers sent" is last week's figure).

    ``key["measures"]`` lists, per measure, how it is worded in prose and where the record keeps it. A figure for the
    incident window must be the window's; last week's figure is fine when the same sentence says it is last week's.
    """
    problems: list[str] = []
    text = words_to_numbers(text, minimum=4)
    for measure in key.get("measures", []):
        window: set[int] = set()
        baseline: set[int] = set()
        for name in measure["keys"]:  # top-level keys of "counts" and "baseline" ("transfer.sent" is one key)
            for source, bucket in ((record.data.get("counts", {}), window), (record.data.get("baseline", {}), baseline)):
                node = source.get(name)
                leaves = _leaf_values(node)
                bucket.update(leaves)
                if isinstance(node, dict):
                    bucket.add(sum(leaves))
        pattern = re.compile(measure["pattern"], re.I)
        for unit in units(text):
            for m in pattern.finditer(unit):
                value = int(m.group(1).replace(",", ""))
                if value in window or (value in baseline and _BASELINE_MARKER.search(unit)):
                    continue
                problems.append(f"{value} is not the record's figure for {measure['say']} in the incident window"
                                + (" (it is the figure for another week: say so)" if value in baseline else ""))
                break
    return list(dict.fromkeys(problems))


_ROLE = (r"(?:sre|engineer|engineers|lead|manager|commander|analyst|officer|director|head|developer|operator|responder|"
         r"supervisor|owner|administrator|dba|technician|agent)")
_PERSON_VERBS = (r"(?:acknowledged|paged|opened|declared|escalated|joined|called|phoned|emailed|messaged|noticed|investigated|"
                 r"diagnosed|approved|decided|posted|wrote|reported|confirmed|asked|told|said|read|checked|ran|took|closed|"
                 r"added|finished|started|began|responded|replied)")
_NAMED = r"(?-i:\b([A-Z][a-z]{2,})\b)"
_PERSON_PATTERNS = [
    re.compile(rf"{_NAMED}\s*,\s*(?:the|our|an?)\s+(?:[\w-]+\s+){{0,3}}?{_ROLE}\b", re.I),  # Hassan, the on-call SRE
    re.compile(rf"\b{_ROLE}\s*(?:,|\()\s*{_NAMED}", re.I),  # the on-call SRE, Hassan  /  the SRE (Hassan)
    re.compile(rf"\b{_ROLE}\s+{_NAMED}", re.I),  # engineer Fatima
    re.compile(rf"\b(?:by|with|from|to|asked|told|paged|called|phoned|emailed|messaged|thanks to)\s+{_NAMED}", re.I),  # paged Hassan
    re.compile(rf"(?<=[a-z,;:] ){_NAMED}\s+{_PERSON_VERBS}\b", re.I),  # ... and Hassan acknowledged the page
]
_NOT_NAMES = {
    "najm", "remit", "bank", "qatar", "doha", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
    "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
    "december", "english", "arabic", "python", "utc", "the", "this", "that", "these", "those", "they", "them", "workbook",
    "none", "nobody", "someone", "everyone", "anyone", "team", "teams", "staff", "engineering", "operations", "platform",
    "security", "product", "management", "leadership", "compliance", "governance", "support", "payments", "customer",
}


def invented_people(text: str, record: Record) -> list[str]:
    """People the record does not name: the cast of the course, and anyone introduced by a name next to a role
    ("Hassan, the on-call SRE", "paged Hassan"). A name that appears in the record (Maha) is fine."""
    found: dict[str, None] = {}
    for name in CAST:
        if name not in record.people and re.search(rf"\b{name}\b", text):
            found[name] = None
    for pattern in _PERSON_PATTERNS:
        for m in pattern.finditer(text):
            name = m.group(1)
            if name not in record.people and name.lower() not in record.words and name.lower() not in _NOT_NAMES:
                found[name] = None
    return [f"{name} is not named in the record" for name in found]


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
        return ["there is no 'What we infer' section"]
    items = [i for i in list_items(sec.full) if len(i.split()) >= 6]
    if len(items) < 2:
        return [f"found {len(items)} inference(s) of six words or more; a postmortem that infers nothing is rarely complete (expected at least 2)"]
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
        return ["there is no 'What we do not know' section"]
    items = [i for i in list_items(sec.full) if len(i.split()) >= 4]
    problems = []
    if len(items) < 2:
        problems.append(f"found {len(items)} open question(s) of four words or more; the record leaves several (expected at least 2)")
    hits = sum(1 for pattern in key["gaps"] if re.search(pattern, sec.full, re.I))
    if hits < key["min_gaps"]:
        problems.append(f"the open questions name {hits} of the real gaps in the record (at least {key['min_gaps']} expected)")
    return problems


BLAME = re.compile(r"\b(blame|blamed|fault of|careless|negligen\w*|forgot|incompeten\w*|sloppy|human error|operator error|engineer error)\b", re.I)
# fault put on a person or a team: "the on-call SRE was slow to respond", "support should have escalated"
BLAME_ROLE = re.compile(
    r"\b(?:sre|engineers?|lead|commander|team|operators?|responders?|support|on-call|maha)\b[^.\n]{0,60}"
    r"\b(?:should have|failed to|slow to|too slow|was slow|were slow|neglected|ignored|was late|were late|missed (?:the|an?) (?:page|alert|call))\b",
    re.I,
)


def blame_problems(text: str) -> list[str]:
    return [f'"{snippet(u, 64)}"' for u in units(text) if (BLAME.search(u) or BLAME_ROLE.search(u)) and not NEGATION.search(u)]


def preamble(text: str) -> str:
    """The title and the lines before the first '## ' heading (severity, service, version, date ...)."""
    lines = text.splitlines()
    end = next((i for i, ln in enumerate(lines) if ln.startswith("## ")), len(lines))
    return "\n".join(lines[:end])


def section_texts(sections: dict[str, Sec], keys: Iterable[str]) -> str:
    return "\n".join(sections[k].full for k in keys if k in sections)


def action_item_count(sec: Sec | None) -> int:
    return 0 if sec is None else len([i for i in list_items(sec.full) if len(i.split()) >= 5])


_OWNER = re.compile(
    r"\b(?:owners?|owned by|assigned to|led by|responsible|team|sre|engineers?|engineering|lead|support|payments|platform|product|"
    r"on-call|commander|security|ops|operations|quality|qa|manager|compliance|governance|vendor management|"
    + "|".join(CAST) + r")\b", re.I)
_DONE = re.compile(
    r"\b(?:done (?:when|if)|complete when|we will know|verif\w+|measur\w+|tests?|tested|replay\w*|drill|alert fires|dashboard|"
    r"reviewed?|merged|ticket|passes|visible|evidence|confirm\w*|checks?|checked|metric|exercise|rehears\w+|shows?|appears?|exists?)\b", re.I)


def action_item_problems(sec: Sec | None) -> list[str]:
    """Three action items, each with an owner (a role or a team) and a way to see that it is done."""
    if sec is None:
        return []
    items = [i for i in list_items(sec.full) if len(i.split()) >= 5]
    if len(items) < 3:
        return [f"found {len(items)} action item(s) of five words or more; at least 3 are expected"]
    complete = [i for i in items if _OWNER.search(i) and _DONE.search(i)]
    if len(complete) < 3:
        return [f"only {len(complete)} of {len(items)} action items name an owner (a role or a team) and say how we will see "
                "that they are done; at least 3 must"]
    return []


# =================================================================================
# 7. the repository: one commit per document, and secrets in prose
# =================================================================================
def document_commit_problems(work: Path | str, documents: dict[str, str]) -> list[str]:
    """Each document must first appear in a commit of its own. ``documents`` maps a label to a path.

    Counting commits is not enough: one commit with all three documents followed by two empty commits is not three
    commits. What counts is the first commit since the start that touches each file.
    """
    work = Path(work)
    first: dict[str, str] = {}
    problems: list[str] = []
    for label, rel in documents.items():
        if not (work / rel).is_file():
            problems.append(f"{label} does not exist yet")
            continue
        shas = gitutil.out(work, "log", "--reverse", "--format=%H", f"{gitutil.TAG_START}..HEAD", "--", rel, check=False).split()
        if shas:
            first[label] = shas[0]
        else:
            problems.append(f"{label} is not committed yet")
    by_commit: dict[str, list[str]] = {}
    for label, sha in first.items():
        by_commit.setdefault(sha, []).append(label)
    for labels in by_commit.values():
        if len(labels) > 1:
            problems.append(", ".join(labels[:-1]) + " and " + labels[-1] + " were first committed together")
    return problems


# a password-like name with a value that is not written inside quotes (the shared secret scan wants quotes)
_ASSIGNED_SECRET = re.compile(
    r"(?i)\b(?P<name>pass(?:word|wd)?|pwd|secret|api[_-]?key|access[_-]?key|private[_-]?key|client[_-]?secret)\b\s*[:=]\s*"
    r"[\"']?(?P<value>[^\s\"'<>`{}$]{8,})")
_SECRET_PLACEHOLDER = re.compile(r"(?i)change.?me|your[_-]|example|placeholder|dummy|fake|x{4,}|\*{3,}|redacted|os\.environ|getenv|\.\.\.")


def assigned_secret_files(work: Path | str) -> list[str]:
    """Files whose added text assigns a value to a password-like name (never the value itself)."""
    hits = []
    for rel, added in checks.added_text(work).items():
        for m in _ASSIGNED_SECRET.finditer(added):
            if not _SECRET_PLACEHOLDER.search(m.group("value")):
                hits.append(rel)
                break
    return hits
