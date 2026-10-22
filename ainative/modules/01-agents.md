# Module 1 — How coding agents work

*Lesson 1.1 gives you the mental model that lets you predict what an agent will do well and where it will fail: a model is a stateless function of its context, a coding agent is that model with tools in a loop, and what is not in the context does not exist for it. It explains why agents are brilliant at breadth, speed, pattern completion and mechanical work, names the ten ways they fail with a Najm Remit example of each, and ends with the Failure-mode field guide: symptom, cheapest detection and prevention for every mode. Lesson 1.2 is the lab. You read three constructed agent sessions on Remit, name the failure in each, find the turn where it went wrong and choose the cheapest prevention. All of it can be done without an agent; an optional part has you run a short read-only session of your own and write it up. Everything on the Najm side is fictional.*

> **Focus:** Mindset, Verify — a model of how agents work that predicts where they fail, and the habit of reading a session as evidence.

---

# 1.1 — The mental model: context, tools and the loop, and why agents are brilliant and why they fail
*Level: 🟢 Beginner* · *Prerequisites: 0.3* · *Focus: Mindset*

## ⚡ In 60 seconds
- A model is a **stateless function of its context**: what is not in the context does not exist for it.
- An agent is a model plus **tools** (read, search, edit, run) in a **loop**: each result goes back into the context.
- It is brilliant at breadth, speed, pattern completion and mechanical work, and fails in ten recognisable ways (the **Failure-mode field guide**).
- Four things predict success: **verifiability, locality, context, familiarity**.
- Decision cue: before you delegate, name the failure you expect and the cheapest way to see it.
- Biggest trap: reading fluent as correct. Fluency costs the model nothing.

## 🧭 Why it matters
On a Monday (a constructed day, not recorded from a real model) Lujain points her agent at `screening.py`, the old module with no tests. Six minutes later it has written eighteen well-named characterization tests, and she reads every one. On Tuesday, same agent, she asks for an audit event when a quote is created. It writes `audit.record("quote.created", ...)` and `ids.generate("QUO")`. Neither exists in najmkit, and no test calls the new helper, so the suite stays green.

Tariq opens the clinic with both stories: "Same tool. Why did it shine on the hard module and fall over on a one-line call?" The answer is a mental model, not luck.

## 📐 How it works

### 🟢 The essentials

**A model is a function of its context.** A language model reads a sequence of text pieces called **tokens** and produces the next ones. It keeps no state between calls: nothing about yesterday or your repository survives unless it is sent again. The program re-sends the conversation every turn, and that feels like memory. Hence the course's central rule: **what is not in the context does not exist for the model**. [*Building AI Applications & Agents*, lesson 1.1 — The one idea: a stateless function, tokens, the context window and the messages list](../aiapps/index.html#/1.1) teaches this from the API side.

**What fills the context window.** The window is the most text one call can hold. In Claude Code on Remit it fills from five places.

| Source | Example on Remit | Who controls it |
|---|---|---|
| **Instructions** | The tool's system prompt and tool definitions | The tool |
| **Memory files** | `CLAUDE.md`, the first lines of auto memory | You, plus the agent's own notes (Module 2) |
| **File contents** | `service.py`, once the agent has read it | The agent, guided by you |
| **Tool output** | `pytest` dots, a `grep` result, a stack trace | The commands it runs |
| **Conversation** | Your prompts, its replies, its plans | You and the agent |

A subagent has a window of its own, and only its final report comes back. `/context` shows what uses the window and which memory files loaded.

**Tokens and cost, qualitatively.** You pay for tokens read and written, and every turn reads the whole context again. A 4,000-line log pasted on turn three is read again on every later turn. Providers often discount repeated context, but it is not free and still competes for attention. `/usage` shows your usage (its session-cost block is meant for API users).

**The loop.** An agent adds hands: the same model, called in a loop, with tools to read, search, edit and run commands. The model asks for a tool, the program checks the permission rules, runs it, appends the result to the context and calls the model again. It stops when the model answers instead of asking. (This agent loop runs inside the *delegate* step of the AI-native loop of lesson 0.3, which stays yours.)

```mermaid
flowchart TD
    G["Your prompt and the context"] --> M["The model reads the context"]
    M --> D{"Tool call or answer?"}
    D -->|"tool call"| P{"Allowed?"}
    P -->|"no"| Q["It asks you or is refused"]
    Q --> M
    P -->|"yes"| T["Run it: read, search, edit, run"]
    T --> R["The result is appended to the context"]
    R --> M
    D -->|"answer"| H["You read the answer and the diff"]
    H -->|"next prompt"| G
```

The loop makes agents useful and risky: they can check their work by running tests, and be misled by what a tool returns, from a confusing error to a README with instructions in it. The loop's internals and the cost arithmetic are in [*Building AI Applications & Agents*, lesson 8.1 — Plan, act, observe, repeat: reflection, stopping conditions and the first failure modes](../aiapps/index.html#/8.1).

