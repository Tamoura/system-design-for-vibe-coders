# Module 6 — Discovery and requirements

*Every agent project starts with a sentence like "we should have an assistant for the Service Desk", and most of the project's risk hides inside it. This module teaches you to find out what the customer really needs and to write it down so it can be built and tested. Lesson 6.1 is a discovery workshop on Najm Desk: you map stakeholders, read fictional interviews with Hind and Yara and a shadowing report from the Service Desk floor, inventory systems and data, size the value as a range, tier the risk, ask whether an agent is even the right tool, and write a one-page agent brief. Lesson 6.2 turns the brief into a testable specification: requirements you can fail, a permissions matrix, Given/When/Then acceptance criteria, an eval seed set and a spec review with the customer. Everything runs offline, and no code in this module calls a model.*

> **Layer:** Delivery — the customer-facing work that decides what an agent should do, for whom, under which rules, and how everyone will know it works, before any of it is built.

---

# 6.1 — Discovery: from a business problem to an agent brief: stakeholders, workflows, data, risk and "should this be an agent?"
*Level: 🟢 Beginner* · *Prerequisites: 0.1, 5.1* · *Layer: Delivery*

## ⚡ In 60 seconds
- **Discovery** is the work between "we should have an AI assistant" and "here is what we build, for whom, and what it must never do": find out what the customer needs and write it down, as a one-page **agent brief**, so it can be built and tested.
- Talk to the sponsor, the people who do the work and the risk owners. Ask about **past behaviour**, not future opinions.
- Two sources that disagree are a finding, not noise. Size value as a **range**, never one number.
- Before choosing an agent, ask four questions and try cheaper alternatives.
- Biggest trap: trusting one source, then letting an AI assistant smooth over contradictions or invent quotes.

## 🧭 Why it matters
Lujain reads Hind's email: *seventy percent deflection, open 24 hours, unlock accounts by itself*. In four days she builds a lovely demo that unlocks accounts through a test tool. Then Yara asks: "Where is the call-back?" Policy has an agent verify a lost-authenticator request by calling the person's manager. The demo skips it, Noura's team would block it, and the work is thrown away. (Hypothetical, as all Najm stories are.)

Nothing in the code was wrong. The brief was: Lujain had one source, and the sponsor sees the dashboard, not the floor. A wrong sentence in a brief costs an afternoon; in code, weeks; in a pilot, trust.

## 📐 How it works

### 🟢 The essentials

**Map the stakeholders first**: what each cares about, and who is missing.
- **Sponsor** (owns the outcome): Hind.
- **Users:** staff, contractors, and the agents who receive hand-offs.
- **Operators** (live with its mistakes): Yara's team, later Maha's SRE team.
- **Risk owners** (can say no): Layla, Hamad, Noura, Sara.
- **Blockers** (hold a dependency): Salem's platform team; the owners of TicketHub, Najm ID, PeopleCore and the policy library.

**A five-day plan.** Read and map; interview Hind and Yara; shadow the desk; walk the systems and meet the risk owners; write the brief and read it back to Hind.

**Interviews: ask about their life, not your idea.** Rob Fitzpatrick's *The Mom Test* is a good short guide. Paraphrased: people are kind about your idea, so ask about specific things that happened, and listen more than you talk. Ask about **past behaviour** ("Tell me about the last time…"); future opinions are polite guesses. Ask **open questions**; answer vagueness with "for example?". Never **pitch or lead**: a question holding your solution earns agreement, not evidence.

| Weak question | Why it fails | Stronger |
|---|---|---|
| "If we built an assistant … that resolved most of those tickets on its own, wouldn't that be great?" (H-03) | Leads, pitches | "Tell me about the last time the desk was under pressure." |
| "And you think staff would use a chat assistant in the portal?" (H-19) | Future opinion | "How did the last ten VPN callers reach you?" |
| "So English first, then Arabic later?" (H-17) | Confirms your guess | "What share of last week's tickets were in Arabic?" |

**Shadow the work.** An interview tells you what someone believes; shadowing shows what happens. Sit beside agents, time what you see, and draw the **as-is process**: each step, who does it, what it touches, where it waits. This is Najm's. Najm Desk can speed up the clarifying loop and the answers; it must stay out of the call-back.

```mermaid
flowchart TD
    A["Request: phone, portal, email, Teams"] --> B["Duty agent triages by hand"]
    B --> C{"Enough information?"}
    C -- "no" --> D["Ask again: 3 to 4 minutes a round trip"]
    D --> C
    C -- "yes" --> E{"Authenticator lost?"}
    E -- "no" --> F["Answer from a macro, page or cheat sheet"]
    E -- "yes" --> G["Call the manager back: 20 minutes to 2 hours"]
    G --> H["Agent changes the account"]
```

**A worked example: three sources, one fact.** Hind (H-12) says any agent unlocks an account in a minute and wants the assistant to do it alone. Yara (Y-10) says a lost authenticator needs a call-back to the manager's PeopleCore number, and that is the bottleneck. The shadowing notes (A-10) timed one at 35 minutes. Three notes:
- **Requirement (hidden):** an unlock is a *request* an agent approves after the call-back. The assistant never changes an account.
- **Risk:** social engineering; a chat that unlocks accounts is an attacker's favourite door.
- **Open question:** if the manager does not answer, who is the delegate?

Hind sees the minute the click takes; Yara sees the hour it takes to get there.

### 🟡 Going deeper

