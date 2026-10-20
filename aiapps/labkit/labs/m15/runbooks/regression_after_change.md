# Runbook: regression after a model or prompt change, Najm Desk
<!-- The most common incident. A change that passed the gate still hurts a slice of real traffic. -->
Owner: Lujain (builder) with Yara   Last drilled: TODO date   Version: 1

## Trigger
The canary or a fresh release shows worse numbers than the baseline in `trace_report.py --by release`: success, p95, cost per resolved conversation, hand-off rate, thumbs-down.

## First five minutes
1. Canary only? Send all traffic back to the previous release now (`change_prompt_or_model.md`, step "Promote or roll back"). No approval needed.
2. Everyone affected and harm possible? Press the kill switch (`kill_switch.md`).

## Diagnose
What exactly differs between the two releases: prompt text, model id, tools, retrieval content, limits? Change one thing back at a time in staging. Compare the traces of the same question under both.

## Fix or mitigate
Keep the old release until the new one beats it on the eval set and on a canary. A model id change gets its own canary even if the prompt did not change.

## Tell people
Yara tells the desk if answers in the window were affected. Hind hears if rollback delayed a promised change.

## Recover and resume
The failing behaviour is now an eval case that fails on the bad release and passes on the fix. Then repeat the canary.

## After
Postmortem: why did the gate not catch it? Add the missing case or the missing check.
