# Arabic edition — translation guide (AI Product Management: Zero to Hero)

Not published. Every translator follows this.

## Language and English terms
- Modern Standard Arabic, clear and professional, like a well-written bank or technology training manual. Faithful: same meaning, structure, emphasis, lists, tables. Never summarise, add or drop content.
- **English beside every technical term everywhere.** In every paragraph, list item, table cell, heading, quiz question, option and answer, each technical term and key phrase carries its English in parentheses on its first appearance in that unit (a unit = one paragraph, one list item, one table cell, one heading): `الاكتشاف (discovery)`, `حالة الاستخدام (use case)`, `التقييمات (evals)`, `مجموعة مرجعية (golden set)`, `الأتمتة (automation)`, `تكلفة الخدمة (cost to serve)`. Aim for roughly one gloss every 4–6 Arabic words in technical text. Gloss whole phrases, never split a construct (`إدارة المنتج (product management)`, not `إدارة (management) المنتج`). A space always separates the Arabic word from `(`. Use the English exactly as the English lesson words it.
- Key phrases, slogans, labels and framework step names also get their English: `هل يجب أن نبنيه؟ (Should we build it?)`, `يكتمل عندما (Done when)`.
- If a gloss ends in punctuation (`?`, `.`, `!`), wrap it in a left-to-right isolate: `⁦(Should we build it?)⁩` (the characters U+2066 and U+2069), so it displays correctly in right-to-left text.
- Names of products, companies, books, frameworks and papers stay in their English form (Jobs to be Done, RICE, Kano, HEART, Opportunity Solution Tree, People + AI Guidebook, GitHub Copilot, Moffatt v. Air Canada). On first use in a unit you may add a short Arabic rendering before it: «شجرة الفرص والحلول (Opportunity Solution Tree)».
- People: Rania رانيا, Faisal فيصل, Hessa حصة, Tariq طارق, Dana دانة, Khalid خالد, Layla ليلى, Sara سارة, Yusuf يوسف, Omar عمر. Najm Bank → بنك نجم (Najm Bank). Products: Credit Memo Copilot → مساعد مذكرات الائتمان (Credit Memo Copilot); Najm Assist → نجم أسيست (Najm Assist); SME Instant Finance → التمويل الفوري للشركات الصغيرة (SME Instant Finance); Smart Alerts → التنبيهات الذكية (Smart Alerts); Staff GenAI → مساعد الموظفين التوليدي (Staff GenAI).

## Fixed terms
| English | Arabic |
|---|---|
| product manager (PM) / product management | مدير المنتج (PM) / إدارة المنتج |
| AI product | منتج ذكاء اصطناعي |
| discovery / delivery | الاكتشاف / التسليم |
| use case | حالة الاستخدام |
| job to be done | المهمة المطلوب إنجازها (job to be done) |
| opportunity | الفرصة |
| value / usability / feasibility / viability | القيمة / سهولة الاستخدام / الجدوى التقنية / الجدوى التجارية |
| prioritisation | تحديد الأولويات |
| roadmap | خارطة الطريق |
| requirements / spec / PRD | المتطلبات / المواصفات / وثيقة متطلبات المنتج (PRD) |
| acceptance criteria | معايير القبول |
| prototype / MVP | النموذج الأولي / الحد الأدنى من المنتج القابل للتطبيق (MVP) |
| evaluation (eval) / evals | التقييم (eval) / التقييمات (evals) |
| golden set | المجموعة المرجعية (golden set) |
| error analysis | تحليل الأخطاء |
| precision / recall | الدقة (precision) / الاستدعاء (recall) |
| false positive / false negative | إيجابي كاذب / سلبي كاذب |
| hallucination | الهلوسة |
| model / large language model (LLM) | النموذج / النموذج اللغوي الكبير (LLM) |
| prompt / context window | الموجّه (prompt) / نافذة السياق (context window) |
| token | الرمز (token) |
| retrieval-augmented generation (RAG) | التوليد المعزّز بالاسترجاع (RAG) |
| fine-tuning | الضبط الدقيق (fine-tuning) |
| agent / tool use | الوكيل (agent) / استخدام الأدوات (tool use) |
| human in the loop | الإنسان في الحلقة (human in the loop) |
| guardrails | الضوابط الوقائية (guardrails) |
| latency | زمن الاستجابة (latency) |
| cost to serve / unit economics | تكلفة الخدمة / اقتصاديات الوحدة (unit economics) |
| pricing model | نموذج التسعير |
| experiment / A/B test | التجربة / اختبار A/B |
| staged rollout | الإطلاق المرحلي (staged rollout) |
| launch / go-to-market | الإطلاق / الطرح في السوق (go-to-market) |
| adoption / retention | التبنّي / الاحتفاظ |
| North Star metric | مقياس نجم الشمال (North Star metric) |
| guardrail metric | مقياس وقائي (guardrail metric) |
| feedback loop / data flywheel | حلقة التغذية الراجعة / دولاب البيانات (data flywheel) |
| drift | الانجراف (drift) |
| trust / explainability | الثقة / قابلية التفسير |
| stakeholder | صاحب المصلحة |
| change management | إدارة التغيير |
| moat / defensibility | الخندق التنافسي (moat) / القابلية للدفاع |
| operating model | نموذج التشغيل |
| responsible AI | الذكاء الاصطناعي المسؤول |