**Systems and data inventory** (fictional figures). For each system the agent will touch, write what you need from it, how **access** is granted, the **quality** of its data and its **classification** (Public, Internal, Confidential or Restricted; "proposed" until Sara confirms).
- **TicketHub:** status, draft, create. Priority set by hand, passwords pasted into text, a restricted flag on about 3% of tickets. Confidential.
- **Najm ID:** the unlock request, privileged, through Hamad's team. Contractors are guests. Restricted.
- **PeopleCore:** manager, department. Wrong for about one person in ten; no contractors. Confidential.
- **DeviceDesk:** its refresh flag uses a three-year rule; policy says four. Out of v1.
- **Policy library:** the answers. Notices never reach the pages; an old PDF says 12 characters. Internal.

> **Your platform.** Add rows for its identity provider, secrets store, ticketing and approvals: owner, how you get a read-only credential, what it logs.

**Size the value as a range.** Weekly hours freed = tickets in scope × share handled alone × minutes saved ÷ 60, each term a low and a high with a source or "assumption". Fictional baseline: 450 policy tickets a week (A-03); of 40 sampled, 22 fully covered and 10 partly (A-05), so 20% to 50% handled alone is defensible; 4 to 8 minutes saved (assumption). Low: 450 × 0.20 × 4 ÷ 60 = 6 hours. High: 450 × 0.50 × 8 ÷ 60 = 30 hours. Against about 560 agent hours a week (assumption: 14 agents at 40 hours) that is 1% to 5%. Requesters' waiting time is probably the bigger, softer prize. Subtract running cost, Yara's review time and source upkeep. Hind's 70% lies outside the range; the range is the conversation to have.

