"""An offline, Anthropic-compatible mock of the Messages API, for the course labs.

Run it:      python -m labkit.mock_server --port 8787
Point at it: export ANTHROPIC_BASE_URL=http://127.0.0.1:8787  ANTHROPIC_API_KEY=mock

Your lab code does not change: the real `anthropic` SDK talks to this server exactly as it
would talk to the real API. The "model" behind it is a set of scripted rules (labkit/brain.py),
so use it to practise the MECHANICS: the messages list, tool_use and tool_result, the loop,
retries, token growth, JSON validation. Do not use it to judge answer quality.

Validation mimics the real API where the course depends on it (a missing tool_result is a 400,
newest models reject sampling parameters, an over-long prompt is a 400). Error texts are
approximations: read the real API's messages when you meet them.
Environment:  MOCK_CONTEXT_WINDOW (default 200000 tokens)  MOCK_FAIL_EVERY=N (every Nth request
returns 529 overloaded, which the SDK retries)  MOCK_RATE_LIMIT_EVERY=N (every Nth returns 429)
MOCK_PLAYBOOK=a.json,b.json (extra scripted replies, see labkit/README.md)."""
from __future__ import annotations

import argparse
import asyncio
import itertools
import json
import os
import re
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse

from . import brain, tokens

# Models that reject sampling parameters or forced tool choice (see the course, lesson 1.1 and 3.1).
NEWEST = ("claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5", "claude-opus-5", "claude-sonnet-5",
          "claude-fable-5", "claude-fable-5-1", "claude-mythos-5", "claude-mythos-5-1", "claude-opus-4-8", "claude-opus-4-7")
NO_FORCED_TOOLS = ("claude-opus-5-5", "claude-sonnet-5-5", "claude-fable-5-1", "claude-mythos-5-1")
SMALL_CONTEXT = ("claude-haiku-4-5",)

counter = itertools.count(1)


def err(status: int, kind: str, message: str, headers: dict | None = None) -> JSONResponse:
    return JSONResponse({"type": "error", "error": {"type": kind, "message": message}}, status_code=status,
                        headers={"request-id": "req_mock_" + uuid.uuid4().hex[:12], **(headers or {})})


def validate(body: dict) -> str | None:
    """Return an error message, or None when the request is acceptable."""
    for key in ("model", "max_tokens", "messages"):
        if key not in body:
            return f"{key}: Field required"
    if not isinstance(body["max_tokens"], int) or body["max_tokens"] < 1:
        return "max_tokens: must be a positive integer"
    msgs = body["messages"]
    if not isinstance(msgs, list) or not msgs:
        return "messages: at least one message is required"
    if msgs[0].get("role") != "user":
        return "messages: first message must use the \"user\" role"
    for i, m in enumerate(msgs):
        if m.get("role") not in ("user", "assistant"):
            return f"messages.{i}.role: Input should be 'user' or 'assistant'"
        if "content" not in m or m["content"] in ("", []):
            return f"messages.{i}: content must not be empty"
    model = body["model"]
    for p in ("temperature", "top_p", "top_k"):
        if p in body and model.startswith(NEWEST) and not (p == "temperature" and body[p] == 1 and "opus-4-7" not in model):
            return f"`{p}` is not supported for this model"
    tc = (body.get("tool_choice") or {}).get("type")
    if tc in ("any", "tool") and model.startswith(NO_FORCED_TOOLS):
        return "tool_choice: type \"tool\" and \"any\" are not supported for this model."
    for i, t in enumerate(body.get("tools") or []):
        if "name" not in t or not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", t["name"]):
            return f"tools.{i}.name: String should match pattern '^[a-zA-Z0-9_-]{{1,64}}$'"
        if t.get("input_schema", {}).get("type") != "object":
            return f"tools.{i}.input_schema: type must be \"object\""
    # tool_use / tool_result pairing
    norm = brain.normalise(msgs)
    for i, m in enumerate(norm):
        uses = [b["id"] for b in m["content"] if b.get("type") == "tool_use"] if m["role"] == "assistant" else []
        if uses:
            nxt = norm[i + 1] if i + 1 < len(norm) else None
            have = {b.get("tool_use_id") for b in nxt["content"] if b.get("type") == "tool_result"} if nxt and nxt["role"] == "user" else set()
            missing = [u for u in uses if u not in have]
            if missing and nxt is not None:
                return (f"messages.{i + 1}: `tool_use` ids were found without `tool_result` blocks immediately after: "
                        f"{', '.join(missing)}. Each `tool_use` block must have a corresponding `tool_result` block in the next message.")
            if nxt is None:
                continue
        if m["role"] == "user":
            res = [b.get("tool_use_id") for b in m["content"] if b.get("type") == "tool_result"]
            prev_uses = {b["id"] for b in norm[i - 1]["content"] if b.get("type") == "tool_use"} if i and norm[i - 1]["role"] == "assistant" else set()
            bad = [r for r in res if r not in prev_uses]
            if bad:
                return (f"messages.{i}.content: unexpected `tool_use_id` found in `tool_result` blocks: {', '.join(bad)}. "
                        "Each `tool_result` block must have a corresponding `tool_use` block in the previous message.")
    return None


