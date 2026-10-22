# Payments Platform: AI engineering playbook

Owner: <<a named person>>. Status: draft. Next review: <<a date or an event>>.

Replace every `<<...>>` prompt with your own text. A rule is a bullet that starts with MUST or MUST NOT and ends with `Check:`.

## 1. Tools and environments
<<Which tools are approved and who keeps the list. Where agents may run and where they never run. How a new tool gets approved.>>

## 2. Data rules
<<The data classes. What never goes into a prompt. What test data is allowed. Which accounts may be used.>>

## 3. Context and memory
<<The memory file, who owns it, how big it may be, and what makes us add a line to it.>>

## 4. Spec and review norms
<<What a ticket needs before an agent starts. The label, the largest diff, who reviews money logic, how fast, what the author must explain.>>

## 5. Verification standard
<<What "done" means. The test command. The rule for money. What an agent may never do to a test.>>

## 6. Security baseline
<<Secrets, permissions, production, dependencies, untrusted content, MCP servers.>>

## 7. Automation
<<What we automate and how. What we never automate. The limits on unattended runs.>>

## 8. Metrics plan
<<At least three delivery metrics and one guard metric, one block each, in this shape.>>

### <<Metric name>>
- Kind: <<delivery or guard>>
- Definition: <<exactly what is counted or timed, from which event to which event, per what period>>
- Source: <<where the numbers come from>>
- Cadence: <<how often, and who reviews it>>
- Baseline: <<a figure from team-context.md, or "to be measured">>
- Threshold: <<the target (delivery) or the line that makes us act and what we then do (guard)>>

## 9. Incident handling
<<What happens in the first hour and the first week when an AI-assisted change or an agent's action is part of an incident.>>

## 10. Onboarding
<<The first two weeks. What juniors do differently. How skill is kept.>>