## Structure the build depends on (do not break)
- Module heading: `# الوحدة N — العنوان` (N unchanged). Lesson heading: `# N.M — العنوان` (numbers unchanged).
- The line right after each lesson heading, translated exactly like this pattern:
  `*المستوى (Level): 🟡 متوسط (Intermediate)* · *المتطلبات (Prerequisites): 1.2، 2.1* · *المرحلة (Stage): Design*`
  (🟢 مبتدئ (Beginner) / 🟡 متوسط (Intermediate) / 🔴 متقدم (Advanced); keep the same emoji; keep lesson numbers; **stage names stay in English** exactly as in the English line, e.g. `Build, Evaluate`; separate lesson lists with «، »). If the English has no prerequisites, omit that part as the English does.
- Section headings keep their emoji first, translated: `## ⚡ الدرس في دقيقة (In 60 seconds)`, `## 🧭 لماذا يهم (Why it matters)`, `## 📐 كيف يعمل (How it works)`, `### 🟢 الأساسيات (The essentials)`, `### 🟡 التعمق أكثر (Going deeper)`, `### 🔴 نظرة الخبير (Expert view)`, `## 🧰 الأدوات (The toolkit)`, `## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)`, `## 🛠️ التمارين (Exercises)`, `## ⚠️ أخطاء وفخاخ (Mistakes and traps)`, `## 🧾 الخلاصة (Recap)`, `## ✍️ اختبر نفسك (Check yourself)`, `## 📚 المراجع (References)` (10.3: `## ✍️ الامتحان التدريبي (Practice exam)`). Same number of `#`/`##`/`###` headings in the same order as the English.
- **🧰 tables:** the first cell of every row must START with the same bold English tool name as the English row, exactly (e.g. `**RICE** (Intercom) — …`, `**Golden set**`). Translate everything after the bold name and the other cells. Header row: `| الأداة أو الإطار (Tool or framework) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |`.
- **Quizzes:** keep the question numbers; options stay labelled `- A.` `- B.` `- C.` `- D.` in Latin letters and in the same order; `<details><summary>الإجابة</summary>` then a blank line, then `**X.**` with the SAME correct letter as the English; letters cited in explanations stay the same Latin letters. Same number of questions and `<details>` blocks. In 10.3 keep the stage/lesson tag in English, e.g. `*(Evaluate · 6.1)*`.
- **Mermaid diagrams:** keep the syntax, the direction line (`flowchart LR`/`TD`) and node IDs exactly; translate only the label text into Arabic (no English in the labels, no parentheses inside labels). The build adds the English and flips the direction for Arabic afterwards.
- Keep unchanged: fenced code, inline `code`, URLs and link targets, numbers, `---` separators, tables' column counts.
- `*Done when:*` → `*يكتمل عندما (Done when):*`.

## Verify
Run: `python3 aipm/check_ar.py <english file> <arabic file>` until it prints ✓. It checks headings, the level/stage lines, section emoji order, 🧰 bold names, quiz letters, details blocks, mermaid blocks, code, links and that the text is really Arabic.
