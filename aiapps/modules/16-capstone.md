# Module 16 — Hero: capstone and practice exam

*Every earlier module taught one skill on its own. This one asks you to use them all, in order, for a customer. Lesson 16.1 is the capstone: you take Najm Desk, the assistant for Najm Bank's IT Service Desk, from Hind's first request to a go-live decision in about four weeks. It gives you eight milestones with a customer gate at each, a repository checklist and layout, a rubric, a role-play guide for rehearsing the interviews, a go or no-go meeting, a final demo script and a retrospective, plus a small audit script that checks the evidence exists and links up. Lesson 16.2 is a 60-question practice exam across all seventeen modules, with a plan for turning your misses into study.*

> **Layer:** Delivery, Production — taking one engagement from discovery to go-live, and checking yourself with a 60-question exam.

---

# 16.1 — Capstone: take Najm Desk from discovery to go-live, with the customer
*Level: 🔴 Advanced* · *Prerequisites: Modules 0–15* · *Layer: Delivery, Production*

## ⚡ In 60 seconds
- The capstone takes one engagement, Najm Desk, through eight milestones (M1 to M8) in about four weeks. After each, the customer answers a gate question.
- Each milestone feeds the next: a requirement id in the specification reappears in an eval case, a UAT row and a runbook.
- Pick a **scope tier**: 🟢 core path, 🟡 with MCP and the evals gate, 🔴 with multi-agent and full governance. Finish a smaller tier with evidence.
- Decision cue: before each gate, write the question its owner will ask. If the artefact cannot answer it, stop.
- Biggest trap: treating the capstone as a build exercise. The code is one milestone of eight.

## 🧭 Why it matters
On Thursday Lujain demos her Najm Desk prototype: it answers policy questions and drafts tickets. Hind says, "Go live on Sunday." But nobody agreed a specification, and there is no eval set, so nobody can say whether Sunday's build is worse than Thursday's. Layla asks for the system card, Noura for the injection results, Maha for who is paged at 07:05.

Fahad: "A demo shows it can work. Go-live shows we know when it doesn't." In *Moffatt v. Air Canada* (2024) a tribunal held an airline responsible for what its chatbot told a customer. The capstone closes such gaps in order.

## 📐 How it works

### 🟢 The essentials
```text
Engagement brief: Najm Desk v1 (fictional)
Customer: Hind, Head of IT Service Desk (sponsor); Yara, team lead (domain expert).
Request: "Staff wait too long for a first answer. Give me an assistant for policy questions, ticket status
  and password problems, and a pilot before the end of next month."
Baseline (fictional): about 1,800 tickets a week; median first response 3 h 40 min; English and Arabic.
Constraints: no Confidential or Restricted data to external AI tools; every write needs a person or a policy
  gate; Layla, Noura, Hamad and Sara sign off before any pilot.
Systems: TicketHub, Najm ID, PeopleCore, DeviceDesk, the policy library. Timeline: about four weeks.
```

| Milestone (lessons) | You deliver | Gate question, and who answers | Week |
|---|---|---|---|
| **M1** discovery pack (6.1) | notes, stakeholder map, agent brief | Right problem? Hind | 1 |
| **M2** specification (6.2) | spec with ids, 30 seeds | Would my team recognise it? Yara | 1 |
| **M3** architecture and ADRs (7.1) | architecture, three ADRs | Design review answered? Layla, Noura, Maha | 2 |
| **M4** prototype and proposal (7.2) | demo, statement of work, rollout plan | What do I get, when? Hind signs | 2 |
| **M5** build with evals (Modules 1–5, 8–12) | prompt, tools, RAG, tests, 50-case eval | Better than last week? The eval gate | 2–3 |
| **M6** security review and governance pack (13.1, 13.2) | threat sheet, attacks, governance pack | Safe to trust? Risk owners sign | 3 |
| **M7** deployment and release (14.1, 14.2) | image, release checklist, cost sheet | Rollback in minutes? Maha | 3–4 |
| **M8** runbook, handover and go-live (15.1, 15.2) | runbooks, UAT, handover pack, go/no-go | Go or no-go? Hind | 4 |

Three rules apply. **Gate before step:** the owner answers in writing. **Ids thread through:** FR, GR, NFR and AC ids reappear in eval cases, UAT rows, runbooks and the cost sheet. **After M4, scope moves by change request:** an impact analysis, not a quick edit.

