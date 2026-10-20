# Runbook: monthly eval refresh, Najm Desk
<!-- A routine. The eval set must keep pace with what users really ask. -->
Owner: Yara (domain) and Lujain (builder)   Last drilled: TODO date   Version: 1

## Trigger
First working week of each month, and after any incident.

## First five minutes
1. Export last month's feedback, hand-off packets and failed runs (stop reasons other than `done`), with personal data removed.
2. Book 60 minutes with Yara; bring the list.

## Diagnose
Sort the list: wrong answer, missing document, tool failure, guard fired, user expectation. Count each.

## Fix or mitigate
Turn the five most common into eval cases (input, expected behaviour, requirement id, source). Retire cases whose policy changed. Re-run the whole set and record the score.

## Tell people
Send the one-page result to Hind and Layla: the score, what was added, what is still weak.

## Recover and resume
The set is committed with the date; the next run uses it as the new baseline.

## After
Update the eval report in the handover pack.
