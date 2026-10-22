"""Tests for lab m05 (review a pull request an agent wrote, then fix it).

Three groups:

* the review reader: formats it accepts, how tolerant it is, and what it refuses to count;
* the review checks against a started lab: the wrong reviews a learner or an AI reviewer really writes;
* the fix checks: the wrong fixes (including the ones an agent tends to make) and two different right ones.

Every test starts from the same started lab (copied, so the tests do not disturb each other).
"""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest

from ailab import checks_m05, framework, gitutil
from conftest import LEARNER, learner_commit, start

LAB = framework.load_lab("m05")

# check names, shortened
R_FILE, R_FORM, R_VERDICT, R_FOUND, R_SEVERITY, R_ALL, R_KEY = (
    "review.md has a verdict, what you ran and findings",
    "Each finding names a file, a line and a severity",
    "Your verdict blocks the merge",
    "Your review covers the problems in the pull request",
    "Your severities fit the risk",
    "Your review covers every problem the grader knows",
    "Your review names the follow-up beyond the diff",
)
F_VISIBLE, F_HIDDEN, F_RULES, F_CHECKLIST, F_CATCH, F_SCOPE, F_COMMITS, F_CLEAN, F_SMALL, F_BRANCH = (
    "The branch's own tests pass",
    "The discount behaves as REMIT-229 says",
    "The team's code rules hold (CONTRIBUTING.md)",
    "The branch passes the review checklist (lesson 5.1)",
    "Your tests would have caught the agent's bugs",
    "Only the files the change needs changed",
    "Your commit messages follow CONTRIBUTING.md",
    "Your fix is committed",
    "The fix is small",
    "You fixed the agent's branch on top of its commits",
)
REVIEW_CHECKS = {R_FILE, R_FORM, R_VERDICT, R_FOUND, R_SEVERITY}
FIX_CHECKS = {F_VISIBLE, F_HIDDEN, F_RULES, F_CHECKLIST, F_CATCH, F_SCOPE, F_COMMITS, F_CLEAN}
ADVISORY = {R_ALL, R_KEY, F_SMALL, F_BRANCH}
REQUIRED = REVIEW_CHECKS | FIX_CHECKS

# what the two aggregated checks print when a particular rule is broken
MARKERS = {
    "deps": "standard library only", "secrets": "secrets:", "float": "money is Decimal",
    "except": "errors hidden", "assert": "no assertion in", "faked": "fee code patched", "deleted": "existing test missing",
}


def broken(result: dict[str, framework.Check]) -> set[str]:
    """Which rules the two aggregated fix checks say are broken."""
    text = result[F_RULES].detail + " | " + result[F_CHECKLIST].detail
    return {tag for tag, marker in MARKERS.items() if marker in text}


def strip(name: str) -> str:
    return re.sub(r" \(advisory\)$", "", name)


# ---------------------------------------------------------------------------------------------
# fixtures and helpers
# ---------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def template(tmp_path_factory) -> Path:
    return start("m05", tmp_path_factory.mktemp("m05-template") / "work")


@pytest.fixture
def work(template, tmp_path) -> Path:
    target = tmp_path / "work"
    shutil.copytree(template, target)
    return target


def grade(work: Path) -> dict[str, framework.Check]:
    return {c.name: c for c in framework.grade_lab(LAB, work, catch=False)}


def failing(result: dict[str, framework.Check]) -> set[str]:
    return {name for name, check in result.items() if not check.ok}


def required_failures(result: dict[str, framework.Check]) -> set[str]:
    return {name for name, check in result.items() if not check.ok and check.required}


def assert_required_failures(result: dict[str, framework.Check], *expected: str) -> None:
    got = required_failures(result)
    detail = "\n".join(f"  {'ok  ' if c.ok else 'FAIL'} {n}: {c.detail}" for n, c in result.items())
    assert got == set(expected), f"expected required failures {set(expected)}, got {got}\n{detail}"


# the eight problems, written the way a reviewer might (not copied from the reference review)
GOOD = {
    "dep": ("pyproject.toml", "11", "blocker", "New package najm-loyalty added to dependencies. I cannot find it anywhere; it looks invented. Standard library only."),
    "key": ("src/remit/loyalty.py", "14", "blocker", "A live API key is hard-coded in the module. It is in git history now: rotate it."),
    "float": ("src/remit/fees.py", "117", "blocker", "The discount uses float and round(), not Decimal half-up. Cents are wrong on ties."),
    "swallow": ("src/remit/fees.py", "119", "major", "except Exception swallows every error and quietly charges the full fee."),
    "scope": ("src/remit/fees.py", "145", "blocker", "Unrequested change: the express surcharge is now inside the cap. Scope creep in money logic."),
    "deleted": ("tests/test_fees.py", "-", "major", "The test for the express surcharge after the cap was deleted so the suite stays green."),
    "noassert": ("tests/test_loyalty.py", "30", "minor", "The gold test only prints the fee. No assert, it can never fail."),
    "mock": ("tests/test_loyalty.py", "23", "minor", "The silver test patches _apply_discount and then asserts the mock's own value."),
}