Scope tiers: 🟢 **Core path:** policy answers with citations, ticket status, draft and create with confirmation, unlock request, hand-off, two governance documents. 🟡 **MCP and evals gate:** adds a TicketHub MCP server (lesson 10.2) and a CI eval gate (lesson 12.2). 🔴 **Multi-agent and full governance:** adds a second agent if an ADR and an eval justify it (lesson 11.1), and all seven governance documents.

### 🟡 Going deeper
**The deliverables checklist and layout.** The tree is the checklist: docs, code, prompts, evals and CI, governance pack, deployment files, runbooks, handover pack. 🟡 and 🔴 mark what a larger tier adds.

```text
najm-desk/
├── README.md  CLAUDE.md  Dockerfile  deploy/release_checklist.yaml   M7
├── docs/
│   ├── discovery-notes  stakeholder-map  agent-brief               M1
│   ├── najm-desk-spec                                              M2
│   ├── architecture  adr/ (three or more)  (🔴 team-design-record) M3
│   ├── demo-script  proposal  rollout-plan                         M4
│   ├── threat-control-sheet  governance/ (two; 🔴 seven)           M6
│   ├── cost-and-reliability                                        M7
│   └── runbooks/  handover/  go-no-go  retrospective               M8
├── prompts/  src/najm_desk/ (🟡 ticket_server  🔴 team)  tests/
├── evals/  seed  cases  report  (🟡 baseline  gate)                M2, M5
└── .github/workflows/  (🟡 eval  release)                          M5, M7
```

The paths live in `labkit/data/m16_checklist.json`; edit them for your customer.

```python
# labs/m16/capstone_audit.py
"""Lab 16.1: audit a capstone repository. Is the evidence there, and does it link up?
  python labs/m16/capstone_audit.py REPO [--tier 1|2|3] [--strict]      strict: a leftover TODO is a problem
EXISTS: each deliverable in labkit/data/m16_checklist.json is present and not empty, milestone by milestone.
LINKED: each requirement id the spec defines is cited downstream, and no cited id is missing from the spec.
It cannot tell whether evidence is good, true or signed: that stays with people."""
import argparse
import json
import re
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
CHECKLIST = json.loads((KIT / "labkit" / "data" / "m16_checklist.json").read_text(encoding="utf-8"))   # milestone -> tier -> items
sys.path.insert(0, str(KIT / "labs" / "m13"))
import pack_check                                             # noqa: E402  Lab 13.2: the governance pack check

REQ = r"(?:FR|GR|NFR|AC)-\d+"                                 # ids as in lesson 6.2


def exists(repo: Path, tier: int, strict: bool) -> dict:
    """milestone -> problems, counting the items up to `tier`. A glob item needs at least `count` files."""
    report = {}
    for milestone, by_tier in CHECKLIST.items():
        problems = report[milestone] = []
        for t, items in by_tier.items():
            for item in items if int(t) <= tier else []:
                pattern, count = (item, 1) if isinstance(item, str) else item
                found = [p for p in sorted(repo.glob(pattern)) if p.is_file()]
                if len(found) < count:
                    problems.append(f"{pattern}: {len(found)} found, {count} needed")
                elif any(p.stat().st_size == 0 for p in found):
                    problems.append(f"{pattern}: an empty file")
                elif strict and any("TODO" in p.read_text(encoding="utf-8", errors="replace") for p in found):
                    problems.append(f"{pattern}: still has a TODO")
    return report


def linked(repo: Path):
    """(ids the spec defines that nothing downstream cites, ids cited downstream that the spec lacks)."""
    spec = repo / "docs" / "najm-desk-spec.md"
    if not spec.is_file():
        return [], []
    defined = set(re.findall(rf"^- \*\*({REQ})\*\*", spec.read_text(encoding="utf-8"), re.M))
    downstream = [p for p in [*repo.glob("evals/*.jsonl"), *repo.glob("docs/**/*.md")] if p != spec]
    cited = set().union(*[set(re.findall(rf"\b{REQ}\b", p.read_text(encoding="utf-8"))) for p in downstream])
    return sorted(defined - cited), sorted(cited - defined)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", type=Path)
    ap.add_argument("--tier", type=int, choices=(1, 2, 3), default=1)
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args(argv)
    problems = 0
    for milestone, issues in exists(a.repo, a.tier, a.strict).items():
        print(f"{milestone:40} {'fix' if issues else 'ok'}")
        for issue in issues:
            print("    " + issue)
        problems += len(issues)
    untraced, orphans = linked(a.repo)
    notes = [f"{i}: defined in the spec, cited nowhere downstream" for i in untraced]
    notes += [f"{i}: cited downstream, not defined in the spec" for i in orphans]
    if a.tier == 3:                                           # the seven-document pack is a tier 3 deliverable
        notes += ["governance: " + p for p in pack_check.check(a.repo / "docs" / "governance", structure_only=not a.strict)]
    print(*notes, sep="\n", end="\n" if notes else "")
    problems += len(notes)
    print(f"audit (tier {a.tier}{', strict' if a.strict else ''}): {problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
```

