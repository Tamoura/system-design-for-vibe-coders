# Claims register

Every legal or numeric claim in a lesson is listed here, so someone can check it and so it can be re-checked on a date.
A claim is a statement that could be wrong in a way that matters: a law, a fine, a deadline, a price, a limit, a statistic, a version number.

A row is added only when a person has looked at the source, or, if only a search summary was read, when its method says so.

## Where rows go

Put rows in a Markdown file in this folder, one file per course: `academy/claims/<course>.md`. Use this table header exactly:

```
| id | course/lesson | claim | source URL | date checked | method | review-by date | status |
|---|---|---|---|---|---|---|---|
```

## Columns

| Column | What to write |
|---|---|
| id | A short unique id, for example `cloud-03-001` (course, lesson number, running number). |
| course/lesson | The course folder and lesson file, for example `cloud/modules/03-networking.md`. |
| claim | The claim in one plain sentence, as the lesson states it. |
| source URL | A link to the primary text (the law, the standard, the vendor documentation page) where one exists. |
| date checked | The day someone last read the source, as `YYYY-MM-DD`. |
| method | `primary text` if the person read the source itself, or `search summary` if the fact is only reported by a web search summary. A search summary is "reported", never "verified". |
| review-by date | The day the claim must be checked again, as `YYYY-MM-DD`. Laws and prices: at most 12 months after the date checked. |
| status | `open` (not yet checked), `checked` (read against the source), or `changed` (the source changed, the lesson needs an edit). |

## How to add one

1. Find the claim in the lesson.
2. Open the source and read the passage. Do not rely on memory.
3. Add one row to the course file with all eight columns filled in.
4. Put the same source link in the lesson, next to the claim.
5. Mention the new row in your pull request.

## The weekly check

`.github/workflows/maintenance.yml` reads every table row in this folder (this README is skipped). If a row has a review-by date in the past, the staleness job fails. Fix it by re-checking the source, then updating the date checked and the review-by date. If there are no rows, the job passes.
