"""Lab m14 (lesson 14.1): "Capstone: take a change to Najm Remit through the full AI-native cycle".

The story
---------
Hessa's ticket REMIT-414 opens a Bangladesh corridor, ``QAR-BDT``: its own fee schedule (STD-C), a rate and a margin,
a per-transfer minimum and maximum, and a confirmation message of its own in English and Arabic. The numbers are all
in the ticket, because hidden tests cannot guess them. The change is small on purpose. What the capstone grades is
everything around it: the memory file, a spec and a plan written before the code, tests traced to the spec, one
decision record, review notes on the learner's own diff, hardened settings with a guard hook, documents that stay
true, an agent log and a retrospective, all in small commits that follow CONTRIBUTING.md.

What the seed plants
--------------------
Nothing. The base repository already is the starting situation (the BDT corridor is absent on purpose, G-BDT in
KIT_NOTES.md). ``TASK.md`` and ``lab-assets/`` (the templates, Hessa's meeting notes, a baseline guard hook and
settings file) are added by the framework.

What the grader checks, and what it cannot
------------------------------------------
Code: the visible tests, five groups of hidden acceptance tests (the corridor, the fee schedule, the rate and
quote, the wording, and the whole send path with the KYC limits, the ledger and the command line), existing tests
untouched, only the expected files changed, the learner's new tests failing without the change and noticing six
deliberate defects (at least four). A test that asserts nothing, or checks only that the corridor exists, notices none.
Evidence: each document exists, has the template's sections, has no TODO placeholder left, and *refers* to the others:
the plan covers every acceptance criterion of the spec, the tests name them, the corridors page matches the code, the
review names the files that changed, the retrospective quotes the agent log's total and one of the learner's commits.
The rules the grader enforces are listed for the learner in ``assets/README.md`` and in the templates.
Hygiene and security: Conventional Commits, one kind of change per commit, no secrets, no float or clock shortcuts,
no new dependency, no local data, a hook that really blocks (run on sample inputs in a subprocess).
It cannot tell whether the spec is wise, the review honest, the agent log true or the retrospective sincere: those
are for the group session. Advisory checks look at habits (tests before or with the code, a plan the history follows,
small commits, a guard that sees through wrappers, ask rules for the money files).
"""
from __future__ import annotations

from pathlib import Path

from ailab import checks, checks_m14 as m14, framework, gitutil
from ailab.framework import Check, Lab

HERE = Path(__file__).resolve().parent
SOLUTION = HERE / "solution"
LEARNER = ("Najm Learner", "learner@najm.example")
MIN_COMMITS = 8
TIMEOUT = 40.0  # seconds per pytest run; a real run takes about one

# (hidden test module, check name, hint)
PARTS = [
    ("test_m14_corridor", "Corridor: code, minimum, maximum and delivery",
     "Compare the corridor with the table in the ticket. Is each limit inclusive, and does one cent outside it fail?"),
    ("test_m14_fees", "Fees: the STD-C schedule",
     "Work three amounts out by hand (the minimum, a tier edge, the cap), then compare them with `PYTHONPATH=src python -m remit quote QAR <amount> BDT` once the corridor exists."),
    ("test_m14_fx", "Rate, margin and the 60-second quote",
     "Multiply the mid rate by one minus the margin, round half up to four places, and check the other corridors did not move."),
    ("test_m14_notify", "Wording in English and Arabic",
     "Compare your template with the ticket, word for word, in both languages. Arabic amounts use Arabic digits."),
    ("test_m14_together", "Quote, send, ledger, KYC limits and the command line",
     "Send from each kind of customer (English T2, Arabic T3, a T1 at the daily limit) and read what was stored, posted and said."),
]


def seed(work: Path) -> None:
    """Nothing to plant: the base repository, without the BDT corridor, is the starting situation."""


# ---------------------------------------------------------------------------------------------
# grade
# ---------------------------------------------------------------------------------------------
def grade(work: Path) -> list[Check]:
    files = m14.repo_files(work)
    _, spec_ids = m14.spec_info(work)
    hidden = checks.run_hidden_pytest(work, HERE / "hidden", args=["--continue-on-collection-errors"], timeout=TIMEOUT)
    return [
        # -- 1. the change itself -------------------------------------------------------
        checks.tests_pass(work, name="Your tests pass", timeout=TIMEOUT),
        *[m14.hidden_part(hidden, module, name, hint) for module, name, hint in PARTS],
        m14.tests_not_weakened_check(work),
        m14.new_tests_fail_on_starter(work),
        m14.teeth_check(work),
        checks.files_changed_within(
            work, m14.ALLOWED_TO_CHANGE, name="Only the expected files changed",
            hint="The ticket needs corridors.py, fees.py, fx.py, notify.py and service.py, new tests, documents and agent configuration. "
                 "Undo the rest with git restore --source=lab-start <file>, and keep throwaway scripts outside the repository."),
        # -- 2. the evidence around it --------------------------------------------------
        m14.memory_check(work, files),
        m14.spec_check(work),
        m14.plan_check(work, spec_ids, files),
        m14.tests_trace_check(work, spec_ids),
        m14.adr_check(work, files),
        m14.review_check(work, files),
        m14.settings_check(work),
        m14.hook_check(work),
        m14.corridors_doc_check(work),
        m14.architecture_check(work),
        m14.agent_log_check(work, files),
        m14.retro_check(work, files),
        # -- 3. hygiene and security ----------------------------------------------------
        checks.all_committed(work, name="Everything is committed"),
        checks.conventional_commits(work, min_commits=MIN_COMMITS),
        m14.one_thing_per_commit_check(work),
        checks.no_secrets(work),
        m14.forbidden_constructs_check(work),
        m14.dependencies_check(work),
        m14.local_data_check(work),
        # -- 4. habits (advisory) -------------------------------------------------------
        m14.tests_first_check(work),
        m14.plan_vs_history_check(work),
        m14.small_commits_check(work),
        m14.hook_check(work, harder=True),
        m14.ask_for_money_files_check(work),
    ]


