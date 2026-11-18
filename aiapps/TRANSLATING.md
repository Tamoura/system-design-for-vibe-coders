# Arabic edition — translation guide (Building AI Applications & Agents: Zero to Hero)

Not published. Every translator follows this.

## Language and English terms
- Modern Standard Arabic, clear and professional, like a well-written university or professional training manual. Faithful: same meaning, structure, emphasis, lists, tables. Never summarise, add or drop content.
- **Gloss technical terms once per lesson.** Add the English in parentheses only after a real technical or business term, and only the first time that term appears in each lesson (a lesson runs from one `# N.M` heading to the next; the module intro counts as its own unit): `حلقة الوكيل (agent loop)`, `نافذة السياق (context window)`, `التوليد المعزَّز بالاسترجاع (retrieval-augmented generation, RAG)`, `الحواجز الوقائية (guardrails)`. Do not gloss plain words or phrases, do not repeat a gloss already given in the lesson, and never nest parentheses. Gloss whole phrases, never split a construct. A space always separates the Arabic word from `(`. Use the English exactly as the English lesson words it.
- Quiz and exam options get no new glosses of their own: a gloss makes an option longer and adds Latin letters, which can give the key away. Keep options as close as possible to the English in length and detail, and never add words the English does not have.
- Parentheses that hold formulas, numbers, option letters (`(A)` to `(D)`), citations (`Cemri et al.`, `Madaan et al., 2023`), standard identifiers (`LLM06:2025`, `RFC 8693`) or lesson pointers (`(الدرس 4.2)`) are content, not glosses: always keep them, exactly as in the English.
- If a gloss ends in punctuation (`?`, `.`, `!`), wrap it in a left-to-right isolate (the characters U+2066 before `(` and U+2069 after `)`), so it displays correctly in right-to-left text.
- Names of tools, products, standards, companies, platforms, programming languages and commands stay in their English form, in Latin letters and with no parentheses (Claude, Claude Code, Anthropic, MCP, Python, Pydantic, Chroma, ChromaDB, BM25, FastAPI, Docker, Kubernetes, GitHub Actions, OpenTelemetry, LangGraph, CrewAI, TicketHub, Najm ID, PeopleCore, DeviceDesk).
- People and fictional names are not glossed: Fahad فهد, Lujain لجين, Hind هند, Yara يارا, Layla ليلى, Noura نورة, Hamad حمد, Sara سارة, Maha مها, Salem سالم, Dana دانة, Tariq طارق, Rayan ريان; Najm Bank → بنك نجم; Najm Desk → نجم ديسك. IT Service Desk → مكتب خدمة تقنية المعلومات; Developer Enablement → فريق تمكين المطوّرين.
- Strings the lab code matches stay in English, for example the refusal sentence «⁦I don't know⁩».

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
| offline evaluation / online evaluation | التقييم خارج الإنتاج / التقييم في الإنتاج; an eval run on the lab mock is التقييم على المحاكي (never التقييم دون اتصال) |
| accuracy / precision / recall | الصحة الإجمالية (accuracy) / الدقة (precision) / الشمول (recall); recall@k → الشمول عند k (recall@k). استدعاء is used only for calls |
| mean reciprocal rank (MRR) / reciprocal rank fusion (RRF) | متوسط مقلوب الرتبة (MRR) / دمج مقلوب الرتب (RRF) |
| false positive / false negative | النتيجة الإيجابية الكاذبة (الإيجابيات الكاذبة) / النتيجة السلبية الكاذبة (السلبيات الكاذبة) |
| LLM-as-judge / trajectory | النموذج اللغوي حَكَمًا (LLM-as-judge) / مسار التنفيذ (trajectory) |
| regression test / CI gate | اختبار الانحدار (regression test) / بوابة التكامل المستمر (CI gate) |
| guardrails / prompt injection | الحواجز الوقائية (guardrails) / حقن الموجّه (prompt injection) |
| human-in-the-loop / approval / audit log | الإنسان في الحلقة (human-in-the-loop) / الموافقة (approval) / سجل التدقيق (audit log) |
| PII masking | إخفاء البيانات الشخصية (PII masking) |
| excessive agency | الصلاحيات المفرطة للوكيل (excessive agency) |
| governance / compliance / risk register | الحوكمة (governance) / الامتثال (compliance) / سجل المخاطر (risk register) |
| vendor / provider / vendor assessment | المورّد (vendor) / المزوّد (provider: model or cloud) / تقييم المورّد |
| organisation (the company or account) / enterprise | المنظمة / المؤسسات (enterprise customers or plan), المستوى المؤسسي (enterprise-grade) |
| middleware / proxy / reverse proxy | البرمجية الوسيطة / الخادم الوسيط / الخادم الوسيط العكسي (never bare الوسيط, never الوكيل) |
| TTL / capstone | مدة البقاء (TTL) / المشروع الختامي (capstone) |
| multi-tenancy / data residency | تعدد المستأجرين (multi-tenancy) / إقامة البيانات (data residency) |
| deployment / environment / rollback | النشر (deployment) / البيئة (environment) / التراجع (rollback) |
| container / queue / durable execution | الحاوية (container) / الطابور (queue) / التنفيذ المتين (durable execution) |
| idempotency / timeout / backoff | عدم التأثر بالتكرار (idempotency) / المهلة (timeout; expiry: انتهاء المهلة) / التأخير الأسي (backoff; exponential backoff: إعادة المحاولة بتأخير أسي) — never تراجع for backoff |
| deadline / wall-clock deadline | الموعد النهائي (deadline) / الموعد النهائي بالساعة الفعلية (wall-clock deadline) — never مهلة or أجل for deadline |
| guard (a loop or limit guard) / input, output guard | الحاجز (guard) / حارس المدخلات، حارس المخرجات (input / output guard) — guardrails are always الحواجز الوقائية, with الوقائية |
| jitter | الإزاحة العشوائية (jitter) |
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
  `*المستوى: 🟡 متوسط* · *المتطلبات: 1.1، 1.2* · *الطبقة: Applications, Agents*`
  (🟢 مبتدئ / 🟡 متوسط / 🔴 متقدم; keep the same emoji; keep lesson numbers; **layer names stay in English** exactly as in the English line; separate lesson lists with «، »). If the English has no prerequisites, omit that part as the English does.