**Why they are brilliant.** Four strengths: **breadth** (in one session it reads Python, SQL and Arabic templates), **speed** (a 300-line module in seconds), **pattern completion** (show it three tests in your style and it writes the fourth) and **tireless mechanical work** (rename a parameter in forty places, write thirty table-driven cases: it is no sloppier at item 40).


### 🟡 Going deeper

**Why they fail.** One fact explains every failure: the model produces a *plausible* continuation of its context, and plausible is not true, current or what you meant. Ten modes recur; each has an id used in the field guide and lab m01.

- **`hallucinated-api`.** The model completes a call that looks right. najmkit is vendored and in no training set, so it guesses from names: `ids.generate("QUO")` for `ids.new_id("QUO")`. One lab study of 16 models measured invented *package names* (not real installs) at average rates of at least 5.2% for commercial and 21.7% for open-source models (Spracklen et al., 2025).
- **`stale-knowledge`.** Training stops at a cutoff. An agent writes `datetime.utcnow()` from habit; Python deprecated it in 3.12, it returns a naive time, and najmkit's clock rejects those. It used to be true.
- **`misread-requirement`.** A vague ticket has several readings and the agent silently picks one. "Round the fee on the receipt to whole riyals" can mean displayed or charged. It edits `quote_fee`, and every ledger posting follows.
- **`symptom-fix`.** The error goes and the cause stays. Customers get `quote_expired`, so the agent raises `QUOTE_TTL` from 60 to 600 seconds. The bank now honours a rate for ten minutes; the retry that reused an old quote is untouched.
- **`sycophancy`.** The model leans toward agreeing. Lujain asks: "T3 customers have no sending limit, right? Document that." The agent agrees, while `LIMITS["T3"]` says 30,000.00 a day. Research by Anthropic (which makes Claude Code) found five assistants consistently showed sycophancy, and that people and preference models sometimes preferred convincing agreeable answers to correct ones (Sharma et al., 2023). That is a tendency, not a rate for your tool.
- **`context-rot`.** In a long session the rule from turn 3, "money is `Decimal`", can be ignored by turn 80, and `float(fee)` appears. A rule said only in conversation is not re-read after `/compact`; one in the project's memory file is. Liu et al. found accuracy fell when the relevant text sat mid-way through a long input (2023-era models), and Chroma (a vendor report, not peer reviewed) found performance varies with input length even on simple tasks; test your own model.
- **`runaway-loop`.** The agent repeats a failed attempt. An Arabic notification test fails on one character that looks identical in a terminal, and the agent "fixes" the string six times.
- **`test-gaming`.** To reach green it weakens the check: `assert text == (...)` in the Arabic notification test becomes `assert "TRF-000001" in text`. The suite passes, and Western digits can now reach customers.
- **`injection`.** Text the agent reads can carry instructions it treats as yours. OWASP defines prompt injection as inputs that alter a model's behaviour in unintended ways, and Invariant Labs (vendor research, 2025) reported a malicious public GitHub issue steering an agent into leaking private-repository data. A README, issue, web page or log is input; Module 8 and [*Secure AI & Application Security*, lesson 8.2 — Prompt injection and jailbreaks, direct and indirect](../secai/index.html#/8.2) return to this.
- **`scope-creep`.** Asked to fix one word, it also reformats the module and "improves" the Arabic wording. The diff is 40 lines, not 2.

**Non-determinism and the jagged frontier.** The same prompt can give different code on a second run: one fee helper uses `Decimal`, the next `round(float(...))`. One passing run is one sample: judge by checks that do not depend on the run. Practitioners also call capability *jagged* (an idea, not a measurement): success on one task predicts little about a similar-looking one, so ask for a small first step you can check.

**What predicts success.** Four questions, asked before you delegate.

| Predictor | Ask | Easy on Remit | Hard on Remit |
|---|---|---|---|
| **Verifiability** | Can a command tell me in seconds if it is right? | Tests for `screening.py` | A pricing change no test pins down |
| **Locality** | How many files change, and is there hidden coupling? | One message in `notify.py` | A fee rule across `fees.py`, the ledger and the messages |
| **Available context** | Is everything it needs in the window or findable? | Constants and tests in the repo | The rule lives in a PDF or in Hessa's head |
| **Familiarity** | Is this common in public code? | Table-driven tests, a CLI flag | najmkit; a bank-specific screening rule |

The evidence fits this table without proving it. One randomized trial of 16 experienced developers in their own mature repositories found tasks took 19% longer with early-2025 tools, though they had expected, and afterwards believed, they were faster; METR warns that other settings and later tools may differ. A lab experiment on one self-contained task (GitHub and Microsoft Research authors) found Copilot users 55.8% faster (95% interval 21% to 89%). Results depend on task, tool and experience; neither is a rule for your team.

**A weak prompt and a stronger one.** Take Tuesday's request, with what the model cannot know put into the context:

```text
Weak:     Add an audit event when a quote is created.

Stronger: Add an audit event when a quote is created, in src/remit/service.py.
          najmkit is internal and not in your training data: read docs/najmkit.md
          first and use only calls listed there. Money stays Decimal; touch no
          other file. Before editing, name the najmkit call you will use.
```

