# Sign-off records

A sign-off record is the evidence that a named person reviewed part of a course. See `academy/STANDARD.md` for the four roles.

## Where records go

`academy/reviews/<course>/<role>-<date>.md`

- `<course>` is the course folder name, for example `cloud`.
- `<role>` is one of `subject-expert`, `assessment-lead`, `arabic-editor`, `pilot`.
- `<date>` is the day of the sign-off, `YYYY-MM-DD`.

Start from `TEMPLATE.md` in this folder. One file per reviewer, per scope, per date.

## What an empty folder means

If there is no record for a course and role, nobody has signed. No course may show the label "expert-reviewed" or "piloted" without a record here. Today this folder holds only this README and the template, so nothing has been signed.

## Rules

- Records are written by the reviewer or with the reviewer's agreement. Never write a record for someone who has not agreed.
- Use the reviewer's name and credential or affiliation. Do not write personal email addresses.
- The commit is the hash of the version that was reviewed. If the lessons change later, the record covers the old commit only.