def make_message(body: dict, playbooks: list[dict]) -> dict:
    ctx = brain.build_ctx(body, playbooks)
    reply = brain.respond(ctx)
    blocks, stop = reply.blocks, reply.stop_reason
    max_tokens = body["max_tokens"]
    out_tokens = sum(tokens.estimate(tokens.block_text(b)) for b in blocks)
    if out_tokens > max_tokens:
        for b in blocks:
            if b["type"] == "text":
                b["text"] = b["text"][: max(1, max_tokens * 4)]
        blocks = [b for b in blocks if b["type"] != "tool_use"]
        stop = "max_tokens"
        out_tokens = max_tokens
    in_tokens = tokens.estimate_request(body.get("system"), body["messages"], body.get("tools"))
    return {"id": "msg_mock_" + uuid.uuid4().hex[:20], "type": "message", "role": "assistant", "model": body["model"],
            "content": blocks, "stop_reason": stop, "stop_sequence": None,
            "usage": {"input_tokens": in_tokens, "output_tokens": out_tokens, "cache_creation_input_tokens": 0,
                      "cache_read_input_tokens": 0}}


def sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


def stream_events(msg: dict):
    start = {**msg, "content": [], "stop_reason": None, "usage": {**msg["usage"], "output_tokens": 1}}
    yield sse("message_start", {"type": "message_start", "message": start})
    for i, b in enumerate(msg["content"]):
        if b["type"] == "text":
            yield sse("content_block_start", {"type": "content_block_start", "index": i, "content_block": {"type": "text", "text": ""}})
            chunks = re.findall(r"\S+\s*", b["text"]) or [""]
            for c in chunks:
                yield sse("content_block_delta", {"type": "content_block_delta", "index": i, "delta": {"type": "text_delta", "text": c}})
        elif b["type"] == "tool_use":
            yield sse("content_block_start", {"type": "content_block_start", "index": i,
                                              "content_block": {"type": "tool_use", "id": b["id"], "name": b["name"], "input": {}}})
            yield sse("content_block_delta", {"type": "content_block_delta", "index": i,
                                              "delta": {"type": "input_json_delta", "partial_json": json.dumps(b["input"], ensure_ascii=False)}})
        else:  # thinking
            yield sse("content_block_start", {"type": "content_block_start", "index": i,
                                              "content_block": {"type": "thinking", "thinking": "", "signature": ""}})
            yield sse("content_block_delta", {"type": "content_block_delta", "index": i,
                                              "delta": {"type": "signature_delta", "signature": b.get("signature", "")}})
        yield sse("content_block_stop", {"type": "content_block_stop", "index": i})
    yield sse("message_delta", {"type": "message_delta", "delta": {"stop_reason": msg["stop_reason"], "stop_sequence": None},
                                "usage": {"output_tokens": msg["usage"]["output_tokens"]}})
    yield sse("message_stop", {"type": "message_stop"})