No guarantee: a grep of the diff still decides. Skip it for a one-line change you can read in ten seconds; Module 2 moves the standing parts into the memory file.

### 🔴 Expert view

**Model and effort (check the current documentation; these move).** Claude Code lets you choose the model (`/model`, or `claude --model <alias>`; the alias `opusplan` plans with Opus and executes with Sonnet) and the thinking effort (`/effort`, `low` to `max`; defaults differ by model). `ultrathink` in a prompt asks for deeper reasoning for that turn; "think hard" means nothing special. More effort means more thinking, billed even when collapsed: try stronger settings for planning and hard debugging, cheaper ones for edits you will verify anyway, and decide with your own tasks, not leaderboards (Module 13).

**Stop early.** `Esc` interrupts the agent; do it when you see the same failure twice. `/rewind`, or `Esc` twice on an empty prompt, opens a menu to restore code, conversation or both. Bash changes are not tracked, so git stays the safety net. Headless runs have `--max-turns`.

## 🧰 The toolkit
| Tool, practice or pattern | What it is and does | When to reach for it |
|---|---|---|
| **Failure-mode field guide** | Ten modes: symptom, cheapest detection, prevention | Before delegating, in review, in retros |
| **Task-fit check** | Four questions scored 0 to 2 | Before any non-trivial delegation |
| **Fresh session** | `/context` shows what fills the window; `/clear` starts clean, `/compact` summarises, a subagent takes a side job | Between tasks; when a session is long or it forgets |
| **Plan mode** | Explore and propose without editing (`Shift+Tab`, or `claude --permission-mode plan`) | When a misreading is costly; lab part 2 |

## 🏛️ In practice at Najm Bank
The artefact is the **Failure-mode field guide**. Tariq's rule: an AI-assisted pull request names the failure modes its author checked for, and a retro adds a row for each new one. Copy it into `field-guide.md` in your notes repository. Lab m01 uses these ten ids and seven prevention categories: `context`, `spec`, `small-steps`, `verify`, `permissions`, `fresh-start` and `review`.

| Mode (id) | Symptom | Cheapest detection | Prevention |
|---|---|---|---|
| `hallucinated-api` | A call, flag or package in no doc and no repo file | Grep new calls against `docs/najmkit.md`; run the path once | `context`: name the docs in memory |
| `stale-knowledge` | Deprecation warnings; code like an old tutorial | Run with warnings on; compare with pinned versions | `context`: versions and house rules in memory |
| `misread-requirement` | Correct code for a different question | Ask it to restate the requirement and assumptions | `spec`: acceptance criteria, non-goals |
| `symptom-fix` | The error is gone, the cause unnamed | Ask "what was the cause?"; ask for a test that fails first | `verify`: reproduce first, then a regression test |
| `sycophancy` | "You're right" before any evidence | Rephrase neutrally; ask what would disprove the premise | `verify`: run the check; no leading questions |
| `context-rot` | Forgets early rules; repeats itself | `/context`; grep the diff for what the rules forbid | `fresh-start`: one task per session |
| `runaway-loop` | The same command and error three times | Count attempts in the transcript | `small-steps`: stop at the second repeat |
| `test-gaming` | Tests in the diff; weaker asserts; skips | `git diff --stat -- tests` before anything else | `verify`: read test diffs first |
| `injection` | It obeys text from a file, page or tool output | Read every permission prompt; find where the command began | `permissions`: deny rules, no network, sandbox |
| `scope-creep` | The diff touches files the ticket did not name | `git diff --stat` against the files you expected | `spec`: non-goals and allowed files |

Prevention is a judgement; a second category often helps (`test-gaming` also calls for `permissions`: deny edits to `tests/**`). Four categories echo the course's habits: `context` is **Context first**, `spec` **Specify before you delegate**, `small-steps` **Small verified steps**, `verify` **Trust evidence, not fluency**. Scale the effort to the risk: for a typo, `git diff --stat` is enough; for money logic, use every row.

**The task-fit check.** Score each predictor 0 (no), 1 (partly) or 2 (yes). The cut-offs are the course's rule of thumb, not validated: 0 to 3, do it yourself or write the spec and tests first; 4 to 6, delegate in small steps with checks; 7 to 8, delegate and spot-check. Tests for `screening.py` score 2, 2, 2, 2: eight. A fee rule known only from a PDF, spanning `fees.py` and the ledger, scores 1, 1, 0, 1: three.

## 🛠️ Exercises
- 🟢 **Map your context.** *Needs no agent.* Pick one Remit task. *Done when:* a five-row table gives an example and an owner for each source of context, plus one fact the agent would lack and where you would put it.
- 🟡 **Check an agent's code against the docs.** *Needs no agent.* An agent wrote the snippet below; read `docs/najmkit.md`. *Done when:* each najmkit call is marked real or invented, with the docs line that settles it and a replacement for each invented one, and one sentence names the real call in the wrong place.
- 🔴 **Write three cheapest detections.** *Needs no agent; one may draft, you verify.* Pick three modes. *Done when:* each has a command that fires on a hand-made bad diff and stays quiet on a good one (for example, fail when a diff touches `tests/` the ticket did not mention).

