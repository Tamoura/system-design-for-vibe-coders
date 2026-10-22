# Payments Platform: AI engineering playbook

Owner: Tariq, engineering lead. Status: version 1, for the AI-native clinic. Next review: end of next quarter,
and after any incident in which an AI tool played a part.

This playbook applies to everyone who works on Najm Remit and to every AI tool that works in the repository.
It sits under the bank's six rules for AI engineering and under `CONTRIBUTING.md`. Where they disagree, they win.
Our rules are written as bullets that begin with MUST or MUST NOT and finish with the check that proves them.

## 1. Tools and environments

Only tools on Salem's approved-tools list are used. Today that is Claude Code on the bank's enterprise account,
signed in through SSO, and GitHub Copilot in the IDE on the enterprise plan. Personal accounts and free tiers are
never used for bank code. Salem keeps the list; Noura reviews the security of a tool and Sara its data handling.

Agents run on a managed laptop, in a clean working tree on a feature branch or a worktree, or on a CI runner with
a read-only token. They never run on a production host and never hold production credentials.

A new tool starts as a request to Salem. It is not used until it is on the list.

- MUST use only tools on the approved-tools list, signed in with the bank's account. Check: Salem's quarterly
  audit compares the licence report with the list, and any other tool named in a pull request is a finding.
- MUST NOT give an agent production credentials or run it on a production host. Check: Salem's CI secrets audit
  shows no production secret reachable from pull-request jobs.

## 2. Data rules

Sara's classes are Public, Internal, Confidential and Restricted. Remit source code is Internal and may go to an
approved tool. Customer names, account numbers, transfer histories, production logs and the sanctions watchlist
are Restricted. Test data is synthetic: fictional names and ids, as in `tests/conftest.py`.

Session transcripts are stored on the laptop, in plain text, for 30 days by default (check the current Claude Code
documentation). Anything pasted into a prompt stays on that disk for a month.

- MUST NOT put Confidential or Restricted data, or any secret, into a prompt, a memory file or an agent's context.
  Check: the secret scan runs in CI on every pull request, and Noura reads ten agent logs a month.
- MUST use synthetic customers in tests, fixtures and prompts. Check: the review checklist has the line "no real
  customer data in fixtures", and a reviewer who finds a real name blocks the merge.
- MUST sign in with the bank's enterprise account and never with a personal one. Check: Salem's quarterly licence
  report lists every user of an approved tool.

## 3. Context and memory

The repository has one `CLAUDE.md` at the root. Other tools read it through an `@AGENTS.md` pointer or an import.
Tariq owns it, and it changes through a pull request like any code. It stays under 200 lines, because a longer
file is followed less well. It holds commands, conventions and gotchas, never secrets and never customer data.

When an agent makes the same mistake twice, the engineer who sees it adds one line to the memory file, or a rule
or hook, in a pull request within a week. A correction is encoded once, for everyone.

- MUST NOT put secrets or customer data in `CLAUDE.md` or in any file it imports. Check: the secret scan covers
  memory files, and the pull-request template asks whether the memory changed.

## 4. Spec and review norms

Before an agent starts non-trivial work there is a ticket with acceptance criteria and non-goals, and the author
has read the agent's plan. If the plan touches a file the ticket did not name, the author stops and asks.

A pull request that an AI tool wrote or substantially shaped carries the label `AI-assisted`. It changes at most
400 lines (additions plus deletions, generated files excluded) and contains one logical change. Its description
says what the agent did, what the author changed by hand, which commands the author ran with their results, and
what was not checked. The author can explain every line; a reviewer who asks and gets no answer sends it back.
Tests are written with the change or before it.

Changes to `money.py`, `fees.py`, `fx.py`, `limits.py`, `ledger.py` or `service.py` need a second human reviewer
in addition to the author. An AI review is a first pass and never counts as that reviewer. Nobody approves their
own pull request. A pull request gets its first human review within one working day.

- MUST label every pull request `AI-assisted` when an AI tool wrote or shaped any part of it. Check: the
  `pr-hygiene` CI job fails when the description's "AI-assisted: yes" line and the label disagree.
