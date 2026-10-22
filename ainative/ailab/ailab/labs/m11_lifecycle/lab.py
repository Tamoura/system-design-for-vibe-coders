"""Lab m11 (lesson 11.2): "An ADR with a critic, docs checked against code and a postmortem that sticks to the facts".

The story
---------
Three documents are overdue at the Payments Platform team. The learner writes (1) an ADR for a decision the
code already embodies, with a critic's objections recorded, (2) the najmkit reference page, regenerated from the
code and VERIFIED against it, and (3) a postmortem for a constructed incident, drafted from ``lab-assets/incident.json``.
The point is not the prose. The point is that every claim in each document can be traced to a source, and
that an AI assistant, left alone, invents the claims that cannot.

What the seed does
------------------
* deletes ``docs/najmkit.md`` ("lost in the docs migration", AUTHORING.md decision 5);
* plants one stale docstring in ``src/najmkit/audit.py`` (``read_events`` claims a missing file raises; the code
  returns ``[]``), the kind of comment an assistant will copy into the docs;
* ``assets/`` adds the incident record, an ADR template, a postmortem template and ``claims_scan.py``.

What the grader can and cannot tell
-----------------------------------
It CAN find claims that contradict the code or the record: a name that does not exist, a signature that does
not fit, an example that fails, a number or time that is in neither the record nor derivable from it, a cause
stated as fact. It CANNOT tell whether the prose is good, whether the ADR's decision is wise, whether a real AI
critic produced the objections, or whether a false sentence that no rule anticipates slipped through. That is why
the lesson teaches the Claims check as a human routine and not only as a grader.

All the real work is in ``ailab/checks_m11.py`` (a new helper; the shared ``checks.py`` is untouched).
The answer key (event anchors, forbidden claims, the gaps in the record) lives in ``hidden/answer_key.json``.
The record the grader reads is the kit's own copy, never ``lab-assets/incident.json`` in the learner's directory.
"""
from __future__ import annotations

import json
from pathlib import Path

from ailab import checks, checks_m11 as m, framework, gitutil
from ailab.framework import Check, Lab

HERE = Path(__file__).resolve().parent

NAJMKIT_PAGE = "docs/najmkit.md"
POSTMORTEM = "docs/postmortems/INC-2031.md"
DOCSTRING_FILE = "src/najmkit/audit.py"
DOCSTRING_OK = "Missing file -> []."
DOCSTRING_STALE = "A missing file raises FileNotFoundError."


def _key() -> dict:
    return json.loads((HERE / "hidden" / "answer_key.json").read_text(encoding="utf-8"))


def _record() -> m.Record:
    return m.load_record(HERE / "assets" / "incident.json")


# ---------------------------------------------------------------------------------------------
# seed
# ---------------------------------------------------------------------------------------------
def seed(work: Path) -> None:
    """Lose the najmkit page and plant one stale docstring (both strict edits: a changed base fails loudly)."""
    framework.remove_file(work, NAJMKIT_PAGE)
    framework.edit_file(work, DOCSTRING_FILE, DOCSTRING_OK, DOCSTRING_STALE)


# ---------------------------------------------------------------------------------------------
# grade
# ---------------------------------------------------------------------------------------------
def _check(name: str, problems: list[str], hint: str, ok_detail: str = "", *, required: bool = True, show: int = 3) -> Check:
    if problems:
        extra = f" (+{len(problems) - show} more)" if len(problems) > show else ""
        return Check(name, False, "; ".join(problems[:show]) + extra, hint, required)
    return Check(name, True, ok_detail, "", required)


def _waiting(name: str, what: str, hint: str, *, required: bool = True) -> Check:
    return Check(name, False, f"waiting for {what}", hint, required)