def review_text(keys=tuple(GOOD), *, verdict="request changes", ran="- ran git diff main...agent/loyalty-discount and pytest -q on the branch; read the ticket first",
                overrides=None, style="headings") -> str:
    overrides = overrides or {}
    rows = []
    for number, key in enumerate(keys, start=1):
        file, line, severity, problem = (*GOOD[key][:3], GOOD[key][3])
        file, line, severity, problem = overrides.get(key, (file, line, severity, problem))
        rows.append((number, file, line, severity, problem))
    head = f"# Review\n\n## Verdict\n\n{verdict}\n\n## What I ran\n\n{ran}\n\n## Findings\n\n"
    if style == "headings":
        body = "".join(f"### {n}. {p.split('.')[0]}\n- **File:** {f}\n- **Line:** {ln}\n- **Severity:** {s}\n- **Problem:** {p}\n- **Fix:** fix it\n\n"
                       for n, f, ln, s, p in rows)
    elif style == "table":
        body = "| # | File | Line | Severity | Problem |\n|---|---|---|---|---|\n" + "".join(
            f"| {n} | `{f}` | {ln} | {s} | {p} |\n" for n, f, ln, s, p in rows)
    elif style == "bullets":
        body = "".join(f"{n}. [{s}] `{f}:{ln}` {p}\n" if ln != "-" else f"{n}. [{s}] `{f}` (line -) {p}\n" for n, f, ln, s, p in rows)
    else:
        raise ValueError(style)
    return head + body + "\n## What is good\n\nThe service wiring is right.\n"


def write_review(work: Path, text: str) -> None:
    (work / "review.md").write_text(text, encoding="utf-8")


def known(work: Path) -> list[str]:
    return gitutil.out(work, "ls-tree", "-r", "--name-only", "lab-start").splitlines()


# the right fix, applied with the reference commits but without its review
def apply_reference_fix(work: Path, upto: int = 99) -> None:
    for number, patch in enumerate(sorted((LAB.solution_dir).glob("*.patch")), start=1):
        if number > upto:
            break
        gitutil.apply_patch(work, patch)
        learner_commit(work, patch.with_suffix(".msg").read_text(encoding="utf-8").strip())


def edit(work: Path, rel: str, old: str, new: str, count: int = 1) -> None:
    framework.edit_file(work, rel, old, new, count=count)


# =============================================================================================
# 1. the review reader
# =============================================================================================
def test_the_reader_accepts_headings_tables_and_numbered_lists(work):
    for style in ("headings", "table", "bullets"):
        review = checks_m05.parse_review(review_text(style=style), known(work))
        assert len(review.findings) == 8, style
        matches = checks_m05.match_findings(review.findings, checks_m05.flaw_lines(work))
        assert matches.count == 8, (style, sorted(matches.found))
        assert not checks_m05.under_rated(matches)


def test_the_reader_accepts_the_styles_an_ai_reviewer_uses(work):
    table = """## Verdict
Request changes
## What I ran
git diff main...agent/loyalty-discount and pytest -q on the branch, plus a check by hand
## Findings
| # | Severity | Location | Issue | Fix |
|---|---|---|---|---|
| 1 | **Blocker** | `src/remit/loyalty.py:14` | Hard-coded API key, rotate it | remove it |
| 2 | Major | src/remit/fees.py#L117-L119 | float used for money, and except Exception | use Decimal |
"""
    numbered = """## Verdict
reject
## What I ran
stuff I ran here for the review of the branch
## Findings
1. **Hard-coded key** — `src/remit/loyalty.py` line 14 — *blocker*. A live key.
2. **Deleted test** — tests/test_fees.py, line - — major. The express test was removed.
"""
    bracketed = """## Verdict
request changes
## What I ran
stuff I ran here for the review of the branch
## Findings
### [BLOCKER] Hard-coded API key (loyalty.py:14)
The key is in the module.
### [MAJOR] swallowed error (fees.py:119)
except Exception hides errors.
### Questions for the author
Why the rename?
"""
    for style, text, expected in (("table", table, 2), ("numbered", numbered, 2), ("bracketed", bracketed, 2)):
        review = checks_m05.parse_review(text, known(work))
        assert len(review.findings) == expected, style
        assert all(f.complete for f in review.findings), (style, [(f.files, f.severity, f.line_given) for f in review.findings])
        assert checks_m05.verdict_blocks_merge(review.verdict), style
        found = checks_m05.match_findings(review.findings, checks_m05.flaw_lines(work)).found
        assert len(found) == 2, (style, sorted(found))


