# System card: Najm Desk
<!-- One page a risk owner can read in ten minutes. Every statement must be true of the system as deployed; pack_check.py compares the tool list with guardrails.py. -->
Version: TODO   Date: TODO   Owner: TODO

## Purpose and scope
What the agent is for, who uses it, what it must never be used for, and the autonomy level of each action (suggest, draft, approve first, act).
TODO

## Tools and permissions
One row per tool the model can call, in backticks. Read or write, the scope the USER must hold, who approves, rate limit.

| Tool | Read or write | Scope the user must hold | Approval | Rate limit |
|---|---|---|---|---|
| `TODO` | TODO | TODO | TODO | TODO |

## Data and models
Data classes the agent touches (Public, Internal, Confidential, Restricted), the model ids and provider, the endpoint and inference geography, prompt and rules versions, what is logged and for how long.
TODO

## Evaluation results
Eval set (name, size, date), the numbers against the targets in the specification, the latest red-team run (attack set, date, how many attacks still work), and the failures you know about.
TODO

## Known limits
Languages, topics and situations where it does badly; what a person should check; when to switch it off.
TODO

## Sign-off
| Name | Role | Decision | Date |
|---|---|---|---|
| Layla | Head of AI Governance | TODO | TODO |
| Noura | Application and AI Security | TODO | TODO |
