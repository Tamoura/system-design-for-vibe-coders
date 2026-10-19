"""The scripted "model" behind the offline mock server.

This is NOT a language model. It is a small set of transparent rules that behave like a
model in the ways the course labs need: it answers from the messages it is given (so it has
no memory of its own), it asks for tools when a tool looks relevant, it answers from documents
you put in the prompt, and it can be told to misbehave with `[mock:...]` directives so you can
practise handling loops, bad JSON, injected instructions and silent failures.
Real models behave differently: run the labs against the real API to see that.

Order of rules (first match wins):
  1. directives       [mock:loop] [mock:giveup] [mock:gullible] [mock:bad_json] [mock:thinking]
  2. playbook rules   JSON files you load with --playbook (see labkit/README.md)
  3. tool results     the last user turn carries tool_result blocks -> write the final answer
  4. structured out   output_config.format is a JSON schema -> JSON that fits the schema
  5. tool calls       a tool in `tools` looks relevant and its required inputs can be found
  6. documents        the prompt contains <document id="..."> blocks -> extractive answer + citation
  7. labels           the system prompt has a "Labels: a, b, c" line -> classify by keywords
  8. conversation     "what is my name", "what did I ask" -> answered only from the messages sent
  9. fallback         "(mock) I received: ..."
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from . import tokens

DATA = Path(__file__).parent / "data"
DIRECTIVE = re.compile(r"\[mock:([a-z_]+)\]")
STOP = {
    "a", "an", "the", "is", "are", "was", "of", "to", "in", "on", "for", "and", "or", "do", "does", "i", "my",
    "me", "what", "how", "can", "be", "it", "that", "this", "at", "by", "with", "much", "many", "when", "will",
    "you", "your", "get", "has", "have", "from", "yet", "its", "please", "tell", "about", "there", "who", "which",
}


def words(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-zA-Z]{3,}", text.lower()) if w not in STOP]


def clip(text: str, n: int) -> str:
    text = " ".join(text.split())
    return text if len(text) <= n else text[: n - 1] + "…"


@dataclass
class Ctx:
    model: str
    system: str
    messages: list[dict]          # content normalised to a list of blocks
    tools: list[dict]
    tool_choice: dict | None
    output_config: dict | None
    directives: set[str]
    last_user_text: str
    tool_results: list[dict] = field(default_factory=list)   # in the last user turn
    playbooks: list[dict] = field(default_factory=list)


@dataclass
class Reply:
    blocks: list[dict]
    stop_reason: str = "end_turn"


def normalise(messages: list[dict]) -> list[dict]:
    out = []
    for m in messages:
        c = m["content"]
        blocks = [{"type": "text", "text": c}] if isinstance(c, str) else list(c)
        out.append({"role": m["role"], "content": blocks})
    return out


def build_ctx(req: dict, playbooks: list[dict]) -> Ctx:
    msgs = normalise(req["messages"])
    system = tokens.system_text(req.get("system"))
    texts = [system] + [tokens.content_text(m["content"]) for m in msgs if m["role"] == "user"]
    directives = set(DIRECTIVE.findall(" ".join(texts)))
    last = msgs[-1]
    last_user_text = " ".join(b.get("text", "") for b in last["content"] if b.get("type") == "text") if last["role"] == "user" else ""
    results = [b for b in last["content"] if b.get("type") == "tool_result"] if last["role"] == "user" else []
    return Ctx(req["model"], system, msgs, req.get("tools") or [], req.get("tool_choice"), req.get("output_config"),
               directives, DIRECTIVE.sub("", last_user_text).strip(), results, playbooks)


def tool_id(name: str, inp: dict, turn: int) -> str:
    h = hashlib.sha1(f"{name}{json.dumps(inp, sort_keys=True)}{turn}".encode()).hexdigest()[:16]
    return f"toolu_mock_{h}"


def tool_block(ctx: Ctx, name: str, inp: dict) -> dict:
    return {"type": "tool_use", "id": tool_id(name, inp, len(ctx.messages)), "name": name, "input": inp}


def text_block(text: str) -> dict:
    return {"type": "text", "text": text}


# ------------------------------------------------------------------ playbooks

def matches(when: dict, ctx: Ctx) -> re.Match | bool:
    m: re.Match | bool = True
    if "system_contains" in when and when["system_contains"].lower() not in ctx.system.lower():
        return False
    if "user_contains" in when and when["user_contains"].lower() not in ctx.last_user_text.lower():
        return False
    if "user_regex" in when:
        m = re.search(when["user_regex"], ctx.last_user_text, re.I | re.S)
        if not m:
            return False
    if "has_tool_result" in when and bool(ctx.tool_results) != when["has_tool_result"]:
        return False
    if "tool_result_contains" in when and not any(when["tool_result_contains"].lower() in tokens.block_text(r).lower() for r in ctx.tool_results):
        return False
    if "tools_include" in when and when["tools_include"] not in {t["name"] for t in ctx.tools}:
        return False
    if "model_contains" in when and when["model_contains"] not in ctx.model:
        return False
    if "turn" in when and sum(1 for x in ctx.messages if x["role"] == "assistant") != when["turn"]:
        return False
    return m


def fill(template, ctx: Ctx, m) -> object:
    """Substitute {user}, {system}, {tool_results}, {1} (regex group) in strings, recursively."""
    if isinstance(template, str):
        subs = {"user": ctx.last_user_text, "system": ctx.system,
                "tool_results": "; ".join(tokens.block_text(r) for r in ctx.tool_results)}
        for k, v in subs.items():
            template = template.replace("{" + k + "}", v)
        if isinstance(m, re.Match):
            for i, g in enumerate(m.groups(), 1):
                template = template.replace("{" + str(i) + "}", g or "")
        return template
    if isinstance(template, list):
        return [fill(x, ctx, m) for x in template]
    if isinstance(template, dict):
        return {k: fill(v, ctx, m) for k, v in template.items()}
    return template


def from_playbook(ctx: Ctx) -> Reply | None:
    for pb in ctx.playbooks:
        for rule in pb.get("rules", []):
            m = matches(rule.get("when", {}), ctx)
            if not m:
                continue
            r = fill(rule["reply"], ctx, m)
            if "tool_use" in r:
                blocks = [tool_block(ctx, t["name"], t.get("input", {})) for t in r["tool_use"]]
                if r.get("text"):
                    blocks.insert(0, text_block(r["text"]))
                return Reply(blocks, "tool_use")
            if "json" in r:
                return Reply([text_block(json.dumps(r["json"], ensure_ascii=False))])
            return Reply([text_block(r.get("text", ""))] if r.get("text", "") != "" else [])
    return None


# ------------------------------------------------------------------ tools

EXPR = re.compile(r"(?<![\w.])(\(?-?\d+(?:\.\d+)?\)?(?:\s*[-+*/x×÷^]\s*\(?-?\d+(?:\.\d+)?\)?)+)")


def _numbers(text: str) -> list[str]:
    return re.findall(r"(?<![\w.])\d{2,8}(?![\w.])", text)


def fill_params(tool: dict, text: str):
    """Return a list of input dicts (one per call) or None when a required value is missing."""
    schema = tool.get("input_schema", {})
    props = schema.get("properties", {})
    required = schema.get("required", list(props))
    values: dict = {}
    fan_out: list = []
    for name in props:
        spec = props[name]
        low = name.lower()
        typ = spec.get("type", "string")
        val = None
        if "enum" in spec:
            val = next((e for e in spec["enum"] if str(e).lower() in text.lower()), spec["enum"][0])
        elif typ in ("integer", "number"):
            nums = re.findall(r"-?\d+(?:\.\d+)?", text)
            val = (int(nums[0]) if typ == "integer" else float(nums[0])) if nums else None
        elif typ == "boolean":
            val = False
        elif typ == "string":
            if any(k in low for k in ("expression", "formula", "calculation")):
                m = EXPR.search(text)
                val = m.group(1).replace("×", "*").replace("x", "*").replace("÷", "/").replace("^", "**") if m else None
            elif any(k in low for k in ("id", "number", "ticket", "order", "code")):
                nums = _numbers(text)
                if len(nums) > 1 and len(required) <= 1:
                    fan_out = nums
                    val = nums[0]
                else:
                    val = nums[0] if nums else None
            elif any(k in low for k in ("city", "location", "place")):
                m = re.search(r"\b(?:in|for|at)\s+([A-Z][A-Za-z]+(?:\s[A-Z][A-Za-z]+)?)", text)
                val = m.group(1) if m else None
            elif any(k in low for k in ("email", "address")):
                m = re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", text)
                val = m.group(0) if m else None
            elif "name" in low:
                m = re.search(r"\b(?:is|about|for|named|called)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)", text)
                val = m.group(1) if m else None
            elif any(k in low for k in ("query", "question", "text", "search", "message", "prompt", "input", "q", "topic")):
                val = text
        if val is not None:
            values[name] = val
        elif name in required:
            return None
    if fan_out:
        key = next(n for n in props if any(k in n.lower() for k in ("id", "number", "ticket", "order", "code")))
        return [{**values, key: n} for n in fan_out]
    return [values]


def relevant(tool: dict, text: str) -> bool:
    tw = set(words(text))
    name_words = {w for w in re.split(r"[_\-]", tool["name"].lower()) if len(w) >= 3} - {"get", "set", "run", "the"}
    desc_words = set(words(tool.get("description", "")))
    if tw & name_words:
        return True
    if len(tw & desc_words) >= 2:
        return True
    props = " ".join(tool.get("input_schema", {}).get("properties", {}))
    return bool(EXPR.search(text)) and any(k in props.lower() for k in ("expression", "formula", "calculation"))


def tool_calls(ctx: Ctx) -> Reply | None:
    if not ctx.tools or (ctx.tool_choice or {}).get("type") == "none":
        return None
    text = ctx.last_user_text
    blocks: list[dict] = []
    for tool in ctx.tools:
        if not relevant(tool, text):
            continue
        calls = fill_params(tool, text)
        if calls is None:
            return Reply([text_block(f"I can use the `{tool['name']}` tool for that, but I need more detail first. Which "
                                     f"{', '.join(tool.get('input_schema', {}).get('required', ['value']))} do you mean?")])
        blocks += [tool_block(ctx, tool["name"], c) for c in calls]
    if blocks:
        return Reply(blocks, "tool_use")
    return None


def after_tools(ctx: Ctx) -> Reply:
    errors = [r for r in ctx.tool_results if r.get("is_error")]
    results = [tokens.block_text(r) for r in ctx.tool_results]
    if errors:
        return Reply([text_block("A tool returned an error, so I could not finish: " + "; ".join(tokens.block_text(r) for r in errors) + ".")])
    return Reply([text_block("Here is what I found: " + "; ".join(results) + ".")])


# ------------------------------------------------------------------ structured output

LABEL_KW = json.loads((DATA / "label_keywords.json").read_text(encoding="utf-8"))


def score_labels(text: str, labels: list[str]) -> str:
    low = text.lower()
    best, best_n = None, 0
    for lab in labels:
        n = sum(1 for kw in LABEL_KW.get(lab, []) if kw in low)
        if n > best_n:
            best, best_n = lab, n
    if best:
        return best
    return "other" if "other" in labels else labels[0]


def json_from_schema(schema: dict, text: str, bad: bool = False):
    typ = schema.get("type", "object")
    if "anyOf" in schema:
        return json_from_schema(schema["anyOf"][0], text, bad)
    if typ == "object":
        props = schema.get("properties", {})
        out = {}
        for i, (k, spec) in enumerate(props.items()):
            if bad and i == 0 and k in schema.get("required", []):
                continue          # the bug: a required field is missing
            out[k] = json_from_schema(spec, text, bad)
        if bad and props:
            first_int = next((k for k, s in props.items() if s.get("type") in ("integer", "number")), None)
            if first_int:
                out[first_int] = "not-a-number"   # the bug: wrong type
        return out
    if "enum" in schema:
        return score_labels(text, [str(e) for e in schema["enum"]]) if all(isinstance(e, str) for e in schema["enum"]) else schema["enum"][0]
    if typ == "string":
        return clip(text, 60)
    if typ == "integer":
        n = re.findall(r"-?\d+", text)
        return int(n[0]) if n else 0
    if typ == "number":
        n = re.findall(r"-?\d+(?:\.\d+)?", text)
        return float(n[0]) if n else 0.0
    if typ == "boolean":
        return False
    if typ == "array":
        return []
    return None


def structured(ctx: Ctx) -> Reply | None:
    fmt = (ctx.output_config or {}).get("format")
    if not fmt or fmt.get("type") != "json_schema":
        return None
    bad = "bad_json" in ctx.directives and not any(m["role"] == "assistant" for m in ctx.messages)
    return Reply([text_block(json.dumps(json_from_schema(fmt["schema"], ctx.last_user_text, bad), ensure_ascii=False))])


# ------------------------------------------------------------------ documents, labels, conversation

DOC = re.compile(r"<document[^>]*?(?:id|name)=\"([^\"]+)\"[^>]*>(.*?)</document>", re.S)


def documents(ctx: Ctx) -> Reply | None:
    blob = ctx.system + "\n" + "\n".join(tokens.content_text(m["content"]) for m in ctx.messages if m["role"] == "user")
    docs = DOC.findall(blob)
    if not docs:
        return None
    question = DOC.sub("", ctx.last_user_text).strip()
    q = set(words(question))
    best, best_n, best_id = "", 0, ""
    for doc_id, body in docs:
        for s in re.split(r"(?<=[.!?])\s+|\n+", body.strip()):
            n = len(q & set(words(s)))
            if n > best_n or (n == best_n and n and len(s) < len(best)):
                best, best_n, best_id = s.strip(), n, doc_id
    if best_n == 0:
        return Reply([text_block("I don't know based on the provided documents.")])
    return Reply([text_block(f"{best} [{best_id}]")])


def labels(ctx: Ctx) -> Reply | None:
    m = re.search(r"labels?\s*:\s*([^\n]+)", ctx.system, re.I)
    if not m:
        return None
    labs = [x.strip(" .`\"'") for x in re.split(r"[,|/]", m.group(1)) if x.strip(" .`\"'")]
    text = ctx.last_user_text
    ex = re.findall(r"example\s*:\s*[\"“]?(.+?)[\"”]?\s*(?:=>|->)\s*([\w-]+)", ctx.system, re.I)
    label = None
    for ex_text, ex_label in ex:
        if len(set(words(ex_text)) & set(words(text))) >= 3 and ex_label in labs:
            label = ex_label
    label = label or score_labels(text, labs)
    strict = re.search(r"\b(only|exactly|just the label|nothing else)\b", ctx.system, re.I)
    if strict:
        return Reply([text_block(label)])
    return Reply([text_block(f"Thanks for the ticket! I think this is most likely a {label} issue, although it could "
                             f"also touch on other areas. Let me know if you would like more detail.")])


def conversation(ctx: Ctx) -> Reply | None:
    low = ctx.last_user_text.lower()
    prev_user = [tokens.content_text(m["content"]) for m in ctx.messages[:-1] if m["role"] == "user"]
    if re.search(r"what('s| is) my name|who am i", low):
        for t in reversed(prev_user + [ctx.last_user_text]):
            m = re.search(r"my name is ([A-Z][\w-]+)", t, re.I)
            if m:
                return Reply([text_block(f"Your name is {m.group(1)}.")])
        return Reply([text_block("I don't know your name. It has not come up in this conversation.")])
    if re.search(r"what did i (just )?(ask|say)|my (last|previous) question", low):
        if prev_user:
            return Reply([text_block(f"You asked: \"{clip(prev_user[-1], 120)}\"")])
        return Reply([text_block("This is the first message I can see in this conversation.")])
    return None


def fallback(ctx: Ctx) -> Reply:
    if not ctx.last_user_text:
        return Reply([text_block("(mock) Nothing to answer.")])
    return Reply([text_block(f"(mock) I received: {clip(ctx.last_user_text, 120)}")])


# ------------------------------------------------------------------ directives

def from_directives(ctx: Ctx) -> Reply | None:
    d = ctx.directives
    if "gullible" in d:
        blob = " ".join([ctx.system] + [tokens.content_text(m["content"]) for m in ctx.messages])
        m = re.search(r"ignore (?:all )?(?:your )?previous instructions.{0,200}?(?:call|use|run)\s+`?(\w+)`?(?:\s+with\s+([^\n]+))?", blob, re.I | re.S)
        if m and m.group(1) in {t["name"] for t in ctx.tools}:
            args = {k: v.rstrip(".") for k, v in re.findall(r"(\w+)\s*=\s*['\"]?([^\s,'\"]+)['\"]?", m.group(2) or "")}
            if not any(b.get("type") == "tool_use" and b["name"] == m.group(1) for msg in ctx.messages for b in msg["content"]):
                return Reply([tool_block(ctx, m.group(1), args)], "tool_use")
    if "loop" in d and ctx.tools:
        prev = next((b for m in reversed(ctx.messages) for b in m["content"] if b.get("type") == "tool_use"), None)
        if prev:   # the stuck agent asks for exactly the same thing again
            return Reply([tool_block(ctx, prev["name"], prev["input"])], "tool_use")
        tool = ctx.tools[0]
        calls = fill_params(tool, ctx.last_user_text) or [{}]
        return Reply([tool_block(ctx, tool["name"], calls[0])], "tool_use")
    if "giveup" in d and ctx.tool_results:
        return Reply([], "end_turn")
    return None


def respond(ctx: Ctx) -> Reply:
    reply = (from_directives(ctx) or from_playbook(ctx) or (after_tools(ctx) if ctx.tool_results else None)
             or structured(ctx) or tool_calls(ctx) or documents(ctx) or labels(ctx) or conversation(ctx) or fallback(ctx))
    if "thinking" in ctx.directives:
        reply.blocks.insert(0, {"type": "thinking", "thinking": "", "signature": "mock-signature"})
    return reply