- MUST NOT merge a pull request of more than 400 changed lines. Check: a CI step counts changed lines and fails
  above the limit; the author splits the work instead.
- MUST get a second human approval for the six money modules. Check: branch protection requires two approvals
  on those paths through the code-owners file.
- MUST have a first human review within one working day. Check: the weekly review-turnaround report lists
  every pull request that waited longer.

## 5. Verification standard

Done means verified, not "it compiles". Before a pull request is opened, `pytest -q` passes. New behaviour has a
test that fails without the change: the author reverts the source change, watches the new test fail, restores it,
and says so in the description. Money is `Decimal` through `Money`, never `float`, and money tests assert exact
values at the boundaries, such as 500.00 and 500.01. The author runs the changed command once by hand and pastes
the output.

- MUST pass `pytest -q` before review. Check: CI runs `pytest -q` as a required status check on every pull request.
- MUST NOT edit, delete or skip an existing test to make a change pass. Check: a CI step reports deleted test
  files and removed assertions, and the description must explain each one.
- MUST NOT use `float` for money. Check: a CI step greps `src/` for `float(` and fails on a match.

## 6. Security baseline

Secrets never go into prompts, code, tests, memory files or commits; `.env` files are denied to agents with
`Read(./.env)` and `Read(./.env.*)` deny rules in the shared settings. Agents never hold production credentials. Agents run in the default mode that asks
before acting, or in plan mode for exploration. Bypass mode (`--dangerously-skip-permissions`) is never used on a
laptop; managed settings disable it (`permissions.disableBypassPermissionsMode`, check the current documentation).

Standard library only: a new dependency needs a ticket and a second reviewer, and every package name an agent
suggests is looked up in the registry before anyone installs it, because agents invent names. Text from issues,
web pages and other repositories is data, not instructions. MCP servers and plugins are used only when Noura has
reviewed them, and a project `.mcp.json` change needs her approval.

- MUST NOT add a dependency without a ticket and a second reviewer. Check: `pyproject.toml` has an empty
  `dependencies` list, and CI fails when it changes without the `dependency-approved` label.
- MUST review every new MCP server or plugin with Noura first. Check: the list of approved servers lives in the
  repository, and CODEOWNERS routes any `.mcp.json` change to her.

## 7. Automation

We automate checks, not decisions. A PostToolUse hook runs the formatter and the fast tests after every edit. CI
runs `pytest -q`, the secret scan and the pull-request checks. A scheduled headless run triages new tickets and
writes a comment, nothing more.

We never automate merging to `main`, deploying, any change to the six money modules without a human reviewer, or
anything that needs production credentials.

Every unattended or scheduled run has a cap: `--max-turns 20`, `--max-budget-usd 5` and a 15-minute timeout.
Each run writes a log that is kept for 90 days.

- MUST cap every unattended run with turns, budget and a timeout. Check: the headless wrapper script refuses to
  start without all three flags, and a unit test covers that refusal.
- MUST NOT let an automated job merge or deploy. Check: the bot account has no merge permission, and the branch
  protection settings are audited monthly by Salem.

## 8. Metrics plan

We measure what reaches production and what it costs. We do not measure lines of code, suggestion acceptance or
the share of AI-written code: they reward volume, not delivery. Every metric is reported for AI-assisted pull
requests and for the others separately, using the label, so the team compares them instead of guessing. The
share of AI-assisted pull requests (60% last quarter) is reported and never given a target.

### Lead time for changes
- Kind: delivery
- Definition: Median time from the first commit of a pull request to the moment the deployment that contains it
  reaches production, for the pull requests merged in the week.
- Source: git history and the CI deployment log.
- Cadence: weekly, reviewed by Tariq at the AI-native clinic.
- Baseline: 52 hours (median, last quarter).
- Threshold: Target: a median at or below 48 hours by the end of next quarter.

