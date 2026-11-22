# Arabic edition — translation guide (Digital Practice)

Not published. Every Arabic writer follows this.

## Language and English terms
- Modern Standard Arabic, clear and professional, the way a good Arabic technology writer would explain it to a newcomer. Write it **as Arabic**: restructure sentences the Arabic way (short sentences, active voice, verb first where natural), no word-for-word translation, no English idioms carried over. Same meaning, structure, lists, tables and facts as the English; never summarise, add or drop content.
- **English only on technical terms, once per lesson.** Add the English in parentheses only after a real technical or business term, and only the first time that term appears in each lesson: `مسار القيمة (value stream)`. Do not gloss plain words or phrases, do not repeat a gloss already given in the lesson, and never nest parentheses. Parentheses that hold formulas, numbers, option letters or lesson pointers are content, not glosses, so they always stay. Inside a quiz item, treat the same term the same way in every option.
- Product, platform, protocol, acronym and standard names stay in Latin letters with no parentheses (Git, GitHub, ITIL, Scrum, DORA, API, SaaS, SQL).
- If a gloss ends in punctuation (`?`, `.`, `!`), wrap it in a left-to-right isolate (U+2066 before `(` and U+2069 after `)`).
- Fictional names: Qafila قافلة (fictional), Maha مها, Faisal فيصل, Aisha عائشة, Karim كريم, Salma سلمى, Hamad حمد, Dana دانة, Bilal بلال, Yasmin ياسمين. Growth stages: Launch الانطلاق, Traction الجذب, Growth النمو, Scale-up التوسّع, Established الرسوخ. Say in 0.2 that Qafila is fictional.
- Numbers use Western digits (1, 2, 3), as in the other Arabic editions. Currency amounts stay as in the English (illustrative).
- "DPO" is always written with the Arabic word for protection: «مسؤول حماية البيانات (DPO)».

## Fixed terms
Use the library term table everywhere (accuracy الصحة الإجمالية, precision الدقة, recall الشمول, tool call استدعاء الأداة, deadline الموعد النهائي, timeout المهلة, middleware البرمجية الوسيطة, proxy الخادم الوسيط, backoff التأخير الأسي, rollback التراجع, capstone المشروع الختامي, vendor المورّد, provider المزوّد, TTL مدة البقاء, postmortem مراجعة ما بعد الحادثة, pilot التجربة التشغيلية, false positive النتيجة الإيجابية الكاذبة). Course terms:

| English | Arabic |
|---|---|
| digital practice / practitioner | الممارسة الرقمية (digital practice) / الممارس |
| digital product / service / customer | المنتج الرقمي (digital product) / الخدمة / العميل |
| value / outcome / output | القيمة / النتيجة (outcome) / المُخرَج (output) |
| job to be done / assumption / hypothesis | المهمة المطلوب إنجازها (job to be done) / الافتراض / الفرضية |
| discovery / prototype / MVP | الاستكشاف (discovery) / النموذج الأولي (prototype) / المنتج الأدنى القابل للتجربة (MVP) |
| business model / unit economics | نموذج العمل (business model) / اقتصاديات الوحدة (unit economics) |
| version control / repository / branch / pull request | التحكم في الإصدارات (version control) / المستودع (repository) / الفرع (branch) / طلب الدمج (pull request) |
| code review / working agreement | مراجعة الشيفرة (code review) / اتفاق العمل (working agreement) |
| automated test / continuous integration (CI) | الاختبار الآلي / التكامل المستمر (CI) |
| continuous delivery / deployment / release / rollback | التسليم المستمر (continuous delivery) / النشر (deployment) / الإصدار (release) / التراجع |
| pipeline / environment / infrastructure as code | خط النشر (pipeline) / البيئة / البنية التحتية بوصفها شيفرة (infrastructure as code) |
| monitoring / alert / on-call / runbook | المراقبة (monitoring) / التنبيه (alert) / المناوبة (on-call) / دليل التشغيل (runbook) |
| incident / post-incident review / SLO / error budget | الحادثة (incident) / مراجعة ما بعد الحادثة (post-incident review) / هدف مستوى الخدمة (SLO) / ميزانية الخطأ (error budget) |
| psychological safety / retrospective | الأمان النفسي (psychological safety) / الاجتماع الاستعادي (retrospective) |
| backlog / iteration / work in progress (WIP) / flow | قائمة الأعمال المتراكمة (backlog) / التكرار (iteration) / العمل الجاري (WIP) / التدفّق (flow) |
| roadmap / prioritisation / user story / acceptance criteria | خارطة الطريق (roadmap) / ترتيب الأولويات / قصة المستخدم (user story) / معايير القبول (acceptance criteria) |
| product analytics / experiment / A/B test | تحليلات المنتج (product analytics) / التجربة / اختبار A/B |
| service desk / request / knowledge base / service level | مكتب الخدمة (service desk) / الطلب / قاعدة المعرفة (knowledge base) / مستوى الخدمة |
| platform team / enabling team / stream-aligned team | فريق المنصة (platform team) / فريق التمكين (enabling team) / الفريق المحاذي لمسار القيمة (stream-aligned team) |
| dependency / developer experience | الاعتمادية (dependency) / تجربة المطوّر (developer experience) |
| architecture decision record (ADR) / trade-off | سجل القرار المعماري (ADR) / المفاضلة (trade-off) |
| data quality / data owner / personal data | جودة البيانات / مالك البيانات (data owner) / البيانات الشخصية |
| technical debt / modernisation | الدَّين التقني (technical debt) / التحديث (modernisation) |
| budget / business case / product funding | الميزانية / دراسة الجدوى (business case) / تمويل المنتجات (product funding) |
| unit cost / cloud cost | تكلفة الوحدة (unit cost) / تكلفة السحابة |
| supplier / contract / outsourcing | المورّد / العقد / الإسناد الخارجي (outsourcing) |
| governance / decision rights / guardrail | الحوكمة (governance) / صلاحيات القرار (decision rights) / الضابط الوقائي (guardrail) |
| risk / control / audit / compliance | المخاطر / الضابط الرقابي (control) / التدقيق (audit) / الامتثال (compliance) |
| enterprise architecture / portfolio | البنية المؤسسية (enterprise architecture) / المحفظة (portfolio) |
| body of knowledge / learning path | مجموعة المعارف (body of knowledge) / مسار التعلّم (learning path) |
| template | القالب (not «النموذج», kept for an AI model or a business model) |