def test_html_comments_in_the_template_are_not_findings(work):
    template = (work / "lab-assets" / "review-template.md").read_text(encoding="utf-8")
    review = checks_m05.parse_review(template, known(work))
    assert [f for f in review.findings if f.complete] == []  # the empty template has nothing a grader could count
    assert "approve | approve" not in review.verdict


@pytest.mark.parametrize("token, expected", [
    ("fees.py", "src/remit/fees.py"), ("src/remit/fees.py", "src/remit/fees.py"), ("./src/remit/fees.py", "src/remit/fees.py"),
    ("`tests/test_fees.py`", "tests/test_fees.py"), ("pyproject.toml", "pyproject.toml"), ("loyalty.py", "src/remit/loyalty.py"),
    ("nonsense.py", None),
])
def test_paths_are_resolved_whatever_way_the_reviewer_wrote_them(work, token, expected):
    assert checks_m05.resolve_path(token, known(work)) == expected


def test_severity_words_are_normalised(work):
    text = review_text(overrides={"key": ("src/remit/loyalty.py", "14", "critical", GOOD["key"][3]),
                                  "mock": ("tests/test_loyalty.py", "23", "low", GOOD["mock"][3]),
                                  "noassert": ("tests/test_loyalty.py", "30", "nitpick", GOOD["noassert"][3])})
    got = {f.files[0] + ":" + str(f.lines[0]): f.severity for f in checks_m05.parse_review(text, known(work)).findings if f.lines}
    assert got["src/remit/loyalty.py:14"] == "blocker" and got["tests/test_loyalty.py:23"] == "minor" and got["tests/test_loyalty.py:30"] == "nit"


@pytest.mark.parametrize("verdict, blocks", [
    ("request changes", True), ("Request changes: do not merge", True), ("reject", True), ("changes requested", True),
    ("approve", False), ("approve with comments", False), ("LGTM", False), ("", False),
    ("approve once the key is rotated", False),
])
def test_only_a_verdict_that_asks_for_changes_blocks_the_merge(verdict, blocks):
    assert checks_m05.verdict_blocks_merge(verdict) is blocks


def test_matching_is_tolerant_of_wording_and_of_line_numbers(work):
    wrong_lines = {k: (v[0], "3", v[2], v[3]) for k, v in GOOD.items()}  # every line number is wrong
    review = checks_m05.parse_review(review_text(overrides=wrong_lines), known(work))
    assert checks_m05.match_findings(review.findings, checks_m05.flaw_lines(work)).count == 8
    no_words = {k: (v[0], v[1], v[2], "Look here.") for k, v in GOOD.items() if v[1] != "-"}  # right place, no explanation
    review = checks_m05.parse_review(review_text(overrides=no_words), known(work))
    found = checks_m05.match_findings(review.findings, checks_m05.flaw_lines(work)).found
    assert "float-money" in found and "swallowed-exception" in found and "hard-coded-key" in found


def test_one_finding_covers_one_problem_however_many_words_it_uses(work):
    everything = ("Float money, a swallowed exception with except Exception, a hard-coded api key, a hallucinated dependency, "
                  "scope creep, a deleted test, a test with no assert and a mock.")
    one = {"float": ("src/remit/fees.py", "117", "blocker", everything)}
    review = checks_m05.parse_review(review_text(("float",), overrides=one), known(work))
    assert checks_m05.match_findings(review.findings, checks_m05.flaw_lines(work)).count == 1


def test_a_finding_in_the_wrong_file_does_not_count(work):
    wrong = {"key": ("README.md", "3", "blocker", GOOD["key"][3]), "dep": ("src/remit/money.py", "1", "blocker", GOOD["dep"][3])}
    review = checks_m05.parse_review(review_text(("key", "dep"), overrides=wrong), known(work))
    assert checks_m05.match_findings(review.findings, checks_m05.flaw_lines(work)).count == 0


# =============================================================================================
# 2. the starter and the reference
# =============================================================================================
def test_the_starter_waits_for_a_review_and_names_nothing(work):
    result = grade(work)
    assert REVIEW_CHECKS | FIX_CHECKS <= {strip(n) for n in result}
    assert required_failures(result) == REQUIRED
    assert all(not result[n].ok for n in result if strip(n) in FIX_CHECKS)
    assert all("not checked yet" in c.detail for n, c in result.items() if strip(n) in FIX_CHECKS | {F_SMALL, F_BRANCH})
    spill = " ".join(c.detail + c.hint for c in result.values()).lower()
    for word in ("najm-loyalty", "float", "except", "mock", "api key", "express", "hard-coded"):
        assert word not in spill, f"the starter output gives away {word!r}"


