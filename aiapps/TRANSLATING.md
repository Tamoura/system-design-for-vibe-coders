# Arabic edition — translation guide (Building AI Applications & Agents: Zero to Hero)

Not published. Every translator follows this.

## Language and English terms
- Modern Standard Arabic, clear and professional, like a well-written university or professional training manual. Faithful: same meaning, structure, emphasis, lists, tables. Never summarise, add or drop content.
- **English beside every technical term everywhere.** In every paragraph, list item, table cell, heading, quiz question, option and answer, each technical term and key phrase carries its English in parentheses on its first appearance in that unit (a unit = one paragraph, one list item, one table cell, one heading): `حلقة الوكيل (agent loop)`, `نافذة السياق (context window)`, `استخدام الأدوات (tool use)`, `التوليد المعزَّز بالاسترجاع (retrieval-augmented generation, RAG)`, `الحواجز الوقائية (guardrails)`. Aim for roughly one gloss every 4–6 Arabic words in technical text. Gloss whole phrases, never split a construct. A space always separates the Arabic word from `(`. Use the English exactly as the English lesson words it.
- Key phrases, rules of thumb, labels and framework step names also get their English, e.g. `يكتمل عندما (Done when)`.
- If a gloss ends in punctuation (`?`, `.`, `!`), wrap it in a left-to-right isolate (the characters U+2066 before `(` and U+2069 after `)`), so it displays correctly in right-to-left text.
- Names of tools, products, standards, companies, platforms, programming languages and commands stay in their English form (Claude, Claude Code, Anthropic, MCP, Python, Pydantic, Chroma, ChromaDB, BM25, FastAPI, Docker, Kubernetes, GitHub Actions, OpenTelemetry, LangGraph, CrewAI, TicketHub, Najm ID, PeopleCore, DeviceDesk). On first use in a unit you may add a short Arabic rendering before it.
- People: Fahad فهد, Lujain لجين, Hind هند, Yara يارا, Layla ليلى, Noura نورة, Hamad حمد, Sara سارة, Maha مها, Salem سالم, Dana دانة, Tariq طارق. Najm Bank → بنك نجم (Najm Bank). Najm Desk → نجم ديسك (Najm Desk); IT Service Desk → مكتب خدمة تقنية المعلومات (IT Service Desk); Developer Enablement → فريق تمكين المطوّرين (Developer Enablement).

## Fixed terms
| English | Arabic |
|---|---|
| large language model (LLM) | النموذج اللغوي الكبير (LLM) |
| token / context window | الرمز (token) / نافذة السياق (context window) |
| prompt / system prompt | الموجّه (prompt) / موجّه النظام (system prompt) |
| message / messages list | الرسالة (message) / قائمة الرسائل (messages list) |
| stateless | عديم الحالة (stateless) |
| agent / agent loop | الوكيل (agent) / حلقة الوكيل (agent loop) |
| tool / tool use / tool call / tool result | الأداة (tool) / استخدام الأدوات (tool use) / استدعاء الأداة (tool call) / نتيجة الأداة (tool result) |
| structured output / schema | المخرجات المهيكلة (structured output) / المخطط (schema) |
| validation / retry | التحقق من الصحة (validation) / إعادة المحاولة (retry) |
| retrieval-augmented generation (RAG) | التوليد المعزَّز بالاسترجاع (retrieval-augmented generation, RAG) |
| embedding / chunking / vector store | التضمين (embedding) / التقطيع (chunking) / مخزن المتجهات (vector store) |
| hybrid search / reranking / citation | البحث الهجين (hybrid search) / إعادة الترتيب (reranking) / الاستشهاد (citation) |
| workflow / prompt chaining / routing / parallelisation | سير العمل (workflow) / تسلسل الموجّهات (prompt chaining) / التوجيه الشرطي (routing) / التوازي (parallelisation) |
| reflection / planning | التأمل الذاتي (reflection) / التخطيط (planning) |
| stopping condition / iteration cap | شرط التوقف (stopping condition) / حدّ التكرارات (iteration cap) |
| memory (short-term / working / long-term) | الذاكرة (قصيرة المدى / العاملة / طويلة المدى) (short-term / working / long-term memory) |
| Model Context Protocol (MCP) | بروتوكول سياق النموذج (Model Context Protocol, MCP) |
| server / resource / transport | الخادم (server) / المورد (resource) / وسيلة النقل (transport) |
| least privilege / authorisation | أقل الصلاحيات (least privilege) / التفويض (authorisation) |
| multi-agent / supervisor / worker / hand-off | تعدد الوكلاء (multi-agent) / المشرف (supervisor) / العامل (worker) / التسليم بين الوكلاء (hand-off) |
| evaluation / eval set / grader | التقييم (evaluation) / مجموعة التقييم (eval set) / المقيِّم (grader) |
| LLM-as-judge / trajectory | النموذج اللغوي حَكَمًا (LLM-as-judge) / مسار التنفيذ (trajectory) |
| regression test / CI gate | اختبار الانحدار (regression test) / بوابة التكامل المستمر (CI gate) |
| guardrails / prompt injection | الحواجز الوقائية (guardrails) / حقن الموجّه (prompt injection) |
| human-in-the-loop / approval / audit log | الإنسان في الحلقة (human-in-the-loop) / الموافقة (approval) / سجل التدقيق (audit log) |
| PII masking | إخفاء البيانات الشخصية (PII masking) |
| excessive agency | الصلاحيات المفرطة للوكيل (excessive agency) |
| governance / compliance / risk register | الحوكمة (governance) / الامتثال (compliance) / سجل المخاطر (risk register) |
| multi-tenancy / data residency | تعدد المستأجرين (multi-tenancy) / إقامة البيانات (data residency) |
| deployment / environment / rollback | النشر (deployment) / البيئة (environment) / التراجع (rollback) |
| container / queue / durable execution | الحاوية (container) / الطابور (queue) / التنفيذ المتين (durable execution) |
| idempotency / timeout / backoff | عدم التأثر بالتكرار (idempotency) / المهلة (timeout) / التراجع الأسي (backoff) |
| canary release / feature flag | الإطلاق الكناري (canary release) / مفتاح الميزة (feature flag) |
| prompt caching / batch API / model routing | التخزين المؤقت للموجّه (prompt caching) / واجهة الدُّفعات (batch API) / توجيه النماذج (model routing) |
| cost per request / budget | التكلفة لكل طلب (cost per request) / الميزانية (budget) |
| observability / trace / SLO | قابلية المراقبة (observability) / التتبّع (trace) / هدف مستوى الخدمة (SLO) |
| incident / runbook / postmortem | الحادثة (incident) / دليل التشغيل (runbook) / مراجعة ما بعد الحادثة (postmortem) |
| discovery / stakeholder / requirements | الاستكشاف (discovery) / صاحب المصلحة (stakeholder) / المتطلبات (requirements) |
| acceptance criteria / user story | معايير القبول (acceptance criteria) / قصة المستخدم (user story) |
| agent brief / agent specification | موجز الوكيل (agent brief) / مواصفات الوكيل (agent specification) |
| autonomy level | مستوى الاستقلالية (autonomy level) |
| architecture decision record (ADR) | سجل القرار المعماري (architecture decision record, ADR) |
| prototype / proof of concept / pilot | النموذج الأولي (prototype) / إثبات المفهوم (proof of concept) / التجربة التشغيلية (pilot) |
| statement of work (SOW) / scope / change control | بيان العمل (statement of work, SOW) / النطاق (scope) / ضبط التغيير (change control) |
| handover / adoption / change management | التسليم (handover) / التبنّي (adoption) / إدارة التغيير (change management) |
| coding agent / Claude Code | وكيل البرمجة (coding agent) / Claude Code |
| spec / plan / verify | المواصفة (spec) / الخطة (plan) / التحقق (verify) |