## Structure the build depends on (do not break)
- Module heading: `# الوحدة N — العنوان` (N unchanged). Lesson heading: `# N.M — العنوان` (numbers unchanged).
- The line right after each lesson heading, translated exactly like this pattern:
  `*المستوى (Level): 🟡 متوسط (Intermediate)* · *المتطلبات (Prerequisites): 1.1، 1.2* · *الخطوة (Step): Build, Deliver*`
  (🟢 مبتدئ (Beginner) / 🟡 متوسط (Intermediate) / 🔴 متقدم (Advanced); keep the same emoji; keep lesson numbers; **step names stay in English** exactly as in the English line; separate lesson lists with «، »). Step names are tags: the 0.2 step table pairs each with its Arabic name (`**Build** — البناء`); in running prose that explains a step, write the Arabic name with the English after it, «خطوة البناء (Build)». If the English has no prerequisites, omit that part as the English does.
- Section headings keep their emoji first, translated: `## ⚡ الدرس في دقيقة (In 60 seconds)`, `## 🧭 لماذا يهم (Why it matters)`, `## 📐 كيف يعمل (How it works)`, `### 🟢 الأساسيات (The essentials)`, `### 🟡 التعمق أكثر (Going deeper)`, `### 🔴 نظرة الخبير (Expert view)`, `## 🧰 الأدوات (The toolkit)`, `## 🏛️ عمليًا في قافلة (In practice at Qafila)`, `## 🛠️ التمارين (Exercises)`, `## ⚠️ أخطاء وفخاخ (Mistakes and traps)`, `## 🧾 الخلاصة (Recap)`, `## ✍️ اختبر نفسك (Check yourself)`, `## 📚 المراجع (References)` (13.2: `## ✍️ الامتحان التدريبي (Practice exam)`). Same number of `#`/`##`/`###` headings in the same order as the English.
- **🧰 tables:** the first cell of every row must START with the same bold English name as the English row, exactly, followed by ` — ` and the Arabic name (e.g. `**Problem statement** — بيان المشكلة`, `**Pull request checklist** — قائمة تحقق طلب الدمج`). Translate everything after the bold name and the other cells. Header row: `| المصدر أو الأداة أو القالب (Resource, tool or template) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |`. `check_ar.py` fails any Arabic 🧰 row or header that breaks this pattern.
- **Quizzes:** keep the question numbers; options stay labelled `- A.` `- B.` `- C.` `- D.` in Latin letters and in the same order; `<details><summary>الإجابة</summary>` then a blank line, then `**X.**` with the SAME correct letter as the English; letters cited in explanations stay the same Latin letters. Same number of questions and `<details>` blocks. In 13.2 keep the step/lesson tag in English, e.g. `*(Build · 3.2)*`.
- **Code blocks stay byte-identical** (code, SQL, YAML, shell, config). Comments inside code stay in English.
- **Mermaid diagrams:** keep the syntax and node IDs exactly; translate only the label text into Arabic (no English in the labels, no parentheses inside labels). Diagrams run right to left in Arabic: write `flowchart RL` (or `direction RL`) where the English has `LR`.
- **Links:** keep external URLs unchanged. Relative links to other courses in the library point to their Arabic pages: `index.html` → `index.ar.html`, `index.en.html` → `index.ar.html`, `learning-path.html` → `learning-path.ar.html`, `assessment.html` → `assessment.ar.html` (keep the `#…` part). Translate the link text.
- Keep unchanged: inline `code`, numbers, `---` separators, tables' column counts.
- `*Done when:*` → `*يكتمل عندما (Done when):*`.

## Verify
Run: `python3 dprac/check_ar.py <english file> <arabic file>` until it prints ✓. It checks headings, the level/step lines, section emoji order, 🧰 bold names, quiz letters, details blocks, code and mermaid blocks, links and that the text is really Arabic.
