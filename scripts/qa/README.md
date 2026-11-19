# Content checks (scripts/qa)

Checks that keep the course library honest. They need Python 3.9 or newer and nothing outside the standard
library. CI runs them with Python 3.11 in `.github/workflows/publish.yml`, and every one of them blocks the build.

| Check | Command | What it does | Fails when |
|---|---|---|---|
| Arabic lesson checkers | `npm run qa:ar` | Runs each course's `<course>/check_ar.py` on every lesson pair (`modules/NN-*.md` and its `.ar.md` twin) and prints one line per course. | A pair fails its course checker, or an English lesson has no Arabic twin. |
| Answer-cue audit | `npm run qa:cues` | Scores content-free strategies on every multiple-choice instrument (see below). | A score rises above the baseline, or a new instrument is too easy to guess. |
| Arabic rules | `npm run qa:arabic` | The owner's three standing rules for Arabic text (see below). | A violation that is not in the baseline. |
| Claims lint | `npm run qa:claims` | Looks for wording the library must not publish (see below). | Any hit. There is no baseline. |
| Site counts | `npm run qa:counts` | Compares the landing cards and about pages with `academy/catalogue.json`, and each course's assurance level with its sign-off records (see below). | Any count differs, or a level has no record. |
| Lesson outcomes | `npm run qa:outcomes` | Every lesson (EN and AR) opens with "After this you can ..." and a study-time estimate (`academy/STANDARD.md` section 3). | A lesson lacks either line. |
| Arabic content parity | `npm run qa:parity` | Each Arabic lesson and assessment string keeps the English's formula operators, option letters and citations (see below). | The Arabic has fewer than the English, beyond `scripts/qa/ar-parity-baseline.json`. |
| Internal links | `npm run qa:links` | Every internal link and `#anchor` on the assembled `_site/` resolves. Runs in the publish workflow after "Assemble the site". | Any broken internal link. |

`npm run qa` runs the first seven (the internal-link check needs the assembled site), keeps going after a failure and prints a summary. Each script also runs on its own:
`python3 scripts/qa/<name>.py`. Exit status 0 means pass, 1 means fail, 2 means the check could not run.

Two other tools live here:

- `run_all.py` is what `npm run qa` calls.
- `pytest_shard.py` splits a pytest suite into shards for a CI matrix. `.github/workflows/kits.yml` uses it for the
  `ainative/ailab` suite.

## Answer-cue audit (`quiz_cues.py`)

A good multiple-choice item cannot be answered by looking at the shape of the options. The audit reads:

- **quiz**: the "✍️ Check yourself" questions in `<course>/modules/*.md` and `*.ar.md`;
- **exam**: the "✍️ Practice exam" or "✍️ Mock exam" section in the same files;
- **self**: the self-assessment items in `<course>/assessment/data/*.json` (the vibe course: `assessment/data/`).

