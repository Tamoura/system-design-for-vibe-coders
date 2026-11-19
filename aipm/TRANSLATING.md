# Arabic edition — translation guide (AI Product Management: Zero to Hero)

Not published. Every translator follows this.

## Language and English terms
- Modern Standard Arabic, clear and professional, like a well-written bank or technology training manual. Faithful: same meaning, structure, emphasis, lists, tables. Never summarise, add or drop content.
- **Gloss rule (one English gloss per term per lesson).** Add the English in parentheses only after a real technical or business term, and only the first time that term appears in each lesson: `الاكتشاف (discovery)`, `حالة الاستخدام (use case)`, `المجموعة المرجعية (golden set)`. Do not gloss plain words or plain phrases, do not repeat a gloss already given in the lesson, and never nest parentheses (write `نتيجة إيجابية كاذبة (FP)`, not `(False positive (FP))`). Keep product, standard and acronym names in Latin letters with no parentheses (GDPR, RAG, PM). Parentheses that hold formulas, numbers, option letters or section pointers, such as `TP ÷ (TP + FP)`, `(A)` or `(6.1)`, are content, not glosses: they always stay, exactly as in the English. Gloss whole phrases, never split a construct, and keep a space between the Arabic word and `(`.
- If a gloss ends in punctuation (`?`, `.`, `!`), wrap it in a left-to-right isolate (the characters U+2066 and U+2069) so it displays correctly in right-to-left text.
- Quiz and exam options say what the English option says, at about the same length and level of detail. Do not pad or trim one option, so the key is never findable by length or wording.
- Names of products, companies, books, frameworks and papers stay in their English form (Jobs to be Done, RICE, Kano, HEART, Opportunity Solution Tree, People + AI Guidebook, GitHub Copilot, Moffatt v. Air Canada). On first use in a lesson you may add a short Arabic rendering before it: «شجرة الفرص والحلول (Opportunity Solution Tree)».
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
| accuracy (the metric) | الصحة الإجمالية (never الدقة, never bare الصحة) |
| precision / recall | الدقة (precision) / الشمول (recall); recall@k = الشمول عند k |
| false positive / false negative | النتيجة الإيجابية الكاذبة / النتيجة السلبية الكاذبة (plural: الإيجابيات الكاذبة / السلبيات الكاذبة) |
| false alarm | إنذار كاذب (only where the English says false alarm) |
| tool call / API call | استدعاء الأداة / استدعاء الواجهة (استدعاء is used only for calls) |
| offline evaluation / online evaluation | التقييم خارج الإنتاج / التقييم في الإنتاج |
| pilot | التجربة التشغيلية |
| vendor / provider | المورّد / المزوّد; vendor lock-in = الارتباط بمورّد واحد |
| enterprise (customer segment or plan) | المؤسسات (عملاء المؤسسات) |
| deadline / timeout | الموعد النهائي / المهلة |
| capstone | المشروع الختامي |
| postmortem | مراجعة ما بعد الحادثة |
| TTL | مدة البقاء (TTL) |
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
  `*المستوى: 🟡 متوسط* · *المتطلبات: 1.2، 2.1* · *المرحلة: Design*`
  (🟢 مبتدئ / 🟡 متوسط / 🔴 متقدم; keep the same emoji; keep lesson numbers; **stage names stay in English** exactly as in the English line, e.g. `Build, Evaluate`; separate lesson lists with «، »). If the English has no prerequisites, omit that part as the English does.
- Section headings keep their emoji first, translated: `## ⚡ الدرس في دقيقة`, `## 🧭 لماذا يهم`, `## 📐 كيف يعمل`, `### 🟢 الأساسيات`, `### 🟡 التعمق أكثر`, `### 🔴 نظرة الخبير`, `## 🧰 الأدوات`, `## 🏛️ عمليًا في بنك نجم`, `## 🛠️ التمارين`, `## ⚠️ أخطاء وفخاخ`, `## 🧾 الخلاصة`, `## ✍️ اختبر نفسك`, `## 📚 المراجع` (10.3: `## ✍️ الامتحان التدريبي`). Headings carry no English gloss. Same number of `#`/`##`/`###` headings in the same order as the English.
- **🧰 tables:** the first cell of every row must START with the same bold English tool name as the English row, exactly (e.g. `**RICE** (Intercom) — …`, `**Golden set**`). Translate everything after the bold name and the other cells. Header row: `| الأداة أو الإطار | ما هو وماذا يفعل | متى تلجأ إليه |`.
- **Quizzes:** keep the question numbers; options stay labelled `- A.` `- B.` `- C.` `- D.` in Latin letters and in the same order; `<details><summary>الإجابة</summary>` then a blank line, then `**X.**` with the SAME correct letter as the English; letters cited in explanations stay the same Latin letters. Same number of questions and `<details>` blocks. In 10.3 keep the stage/lesson tag in English, e.g. `*(Evaluate · 6.1)*`.
- **Mermaid diagrams:** keep the syntax and node IDs exactly; translate only the label text into Arabic (no English in the labels, no parentheses inside labels). In the Arabic file a left-to-right diagram runs right to left: `flowchart LR` becomes `flowchart RL` and `direction LR` becomes `direction RL`.
- Keep unchanged: fenced code, inline `code`, URLs and link targets, numbers, `---` separators, tables' column counts.
- `*Done when:*` → `*يكتمل عندما:*`.

## Verify
Run: `python3 aipm/check_ar.py <english file> <arabic file>` until it prints ✓. It checks headings, the level/stage lines, section emoji order, 🧰 bold names, quiz letters, details blocks, mermaid blocks, code, links and that the text is really Arabic.
