# Agent log

Entry: REMIT-318, branch remit-318-limit-warning (the reference solution's log, constructed for the kit's tests, not a recorded session)
Prompt (paste or summarise): spec first (specs/REMIT-318.md), plan mode, then one step per commit; no existing test edited; the approved wording copied from the ticket
What the agent did: read limits.py, notify.py and service.py; proposed a five-step plan; wrote the template, the decision in send, then the tests
What I corrected: it first compared the ratio with 0.8 (a float: exactly 80% did not warn); it passed the percentage as an int (Western digits in Arabic); it called the notifier directly instead of the best-effort helper
What I checked myself: pytest -q after every step; the new tests against the starting code (they fail); a real send of 1,700.00 as T1 in English and Arabic; git diff lab-start --stat
Minutes: spec and plan 20 - agent 25 - verify 20 - integrate 10
Would I delegate it again? Yes, with the same spec; the three corrections are now lines in the spec