def test_the_reference_solution_passes_every_check(work):
    framework.solve_lab(LAB, work)
    result = grade(work)
    assert all(c.ok for c in result.values()), {n: c.detail for n, c in result.items() if not c.ok}
    assert "8 of 8" in result[R_ALL].detail or "8 of 8" in result[R_ALL].detail


def test_the_starter_branch_is_what_the_lesson_says(work):
    assert gitutil.current_branch(work) == "agent/loyalty-discount" and "main" in gitutil.branches(work)
    log = gitutil.out(work, "log", "--format=%s", "main..agent/loyalty-discount").splitlines()
    assert log == ["Lab starting state", "refactor(fees): tidy helper names and docs", "test(loyalty): cover the loyalty discount",
                   "feat(service): charge the customer's loyalty tier on quote and send", "feat(fees): add a loyalty discount to quote_fee"]
    stat = gitutil.out(work, "diff", "--name-only", "main...agent/loyalty-discount").splitlines()
    assert stat == ["pyproject.toml", "src/remit/fees.py", "src/remit/loyalty.py", "src/remit/service.py", "tests/test_fees.py", "tests/test_loyalty.py"]
    assert (work / "TASK.md").is_file() and (work / "lab-assets" / "ticket-REMIT-229.md").is_file()
    # the suite on the branch is green: that is the whole point
    from ailab import checks
    assert checks.run_pytest(work).ok


def test_every_seeded_problem_is_where_the_markers_say(work):
    lines = checks_m05.flaw_lines(work)
    assert {fid for fid, per_file in lines.items() if per_file} == set(checks_m05.FLAW_IDS)
    for flaw in checks_m05.FLAWS:  # every declared marker was found, once
        for path, marker in flaw.markers:
            assert len(lines[flaw.id].get(path, [])) >= 1, (flaw.id, path, marker)


# =============================================================================================
# 3. wrong reviews
# =============================================================================================
def test_a_review_that_approves(work):
    write_review(work, review_text(verdict="approve with comments"))
    result = grade(work)
    assert R_VERDICT in failing(result)
    assert result[R_FOUND].ok  # the findings are fine; the decision is not
    assert "request changes" in result[R_VERDICT].hint


def test_a_review_without_the_required_sections(work):
    write_review(work, "# Review\n\nLooks fine to me, tests are green.\n")
    result = grade(work)
    assert {R_FILE, R_FORM, R_VERDICT, R_FOUND} <= failing(result)
    assert "missing" in result[R_FILE].detail


def test_the_untouched_template_is_not_a_review(work):
    shutil.copyfile(work / "lab-assets" / "review-template.md", work / "review.md")
    result = grade(work)
    assert {R_FORM, R_VERDICT, R_FOUND} <= failing(result)


def test_findings_without_files_lines_or_severities(work):
    text = review_text()
    text = re.sub(r"- \*\*File:\*\* .*\n", "", text, count=2)
    text = re.sub(r"- \*\*Severity:\*\* .*\n", "", text, count=1)
    write_review(work, text)
    result = grade(work)
    assert R_FORM in failing(result) and "incomplete" in result[R_FORM].detail


def test_a_vague_review_finds_nothing(work):
    vague = {k: ("README.md", "1", "major", "This could be improved.") for k in GOOD}
    write_review(work, review_text(overrides=vague))
    result = grade(work)
    assert R_FOUND in failing(result) and "0 of 8" in result[R_FOUND].detail
    assert "Nothing found yet in:" in result[R_FOUND].hint


def test_five_of_eight_is_not_enough_and_the_hint_names_classes_not_lines(work):
    write_review(work, review_text(("dep", "key", "float", "swallow", "scope")))
    result = grade(work)
    assert R_FOUND in failing(result) and "5 of 8" in result[R_FOUND].detail
    assert "tests" in result[R_FOUND].hint
    assert "loyalty.py" not in result[R_FOUND].hint and "assert" not in result[R_FOUND].hint.lower()


def test_six_of_eight_passes_but_the_advisory_asks_for_the_rest(work):
    write_review(work, review_text(("dep", "key", "float", "swallow", "scope", "deleted"), ran="- git diff and pytest, then the old test from main"))
    result = grade(work)
    assert result[R_FOUND].ok and not result[R_ALL].ok
    assert required_failures(result) == FIX_CHECKS - {F_VISIBLE, F_CLEAN}  # the fix is graded now, and it is not there yet


