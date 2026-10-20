# labs/m09/memory.py
"""Lab 9.2: one user's long-term memory in SQLite. A Memory is bound to ONE user id from the login session."""
import re
import sqlite3
import sys
import time
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parents[2])]            # the lab kit, for its toy embedding
from labkit.embeddings import embed                                   # noqa: E402  use a real embedding model in production

KINDS = {"preference", "ticket_context"}                              # the only purposes we keep a memory for
SECRET = re.compile(r"(?i)\b(?:password|pin|otp|secret|token|api[ _-]?key)\b\s*(?:is|=|:)\s*\S+|\bsk-\w{10,}|\b(?:\d[ -]?){13,19}\b")
ORDER = re.compile(r"(?i)ignore (?:\w+ )?(?:previous|prior)|system note|always trust|pre-?approved")
SCHEMA = """
CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY, user_id TEXT, kind TEXT, text TEXT, created REAL);
CREATE TABLE IF NOT EXISTS turns (id INTEGER PRIMARY KEY, user_id TEXT, user_text TEXT, reply TEXT, created REAL);
CREATE TABLE IF NOT EXISTS summaries (user_id TEXT PRIMARY KEY, text TEXT, upto INTEGER);"""


class Memory:
    def __init__(self, path, user_id: str, clock=time.time):
        self.db, self.user, self.clock = sqlite3.connect(path, isolation_level=None), user_id, clock
        self.db.execute("PRAGMA secure_delete = ON")                  # deleted bytes are zeroed, not merely unlinked
        self.db.executescript(SCHEMA)

    def rows(self, table: str) -> list[dict]:                         # our table names; values are parameters
        cur = self.db.execute(f"SELECT * FROM {table} WHERE user_id = ? ORDER BY id", (self.user,))
        return [dict(zip([c[0] for c in cur.description], row)) for row in cur]

    def remember(self, text: str, kind: str = "preference") -> int:
        """The write policy: a speed bump, not a wall."""
        if kind not in KINDS or len(text) > 300 or SECRET.search(text) or ORDER.search(text):
            raise ValueError(f"not stored: kind must be one of {sorted(KINDS)}; one short fact; no secrets, no instructions")
        cur = self.db.execute("INSERT INTO memories (user_id, kind, text, created) VALUES (?,?,?,?)", (self.user, kind, text.strip(), self.clock()))
        return cur.lastrowid

    def recall(self, query: str = "", k: int = 3) -> list[dict]:
        """Relevance GATES (no match, never returned); recency only re-ranks what passed."""
        q, found = (embed(query) if query.strip() else None), []
        for row in self.rows("memories"):
            relevance = sum(a * b for a, b in zip(q, embed(row["text"]))) if q else 1.0       # no query: browse
            if relevance >= 0.15:
                recency = 0.5 ** ((self.clock() - row["created"]) / 86400 / 30)               # halves every 30 days
                found.append({**row, "score": relevance + 0.25 * recency})
        return sorted(found, key=lambda r: -r["score"])[:k]

    def log_turn(self, user_text: str, reply: str) -> int:
        """Secrets are redacted on the way in: the log feeds the summaries."""
        clean = [SECRET.sub("[removed]", t) for t in (user_text, reply)]
        return self.db.execute("INSERT INTO turns (user_id, user_text, reply, created) VALUES (?,?,?,?)", (self.user, *clean, self.clock())).lastrowid

    def summary(self) -> tuple[str, int]:
        return self.db.execute("SELECT text, upto FROM summaries WHERE user_id = ?", (self.user,)).fetchone() or ("", 0)

    def set_summary(self, text: str, upto: int) -> None:
        self.db.execute("INSERT OR REPLACE INTO summaries VALUES (?,?,?)", (self.user, text, upto))

    def unsummarised(self, keep: int = 0) -> list[dict]:
        """Logged turns the summary has not absorbed, except the newest `keep` (sent word for word)."""
        todo = [t for t in self.rows("turns") if t["id"] > self.summary()[1]]
        return todo[: max(0, len(todo) - keep)]

    def forget(self, what: str) -> dict:
        """A real delete, this user only: memories and turns containing the phrase, and the summary that may hold them.
        Derived data is dropped, not edited."""
        term = what.strip().lower()
        if not term:
            raise ValueError("say what to forget: a word or phrase from the memory")
        delete = lambda table, text: self.db.execute(f"DELETE FROM {table} WHERE user_id = ? AND instr(lower({text}), ?) > 0", (self.user, term)).rowcount
        gone = {"term": term, "memories": delete("memories", "text"), "turns": delete("turns", "user_text || ' ' || reply")}
        gone["summary_dropped"] = bool(gone["turns"] or term in self.summary()[0].lower())
        if gone["summary_dropped"]:
            self.db.execute("DELETE FROM summaries WHERE user_id = ?", (self.user,))
        return gone

    def export(self) -> dict:
        return {"user": self.user, "memories": self.rows("memories"), "turns": self.rows("turns"), "summary": self.summary()[0]}
