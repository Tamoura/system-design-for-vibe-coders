# Runbook: tool outage, Najm Desk
<!-- TicketHub, Najm ID, PeopleCore or DeviceDesk is down or slow. The agent must say so, never pretend. -->
Owner: Maha (SRE lead)   Last drilled: TODO date   Version: 1

## Trigger
`tool` events with `is_error` rise in the traces, and `no_progress` or `iteration_cap` climb in the report; the agent says "I could not reach" more than usual; the owning team announces an outage.

## First five minutes
1. Writes failing or doubled? Press `write_tools off` (`kill_switch.md`) so nothing is half-done.
2. Ask the owning team (TicketHub: TODO owning team; Najm ID: Hamad's team) for status and an estimate.

## Diagnose
Is it one tool or all of them? Our network or theirs? Errors since when (the first failing trace)? Is the agent retrying in a loop (`outcomes` shows `no_progress` or `iteration_cap`)?

## Fix or mitigate
Read-only mode keeps policy answers and status lookups working. For a long outage, `model_calls off` shows the portal's phone and ticket routes (NFR-02). Never retry a write without an idempotency key.

## Tell people
Yara tells the desk what Najm Desk can and cannot do meanwhile. Staff see an honest message, not "Done".

## Recover and resume
Tool healthy for 15 minutes in staging; replay one status lookup and one draft; turn `write_tools` on last. Check that tickets from the outage are not duplicated.

## After
Was the degraded mode clear to staff? Add an eval case for the failure message.
