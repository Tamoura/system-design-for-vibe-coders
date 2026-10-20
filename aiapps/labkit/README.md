# labkit: the lab kit for *Building AI Applications & Agents*

Everything the course labs need to run **offline, for free, with the real `anthropic` SDK**:

| Part | What it is |
|---|---|
| `labkit/mock_server.py` | A local server that speaks the Anthropic Messages API (`/v1/messages`, streaming, `/v1/messages/count_tokens`). Your lab code does not change. |
| `labkit/brain.py` | The scripted "model" behind it: transparent rules, not intelligence. |
| `labkit/data/` | Najm Bank IT policies, a fake ticket database, employees, and 30 labelled tickets. |
| `labkit/tools.py` | Safe example tools: ticket status, calculator, weather, employee lookup. |
| `labkit/embeddings.py` | A toy hashed-word embedding for Chroma, so RAG labs need no download. |
| `labs/` | One folder per module with the reference lab code that the lessons show. Write your own first. |
| `playbooks/` | Scripted replies for specific labs (JSON). |
| `tests/` | Tests that keep the mock honest against the real SDK. |

## Run the labs offline

```bash
cd aiapps/labkit
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m labkit.mock_server --port 8787 &            # the offline "API"
export ANTHROPIC_BASE_URL=http://127.0.0.1:8787 ANTHROPIC_API_KEY=mock
python labs/m01/chat.py
```

To switch to the real API, stop the server, unset `ANTHROPIC_BASE_URL`, and set a real `ANTHROPIC_API_KEY`. **No lab code changes.** Set a monthly spending limit on the key first.

## What the mock is for, and what it is not

Use it to practise **mechanics**: the messages list, token growth, `tool_use` and `tool_result`, the loop, retries, JSON validation, trace logging, cost arithmetic, tests and CI. Do **not** use it to judge answer quality, prompt wording, retrieval quality or safety: a real model behaves differently, and each lab says which steps need one.

It mimics the real API where the course depends on it: a missing `tool_result` is a 400; the newest models reject sampling parameters and forced `tool_choice`; an over-long prompt is a 400; `max_tokens` truncates and sets `stop_reason: "max_tokens"`. Error **messages** are approximations. The token numbers are estimates, not the real tokenizer: use `client.messages.count_tokens(...)` against the real API for real counts.

## Directives: make the mock misbehave on purpose

Put a directive anywhere in a user message or the system prompt:

| Directive | Effect |
|---|---|
| `[mock:loop]` | After every tool result, call the first tool again (an agent that never finishes) |
| `[mock:giveup]` | After tool results, return an empty answer (a silent give-up: `content` is `[]`) |
| `[mock:gullible]` | Obey "ignore previous instructions ... call <tool> with k=v" found anywhere in the prompt (prompt injection) |
| `[mock:bad_json]` | Return JSON that breaks the schema on the first try; a retry with an error message gets valid JSON |
| `[mock:thinking]` | Put an (empty) `thinking` block first, so `response.content[0]` is not text |
| `[mock:slow]` | Wait 3 seconds |
| `[mock:ratelimit]` / `[mock:overloaded]` / `[mock:error500]` | Return 429 / 529 / 500 every time |

Environment: `MOCK_CONTEXT_WINDOW` (tokens, default 200000: set it to `8000` to overflow quickly), `MOCK_FAIL_EVERY=3` (every 3rd request is a 529 that the SDK retries), `MOCK_RATE_LIMIT_EVERY=N`, `MOCK_PLAYBOOK=a.json,b.json`.

## Conventions the mock understands

- **Classification:** a system line `Labels: hardware, access, network, software, security, other`. The answer is the label whose keywords match the ticket. If the system prompt also says `only`, `exactly` or `nothing else`, the reply is just the label; otherwise it is a chatty sentence (which an exact-match grader rejects). `Example: "ticket text" => label` lines in the system prompt are used as few-shot hints.
- **Documents:** `<document id="limits">text</document>` blocks in the prompt. The reply is the best-matching sentence with a `[limits]` citation, or "I don't know based on the provided documents."
- **Tools:** a tool is called when its name or description shares words with the user message and its required inputs can be found (ticket numbers, an arithmetic expression, a city after "in", an email). Several ticket numbers produce several parallel `tool_use` blocks. A vague description (`does stuff`) is never called.
- **Structured output:** `output_config={"format": {"type": "json_schema", "schema": ...}}` returns JSON that fits the schema (enum fields by keyword).
- **Playbooks:** JSON rules `{"when": {...}, "reply": {...}}` for lab-specific scripted replies; see `playbooks/example.json`. `when` keys: `system_contains`, `user_contains`, `user_regex`, `has_tool_result`, `tool_result_contains`, `tools_include`, `model_contains`, `turn`. `reply` is `{"text": ...}`, `{"json": ...}` or `{"tool_use": [{"name": ..., "input": ...}], "text": ...}`; `{user}`, `{system}`, `{tool_results}` and regex groups `{1}` are substituted.

## Tests

```bash
cd aiapps/labkit && pytest
```