def test_calling_the_hard_coded_key_a_nit(work):
    write_review(work, review_text(overrides={"key": ("src/remit/loyalty.py", "14", "nit", GOOD["key"][3])}))
    result = grade(work)
    assert R_SEVERITY in failing(result)
    assert "1 finding" in result[R_SEVERITY].detail


def test_calling_a_test_problem_a_nit_is_also_an_under_rating(work):
    write_review(work, review_text(overrides={"noassert": ("tests/test_loyalty.py", "30", "nit", GOOD["noassert"][3])}))
    assert R_SEVERITY in failing(grade(work))


def test_a_second_model_review_pasted_in_with_extra_noise_still_counts(work):
    """An AI reviewer's list: eight real findings plus three the grader cannot judge. Extra findings never fail a review."""
    text = review_text()
    text += "\n"  # the findings section is last-but-one in this file; add noise as more findings before 'What is good'
    noise = ("### 9. Missing docstring\n- **File:** src/remit/loyalty.py\n- **Line:** 19\n- **Severity:** nit\n- **Problem:** Add a docstring.\n\n"
             "### 10. Consider a dataclass\n- **File:** src/remit/service.py\n- **Line:** 90\n- **Severity:** nit\n- **Problem:** Use a dataclass.\n\n")
    write_review(work, text.replace("## What is good", noise + "## What is good"))
    result = grade(work)
    assert result[R_FOUND].ok and "more finding" in result[R_FOUND].detail


def test_the_key_advisory_wants_the_word_rotate_or_leak(work):
    write_review(work, review_text(overrides={"key": ("src/remit/loyalty.py", "14", "blocker", "A key is hard-coded in the module.")}))
    assert not grade(work)[R_KEY].ok
    write_review(work, review_text())
    assert grade(work)[R_KEY].ok


# =============================================================================================
# 4. a good review, then wrong fixes
# =============================================================================================
def test_a_good_review_with_no_fix_yet(work):
    write_review(work, review_text())
    result = grade(work)
    assert REVIEW_CHECKS <= {n for n, c in result.items() if c.ok}
    assert result[F_VISIBLE].ok  # the agent's own suite is green: that is the trap
    assert_required_failures(result, F_HIDDEN, F_RULES, F_CHECKLIST, F_CATCH, F_SCOPE, F_COMMITS)
    assert broken(result) == set(MARKERS)
    assert "22.5720" not in " ".join(c.detail + c.hint for c in result.values())  # nothing from the hidden tests leaks


def solved_without_review(template, tmp_path, upto=99) -> Path:
    target = tmp_path / "fixed"
    shutil.copytree(template, target)
    apply_reference_fix(target, upto)
    write_review(target, review_text())
    return target


def test_removing_the_package_and_the_key_is_not_a_fix(template, tmp_path):
    work = solved_without_review(template, tmp_path, upto=1)
    result = grade(work)
    assert_required_failures(result, F_HIDDEN, F_RULES, F_CHECKLIST, F_CATCH)
    assert broken(result) == {"float", "except", "assert", "faked", "deleted"}  # the package and the key are gone
    assert result[F_COMMITS].ok


def test_fixing_the_code_but_leaving_the_tests_weak(template, tmp_path):
    work = solved_without_review(template, tmp_path, upto=3)
    result = grade(work)
    assert result[F_HIDDEN].ok and result[F_RULES].ok
    assert_required_failures(result, F_CHECKLIST, F_CATCH)
    assert broken(result) == {"assert", "faked", "deleted"}


def test_restoring_the_deleted_test_alone_does_not_make_the_tests_honest(template, tmp_path):
    work = solved_without_review(template, tmp_path, upto=4)
    result = grade(work)
    assert "deleted" not in broken(result) and {"assert", "faked"} <= broken(result)
    assert result[F_CATCH].ok is False and "1 new or changed test" in result[F_CATCH].detail


def test_special_casing_the_example(work):
    """A 'fix' that makes the ticket's tie example pass by recognising it, and still computes with floats."""
    apply_reference_fix(work)
    edit(work, "src/remit/fees.py", "    discount = base * discount_rate(tier)  # Money x Decimal: rounded half up to the cent\n",
         "    if base == Money('5.85', base.currency) and tier == 'silver':\n        return Money('5.26', base.currency)\n"
         "    discount = Money(str(round(float(base.amount) * float(discount_rate(tier)), 2)), base.currency)\n")
    learner_commit(work, "fix(fees): handle the half-cent case")
    write_review(work, review_text())
    result = grade(work)
    assert F_HIDDEN in failing(result)  # the sweep finds the other ties
    assert "float" in broken(result)