A question is a bold numbered line (`**3. ...**`), its options are `- A. ...` lines, and its key is the bold letter
that opens the `<details>` answer block (`**C.**`). Open-answer questions (the SaaS course's quizzes) are counted in
the `open` column and not scored. The parser finds 295 four-option items in the AIGP course in English (195 quiz,
100 exam), 225 in AI PM and 255 in Secure AI, which match the known counts.

For each course, instrument and language it scores these strategies, in percent:

| Column | Strategy | Score by chance |
|---|---|---|
| `longest` | Pick the option that is uniquely the longest (characters). | about 25% |
| `shortest` | Pick the option that is uniquely the shortest. | about 25% |
| `mid` | How often the key survives when you drop the unique longest and unique shortest options. | about 50% |
| `midguess` | Drop those two and guess between the rest: the expected score. With four options it cannot pass 50%. | about 25% |
| `latin` | Arabic only: pick the option with uniquely the most Latin letters (glosses can point at the key). | about 25% |
| `key` | Share of the most common key letter, with the letter. The self-assessment pages shuffle the options for each reader, so for `self` this only describes the source files. | 25% |

**Current scores are never written in this README.** They change whenever an item changes. Run `npm run qa:cues`
for the live table, or read `scripts/qa/cue-baseline.json`, which the tool writes. (For history only: when this
audit was first written in November 2026, the longest option was the key in most AIGP and AI PM exam questions;
those items have since been rewritten.)

**The ratchet.** `scripts/qa/cue-baseline.json` holds every row's scores. The check fails when

- a score in a row that is in the baseline rises by more than 2 percentage points, or
- a row that is not in the baseline (a new course, instrument or language) scores above 35% on `longest`,
  `shortest`, `midguess`, `latin` or `key`, or above 62.5% on `mid`.

Rows above those limits are marked `*` in the table. The ratchet does not make them pass or fail; it stops them
getting worse. A row near chance on every strategy is only free of these particular cues: it says nothing about
whether the questions measure the right thing, which needs a blind review by an assessment lead and a learner pilot. To see which items a strategy gets right:

```bash
python3 scripts/qa/quiz_cues.py --items aigp/exam/en --strategy longest
```

## Arabic rules (`arabic_rules.py`)

1. **Diagrams run right to left.** Every Mermaid `flowchart LR` or `graph LR` in an English source is `RL` in the Arabic
   twin, and every `direction LR` inside it is `direction RL`. Twins (`X.md`, `X.ar.md`) are compared block by block.
   TB, TD and other diagram types are not checked.
2. **"DPO" uses the word for protection.** Every `DPO` in Arabic text has «حماية» within 100 characters before it or
   60 after it on the same line. In today's sources the word is at most 63 characters before the token, for
   example «مسؤولة حماية البيانات (DPO)».
3. **English glosses on technical terms only, once per lesson.** The first use of a technical term in a lesson carries
   its English term in parentheses; plain phrases, repeated terms, product and acronym names do not. Every Arabic
   lesson file must lie between a floor (0.2 per 100 Arabic words, so glosses are not stripped away) and a ceiling
   (8 per 100, so they do not return to every phrase). Both are stored in `scripts/qa/arabic-baseline.json`.
   `--gloss-table` lists every lesson's density; `python3 scripts/qa/trim_glosses.py` applies the rule to files.

Sources: Arabic Markdown files that a builder did not generate, the Arabic fields of the self-assessment items, and
`about/index.ar.html`. Generated pages repeat the sources and are not scanned again. `agentic/` is a published copy
of another repository and is not checked. When the check was written there were no violations, so the list of known
exceptions in the baseline is empty.

## Arabic content parity (`ar_parity.py`)

A translation must carry some tokens over unchanged. The November 2026 content audit found that an automated
gloss-trimming pass had deleted formula parts ("TP ÷ (TP + FP)" became "TP ÷."), quiz option letters and research
citations from the Arabic editions, and no check noticed. This check compares every `X.md` with `X.ar.md`, and the
`en` and `ar` strings of every self-assessment item file, on three counts: option letters in parentheses, formula
operators (÷ × = ≈ ≤ ≥ and a spaced + or −), and citations ("et al.", «وزملاؤه», "Name, 2024"). Code is left out.
The Arabic count must not be lower than the English one. `--list` prints every shortfall.

`scripts/qa/trim_glosses.py` now pins these parentheticals as content, so it cannot delete them again.

## Claims lint (`claims_lint.py`)

Scans every tracked or new text file except `agentic/` (checked by `scripts/agentic-neutral.mjs --check`) and
`scripts/qa/` (these checks). It fails on:

- the name of the real organisation an earlier draft named (English, its short token, Arabic). The patterns live
  base64-encoded in `scripts/blocked-text.b64` (read through `scripts/blocked_text.py`), so no public file spells it out;
- exam-pass promises anywhere: "pass the AIGP", "ready for the AIGP exam", "sit the real exam", and their Arabic forms
  from the sources: «اجتياز امتحان شهادة (certification exam) AIGP», «اجتز امتحان AIGP», «جاهز لامتحان AIGP»,
  «تقدّم للامتحان الحقيقي»;
- in `aigp/` only: "pass the exam" and «اجتياز الامتحان»;
- a link from `landing.html` to the `agentic/` pages.

Lines are compared after HTML tags, Markdown emphasis and Arabic diacritics are removed, so `pass the **AIGP**` and
`pass the <strong>AIGP</strong>` are caught. A hit in a generated page (`COURSE.md`, `index.html`, `course.html`)
goes away when its source is fixed and the course is rebuilt.

## Site counts (`site_counts.py`)

`academy/catalogue.json` is the one source for how many courses, modules and lessons the library has. The check fails
when a hand-written page disagrees with it:

- a `landing.html` course card whose first two numbers (modules, lessons) differ from the catalogue, a card for a
  course the catalogue does not list, or a catalogue course with no card;
- `about/index.html` or `about/index.ar.html` not stating the catalogue's course count and total lesson count.

When a course gains or loses a lesson, change the catalogue first, then the pages, and run the check.

## Updating a baseline

```bash
python3 scripts/qa/quiz_cues.py --update-baseline      # rewrites scripts/qa/cue-baseline.json
python3 scripts/qa/arabic_rules.py --update-baseline   # rewrites the exception list, keeps the gloss floor
python3 scripts/qa/arabic_rules.py --update-baseline --reset-floor   # also recomputes the floor
```

Review the diff of the baseline file before you commit it, and say why in the commit message.

Acceptable:

- **Scores fell or a violation was fixed.** The check prints "lower than the baseline" or "fixed" and suggests an
  update. Updating locks the improvement in, so it cannot quietly come back.
- **A new course, instrument or language passes the limits for new instruments.** Update so that its numbers are
  ratcheted from then on.
- **A count changed for a reason that is not a cue.** For example, items were removed and a percentage moved by
  arithmetic, not because an option got longer. Check with `--items` first.

Not acceptable:

- Updating to make CI pass after adding or rewriting items whose options give the key away. Rewrite the options:
  make the key and the distractors similar in length and detail, and give every option the same kind of glosses.
- Adding an Arabic-rule exception or lowering the gloss floor without the owner's agreement. The three rules are the
  owner's standing rules; an exception needs a stated reason (for example a diagram whose left-to-right order is
  part of what it shows) recorded in the commit message.
- Adding a claims-lint exclusion to hide a hit. Fix the wording at its source.
