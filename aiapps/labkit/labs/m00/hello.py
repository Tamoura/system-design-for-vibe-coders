# labs/m00/hello.py
"""Smoke test: which mode are you in, and does one real SDK call work?
Offline: start the mock, then  export ANTHROPIC_BASE_URL=http://127.0.0.1:8787 ANTHROPIC_API_KEY=mock
Real: unset ANTHROPIC_BASE_URL and keep your key in .env. The code is the same; only the environment differs.
Exit codes: 0 worked, 1 the API call failed, 2 configuration problem."""
import os
import sys
from urllib.parse import urlparse

import anthropic
from anthropic import Anthropic
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True))          # nearest .env, here or in a parent folder; exported variables win over the file
MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")   # never hard-code a model id in lab code


def detect_mode(base_url, api_key):
    """Return (mode, hint). A pure function, so a test can call it with no network."""
    if not api_key:
        return "NO KEY", "set ANTHROPIC_API_KEY (offline: mock; real: your key in .env)"
    host = urlparse(base_url).hostname if base_url else None
    if host in ("127.0.0.1", "localhost", "::1"):
        return "MOCK (offline)", "free and scripted: good for mechanics, useless for judging answer quality"
    if host in (None, "api.anthropic.com"):
        if api_key == "mock":
            return "MISCONFIGURED", "the dummy key would get a 401 from the real API: set ANTHROPIC_BASE_URL or a real key"
        return "REAL API (billable)", "every call costs money: is your spending cap set?"
    return "CUSTOM ENDPOINT", f"the gateway at {host} sees your key and prompts: trust whoever runs it"


def main() -> int:
    base_url, key = os.environ.get("ANTHROPIC_BASE_URL"), os.environ.get("ANTHROPIC_API_KEY")
    mode, hint = detect_mode(base_url, key)
    print(f"mode     : {mode}  ({hint})")
    print(f"endpoint : {base_url or 'https://api.anthropic.com (SDK default)'}   model: {MODEL}")
    print(f"key      : {f'set, {len(key)} characters, never printed' if key else 'NOT SET'}")
    if mode in ("NO KEY", "MISCONFIGURED"):
        return 2
    try:
        resp = Anthropic(max_retries=0).messages.create(      # max_retries=0: fail fast while you set up
            model=MODEL,
            max_tokens=1024,                                  # required; thinking tokens count as output
            messages=[{"role": "user", "content": "Reply with one short sentence confirming you can hear me."}],
        )
    except anthropic.APIConnectionError:                      # no HTTP response at all
        print("FAILED   : cannot connect. Is the mock running on that port? Behind a proxy? See the table.")
        return 1
    except anthropic.APIStatusError as e:                     # an HTTP error: 400, 401, 404, 429, 5xx ...
        print(f"FAILED   : {type(e).__name__} (HTTP {e.status_code}): {e.message}")
        return 1
    text = next((b.text for b in resp.content if b.type == "text"), "")      # never resp.content[0].text
    u = resp.usage
    print(f"reply    : {text}")
    print(f"stop     : {resp.stop_reason}   request id: {resp._request_id}")
    print(f"tokens   : in={u.input_tokens} out={u.output_tokens}")
    p_in, p_out = os.environ.get("PRICE_IN_PER_MTOK"), os.environ.get("PRICE_OUT_PER_MTOK")
    if p_in and p_out:
        print(f"cost     : {(u.input_tokens * float(p_in) + u.output_tokens * float(p_out)) / 1_000_000:.6f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