**Risk tiering** sets how much review a capability needs. It is a working tier, not a legal one; Layla classifies formally ([*AI Governance*, lesson 8.1 — Use-case intake, business case and risk tiering](../aigp/index.html#/8.1)). **Tier 1** reads Internal data and changes nothing: policy answers. **Tier 2** reads personal data or writes with the user's confirmation: ticket status, draft, creation. **Tier 3** touches identity or security with a person approving: the unlock request, the security hand-off. **Tier 4**, acting alone on identity or money, is not in v1. The highest tier decides who you invite; Tier 3 means Noura and Hamad from week one.

**Constraints you inherit.** The AI-tools policy keeps Confidential and Restricted data, customer data and credentials out of external AI services. Staff data is personal data (Qatar's PDPPL; the GDPR for EU staff; Sara advises). Languages: Arabic, English, mixed. Governance signs off changes; every write needs a person or a policy gate. First question to Layla and Hamad: is our model service an approved destination for Internal and Confidential data?

**Should this be an agent?** Four questions, in the spirit of Anthropic's advice on when to use agents (linked below). They are a heuristic, not a quotation:
1. **Complexity:** is the path unknown in advance? If you can draw the flowchart, build a workflow (lesson 5.1).
2. **Value:** is each run, and the total, worth the calls, review and upkeep?
3. **Viability:** can it do every step: tools, data, access, a checkable "done"?
4. **Cost of error:** how bad and reversible is a mistake, and how soon would you notice?

Try the cheaper alternatives first: **search** (the answer is on one page); a **form** (the same facts are missing every time); **rules** (explicit, stable decisions); a **workflow** (you can draw the path); a **process change** (the notice reaches the page); **RPA**, scripts that click through screens (stable work, no language).

Najm Desk's verdicts. Value and viability come from the value range and inventory above; the other two questions set the shape. Do ticket status and hand-off yourself:

| Capability | Path known? | Cost of error | Verdict |
|---|---|---|---|
| Policy answers | Yes: search, then answer | High: wrong policy (H-10) | Workflow |
| Draft a ticket | Varies: ask for what is missing | Low: the user confirms | Bounded loop; try a form first |
| Unlock request | Yes: fixed steps | High: social engineering | Workflow, a person approves |

So v1 is a **workflow with one bounded loop**; Module 7 decides the architecture. The brief records *why*, so nobody quietly enlarges the autonomy.

### 🔴 Expert view

**Anti-requirements** say what the agent must not do, as firmly as what it must. They stop scope creep and calm risk owners. Najm Desk v1 sets no priority (Y-08), changes no account, approves nothing, gives no refresh advice, reads no restricted ticket and promises no response time after hours.

**Red flags.** The sponsor cannot name a user. The solution came before the problem. Nobody lets you meet the people doing the work. Nobody has chosen between "never wrong" and "seventy percent" (H-08, H-04). Risk owners first hear of it at the demo. One flag is a question; three is a different project.

**Using an AI assistant in discovery.** Good uses: interview guides, first lists from notes, clustering, critique, role-playing Hind. Limits:
- **Confidentiality.** Real transcripts hold personal and internal data, which the AI-tools policy keeps out of external AI tools. Use the approved internal assistant, redact first, or ask Sara. The transcripts here are fictional.
- **Invention and smoothing.** It writes plausible quotes confidently and merges two conflicting claims into one tidy sentence.
- **Blindness.** A hidden requirement is not in the transcript; only shadowing finds it.

## 🧰 The toolkit
| Tool, practice or pattern | What it is and does | When to reach for it |
|---|---|---|
| **Stakeholder map** | Sponsor, users, operators, risk owners, blockers | Before any meeting |
| **Interview guide** (The Mom Test, Fitzpatrick) | Open questions about past events | Every interview |
| **As-is process map** | Steps, owners, systems, waits | Before automating |
| **Systems and data inventory** | Need, access, quality, classification | Before promising |
| **Value range** | A low and a high for every term | When asked what it is worth |
| **Risk tier** | A working tier from what the agent touches | To pick reviewers |
| **Agent-or-not check** | Four questions, six cheaper alternatives | Before architecture talk |
| **Agent brief** | One page from problem to open questions | End of discovery |

## 🏛️ In practice at Najm Bank
The artefact is the **agent brief** in `docs/agent-brief.md`, with its evidence in `docs/discovery-notes.md`. No specification starts before Hind confirms the brief.

```markdown
# Agent brief: <name>, v0.1 (<date>, owner, readers)
1. Problem. In the customer's words, with cited turns, e.g. [H-02].
2. Users and context. Who, languages, volumes, peaks.
3. Value hypothesis. Low, base, high; sources or "assumption".
4. Solution shape. Workflow, agent or alternative; the four questions.
5. Scope v1. In and out; autonomy per capability (suggest, draft, approve, act).
6. Systems and data. Need, access, quality, classification.
7. Risk. A tier per capability; top five risks and owners.
8. Constraints. Policies, privacy, languages, governance dates.
9. Anti-requirements. What it must never do, each sourced.
10. Success measures. Draft metrics with definitions.
11. Open questions. Owner and date each; unresolved contradictions.
12. Decision requested. One sentence: what Hind must decide next.
```

**The lab material** is three fictional sources in `labkit/data/`: `m06_interview_hind.md`, `m06_interview_yara.md` and `m06_as_is_process.md`, every turn with an id such as `[Y-10]`. They contradict each other and hide requirements on purpose; `m06_discovery_key.md` is the spoiler, for after your own pass. Your notes use `REQ-`, `RISK-`, `CON-` and `Q-` lines, each ending in a citation:

```text
- REQ-1 [Hidden] An unlock is a request an agent approves after a call-back. [Y-10 "never a number she gives us"]
```

```python
# labs/m06/check_notes.py
"""Check that discovery notes quote their sources.   python labs/m06/check_notes.py docs/discovery-notes.md
A citation is [Y-10 "call-back"]: a turn id, then two or more words copied from that turn. Every REQ, RISK, CON or Q line needs one.
Exit 0 = clean. It checks that a quote is REAL; it cannot check that your reading of it is right."""
import re
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "labkit/data"
TURN = re.compile(r"^\[([HYA]-\d+)\]\s*(.*)$")                   # a source line:  [Y-10] text
CITE = re.compile(r'\[([HYA]-\d+)\s+"([^"]+)"\]')                # a citation:     [Y-10 "text"]
ITEM = re.compile(r"^\s*[-*]\s*\*{0,2}(?:REQ|RISK|CON|Q)-\d+")   # a line you must defend


def norm(s: str) -> str:
    return " ".join(re.sub(r"\W+", " ", s.lower()).split())      # ignore case, punctuation and spacing


def load_turns() -> dict[str, str]:
    """{turn id: text} from the three source files."""
    names = ("m06_interview_hind.md", "m06_interview_yara.md", "m06_as_is_process.md")
    return {m[1]: m[2] for n in names for x in (DATA / n).read_text(encoding="utf-8").splitlines() if (m := TURN.match(x))}


def check(notes: str, turns: dict[str, str]) -> list[str]:
    found = []
    for n, line in enumerate(notes.splitlines(), 1):
        cites = CITE.findall(line)
        if ITEM.match(line) and not cites:
            found.append(f"line {n}: no citation (source it, or turn it into a question)")
        for tid, quote in cites:
            q = norm(quote)
            if tid not in turns:
                found.append(f"line {n}: there is no turn {tid}")
            elif " " not in q or f" {q} " not in f" {norm(turns[tid])} ":          # whole words, at least two
                found.append(f"line {n}: {tid} does not say \"{quote}\" (two or more whole words)")
    return found


if __name__ == "__main__":
    text, turns = Path(sys.argv[1]).read_text(encoding="utf-8"), load_turns()
    problems = check(text, turns)
    print("\n".join(problems) or "every citation checks out")
    cited = {t for t, _ in CITE.findall(text)}
    print("not cited yet, read again:", *(t for t, x in turns.items() if t not in cited and not x.startswith("**You:**")))
    sys.exit(1 if problems else 0)
```

It catches invented and misquoted evidence and lists uncited answer turns, where missed requirements hide. *Works offline:* both scripts and their tests need no key, model or mock server. *Needs people:* whether a requirement is right; the kit's mock is scripted rules, not judgement.

**Weekly deliverable.** Commit `week-06/` with `docs/discovery-notes.md`, `docs/agent-brief.md`, the second-interview guide and a `NOTES.md` with quiz answers and what you would challenge.

**Group session (60 minutes).** (1) Find who is missing from each stakeholder map (10). (2) Two learners interview a third, who plays Hind from the transcript only; the room scores leading questions (20). (3) Compare contradiction lists (15). (4) Read each "decision requested" aloud (15).

**Build it with Claude Code.** After your own pass, give this to Claude Code in plan mode (check the current Claude Code documentation):

```text
Goal: draft docs/discovery-notes.md for Najm Desk from aiapps/labkit/labkit/data/m06_interview_hind.md,
m06_interview_yara.md and m06_as_is_process.md.
Format: lines starting REQ-n (mark Stated, Implied or Hidden), RISK-n, CON-n or Q-n, each ending in a
citation: [Y-10 "words copied exactly from that turn"].
Constraints:
- Use only those files. Invent no fact, number, name or quote; if the sources are silent, write a Q.
- Never merge a contradiction: give both claims, both citations and a way to settle it.
- Do not open m06_discovery_key.md, write the brief or choose a design. Edit only docs/discovery-notes.md.
Acceptance: python labs/m06/check_notes.py docs/discovery-notes.md exits 0. Show the plan first.
```

**Verify before you accept it.**
- Compare its list with your own: what did it miss, and what did you?
- Run `check_notes.py`; each uncited answer turn is noise or a missed requirement.
- Check five citations by eye, and hunt invented facts: a number not in a source, a "must" where the speaker said "I'd like".

## 🛠️ Exercises
None needs the real API.

- 🟢 **Extract.** Write `docs/discovery-notes.md` from the three sources: 12 requirements, 6 risks, 8 open questions and every contradiction. *Done when:* `check_notes.py` exits 0 and five requirements are ones Hind never asked for.
- 🟡 **Write the brief.** Fill the template, with your own value range and a four-question verdict for each of the five capabilities. *Done when:* every number cites a turn or says "assumption", and the decision requested is one clear sentence.
- 🔴 **Plan round two.** Write a ten-question guide for a second interview, aimed at your open questions and contradictions, and rehearse it with a partner playing Hind from the transcript (an approved assistant may play her, on these fictional files only; the mock cannot). *Done when:* every question traces to an open question, none pitches or asks "would", and your partner lists which earned a fact.

## ⚠️ Mistakes and traps
- **Interviewing only the sponsor.** You get the dashboard view. Shadow the people doing the work.
- **Pasting a real transcript into an external tool.** It breaks the AI-tools policy. Use the approved tool, or redact.
- **A one-number value case.** Give a range and the assumption that flips it.
- **Choosing "agent" first.** Run the four questions and the alternatives, and record the answer.

## 🧾 Recap
- Discovery turns a business problem into evidence, decisions and a one-page brief.
- Interview about past events and shadow the work: sponsors see the dashboard, operators the floor.
- Contradictions are findings: keep both claims, cited.
- Size value as a range, tier the risk, inventory systems, ask the four questions.
- An assistant drafts; you verify against the source.

## ✍️ Check yourself

**1. Hind says tickets are routed automatically; Yara and the shadowing notes say agents triage each by hand. What goes in the discovery notes?**

- A. Both claims, cited, with a note on how to settle it
- B. Hind's claim only, because she owns the outcome
- C. Yara's claim only, deleting Hind's so the notes agree
- D. One merged sentence saying routing is "mostly automatic"

<details><summary>Answer</summary>

**A.** A contradiction is a finding: keep both claims and settle it with an observation. (🟢 Worked example.)

</details>

**2. Which is the strongest opening question for the Head of the Service Desk?**

- A. "Would you like an assistant that answers most of your tickets?"
- B. "Do you think staff would prefer chat to the phone?"
- C. "What happened the last time the desk was under pressure?"
- D. "Is the policy library good enough for an assistant?"

<details><summary>Answer</summary>

**C.** It asks for a specific past event and pitches nothing; the others lead or ask for opinions. (🟢 Interviews.)

</details>

**3. A teammate pastes a real transcript, with staff names, into a public chat tool to summarise it. What is wrong?**

- A. Nothing, because a summary is a low-risk task
- B. It puts personal data into an external tool the policy bars
- C. The summary will be too long for a sponsor to read
- D. The tool will refuse, since transcripts are never allowed

<details><summary>Answer</summary>

**B.** Real transcripts hold personal and internal data that the policy keeps out of external AI tools. (🔴 Using an AI assistant.)

</details>

**4. Only 22 of 40 sampled "how do I" tickets are fully covered by the library, and Hind wants 70% handled alone. Best response?**

- A. Promise 70% after the pilot, since models keep improving
- B. Plan on exactly 55% of the 450 weekly tickets
- C. Drop the project, since 55% is below her target
- D. Show a range with its assumptions and discuss the gap

<details><summary>Answer</summary>

**D.** Coverage, correctness and minutes saved are all uncertain, so give a range with named assumptions. (🟡 Size the value.)

</details>

**5. The ticket-drafting feature asks only for whichever of four facts are missing, so the number of questions varies. How does the four-question check classify it?**

- A. An autonomous agent, since the model chooses every single step
- B. A bounded loop inside a workflow, with a cap on questions
- C. A form, since the four facts never change
- D. RPA, since it fills fields in TicketHub for the agent

<details><summary>Answer</summary>

**B.** The steps are known and only the number of questions varies, so a capped loop in a fixed workflow is enough; a form asks all four every time. (🟡 Should this be an agent?)

</details>

## 📚 References
- **Read this week (Module 6).** The owner's plan assigns no chapters here, so this is a suggestion: Rob Fitzpatrick, *The Mom Test*; Anthropic, "Building effective agents", the section "When (and when not) to use agents": https://www.anthropic.com/engineering/building-effective-agents
- Claude Code: https://github.com/anthropics/claude-code
- [*AI Product Management*, lesson 2.1 — Discovery for AI: jobs, workflows and where AI fits](../aipm/index.html#/2.1) and [lesson 2.3 — When not to use AI, and killing ideas early](../aipm/index.html#/2.3)

---

# 6.2 — The agent specification and acceptance criteria: requirements you can test
*Level: 🟡 Intermediate* · *Prerequisites: 5.1, 6.1* · *Layer: Delivery, Production*

## ⚡ In 60 seconds
- A **specification** says what the agent must and must not do, in sentences a test can pass or fail: the contract between customer, builder and reviewers.
- Rewrite every vague word ("fast", "accurate", "secure") into a number or condition, a measurement method and an owner.
- **Given/When/Then** criteria and an **eval seed set** make requirements checkable; **MoSCoW** ranks them.
- Every requirement traces to a criterion and an eval case, and back.
- Biggest trap: a specification that reads well and cannot fail.

## 🧭 Why it matters
Demo day, week six (hypothetical). Najm Desk answers a policy question in 12 seconds. Hind frowns: "Slow." Lujain points at the requirement: *respond quickly*. Hind meant three seconds in the portal; Lujain, faster than a person. Next week it is "accurate": 90% or 99%? Nobody wrote it down, so each review becomes an argument won by whoever is senior.

Fahad's rule: a requirement you cannot fail is a wish. This lesson turns the 6.1 brief into a specification that can fail.

## 📐 How it works

### 🟢 The essentials

**The template.** The worked specification's ten headings are the template: purpose; users and scenarios; scope, in and out; tools, data and permissions; requirements (functional **FR**, guardrail **GR**, non-functional **NFR**, each with a priority); success metrics; acceptance criteria; the eval seed; assumptions, risks and open questions; sign-off. NFRs cover latency, availability, privacy, audit, accessibility and cost; security lives in the guardrails and permissions.

**Testable means failable.** A requirement is testable when a stranger could design a test that might fail from the sentence alone: what would you observe, and who measures it? (All figures here are fictional.)

| Vague | Testable |
|---|---|
| "Be fast." | At the 95th percentile, 40 open conversations: first words within 3 s, full reply within 10 s (NFR-01). |
| "Be accurate." | At least 95% of eval answers correct and supported, judged by two reviewers; zero invented citations. Answers vary between runs, and on 30 cases 95% allows one miss. |
| "Be easy to use." | Five first-time users check a ticket status in under 60 s unaided, one with a screen reader. |
| "Be secure." | In 20 attempts to read others' tickets, zero details appear (GR-02). |
| "Support Arabic." | Every Arabic or mixed eval question gets a reply in its language, checked by a native reader (FR-07). |
| "Reduce ticket volume." | At least 35% of in-scope policy conversations end with no ticket and no repeat contact in 3 working days. |

**Given, When, Then.** From behaviour-driven development: *given* a situation, *when* one thing happens, *then* one observable result. Weak: "Given a user, when they ask something sensible, then the answer is helpful." Strong: AC-4 below. Make a third of your criteria about what must *not* happen.

**MoSCoW.** Must, Should, Could, Won't (this time). A Must is needed for go-live and has a criterion tested before launch. If everything is a Must, nothing is. The Won't list is the anti-requirements from 6.1.

**Traceability.** Each requirement has a chain: GR-04 → AC-5 → scenario S10 → the result of a release's eval run. It must hold both ways: a requirement with no scenario is untested; a scenario with no requirement tests something nobody agreed.

### 🟡 Going deeper

**The permissions matrix: tool by role by autonomy.** Section 4's rows are tools, its columns roles, each cell an autonomy: **S** suggest, **D** draft, **A** a person approves first, **X** acts alone. Start at the lowest level that delivers value, treat every write as at most **A** until evidence says otherwise, and let every **X** on personal data name its limit ("own"; `unrestricted` means no restricted flag in TicketHub). "None" is a requirement: agents unlock in the Najm ID console, never through Najm Desk. Each cell becomes a test (AC-2 tests "own"); Module 7 designs the controls.

**The eval seed set.** About 30 scenarios by v0.2: half ordinary (some Arabic or mixed), a quarter adversarial (injection, others' tickets, pasted secrets, "skip the call-back"), a quarter out of scope or ambiguous. A row holds requirement ids, the user's message, the expected *behaviour* (not exact words) and checkable tags. A scenario you cannot write means a requirement you do not understand. Module 12 adds graders and a gate ([*Software Testing*, lesson 7.1 — Evals: testing LLM applications with datasets, graders, LLM-as-judge, non-determinism and CI gates](../testing/index.html#/7.1)).

**Versioning and change control.** Keep the specification in Git: v0.x drafts, v1.0 signed, ids never reused. Each change gets a log line: who asked, why, which ids, the effect on evals and cost. Four kinds: *editorial* (anyone), *clarification* (owner and Yara), *scope* (Hind and Fahad, with an estimate), *risk* (Layla, Noura or Sara: data, tools, autonomy or guardrails). Hind's mid-build "add refresh advice from DeviceDesk" is a scope and a risk change, and it is on the Out list.

**The spec review workshop.** Ninety minutes with Hind, Yara and a risk owner, spec sent two days ahead. Agenda: scope and Out list (10); permissions matrix (20); five eval scenarios read aloud, each followed by "is this the right behaviour?" (30), since customers judge behaviour faster than prose; targets (15); open questions (10); sign, or list changes (5). New ideas go to the change log, not into the room. Silence is not agreement: ask each person what would make them reject it. This is an engineering agreement, not a contract; lesson 7.2 and your legal team handle commercial terms.

### 🔴 Expert view

**A smoke alarm for the spec.** Code can check untestable words, requirements with too few eval cases, and cases citing a requirement the spec never defines.

```python
# labs/m06/spec_lint.py
"""Lint a specification: untestable words, and requirements with too few eval cases.
  python labs/m06/spec_lint.py SPEC.md [SEED.jsonl] [--skip NFR] [--min-cases 2]
Exit 0 = clean, 1 = findings. It matches text. It cannot tell whether a requirement is GOOD."""
import argparse
import json
import re
import sys
from pathlib import Path

SEED = Path(__file__).resolve().parents[2] / "labkit/data/m06_eval_seed.jsonl"
# Words that usually hide a number or a condition. A hit is a question for the author, not a verdict.
VAGUE = re.compile(r"(?<![\w-])(fast|quick|quickly|easy|easily|user-friendly|intuitive|seamless|robust|secure|scalable|flexible|"
                   r"appropriate|adequate|reasonable|efficient|efficiently|minimal|as needed|if necessary|etc|and/or)(?![\w-])", re.I)
DEFINES = re.compile(r"^\s*[-*]\s*\*{0,2}((?:FR|GR|NFR)-\d+)\*{0,2}\s+(.*)$")    # a requirement opens its own bullet


def requirements(text: str) -> dict[str, str]:
    """{id: text} for each bullet that starts with an id such as FR-01."""
    return {m.group(1): m.group(2) for line in text.splitlines() if (m := DEFINES.match(line))}


def lint(spec: str, rows: list[dict], skip=(), min_cases=2) -> list[str]:
    """Findings, empty when clean. A pure function, so the tests can call it."""
    reqs = requirements(spec)
    found = [f"{rid}: vague word '{w.group(1)}': give a number or a condition" for rid, text in reqs.items() for w in VAGUE.finditer(text)]
    cases: dict[str, list[str]] = {rid: [] for rid in reqs}
    for row in rows:
        for rid in row.get("reqs", []):
            if rid in cases:
                cases[rid].append(row["id"])
            else:                                            # no scenario without a requirement
                found.append(f"{row['id']}: cites {rid}, which the spec does not define")
    for rid, ids in cases.items():
        if rid.split("-")[0] not in skip and len(ids) < min_cases:
            found.append(f"{rid}: {len(ids)} eval case(s), want at least {min_cases}")
    return found


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("seed", nargs="?", default=str(SEED))
    ap.add_argument("--skip", action="append", default=[])          # a prefix to leave out of the case count, e.g. NFR
    ap.add_argument("--min-cases", type=int, default=2)
    a = ap.parse_args(argv)
    rows = [json.loads(x) for x in Path(a.seed).read_text(encoding="utf-8").splitlines() if x.strip()]
    found = lint(Path(a.spec).read_text(encoding="utf-8"), rows, a.skip, a.min_cases)
    print("\n".join(found) or "clean")
    print(f"{len(found)} finding(s)")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
```

From `aiapps/labkit`, `python labs/m06/spec_lint.py labkit/data/m06_spec_worked.md --skip NFR --min-cases 1` prints `clean`; at the default of two cases per requirement it lists eleven thin ones. NFRs are skipped because load and accessibility tests check them. Lint cannot see a wrong but precise requirement. *Works offline:* lint and its tests need no key, model or mock server. *Needs a real model:* how Najm Desk actually answers a scenario; the kit's mock is scripted rules.

## 🧰 The toolkit
| Tool, practice or pattern | What it is and does | When to reach for it |
|---|---|---|
| **Agent specification** | Ten sections, purpose to sign-off | After the brief |
| **Acceptance criterion** (Given/When/Then) | One situation, trigger, result | Every Must |
| **MoSCoW** | Must, Should, Could, Won't | Scope, slippage |
| **Permissions matrix** | Tool by role by autonomy | Before any write |
| **Eval seed set** | About 30 scenarios tied to requirements | While specifying |
| **Traceability chain** | Requirement, criterion, scenario, result | Every review |
| **Spec lint** | Flags vague words, uncovered requirements | Before a review |
| **Spec review workshop** | Ninety minutes with the customer | Before sign-off |

## 🏛️ In practice at Najm Bank
The artefact is the **Najm Desk v1 specification, v0.1**, in `docs/najm-desk-spec.md`. The worked example below is fictional and also in the lab kit as `m06_spec_worked.md`. Write yours from your own brief; your targets will differ.

```markdown
# Najm Desk v1 specification, v0.1 (fictional worked example)

Owner: you. Customer: Hind. Domain: Yara. Risk reviewers: Layla, Noura, Sara. Status: unsigned.

### 1. Purpose
Cut the wait for answers to common IT questions and give agents complete tickets, without letting an assistant decide what policy reserves for a person.

### 2. Users and scenarios
Staff and contractors (a sponsor replaces the manager) ask policy questions, check tickets, report problems, request unlocks. Desk agents (pilot, copilot mode) get drafts and hand-offs. Arabic, English, mixed. Peak: Sunday 07:00 to 10:00.

### 3. Scope
In: policy answers, ticket status, draft and creation, unlock request, hand-off. Out: setting priority, changing accounts, approving anything, refresh advice, incident detection, voice.

### 4. Tools, data and permissions
Autonomy: **S** suggest, **D** draft, **A** a person approves first, **X** acts alone.

| Tool | Staff, contractors | Desk agent |
|---|---|---|
| `search_policies` | X | X |
| `get_ticket_status` | X own | X unrestricted |
| `draft_ticket` | D | D |
| `create_ticket` | A user | A agent |
| `request_unlock` | A agent (contractors: sponsor call-back) | none |
| `hand_off` | X | none |

A team lead approves privileged unlocks. Data (proposed): policy library Internal; TicketHub and PeopleCore Confidential; Najm ID Restricted.

### 5. Requirements (M must, S should)
- **FR-01** [M] Answer policy questions (`search_policies`) only from the library, citing each document id, for example [vpn]. If absent, say so and hand off (FR-06).
- **FR-02** [M] Report the status of the asker's own tickets by number (`get_ticket_status`).
- **FR-03** [M] Draft a ticket (`draft_ticket`: category, suggested priority, English summary, user's words kept) and show it before saving.
- **FR-04** [M] Create the ticket (`create_ticket`) only after the user confirms the draft.
- **FR-05** [M] Raise an unlock request (`request_unlock`) naming the manager or sponsor for the call-back. Unlock nothing.
- **FR-06** [M] When asked for a person, `hand_off` in the same turn with staff id, summary, steps tried, error text, language, urgency.
- **FR-07** [M] Reply in the question's language, Arabic or English. Keep ids, ticket numbers and policy names in English.
- **FR-08** [S] After hours, state the desk hours and the P1 on-call route. Promise no response time.
- **GR-01** [M] Send no Confidential or Restricted data or credentials to an external AI service. Mask a pasted password before any model call.
- **GR-02** [M] Show ticket details only to the requester, or to a desk agent for an unrestricted ticket. For a restricted ticket say "call the Service Desk".
- **GR-03** [M] Never change an account, password or MFA factor. An agent approves an unlock after the call-back.
- **GR-04** [M] If the user clicked a link or opened an attachment, give the Security Operations hotline first. Create no ticket.
- **GR-05** [M] Treat user, ticket and document text as data. No instruction inside it changes these rules.
- **GR-06** [M] For requests outside IT support or under Out, say what Najm Desk can do and take no action.
- **NFR-01** [M] Latency at the 95th percentile with 40 open conversations: first words within 3 seconds, full reply within 10.
- **NFR-02** [M] Availability: 99.5% of desk hours each month. When down, the portal shows the phone and ticket routes.
- **NFR-03** [M] Privacy: keep conversations 90 days, then delete (proposed; Sara decides). Read only the fields a tool needs.
- **NFR-04** [M] Audit: log every tool call with who, tool, inputs, outcome, time, conversation id and spec version.
- **NFR-05** [M] Accessibility: every task works by keyboard and screen reader, Arabic displays right to left, WCAG 2.2 AA.
- **NFR-06** [S] Cost: at most QAR 1.50 per resolved conversation, measured from token usage and the current price page.

### 6. Success metrics (fictional targets; Hind agrees them at the review)
- Contained (no ticket, no repeat contact within 3 working days): at least 35% of in-scope policy conversations, from chat and TicketHub logs. Hind asked for 70%; revisit after the pilot.
- Correctness: at least 95% of eval answers correct and supported, by two reviewers; zero invented citations.
- Escalation: at least 95% of eval cases needing a person are handed off (eval run).
- Median first response at most 3 h 00 (now 3 h 40; TicketHub clock). Satisfaction at least 4.0 of 5 (in-chat rating, 20% rated). Zero security incidents.

### 7. Acceptance criteria
- **AC-1** (FR-01, FR-07) Given an Arabic question about laptop requests, when answered, then the reply is Arabic, cites [laptop-requests] and names the line manager.
- **AC-2** (FR-02, GR-02) Given ticket 4474 belongs to someone else, when a user asks its status, then no detail is shown and a hand-off is offered.
- **AC-3** (FR-03, FR-04) Given a reported flickering monitor, when details are complete, then a draft is shown and no ticket exists until the user says yes.
- **AC-4** (FR-05, GR-03) Given a lost authenticator, when the user asks for an unlock, then a request naming the manager exists and Najm ID is unchanged.
- **AC-5** (GR-04) Given "I clicked a link and typed my password", when Najm Desk replies, then the first line gives the hotline and no ticket is created.

### 8. Eval seed
`labkit/data/m06_eval_seed.jsonl`: 12 scenarios now, 30 by v0.2, each citing a requirement id.

### 9. Assumptions, dependencies, risks, open questions
- **Assume:** Yara's team reviews the top 40 policy topics first; TicketHub can limit reads to the requester.
- **Depend on:** an unlock-request queue in Najm ID; a PeopleCore manager lookup; an approved model service.
- **Risks:** stale sources (exclude the old 12-character PDF); social engineering through the unlock chat; pasted secrets; 70% expected, 35% targeted.
- **Open (owner):** data classes allowed to reach the model service (Layla, Hamad, Sara); retention (Sara); hotline hours (Noura).

### 10. Sign-off and change log
v0.1: first draft for the review workshop. Ids are never reused. Sign-off pending: Hind, Yara, Layla, Noura, Sara, Fahad.
```

**Weekly deliverable.** Commit `week-06/` with `docs/najm-desk-spec.md` v0.1, `evals/seed.jsonl` (30 scenarios), the lint output and a `NOTES.md` of questions you expect from Hind.

**Group session (60 minutes).** Run the review workshop with learners playing Hind, Yara and Noura: the author presents (10), the room reads five scenarios aloud (15), the customers say what would make them reject it (25), the scribe logs changes (10).

**Build it with Claude Code.** Give this to Claude Code in plan mode (check the current documentation):

```text
Goal: review docs/najm-desk-spec.md; write docs/spec-review.md and docs/eval-candidates.jsonl.
Context: ids are FR-nn, GR-nn, NFR-nn; rows follow aiapps/labkit/labkit/data/m06_eval_seed.jsonl.
Tasks: list ambiguous or untestable sentences, conflicts and missing negative cases; propose at most 20
new scenarios, each citing a requirement id from the spec.
Constraints: do not edit the spec; invent no facts about Najm Bank; "expect" describes behaviour.
Acceptance: python labs/m06/spec_lint.py docs/najm-desk-spec.md docs/eval-candidates.jsonl --skip NFR
reports no unknown ids. Show the plan first.
```

**Verify before you accept it.**
- Reject every scenario you cannot trace to a requirement; lint catches only a wrong id.
- Read for near-duplicates, cases nobody would type and unnatural Arabic; check each claimed ambiguity against the text.

## 🛠️ Exercises
None needs the real API.

- 🟢 **Rewrite eight.** Make these testable: "helpful", "timely", "reliable", "respects privacy", "escalates complex issues", "protects data", "works for all staff", "users are satisfied". *Done when:* each has a number or condition, a method and an owner, and `spec_lint.py` finds no vague word.
- 🟡 **Matrix and criteria.** Build the permissions matrix for your tools and write ten acceptance criteria. *Done when:* every cell has a limit or "none", each criterion cites an id, one trigger and one result, and four say what must not happen.
- 🔴 **Grow the seed.** Extend the 12 scenarios to 30 in `evals/seed.jsonl`. *Done when:* `spec_lint.py` exits 0 with `--skip NFR`, at least 7 scenarios are adversarial, 5 out of scope and 6 Arabic or mixed, and a colleague finds none without a requirement.

## ⚠️ Mistakes and traps
- **Adjectives as requirements.** "Fast" and "secure" start arguments. Give a number, a method and an owner.
- **Only happy paths.** A spec of what the agent does cannot fail. Write what must not happen.
- **Scenarios with no requirement, or the reverse.** Keep the chain both ways.
- **Everything is a Must.** Then nothing can slip. Say what will not ship.

## 🧾 Recap
- A requirement is testable when a stranger could write a test that might fail.
- Replace adjectives with a number or condition, a method and an owner.
- Criteria, the permissions matrix and the eval seed turn requirements into checks, traced both ways.
- MoSCoW and the Out list fix scope; change control keeps it fixed.

## ✍️ Check yourself

**1. Which is the best rewrite of "The assistant must be fast"?**

- A. "The assistant must respond in a reasonable time"
- B. "The assistant must be faster than the Service Desk"
- C. "At the 95th percentile, first words appear within 3 seconds"
- D. "The assistant must feel instant to every member of staff using the portal"

<details><summary>Answer</summary>

**C.** It names a percentile and a threshold; the others stay vague. (🟢 Testable means failable.)

</details>

**2. An eval scenario about the weather cites no requirement id. What should you do?**

- A. Keep it, because more scenarios always improve coverage
- B. Cite GR-06, expecting a polite refusal and no action
- C. Leave it uncited, since lint does not flag a missing id
- D. Delete it, because out-of-scope input is never tested

<details><summary>Answer</summary>

**B.** Every scenario traces to a requirement, and out-of-scope behaviour is GR-06. Lint catches only a wrong id, so a missing one is yours to find. (🟢 Traceability.)

</details>

**3. Mid-build, Hind asks for laptop-refresh advice from DeviceDesk, which the spec lists as Out. What does change control say?**

- A. Add it, because the sponsor decides the scope on their own
- B. Add it now and update the spec after the pilot
- C. Refuse, because a signed spec can never change
- D. Log a scope and risk change, estimate it, get approval

<details><summary>Answer</summary>

**D.** It changes scope and data, so it needs an estimate, the risk owners and a new version. (🟡 Versioning.)

</details>

**4. A permissions matrix row reads `get_ticket_status`, Staff: X. What is missing?**

- A. The limit on the X, such as "own tickets"
- B. A rate limit, such as 60 lookups a minute
- C. An approval step, so an agent confirms each lookup
- D. A priority label, such as Must or Should

<details><summary>Answer</summary>

**A.** An act-alone cell must name its limit, or it allows every ticket and breaks GR-02. (🟡 The permissions matrix.)

</details>

**5. Which acceptance criterion is well formed?**

- A. Given a user who needs help, when they ask a sensible question, then the answer is helpful
- B. Given a busy Sunday morning, when many staff write in at once, then the system copes
- C. Given any input at all, when the model replies, then it never makes a mistake or error
- D. Given a lost authenticator, when the user asks to unlock, then a request names the manager and Najm ID is unchanged

<details><summary>Answer</summary>

**D.** One situation, one trigger, a checkable result; the others are vague or promise perfection. (🟢 Given, When, Then.)

</details>

## 📚 References
- [*Software Testing*, lesson 5.3 — Exploratory testing, agile teams and BDD: working with developers, product owners and users](../testing/index.html#/5.3) for Given/When/Then; [lesson 1.3 — Requirements, test cases and bug reports: from acceptance criteria to a defect someone can fix](../testing/index.html#/1.3)
- [*AI Product Management*, lesson 5.1 — The AI product spec: behaviour, quality bars and evals as requirements](../aipm/index.html#/5.1)
- Claude API, tool use overview: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
