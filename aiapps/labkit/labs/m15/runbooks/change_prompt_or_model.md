# Runbook: change a prompt, a model id or a rule, Najm Desk
<!-- A routine, not an incident. Every change walks the same steps. -->
Owner: Lujain (builder); approvals per the change policy   Last drilled: TODO date   Version: 1

## Trigger
Anyone wants to change the system prompt, a tool definition, the model id, a guardrail rule or the policy index. Also: a provider announces a model deprecation.

## First five minutes
1. Write the change down: what, why, who asked, which requirement it serves. One pull request, one change.
2. Name the previous version you will roll back to.

## Diagnose
Which eval cases and attack cases should move? Say before you run them.

## Fix or mitigate
Evaluate: run the eval gate and the red-team set on the new version; compare cost and latency, not only correctness.
Approve: security-relevant changes need Noura; anything that changes scope needs Hind and Layla (see the change policy).
Canary: send a small slice (desk agents in copilot mode first) to the new version for a set time.
Watch: `python labs/m15/trace_report.py TRACE --by release`; compare with the baseline against the thresholds you wrote in step 1.
Promote or roll back: roll back by pointing the config at the previous version; it needs no deploy.

## Tell people
Release note to the desk team lead for every behaviour change; Layla's register is updated for material changes.

## Recover and resume
Roll back means the previous version is live and the trace report shows the baseline numbers again.

## After
Record the decision, the numbers and the date in the change log.