On the course's own worked specification, eval seed and UAT script it reports NFR-01, NFR-03, NFR-04 and NFR-06 as cited nowhere.

**The stakeholder role-play guide.** Each fictional composite hides things that surface only if you ask about a real past event.

| Persona | Opens with | Hides until you ask about the last time |
|---|---|---|
| **Hind**, sponsor | "Seventy percent, and never wrong." | the 2022 vendor bot had no route to a person; governance takes weeks |
| **Yara**, team lead | "Nobody finds the answers." | triage is by hand; the PeopleCore manager is wrong one time in ten |
| **Layla**, AI governance | "What can it do without a person?" | the committee meets every second Tuesday; no write tool without eval evidence |
| **Noura**, security | "What if a ticket gives it orders?" | attacks run with guards off and on; an unlock tool that only requests |

A weak question invites a number: "Wouldn't it be great if it resolved most tickets?" earned 70 percent and no evidence. A strong one asks for a story: "Tell me about the last time the desk was under pressure."

An **AI stakeholder simulator** is a model told to play one row. It is **practice only**: it agrees too easily, invents detail and knows nothing about your real Hind. Use it to find weak questions, never as a source. The same template, read-only in Claude Code, plays a sceptical reviewer of your repository:

```text
PRACTICE ONLY: you are a simulator, not the real person. Play <Hind|Yara|Layla|Noura> of Najm Bank (fictional).
Persona: <paste the row>.
Interview (chat): stay in character, answer in two to four sentences, reveal a hidden fact only when asked about
  a real past event, never for a leading question, and invent no numbers.
Review (Claude Code, plan mode, read-only): read docs/ and ask this person's three hardest go/no-go questions,
  each with the file and line that should answer it, or "no answer found".
Never write "approved" or edit a file. Then list the facts I missed and my weakest question.
```

### 🔴 Expert view
**The go or no-go meeting.** Forty-five minutes, chaired by Fahad; Hind decides; Layla, Noura, Hamad and Sara each hold a veto in their area.

```text
 5  Scope: changes since the proposal; change requests; written waivers
10  Quality: eval report against targets; critical cases; open defects
10  Safety: attack results with guards on; governance pack; any risk owner's objection
 8  Operations: rollback minutes; kill-switch drill; owned runbooks; cost per conversation
 5  Adoption: UAT by Yara's team; training; support model
 7  Decision: go, go with written conditions, or no-go and the date to meet again
```

Show evidence; do not describe it. A condition needs an owner and a date, and none overrides a veto. A no-go is a professional outcome: record in `docs/go-no-go.md` what would change it.

**The final demo script.** Twelve minutes on the release candidate, rehearsed twice; each step shows evidence for one claim.

1. The problem in Hind's (fictional) numbers.
2. A cited policy answer, in English and Arabic.
3. An unanswerable question: "I don't know", then a hand-off.
4. Your ticket's status; someone else's refused.
5. A drafted ticket; nothing saved until "yes".
6. An unlock request naming the manager; Najm ID unchanged.
7. Hidden instructions in ticket text ignored.
8. One real eval failure and the gate that caught it.
9. Kill switch off, degraded message, on.
10. Eval table, cost per conversation, open conditions.

**The rubric.** Pass means no Developing; distinction means Customer-ready in four or more.

| Criterion | Developing | Competent | Customer-ready |
|---|---|---|---|
| Discovery, spec, design | copied requirements; boxes only | contradictions found; ADRs with costs | hidden needs found; options rejected on evidence |
| Build and evals | demo path works | 50-case eval, gate | error analysis drives change |
| Security, release, operations | rules in the prompt; runs on a laptop | tool gate, attacks run; rollback rehearsed | pack checked by owners; kill switch drilled |
| Handover and judgement | a zip file | customer-run UAT | unaided task; honest go/no-go |

