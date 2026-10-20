# labs/m14/smoke.py
"""Lab 14.1: the smoke test. Boot the service in-process (FastAPI's TestClient) and check the few things that must be true before a
release goes anywhere. Exit 0 = safe to continue.
  ANTHROPIC_BASE_URL=http://127.0.0.1:9014 ANTHROPIC_API_KEY=mock python labs/m14/smoke.py
Set SMOKE_URL=https://staging.example to run the same checks against a deployed service. TestClient needs the httpx2 package, which the anthropic package installs."""
import contextlib
import io
import os
import sys

import httpx2 as httpx             # anthropic 1.x is built on httpx2; the old httpx package may be absent
from fastapi.testclient import TestClient

import app as service


def main() -> int:
    url = os.environ.get("SMOKE_URL")
    service_log = io.StringIO()                     # the service logs JSON to stdout: keep it out of the verdict, show it only after a failure
    with contextlib.redirect_stdout(service_log):
        c = httpx.Client(base_url=url, timeout=30) if url else TestClient(service.create_app())
        q, key = {"question": "How many days a week can I work remotely?", "user": "smoke"}, {"Idempotency-Key": "smoke-1"}
        first, again, ready = c.post("/v1/ask", json=q, headers=key), c.post("/v1/ask", json=q, headers=key), c.get("/ready")
        prompts = ready.json().get("prompts", {})
        checks = {
            "liveness answers": c.get("/health").status_code == 200,
            "readiness answers": ready.status_code == 200,
            "readiness names the prompt versions": bool(prompts) and all("@" in v for v in prompts.values()),
            "an answer arrives with a citation": first.status_code == 200 and "[" in first.json()["answer"],
            "the same key replays and does not pay twice": again.json().get("replayed") is True and again.json()["answer"] == first.json()["answer"],
            "bad input is refused, not crashed": c.post("/v1/ask", json={"question": ""}).status_code == 422,
        }
    for name, passed in checks.items():
        print(("PASS  " if passed else "FAIL  ") + name)
    if not all(checks.values()):
        print(service_log.getvalue(), end="")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
