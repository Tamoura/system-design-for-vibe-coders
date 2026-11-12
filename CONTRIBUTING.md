# Contributing

Thank you for helping. The courses are drafted with AI and have not been reviewed by a subject expert. Corrections are welcome.

## Report a problem

Use the issue form: `.github/ISSUE_TEMPLATE/report-a-problem.yml` (New issue, then "Report a problem"). Name the course and lesson, say what is wrong, and give a source if you have one. Do not include personal data or passwords.

## Propose a change

1. Fork the repository and make a branch.
2. Edit the Markdown source in `<course>/modules/`. Do not edit generated files (`COURSE.md`, `course.html`, `index.html`, `assessment.html`); they are rebuilt from the sources.
3. Change the English and the Arabic file together. Every English change needs the matching Arabic change.
4. Run the checks below.
5. Open a pull request. The template lists what to confirm.

Once a second maintainer exists, every pull request needs a review from someone other than its author before it is merged.

## Arabic rules

1. Put the English expression in parentheses beside every Arabic term.
2. Arabic diagrams run right to left.
3. Write "DPO" with the Arabic word for protection (حماية).

Each course has a checker: `python3 <course>/check_ar.py EN.md AR.md`.

## Run the checks

```
npm run qa          # Arabic pairs, answer cues, Arabic rules, claims lint
npm run test:assess # self-assessment group view tests
npm run check       # vibe course output matches its markdown
npm run cloud:check # the same for another course; each course has its own :check script
```

See `scripts/qa/README.md` for what each check does.

## Status labels

A course may show "expert-reviewed" or "piloted" only if a sign-off record exists in `academy/reviews/`. Without a record, the label is "AI-drafted". Read `academy/STANDARD.md` for the full rule, and add legal or numeric claims to `academy/claims/`.