# -- part 1: the ADR --------------------------------------------------------------------------
def adr_checks(work: Path, index: m.CodeIndex) -> list[Check]:
    names = ["ADR exists in docs/adr/", "ADR follows Nygard's format", "ADR facts trace to the code",
             "ADR records the critic's objections"]
    path = m.find_adr(work)
    if path is None:
        return [Check(names[0], False, "no file like docs/adr/0001-short-title.md",
                      "Create docs/adr/0001-<short-title>.md (start from lab-assets/adr-template.md)."),
                *[_waiting(n, "the ADR file", "Write the ADR first (part 1 of TASK.md).") for n in names[1:]]]
    text = m.read(path) or ""
    shown = path.relative_to(work).as_posix()
    unresolved, resolved, in_src = m.adr_references(text, index)
    fact_problems = [f"`{t}` points at nothing" for t in unresolved] + m.adr_fact_problems(text)
    if not fact_problems and (resolved < 2 or in_src < 1):
        fact_problems.append(f"only {resolved} reference(s) to the code resolve, {in_src} into src/ (at least 2, and 1 into src/)")
    return [
        Check(names[0], True, shown),
        _check(names[1], m.adr_format_problems(text),
               "Use the headings Status, Context, Decision and Consequences in that order, and name a downside (lab-assets/adr-template.md)."),
        _check(names[2], fact_problems,
               "Check every `path` and `module.name` with ls or grep (python lab-assets/claims_scan.py <file> does the lookup), and check numbers against the code, not against docs/ARCHITECTURE.md.",
               f"{resolved} references resolve"),
        _check(names[3], m.adr_critic_problems(text),
               "Add a section 'Critic's objections': at least three objections, each with what you did about it (accepted, rejected with a reason, deferred)."),
    ]


# -- part 2: the najmkit page -----------------------------------------------------------------
def docs_checks(work: Path, index: m.CodeIndex) -> list[Check]:
    names = ["najmkit page exists (docs/najmkit.md)", "Docs: every name exists in the code", "Docs: signatures match the code",
             "Docs: the examples run", "Docs: the public API is covered", "Docs: nothing contradicts the code"]
    text = m.read(work / NAJMKIT_PAGE)
    if text is None:
        return [Check(names[0], False, f"{NAJMKIT_PAGE} does not exist",
                      "Write docs/najmkit.md from the code in src/najmkit/ (part 2 of TASK.md)."),
                *[_waiting(n, "the najmkit page", "Write the page first.") for n in names[1:]]]
    out = [Check(names[0], len(text.split()) >= 150, f"{len(text.split())} words" if len(text.split()) >= 150 else "the page is almost empty",
                 "Document every public function and class of ids, clock and audit.")]
    out.append(_check(names[1], m.docs_name_problems(text, index),
                      "Open src/najmkit/ and look the name up. If grep cannot find it, the page must not mention it."))
    out.append(_check(names[2], m.docs_signature_problems(text, index),
                      "Copy the parameters from the def line in the code, not from memory or from a docstring."))
    failures, ok_by_module, tried = m.run_doc_examples(work, text)
    missing = [mod for mod, n in ok_by_module.items() if n == 0]
    example_problems = list(failures)
    if not failures and missing:
        example_problems.append("no example that runs for: " + ", ".join(f"najmkit.{x}" for x in missing)
                                + (f" ({tried} Python statements tried)" if tried else " (no Python examples found)"))
    out.append(_check(names[3], example_problems,
                      "Put at least one runnable Python example per module in a ```python block, with its imports, and run it yourself.",
                      f"{sum(ok_by_module.values())} statements ran"))
    covered, total, not_covered = m.docs_coverage(text, work)
    cover_problems = [f"{covered} of {total} public names are documented; missing: {', '.join(not_covered[:5])}"] if covered < total - 1 else []
    out.append(_check(names[4], cover_problems, "List every public function and class of the three modules (src/najmkit/*.py).",
                      f"{covered} of {total} names"))
    out.append(_check(names[5], m.docs_fact_problems(text, m.read_facts(work)),
                      "Run the code and look. A docstring or a comment is a claim too; if it disagrees with what the code does, the code wins "
                      "(put the disagreement under 'Known problems')."))
    return out


