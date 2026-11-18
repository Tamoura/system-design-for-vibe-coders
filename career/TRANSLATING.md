# Arabic edition — translation guide (From Graduate to Hired)

Not published. Every translator follows this.

## Language and English terms
- Modern Standard Arabic, clear and professional, like a well-written university or professional training manual. Faithful: same meaning, structure, emphasis, lists, tables. Never summarise, add or drop content.
- **Gloss rule: English at first use per lesson.** Add the English in parentheses only after a real technical or business term, and only the first time that term appears in each lesson: `السيرة الذاتية (CV)`, `معرض الأعمال (portfolio)`, `نظام تتبّع المتقدّمين (applicant-tracking system)`, `المقابلة السلوكية (behavioural interview)`. Do not gloss plain words or key phrases, do not repeat a gloss already given in the lesson, and never nest parentheses (`بنود الملكية الفكرية (IP clauses)`, not `(Intellectual-property (IP) clauses)`). Gloss whole phrases, never split a construct. A space always separates the Arabic word from `(`. Use the English exactly as the English lesson words it. Keep product, standard and acronym names in Latin letters with no parentheses. Parentheses that hold formulas, numbers, option letters or section and lesson pointers are content, not glosses, so they always stay.
- Where an Arabic term spells out an English acronym (STAR: الموقف (Situation)، والمهمة (Task)، والإجراء (Action)، والنتيجة (Result)), gloss each part at first use and keep the English on quiz options that test a letter of the acronym.
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
| total compensation | إجمالي التعويضات (total compensation); not إجمالي المكافآت, which reads as "total bonuses". Use الحزمة only where the English says "package" |
| capstone | المشروع الختامي (capstone); not مشروع التخرّج |
| final-year / graduation project (university) | مشروع التخرّج |
| story bank | بنك القصص (story bank) |
| rubric | معيار التقييم (rubric) |
| references and checks / referees (hiring) | التحقّق من المزكّين والخلفية (references and checks) / المزكّون (referees); never المراجع, which is the bibliography heading |
| exploding offer | العرض الضاغط (exploding offer): an offer with a very short reply deadline |
| cliff (vesting) | فترة الانتظار الأولية (cliff) |
| deadline / timeout | الموعد النهائي / المهلة (expiry: انتهاء المهلة); never المهلة for a deadline |
| rollback / backoff | التراجع / التأخير الأسي (exponential backoff: إعادة المحاولة بتأخير أسي) |
| accuracy / precision / recall | الصحة الإجمالية / الدقة / الشمول (recall); استدعاء is only for calls (استدعاء الأداة = tool call) |
| false positive / false negative | النتيجة الإيجابية الكاذبة (plural الإيجابيات الكاذبة) / النتيجة السلبية الكاذبة (plural السلبيات الكاذبة) |
| organization (tenant) / enterprise | المنظمة / المؤسسات (عملاء المؤسسات، خطة المؤسسات) |
| middleware / proxy / reverse proxy | البرمجية الوسيطة / الخادم الوسيط / الخادم الوسيط العكسي; never bare الوسيط or الوكيل |
| vendor / provider | المورّد / المزوّد (cloud or model provider) |
| TTL | مدة البقاء (TTL) |
| postmortem | مراجعة ما بعد الحادثة (the written document: تقرير مراجعة ما بعد الحادثة) |
| offline / online evaluation | التقييم خارج الإنتاج / التقييم في الإنتاج |
| pilot | التجربة التشغيلية |
| onboarding | التهيئة الوظيفية (onboarding) |
| pull request (PR) / code review | طلب الدمج (pull request, PR) / مراجعة الشيفرة (code review) |
| AI coding agent | وكيل البرمجة بالذكاء الاصطناعي (AI coding agent) |
| role path / study path | مسار الدور (role path) / المسار الدراسي (study path) |
| nationalisation programme | برنامج التوطين (nationalisation programme) |

## Structure the build depends on (do not break)
- Module heading: `# الوحدة N — العنوان` (N unchanged). Lesson heading: `# N.M — العنوان` (numbers unchanged).
- The line right after each lesson heading, translated exactly like this pattern:
  `*المستوى: 🟡 متوسط* · *المتطلبات: 1.1، 1.2* · *الخطوة: Build, Prove*`
  (🟢 مبتدئ / 🟡 متوسط / 🔴 متقدم; keep the same emoji; keep lesson numbers; **step names stay in English** exactly as in the English line; separate lesson lists with «، »). If the English has no prerequisites, omit that part as the English does.
- Section headings keep their emoji first, translated: `## ⚡ الدرس في دقيقة`, `## 🧭 لماذا يهم`, `## 📐 كيف يعمل`, `### 🟢 الأساسيات`, `### 🟡 التعمق أكثر`, `### 🔴 نظرة الخبير`, `## 🧰 الأدوات`, `## 🏛️ عمليًا في بنك نجم`, `## 🛠️ التمارين`, `## ⚠️ أخطاء وفخاخ`, `## 🧾 الخلاصة`, `## ✍️ اختبر نفسك`, `## 📚 المراجع` (7.2: `## ✍️ الامتحان التدريبي (Practice exam)`). Same number of `#`/`##`/`###` headings in the same order as the English.
- **🧰 tables:** the first cell of every row must START with the same bold English name as the English row, exactly (e.g. `**STAR method** — …`, `**Applicant-tracking system (ATS)** — …`). Translate everything after the bold name and the other cells. Header row: `| المورد أو الأداة أو النموذج | ما هو وماذا يفعل | متى تلجأ إليه |`.
- **Quizzes:** keep the question numbers; options stay labelled `- A.` `- B.` `- C.` `- D.` in Latin letters and in the same order; `<details><summary>الإجابة</summary>` then a blank line, then `**X.**` with the SAME correct letter as the English; letters cited in explanations stay the same Latin letters. Same number of questions and `<details>` blocks. In 7.2 keep the step/lesson tag in English, e.g. `*(Interview · 5.1)*`.
- **Code blocks stay byte-identical** (code, SQL, YAML, shell, config). Comments inside code stay in English.
- **Mermaid diagrams:** keep the syntax and node IDs exactly. Arabic diagrams run right to left: `flowchart RL` / `direction RL` where the English is `LR`. Each label is the Arabic text, then `<br/>` and the English label in parentheses, e.g. `["بنك القصص<br/>(Story bank)"]`.
- **Links:** keep external URLs unchanged. Relative links to other courses in the library point to their Arabic pages: `index.html` → `index.ar.html`, `index.en.html` → `index.ar.html`, `learning-path.html` → `learning-path.ar.html`, `assessment.html` → `assessment.ar.html` (keep the `#…` part). Translate the link text.
- Keep unchanged: inline `code`, numbers, `---` separators, tables' column counts.
- `*Done when:*` → `*يكتمل عندما:*`.

## Verify
Run: `python3 career/check_ar.py <english file> <arabic file>` until it prints ✓. It checks headings, the level/step lines, section emoji order, 🧰 bold names, quiz letters, details blocks, code and mermaid blocks, links and that the text is really Arabic.
