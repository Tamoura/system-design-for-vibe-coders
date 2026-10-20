# labs/m03/trace.py
"""A JSONL trace: one JSON object per line, one line per event. Read one with: python labs/m03/trace.py FILE"""
import json
import sys
import time
import uuid


class TraceLog:
    """The events of one run, kept in memory and, with a path, appended to that file as they happen."""

    def __init__(self, path: str | None = None):
        self.path, self.run_id, self.events = path, uuid.uuid4().hex[:8], []

    def log(self, event: str, **fields) -> dict:
        fields = {k: v[:300] if isinstance(v, str) else v for k, v in fields.items()}     # clip: tool output can hold personal data
        rec = {"run": self.run_id, "seq": len(self.events) + 1, "ts": round(time.time(), 3), "event": event, **fields}
        self.events.append(rec)
        if self.path:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
        return rec


if __name__ == "__main__":
    for line in open(sys.argv[1], encoding="utf-8"):
        e = json.loads(line)
        print(e["run"], e["seq"], e["event"], {k: v for k, v in e.items() if k not in ("run", "seq", "ts", "event")})
