# Lesson-Authoring Spec (read this fully before writing)

You are writing lessons for **System Design for Vibe Coders** — a bilingual
(English + Arabic) course teaching practical production engineering to people who
build with AI agents, **including people who have never written code**. Match the
existing written lessons exactly. Study these before writing:

- `modules/00-foundations/foundations.md` + `.ar.md` (the register + format bible)
- `modules/0-the-gap/the-gap.md` + `.ar.md`
- `modules/01-anatomy-of-a-real-app/lesson-1-draw-the-boxes.md` + `.ar.md`
- `modules/03-caching/lesson-2-cache-poisoning.md` + `.ar.md` (flagship)
- `OUTLINE.md` — the lesson list + one-line briefs for YOUR module
- `war-stories/incident-bank.md` — our real incidents (the 🔥 source)
- `war-stories/famous-cases.md` — industry cases to pair in each lesson
- `GLOSSARY.md` / `GLOSSARY.ar.md` — term definitions

## Output

Write TWO files for your module:
- `modules/NN-slug/module.md` — all lessons in English, one after another
- `modules/NN-slug/module.ar.md` — the Arabic mirror

Each lesson starts with `# N.M — Title` (e.g. `# 2.1 — The database is the easy part`).
Arabic lesson headings use the same `# N.M — عنوان`. Separate lessons with a blank
line, `---`, blank line.

## The six-part anatomy (EVERY lesson, both languages, in this order)

1. `## 🔥 The War Story` — open with a concrete incident. Use a real one from the
   incident bank when your outline line references it; otherwise use a famous case
   from famous-cases.md. Tell it as a story: symptoms → wrong theories → root cause
   → the fix that shipped. 2–4 short paragraphs. Land the lesson's core idea in one
   bold sentence. (Concept-only lessons with no incident: open with a famous case
   or a vivid "the day this bites you" scenario instead — still under 🔥.)
2. `## 📐 The Principle` — teach the concept from first principles, plain language,
   defined-before-used. Include **at least one Mermaid diagram** (flowchart,
   sequence, table-as-diagram, etc.). Use short numbered sub-points `### 1. ...`
   when there are distinct ideas. Include a Markdown table where it clarifies.
   Pair in a famous case if the war story was one of ours (and vice versa).
3. `## 🎛️ Direct Your Agent` — this is the "build-along," rewritten for non-coders:
   numbered steps, each an **exact prompt the reader gives their agent**, in a
   blockquote. Apply it to **Relay** (the course's generic build-along product:
   accounts, creator content, media uploads, feeds, email, a mobile client). End
   with a commit-checkpoint line. Add ONE optional `> 🔧 **Under the hood**` box
   with the manual command/code for readers who do code. Optionally a short
   "Review questions" or "Context to give" sub-block.
4. `## ✅ Verify It` — a checklist of `- [ ] ...` items, each checkable **without
   reading code**: things the reader sees, clicks, or makes the agent demonstrate
   from the layer users touch. 4–6 items. At least one should reference the war
   story ("you can retell X and name Y").
5. `## 🧾 Recap card` — 4–5 `- ` bullets, the memorable takeaways.
6. `## 📚 References & further wandering` — 4–6 `- ` bullets: real, checkable
   sources (RFCs, MDN, Google SRE book, the System Design Primer, official docs,
   the specific postmortem). Prefer things that actually exist; do not invent URLs.

End each lesson's file section (last lesson of the module only) with a one-line
pointer to the next module.

## Cross-references

Reference other lessons as `(3.2)` or "lesson 5.2" — they must exist in OUTLINE.md.
Reference incidents by their nature, not internal ticket numbers.

## Pillar labels (the converter depends on these EXACT headings)

English: `## 🔥 The War Story`, `## 📐 The Principle`, `## 🎛️ Direct Your Agent`,
`## ✅ Verify It`, `## 🧾 Recap card`, `## 📚 References & further wandering`.

Arabic: `## 🔥 قصة من الميدان`, `## 📐 المبدأ`, `## 🎛️ وجّه وكيلك`,
`## ✅ تحقق منه`, `## 🧾 بطاقة الخلاصة`, `## 📚 المراجع ومزيد من القراءة`.

(The 🔥/📐/🎛️/✅ emoji + the first word must match so the styled boxes render.)

## English voice

Direct, concrete, a smart friend who has operated real systems. Short sentences.
Concrete nouns. No hype, no "in today's fast-paced world." Technical terms defined
on first use. Diagrams do heavy lifting.

## Arabic register (CRITICAL — the CEO rejected two earlier attempts)

Write **professional-concise Modern Standard Arabic** — the style of good Arabic
technical documentation (like Hsoub Academy / حسوب). Rules:

- **Short, clear sentences.** No literary flourishes, no rhymed prose, no archaic
  or ornate vocabulary. NOT «بأفدح الأثمان»، NOT «أمّا النشرُ فهو أن...»، NOT
  «ادّعاءُ مكوّنٍ يرتدي زيَّ نظام». These read as *poor* — too effortful.
- **No verbless telegraphic fragments either.** Use full sentences with verbs and
  normal connectors (لأن، عندما، لكن، لذلك، ثم، أي).
- **Technical terms: Arabic then English in parentheses on first mention**, Arabic
  alone after. Examples: النشر (Deploy)، الكاش (Cache)، المستودع (Repository)،
  قاعدة البيانات (Database)، الوسيط العكسي (Reverse Proxy)، تحديد المعدل
  (Rate Limiting)، المصادقة (Authentication). Product/tool names stay Latin
  (Cloudflare, Sentry, Stripe, Redis, nginx, git).
- Numbers as digits (440 مليون دولار، 45 دقيقة، 9 خوادم).
- Use ✓/✗ and diagrams identically to English; translate diagram node labels to
  Arabic (keep Latin product names).

**Calibration example** (this is the target — match it):

> النشر (Deploy) هو نقل نسخة محددة من الكود إلى الخادم الدائم لتصبح متاحة
> للمستخدمين. هناك فرق جوهري بين "يعمل على جهازي" و"يعمل على الإنترنت": هما مكانان
> مختلفان، والانتقال بينهما عملية مقصودة يجب أن تكتمل على كل الخوادم بالنسخة نفسها،
> مع التحقق من ذلك. هذا بالضبط ما فشلت فيه Knight Capital.
>
> التراجع (Rollback) هو العودة إلى نسخة سابقة. وبما أن جميع النسخ محفوظة في السجل،
> فالعودة قرار بسيط وليست حالة طوارئ.

The Arabic is a faithful mirror of the English lesson — same structure, same
diagrams, same checklist items, same references — not a looser paraphrase.

## Length

Each lesson ≈ 900–1,600 words of body per language. Quality over padding. A tight
1,000-word lesson beats a bloated 2,000-word one.

## Do not

- Do not invent incidents; use the banks. Do not invent URLs.
- Do not use the old pillar names (Build-Along / Prompting Your Agent).
- Do not write code the non-coder must type in the main flow — code lives only in
  the optional 🔧 box.
- Do not skip the Arabic file or write it in a different register than the example.
