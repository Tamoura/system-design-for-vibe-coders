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
approved tools, what the repository has today and last quarter's numbers. Do not edit it, and do not
edit `CONTRIBUTING.md` to suit your playbook: the playbook sits under both.

### What I need

1. **The ten sections** of the skeleton, in order, each with real content, in 700 to 4,500 words. Keep
   each heading's key word (tools, data, context or memory, spec or review, verification, security,
   automation, metrics, incident, onboarding): a topic is read only in its own section.
2. **Rules, not wishes.** A rule is one list item that starts with `MUST` or `MUST NOT` and ends with
   `Check:` and what runs or leaves a record: a command, a CI job or status check, a hook, a script, a
   scan, a report or log, a checklist item, a label, a branch-protection setting, or an audit that
   compares or lists named things. A person ("the team lead reviews it") is not a check, nor is "a CI
   job" with no word on what it looks at. Write at least 12, with at least one each under data rules,
   spec and review norms, verification standard, security baseline, automation and incident handling.
   No soft words ("carefully", "regularly", "where possible"). "Be careful with customer data" is a
   wish; "MUST NOT put customer names or account numbers in a prompt. Check: ..." is a rule.
3. **Concrete review norms, in section 4:** the label, the largest diff you accept (10 to 800 lines), who must
   review money logic (`CONTRIBUTING.md` names the modules), how soon a review happens, what the author
   must explain.
4. **A metrics plan**, one `###` block per metric in the skeleton's shape; `Kind` is `delivery` or
   `guard`. At least three delivery metrics (DORA-style: lead time, deployment frequency, change
   failure rate, recovery time or rework rate) and at least one guard metric, whose Threshold gives a
   number and says what we do when it is crossed. A definition says what is counted or timed, from
   which event to which event, over which period. A baseline is a figure from the facts file, in its
   unit or an equivalent (52 hours, about 2 days), or "to be measured". Thresholds and limits are our
   own choice: say so. Lines of code, suggestion acceptance and the share of AI-written code are not
   metrics or targets here, nor is the 60% label share, which is context.
5. **The bank's rules hold:** nothing looser than the six rules or `CONTRIBUTING.md`; say in your own
   words that agents never touch production.
6. **No invented evidence:** no statistic or "studies show" without a source in the same sentence. A
   backticked file must exist, or the sentence that names it must call it new or proposed ("a new
   `CODEOWNERS` file").

### Done when

- `playbook.md` has no `<<...>>` left, and nothing else has changed.
- It is committed on the branch you started on, with messages that follow `CONTRIBUTING.md` (any
  lower-case scope, such as `docs(playbook):`).
- Grade it from the `ailab` folder of the course repository:
  `python -m ailab grade m12 --dir <this directory>`