# ---------------------------------------------------------------------------------------------
# solve: the reference solution, done the way the lab asks (documents first, tests first, small commits)
# ---------------------------------------------------------------------------------------------
def _stamp(step: int) -> str:
    return f"2026-03-02T{10 + step // 60:02d}:{step % 60:02d}:00+00:00"


def solve(work: Path) -> None:
    """Spec, plan, memory, hardening, tests, then the five code steps in dependency order, then documents.

    The code patches in ``solution/`` were produced by making the changes by hand in this order. The retrospective
    quotes a real commit of this very history and the real total of the agent log.
    """
    step = 0

    def commit(message: str) -> None:
        nonlocal step
        step += 7
        gitutil.commit_all(work, message, author=LEARNER, date=_stamp(step))

    def put(source: Path, rel: str, **fill: str) -> None:
        text = source.read_text(encoding="utf-8")
        for key, value in fill.items():
            text = text.replace("{" + key + "}", value)
        framework.write_file(work, rel, text)

    harden = HERE / "assets" / "harden"
    # 1. the documents that come before any code
    put(SOLUTION / "spec.md", m14.SPEC)
    commit("docs(specs): specify the Bangladesh corridor for REMIT-414")
    put(SOLUTION / "plan.md", m14.PLAN)
    commit("docs(specs): plan the Bangladesh corridor in small steps")
    # 2. the agent's working conditions
    put(SOLUTION / "CLAUDE.md", "CLAUDE.md")
    commit("chore(claude): add project memory with the corridor checklist")
    put(harden / "settings.json", m14.SETTINGS)
    put(harden / "guard.py", m14.GUARD)
    (work / m14.GUARD).chmod(0o755)
    commit("chore(claude): harden permissions and add a guard hook")
    # 3. tests first, then the code, providers before the consumer
    put(SOLUTION / "test_bdt_corridor.py", "tests/test_bdt_corridor.py")
    commit("test(corridors): pin the Bangladesh corridor, fees, rate and wording")
    for patch, message in [
        ("01_fees.patch", "feat(fees): add the STD-C fee schedule for Bangladesh"),
        ("02_fx.patch", "feat(fx): add the BDT mid rate and margin"),
        ("03_corridor.patch", "feat(corridors): open the QAR-BDT corridor"),
        ("04_notify.patch", "feat(notify): add the transfer_sent_bdt wording"),
        ("05_service.patch", "feat(service): send the Bangladesh wording on QAR-BDT transfers"),
    ]:
        gitutil.apply_patch(work, SOLUTION / patch)
        commit(message)
    # 4. the documents that describe what was built
    put(SOLUTION / "adr.md", f"{m14.ADR_DIR}/0001-own-fee-schedule-for-bangladesh.md")
    commit("docs(adr): record why Bangladesh gets its own fee schedule")
    put(SOLUTION / "corridors.md", m14.CORRIDORS_DOC)
    gitutil.apply_patch(work, SOLUTION / "06_architecture.patch")
    commit("docs(docs): add the corridors page and fix the architecture notes")
    put(SOLUTION / "review.md", m14.REVIEW)
    commit("docs(review): review the REMIT-414 diff")
    put(SOLUTION / "agent-log.md", m14.AGENT_LOG)
    commit("docs(docs): log the agent sessions for REMIT-414")
    # 5. the retrospective cites a real commit of this history and the log's real total
    fx_commit = next(c for c in gitutil.commits_since(work) if c.subject.startswith("feat(fx)"))
    total = m14.total_minutes((work / m14.AGENT_LOG).read_text(encoding="utf-8"))
    put(SOLUTION / "retrospective.md", m14.RETRO, HASH=fx_commit.sha[:9], TOTAL=str(total))
    commit("docs(docs): write the retrospective for REMIT-414")


LAB = Lab(
    id="m14",
    title="Capstone: take a change to Najm Remit through the full AI-native cycle",
    lesson="14.1",
    needs_agent=False,  # an agent is recommended (that is what the capstone practises); the grader only sees the result
    seed=seed,
    grade=grade,
    solve=solve,
)
