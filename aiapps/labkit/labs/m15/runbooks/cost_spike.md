# Runbook: cost spike, Najm Desk
<!-- Cost is a symptom: a loop, a bloated prompt, a broken cache, or abuse. Find which. -->
Owner: Maha (SRE lead) with Lujain   Last drilled: TODO date   Version: 1

## Trigger
The cost breaker tripped, or tokens per hour or per resolved conversation passed the alert line; the provider's usage page shows a jump; a budget alert fired.

## First five minutes
1. Did the breaker already switch `model_calls` off? Check `SWITCH_FILE.log`. If not, and spend is still climbing, press the kill switch (`kill_switch.md`).
2. Write down tokens so far and the time.

## Diagnose
1. `python labs/m15/trace_report.py TRACE`: the `token_budget` and `iteration_cap` counts and tokens per run p95. Then sort the raw trace by tokens to find the dearest runs.
2. One run or one user? A loop shows many model calls in one run. Abuse shows many runs from one `user` hash.
3. Did a release or prompt change land just before? `--by release`. A prompt change also invalidates the prompt cache for a while.

## Fix or mitigate
Loop: fix the guard (`no_progress`, step cap) and roll back the change that removed it. Abuse: rate-limit that user at the gateway. Bloat: roll back the prompt. Do not raise the breaker limit to make the alert stop.

## Tell people
Hind hears if the bill or the budget is affected. Finance is told by Hind, not by the builders.

## Recover and resume
Breaker limit reviewed against a normal peak hour in the trace report; switch on; watch spend for an hour.

## After
Add the loop or bloat case to the eval set. Review the budget alert and the breaker limit.
