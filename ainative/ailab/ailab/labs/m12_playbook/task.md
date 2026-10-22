# REMIT-262: write the Payments Platform AI engineering playbook

**From:** Hessa, Product Owner, Najm Remit, for Tariq
**To:** Payments Platform
**Priority:** Medium. Tariq presents it at Thursday's AI-native clinic.

Most of us use AI coding tools every day, each a little differently. Tariq wants one document we can
point to when a pull request, a new joiner or an incident asks "what is our rule for this?". Write it as
`playbook.md` in the repository root; a skeleton is already there. You may draft it with an AI
assistant. You are accountable for every line, and a playbook that says nothing anyone can check is
worse than none.

You may rely on `lab-assets/team-context.md`: the team, the bank's six rules, the data classes, the
approved tools and last quarter's numbers. Do not edit it, and do not edit `CONTRIBUTING.md` to suit
your playbook: the playbook sits under both.

### What I need

1. **The ten sections** of the skeleton, each with real content, in roughly 800 to 3,000 words in all.
2. **Rules, not wishes.** A rule is one list item that starts with `MUST` or `MUST NOT` and ends with
   `Check:` and how anyone can verify it: a command, a CI job, a hook, a checklist item or an audit.
   Write at least 12, with at least one each under data rules, spec and review norms, verification
   standard, security baseline, automation and incident handling. "Be careful with customer data" is a
   wish; "MUST NOT put customer names or account numbers in a prompt. Check: ..." is a rule.
3. **Concrete review norms:** the label, the largest diff you accept (in lines), who must review money
   logic (`CONTRIBUTING.md` names the modules), how soon a review happens, what the author must explain.
4. **A metrics plan**, one `###` block per metric in the skeleton's shape: at least three delivery
   metrics (DORA-style: lead time, deployment frequency, change failure rate, recovery time or rework
   rate) and at least one guard metric, whose Threshold gives a number and says what we do when it is
   crossed. A definition says what is counted or timed, from which event to which event, over which
   period. A baseline is a figure from the facts file, or "to be measured". Lines of code, suggestion
   acceptance and the share of AI-written code are not metrics or targets here.
5. **No invented evidence:** no statistic or "studies show" without a source, and no file the
   repository does not have.

### Done when

- `playbook.md` has no `<<...>>` left, and nothing else has changed.
- It is committed, with messages that follow `CONTRIBUTING.md`.
- `python -m ailab grade m12 --dir <this directory>`, run from the `ailab` folder of the course
  repository, passes.