# -- part 3: the postmortem -------------------------------------------------------------------
def postmortem_checks(work: Path) -> list[Check]:
    names = ["Postmortem has all its sections", "Postmortem: every timeline row matches the record",
             "Postmortem: the timeline covers the key events", "Postmortem: no invented numbers, times, dates or ids",
             "Postmortem: nothing unknown is stated as fact", "Postmortem: inferences are labelled, open questions listed",
             "Postmortem: blameless wording"]
    text = m.read(work / POSTMORTEM)
    if text is None:
        return [Check(names[0], False, f"{POSTMORTEM} does not exist",
                      "Write docs/postmortems/INC-2031.md from lab-assets/incident.json (part 3 of TASK.md)."),
                *[_waiting(n, "the postmortem", "Write the postmortem first.", required=(i < 5)) for i, n in enumerate(names[1:])]]
    record, key = _record(), _key()
    sections = m.postmortem_sections(text)
    section_problems = m.postmortem_section_problems(sections)
    if m.action_item_count(sections.get("actions")) < 3 and "actions" in sections:
        section_problems.append("fewer than 3 action items")
    out = [_check(names[0], section_problems,
                  "Use the headings of lab-assets/postmortem-template.md: Summary, Impact, Timeline, What we know, What we infer, "
                  "What we do not know, Action items.")]
    timeline = sections.get("timeline")
    if timeline is None:
        out += [_waiting(names[1], "a Timeline section", "Add the Timeline table."),
                _waiting(names[2], "a Timeline section", "Add the Timeline table.")]
    else:
        row_problems, covered, rows = m.timeline_problems(timeline.full, record, key)
        if rows == 0:
            row_problems = ["no timeline rows found (each row starts with a time like 10:11)"]
        out.append(_check(names[1], row_problems,
                          "For each row: take the time and the event id from lab-assets/incident.json, and say what that event says.",
                          f"{rows} rows checked"))
        missing_required = [e for e in key["required_events"] if e not in covered]
        cover = []
        if len(covered) < key["min_events"]:
            cover.append(f"{len(covered)} of the record's {len(record.events)} events are in the timeline (at least {key['min_events']} expected)")
        if missing_required:
            cover.append("key events missing: " + ", ".join(missing_required))
        out.append(_check(names[2], cover, "A timeline with gaps hides what happened. Cover the start, the detection, the recovery and the check that no money was lost.",
                          f"{len(covered)} events"))
    non_action = m.section_texts(sections, ("summary", "impact", "timeline", "facts", "inferences", "unknowns"))
    checked_text = m.preamble(text) + "\n" + non_action
    invented = m.invented_facts(checked_text, record) + m.invented_people(checked_text, record)
    out.append(_check(names[3], invented,
                      "Every number, time, date, id and name must come from the record (or be a difference of its times or counts). "
                      "python lab-assets/claims_scan.py <file> --record lab-assets/incident.json finds times and ids that are not in it."))
    facts_text = m.section_texts(sections, ("summary", "impact", "timeline", "facts"))
    out.append(_check(names[4], m.forbidden_problems(facts_text, key),
                      "If the record does not say it, it is not a fact. Move it to 'What we infer' (with what it rests on and what would confirm it) or to 'What we do not know'."))
    label_problems = m.inference_problems(sections.get("inferences")) + m.unknown_problems(sections.get("unknowns"), key)
    out.append(_check(names[5], label_problems,
                      "Each inference: what it rests on (an event id), how confident you are, what would confirm it. Open questions: what no event in the record can answer."))
    blame = m.blame_problems(non_action)
    out.append(_check(names[6], blame, "Describe what happened and what the system allowed; leave out fault and carelessness.", required=False))
    return out


# -- hygiene ------------------------------------------------------------------------------------
def hygiene_checks(work: Path) -> list[Check]:
    return [
        checks.files_changed_within(work, ["docs/**"], name="Only documentation changed",
                                    hint="This ticket is documentation only. Revert code, tests and lab-assets (git restore <file>)."),
        checks.commit_count(work, at_least=3, name="Three documents, three commits",
                            hint="Commit each document on its own, so each commit can be reviewed alone."),
        checks.conventional_commits(work),
        checks.all_committed(work),
        checks.no_secrets(work),
    ]


def grade(work: Path) -> list[Check]:
    index = m.CodeIndex(work)
    return [*adr_checks(work, index), *docs_checks(work, index), *postmortem_checks(work), *hygiene_checks(work)]


# ---------------------------------------------------------------------------------------------
# solve
# ---------------------------------------------------------------------------------------------
def solve(work: Path) -> None:
    """Write the three reference documents and commit each one on its own (solution/commits.json)."""
    plan = json.loads((HERE / "solution" / "commits.json").read_text(encoding="utf-8"))
    for n, step in enumerate(plan):
        for rel, source in step["files"].items():
            framework.write_file(work, rel, (HERE / "solution" / source).read_text(encoding="utf-8"))
        gitutil.commit_all(work, step["message"], author=("Najm Learner", "learner@najm.example"),
                           date=f"2026-03-12T1{n}:00:00+00:00")


LAB = Lab(
    id="m11",
    title="An ADR with a critic, docs checked against code and a postmortem that sticks to the facts",
    lesson="11.2",
    needs_agent=False,  # recommended, not required: the grader only looks at the result
    seed=seed,
    grade=grade,
    solve=solve,
)