## Structure the build depends on (do not break)
- Module heading: `# الوحدة N — العنوان` (N unchanged). Lesson heading: `# N.M — العنوان` (numbers unchanged).
- The line right after each lesson heading, translated exactly like this pattern:
  `*المستوى (Level): 🟡 متوسط (Intermediate)* · *المتطلبات (Prerequisites): 1.1، 1.2* · *الطبقة (Layer): Applications, Agents*`
  (🟢 مبتدئ (Beginner) / 🟡 متوسط (Intermediate) / 🔴 متقدم (Advanced); keep the same emoji; keep lesson numbers; **layer names stay in English** exactly as in the English line; separate lesson lists with «، »). If the English has no prerequisites, omit that part as the English does.
- Section headings keep their emoji first, translated: `## ⚡ الدرس في دقيقة (In 60 seconds)`, `## 🧭 لماذا يهم (Why it matters)`, `## 📐 كيف يعمل (How it works)`, `### 🟢 الأساسيات (The essentials)`, `### 🟡 التعمق أكثر (Going deeper)`, `### 🔴 نظرة الخبير (Expert view)`, `## 🧰 الأدوات (The toolkit)`, `## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)`, `## 🛠️ التمارين (Exercises)`, `## ⚠️ أخطاء وفخاخ (Mistakes and traps)`, `## 🧾 الخلاصة (Recap)`, `## ✍️ اختبر نفسك (Check yourself)`, `## 📚 المراجع (References)` (16.2: `## ✍️ الامتحان التدريبي (Practice exam)`). Same number of `#`/`##`/`###` headings in the same order as the English.
- **🧰 tables:** the first cell of every row must START with the same bold English name as the English row, exactly (e.g. `**Tool use loop** — …`, `**Prompt caching** — …`). Translate everything after the bold name and the other cells. Header row: `| الأداة أو الممارسة أو النمط (Tool, practice or pattern) | ما هي وماذا تفعل (What it is and does) | متى تلجأ إليها (When to reach for it) |`.
- **Quizzes:** keep the question numbers; options stay labelled `- A.` `- B.` `- C.` `- D.` in Latin letters and in the same order; `<details><summary>الإجابة</summary>` then a blank line, then `**X.**` with the SAME correct letter as the English; letters cited in explanations stay the same Latin letters. Same number of questions and `<details>` blocks. In 16.2 keep the layer/lesson tag in English, e.g. `*(Agents · 8.2)*`.
- **Code blocks stay byte-identical** (code, YAML, shell, config, Gherkin). Comments and string literals inside code stay in English.
- **Mermaid diagrams:** keep the syntax, the direction line and node IDs exactly; translate only the label text into Arabic (no English in the labels, no parentheses inside labels). The build adds the English and flips the direction for Arabic afterwards.
- **Links:** keep external URLs unchanged. Relative links to other courses in the library point to their Arabic pages: `index.html` → `index.ar.html`, `index.en.html` → `index.ar.html`, `learning-path.html` → `learning-path.ar.html`, `assessment.html` → `assessment.ar.html` (keep the `#…` part). Translate the link text.
- Keep unchanged: inline `code`, numbers, `---` separators, tables' column counts.
- `*Done when:*` → `*يكتمل عندما (Done when):*`.

## Verify
Run: `python3 testing/check_ar.py <english file> <arabic file>` until it prints ✓. It checks headings, the level/phase lines, section emoji order, 🧰 bold names, quiz letters, details blocks, code and mermaid blocks, links and that the text is really Arabic.
