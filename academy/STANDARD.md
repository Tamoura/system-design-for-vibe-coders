# Academy standard

This is the one standard every course in this library inherits. It says what a level means, what a unit is, who must sign off, and which labels a course may show.

Status today: every course is drafted with AI and has not been reviewed by an expert. No course has a sign-off record.

## 1. Levels

Each course declares one level. A level is described by what a learner can do, not by how long the course is.

| Level | Name | A learner at the end can |
|---|---|---|
| 100 | Foundation | Explain the main terms in their own words, recognise them in a real system, and follow a guided procedure to a correct result. |
| 200 | Practitioner | Do routine tasks alone, choose between common options and give a reason, and find and fix a typical fault. |
| 300 | Advanced | Design for a stated requirement, weigh trade-offs with evidence, review other people's work and find the faults in it. |
| 400 | Lead | Set direction for a team, decide under uncertainty, and write the standard others follow. |

## 2. Unit types

| Type | Purpose | Typical size (estimate) |
|---|---|---|
| Concept | Teaches an idea with examples. | 20 to 40 minutes |
| Lab | The learner does a task and checks the result. | 45 to 90 minutes |
| Project | The learner produces a larger piece of work against a rubric. | 3 to 10 hours |
| Review | The learner checks given work against a checklist and writes findings. | 30 to 60 minutes |

## 3. Every lesson states an outcome and a time

- Each lesson or unit begins with one measurable outcome: "After this you can ..." followed by something a person can show. "Understand caching" is not measurable. "Explain which of three data items may be cached and why" is.
- Each lesson states a study time. It is labelled "estimate" until a pilot cohort has measured it. After a pilot, record the measured median and the number of learners.

## 4. Sign-offs

Four people sign off. Each one writes a record using `academy/reviews/TEMPLATE.md`, stored at `academy/reviews/<course>/<role>-<date>.md`.

| Role | Signs off | Must record |
|---|---|---|
| Subject expert | Accuracy of the content. | Name, credential, date, commit hash. |
| Assessment lead | Outcomes, rubrics and exam forms. | Name, credential, date, commit hash. |
| Arabic editor | The Arabic edition, including the standing Arabic rules. | Name, credential, date, commit hash. |
| Pilot cohort | A group of learners completed the course and results were collected before release. | Name of the person who ran it, cohort size, dates, commit hash, what was measured. |

A sign-off covers the commit named in the record. Later changes need a new record.

## 5. Status labels

A course may carry these labels:

- **AI-drafted**: written with AI, no expert has signed.
- **expert-reviewed**: the subject expert and the Arabic editor records exist for the current content.
- **piloted**: a pilot record exists.

Rule: no label other than "AI-drafted" is shown until its record exists in `academy/reviews/`. Do not write that anything was reviewed, piloted or accredited unless a record says so.

## 6. Exam items

- Credential items come from a private bank that is not published. Public items are practice only and are labelled so.
- Run the answer-cue check on both sides: the correct option must not be identifiable by length, gloss or position, and a wrong option must not be eliminated by those cues either. `npm run qa:cues` does this for the published items.
- Gloss every option or none of them. Never gloss only the correct one.

## 7. Claims

Every legal or numeric claim has a row in `academy/claims/` with:

- a source link;
- the date it was checked;
- the method: primary text, or search summary;
- a review-by date.

A fact known only from a search summary is called "reported", never "verified". When the review-by date passes, the claim is checked again or removed.