## 🧰 The toolkit
| Tool, practice or pattern | What it is and does | When to reach for it |
|---|---|---|
| **Milestone gate** | A question its owner answers in writing before the next step | Between milestones |
| **Capstone audit** | Checks deliverables exist and requirement ids are cited downstream | Before each gate |
| **Go/no-go record** | Decision, evidence, conditions with owners and dates | The last meeting |
| **Persona rehearsal** | Practice interviews with a simulated stakeholder | Before real meetings |

## 🏛️ In practice at Najm Bank
The artefact is the **Najm Desk capstone repository** (`najm-desk/`, above): yours, reviewed by Fahad at every gate, read by Hind at the end. The **reference-solution outline** says what a strong one decides, not how to build it:

- **M1:** five capabilities in, the rest out; contradictions cited by turn id (70% against the data, Arabic in v1, an unlock needs a call-back).
- **M2:** metrics with definitions; 30 seeds citing ids.
- **M3:** a workflow before an agent; ADRs for model tiers, retrieval, request-only write tools.
- **M4:** seven scenarios, one planned failure; password reset in the scope-out.
- **M5:** versioned prompt; 50 cases, some critical; a regression gate.
- **M6:** attacks fail with guards on; claims have evidence; signatures blank.
- **M7:** non-root pinned image; one manifest; rehearsed rollback.
- **M8:** owned runbooks; UAT run by Yara's team; conditions recorded.

**Your platform.** Before M3, note how identity reaches tools, where secrets and traces live, how deploys are approved and where data rests.

**Retrospective template.**

```text
Retrospective (within two weeks of closing): Najm Desk v1, <date>, <attendees>
1. Facts: planned and actual dates; gates passed first time; conditions at go.
2. Went well.  3. Surprised us.  4. Escaped defects: which gate missed each, the eval case added.
5. Decisions to reverse (new ADR).  6. Customer feedback.  7. One method change, owner and date.
```

