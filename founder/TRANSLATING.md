# Arabic edition — translation guide (Founder's Playbook for AI-First Builders)

Not published. Every Arabic writer follows this.

## Language and English terms
- Modern Standard Arabic, clear and professional, the way a good Arabic business or technology writer would explain it. Write it **as Arabic**: restructure sentences the Arabic way (short sentences, active voice, verb first where natural), no word-for-word translation, no English idioms carried over. Same meaning, structure, lists, tables and facts as the English; never summarise, add or drop content.
- **English only on technical terms, once per lesson.** Add the English in parentheses only after a real technical or business term, and only the first time that term appears in each lesson: `الاقتصاديات الوحدوية (unit economics)`. Do not gloss plain words or phrases, do not repeat a gloss already given in the lesson, and never nest parentheses. Parentheses that hold formulas, numbers, option letters or lesson pointers are content, not glosses, so they always stay. Inside a quiz item, treat the same term the same way in every option.
- Product, platform, protocol, acronym and standard names stay in Latin letters with no parentheses (Stripe, GitHub, GDPR, CSV, SQL).
- If a gloss ends in punctuation (`?`, `.`, `!`), wrap it in a left-to-right isolate (U+2066 before `(` and U+2069 after `)`).
- Fictional names: Tick تيك (Tick, the fictional app), Layla ليلى, Nadia نادية, Sam سام, Mona منى, Hana هناء, Rashid راشد. Say in 0.1 that Tick is fictional.
- Numbers use Western digits (1, 2, 3), as in the other Arabic editions. Currency amounts stay as in the English (illustrative).
- "DPO" is always written with the Arabic word for protection: «مسؤول حماية البيانات (DPO)».

## Fixed terms
| English | Arabic |
|---|---|
| founder / solo founder | المؤسس / المؤسس المنفرد (solo founder) |
| customer discovery / customer interview | استكشاف العملاء (customer discovery) / مقابلة العميل (customer interview) |
| smoke test / pre-sale | اختبار الدخان (smoke test) / البيع المسبق (pre-sale) |
| minimum viable product (MVP) | الحد الأدنى من المنتج القابل للتسويق (MVP) |
| kill list | قائمة الاستبعاد (kill list) |
| unit economics | الاقتصاديات الوحدوية (unit economics) |
| pricing / price test | التسعير (pricing) / اختبار السعر (price test) |
| runway | مدة الاستمرار المالي (runway) |
| invoice | الفاتورة (invoice) |
| onboarding | التهيئة (onboarding) |
| churn | فقدان العملاء (churn) |
| terms of service / privacy notice | شروط الخدمة (terms of service) / إشعار الخصوصية (privacy notice) |
| key-person risk | مخاطر الاعتماد على شخص واحد (key-person risk) |
| handover pack | حزمة التسليم (handover pack) |
| vendor lock-in | الارتباط بمورّد واحد (vendor lock-in) |
| vendor | المورّد (plural المورّدون / المورّدين); never المزوّد or البائع for "vendor" |
| provider (model, payment, message, cloud provider) | المزوّد: مزوّد النموذج، مزوّد الدفع، مزوّد الرسائل |
| pilot / pilot deposit | التجربة التشغيلية (pilot) / عربون التجربة; never «تجربة تجريبية» |
| free trial | التجربة المجانية |
| capstone | المشروع الختامي (capstone) |
| rollback / undo | التراجع |
| deadline / timeout | الموعد النهائي / المهلة |
| post-incident note | ملاحظة ما بعد الحادثة (post-incident note) |
| typical (customer, task) | معتاد: عميل معتاد، مهمة معتادة (not «نموذجي», which reads as "model") |
| template | القالب (not «النموذج», which is kept for an AI model) |
| sample (invoice, records) | عيّنة: عيّنة فاتورة |

## Structure the build depends on (do not break)
- Module heading: `# الوحدة N — العنوان` (N unchanged). Lesson heading: `# N.M — العنوان` (numbers unchanged).
- The line right after each lesson heading, translated exactly like this pattern:
  `*المستوى (Level): 🟡 متوسط (Intermediate)* · *المتطلبات (Prerequisites): 1.1، 1.2* · *الخطوة (Step): Sell, Launch*`
  (🟢 مبتدئ (Beginner) / 🟡 متوسط (Intermediate) / 🔴 متقدم (Advanced); keep the same emoji; keep lesson numbers; **step names stay in English** exactly as in the English line; separate lesson lists with «، »). Step names are tags: the 0.2 step table pairs each with its Arabic name (`**Protect** — الحماية`); in running prose that explains a step, write the Arabic name with the English after it, «خطوة الحماية (Protect)». If the English has no prerequisites, omit that part as the English does.
- Section headings keep their emoji first, translated: `## ⚡ الدرس في دقيقة (In 60 seconds)`, `## 🧭 لماذا يهم (Why it matters)`, `## 📐 كيف يعمل (How it works)`, `### 🟢 الأساسيات (The essentials)`, `### 🟡 التعمق أكثر (Going deeper)`, `### 🔴 نظرة الخبير (Expert view)`, `## 🧰 الأدوات (The toolkit)`, `## 🏛️ عمليًا مع تيك (In practice with Tick)`, `## 🛠️ التمارين (Exercises)`, `## ⚠️ أخطاء وفخاخ (Mistakes and traps)`, `## 🧾 الخلاصة (Recap)`, `## ✍️ اختبر نفسك (Check yourself)`, `## 📚 المراجع (References)` (7.2: `## ✍️ الامتحان التدريبي (Practice exam)`). Same number of `#`/`##`/`###` headings in the same order as the English.
- **🧰 tables:** the first cell of every row must START with the same bold English name as the English row, exactly, followed by ` — ` and the Arabic name (e.g. `**Kill list** — قائمة الاستبعاد`, `**Unit-economics sheet** — ورقة الاقتصاديات الوحدوية`). Translate everything after the bold name and the other cells. Header row: `| المصدر أو الأداة أو القالب (Resource, tool or template) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |`. `check_ar.py` fails any Arabic 🧰 row or header that breaks this pattern.
- **Quizzes:** keep the question numbers; options stay labelled `- A.` `- B.` `- C.` `- D.` in Latin letters and in the same order; `<details><summary>الإجابة</summary>` then a blank line, then `**X.**` with the SAME correct letter as the English; letters cited in explanations stay the same Latin letters. Same number of questions and `<details>` blocks. In 7.2 keep the step/lesson tag in English, e.g. `*(Interview · 5.1)*`.
- **Code blocks stay byte-identical** (code, SQL, YAML, shell, config). Comments inside code stay in English.
- **Mermaid diagrams:** keep the syntax and node IDs exactly; translate only the label text into Arabic (no English in the labels, no parentheses inside labels). Diagrams run right to left in Arabic: write `flowchart RL` (or `direction RL`) where the English has `LR`.
- **Links:** keep external URLs unchanged. Relative links to other courses in the library point to their Arabic pages: `index.html` → `index.ar.html`, `index.en.html` → `index.ar.html`, `learning-path.html` → `learning-path.ar.html`, `assessment.html` → `assessment.ar.html` (keep the `#…` part). Translate the link text.
- Keep unchanged: inline `code`, numbers, `---` separators, tables' column counts.
- `*Done when:*` → `*يكتمل عندما (Done when):*`.

## Verify
Run: `python3 founder/check_ar.py <english file> <arabic file>` until it prints ✓. It checks headings, the level/step lines, section emoji order, 🧰 bold names, quiz letters, details blocks, code and mermaid blocks, links and that the text is really Arabic.
