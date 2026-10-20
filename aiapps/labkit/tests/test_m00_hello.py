"""Module 0, lesson 0.2: the smoke script tells you which mode you are in, and works offline."""
import json
import os
import re
import socket
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest

from labs.m00.hello import detect_mode

HELLO = Path(__file__).resolve().parents[1] / "labs" / "m00" / "hello.py"


def run_hello(tmp_path, **env):
    """Run hello.py in a clean environment (no inherited ANTHROPIC_*, MODEL or PRICE_* variables)."""
    clean = {k: v for k, v in os.environ.items() if not k.startswith(("ANTHROPIC_", "PRICE_")) and k != "MODEL"}
    clean.update({"NO_PROXY": "127.0.0.1,localhost", "no_proxy": "127.0.0.1,localhost"})
    clean.update(env)
    return subprocess.run([sys.executable, str(HELLO)], cwd=tmp_path, env=clean, capture_output=True, text=True, timeout=60)


@pytest.mark.parametrize("base_url, key, mode", [
    (None, None, "NO KEY"),
    ("http://127.0.0.1:8787", None, "NO KEY"),
    ("http://127.0.0.1:8787", "mock", "MOCK (offline)"),
    ("http://localhost:9000", "mock", "MOCK (offline)"),
    (None, "mock", "MISCONFIGURED"),
    ("https://api.anthropic.com", "mock", "MISCONFIGURED"),
    (None, "a-real-looking-key", "REAL API (billable)"),
    ("https://api.anthropic.com", "a-real-looking-key", "REAL API (billable)"),
    ("https://gateway.example.com/v1", "a-real-looking-key", "CUSTOM ENDPOINT"),
])
def test_detect_mode(base_url, key, mode):
    assert detect_mode(base_url, key)[0] == mode


def test_offline_run_succeeds_and_reports_the_mode(server, tmp_path):
    secret = "mock-secret-value-123"
    r = run_hello(tmp_path, ANTHROPIC_BASE_URL=server, ANTHROPIC_API_KEY=secret)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "mode     : MOCK (offline)" in r.stdout
    assert "model: claude-sonnet-5-5" in r.stdout
    assert re.search(r"tokens   : in=\d+ out=\d+", r.stdout)
    assert "request id: req_mock_" in r.stdout
    assert secret not in r.stdout + r.stderr          # the key is never printed


def test_the_model_comes_from_the_environment(server, tmp_path):
    r = run_hello(tmp_path, ANTHROPIC_BASE_URL=server, ANTHROPIC_API_KEY="mock", MODEL="claude-haiku-5-5")
    assert "model: claude-haiku-5-5" in r.stdout and r.returncode == 0


def test_cost_line_is_arithmetic_on_usage_and_your_prices(server, tmp_path):
    r = run_hello(tmp_path, ANTHROPIC_BASE_URL=server, ANTHROPIC_API_KEY="mock", PRICE_IN_PER_MTOK="1", PRICE_OUT_PER_MTOK="5")
    t_in, t_out = map(int, re.search(r"tokens   : in=(\d+) out=(\d+)", r.stdout).groups())
    assert f"cost     : {(t_in * 1 + t_out * 5) / 1_000_000:.6f}" in r.stdout


def test_no_key_is_a_configuration_error(server, tmp_path):
    r = run_hello(tmp_path, ANTHROPIC_BASE_URL=server)
    assert r.returncode == 2 and "NOT SET" in r.stdout


def test_a_dead_port_is_a_connection_failure_with_a_hint(tmp_path):
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]                       # nothing listens here once the socket closes
    r = run_hello(tmp_path, ANTHROPIC_BASE_URL=f"http://127.0.0.1:{port}", ANTHROPIC_API_KEY="mock")
    assert r.returncode == 1 and "FAILED   : cannot connect" in r.stdout


def test_an_http_error_is_reported_with_its_typed_name_and_status(tmp_path):
    """The mock never answers 401, so a stub server plays the real API refusing a bad key."""
    class Refuse(BaseHTTPRequestHandler):
        def do_POST(self):
            body = json.dumps({"type": "error", "error": {"type": "authentication_error", "message": "invalid x-api-key"}}).encode()
            self.send_response(401)
            self.send_header("content-type", "application/json")
            self.send_header("content-length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    stub = HTTPServer(("127.0.0.1", 0), Refuse)
    threading.Thread(target=stub.serve_forever, daemon=True).start()
    try:
        r = run_hello(tmp_path, ANTHROPIC_BASE_URL=f"http://127.0.0.1:{stub.server_port}", ANTHROPIC_API_KEY="wrong-key")
    finally:
        stub.shutdown()
    assert r.returncode == 1
    assert "FAILED   : AuthenticationError (HTTP 401)" in r.stdout and "invalid x-api-key" in r.stdout
