# Runbook: injection incident, Najm Desk
<!-- Text that someone else wrote made the agent act, or may have. This is a security incident first and a bug second. -->
Owner: Noura (Application and AI Security)   Last drilled: TODO date   Version: 1

## Trigger
A guard-fire spike in the trace report (taint or approval refusals); an unexpected tool call; a user or the desk reports odd behaviour after reading a ticket or policy page; Noura's red-team run finds a gap.

## First five minutes
1. Press `write_tools off` at once (`kill_switch.md`); `model_calls off` too if data may be leaving.
2. Preserve the evidence: do not delete traces, tickets or pages. Copy the run ids and the suspect text.
3. Call Noura. If personal data may have left the bank, call Sara as well.

## Diagnose
Where did the text come from (policy page, ticket comment, pasted by a user)? Which tool calls followed it? Were they refused by the gate, or did they happen? Do not re-run the attack against production.

## Fix or mitigate
Quarantine the source page or comment (its owner removes it). Rotate any secret the agent could reach. Close the gap in the gate (not the prompt), then add the attack to the red-team set.

## Tell people
Noura leads communication and follows the bank's security incident process. Hind and Layla hear the same day.

## Recover and resume
Noura approves resuming in writing. The red-team run and the eval gate must be green, with the new attack in the set.

## After
Blameless postmortem within 5 working days; update the threat sheet and the risk register.