**Presenting it as a portfolio piece.** Label it a course engagement. The README leads with the problem, the fictional baseline and the result, marking what you measured; then three ADRs, the eval table with its failures and the go/no-go record. Publish no real data, keys or names, and claim no production use. See [*From Graduate to Hired*, lesson 3.1 — Projects that prove you can do the job: one capstone spec per role](../career/index.html#/3.1) and [lesson 3.2 — Your GitHub, READMEs and writing about your work](../career/index.html#/3.2).

**Weekly deliverable.** Commit the repository at your tier, the strict audit output, the retrospective and a one-page portfolio README.

**Group session (60 minutes).** (1) Demo the release candidate from the script (20). (2) Role-play the go/no-go (40).

**Build it with Claude Code.** Give this in plan mode (check the current Claude Code documentation): spec, plan, small steps, verify, review the diff, commit.

```text
Goal: build the Najm Desk capstone at tier <1|2|3>, one milestone at a time, stopping at every gate.
Context: CLAUDE.md; the layout in lesson 16.1; docs/; labkit/data/m16_checklist.json; the labs of Modules 4 to 15.
Per milestone: read the last gate's answer; plan at most ten steps, each with the command that proves it, and wait;
  do one step, run it, show the diff; finish with labs/m16/capstone_audit.py and stop.
Constraints: invent no numbers, names, dates or approvals; every claim cites a file, test or command; never write
  "approved" in a sign-off row; no sampling parameters, prefill or forced tool_choice.
Do not: start the next milestone before I answer the gate; weaken a test or eval case; edit a signed document.
```

**Verify before you accept it.**
- Run the audit with `--strict` (a pass shows presence, not truth) and trace three ids by hand, from specification to runbook.
- Break it: weaken the prompt and watch the gate fail; delete an owner check and watch a test fail.
- Read `git log` and search the diff for secrets, `temperature`, `content[0]` and filled sign-off rows.

## 🛠️ Exercises
- 🟢 **Core path.** Offline on the mock (mechanics, not quality); a real eval run *needs the real API*. Build M1 to M8 at tier 1. *Done when:* the strict audit shows 0 problems, you traced three ids by hand, a peer playing Hind answered the M8 gate, and the retrospective is filled.
- 🟡 **With MCP and the evals gate.** *Needs the real API* and a spending cap. Add the MCP server and CI gate. *Done when:* the tier 2 audit passes, a weakened prompt fails the pull request, and the MCP scopes match the permissions matrix.
- 🔴 **Multi-agent and full governance.** *Needs the real API* and a human reviewer. *Done when:* the strict tier 3 audit passes; a second agent has an ADR and an eval showing it beats one (or is removed, with a reason); a colleague playing Layla signed or refused; `docs/go-no-go.md` records conditions.

## ⚠️ Mistakes and traps
- **Demo first, documents later.** A demo invites a date. Specify first.
- **Taking the simulator's word.** It is practice. Cite people in discovery notes.
- **One giant prompt to Claude Code.** Sixty files cannot be verified. Work in milestones.
- **Ticking boxes for people.** A green audit is not an approval. Signers sign.

## 🧾 Recap
- Eight milestones, a customer gate after each, answered in writing.
- Ids thread from specification to eval case, UAT row and runbook; the audit checks they exist and link.
- Choose the tier you can finish with evidence; later scope moves by change request. Rehearse with personas as practice only.
- Go or no-go needs evidence, conditions and owners; a risk owner's no stops the go.

## ✍️ Check yourself
**1. Lujain finishes the demo and wants to start building, but Hind has not signed the scope and rollout plan. What should Fahad insist on?**

- A. Build behind a feature flag and sign after the pilot
- B. Wait for Hind's written answer, then use change requests
- C. Build the safest capabilities now and sign at the go/no-go
- D. Build the core path and let Yara sign for Hind

<details><summary>Answer</summary>

**B.** The M4 gate is Hind's written answer on scope; later asks need change control. A and C delay it until the work is sunk cost; D lets the wrong person answer.

</details>

**2. Lujain's repository passes `capstone_audit.py --tier 2`. What has the audit shown?**

- A. The eval gate passes on the latest commit, so it can ship
- B. Each governance document is accurate and every owner approved it
- C. Every requirement has a passing test
- D. The files exist, are not empty, and every spec id is cited downstream

<details><summary>Answer</summary>

**D.** It checks presence and links only. It never runs the eval gate (A), never judges whether a document is true or signed (B), and "cited" is not "tested" (C).

</details>

**3. Lujain pastes an AI Hind's answers, praising every idea and agreeing that 70 percent is realistic, into `discovery-notes.md`. What is the right correction?**

- A. Keep them, because a model has seen many sponsors
- B. Make it disagree more, then cite it as Hind's view
- C. Remove them and interview Hind about a recent event
- D. Keep them, marked low confidence until Yara has confirmed them

<details><summary>Answer</summary>

**C.** A simulator agrees too easily and knows nothing about the real person, so it is practice, never a source. A, B and D still treat invented answers as evidence.

</details>

**4. At the go/no-go meeting the eval gate is green and the UAT passed, but Noura reports that two of ten injection attacks still succeed with guards on. Hind wants to go. What follows?**

- A. No-go on safety until both attacks fail
- B. Go, because Hind decides and the other areas are green
- C. Go, with a condition to fix both within the first month
- D. Go to a smaller audience while the fix is being built

<details><summary>Answer</summary>

**A.** A risk owner's "no" stops the go in that area, and no condition overrides it. Hind's decision (B) does not outrank a veto, and a smaller audience (D) changes exposure, not the hole.

</details>

**5. Lujain asks Claude Code to build the whole capstone in one prompt and gets sixty files and a green test run. What should she do first?**

- A. Merge it, since the tests pass and the files exist
- B. Split it into milestones, each with a plan and a gate
- C. Ask a second agent to review all sixty files before merging
- D. Add tests until every file is covered, then merge

<details><summary>Answer</summary>

**B.** Sixty files at once cannot be verified, and a green run shows only that the tests Claude Code wrote pass. A trusts them, C stacks one unverified opinion on another, and D chases coverage.

</details>

## 📚 References
- Claude Code documentation (from the Anthropic start page): https://docs.anthropic.com/; repository: https://github.com/anthropics/claude-code
- [*From Graduate to Hired*, lesson 2.2 — AI application engineer](../career/index.html#/2.2); [*System Design for Vibe Coders*, lesson 9.4 — Verification before completion](../vibe/index.en.html#l9-4)
- **Read this week (Module 16).** The course plan assigns no chapters to Module 16; its capstone closes the plan's last module, whose reading is under Module 14 (Grokking AI Applications, chapter 8; Gulli, chapter 16; Microsoft, lessons 15-17). Revisit chapters you skipped in lessons 1.1 to 15.1.

---

# 16.2 — Practice exam: 60 scenario questions
*Level: 🔴 Advanced* · *Prerequisites: Modules 0–16* · *Layer: Model, Applications, Agents, Delivery, Production*

## ⚡ In 60 seconds
- This is a 60-question practice exam covering every module from 0 to 16. Most questions are scenarios at Najm Bank. They are mixed, as in real work, not grouped by module.
- Take it in one sitting of about 90 minutes, which is 90 seconds a question. Closed book: no terminal, no search, no assistant. Write each answer and mark it "sure" or "guess" before you open any answer.
- Every answer ends with its Layer tag and the lesson to review, for example *(Agents · 8.2)*. Review by lesson tag: your misses are your study plan.
- Suggested reading of your score (the course's own guide, not a certification): 48 or more correct means you are ready to build for a customer; 36 to 47 means review the lessons you missed and redo their exercises; under 36 means work through the modules again.
- Decision cue: for each miss, write down why the wrong option tempted you. That reason is the habit to fix.
- Biggest trap: checking each answer as you go, or retaking the exam the next day. Both measure memory, not judgement.

## 🧭 Why it matters
Before Lujain's first customer engagement, Fahad asks her to sit the exam. She does well on Applications and Agents, and badly on Production. "That matches your prototype," he says. "You built a good agent and never asked what happens when it is wrong at 07:05 on a Sunday." Her misses share a pattern: when something fails she reaches for a better prompt or a bigger model, when the right answer was a check in code, an eval case or a runbook.

Real work does not ask you to define a token. It gives you a looping agent, a confident wrong answer or a nervous risk owner and asks what you do first. Most wrong options on a scenario exam are habits that sound reasonable, which is why they ship defects. Choosing the right layer to fix is the skill the exam measures.

## 📐 How it works

### 🟢 Question styles
Four options, one defensible answer, no "all of the above". The questions come in five styles:
- **Decision:** what do you do first, or next, in this situation?
- **Diagnosis:** which cause explains this symptom, and in which layer?
- **Evidence:** which eval, trace, log or test could fail, and so proves something?
- **Design:** which pattern, tool surface or control fits this requirement?
- **Trade-off:** which choice fits the cost, latency, autonomy and risk in the scenario?

### 🟡 Elimination
Read the last line first, then the scenario. Strike options that do not answer the question asked. Then watch for the shortcuts practitioners really take: a longer prompt, a bigger model, "lower the temperature" (which you mostly cannot set on current models), another agent, a rule in the system prompt used as a control, retry until it works, or an absolute word where a lesson says it depends. Compare the last two against the scenario's specifics: who is hurt, what evidence exists and who owns the decision.

> *Scenario:* Najm Desk cites a policy document it was never given. *Options, paraphrased:* lower the temperature; add "never invent citations" to the prompt; check each citation against the retrieved ids in code and withhold the answer; fine-tune on cited answers. *Elimination:* temperature is mostly not yours to set on current models and would not stop it; a prompt line is a request, not a control; fine-tuning is slow and unmeasured. Only the code check fails for the right reason.

### 🔴 Scenario reading
Ask four things of every stem. **Who is hurt, and how?** (Staff data, a wrong policy answer, an unconfirmed write, a bill.) **Which layer failed?** (The model call, the application around it, the agent loop, the delivery work or production.) **What is the cheapest control that can fail for the right reason?** (A code check, an eval case, a trace field.) **What word limits the answer?** ("First", "best", "most likely", "before".) Do not assume facts the stem does not give.

The five Layer tags map to the course like this. A lesson with two tags counts under the tag in the answer line. Use the table to tally your misses.

| Layer tag | Lessons that carry it | Mostly | Your misses |
|---|---|---|---|
| Model | 0.2, 1.1, 1.2 | Modules 0 and 1 | |
| Applications | 2.1, 2.2, 3.1, 3.2, 4.1, 4.2, 5.1, 5.2 | Modules 2 to 5 | |
| Agents | 1.2, 3.2, 7.1, 8.1 to 11.2, 12.1, 13.1 | Modules 8 to 11 | |
| Delivery | 0.1 to 0.3, 2.2, 6.1 to 7.2, 10.2, 12.1 to 12.2, 13.2 to 14.2, 15.2, 16.1 | Modules 6, 7, 12, 14 and 15 | |
| Production | 5.2, 6.2, 8.2, 9.2, 12.2, 13.1 to 15.1, 16.1 | Modules 13 to 15 | |

## 🧰 The toolkit
| Tool, practice or pattern | What it is and does | When to reach for it |
|---|---|---|
| **Confidence marking** | Writing "sure" or "guess" beside each answer before checking | Every practice exam; it exposes lucky guesses and false certainty |
| **Miss log** | A table of each wrong or guessed answer with its Layer tag, lesson and type of error | Straight after scoring; it becomes your study plan |

## 🏛️ In practice at Najm Bank
Fahad keeps one rule: no lesson with two or more misses is left without a dated action, and nobody retakes the exam within two weeks. Three rows of Lujain's **miss log** show the template:

| Question | Layer · lesson | My answer (confidence) | Type of error | Action and date |
|---|---|---|---|---|
| 14 | Production · 13.1 | A (sure) | Tempted: a "never reveal" rule in the system prompt | Reread 13.1; redo the attack run with one layer skipped, Friday |
| 31 | Delivery · 12.2 | C (guess) | Did not know why a gate compares like with like | Reread 12.2; redo the gate drill, Monday |
| 47 | Agents · 8.1 | B (sure) | Tempted: raise the step cap instead of finding the stop reason | Reread 8.1; redo its exercise, next Wednesday |

Then she writes the plan from the pattern, not from single questions. A wrong "sure" goes first, because it is a belief she would act on at work. Copy this template:

| Layer tag | Misses | Reread | Redo | By |
|---|---|---|---|---|
| Production | 2 | 13.1, 15.1 | the attack run with one layer skipped; the kill-switch drill | Friday |
| Delivery | 1 | 12.2 | the gate drill | next Monday |
| Retake | | | the whole exam, closed book | in two weeks |

## 🛠️ Exercises
- 🟢 **Review your misses.** Tally every wrong or guessed question by Layer tag in the table above and label each "did not know", "misread" or "tempted". *Done when:* you can name your two weakest tags and the habit behind each, and every miss has a lesson to reread.
- 🟡 **Write five questions of your own.** Choose your weakest tag. Write five scenarios in the exam's format, each with one defensible answer, three tempting wrong ones and an explanation that ends with its tag and lesson. *Done when:* a peer has answered all five, every disagreement is settled in your explanation, and the correct option is not always the longest.
- 🔴 **Teach one lesson.** Teach the lesson behind your weakest tag to a peer in 20 minutes, with one failing-then-passing run from the lab kit. *Done when:* the peer can state the lesson's main rule and one weak-versus-strong pair in their own words, and you have redone anything you could not answer.

## ⚠️ Mistakes and traps
- **Checking answers as you go.** You learn one answer and lose the measure of the rest. Answer all 60, then check.
- **Counting only the score.** A good score with many guesses hides gaps. Review guesses as if they were misses.
- **Rereading instead of practising.** An explanation fixes one answer; the lesson's exercise builds the judgement. Redo it.
- **Treating this as a certification mock.** It follows this course, not any exam syllabus. Use an issuer's own guides for a certificate.

## 🧾 Recap
- Sit the exam closed book in one go, and mark every answer "sure" or "guess".
- Read each stem for who is hurt, which layer failed, the cheapest control and the limiting word.
- Log every miss by Layer tag, lesson and type of error: did not know, misread or tempted.
- Redo the exercises for your weakest lessons, then retake the exam after at least two weeks.

## ✍️ Practice exam

@@EXAM@@

## 📚 References
- Anthropic developer documentation (start page): https://docs.anthropic.com/; Claude API, Models overview: https://platform.claude.com/docs/en/about-claude/models/overview; lab kit: https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/aiapps/labkit
- Other practice exams in the library: [*Software Testing*, lesson 8.3 — Practice exam: 60 scenario questions](../testing/index.html#/8.3); [*Secure AI & Application Security*, lesson 12.3 — Practice exam: 60 scenario questions](../secai/index.html#/12.3); [*AI Product Management*, lesson 10.3 — Practice exam: 60 scenario questions](../aipm/index.html#/10.3)
