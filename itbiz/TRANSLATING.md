# Arabic edition — translation guide (Running IT as a Business)

Not published. Every Arabic writer follows this.

## Language and English terms
- Modern Standard Arabic, clear and professional, the way a good Arabic technology-management writer would explain it. Write it **as Arabic**: restructure sentences the Arabic way (short sentences, active voice, verb first where natural), no word-for-word translation, no English idioms carried over. Same meaning, structure, lists, tables and facts as the English; never summarise, add or drop content.
- **English only on technical terms, once per lesson.** Add the English in parentheses only after a real technical or business term, and only the first time that term appears in each lesson: `مسار القيمة (value stream)`. Do not gloss plain words or phrases, do not repeat a gloss already given in the lesson, and never nest parentheses. Parentheses that hold formulas, numbers, option letters or lesson pointers are content, not glosses, so they always stay. Inside a quiz item, treat the same term the same way in every option.
- Product, platform, protocol, acronym and standard names stay in Latin letters with no parentheses (ITIL, COBIT, TOGAF, DORA, CMDB, SaaS, SQL).
- If a gloss ends in punctuation (`?`, `.`, `!`), wrap it in a left-to-right isolate (U+2066 before `(` and U+2069 after `)`).
- Fictional names: Najm Bank بنك نجم (fictional), Omar عمر, Huda هدى, Yousef يوسف, Reem ريم, Sami سامي, Tariq طارق, Lina لينا, Nour نور. Say in 0.2 that Najm Bank is fictional.
- Numbers use Western digits (1, 2, 3), as in the other Arabic editions. Currency amounts stay as in the English (illustrative).
- "DPO" is always written with the Arabic word for protection: «مسؤول حماية البيانات (DPO)».

## Fixed terms
Use the library term table everywhere (accuracy الصحة الإجمالية, precision الدقة, recall الشمول, tool call استدعاء الأداة, deadline الموعد النهائي, timeout المهلة, middleware البرمجية الوسيطة, proxy الخادم الوسيط, backoff التأخير الأسي, rollback التراجع, capstone المشروع الختامي, vendor المورّد, provider المزوّد, TTL مدة البقاء, postmortem مراجعة ما بعد الحادثة, pilot التجربة التشغيلية, false positive النتيجة الإيجابية الكاذبة). Course terms:

| English | Arabic |
|---|---|
| value stream / value-stream map | مسار القيمة (value stream) / خريطة مسار القيمة (value-stream map) |
| flow / lead time / cycle time | التدفّق (flow) / زمن التسليم الكلي (lead time) / زمن الدورة (cycle time) |
| hand-off / wait time | التسليم بين الفرق (hand-off) / زمن الانتظار |
| digital product / product owner / product manager | المنتج الرقمي (digital product) / مالك المنتج (product owner) / مدير المنتج (product manager) |
| service / service catalogue / service owner | الخدمة / دليل الخدمات (service catalogue) / مالك الخدمة (service owner) |
| operating model | نموذج التشغيل (operating model) |
| platform team / enabling team / stream-aligned team | فريق المنصة (platform team) / فريق التمكين (enabling team) / الفريق المحاذي لمسار القيمة (stream-aligned team) |
| portfolio / investment / business case | المحفظة (portfolio) / الاستثمار / دراسة الجدوى (business case) |
| cost of delay | كلفة التأخير (cost of delay) |
| demand / intake | الطلب (demand) / بوابة الاستقبال (intake) |
| backlog / requirement / traceability | قائمة الأعمال المتراكمة (backlog) / المتطلب / التتبّع (traceability) |
| non-functional requirement | المتطلب غير الوظيفي (non-functional requirement) |
| pipeline / quality gate | خط النشر (pipeline) / بوابة الجودة (quality gate) |
| release / deployment / change | الإصدار (release) / النشر (deployment) / التغيير (change) |
| change advisory board (CAB) / standard change | مجلس استشارات التغيير (CAB) / التغيير القياسي (standard change) |
| environment / configuration item / CMDB | البيئة / عنصر التهيئة (configuration item) / قاعدة بيانات إدارة التهيئة (CMDB) |
| request fulfilment / self-service | تلبية الطلبات (request fulfilment) / الخدمة الذاتية (self-service) |
| subscription / entitlement / access right | الاشتراك / الاستحقاق (entitlement) / صلاحية الوصول |
| showback / chargeback | عرض التكلفة (showback) / تحميل التكلفة (chargeback) |
| incident / problem / event | الحادثة (incident) / المشكلة (problem) / الحدث (event) |
| service level / SLO / error budget | مستوى الخدمة / هدف مستوى الخدمة (SLO) / ميزانية الخطأ (error budget) |
| system of record | نظام السجل المرجعي (system of record) |
| asset / reconciliation | الأصل / المطابقة (reconciliation) |
| unit cost / cost model | تكلفة الوحدة (unit cost) / نموذج التكلفة (cost model) |
| sourcing / supplier / multi-supplier integration | التوريد (sourcing) / المورّد / تكامل المورّدين المتعددين (multi-supplier integration) |
| control / control owner / audit evidence | الضابط الرقابي (control) / مالك الضابط / دليل التدقيق (audit evidence) |
| toolchain / rationalisation | سلسلة الأدوات (toolchain) / ترشيد الأدوات (rationalisation) |
| maturity assessment / roadmap | تقييم النضج (maturity assessment) / خارطة الطريق (roadmap) |
| template | القالب (not «النموذج», kept for an AI model or the operating model) |

