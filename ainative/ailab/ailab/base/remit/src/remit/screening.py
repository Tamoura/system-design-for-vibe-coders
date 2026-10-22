"""LEGACY: name screening against the sanctions watchlist.

Written in 2021 for the first version of Remit, ported unchanged when risk.py was
split up, and still doing its job. It has no tests of its own. Do not "tidy" it
without a ticket and a characterization test first: compliance owns its behaviour.

How it works
------------
1. ``tokens(name)`` normalises a name: strips accents and Arabic vowel marks, folds
   case, turns Arabic script into Latin letters, splits on anything that is not a
   letter or digit, and drops the particles ``al el bin ibn bint ben``.
2. ``match_score`` compares two token lists and returns 0-100.
3. ``screen`` scores a name against every watchlist entry and keeps the entries at or
   above ``THRESHOLD`` (100: every token of the shorter name must be matched).

Known quirks (documented, intentional or inherited; see KIT_NOTES.md)
----------------------------------------------------------------------
Q-SCR-1  Tokens of four characters or fewer must match exactly. Longer tokens match
         when they are at least 85% similar, so "Hasan" matches "Hassan" but "Omar"
         does not match "Omer".
Q-SCR-2  A name with a single token never matches an entry with several tokens (and
         the other way round); only single-token names match single-token entries.
Q-SCR-3  Only the first four tokens of a name are compared (the old fixed-width file
         format had four name fields). A fifth token is ignored.
Q-SCR-4  Arabic words that are not in NAME_TABLE are transliterated letter by letter
         with no vowels ("حمزة" becomes "hmza"), so they only match entries written
         the same way. Characters that are neither Latin letters, digits nor Arabic
         letters are treated as separators, so a name in another script has no
         tokens and never matches anything.

TODO(farid, 2022): move the watchlist to the vendor feed and delete DEFAULT_WATCHLIST.
"""
from __future__ import annotations

import difflib
import re
import unicodedata
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

THRESHOLD = 100  # percent of the shorter name's tokens that must be matched
FUZZY_PERCENT = 85  # similarity needed between two long tokens
MIN_FUZZY_LEN = 5  # tokens shorter than this must match exactly (Q-SCR-1)
MAX_TOKENS = 4  # Q-SCR-3

PARTICLES = frozenset({"al", "el", "bin", "ibn", "bint", "ben"})

# Whole Arabic words (without article or vowel marks) -> the usual Latin spelling.
NAME_TABLE: dict[str, str] = {
    "محمد": "mohammed",
    "احمد": "ahmed",
    "علي": "ali",
    "عمر": "omar",
    "حسن": "hassan",
    "حسين": "hussein",
    "خالد": "khalid",
    "فاطمه": "fatima",
    "فاطمة": "fatima",
    "كريم": "karim",
    "ناصر": "nasser",
    "يوسف": "youssef",
    "ابراهيم": "ibrahim",
    "سعيد": "saeed",
    "قادري": "qadiri",
    "فارسي": "farsi",
    "بن": "bin",
    "بنت": "bint",
    "ابن": "ibn",
}

# Letter-by-letter fallback. Lossy on purpose: several Arabic letters share a Latin one.
LETTER_TABLE: dict[str, str] = {
    "ا": "a", "ب": "b", "ت": "t", "ث": "th", "ج": "j", "ح": "h", "خ": "kh",
    "د": "d", "ذ": "dh", "ر": "r", "ز": "z", "س": "s", "ش": "sh", "ص": "s",
    "ض": "d", "ط": "t", "ظ": "z", "ع": "a", "غ": "gh", "ف": "f", "ق": "q",
    "ك": "k", "ل": "l", "م": "m", "ن": "n", "ه": "h", "ة": "a", "و": "w",
    "ي": "y", "ى": "a", "ء": "",
}  # fmt: skip

# Fictional names, for demos and tests only.
DEFAULT_WATCHLIST: tuple[str, ...] = (
    "Karim Nasser Al-Qadiri",
    "Vorlon Trading FZE",
    "Samir Haddad Younis",
    "Elena Markovic Petrov",
    "Test Sanctioned Person",
)

_SPLIT = re.compile(r"[^0-9a-zء-ي]+")


@dataclass(frozen=True)
class Match:
    name: str  # the name that was screened
    entry: str  # the watchlist entry it matched
    score: int  # 0-100


@dataclass(frozen=True)
class ScreenResult:
    hit: bool
    matches: tuple[Match, ...]


def _strip_marks(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def _arabic_word(word: str) -> str:
    if word.startswith("ال") and len(word) > 3:  # drop the definite article
        word = word[2:]
    if word in NAME_TABLE:
        return NAME_TABLE[word]
    return "".join(LETTER_TABLE.get(ch, ch) for ch in word)


def tokens(name: str) -> list[str]:
    """Normalise ``name`` into at most MAX_TOKENS lower-case Latin tokens."""
    text = _strip_marks(name).casefold().replace("ـ", "")  # tatweel
    out: list[str] = []
    for word in _SPLIT.split(text):
        if not word:
            continue
        if "ء" <= word[0] <= "ي":
            word = _arabic_word(word)
        if word and word not in PARTICLES:
            out.append(word)
    return out[:MAX_TOKENS]


def _similar(a: str, b: str) -> bool:
    if a == b:
        return True
    if len(a) < MIN_FUZZY_LEN or len(b) < MIN_FUZZY_LEN:
        return False
    blocks = difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks()
    same = sum(block.size for block in blocks)
    return 200 * same >= FUZZY_PERCENT * (len(a) + len(b))  # ratio >= 0.85, in integers


def match_score(a: Sequence[str], b: Sequence[str]) -> int:
    """0-100: the share of the shorter token list that is matched in the longer one."""
    if not a or not b:
        return 0
    shorter, longer = (a, b) if len(a) <= len(b) else (b, a)
    if len(shorter) == 1 and len(longer) > 1:  # Q-SCR-2
        return 0
    used: set[int] = set()
    matched = 0
    for token in shorter:
        for index, other in enumerate(longer):
            if index not in used and _similar(token, other):
                used.add(index)
                matched += 1
                break
    return 100 * matched // len(shorter)


def screen(name: str, watchlist: Iterable[str], threshold: int = THRESHOLD) -> ScreenResult:
    """Screen one name. Matches are sorted by score (high first), then entry."""
    candidate = tokens(name)
    found: list[Match] = []
    for entry in watchlist:
        score = match_score(candidate, tokens(entry))
        if score and score >= threshold:
            found.append(Match(name=name, entry=entry, score=score))
    found.sort(key=lambda m: (-m.score, m.entry))
    return ScreenResult(hit=bool(found), matches=tuple(found))


def screen_names(names: Iterable[str], watchlist: Iterable[str]) -> ScreenResult:
    """Screen several names (sender and recipient) and merge the matches."""
    entries = list(watchlist)
    found: list[Match] = []
    for name in names:
        found.extend(screen(name, entries).matches)
    return ScreenResult(hit=bool(found), matches=tuple(found))


def load_watchlist(path: str) -> list[str]:
    """Read a watchlist file: one name per line, blank lines and ``#`` comments ignored."""
    with open(path, encoding="utf-8") as handle:
        lines = [line.strip() for line in handle]
    return [line for line in lines if line and not line.startswith("#")]
