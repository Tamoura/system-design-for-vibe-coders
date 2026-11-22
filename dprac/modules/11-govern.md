# Module 11 — Governance, risk and security

*Qafila is now Established. About 400 people work there in 35 teams, about 30,000 merchants in four countries use the app, and couriers make about 400,000 deliveries a day. Teams deploy to production many times a day, a data platform feeds every report, and a new integration with a payments partner lets merchants take card and wallet payments inside the app. Before that partner would sign, it sent Qafila a long due-diligence questionnaire: who approves changes, who can reach customer data, how risks are tracked, what evidence exists. Nobody could answer it with one voice, because 35 teams were doing the same things 35 ways. This module follows the work that questionnaire set off, seen mostly through Yasmin, now a senior engineer on Courier Payouts, one of the teams in Qafila's Payments area. First, governance that helps rather than blocks: deciding who decides, and turning rules into automatic guardrails. Second, security and risk as everyday habits of every team: threat modelling a change, rating a risk, writing it down with an owner. Third, compliance and audit without paralysis: knowing your obligations, mapping them to controls, and collecting evidence as a by-product of normal work. Each lesson leaves an artefact: a decision-rights map with a guardrail register, a threat model with risk register entries, and a control-to-evidence map with honest questionnaire answers.*

> **Steps:** Govern — agree who decides what, keep risks visible and owned, and show with evidence that the company does what it says, without slowing the teams that do the work.

---

# 11.1 — Governance that enables: decision rights and guardrails
*Level: 🔴 Advanced* · *Prerequisites: 8.3, 9.1* · *Step: Govern*

**After this you can** sort a set of decisions by how hard they are to reverse and how far their effects reach, write a decision-rights map that names who decides, who must be consulted and what evidence is kept, and turn one manual approval gate into an automatic guardrail with a time-limited exception route. *Study time: reading about 20 min, hands-on about 95 min (estimate).*

## ⚡ In 60 seconds
- **Governance** is how a company decides who makes which decisions, within what limits, and how it checks they were made well. **Management** is making and carrying out those decisions day to day.
- **Decision rights** say, for each kind of decision, who decides, who must be consulted and who is told.
- A **guardrail** is a built-in, usually automatic check that blocks only what is clearly unsafe; a **gate** stops work until a person approves. Good governance uses many guardrails and few gates.
- The rule that matters most: **decide who decides, then make the safe way the default way.**
- Decision cue: the harder a decision is to reverse and the further its effects reach, the higher and slower it should be made.
- Biggest trap: answering a scare or an outside request by adding a central approval step for everything.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

The payments partner's questionnaire held about 200 questions. Question 14 read: "Describe who approves changes to production systems that process payment data, and how approvals are recorded." Faisal, now Head of Engineering, answered from memory: "All production changes are approved by the Head of Engineering." Salma, who leads service and reliability, pointed out that 35 teams deploy many times a day and Faisal had not approved a change in two years. The answer was untrue.

Dana, the security and risk lead, asked the seven teams that touch payments how a change reaches production, and got seven answers. One let engineers merge their own "small" changes. One had a shared emergency admin account whose password four people knew.

Faisal's reflex was a weekly change board. Salma counted about 140 changes to payment services in the previous month: a weekly board would batch them into large, risky releases. Maha, the CEO, asked instead for a one-page map of who decides what, and the checks that would make the honest answer to question 14 a good one. Yasmin drafted it with Dana.

## 📐 How it works

### 🟢 The essentials

**Governance is not bureaucracy.** Its job is to make sure the right people make the right decisions, within agreed limits, and that the company can show this happened. Peter Weill and Jeanne Ross's book *IT Governance* (2004) is widely cited for defining IT governance as "specifying the decision rights and accountability framework to encourage desirable behavior in the use of IT" (as reported in summaries of the book). Governance that people route around has failed at that job. Governance asks "who may decide whether we store card data?"; management asks "shall we store it for this feature?"

**Decision rights.** For each important kind of decision, write down:

- **Decides:** one person or role. Not a committee, unless it truly votes.
- **Must consult:** people whose knowledge is needed *before* the decision. Their view is heard; they cannot block.
- **Informed:** people told *after*, so they can adapt.
- **Evidence:** the record that shows how it was decided (a merged pull request, a ticket, a decision record).

A required approval is not consulting. If the pipeline will not merge a change until a code owner approves, that approver can block it, so the approving role goes under Decides as the one accountable decider; the author proposes. A **RACI chart** (Responsible, Accountable, Consulted, Informed) is a popular format; keep exactly one "Accountable" per decision.

**Sort decisions before you assign them.** Two questions, extending the reversibility idea from lesson 9.1:

| | Easy to reverse | Hard to reverse |
|---|---|---|
| **Effects stay inside the team** | Team decides, now. (Change a dashboard.) | Team decides, writes it down. (Change its own database schema.) |
| **Effects reach other teams, customers or partners** | Team decides within guardrails, informs others. (Deploy a feature behind a flag.) | Named owner decides after consulting; decision record kept. (Store a new kind of personal data.) |

**Guardrails and gates.** A **gate** stops work until a person says yes. A **guardrail** is a check built into the path of the work that lets safe work through and stops only what is clearly unsafe. Three kinds (lesson 8.3 introduced the idea):

| Kind | What it does | Qafila example |
|---|---|---|
| **Preventive** | Stops the unsafe thing happening | The pipeline refuses to merge a change with no approving review from a second engineer |
| **Detective** | Notices it soon after | A nightly job flags any cloud storage bucket that is readable by the public |
| **Corrective** | Puts it right | A failed health check after a deploy rolls the change back automatically |

Keep gates for rare, high-impact, hard-to-reverse decisions: signing a payments partner contract, not the fortieth small deploy of the day.

**Layers of rules.** A **principle** says why ("customer money and data are handled as if they were our own"). A **policy** says briefly what must be true ("every production change is reviewed by someone other than its author"). A **standard** gives the checkable how ("the pipeline requires one code-owner approval"). A **guideline** recommends without requiring ("keep pull requests small"). A policy nobody can quote is not governing anything.

**Exceptions.** An **exception** is permission to break a rule for a stated reason, for a limited time, with an owner and, where possible, a **compensating control** (another safeguard covering the same risk). Keep them in a register with end dates; an exception with no end date is a new, unwritten rule.

### 🟡 Going deeper

**Why central approval often disappoints.** DORA (DevOps Research and Assessment, a research programme now part of Google Cloud) reports on its "streamlining change approval" page that heavyweight approval by people outside the team is associated with worse delivery performance, that its research found no evidence such approval lowers the rate of failed changes, and that peer review backed by automated checks works better (as reported in search summaries of the page). The book *Accelerate* (Forsgren, Humble and Kim, 2018) reported similar findings. These describe the organisations surveyed, not a law. For the manager's view, see [*Running IT as a Business*, lesson 6.2 — Change control that protects stability without stopping flow](../itbiz/index.html#/6.2).