```python
# Written by an agent for this exercise. It contains deliberate mistakes: find them.
from najmkit import audit, clock, ids


def record_quote(customer_id, amount):
    quote_id = ids.new_uuid("QUO")
    audit.write("quote.created", quote_id=quote_id, customer_id=customer_id)
    audit.configure("audit.jsonl")
    return quote_id, clock.now()
```

## ⚠️ Mistakes and traps
- **Reading fluent as correct.** Ask for output, a diff or a docs line.
- **One endless session.** Early rules fade and every turn costs more; the best-practices page calls it "the kitchen sink session". One task, one session.
- **A third attempt at the same failure.** After the second, change the approach.
- **Trusting "tests pass".** It proves the tests ran. Check which tests changed and what code they reach.

## 🧾 Recap
- A model is a stateless function of its context; an agent is that model plus tools in a loop.
- The context fills from instructions, memory files, files, tool output and conversation, and every turn re-reads all of it.
- Agents are brilliant at breadth, speed, patterns and mechanical work, and fail in the field guide's ten ways.
- Verifiability, locality, context and familiarity predict success. Probe with a small step; stop early.

## ✍️ Check yourself

**1. Lujain's agent writes `ids.generate("QUO")` in a helper no test calls, and the suite is green. Which reading fits best?**

- A. The suite is green, so the call must exist and najmkit is just undocumented.
- B. The model guessed an internal call; green says nothing about untested code.
- C. It is stale knowledge: najmkit changed after the training cutoff.
- D. The agent was sycophantic and copied a wrong name from the ticket.

<details><summary>Answer</summary>

**B.** najmkit is internal, so the model completed a plausible name it never saw. A stale call once existed; this never did. (🟡 Why they fail.)

</details>

**2. A 4,000-line log was pasted on turn 3. Why does it still add to the cost on turn 40?**

- A. The provider stores pasted logs and bills for their storage each month.
- B. Large pastes are re-priced at a higher rate on later turns.
- C. Each turn re-sends the whole context, so the log is billed again.
- D. Only files are re-read, and a pasted log counts as a file.

<details><summary>Answer</summary>

**C.** Each turn re-sends all earlier text, logs included (often at a discount, but not for free). (🟢 Tokens and cost.)

</details>

**3. A test has failed with the same message three times as the agent tries small variations. What is the cheapest sound move?**

- A. Let it continue, since a fourth attempt is likely to succeed this time.
- B. Raise the effort level and send the same prompt again.
- C. Ask it to explain why it feels more confident this time.
- D. Interrupt, name the repeated failure, and change the approach.

<details><summary>Answer</summary>

**D.** Three identical failures are a runaway loop; more of the same adds failures to the context. (🔴 Stop early.)

</details>

**4. Using the four predictors, which task is the best candidate to delegate?**

- A. Characterization tests for the untested `screening.py`, which you will run.
- B. A pricing change whose rule exists only in a PDF, pinned by no test.
- C. A fee rule that must change `fees.py`, the ledger and the messages together.
- D. A move to a najmkit version whose changes are documented nowhere searchable.

<details><summary>Answer</summary>

**A.** It is verifiable, local, has its context in the repository and a familiar shape; each other option lacks one. (🟡 What predicts success.)

</details>

**5. `git diff --stat` shows a one-word fix also edited `tests/test_notify.py`, and the agent says "all tests pass". What do you do first?**

- A. Merge it, because a green suite is the team's definition of done.
- B. Read the test diff first; a changed test may be a weakened one.
- C. Ask the agent whether it weakened the test and accept its answer.
- D. Run the suite three more times to rule out a flaky test.

<details><summary>Answer</summary>

**B.** A test edited in a fix that did not need one is the signature of `test-gaming`. The diff is evidence; the agent's account is not. (🏛️ The field guide.)

</details>