def test_narrowing_the_handler_but_still_hiding_the_error(work):
    apply_reference_fix(work)
    edit(work, "src/remit/loyalty.py", '''    try:
        return DISCOUNT_RATES[tier]
    except KeyError:
        raise ValueError(f"unknown loyalty tier {tier!r}; expected one of {tuple(DISCOUNT_RATES)}") from None
''', "    return DISCOUNT_RATES.get(tier, Decimal(0))\n")
    learner_commit(work, "fix(loyalty): be forgiving about the tier")
    write_review(work, review_text())
    result = grade(work)
    assert F_HIDDEN in failing(result)  # 'Gold' with a capital letter silently pays full price again
    assert "except" not in broken(result)  # no handler left: the hidden tests are what catch this one


def test_a_broad_handler_that_logs_and_reraises_is_fine_but_one_that_returns_is_not(work):
    apply_reference_fix(work)
    edit(work, "src/remit/fees.py", "    discount = base * discount_rate(tier)  # Money x Decimal: rounded half up to the cent\n    return max(base - discount, minimum)\n",
         "    try:\n        discount = base * discount_rate(tier)\n    except Exception:\n        raise\n    return max(base - discount, minimum)\n")
    learner_commit(work, "refactor(fees): name the failure")
    write_review(work, review_text())
    assert "except" not in broken(grade(work))
    edit(work, "src/remit/fees.py", "    except Exception:\n        raise\n", "    except Exception:\n        return base\n")
    learner_commit(work, "fix(fees): never fail a quote")
    assert "except" in broken(grade(work))


def test_relaxing_money_so_that_floats_work(work):
    apply_reference_fix(work)
    edit(work, "src/remit/money.py", "    if isinstance(value, (bool, float)):\n        raise TypeError", "    if isinstance(value, float):\n        value = str(value)\n    if isinstance(value, bool):\n        raise TypeError")
    learner_commit(work, "fix(money): accept floats")
    write_review(work, review_text())
    result = grade(work)
    assert F_VISIBLE in failing(result) and F_SCOPE in failing(result)


def test_editing_the_ticket_instead_of_the_code(work):
    apply_reference_fix(work)
    edit(work, "lab-assets/ticket-REMIT-229.md", "rounded half up to 2 decimals", "rounded to 2 decimals")
    learner_commit(work, "docs(docs): relax the rounding rule")
    write_review(work, review_text())
    assert F_SCOPE in failing(grade(work))


def test_weakening_the_hard_test_to_get_green(work):
    """Delete the agent's tests and everything else that could fail, keep the weak ones."""
    apply_reference_fix(work, upto=3)
    (work / "tests" / "test_loyalty.py").write_text(
        (work / "tests" / "test_loyalty.py").read_text(encoding="utf-8")
        .replace('    print(f"gold fee for QAR 1,000: {fee}")', '    assert fee is not None'), encoding="utf-8")
    learner_commit(work, "test(loyalty): make the gold test pass")
    write_review(work, review_text())
    result = grade(work)
    assert "faked" in broken(result)  # the patched silver test is still there
    assert F_CATCH in failing(result)  # nothing the learner added or changed fails on the agent's code


def test_deleting_the_weak_tests_without_replacing_them(template, tmp_path):
    work = solved_without_review(template, tmp_path, upto=4)
    (work / "tests" / "test_loyalty.py").unlink()
    learner_commit(work, "test(loyalty): remove the weak tests")
    result = grade(work)
    assert F_CATCH in failing(result)  # only the restored test now fails on the agent's code
    assert not {"assert", "faked"} & broken(result)


def test_a_new_dependency_for_the_tests(template, tmp_path):
    work = solved_without_review(template, tmp_path)
    (work / "tests" / "test_loyalty_props.py").write_text(
        "from hypothesis import given, strategies as st\n\n\n@given(st.integers())\ndef test_ints(x):\n    assert x == x\n", encoding="utf-8")
    learner_commit(work, "test(loyalty): add a property test")
    result = grade(work)
    assert "deps" in broken(result) and "hypothesis" in result[F_RULES].detail


def test_a_secret_added_by_the_fix(template, tmp_path):
    work = solved_without_review(template, tmp_path)
    edit(work, "src/remit/loyalty.py", 'DISCOUNT_RATES =', 'LOYALTY_API_KEY = "najm-loy-live-0a1b2c3d4e5f6789"\nDISCOUNT_RATES =')
    learner_commit(work, "fix(loyalty): keep the key for later")
    result = grade(work)
    assert "secrets" in broken(result)
    assert "0a1b2c3d" not in result[F_RULES].detail + result[F_RULES].hint


def test_unrelated_files_in_the_fix(template, tmp_path):
    work = solved_without_review(template, tmp_path)
    (work / "src" / "remit" / "limits.py").write_text((work / "src" / "remit" / "limits.py").read_text(encoding="utf-8") + "\n# tidy\n", encoding="utf-8")
    learner_commit(work, "chore(limits): tidy")
    result = grade(work)
    assert F_SCOPE in failing(result) and "limits.py" in result[F_SCOPE].detail


