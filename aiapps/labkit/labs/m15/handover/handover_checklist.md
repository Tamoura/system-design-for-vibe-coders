# Handover checklist: Najm Desk v1
<!-- Fictional engagement. Each line says what, who owns it and the evidence that proves it. Nobody ticks a box without the evidence. Every box starts empty. -->
Handover date: TODO   Hypercare ends: TODO   Customer owner: Hind   Delivery owner: Fahad

## Support model
| Level | Who | Handles | Acknowledges within (Hind agrees the numbers) |
|---|---|---|---|
| L1 | Service Desk champions and agents (Yara's team) | How-to questions, wrong-answer reports, hand-offs, first look at a complaint | TODO |
| L2 | Platform operations (Maha's SRE rota, Salem's platform team) | Alerts, the kill switch, tool outages, cost spikes, deploying approved changes | TODO |
| L3 | Developer Enablement (the builders) | Defects in prompts, tools, retrieval and evals; model changes | TODO |
| Risk | Noura, Sara, Layla, Hamad | Injection incidents, privacy questions, governance changes | TODO |

Prompt and model changes: Yara decides what Najm Desk should say or do, Developer Enablement makes and tests the change, Noura approves anything security-relevant, and Layla is told of material changes (the change policy in the governance pack).

## Acceptance
- [ ] UAT script run by the customer, results recorded. Owner: Yara. Evidence: signed `uat_script.md` and `uat_evidence.json`
- [ ] Every failed row has a severity and a fix, a re-test or a written waiver. Owner: Hind. Evidence: defect list
- [ ] Sign-off table complete. Owner: Hind. Evidence: the Sign-off section of `uat_script.md`

## Documents handed over
- [ ] User guide. Owner: Yara. Evidence: `user_guide.md`, reviewed
- [ ] Admin guide (configuration, flags, how to add or retire a policy document, access). Owner: Salem. Evidence: `admin_guide.md`
- [ ] Architecture and decision records. Owner: Fahad. Evidence: diagrams and ADRs match the running system
- [ ] Runbooks and the index. Owner: Maha. Evidence: `runbook_index.md`, every row has a file
- [ ] Governance pack and risk register. Owner: Layla. Evidence: `pack_check.py` output and signatures
- [ ] Eval report (latest run, set composition, known weaknesses). Owner: Lujain. Evidence: the results file and its date

## Access and ownership
- [ ] Repository, CI, eval sets, prompts and the switch file are in the customer's custody. Owner: Salem. Evidence: access list
- [ ] Secrets rotated since the builders last held them. Owner: Salem. Evidence: rotation record
- [ ] Provider account, billing alerts and the deprecation-notice mailbox have named owners. Owner: Hind. Evidence: names in the support model

## Training
- [ ] Service Desk staff trained, with a short check at the end. Owner: Yara. Evidence: attendance and results
- [ ] Operators have run the kill-switch drill themselves. Owner: Maha. Evidence: the drill output with their names
- [ ] Champions named for every shift. Owner: Yara. Evidence: the list in the user guide

## Operations
- [ ] Dashboard and alerts route to named people, and each alert has a runbook. Owner: Maha. Evidence: alert list
- [ ] Monthly eval refresh and quarterly review are in calendars. Owner: Yara. Evidence: invitations

## Adoption and benefits
- [ ] Baseline and definitions agreed with Hind before go-live. Owner: Lujain. Evidence: the baseline table
- [ ] First monthly benefits report date set. Owner: Hind. Evidence: calendar entry
- [ ] Feedback channel is live and someone reads it weekly. Owner: Yara. Evidence: first triage notes

## Hypercare and close
- [ ] Hypercare plan: length, daily check-in, exit criteria. Owner: Fahad. Evidence: the plan
- [ ] Lessons-learned review booked within two weeks of the end. Owner: Fahad. Evidence: invitation
- [ ] Closure report sent. Owner: Fahad. Evidence: the report