### Deployment frequency
- Kind: delivery
- Definition: Number of deployments to production per week, counted from the CI deployment log.
- Source: the CI deployment log.
- Cadence: weekly, reviewed by Tariq at the clinic.
- Baseline: 30 deployments in 13 weeks (about 2 a week).
- Threshold: Target: at least 2 a week, never bought by larger pull requests.

### Failed deployment recovery time
- Kind: delivery
- Definition: Median time from the moment a production deployment is declared failed until service is restored by
  a fix or a rollback, for the failures of the quarter.
- Source: the incident tickets in Maha's on-call tool and the CI deployment log.
- Cadence: monthly, reviewed by Maha.
- Baseline: 3 hours.
- Threshold: Target: a median at or below 3 hours.

### Change failure rate
- Kind: guard
- Definition: Deployments to production that needed a hotfix or a rollback, divided by all deployments to
  production in the same four weeks.
- Source: the CI deployment log and the incident tickets.
- Cadence: weekly, reviewed by Tariq; the rolling four-week figure is the one that counts.
- Baseline: 3 of 30 deployments (10%).
- Threshold: Above 15% over any four weeks, we stop raising agent autonomy and review every failed change at the
  next clinic.

### Rework rate
- Kind: guard
- Definition: Unplanned deployments, meaning fixes shipped outside the plan, divided by all deployments to
  production in the quarter.
- Source: the CI deployment log and the ticket board.
- Cadence: monthly, reviewed by Nada.
- Baseline: 4 of 30 deployments (13%).
- Threshold: Above 20% in a quarter, Nada reviews the tests of the changes involved and we add the missing ones.

### Review turnaround
- Kind: guard
- Definition: Median working hours from a pull request being marked ready for review until its first human review
  comment or approval, per week.
- Source: the pull-request timeline in GitHub.
- Cadence: weekly, reviewed by Tariq.
- Baseline: 9 hours.
- Threshold: Over 16 hours in any week, we review the queue at the clinic and cap new agent work until it clears.

### AI-related incidents
- Kind: guard
- Definition: Count of incidents whose postmortem names an AI-assisted change or an agent action as a
  contributing cause, per quarter.
- Source: Maha's postmortems.
- Cadence: quarterly, reviewed by Maha and Tariq.
- Baseline: 0 incidents last quarter, and 1 near miss.
- Threshold: At least 1 in a quarter, we pause raising agent autonomy and run section 9 in full.

## 9. Incident handling

An AI-related incident is any incident in which an agent's action or an AI-assisted change is a contributing
cause. The label on the pull request is where we start looking.

1. Contain, within minutes: stop the agent session, revoke or rotate any credential it could reach, and revert the
   change with `git revert`. Page the on-call engineer.
2. Preserve: before anyone cleans up, copy the session transcript, the agent log and the pull request to the
   incident folder. Local transcripts are deleted after 30 days by default.
3. Report to Maha or the on-call SRE within 1 hour.
4. Run a blameless postmortem within 5 working days. It separates facts, inferences and unknowns, and it states
   what the agent was allowed to do.
5. Encode: every postmortem ends with at least one change to a control (a rule, a hook, a permission, a memory
   line or a test), merged within 10 working days.

- MUST preserve the session transcript and the agent log before cleaning up. Check: the postmortem template has a
  field for the transcript's location, and Maha rejects a postmortem where it is empty.
- MUST end every AI-related postmortem with a control change. Check: the postmortem lists the pull request that
  changed the rule, hook, permission, memory line or test.

## 10. Onboarding

In the first week a new joiner sets up the approved tools with Salem, reads `CONTRIBUTING.md` and `docs/TOUR.md`,
and pairs with a buddy on a first ticket. In the second week they open their first pull request.

First-year engineers work under three extra habits. Before merge they explain the diff back to their buddy in 10
minutes, without notes. In every sprint they do one ticket without an AI tool, so the skill stays theirs. Once a
month they read a module of Remit with a senior and write down what they did not understand. For their first 3
months their AI-assisted pull requests have a named senior reviewer.

- MUST explain every AI-assisted pull request to the buddy before merge for engineers in their first year. Check:
  the buddy ticks "explained back" in the pull-request checklist.
