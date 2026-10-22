# Automation decision cards

## Card 1: run /review-change before every pull request

**Candidate:** the review command, started by the author before opening a pull request, on the diff of the branch.

1. **Repeats?** Every pull request, so five to ten times a week for each engineer; today everyone pastes their own prompt.
2. **Mechanical check?** None for the quality of the review. The mechanical parts are that the report has the agreed format and that the checklist ran.
3. **If it is wrong?** A missed finding gives false confidence, and a made-up finding wastes a reviewer's time. Nothing is changed, because it can only read.
4. **Where does it live?** A skill, because a person starts it, with a read-only subagent to do the reading in its own context.
5. **Who reads the output?** The author, before the pull request is opened; the human reviewer still reviews.
6. **Limits?** Read, Grep, Glob and three read-only git commands; fifteen turns for the subagent; no write tool.
7. **Safe to run twice?** Yes, it changes nothing.
8. **Owner and upkeep?** Salem keeps `.claude/` reviewed like code; the checklist changes when CONTRIBUTING.md does.

**Decision:** semi-automate
**Because:** the command saves the typing and the checklist, but a person decides what to do with the findings.

## Card 2: let an agent approve and merge pull requests when the reviewer finds nothing

**Candidate:** a CI job that merges a pull request when the reviewer subagent reports no findings.

1. **Repeats?** Every pull request, which is why it is tempting.
2. **Mechanical check?** None. "No findings" is the opinion of a model, and it reports nothing for many sound and many unsound changes.
3. **If it is wrong?** A float or a deleted test reaches main; in money logic that is a customer's money, with no second human having looked.
4. **Where does it live?** It would be a CI job, which is exactly why the permissions of that job matter most.
5. **Who reads the output?** Nobody, which is the point of the idea and the problem with it.
6. **Limits?** Merge rights are the opposite of a limit.
7. **Safe to run twice?** A merge cannot be undone cheaply.
8. **Owner and upkeep?** No one could own the risk, because the team rule says money changes need a second human reviewer.

**Decision:** keep manual
**Because:** our rules require a second human reviewer for money logic, and approval is a judgement the reviewer agent cannot be accountable for.

## Card 3: run the triage script on every new support ticket

**Candidate:** the triage script, run by a scheduled job on new tickets, writing a suggestion on the board for Hessa.

1. **Repeats?** About forty tickets a week, and Hessa sorts them by hand each time.
2. **Mechanical check?** The reply must validate against the allowed lists, and money areas always get a second reviewer by rule, not by the model's word.
3. **If it is wrong?** A ticket is mislabelled; a person corrects it. Ticket text is untrusted, so the run gets no tools.
4. **Where does it live?** A script around `claude -p`, started by a job, because nobody needs to be in the loop for a suggestion.
5. **Who reads the output?** Hessa, in the morning; the suggestion is not an assignment.
6. **Limits?** No tools, three turns, a budget cap per run, a timeout per ticket.
7. **Safe to run twice?** Yes: same input gives the same output, and the job writes one suggestion per ticket id.
8. **Owner and upkeep?** Payments Platform; tests use the stand-in, and a weekly sample is checked against the real program.

**Decision:** semi-automate
**Because:** the output is a suggestion with a mechanical check, and a person still decides what the ticket is.
