# Runbook: the kill switch, Najm Desk
<!-- A card, not an essay. Print it. Anyone on the IT on-call rota may press it. -->
Owner: Maha (SRE lead)   Last drilled: TODO date   Version: 1

## Trigger
Najm Desk is harming people or costing money right now: wrong or unsafe answers reaching staff, a loop or runaway cost, a possible leak, or a tool doing damage. When in doubt, stop it. A stopped assistant costs minutes; a running one may cost more.

## First five minutes
1. Stop every model call (staff see the degraded-mode message and the phone and ticket routes):
   `python labs/m15/kill_switch.py flip SWITCH_FILE model_calls off YOUR_NAME "what you saw"`
2. Only the writes misbehave (a ticket tool, an unlock request)? Make it read-only instead:
   `python labs/m15/kill_switch.py flip SWITCH_FILE write_tools off YOUR_NAME "what you saw"`
3. Check it worked: ask one question in staging. It must show the degraded message, and the traces must show no new `model` events.
4. Tell the Service Desk team lead (Yara) in one sentence, then open the runbook for the incident class.

## Diagnose
The switch file records who pressed it and why (`SWITCH_FILE.log`). Do not start diagnosis until step 3 is done.

## Fix or mitigate
Backstops, if the switch itself fails: stop the service in the deploy platform (Salem's team), then deactivate the model provider key (L3 only; check the provider's current console or Admin API documentation).

## Tell people
Yara tells the desk. Hind hears within the hour. If personal data may have left the bank, Sara and Noura hear immediately.

## Recover and resume
Only L2 or L3 turns it back on, after the incident runbook's recovery checks pass and the eval gate is green. Resume `write_tools` after `model_calls`, and watch the trace report for 30 minutes.

## After
Every use of the switch is reviewed, including the ones that turned out to be false alarms.