- Section headings keep their emoji first, translated: `## ⚡ الدرس في دقيقة (In 60 seconds)`, `## 🧭 لماذا يهم (Why it matters)`, `## 📐 كيف يعمل (How it works)`, `### 🟢 الأساسيات (The essentials)`, `### 🟡 التعمق أكثر (Going deeper)`, `### 🔴 نظرة الخبير (Expert view)`, `## 🧰 الأدوات (The toolkit)`, `## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)`, `## 🛠️ التمارين (Exercises)`, `## ⚠️ أخطاء وفخاخ (Mistakes and traps)`, `## 🧾 الخلاصة (Recap)`, `## ✍️ اختبر نفسك (Check yourself)`, `## 📚 المراجع (References)` (16.2: `## ✍️ الامتحان التدريبي (Practice exam)`). Same number of `#`/`##`/`###` headings in the same order as the English.
- **🧰 tables:** the first cell of every row must START with the same bold English name as the English row, exactly (e.g. `**Tool use loop** — …`, `**Prompt caching** — …`). Translate everything after the bold name and the other cells. Header row: `| الأداة أو الممارسة أو النمط (Tool, practice or pattern) | ما هي وماذا تفعل (What it is and does) | متى تلجأ إليها (When to reach for it) |`.
- **Quizzes:** keep the question numbers; options stay labelled `- A.` `- B.` `- C.` `- D.` in Latin letters and in the same order; `<details><summary>الإجابة</summary>` then a blank line, then `**X.**` with the SAME correct letter as the English; letters cited in explanations stay the same Latin letters. Same number of questions and `<details>` blocks. In 16.2 keep the layer/lesson tag in English, e.g. `*(Agents · 8.2)*`.
- **Code blocks stay byte-identical** (code, YAML, shell, config, Gherkin). Comments and string literals inside code stay in English.
- **Mermaid diagrams:** keep the syntax and node IDs exactly. Where the English runs left to right (`flowchart LR`, `direction LR`), the Arabic runs right to left (`flowchart RL`, `direction RL`); top-down diagrams stay top-down. Labels are Arabic first, then the English on a new line: `["المحاكي<br/>(Mock)"]`. Edge labels follow the same pattern.
- **Links:** keep external URLs unchanged. Relative links to other courses in the library point to their Arabic pages: `index.html` → `index.ar.html`, `index.en.html` → `index.ar.html`, `learning-path.html` → `learning-path.ar.html`, `assessment.html` → `assessment.ar.html` (keep the `#…` part). Translate the link text.
- Keep unchanged: inline `code`, numbers, `---` separators, tables' column counts.
- `*Done when:*` → `*يكتمل عندما:*`.

## Verify
Run `python3 aiapps/check_ar.py <english file> <arabic file>` for each changed lesson until it prints ✓, then `python3 scripts/qa/ar_parity.py --list` (formula parts, option letters and citations) and `python3 scripts/qa/quiz_cues.py` (option length and Latin-letter cues). It checks headings, the level/phase lines, section emoji order, 🧰 bold names, quiz letters, details blocks, code and mermaid blocks, links and that the text is really Arabic.