def load_playbooks(spec: str | None) -> list[dict]:
    out = []
    for p in (spec or "").split(","):
        if p.strip():
            out.append(json.loads(Path(p.strip()).read_text(encoding="utf-8")))
    return out


def create_app(playbook_spec: str | None = None) -> FastAPI:
    app = FastAPI(title="Course mock of the Anthropic Messages API")
    playbooks = load_playbooks(playbook_spec if playbook_spec is not None else os.environ.get("MOCK_PLAYBOOK"))
    window = int(os.environ.get("MOCK_CONTEXT_WINDOW", "200000"))

    def injected_failure() -> JSONResponse | None:
        n = next(counter)
        every_fail, every_rl = int(os.environ.get("MOCK_FAIL_EVERY", "0")), int(os.environ.get("MOCK_RATE_LIMIT_EVERY", "0"))
        if every_rl and n % every_rl == 0:
            return err(429, "rate_limit_error", "Number of request tokens has exceeded your rate limit (mock).", {"retry-after": "1"})
        if every_fail and n % every_fail == 0:
            return err(529, "overloaded_error", "Overloaded (mock).")
        return None

    async def parse(request: Request):
        if "x-api-key" not in request.headers and "authorization" not in request.headers:
            return None, err(401, "authentication_error", "x-api-key header is required")
        try:
            return await request.json(), None
        except Exception:
            return None, err(400, "invalid_request_error", "Request body must be valid JSON")

    @app.get("/health")
    async def health():
        return {"status": "ok", "mock": True}

    @app.post("/v1/messages/count_tokens")
    async def count(request: Request):
        body, e = await parse(request)
        if e:
            return e
        if "model" not in body or not body.get("messages"):
            return err(400, "invalid_request_error", "model and messages are required")
        return {"input_tokens": tokens.estimate_request(body.get("system"), body["messages"], body.get("tools"))}

    @app.post("/v1/messages")
    async def messages(request: Request):
        body, e = await parse(request)
        if e:
            return e
        d = set(brain.DIRECTIVE.findall(json.dumps(body, ensure_ascii=False)))
        if "ratelimit" in d:
            return err(429, "rate_limit_error", "Rate limited (mock directive).", {"retry-after": "1"})
        if "overloaded" in d:
            return err(529, "overloaded_error", "Overloaded (mock directive).")
        if "error500" in d:
            return err(500, "api_error", "Internal server error (mock directive).")
        fail = injected_failure()
        if fail:
            return fail
        msg_error = validate(body)
        if msg_error:
            return err(400, "invalid_request_error", msg_error)
        limit = 200000 if body["model"].startswith(SMALL_CONTEXT) else window
        n_in = tokens.estimate_request(body.get("system"), body["messages"], body.get("tools"))
        if n_in > limit:
            return err(400, "invalid_request_error", f"prompt is too long: {n_in} tokens > {limit} maximum")
        if "slow" in d:
            await asyncio.sleep(3)
        msg = make_message(body, playbooks)
        if body.get("stream"):
            return StreamingResponse(stream_events(msg), media_type="text/event-stream", headers={"request-id": "req_mock_stream"})
        return JSONResponse(msg, headers={"request-id": "req_mock_" + uuid.uuid4().hex[:12]})

    return app


app = create_app()


def main() -> None:
    import uvicorn
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--playbook", default=None, help="comma-separated playbook JSON files")
    a = ap.parse_args()
    uvicorn.run(create_app(a.playbook), host=a.host, port=a.port, log_level="warning")


if __name__ == "__main__":
    main()