def test_an_uncommitted_fix_and_a_bad_message(template, tmp_path):
    work = solved_without_review(template, tmp_path)
    (work / "docs" / "note.md").write_text("notes\n", encoding="utf-8")
    result = grade(work)
    assert F_CLEAN in failing(result)
    learner_commit(work, "fixed stuff.")
    assert F_COMMITS in failing(grade(work))


def test_a_message_that_ignores_the_scope_rule(template, tmp_path):
    work = solved_without_review(template, tmp_path)
    (work / "docs" / "note.md").write_text("notes\n", encoding="utf-8")
    learner_commit(work, "docs: add a note")
    assert F_COMMITS in failing(grade(work))


# =============================================================================================
# 5. right fixes, reached differently
# =============================================================================================
def test_an_alternative_fix_with_a_different_structure_passes(work):
    """No loyalty.py at all: the rates live in fees.py; unknown tiers raise a different ValueError subclass; tests go to test_fees.py."""
    gitutil.git(work, "rm", "-q", "src/remit/loyalty.py")
    edit(work, "pyproject.toml", 'dependencies = ["najm-loyalty>=2.1"]', "dependencies = []")
    learner_commit(work, "fix(deps): drop the invented package and the module that held the key")
    # the agent's fees.py back to the base behaviour, then the discount written from scratch
    gitutil.git(work, "checkout", "main", "--", "src/remit/fees.py", "tests/test_fees.py")
    edit(work, "src/remit/fees.py", "from remit.money import Money\n", "from remit.money import Money\n\nLOYALTY_DISCOUNT = {'none': Decimal('0'), 'silver': Decimal('0.1'), 'gold': Decimal('0.2')}\n")
    edit(work, "src/remit/fees.py", "def explain_fee(amount: Money, corridor: Corridor, *, express: bool = False) -> FeeBreakdown:",
         "def explain_fee(amount: Money, corridor: Corridor, *, express: bool = False, loyalty_tier: str = 'none') -> FeeBreakdown:")
    edit(work, "src/remit/fees.py", "    base = min(max(raw, minimum), cap)\n",
         "    base = min(max(raw, minimum), cap)\n    if loyalty_tier not in LOYALTY_DISCOUNT:\n        raise ValueError(f'no such loyalty tier: {loyalty_tier}')\n"
         "    reduction = Money(base.amount * LOYALTY_DISCOUNT[loyalty_tier], cur)\n    base = max(base - reduction, minimum)\n")
    edit(work, "src/remit/fees.py", "def quote_fee(amount: Money, corridor: Corridor, *, express: bool = False) -> Money:",
         "def quote_fee(amount: Money, corridor: Corridor, *, express: bool = False, loyalty_tier: str = 'none') -> Money:")
    edit(work, "src/remit/fees.py", "    return explain_fee(amount, corridor, express=express).total", "    return explain_fee(amount, corridor, express=express, loyalty_tier=loyalty_tier).total")
    learner_commit(work, "fix(fees): price the discount in Decimal and restore the cap")
    (work / "tests" / "test_loyalty.py").write_text('''"""Loyalty discount, checked against the ticket."""
import pytest

from remit.corridors import get_corridor
from remit.fees import quote_fee
from remit.money import Money

INR = get_corridor("QAR", "INR")


def qar(v):
    return Money(v, "QAR")


@pytest.mark.parametrize("amount, tier, express, fee", [
    ("670.00", "silver", False, "13.54"), ("670.00", "gold", False, "12.04"), ("100.00", "gold", False, "5.00"),
    ("1000.00", "silver", True, "33.00"), ("192.50", "silver", False, "5.26"), ("20000.00", "none", True, "165.00"),
])
def test_ticket_numbers(amount, tier, express, fee):
    assert quote_fee(qar(amount), INR, express=express, loyalty_tier=tier) == qar(fee)


def test_unknown_tier_raises():
    with pytest.raises(ValueError):
        quote_fee(qar("100"), INR, loyalty_tier="Gold")


def test_service_uses_the_customers_tier(service):
    assert service.send("C002", qar("1000"), "INR", "Ravi Kumar").transfer.fee == qar("18.00")
''', encoding="utf-8")
    learner_commit(work, "test(loyalty): check the ticket's numbers")
    write_review(work, review_text())
    result = grade(work)
    assert required_failures(result) == set(), {n: c.detail for n, c in result.items() if not c.ok}


