# Runbook index: Najm Desk
<!-- Every runbook that exists, who owns it and when it was last drilled. A runbook that is not in this table does not exist, and a row without a file is a lie. -->
Version: TODO   Owner: Maha (SRE lead)   Reviewed: TODO date

## Incident runbooks
| Runbook | Use it when | First move | Owner | Last drilled |
|---|---|---|---|---|
| [Kill switch](../runbooks/kill_switch.md) | Najm Desk is harming people or money now | Press `model_calls off` (or `write_tools off`) | Maha | TODO |
| [Wrong-answer storm](../runbooks/wrong_answer_storm.md) | Reports of wrong answers rise, or canary questions fail | Save three run ids; stop it if harmful | Yara and Lujain | TODO |
| [Tool outage](../runbooks/tool_outage.md) | TicketHub, Najm ID, PeopleCore or DeviceDesk fails | `write_tools off`; ask the owning team | Maha | TODO |
| [Cost spike](../runbooks/cost_spike.md) | The breaker trips or spend climbs | Check whether the breaker already acted | Maha and Lujain | TODO |
| [Injection incident](../runbooks/injection_incident.md) | Odd behaviour after reading a ticket or page | `write_tools off`; keep the evidence; call Noura | Noura | TODO |
| [Regression after a change](../runbooks/regression_after_change.md) | The canary or a release is worse than the baseline | Roll back to the previous release | Lujain and Yara | TODO |

## Routine runbooks
| Runbook | Cadence | Owner | Last run |
|---|---|---|---|
| [Change a prompt, a model id or a rule](../runbooks/change_prompt_or_model.md) | Every change | Lujain | TODO |
| [Monthly eval refresh](../runbooks/monthly_eval_refresh.md) | First working week of the month | Yara and Lujain | TODO |

## Who to call
| Role | Name | How |
|---|---|---|
| First responder (L2) | TODO | TODO |
| Builder on call (L3) | TODO | TODO |
| Security (Noura) and privacy (Sara) | Noura, Sara | TODO |
| Sponsor | Hind | TODO |