## Structure the build depends on (do not break)
- Module heading: `# الوحدة N — العنوان` (N unchanged). Lesson heading: `# N.M — العنوان` (numbers unchanged).
- The line right after each lesson heading, translated exactly like this pattern:
  `*المستوى (Level): 🟡 متوسط (Intermediate)* · *المتطلبات (Prerequisites): 1.1، 1.2* · *الخطوة (Step): Sell, Launch*`
  (🟢 مبتدئ (Beginner) / 🟡 متوسط (Intermediate) / 🔴 متقدم (Advanced); keep the same emoji; keep lesson numbers; **step names stay in English** exactly as in the English line; separate lesson lists with «، »). Step names are tags: the 0.2 step table pairs each with its Arabic name (`**Govern** — الحوكمة`); in running prose that explains a step, write the Arabic name with the English after it, «خطوة الحوكمة (Govern)». If the English has no prerequisites, omit that part as the English does.
- Section headings keep their emoji first, translated: `## ⚡ الدرس في دقيقة (In 60 seconds)`, `## 🧭 لماذا يهم (Why it matters)`, `## 📐 كيف يعمل (How it works)`, `### 🟢 الأساسيات (The essentials)`, `### 🟡 التعمق أكثر (Going deeper)`, `### 🔴 نظرة الخبير (Expert view)`, `## 🧰 الأدوات (The toolkit)`, `## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)`, `## 🛠️ التمارين (Exercises)`, `## ⚠️ أخطاء وفخاخ (Mistakes and traps)`, `## 🧾 الخلاصة (Recap)`, `## ✍️ اختبر نفسك (Check yourself)`, `## 📚 المراجع (References)` (13.2: `## ✍️ الامتحان التدريبي (Practice exam)`). Same number of `#`/`##`/`###` headings in the same order as the English.
- **🧰 tables:** the first cell of every row must START with the same bold English name as the English row, exactly, followed by ` — ` and the Arabic name (e.g. `**Value-stream map** — خريطة مسار القيمة`, `**Service catalogue entry** — مدخل دليل الخدمات`). Translate everything after the bold name and the other cells. Header row: `| المصدر أو الأداة أو القالب (Resource, tool or template) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |`. `check_ar.py` fails any Arabic 🧰 row or header that breaks this pattern.
- **Quizzes:** keep the question numbers; options stay labelled `- A.` `- B.` `- C.` `- D.` in Latin letters and in the same order; `<details><summary>الإجابة</summary>` then a blank line, then `**X.**` with the SAME correct letter as the English; letters cited in explanations stay the same Latin letters. Same number of questions and `<details>` blocks. In 13.2 keep the step/lesson tag in English, e.g. `*(Release · 6.2)*`.
- **Code blocks stay byte-identical** (code, SQL, YAML, shell, config). Comments inside code stay in English.
- **Mermaid diagrams:** keep the syntax and node IDs exactly; translate only the label text into Arabic (no English in the labels, no parentheses inside labels). Diagrams run right to left in Arabic: write `flowchart RL` (or `direction RL`) where the English has `LR`.
- **Links:** keep external URLs unchanged. Relative links to other courses in the library point to their Arabic pages: `index.html` → `index.ar.html`, `index.en.html` → `index.ar.html`, `learning-path.html` → `learning-path.ar.html`, `assessment.html` → `assessment.ar.html` (keep the `#…` part). Translate the link text.
- Keep unchanged: inline `code`, numbers, `---` separators, tables' column counts.
- `*Done when:*` → `*يكتمل عندما (Done when):*`.

## Verify
Run: `python3 itbiz/check_ar.py <english file> <arabic file>` until it prints ✓. It checks headings, the level/step lines, section emoji order, 🧰 bold names, quiz letters, details blocks, code and mermaid blocks, links and that the text is really Arabic.