**Federated governance.** In **federated governance**, a small central group (here Dana's team, the platform team and the architecture group) sets a short list of non-negotiable guardrails and provides tools that make them easy; teams decide everything else. Test for the list: would breaking this rule harm customers, partners or the company, and is it hard to undo?

**A decision-rights map in practice.** Part of Yasmin and Dana's map (illustrative):

| Decision | Decides | Must consult | Informed | Guardrail or evidence |
|---|---|---|---|---|
| Deploy a change to a payment service | An approving code owner other than the author (the author proposes; the pipeline enforces it) | — | Team channel (automatic) | Merge blocked without code-owner approval; deploy log |
| Add a new kind of personal or payment data | Data owner (lesson 9.2) | Dana's team; Hamad (data) | Payments partner if in contract scope | Decision record; data inventory updated |
| Grant production access to a payment system | System owner | — | Dana's team (automatic report) | Access ticket with end date; quarterly review |
| Accept a known security risk (any length; never beyond 30 days for money or payment data) | Head of the affected product area | Dana | Risk committee | Risk register entry with owner and review date |
| Change the payout calculation | Head of Payments | Bilal (finance); Salma (support) | All merchant-facing teams | Decision record; test evidence in pull request |

Faisal's name appears nowhere: he sets the guardrails; he does not approve the changes.

**Policy as code.** Many guardrails can be code that a machine checks, such as branch protection, or a rule in a policy engine like Open Policy Agent (an example, not an endorsement) that rejects a deployment with no owner label. Such rules are consistent, versioned and leave evidence. See [*Cloud & DevOps: Zero to Hero*, lesson 3.3 — Policy as code, drift and guardrails](../cloud/index.html#/3.3).

### 🔴 Expert view

**Measure the governance itself.** Watch how long decisions take, how many exceptions are open or overdue, and where people work around a rule. A rising exception count usually means a rule is wrong.

**Separation of duties without a gate.** Partners often ask that a change's author is not its only approver. Pipeline-enforced peer review that admins cannot skip without a record is a common answer; ask the partner early whether it satisfies them, with sample evidence in hand.

**The memorable rule.** Decide who decides, then make the safe way the default way.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Decision sorting grid** | Two questions (beyond the team? hard to reverse?) that place a decision in one of four boxes | Before assigning who decides |
| **Decision-rights map** | Decisions with decides, must consult, informed and evidence | When people disagree about who may decide, or an outside party asks |
| **Guardrail register** | Automatic checks: what each prevents or detects, where it runs, its owner | When you replace gates, or must show how a policy is enforced |
| **Exception register** | Approved breaks of a rule, with owner, compensating control and end date | Whenever someone must break a rule for a good reason |

## 🏛️ In practice at Qafila
Yasmin's draft for the payments area. Illustrative and fictional.

> **Payments area: decision rights and guardrails (v2)**
>
> **Policies (3).** (1) Every production change is reviewed by someone other than its author. (2) Nobody has standing access to production payment data; access is requested, time-limited and logged. (3) Every known risk we choose not to fix now has a named, written accepter from the day it is found; risks to money or payment data are never accepted for more than 30 days.
>
> | Guardrail | Kind | Where | Owner |
> |---|---|---|---|
> | Merge needs one code-owner approval; no self-approval; admin bypass raises an alert | Preventive | Version control host | Platform team |
> | Pipeline blocks a merge that contains a secret | Preventive | CI | Platform team |
> | Production access for at most 8 hours through the access tool; every session logged | Preventive and detective | Access tool | Dana's team |
> | Weekly report of anyone with standing production access | Detective | Access tool | Dana's team |
> | Failed health check after deploy triggers rollback | Corrective | Deploy tool | Each team |
>
> **Removed.** The shared emergency admin account, replaced by a "break-glass" role (the emergency role from lesson 4.1, now widened from two named people to anyone on call): anyone on call can take it, it pages Dana's team, and every use is reviewed within two working days.
>
> **Exception open.** The legacy payout reconciliation job runs under a broad **service account** (an account used by a program, not a person) until its rewrite. Owner: Payments lead; compensating control: daily log review; end date: end of next quarter.
>
> **Answer to question 14 (draft).** "Changes are proposed as pull requests and must be approved by a second engineer who is a designated code owner before the pipeline will merge them; the pipeline also runs tests and secret scanning. Approvals and deploys are recorded in the version control host and the deploy log. Emergency access uses a logged break-glass role reviewed within two working days."

Instead of the board, Dana sampled 20 pull requests a month for a quarter. Salma noted the shared account had been used because the access tool was slow: the break-glass role was the fix, not a reprimand.

## 🛠️ Exercises
**🟢 Sort eight decisions.** Use the sorting grid on these Qafila decisions: (1) rename a field in an internal dashboard; (2) start storing couriers' national ID numbers; (3) deploy a bug fix behind a feature flag; (4) switch the main database to a different engine; (5) change a team's own on-call rota; (6) give a contractor read access to production order data; (7) change the refund rules shown to merchants; (8) upgrade a test library used by one team.
*Done when:* each decision has a box and one named role as decider, with a one-line reason for the two you found hardest.

<details><summary>Model answer and self-check</summary>

**Model answer.** (1) Inside, easy: the engineer making it. (2) Beyond, hard: data owner, after consulting security and a legal adviser. (3) Beyond, easy: the engineer making it, within guardrails; support informed. (4) Beyond, hard: named architecture owner, decision record (lesson 9.1). (5) Inside, easy: the team lead. (6) Beyond, hard (data seen cannot be unseen): system owner, time-limited and logged. (7) Beyond, hard (easy to change in code, hard to undo in merchants' trust): product owner, after consulting support and finance; decision record kept. (8) Inside, easy: the engineer making it.

**Self-check.**
- Did you name one role, not a group such as "the team"?
- Did you treat access to data as hard to reverse?
- Did anything end up at the CEO that a named owner could decide?

</details>

**🟡 Write a decision-rights map for one area.** Pick a personal or open-source project, a student society, or Qafila's Merchant Orders team. List five recurring decisions and fill the columns: decides, must consult, informed, guardrail or evidence.
*Done when:* every row has exactly one accountable decider and an "informed" entry, at least three rows have evidence a stranger could check, and one row is enforced by a machine.

<details><summary>Model answer and self-check</summary>

**Model answer (open-source library).** Merge a pull request: a maintainer other than the author (the author proposes); consult: —; informed: watchers; guardrail: CI must pass; evidence: approved pull request. Release a major version: lead maintainer; consult: maintainers and top users; informed: all users via release notes; evidence: changelog. Add a dependency: reviewing maintainer; consult: the maintainer who looks after security; informed: maintainers; guardrail: dependency scanner. Grant commit rights: lead maintainer; consult: maintainers; informed: contributors; evidence: issue. Change the licence: lead maintainer; consult: maintainers, contributors and a licensing adviser; informed: all users; evidence: issue and commit.

**Self-check.**
- Are only people under "must consult", with tools and checks under guardrail?
- Could a newcomer find each piece of evidence alone?
- Is there exactly one accountable decider per row, with the author shown as proposer, not decider?

</details>

**🔴 Turn a gate into a guardrail.** Choose a manual approval (for example "a security engineer approves every change to the login code"). Write the risk it reduces; one preventive and one detective guardrail for that risk; what still needs a person; and an exception route.
*Done when:* the risk is one sentence, both guardrails run without anyone waiting, the human step covers only a small named class of changes, and the exception has an owner and a maximum length.

<details><summary>Model answer and self-check</summary>

**Model answer.** Risk: a change weakens a login check and lets someone into another account. Preventive: a code-owner rule requires an identity-team approval on login code, and authentication tests must pass. Detective: alerts on unusual login patterns after each deploy. Still human: changes to the login design (a new login method, a new session length) get a short threat model (lesson 11.2) reviewed by Dana's team. Exception: during an incident with the identity team unavailable, the on-call engineer may merge with any reviewer; the identity team reviews within two working days, the exception's maximum length; owner Dana.

**Self-check.**
- Does each guardrail reduce the same risk as the gate?
- Is the human step kept only where judgement is needed?
- Would the route have handled the night-time use of the shared account?

</details>

## ⚠️ Mistakes and traps
- **Answering with what you wish were true.** Find out what happens, improve it, then answer.
- **A central gate after every scare.** Ask what automatic check would stop the specific failure.
- **Committees as deciders.** Name one accountable role; the board can be consulted.
- **Rules without reasons or end dates.** Write the risk each rule reduces and a review date.
- **Exceptions that never expire.** Give each an owner, a compensating control and an end date.

## 🧾 Recap
- Governance decides who decides and how the company checks; management makes the decisions.
- A decision-rights map names one decider, who is consulted and informed, and the evidence kept.
- Sort decisions by reach and reversibility; most belong to the team, within guardrails.
- Prefer preventive, detective and corrective guardrails; keep gates for rare, hard-to-reverse decisions.
- Rule: decide who decides, then make the safe way the default way.

## ✍️ Check yourself
**1. After the questionnaire arrives, Faisal proposes a weekly board to approve every change to payment services. Which response best fits this lesson?**

- A. Accept it, because a central board is the only reliable way to prove approvals to a partner.
- B. Ask which risk it reduces, and use review and pipeline checks that stop that risk without a wait.
- C. Accept it, but let the board approve urgent changes by email between its weekly meetings.
- D. Reject it, and let each team keep its own approval habits as long as nothing goes wrong.

<details><summary>Answer</summary>

**B.** Name the risk, then find guardrails that reduce it without batching changes. A assumes a board proves more than a recorded review, C still batches most changes and adds an unrecorded side route, and D keeps the seven inconsistent habits. See "Guardrails and gates" and "Why central approval often disappoints".

</details>

**2. Which of these is a detective guardrail?**

- A. The pipeline refuses to deploy infrastructure code that creates unencrypted storage.
- B. A script puts back the approved firewall settings whenever someone changes them by hand.
- C. A team guideline suggests keeping pull requests small enough to review in twenty minutes.
- D. A weekly report lists every account that still has standing access to production systems.

<details><summary>Answer</summary>

**D.** It notices an unsafe state after it has happened. A is preventive, B is corrective, and C is a guideline, which enforces nothing. See "Guardrails and gates" and "Layers of rules".

</details>

**3. Yasmin's draft map lists "the architecture board" as the decider for adding a new kind of personal data. What should she change?**

- A. Name one accountable role, such as the data owner, and list the board as consulted.
- B. Keep the board, since a group decision spreads the responsibility across several experts.
- C. Move the decision to the CEO, because personal data is a company-wide concern.
- D. Let each team decide, because the data owner already appears in the data inventory.

<details><summary>Answer</summary>

**A.** Each decision needs one accountable decider; experts are consulted. B is the committee trap, C moves the decision far from the knowledge, and D ignores that the decision reaches beyond one team and is hard to reverse. See "Decision rights".

</details>

**4. Salma finds the shared emergency admin account was used at night because the access tool takes an hour to grant access. What is the best response?**

- A. Disable the account at once and warn the engineers involved that its use breaks policy.
- B. Keep the account but change its password monthly and share it only with team leads.
- C. Replace it with a logged break-glass role anyone on call can take, reviewed afterwards.
- D. Add a manager's sign-off to every emergency access request, including those at night.

<details><summary>Answer</summary>

**C.** The workaround shows the access path is too slow; a fast, logged role fixes the cause and leaves evidence. A punishes the symptom, B keeps a shared secret with no record of use, and D adds a gate when speed matters most. See "In practice at Qafila".

</details>

**5. A team needs to break the "no broad service accounts" policy for a legacy job until it is rewritten. What makes this exception well governed?**

- A. Approval by the Head of Engineering, recorded in an email to the team's lead.
- B. An owner, a compensating control and an end date, recorded in the exception register.
- C. A note in the code next to the job, so future engineers understand why it is different.
- D. Agreement in the team's retrospective, since the team knows the legacy job best.

<details><summary>Answer</summary>

**B.** A good exception is visible, owned, time-limited and covered by another safeguard. A sets no limit, C is reviewed by nobody, and D keeps inside one team a risk that reaches further. See "Exceptions".

</details>

## 📚 References
- DORA, "Capabilities: Streamlining change approval": https://dora.dev/capabilities/streamlining-change-approval/ — findings on external approval and peer review. Reported from search summaries; the page could not be opened from this environment on 2026-11-22.
- Forsgren, N., Humble, J. and Kim, G., *Accelerate: The Science of Lean Software and DevOps* (IT Revolution, 2018). Full citation; findings on change approval as reported in summaries; not opened.
- Weill, P. and Ross, J. W., *IT Governance: How Top Performers Manage IT Decision Rights for Superior Results* (Harvard Business School Press, 2004). Source of the quoted definition as reported in summaries; not checked against the book.
- Library course: [*Running IT as a Business*, lesson 6.2 — Change control that protects stability without stopping flow](../itbiz/index.html#/6.2).
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 3.3 — Policy as code, drift and guardrails](../cloud/index.html#/3.3).
- Library course: [*Running IT as a Business*, lesson 10.3 — Risk, controls and audit in a regulated bank](../itbiz/index.html#/10.3) (the operating-model view of the same questions).

---

# 11.2 — Security and risk in everyday practice
*Level: 🔴 Advanced* · *Prerequisites: 3.1, 9.2, 11.1* · *Step: Govern*

**After this you can** run a short threat model on a planned change using four questions, rate each risk you find by likelihood and impact, choose a treatment (reduce, avoid, transfer or accept), and write risk register entries with an owner, a due date and a review date that a security lead could act on. *Study time: reading about 20 min, hands-on about 100 min (estimate).*

## ⚡ In 60 seconds
- **Security** is protecting the **confidentiality** (only the right people see it), **integrity** (it is correct and not tampered with) and **availability** (it works when needed) of systems and data.
- **Risk** is the chance that something bad happens, combined with how bad it would be. You choose which risks to reduce, avoid, transfer or accept, and write the choice down.
- Most security work is everyday habit, done by every team, plus a few minutes of threat thinking before building.
- The rule that matters most: **ask "what can go wrong?" before you build, and give every risk an owner.**
- Decision cue: if a change touches money, personal data, logins or access rights, spend fifteen minutes on a threat model first.
- Biggest trap: treating security as the security team's job. A few specialists cannot review 35 teams' work.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

The partner's questionnaire asked: "How do development teams identify security risks in new features? Provide two recent examples." Dana's risk list had 14 rows, most written after incidents. Teams had no habit of looking for risks before building.

The same month, Yasmin reviewed a pull request from a newer engineer on Courier Payouts. It added a page showing a courier's weekly earnings; its address ended with the courier's ID number. Yasmin changed the number by one in her test environment and saw another courier's earnings, name and the last digits of their bank account. The code passed every test, because every test used the right courier.

The fix took an hour; finding it took luck. Dana told Maha that every team needed a cheap, repeatable way to ask what could go wrong, and a shared place to record it.

## 📐 How it works

### 🟢 The essentials

**A few words that matter.**

| Term | Plain meaning | Courier earnings example |
|---|---|---|
| **Asset** | Something of value to protect | Couriers' earnings and bank details |
| **Threat** | Someone or something that could cause harm | A courier curious about others' pay; an outsider with one courier's login |
| **Vulnerability** | A weakness a threat could use | The page trusts the ID in the address without checking who is asking |
| **Control** | A safeguard that reduces risk | A server-side check that the logged-in courier owns the requested ID |
| **Risk** | Likelihood that harm happens, combined with its impact | Likely (easy to try), high impact (personal and financial data) |
| **Trust boundary** | A point where data or requests pass between parts that trust each other differently | Between a courier's phone and Qafila's server: the server must not simply believe what the phone sends |

The earnings page is served by an **endpoint**: one address in Qafila's **API** (application programming interface, the set of addresses that programs call to ask for data or actions). The weakness has a name: **broken access control**, where the system checks that you are logged in but not that you may see *this* record. See [*Application & AI Security*, lesson 3.3 — Authorisation: broken access control, IDOR and multi-tenancy](../secai/index.html#/3.3).

**Everyday security habits.** Verizon's annual Data Breach Investigations Report (DBIR) analyses thousands of reported breaches. Its 2026 edition, covering November 2024 to October 2025, reported that exploiting a vulnerability (31% of breaches) had overtaken credential abuse (13%) as the most common way in, for the first time in the report's history (as reported in Verizon's announcement and press coverage). That describes its dataset, not your company's future, but it points at ordinary habits:

| Habit | What it means in practice | Earlier lesson |
|---|---|---|
| **Least privilege** | Only the access needed, for as long as needed | 7.2, 11.1 |
| **No secrets in code** | Keys in a secret store; the pipeline blocks any that slip in | 2.3, 8.3 |
| **Reviewed changes** | A second person reads every change | 3.1 |
| **Patched dependencies** | Scanning flags weak libraries; fixes scheduled by severity | 3.2 |
| **Strong login** | Multi-factor authentication (a second proof besides the password, such as a code from an app) for staff | — |
| **Useful logs** | Who did what and when, without secrets | 4.2, 9.2 |

**Threat modelling in fifteen minutes.** **Threat modelling** is thinking through how a system could be attacked or fail, before you build it. The Threat Modeling Manifesto, written by practitioners, uses four questions (as reported in summaries and in the OWASP Threat Modeling Cheat Sheet):

1. **What are we working on?** Draw the change: who uses it, what data flows where, and where the trust boundaries are.
2. **What can go wrong?** List ways it could be misused or fail.
3. **What are we going to do about it?** Choose controls, or decide to accept a risk.
4. **Did we do a good enough job?** Check the controls exist and the list was sensible.

For question 2, a prompt list helps. **STRIDE**, which originated at Microsoft, names six kinds of threat: Spoofing (pretending to be someone), Tampering (changing data), Repudiation (denying an action with no record to prove it), Information disclosure (seeing what you should not), Denial of service (making it unavailable) and Elevation of privilege (gaining more rights than given). Read each word and ask "could this happen here?" See [*Application & AI Security*, lesson 1.1 — Threat modelling: data flows, trust boundaries and STRIDE](../secai/index.html#/1.1).

**Rating a risk.** Use two simple scales.

| Level | Likelihood | Impact |
|---|---|---|
| Low | Needs rare skill or access | Minor inconvenience; no personal or money data |
| Medium | Possible with some effort; seen elsewhere | Some customers affected; limited data; recoverable |
| High | Easy to try; anyone who looks could find it | Many customers, money or sensitive personal data; partner or regulator interest |

High with high goes first; the point is ordering, not precision. For CVSS (the Common Vulnerability Scoring System), see [*Application & AI Security*, lesson 1.3 — Rating and prioritising risk: likelihood, impact and CVSS](../secai/index.html#/1.3).

**Four ways to treat a risk.**

| Treatment | Meaning | Example |
|---|---|---|
| **Reduce** | Add a control | Check ownership on the server |
| **Avoid** | Stop doing the risky thing | Do not show bank details at all |
| **Transfer** | Move part of the impact elsewhere, by contract or insurance | The payment provider holds card details |
| **Accept** | Knowingly live with it for now | A low-impact display bug in an internal tool |

Transfer moves some consequences, not the duty to care. Acceptance counts only when someone with the authority to accept it (lesson 11.1) does so in writing, with a date to look again.

### 🟡 Going deeper

**The risk register.** A **risk register** is the shared list of known risks, each with enough detail to act on:

| Field | Example |
|---|---|
| **ID and title** | R-112: Courier earnings visible to other couriers |
| **Description** | Earnings page trusted the courier ID in the address; any logged-in courier could view others' earnings and partial bank details |
| **Likelihood / impact / rating** | High / High / High (before fix) |
| **Treatment and controls** | Reduce: server-side ownership check; test for access to another courier's record; bank digits removed from page |
| **Owner** | Courier Payouts team lead |
| **Due date** | Fix deployed within 2 days |
| **Residual rating and review date** | Low; review at next quarterly access-control check |
| **Status** | Closed after fix verified; class-wide test added to the service template |

The **owner** is usually the leader of the team that owns the system, not the security team, which keeps the register healthy and helps.

**Risk appetite.** **Risk appetite** is how much risk leaders are willing to accept. Qafila's leadership wrote three lines: "We accept small product risks to learn fast. We do not accept known risks to customer money or payment data beyond 30 days. We do not accept risks that would breach our obligations to partners or regulators."

**Vulnerability management.** This is the routine for known weaknesses: find, rate, fix within a time limit set by severity, and verify. Qafila's internal targets (illustrative, not a standard): critical within 7 days, high within 30, medium within 90 (30 for systems handling money or payment data), with exceptions recorded as in lesson 11.1. Measure the share fixed on time. See [*Application & AI Security*, lesson 10.3 — Vulnerability management, disclosure and bug bounties](../secai/index.html#/10.3).

**Security champions.** Many companies name a **security champion** in each team: an engineer with extra training who runs its threat models. Yasmin became Courier Payouts' champion. Champions carry specialists' knowledge into teams; they do not replace specialists.

### 🔴 Expert view

**Threat model the change, not the company.** Whole-system models go stale. Short models attached to significant changes (new data, access paths, suppliers, money flows) stay current; link them from the pull request.

**Turn every finding into a test or a guardrail.** Yasmin's fix included a test that asks for another courier's record and expects a refusal. Dana asked the platform team to add the same test to the service template for every endpoint that takes an ID. A test is fixed once; a memo is fixed until someone forgets. See [*Software Testing*, lesson 4.2 — Security testing for testers: OWASP, SAST, DAST, dependency scanning, fuzzing and authorisation tests](../testing/index.html#/4.2).

**The memorable rule.** Ask "what can go wrong?" before you build, and give every risk an owner.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Four-question threat model** | What are we working on, what can go wrong, what will we do, did we do enough | Before building a change that touches money, personal data, logins or access |
| **STRIDE prompt list** | Six kinds of threat to read through | During question 2 of a threat model |
| **Likelihood and impact scales** | Three levels each, combined into a rating | To order risks before deciding what to fix first |
| **Risk register entry** | ID, description, rating, treatment, owner, dates, residual rating | Whenever a risk is not fixed at once, or is accepted |
| **Risk appetite statement** | A few lines from leadership on which risks are acceptable | When a team must decide quickly whether to accept a risk |

## 🏛️ In practice at Qafila
Yasmin's threat model for the payments partner integration, which she led for the Payments area as a security champion. Illustrative and fictional; shortened.

> **Threat model: merchant card payments through the payments partner (v1)**
>
> **1. What are we working on?** Merchants turn on "accept cards". Customers pay on the courier's handheld or a payment link. The partner processes the card and sends Qafila a result and, next day, a **settlement file** (the partner's list of payments it is paying out to Qafila). Qafila never sees full card numbers; it stores a partner reference, amount and status. Trust boundaries: merchant app ↔ Qafila API; Qafila ↔ partner API; partner → Qafila notifications.
>
> **2. What can go wrong? (STRIDE)**
>
> | # | Threat | Likelihood | Impact | Rating |
> |---|---|---|---|---|
> | T1 | Spoofing: a fake "payment succeeded" notification marks an unpaid order as paid | Medium | High | High |
> | T2 | Tampering: a merchant changes the amount between order and payment | Medium | Medium | Medium |
> | T3 | Repudiation: a merchant disputes enabling card payments and we cannot show who turned it on | Medium | Medium | Medium |
> | T4 | Information disclosure: partner API key leaks from logs or code | Low | High | Medium |
> | T5 | Denial of service: partner outage blocks all deliveries, not just card payments | Medium | High | High |
>
> **3. What are we going to do?** T1: verify the partner's signature on every notification and confirm status with the partner's API. T2: amount fixed server-side from the order. T3: log who enabled card payments, when and from which device. T4: key in the secret store, rotated; log scrubbing tested. T5: if the partner is down, orders continue with "pay on delivery"; Salma's team adds it to the runbook. (All reduce.)
>
> **4. Did we do enough?** Tests for T1 and T2 are in the pipeline. Dana's team reviewed the model and added: a merchant's staff member with a stolen login changes the payout bank account (R-131, owner Payments lead).

Faisal said the partner "handles security". Dana pointed out that T1, T2 and T5 sit on Qafila's side of the boundary.

## 🛠️ Exercises
**🟢 Name the parts.** A Qafila merchant can export its order history as a spreadsheet that includes customers' phone numbers. The export is downloaded from a link that never expires and works for anyone who has it. Write one line each for the asset, two threats, the vulnerability, one control that would fix it and one control that would catch the same problem in future exports.
*Done when:* each line uses the lesson's definitions correctly, and your "future" control could run without a curious reviewer.

<details><summary>Model answer and self-check</summary>

**Model answer.** Asset: customers' phone numbers. Threats: a former staff member who kept the link; anyone it is forwarded to. Vulnerability: the link never expires and does not check who is asking. Fix: links that expire within hours and need the merchant's login, or leave phone numbers out (avoid). Future control: a template test that fails if a download link works without login or after expiry.

**Self-check.**
- Did you keep threat (who) and vulnerability (which weakness) separate?
- Would your future control work on every export, not only this one?

</details>

**🟡 Threat model a small feature.** Use your own project, or this Qafila feature: "merchants invite staff by email link, as 'orders only' or 'full access'". Answer the four questions, using STRIDE, and rate four threats.
*Done when:* you name the trust boundaries, give four threats with a STRIDE letter and rating, one treatment each, and one way to check the controls work.

<details><summary>Model answer and self-check</summary>

**Model answer (staff invitations).** Owner sends an invite link; staff member sets a password and gets a role. Boundaries: email ↔ Qafila; staff device ↔ API. (S) A forwarded link lets someone join: medium/high; single-use links expiring in 24 hours (reduce). (E) "Orders only" staff call the payouts endpoint directly: medium/high; role checked on the server, a test per role (reduce). (R) Owner denies granting full access: medium/medium; log role grants (reduce). (I) Invite email previews shop revenue: low/medium; no business data in emails (avoid). Check: role tests in the pipeline.

**Self-check.**
- Is every "reduce" a specific control, not "be careful"?
- Are roles checked on the server, not only by hiding buttons?

</details>

**🔴 Write and defend three register entries.** From your threat model (or Yasmin's), write three entries with all fields. Make one an accepted risk, written by the accountable person: what, why, until when, and what triggers an early look.
*Done when:* each entry has one owner who leads the affected system, a due or review date and a residual rating; the accepted risk has a named accepter with authority under lesson 11.1, an end date within 30 days if it touches money, and a trigger for early review.

<details><summary>Model answer and self-check</summary>

**Model answer (accepted entry).** R-131: stolen merchant staff login used to change the payout bank account. Medium / high / high. Treatment: reduce (second-channel confirmation of bank changes; first payout to a new account held 24 hours). Owner: Payments lead. Due: 3 weeks. Acceptance: "I, Head of Payments, accept that for up to 21 days bank changes rely on login only, because the fix needs partner changes. Compensating control: support reviews a daily report of bank changes. Look again at once if a merchant reports an unexpected change." Residual: low; review quarterly.

**Self-check.**
- Is the owner the system's leader, not "security"?
- Does the acceptance have a time limit and a compensating control?
- Did you stay within the risk appetite, or escalate where you could not?

</details>

## ⚠️ Mistakes and traps
- **"Security will check it."** Each team runs its own threat models; specialists review the high-risk ones.
- **Hiding buttons instead of checking on the server.** Anyone can call an API directly.
- **Accepting risk by silence.** An unfixed risk with no written acceptance is owned by nobody.
- **Assuming a supplier or partner covers it.** Map the trust boundary; your side is yours.
- **Fixing the instance, not the class.** Add a test or guardrail for the whole class.

## 🧾 Recap
- Security protects confidentiality, integrity and availability; risk combines likelihood and impact.
- A fifteen-minute threat model with four questions and STRIDE finds the obvious risks before code exists.
- Rate risks simply, choose a treatment, and record each with a single owner and a date.
- Rule: ask "what can go wrong?" before you build, and give every risk an owner.

## ✍️ Check yourself
**1. In Yasmin's courier earnings case, which of these is the vulnerability?**

- A. A courier who is curious about how much colleagues earn each week.
- B. The couriers' weekly earnings and the last digits of their bank details.
- C. The page trusted the courier ID in the address without checking ownership.
- D. A server-side check that the logged-in courier owns the requested record.

<details><summary>Answer</summary>

**C.** A vulnerability is the weakness a threat could use; A is a threat, B the asset, D the control. See "A few words that matter".

</details>

**2. Faisal says the payments partner "handles security" for card payments. In Yasmin's threat model, why is that not enough?**

- A. Several threats, such as fake success notifications, sit on Qafila's side of the trust boundary.
- B. The partner's controls are likely weaker than Qafila's, so Qafila should keep card numbers too.
- C. The partner's contract usually leaves card security to merchants, so Qafila should accept it.
- D. Dana's team reviews payment risks, so partner controls are better left out of the model.

<details><summary>Answer</summary>

**A.** The boundary shows risks only Qafila can fix. B adds risk by storing card data, C rests on a claim the lesson does not make, and D repeats the "security will check it" trap. See "In practice at Qafila".

</details>

**3. A risk to merchant payouts cannot be fixed for three weeks. Qafila's appetite allows up to 30 days for money risks. What should happen now?**

- A. Nothing yet, because it is still inside the 30 days the risk appetite allows for money risks.
- B. Dana's team takes ownership of the risk until the fix ships, since they understand it best.
- C. The team delays the fix until the next quarter so it can be bundled with related work.
- D. The accountable lead accepts it in writing with a compensating control and end date.

<details><summary>Answer</summary>

**D.** Every unfixed risk needs a written accepter from day one (policy 3 in lesson 11.1); 30 days is only the ceiling for money risks. A is accepting by silence, B moves ownership away from the system's leader, and C breaks the appetite. See "Four ways to treat a risk" and "Risk appetite".

</details>

**4. After fixing one endpoint that leaked another courier's data, what does this lesson suggest next?**

- A. Send a memo to all engineers reminding them to check ownership on every endpoint.
- B. Add a template test asking for another user's record, so every endpoint is checked.
- C. Ask Dana's team to read every new endpoint before release for the next three months.
- D. Lower the rating to low and leave other endpoints for the next quarterly review.

<details><summary>Answer</summary>

**B.** A test fixes the whole class and keeps working. A relies on memory, C is a bottleneck gate, and D leaves the flaw open elsewhere. See "Turn every finding into a test or a guardrail".

</details>

**5. Citing the 2026 DBIR finding, a team lead proposes dropping multi-factor authentication for staff to spend the time on patching. What is the best reading?**

- A. Agree, since the finding shows stolen credentials have stopped mattering in breaches.
- B. Keep it and patch faster too, since the finding ranks the entry routes and retires none.
- C. Agree for internal tools only, since the report studied mainly customer-facing systems.
- D. Change nothing until next year's edition confirms the finding with another year of data.

<details><summary>Answer</summary>

**B.** The report describes how often each route appeared in its dataset; credential abuse was still a common route. A turns "no longer the most common" into "irrelevant", C relies on a claim the lesson does not make, and D ignores a finding that supports better patching now. See "Everyday security habits".

</details>

## 📚 References
- Threat Modeling Manifesto: https://threatmodelingmanifesto.org/ — the four key questions. Reported from search summaries; the page could not be opened from this environment on 2026-11-22.
- OWASP, Threat Modeling Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html — lists the four questions and STRIDE. Reported from search summaries; not opened.
- Verizon, "Vulnerability exploitation top breach entry point, 2026 industry-wide DBIR finds": https://www.verizon.com/about/news/breach-industry-wide-dbir-finds — 31% vulnerability exploitation versus 13% credential abuse; data period November 2024 to October 2025. Reported; confirmed by multiple secondary sources (SecurityWeek; Help Net Security, 20 May 2026) via search on 2026-11-22; not opened.
- Shostack, A., *Threat Modeling: Designing for Security* (Wiley, 2014). Full citation; not opened.
- Library course: [*Application & AI Security*, lesson 1.1 — Threat modelling: data flows, trust boundaries and STRIDE](../secai/index.html#/1.1).
- Library course: [*Application & AI Security*, lesson 1.3 — Rating and prioritising risk: likelihood, impact and CVSS](../secai/index.html#/1.3).
- Library course: [*Application & AI Security*, lesson 3.3 — Authorisation: broken access control, IDOR and multi-tenancy](../secai/index.html#/3.3).
- Library course: [*Application & AI Security*, lesson 10.3 — Vulnerability management, disclosure and bug bounties](../secai/index.html#/10.3).
- Library course: [*Software Testing*, lesson 4.2 — Security testing for testers: OWASP, SAST, DAST, dependency scanning, fuzzing and authorisation tests](../testing/index.html#/4.2).

---

# 11.3 — Compliance and audit without paralysis
*Level: 🔴 Advanced* · *Prerequisites: 11.1, 11.2* · *Step: Govern*

**After this you can** list the obligations that apply to a product (laws, contracts and standards) as questions for the right adviser, map each obligation to a control and to evidence that the normal work already produces, answer a due-diligence question honestly with a gap and a plan where needed, and prepare for an audit without stopping delivery. *Study time: reading about 20 min, hands-on about 100 min (estimate).*

## ⚡ In 60 seconds
- **Compliance** means meeting obligations the company has taken on or is subject to: laws, contracts, industry standards and its own policies. **Audit** is an independent check, based on evidence, that controls exist and work.
- Compliance is not the same as security. You can be compliant and insecure, or secure and unable to prove it. Aim for real controls, then evidence.
- A **control** is a safeguard with an owner; **evidence** is a record that shows the control worked, at a given time, for a given case.
- The rule that matters most: **build evidence into the work, not on top of it.**
- Decision cue: before writing a new document for an audit, ask whether an existing system record already shows the same thing.
- Biggest trap: answering questionnaires with what you hope is true. An honest "partly, with a plan and a date" builds more trust than a "yes" an audit later disproves.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

By week three of the questionnaire, Dana's team and Yasmin had fixed the decision rights (lesson 11.1) and started threat modelling (lesson 11.2). But for almost every answer, the partner wanted evidence: "Provide the access review for the last two quarters." "Provide three examples of approved production changes." Before going live it also wanted an independent audit report or a visit from its assessors.

Bilal, now CFO, had seen audits stop delivery for weeks while people wrote documents after the fact. Faisal proposed exactly that: freeze payments work for a month and "get compliant".

Maha said no, and asked what if the evidence already existed in the tools teams use every day. Yasmin spent two days with Dana checking. Every merged pull request already carried its review. The pipeline logged every deploy. The access tool from lesson 11.1 logged every grant. The gaps were real but few.

## 📐 How it works

### 🟢 The essentials

**Where obligations come from.** An **obligation** is something the company must do or must be able to show.

| Source | Examples of the *kind* of rule | Who helps you read it |
|---|---|---|
| **Law and regulation** | Data protection, consumer protection, payments, employment, tax and record-keeping rules in each country | Legal adviser in each country |
| **Contracts** | The payments partner agreement; enterprise merchant contracts; cloud and supplier terms | Legal and the contract owner |
| **Industry standards** | Card industry security rules a partner may pass down; information security standards customers ask about | Security lead; the partner |
| **Own policies** | Qafila's change, access and data policies (lesson 11.1) | Policy owners |

This course does not tell you what any law requires; that varies by country and changes over time. Your job is to know the *kinds* of rule that touch your work and ask early: "Does this new field count as personal data where we operate?", "Does the partner contract say how fast we must report an incident?", "How long must we keep these records?"

**Three standards you will hear about.** Know what each is for; do not claim to meet any without checking.

- **ISO/IEC 27001** (current edition 2022): an international standard from ISO and IEC for an **information security management system**, a managed set of policies, risk processes and controls. Companies can choose to be certified by an accredited body.
- **SOC 2**: a report, under criteria set by the American Institute of Certified Public Accountants (AICPA), in which an independent auditor examines a service organisation's controls for security, availability, processing integrity, confidentiality and privacy. A **Type 1** report looks at design at one point in time; a **Type 2** report also tests operation over a period.
- **PCI DSS** (Payment Card Industry Data Security Standard), from the PCI Security Standards Council: security requirements for organisations that store, process or transmit payment card data. Version 4.0.1, a limited revision, was published in 2024. Which parts apply to Qafila depends on how card data flows, a question for Dana, the partner and a **qualified assessor** (a firm approved by the council to assess against the standard).

(All three as reported from the owners' and other public descriptions.)

**Scope is your biggest lever.** **Scope** is the set of systems, data and people a set of rules applies to. The smaller the scope, the less there is to control and prove. Qafila's choice in lesson 11.2 (the partner handles card numbers; Qafila stores only a reference) is a scope decision as much as a security one. Ask early: "Can we keep this data out of our systems altogether?"

**Controls and evidence.**

| Obligation (paraphrased) | Control | Owner | Evidence already produced by the work |
|---|---|---|---|
| Production changes are reviewed by someone other than the author | Branch protection requiring code-owner approval | Platform team | Merged pull requests with approvals; branch protection history |
| Access to payment data is limited and reviewed | Time-limited access tool; quarterly review by system owners | Dana's team | Access tool logs; signed-off review tickets |
| Incidents are handled and learned from | Incident process and post-incident reviews (lesson 4.3) | Salma | Incident tickets; reviews; action items with status |
| Known vulnerabilities are fixed in time | Dependency scanning; fix targets by severity (lesson 11.2) | Each team | Scanner reports; tickets with dates |
| Suppliers with data access are assessed | Supplier checklist (lesson 10.3) | Bilal's procurement lead | Completed checklists; contract register |

**Design versus operation.** An auditor asks two questions. Is the control **designed** to reduce the risk? And is it **operating**: did it actually work, every time, over the period? A policy with no records proves design at best. A pipeline that logs every approval proves operation.

### 🟡 Going deeper

**Continuous compliance.** Instead of an "audit season" of hand-gathered evidence once a year, **continuous compliance** means controls run automatically and evidence is collected as the work happens, so "show me" is a query, not a project.

- **Prefer system records to documents.** A pull request with its approval beats a spreadsheet saying "all changes approved".
- **Keep evidence where it is created,** and know how to export it.
- **Sample, do not dump.** Auditors usually test a sample of items from the period (for example, a few dozen changes; the size is the auditor's choice). Be ready to pull any sample quickly.
- **Watch the controls themselves.** An alert when branch protection is switched off is evidence that it stayed on.
- **Name an owner per control,** not per document.

For how a manager judges pipeline evidence, see [*Running IT as a Business*, lesson 5.2 — Quality gates and evidence a manager can trust](../itbiz/index.html#/5.2).

**Answering a due-diligence questionnaire.** The same questions recur across partners, so keep an **answer bank**: each question, the honest answer, its control, the evidence, the owner and the date last checked. For each question:

1. **Find out what is actually true** today, from records, not memory.
2. **Answer exactly what was asked,** in plain language.
3. **If there is a gap, say so,** with the plan, owner, date and any interim control.
4. **Point to evidence** available on request, without sending sensitive material by default.
5. **Have the answer reviewed** by the control owner and, for contractual or legal statements, the right adviser.

Answers often become part of the contract. An overstated "yes" can become a broken promise.

**Who checks whom.** The Institute of Internal Auditors' **Three Lines Model** (updated in 2020) is a widely used way to describe roles (as reported). **First-line** roles deliver products and own their risks (Qafila's product teams). **Second-line** roles give expertise and challenge on risk (Dana's team). **Third-line** roles give independent assurance (internal audit). As a practitioner, you are first line: your team's risks are yours to manage.

### 🔴 Expert view

**Findings are information, not verdicts.** An audit **finding** is a gap between what a control should do and what the evidence shows. Treat findings like post-incident actions (lesson 4.3): find the cause, fix the system, give each an owner and date, and check the fix worked.

**Map once, answer many.** Keep one **control set** in your own words and map each external requirement to it, without copying any standard's wording or structure. For the bank-scale operating model, see [*Running IT as a Business*, lesson 10.3 — Risk, controls and audit in a regulated bank](../itbiz/index.html#/10.3).

**Protect the evidence itself.** Logs prove something only if the people being audited cannot quietly change them. Keep audit logs out of their reach, for as long as obligations and advisers say, with no more personal data than needed. See [*Data Engineering & Analytics*, lesson 6.3 — Securing the data platform: access control, secrets, audit and sharing safely](../data/index.html#/6.3).

**The memorable rule.** Build evidence into the work, not on top of it.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Obligations register** | Laws, contracts, standards and policies that apply, each with an owner and questions for an adviser | When entering a country, signing a partner, or handling new data |
| **Control-to-evidence map** | Each obligation linked to a control, its owner and the system record that proves it | Before any audit or questionnaire, and kept current after |
| **Answer bank** | Reusable questionnaire answers with control, evidence, owner and date last checked | Whenever a due-diligence questionnaire arrives |
| **Gap and remediation log** | Each gap or finding with cause, fix, owner, date and verification | After an audit, assessment or self-check |
| **Tamper-resistant audit log** | Logs stored where the people they record cannot change them | For access, change and admin actions on important systems |

## 🏛️ In practice at Qafila
Part of the control-to-evidence map and two questionnaire answers Yasmin and Dana prepared. Illustrative and fictional.

> **Payments integration: control-to-evidence map (extract)**
>
> | Ref | Control | Owner | Evidence (system and report) | Status |
> |---|---|---|---|---|
> | C-01 | Code-owner review before merge; no self-approval | Platform lead | Version control host: merged pull requests; branch protection audit log | Operating |
> | C-04 | Time-limited production access, logged | Dana | Access tool: grants report | Operating since 2 months ago; shared emergency account retired [date] |
> | C-05 | Quarterly access review by system owners | Dana | Review tickets with sign-off | **Gap:** only one review done so far |
> | C-09 | Incidents reviewed within 10 working days | Salma | Incident tool: reviews with dates and actions | Operating with exceptions (2 of 14 late; cause and fix logged) |
> | C-12 | Payment notifications verified (lesson 11.2, T1) | Payments lead | Automated tests in pipeline | Operating |
>
> **Question 31: "Provide access reviews for production payment systems for the last two quarters."**
> "Quarterly access reviews by system owners began this quarter. The first is complete (evidence on request); it removed 23 accounts that no longer needed access. Before this quarter, access was not reviewed formally. For the last two months, access granted through the access tool has been time-limited and logged; the shared emergency admin account was retired on [date] and replaced by a break-glass role whose every use is logged and reviewed. The next review is due [date]; owner: security and risk lead."
>
> **Question 47: "Do you store, process or transmit cardholder data?"**
> Drafted with the partner's guidance: "Card details are entered into the partner's payment components and are not stored or processed by Qafila systems; Qafila stores a partner reference, amount and status. Scope confirmation: [to be agreed with the partner and its assessor]."

Faisal wanted question 31 answered "Yes, reviewed quarterly". Dana refused: there was one quarter of evidence, not two. Bilal agreed: "A gap with a plan is a conversation; a false yes is a contract problem." The partner accepted the gap with a follow-up date, and no freeze happened.

## 🛠️ Exercises
**🟢 Find evidence that already exists.** For a project on a public version control host, list five things an auditor might ask ("show that changes are reviewed", "show who can merge", "show that tests run before release", "show how a security issue would be reported", "show the history of a dependency update") and where the evidence already lives.
*Done when:* each has a specific system and record, and any with no evidence is marked as a gap.

<details><summary>Model answer and self-check</summary>

**Model answer.** Reviewed changes: pull request pages show approvals; branch protection settings show the rule (gap if off). Who can merge: the collaborators settings page. Tests before release: CI run history linked from pull requests and release tags. Security reporting: a security policy file (gap if missing). Dependency updates: pull requests from a dependency update tool, with dates.

**Self-check.**
- Did you name records the system produces, not documents you would write now?
- Did you mark gaps rather than skip them?

</details>

**🟡 Build a control-to-evidence map.** Use the merchant staff invitation feature from lesson 11.2's exercise, or your own project. Write four obligations in plain words, each with a control, an owner, the evidence and a status.
*Done when:* every row's evidence is a system record, each control has one owner, and at least one row is honestly a gap with a date.

<details><summary>Model answer and self-check</summary>

**Model answer.** (1) Only the merchant owner can grant full access: server-side role check with tests; owner Merchant Accounts lead; evidence: role tests in CI history; operating. (2) Invites cannot be reused: single-use, 24-hour links; same owner; evidence: automated test and log of expired-link attempts; operating. (3) Role changes are recorded: audit log of grants; same owner; evidence: log export; operating. (4) Inactive staff accounts are removed: monthly job disabling accounts unused for 90 days; same owner; evidence: job run log; **gap**, job planned for next month.

**Self-check.**
- Is each obligation an outcome, not a tool?
- Would the evidence exist if nobody remembered to create it?
- Does your gap have a date and an owner?

</details>

**🔴 Answer three questionnaire questions honestly.** Using only this module's Qafila material, answer: (a) "How are security risks identified and tracked in new development?"; (b) "Describe your process for reviewing and removing user access"; (c) "How quickly do you remediate critical vulnerabilities, and how do you measure it?"
*Done when:* each answer states only what the lessons show to be true, points to evidence available on request, at least one answer states a gap with an owner, a date and an interim measure, and nothing promises what the company cannot yet keep.

<details><summary>Model answer and self-check</summary>

**Model answer.** (a) "Teams run a short four-question threat model on changes that touch money, personal data, logins or access, led by the team's security champion where one is named. Risks found are rated and recorded in a shared risk register with one owner and dates; for example, the threat model for this integration added entry R-131, owned by the Payments lead. Evidence on request: threat models and register extracts. Gap: we have not yet confirmed that every team has a champion; owner: security and risk lead; date: [date]; meanwhile the security and risk team reviews threat models for payment changes."
(b) "Production access to payment systems is requested through an access tool, granted for at most 8 hours and logged; this has been in place for two months. The shared emergency admin account was retired on [date] and replaced by a logged break-glass role. System owners review access quarterly; the first review is complete and removed 23 accounts. Before this quarter, access was not reviewed formally. Next review: [date]; owner: security and risk lead."
(c) "Our internal targets are critical within 7 days, high within 30 and medium within 90 (30 for systems handling money or payment data). Dependency scanning runs on every change, and findings become tickets with severity and dates; exceptions are recorded with an owner and an end date. Gap: we have not yet reported the share of critical findings fixed within target; owner: security and risk lead; first figure by [date]."

**Self-check.**
- Did you avoid "always", "all" and "never" unless the evidence supports them?
- Did you name an owner for each control and each gap?
- Would you be comfortable if the partner asked for a sample tomorrow?

</details>

## ⚠️ Mistakes and traps
- **Treating compliance as security.** Passing a check does not make you safe. Start from real risks, then show evidence.
- **Audit season.** Freezing delivery to write documents is costly and repeats. Collect evidence continuously.
- **Overstating answers.** A hopeful "yes" can become a contractual promise. State gaps with plans.
- **Reading the law yourself and concluding.** Write the question down and take it to the right adviser.

## 🧾 Recap
- Obligations come from law, contracts, industry standards and own policies; know the kinds and ask advisers.
- Map each obligation to a control with an owner, and to evidence the normal work already produces.
- Auditors check design and operation; system records prove operation better than documents.
- Keep scope small, keep an answer bank, and answer honestly with gaps, plans and dates.
- Rule: build evidence into the work, not on top of it.

## ✍️ Check yourself
**1. Faisal proposes freezing payments work for a month to "get compliant" before the partner's assessment. Which response best fits this lesson?**

- A. Agree, because a single focused month will produce cleaner documents than gradual work.
- B. Agree, but limit the freeze to two weeks and ask each team to write one policy document.
- C. Disagree, and leave the assessment until after launch when the teams have more time.
- D. Disagree, and first check which system records already provide the evidence asked for.

<details><summary>Answer</summary>

**D.** Most evidence already exists in the tools teams use; find it, then close the real gaps. A and B repeat the audit-season pattern, and C ignores a condition the partner set before going live. See "Continuous compliance".

</details>

**2. Only one of two requested quarterly access reviews exists. How should Qafila answer the partner?**

- A. Answer "yes, reviewed quarterly", since the process now exists and will continue each quarter.
- B. Leave the question blank, and raise it only if the partner chases for an answer later.
- C. State that one review is done, the gap before it, the interim control and the next date.
- D. Send the full access tool logs for both quarters, so the partner can judge for itself.

<details><summary>Answer</summary>

**C.** An honest gap with a plan and an interim control builds trust. A overstates, B avoids the question, and D dumps sensitive raw data instead of answering. See "Answering a due-diligence questionnaire".

</details>

**3. An auditor asks whether Qafila's review control is "operating". What is the best evidence?**

- A. The written change policy, signed by the Head of Engineering and dated this year.
- B. A sample of merged pull requests from the period, each showing a second approver.
- C. A statement from each team lead confirming that their team follows the policy.
- D. A slide deck describing the review process, prepared specially for the auditor.

<details><summary>Answer</summary>

**B.** System records from the period show the control actually worked. A and D show design at best, and C is an assertion, not evidence. See "Design versus operation".

</details>

**4. Qafila's design keeps full card numbers inside the partner's payment components. Why does this matter for compliance?**

- A. It can shrink which systems the card rules cover, once the partner and an assessor confirm the data flow.
- B. It can remove the need for a written agreement with the partner on card data, once the integration is live.
- C. It matters mainly for cost, because the scope of card rules is usually set by transaction volume.
- D. It matters mainly for security, because compliance scope is usually set by the countries served.

<details><summary>Answer</summary>

**A.** Keeping sensitive data out of your systems reduces what is in scope, confirmed with the partner and an assessor. B ignores that the partner relationship is governed by contract, and C and D misread what sets scope: which systems and data the rules apply to. See "Scope is your biggest lever".

</details>

**5. In the Three Lines Model as this lesson describes it, where does Yasmin's team sit?**

- A. Second line, because the team has a security champion who runs its threat models.
- B. Third line, because the team checks its own controls before the partner assesses them.
- C. First line, because it delivers the product and owns the risks in its own work.
- D. Outside the model, because only risk, compliance and audit functions belong to it.

<details><summary>Answer</summary>

**C.** Teams that deliver products own their risks; the second line supports and challenges, and the third gives independent assurance. A confuses a team role with a function, B confuses self-checking with independent audit, and D leaves out the people who own the risks. See "Who checks whom".

</details>

## 📚 References
- ISO/IEC 27001:2022, *Information security, cybersecurity and privacy protection — Information security management systems — Requirements* (ISO and IEC, 2022). Cited by title, owner and date; ISO's site: https://www.iso.org/ — edition and purpose reported from search summaries; the catalogue page could not be opened from this environment on 2026-11-22.
- AICPA (American Institute of Certified Public Accountants), SOC 2 reports and the trust services criteria. Cited by owner; AICPA & CIMA site: https://www.aicpa-cima.com/ — description of criteria and Type 1/Type 2 reports reported from search summaries; not opened.
- PCI Security Standards Council, *PCI DSS v4.0.1* (2024), a limited revision of v4.0. Cited by title, owner and date; council site: https://www.pcisecuritystandards.org/ — reported from search summaries; not opened.
- The Institute of Internal Auditors, *The IIA's Three Lines Model: An Update of the Three Lines of Defense* (July 2020). Cited by title, owner and date; IIA site: https://www.theiia.org/ — reported from search summaries; not opened.
- Library course: [*Running IT as a Business*, lesson 5.2 — Quality gates and evidence a manager can trust](../itbiz/index.html#/5.2).
- Library course: [*Running IT as a Business*, lesson 10.3 — Risk, controls and audit in a regulated bank](../itbiz/index.html#/10.3).
- Library course: [*Data Engineering & Analytics*, lesson 6.3 — Securing the data platform: access control, secrets, audit and sharing safely](../data/index.html#/6.3).