def test_squashing_the_history_passes_the_required_checks_and_the_advisory_notices(template, tmp_path):
    work = solved_without_review(template, tmp_path)
    gitutil.git(work, "reset", "--soft", "main")
    learner_commit(work, "fix(fees): review fixes for the loyalty discount")
    result = grade(work)
    assert required_failures(result) == set()
    assert F_BRANCH in failing(result)


def test_an_uncommitted_review_is_fine(template, tmp_path):
    work = solved_without_review(template, tmp_path)
    assert (work / "review.md").exists() and "review.md" in gitutil.status_porcelain(work, ignore=())[0]
    assert required_failures(grade(work)) == set()


def test_a_committed_review_is_fine_too(template, tmp_path):
    work = solved_without_review(template, tmp_path)
    learner_commit(work, "docs(review): my review")
    assert required_failures(grade(work)) == set()


# =============================================================================================
# 6. the static scans on their own
# =============================================================================================
def make_tree(tmp_path: Path, files: dict[str, str]) -> Path:
    for rel, text in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return tmp_path


def test_scan_tests_without_assertions(tmp_path):
    make_tree(tmp_path, {"tests/test_a.py": (
        "import pytest\n"
        "def test_none():\n    x = 1\n    print(x)\n"
        "def test_assert():\n    assert 1\n"
        "def test_raises():\n    with pytest.raises(ValueError):\n        int('x')\n"
        "def test_helper():\n    assert_only(1)\n"
        "class TestC:\n    def test_m(self):\n        self.assertEqual(1, 1)\n"
        "def helper():\n    pass\n"
        "def check_fee(x):\n    assert x\n"
        "def test_via_helper():\n    check_fee(1)\n"
        "def test_via_empty_helper():\n    helper()\n")})
    assert checks_m05.unasserted_tests(tmp_path) == ["tests/test_a.py::test_none", "tests/test_a.py::test_via_empty_helper"]


def test_scan_for_faked_fee_code(tmp_path):
    make_tree(tmp_path, {"tests/test_b.py": (
        "from unittest.mock import patch\nfrom remit import fees\n"
        "def test_patch_object():\n    with patch.object(fees, 'x', return_value=1):\n        pass\n"
        "def test_patch_string():\n    with patch('remit.service.quote_fee'):\n        pass\n"
        "def test_monkeypatch(monkeypatch):\n    monkeypatch.setattr('remit.fees._apply', lambda: 1)\n"
        "def test_other_patch():\n    with patch('remit.notify.render'):\n        pass\n"
        "def test_env(monkeypatch):\n    monkeypatch.setenv('REMIT_DB', 'x')\n"
        "def test_environ():\n    with patch.dict('os.environ', {'A': 'b'}):\n        pass\n")})
    assert checks_m05.faked_fee_code(tmp_path) == ["tests/test_b.py::test_monkeypatch", "tests/test_b.py::test_patch_object", "tests/test_b.py::test_patch_string"]


def test_scan_for_floats_and_broad_handlers_and_imports(tmp_path):
    make_tree(tmp_path, {
        "src/remit/a.py": "import json\nimport requests\nx = 0.1\ny = float('1')\ntry:\n    pass\nexcept Exception:\n    pass\n",
        "src/remit/money.py": "def f(v):\n    return isinstance(v, float)\n",
        "src/remit/b.py": "try:\n    pass\nexcept ValueError:\n    pass\ntry:\n    pass\nexcept Exception:\n    raise\ntry:\n    pass\nexcept:\n    print(1)\n",
        "tests/test_c.py": "import pytest\nimport hypothesis\n",
        "pyproject.toml": '[project]\nname = "x"\ndependencies = ["left-pad"]\n[project.optional-dependencies]\ndev = ["pytest"]\n',
    })
    assert checks_m05.float_problems(tmp_path) == ["float literal in src/remit/a.py:3", "float() in src/remit/a.py:4"]
    assert checks_m05.broad_except_problems(tmp_path) == ["src/remit/a.py:7", "src/remit/b.py:11"]
    problems = checks_m05.import_problems(tmp_path)
    assert "requests imported in src/remit/a.py" in problems and "hypothesis imported in tests/test_c.py" in problems
    assert "pyproject.toml lists runtime dependencies" in problems


def test_the_base_repository_passes_every_scan(work):
    base = gitutil.out(work, "rev-parse", "main")
    scratch = work.parent / "base-tree"
    subprocess.run(["git", "worktree", "add", "-q", str(scratch), base], cwd=work, check=True)
    try:
        assert checks_m05.unasserted_tests(scratch) == []
        assert checks_m05.faked_fee_code(scratch) == []
        assert checks_m05.float_problems(scratch) == []
        assert checks_m05.broad_except_problems(scratch) == []
        assert checks_m05.import_problems(scratch) == []
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", str(scratch)], cwd=work, check=True)
