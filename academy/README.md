# Academy catalogue

`catalogue.json` lists every course in the library once, with the school and level it is proposed to sit in. The landing page (`landing.html`) groups its cards the same way.

## Fields

| Field | Meaning |
|---|---|
| `id`, `title`, `titleAr` | Short id, English title, Arabic title with English beside it. |
| `school` | One of four schools, or `early-talent`. Proposed placement. |
| `level`, `levelProposed` | Level range such as `100-200`. Levels: 100 Foundation, 200 Practitioner, 300 Advanced, 400 Lead. The placement is a proposal from the course descriptions, not a decision. |
| `path` | Source folder. The System Design for Vibe Coders course lives in the root `modules/` folder and is published at `vibe/`. |
| `modules`, `lessons` | Counted from the sources (see below). |
| `languages` | `en` and `ar` for every course. |
| `status` | `ai-drafted` for every course: drafted with AI, not yet expert-reviewed. |
| `estimatedHours` | `null` for every course. |
| `flagship`, `flagshipProposed` | `true` for `aigp`, `secai` and `ainative`. This is the audit's recommendation, still proposed. |

## How the counts were made

Modules are the English `modules/NN-*.md` files of the course (the numbered orientation module counts). Lessons are the `# N.M — ` headings in those files. The vibe course counts (13 modules, 69 lessons) are the figures in its README and in the landing page; its modules sit in numbered folders under `modules/`.

## Rules

- **Hours stay `null` until a pilot.** No hour figure has been measured, so none is published. Do not estimate one.
- **`status` may only change when a record exists under `academy/reviews/`.** A record names the reviewer and the date. Until then every course stays `ai-drafted`. Nothing here claims a review, sign-off or pilot.
- The landing page does not show hours and does not mention certification.
- Early Talent (`career`) is outside the professional catalogue.