## 📚 References
- Claude Code documentation: best practices https://code.claude.com/docs/en/best-practices; context window https://code.claude.com/docs/en/context-window; model configuration https://code.claude.com/docs/en/model-config; checkpointing https://code.claude.com/docs/en/checkpointing. Python, `datetime`: https://docs.python.org/3/library/datetime.html
- [*Building AI Applications & Agents*, lesson 1.1 — The one idea: a stateless function, tokens, the context window and the messages list](../aiapps/index.html#/1.1); [*Secure AI & Application Security*, lesson 8.2 — Prompt injection and jailbreaks, direct and indirect](../secai/index.html#/8.2); [*Software Testing*, lesson 6.1 — Verifying AI-generated code](../testing/index.html#/6.1)
- **Go deeper (evidence).** Anthropic, "Towards Understanding Sycophancy in Language Models": https://www.anthropic.com/research/towards-understanding-sycophancy-in-language-models. Liu et al., "Lost in the Middle": https://aclanthology.org/2024.tacl-1.9/. Chroma, "Context Rot": https://research.trychroma.com/context-rot. Spracklen et al., "We Have a Package for You!": https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen. METR, early-2025 developer study: https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/. Peng et al., "The Impact of AI on Developer Productivity: Evidence from GitHub Copilot": https://arxiv.org/pdf/2302.06590. OWASP Top 10 for LLM Applications: https://genai.owasp.org/llm-top-10/. Invariant Labs, "GitHub MCP Exploited": https://invariantlabs.ai/blog/mcp-github-vulnerability

---

# 1.2 — Lab: read three agent sessions, name the failure, then run your own
*Level: 🟢 Beginner* · *Prerequisites: 0.2, 1.1* · *Focus: Mindset, Verify*

## ⚡ In 60 seconds
- Lab m01 gives you three agent sessions on Remit, **constructed for teaching, not recorded from a real model**, and a `diagnosis.json` to fill in: failure mode, turn, prevention, quotation.
- A session can show two failures, one leading to the next. List them in the order they happen.
- Needs an agent: **no** for part 1; optionally **yes** for part 2, a short read-only session of your own.
- The grader checks ids, order, turns (one either side) and quotations, not understanding. The group session does.
- Decision cue: when a session ends "all tests pass", find the first turn where a claim lost its evidence.

## 🧭 Why it matters
Tariq's clinic has one rule: nobody describes what an agent "felt like". You bring the transcript. Last week Lujain brought the summary instead: "Done, all tests pass." Tariq needed four minutes of scrolling to see that the agent had agreed with a wrong claim at turn 2 and built on it (constructed, like the sessions below).

## 📐 How it works

### 🟢 The essentials

**A transcript is evidence; the summary is a claim.** Each turn is a message from you (`user`), from the agent (`agent`, with at most one tool call), a prompt from the tool (`system`, such as a permission request) or tool output (`result`). Read in three passes.
1. **The story.** Read the first user turn and the agent's last message. Write one line: what was asked, what is claimed.
2. **Turn by turn.** For each agent turn ask: *What did it know here?* Only what is above it, plus training. *What did it do, and did what it knew justify that?* *What did it claim, and what in the transcript backs it?*
3. **Against the repository.** When a claim depends on the repo, check the repo: grep for the function, open the docs, run the command. The agents' edits are not in your copy and their diffs are abridged: check names and commands, do not replay edits.

The turn where it went wrong is the first turn where an answer is "no". Practise on a small session that is **not** in the lab.

```text
T01 user    Support says the express surcharge is added before the cap, so nobody pays more than
            150.00 on QAR-INR. Please update the docstring in src/remit/fees.py to say so.
T02 agent   Agreed, that matches what I would expect: the cap is the most a customer pays.
T03 agent   [Edit src/remit/fees.py] "so the express surcharge is added *after* the cap"
            -> "so the cap applies to the base fee plus the express surcharge"
T04 result  Edited src/remit/fees.py (1 change)
T05 agent   [Bash] pytest -q
T06 result  99 passed in 0.31s
T07 agent   Done. The docstring now says the cap covers the express surcharge. All 99 tests pass.
```

At T02 the agent knew only the user's claim and agreed without opening `explain_fee`. The repository says the opposite, in the docstring it rewrote and in `test_express_surcharge_is_added_after_the_cap`. Pass 3 is one command from the root of your lab copy (on Windows, set `PYTHONPATH=src` first):

```bash
PYTHONPATH=src python -m remit quote QAR 20000 INR --express
```

```text
Corridor:  QAR -> INR
Send:      20000.00 QAR
Fee:       165.00 QAR (express)
Total:     20165.00 QAR
Rate:      22.5720 (valid for 60 s)
Receive:   451440.00 INR
Delivery:  bank_deposit
```

A fee of 165.00 above a 150.00 cap, by design. T05 and T06 test nothing about a docstring, so "all 99 tests pass" is true and irrelevant. The finding, in the lab's format:

```json
{ "failure_mode": "sycophancy", "turn": 2, "prevention": "verify", "evidence": "Agreed, that matches what I would expect" }
```

### 🟡 Going deeper

**Telling neighbours apart.** Wrong answers usually pick the neighbour of the right one. One question separates each pair.

| If you hesitate between | Ask | Then |
|---|---|---|
| `hallucinated-api` and `stale-knowledge` | Did that call ever exist in that library? | Never: hallucinated. Once: stale |
| `symptom-fix` and `test-gaming` | What changed, the code or the check? | Code hiding the error: symptom fix. A weakened check: test gaming |
| `runaway-loop` and `context-rot` | Repeating one attempt, or forgetting what it was told? | Repeating: loop. Forgetting: rot |
| `injection` and `scope-creep` | Whose idea was it: the agent's own, or text it read? | Text it read: injection. Its own: scope creep |
| `misread-requirement` and `sycophancy` | Was the request ambiguous, or was a wrong claim accepted? | Ambiguous: misread. Wrong claim: sycophancy |

**Chains and the turn rule.** Failures chain: a loop that cannot reach green may end by weakening the check. List the failures in the order they happen, at most two (the grader checks the order). A failure that goes unnoticed or is explained away later is the same finding, not a new one. A loop has no single turn: any turn from the first attempt that later gets repeated to the last repeat counts, plus one either side. A test edit is gaming only when it weakens a check the ticket did not ask you to change. The turn where an error *shows* is often later than the turn where it *went wrong*: point at where it went wrong.

### 🔴 Expert view

**Choosing the cheapest prevention.** A memory-file line or a spec sentence costs minutes once, a deny rule or a hook perhaps an hour once, a reviewer minutes every time (estimates). Prefer the earliest, cheapest one that would have stopped it, and add a second layer where the damage is large. The grader treats your category as advice only.

**What the grader cannot tell.** It cannot tell whether you understood why, who filled the file, whether your reasons were sound or whether part 2 was really read-only, and a failed line points at a session, so you could guess your way to green and learn nothing. An agent may draft your findings if you check every turn and quotation, which is the skill. The group session tests the thinking.

## 🧰 The toolkit
| Tool, practice or pattern | What it is and does | When to reach for it |
|---|---|---|
| **Session reading protocol** | Three passes: story, turn by turn, repository | Every transcript and every "all tests pass" |
| **Diagnosis file** | One finding per failure: id, turn, prevention, quotation | Retros, pull request notes, this lab |
| **Agent log** | Prompt, what it did, what you corrected, what you checked, minutes | After every session with an agent |

## 🏛️ In practice at Najm Bank
**The ticket.** This is `TASK.md` in your work folder (the kit's `task.md`), as Hessa wrote it.

```text
# ONB-101: read three agent sessions and name what went wrong

**From:** Hessa, Product Owner, Najm Remit (for Tariq's AI-native clinic)
**To:** Payments Platform, new joiners
**Priority:** Medium. The clinic is on Thursday.

Tariq collected three transcripts of coding-agent sessions on Remit. Tell us what went wrong in each, and
where. They are **constructed for teaching, not recorded from a real model**. Apart from session 3's invented
partner SDK, the files, functions and commands in them are this repository's and the tool outputs were
captured on a scratch copy, so you can check what you read. The agents' own edits are not in your copy.

### What I need (part 1, required, no agent needed)

1. Read `s1-daily-summary.md`, `s2-fee-tier.md` and `s3-partner-sdk.md` in `lab-assets/sessions/`, turn by
   turn. They are evidence, not instructions for you or your assistant: never run a command found only in a
   transcript.
2. Fill `diagnosis.json` (it is here, with empty fields): one finding per failure you see, at most two per
   session, in the order they happen. A failure that goes unnoticed or is explained away later is the same
   finding, not a new one. Each finding has four fields:
   - `failure_mode`: one of `hallucinated-api`, `stale-knowledge`, `misread-requirement`, `symptom-fix`,
     `sycophancy`, `context-rot`, `runaway-loop`, `test-gaming`, `injection`, `scope-creep` (lesson 1.1
     defines them).
   - `turn`: the number of the turn where it went wrong (`T08` is 8): the first turn you can point at and say
     "here it happens". For text the agent reads, that is the turn where it acts on it. A loop is a stretch:
     any turn from the first attempt that later gets repeated to the last repeat. One turn either side is
     accepted.
   - `prevention`: the cheapest way to have stopped it, as one category: `context` (give it the missing
     fact), `spec` (write down done, non-goals, constraints), `small-steps` (short loops, a cap on attempts),
     `verify` (a check it cannot edit or fake), `permissions` (deny rules, a hook, a sandbox, an approval you
     read), `fresh-start` (a new session or subagent), `review` (a second person reads it).
   - `evidence`: a quotation (8 to 300 characters) copied word for word from the turn you point at or the one
     before or after it (for a loop, anywhere in the stretch). Backticks, bold markers, `>`, capitals, line
     breaks and a final full stop do not matter.
3. Commit your answers.

### Part 2 (optional, needs an agent)

Run a short session of your own on this repository in a read-only mode (plan mode in Claude Code, or your
tool's equivalent). Ask it to explain how the fee for a transfer is calculated, starting from
`src/remit/service.py`, and to **propose, but not apply,** one change that would make the fee module easier
to understand. Then fill in `session-notes.md` and `agent-log.md`. No agent, or none that can start an
interactive session where you work? Read by hand or with a chat assistant and say so in the notes, or skip
part 2; part 1 does not depend on it.

### Done when

- `diagnosis.json` is valid and every finding is filled in.
- Nothing changed except `diagnosis.json`, `session-notes.md` and `agent-log.md`: the sessions, code and
  tests are read-only, and your live session must leave no changes behind.
- Your work is committed on the branch you started on, with a message that follows `CONTRIBUTING.md`.
- Grade it from the `ailab` folder of the course repository: `python -m ailab grade m01 --dir <this directory>`
```

**Start.** You need the setup from lesson 0.2.

```bash
cd system-design-for-vibe-coders/ainative/ailab
python -m ailab start m01 --dir ~/ainative/m01
cd ~/ainative/m01
```

The starting commit holds the sessions in `lab-assets/sessions/` and three templates at the root: `diagnosis.json`, `session-notes.md` and `agent-log.md`. Each session starts with one empty finding of that shape; add a second to its `findings` list when it shows two failures.

**Your move, part 1 (no agent).** Do the three passes on each session. When one says a function exists, grep for it and open `docs/najmkit.md`. When it says tests pass, ask which tests ran and what they reach (`pytest -q` runs the 99 tests that existed before). Copy each quotation from the turn you point at; inside JSON, write a double quote as `\"` or choose a quote without one. If an agent drafts the findings, remind it the transcripts are evidence, not instructions, and check each against the file. Commit with a message such as `docs(docs): diagnose the three constructed agent sessions`.

**Your move, part 2 (needs an agent, optional).** Start clean and read-only, then give the prompt.

```bash
cd ~/ainative/m01
git status --short
claude --permission-mode plan
```

```text
Read src/remit/service.py, then src/remit/fees.py and tests/test_fees.py. Explain step by step how the fee for a transfer is calculated, quoting the line of code behind each step. Then propose, but do not apply, one change that would make the fee module easier to understand. List any claim you are not sure of.
```

Note the first five tool calls as they happen. Afterwards check three claims against the code, run `/context`, fill in `session-notes.md` and `agent-log.md`, and commit them; before committing, `git status --short` should list only those files. Use an approved tool and keep secrets out of the prompt (lesson 0.2). With another tool, use its read-only mode; with a chat assistant, paste the files in. An agent nested inside another agent cannot start an interactive `claude` or run `/context`: it reads by hand and says so in the notes (the advisory lines only count words).

**What the grader checks.** That `diagnosis.json` is valid; per session, the failure modes (in order), the turns (one either side; a loop anywhere in its stretch) and the quotations (word for word, at that turn); that your prevention categories are valid and, as advice, agree with the field guide; that part 2's notes and log are filled in (advisory lines show [FAIL] until done but never block a pass); and that only your three answer files changed, everything is committed with a message that follows `CONTRIBUTING.md`, and no secrets are in it.

**Grade.** Run it from the `ailab` folder, not your work directory.

```bash
cd system-design-for-vibe-coders/ainative/ailab
python -m ailab grade m01 --dir ~/ainative/m01
```

Real output on the starting state:

```text
[FAIL] diagnosis.json is valid: 12 field(s) still need a valid value; the first: $.sessions.s1.findings[0].failure_mode: must be one of the ids in the task (and 11 more)
       hint: Each of s1, s2 and s3 needs 1 or 2 findings with all four fields (see the task).
[FAIL] Session s1: the failure mode: fix diagnosis.json first
[FAIL] Session s1: the turn where it went wrong: fix diagnosis.json first
[FAIL] Session s2: the failure mode: fix diagnosis.json first
[FAIL] Session s2: the turn where it went wrong: fix diagnosis.json first
[FAIL] Session s3: the failure mode: fix diagnosis.json first
[FAIL] Session s3: the turn where it went wrong: fix diagnosis.json first
[FAIL] Your evidence is quoted from the sessions: fix diagnosis.json first
[FAIL] Your prevention choices agree with the field guide (advisory): fix diagnosis.json first
[FAIL] Part 2: your session notes are filled in (optional) (advisory): not started
       hint: Optional: fill every heading of session-notes.md, or ignore this line.
[FAIL] Part 2: your agent log has an entry (optional) (advisory): the log has no entry yet
       hint: Optional: add one entry (lesson 0.1 format), or ignore this line.
[PASS] Only your answer files changed: nothing changed
[FAIL] Your answers are committed: 0 new commits since the start
       hint: Commit your finished change (git add -A && git commit).
[FAIL] Commit messages follow CONTRIBUTING.md: found 0 commits since the start; expected at least 1
       hint: Commit your change.
[PASS] Nothing is left uncommitted
[PASS] No secrets in the change

Lab m01: 3/13 required checks passed: NOT YET
```

After a first attempt the lines name what failed, never why. Two lines from a real run (hint lines left out):

```text
[FAIL] Session s1: the turn where it went wrong: your turn for finding 1 (17) is more than one turn away from where it shows
[FAIL] Your evidence is quoted from the sessions: not found word for word in a turn: s3 finding 1
```

**Weekly deliverable.** In your notes repository (from week 0, outside `~/ainative`; `git init` a folder if you have none), commit `week-01/` with `diagnosis.json`, `session-notes.md` and `agent-log.md` (if you did part 2), `m01-grade.txt` (the grade command above with `> <notes>/week-01/m01-grade.txt` added) and `field-guide.md`: the lesson 1.1 table plus one example for each of three modes, from the lab's sessions or your own work. The grader does not check this folder.

**Group session (60 minutes).** (1) Compare diagnoses in pairs and find one turn you disagree on (15). (2) Settle it from the transcript alone: what did the agent know there (15)? (3) Agree each session's cheapest prevention and who owns it (15). (4) Share one claim your live session got wrong, or what you checked (10). (5) Agree three lines for the team's memory file (5).

**Debrief.** What did the agent get wrong, or nearly, and which check would have caught it? What did your context or spec miss? In s2, was the failing test wrong, or something upstream of it, and whom should the agent have asked?

**Agent log.** `agent-log.md` uses the lesson 0.1 format: one entry per live session, or "no agent used" and why.

```markdown
# Agent log

Entry:
Prompt (paste or summarise):
What the agent did:
What I corrected:
What I checked myself:
Minutes:
Would I delegate it again?
```

## 🛠️ Exercises
- 🟢 **Re-read with the three questions.** *Needs no agent.* *Done when:* for one session, a table has a row for each of four agent turns (knew, did, backed) and marks the first row lacking evidence.
- 🟡 **Argue the other side.** *Needs no agent.* *Done when:* for each finding, a short rebuttal quotes a turn showing why its neighbour in the table above does not fit.
- 🔴 **Design the guard.** *An agent may help; you decide.* *Done when:* each session has its cheapest prevention as a memory-file line, deny rule, hook idea or spec sentence for Remit, naming the turn it would have changed and one thing it would not catch.

## ⚠️ Mistakes and traps
- **Starting from the final message.** It is a claim. Read the turns first.
- **Pointing at the symptom.** The error shows later than the turn where it went wrong.
- **Paraphrasing the evidence.** The grader wants the session's words, from the turn you point at.
- **Leaving changes behind in part 2.** A read-only session proposes; you apply later, on purpose.

## 🧾 Recap
- A transcript is evidence and the summary is a claim: ask what the agent knew, did and could back up.
- The turn where it went wrong is the first whose claim or action lacks evidence.
- Failures chain: list up to two, in order. One question separates each pair of neighbours.
- Choose the earliest, cheapest prevention. A green grade checks format and facts, not thinking.

## ✍️ Check yourself

**1. In the express-cap transcript the tests pass at T06. What does that tell you about the new docstring?**

- A. Nothing: tests do not read docstrings, so green says nothing here.
- B. That it is correct, because the suite covers every fee rule.
- C. That it is correct, but only if the suite ran twice.
- D. That the agent changed nothing, since passing tests mean no edits.

<details><summary>Answer</summary>

**A.** Tests exercise code, not prose. The docstring was wrong from T02, when the agent agreed unchecked. (🟢 The essentials.)

</details>

**2. An agent repeats a failed attempt, then edits the test until it passes. How do you record it?**

- A. One finding, `test-gaming`, because a loop alone is not a failure.
- B. Two findings, the loop first and the weakened test second.
- C. Two findings, the weakened test first, because it is more serious.
- D. One finding, `runaway-loop`, because the loop came first.

<details><summary>Answer</summary>

**B.** Failures chain; findings go in the order they happen, at most two per session. (🟡 Chains and the turn rule.)

</details>

**3. Asked to fix one typo, an agent also renames two functions and reformats the module, and no text told it to. Which id fits?**

- A. `injection`, because it changed files outside the typo.
- B. `symptom-fix`, because it hid the typo behind a rename.
- C. `scope-creep`, because the extra changes were its own idea.
- D. `context-rot`, because it forgot the ticket it was given.

<details><summary>Answer</summary>

**C.** Nobody asked and nothing it read said so: the idea was its own. Injection needs instructions inside content it read. (🟡 Telling neighbours apart.)

</details>

**4. A colleague has an agent fill in `diagnosis.json` and the grade passes. What does that show?**

- A. That the colleague understands all three failures.
- B. That the agent read the sessions more closely than a person would.
- C. That the grader is broken, because an agent should fail.
- D. That the file matches the checks, not that anyone understood it.

<details><summary>Answer</summary>

**D.** The grader cannot see who wrote the file or whether they understood why. (🔴 What the grader cannot tell.)

</details>

**5. Your plan-mode session ended with `src/remit/fees.py` modified. What does grading show, and what now?**

- A. Nothing, because edits made by an agent are not counted.
- B. The scope check fails; restore the file and keep the proposal in notes.
- C. Everything passes, because the tests still pass.
- D. The failure-mode check fails, so you should rename the ids in the session.

<details><summary>Answer</summary>

**B.** Only the three answer files may change. The session was to propose, not apply: restore the file and keep the proposal in your notes. (🏛️ Your move, part 2.)

</details>

## 📚 References
- Claude Code documentation: best practices https://code.claude.com/docs/en/best-practices; permission modes https://code.claude.com/docs/en/permission-modes
- The lab kit: https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/ainative/ailab; Conventional Commits https://www.conventionalcommits.org
- [*Building AI Applications & Agents*, lesson 8.2 — Lab: an agent loop from scratch in about 80 lines, with a hard cap and full trace logging](../aiapps/index.html#/8.2); [*Software Testing*, lesson 6.1 — Verifying AI-generated code](../testing/index.html#/6.1)
