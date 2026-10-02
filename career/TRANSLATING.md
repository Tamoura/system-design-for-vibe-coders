# Arabic edition — translation guide (From Graduate to Hired)

Not published. Every translator follows this.

## Language and English terms
- Modern Standard Arabic, clear and professional, like a well-written university or professional training manual. Faithful: same meaning, structure, emphasis, lists, tables. Never summarise, add or drop content.
- **English beside every technical term everywhere.** In every paragraph, list item, table cell, heading, quiz question, option and answer, each technical term and key phrase carries its English in parentheses on its first appearance in that unit (a unit = one paragraph, one list item, one table cell, one heading): `السيرة الذاتية (CV)`, `معرض الأعمال (portfolio)`, `نظام تتبّع المتقدّمين (applicant-tracking system, ATS)`, `المقابلة السلوكية (behavioural interview)`, `خطة الأيام التسعين الأولى (30-60-90 plan)`. Aim for roughly one gloss every 4–6 Arabic words in technical text. Gloss whole phrases, never split a construct. A space always separates the Arabic word from `(`. Use the English exactly as the English lesson words it.
- Key phrases, rules of thumb, labels and framework step names also get their English, e.g. `يكتمل عندما (Done when)`.
- If a gloss ends in punctuation (`?`, `.`, `!`), wrap it in a left-to-right isolate (the characters U+2066 before `(` and U+2069 after `)`), so it displays correctly in right-to-left text.
- Names of tools, products, standards, companies, platforms, programming languages and commands stay in their English form (GitHub, LinkedIn, LeetCode, HackerRank, Git, Python, SQL, Docker, AWS, Azure, Google Cloud, Claude Code, Cursor, Copilot, Workday, Greenhouse). On first use in a unit you may add a short Arabic rendering before it.
- People: Omar عمر, Huda هدى, Yousef يوسف, Reem ريم, Mohammed محمد, Khalid خالد, Aisha عائشة, Tariq طارق, Dana دانة, Salem سالم. Najm Bank → بنك نجم (Najm Bank). Najm Tech Graduate Programme → برنامج نجم للخرّيجين التقنيين (Najm Tech Graduate Programme); Sadeem Pay → سديم باي (Sadeem Pay).

## Fixed terms
| English | Arabic |
|---|---|
| graduate / fresh graduate | خرّيج / خرّيج جديد |
| entry-level / junior | مستوى المبتدئين (entry-level) / مبتدئ (junior) |
| hiring manager / recruiter | مدير التوظيف (hiring manager) / مسؤول التوظيف (recruiter) |
| job description | الوصف الوظيفي (job description) |
| CV / résumé | السيرة الذاتية (CV) |
| cover letter | خطاب التقديم (cover letter) |
| portfolio | معرض الأعمال (portfolio) |
| referral | الإحالة (referral) |
| networking | بناء العلاقات المهنية (networking) |
| interview loop | جولات المقابلات (interview loop) |
| behavioural interview | المقابلة السلوكية (behavioural interview) |
| technical interview / take-home | المقابلة التقنية (technical interview) / المهمة المنزلية (take-home) |
| system design | تصميم الأنظمة (system design) |
| offer / negotiation | العرض الوظيفي (offer) / التفاوض (negotiation) |
| total compensation | إجمالي المكافآت (total compensation) |
| onboarding | التهيئة الوظيفية (onboarding) |
| pull request (PR) / code review | طلب الدمج (pull request, PR) / مراجعة الشيفرة (code review) |
| AI coding agent | وكيل البرمجة بالذكاء الاصطناعي (AI coding agent) |
| role path / study path | مسار الدور (role path) / المسار الدراسي (study path) |
| nationalisation programme | برنامج التوطين (nationalisation programme) |

## Structure the build depends on (do not break)
- Module heading: `# الوحدة N — العنوان` (N unchanged). Lesson heading: `# N.M — العنوان` (numbers unchanged).
- The line right after each lesson heading, translated exactly like this pattern:
  `*المستوى (Level): 🟡 متوسط (Intermediate)* · *المتطلبات (Prerequisites): 1.1، 1.2* · *الخطوة (Step): Build, Prove*`
  (🟢 مبتدئ (Beginner) / 🟡 متوسط (Intermediate) / 🔴 متقدم (Advanced); keep the same emoji; keep lesson numbers; **step names stay in English** exactly as in the English line; separate lesson lists with «، »). If the English has no prerequisites, omit that part as the English does.
- Section headings keep their emoji first, translated: `## ⚡ الدرس في دقيقة (In 60 seconds)`, `## 🧭 لماذا يهم (Why it matters)`, `## 📐 كيف يعمل (How it works)`, `### 🟢 الأساسيات (The essentials)`, `### 🟡 التعمق أكثر (Going deeper)`, `### 🔴 نظرة الخبير (Expert view)`, `## 🧰 الأدوات (The toolkit)`, `## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)`, `## 🛠️ التمارين (Exercises)`, `## ⚠️ أخطاء وفخاخ (Mistakes and traps)`, `## 🧾 الخلاصة (Recap)`, `## ✍️ اختبر نفسك (Check yourself)`, `## 📚 المراجع (References)` (7.2: `## ✍️ الامتحان التدريبي (Practice exam)`). Same number of `#`/`##`/`###` headings in the same order as the English.
- **🧰 tables:** the first cell of every row must START with the same bold English name as the English row, exactly (e.g. `**STAR method** — …`, `**Applicant-tracking system (ATS)** — …`). Translate everything after the bold name and the other cells. Header row: `| المورد أو الأداة أو النموذج (Resource, tool or template) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |`.
- **Quizzes:** keep the question numbers; options stay labelled `- A.` `- B.` `- C.` `- D.` in Latin letters and in the same order; `<details><summary>الإجابة</summary>` then a blank line, then `**X.**` with the SAME correct letter as the English; letters cited in explanations stay the same Latin letters. Same number of questions and `<details>` blocks. In 7.2 keep the step/lesson tag in English, e.g. `*(Interview · 5.1)*`.
- **Code blocks stay byte-identical** (code, SQL, YAML, shell, config). Comments inside code stay in English.
- **Mermaid diagrams:** keep the syntax, the direction line and node IDs exactly; translate only the label text into Arabic (no English in the labels, no parentheses inside labels). The build adds the English and flips the direction for Arabic afterwards.
- **Links:** keep external URLs unchanged. Relative links to other courses in the library point to their Arabic pages: `index.html` → `index.ar.html`, `index.en.html` → `index.ar.html`, `learning-path.html` → `learning-path.ar.html`, `assessment.html` → `assessment.ar.html` (keep the `#…` part). Translate the link text.
- Keep unchanged: inline `code`, numbers, `---` separators, tables' column counts.
- `*Done when:*` → `*يكتمل عندما (Done when):*`.

## Verify
Run: `python3 career/check_ar.py <english file> <arabic file>` until it prints ✓. It checks headings, the level/step lines, section emoji order, 🧰 bold names, quiz letters, details blocks, code and mermaid blocks, links and that the text is really Arabic.
