# Arabic edition — translation guide (A Practical Guide to Becoming an AI-Native Engineer)

Not published. Every translator follows this.

## Language and English terms
- Modern Standard Arabic, clear and professional, like a well-written university or professional training manual. Faithful: same meaning, structure, emphasis, lists, tables. Never summarise, add or drop content.
- **English glosses: technical terms only, once per lesson.** The first time a real technical or business term appears in a lesson, it carries its English in parentheses: `حلقة الوكيل (agent loop)`, `نافذة السياق (context window)`, `الحواجز الوقائية (guardrails)`. Do not gloss plain words or phrases, do not repeat a gloss already given in the lesson, never nest parentheses, and do not gloss headings. Product, standard and acronym names stay in Latin letters with no parentheses. Parentheses that hold formulas, numbers, option letters or section pointers are content, not glosses, and always stay. Gloss whole phrases, never split a construct; a space separates the Arabic word from `(`; use the English exactly as the English lesson words it. The checker `python3 scripts/qa/arabic_rules.py` enforces a floor and a ceiling on gloss density per lesson: see [scripts/qa/README.md](../scripts/qa/README.md).
- Rules of thumb and labels such as `يكتمل عندما` (Done when) are plain phrases and carry no gloss; a named framework step that is a real term is glossed once, where the lesson first names it.
- If a gloss ends in punctuation (`?`, `.`, `!`), wrap it in a left-to-right isolate (the characters U+2066 before `(` and U+2069 after `)`), so it displays correctly in right-to-left text.
- Names of tools, products, standards, companies, platforms, programming languages, commands, file names and kit commands stay in their English form (Claude, Claude Code, Anthropic, MCP, Git, GitHub, GitHub Actions, Python, pytest, CLAUDE.md, AGENTS.md, settings.json, SKILL.md, ailab, najmkit, Cursor, GitHub Copilot, Codex CLI, Gemini CLI, Aider, OWASP, DORA). On first use in a unit you may add a short Arabic rendering before it.
- People: Tariq طارق, Lujain لجين, Hessa حصة, Nada ندى, Noura نورة, Maha مها, Layla ليلى, Hamad حمد, Sara سارة, Salem سالم. Najm Bank → بنك نجم. Najm Remit → نجم ريميت; Payments Platform → منصة المدفوعات. These fictional names are not glossed.

## Fixed terms
| English | Arabic |
|---|---|
| AI-native engineer | المهندس الأصيل في الذكاء الاصطناعي (AI-native engineer) |
| coding agent / agentic coding | وكيل البرمجة (coding agent) / البرمجة الوكيلية (agentic coding) |
| large language model (LLM) | النموذج اللغوي الكبير (LLM) |
| agent / agent loop | الوكيل (agent) / حلقة الوكيل (agent loop) |
| tool / tool call | الأداة (tool) / استدعاء الأداة (tool call) |
| token / context window | الرمز (token) / نافذة السياق (context window) |
| turn (one model reply in the agent loop; `--max-turns`) | الدور، والجمع الأدوار (turns); gloss once per lesson; never use it for job roles in an agent passage |
| context / context engineering | السياق (context) / هندسة السياق (context engineering) |
| project memory | ذاكرة المشروع (project memory) |
| prompt | الموجّه (prompt) |
| hallucination / sycophancy / context rot | الهلوسة (hallucination) / المجاملة المفرطة (sycophancy) / تدهور السياق (context rot) |
| spec / spec-driven development | المواصفة (spec) / التطوير الموجَّه بالمواصفات (spec-driven development) |
| ticket | التذكرة (ticket) |
| acceptance criteria / non-goals / constraint | معايير القبول (acceptance criteria) / ما ليس من الأهداف (non-goals) / القيد (constraint) |
| plan / plan mode | الخطة (plan) / وضع التخطيط (plan mode) |
| specify / delegate / verify / integrate | حدِّد (specify) / فوِّض (delegate) / تحقّق (verify) / ادمج (integrate) |
| the daily loop | الحلقة اليومية (the daily loop) |
| verification / evidence / fluency | التحقق (verification) / الدليل (evidence) / الطلاقة (fluency) |
| test / unit test / regression test | الاختبار (test) / اختبار الوحدة (unit test) / اختبار الانحدار (regression test) |
| test-driven development (TDD) | التطوير الموجَّه بالاختبارات (test-driven development, TDD) |
| mutation testing / property-based testing | اختبار الطفرات (mutation testing) / الاختبار القائم على الخصائص (property-based testing) |
| characterization test | اختبار التوصيف (characterization test) |
| code review / diff / commit | مراجعة الشيفرة (code review) / الفروقات (diff) / الإيداع (commit) |
| branch / pull request / merge / merge conflict | الفرع (branch) / طلب الدمج (pull request) / الدمج (merge) / تعارض الدمج (merge conflict) |
| worktree | شجرة العمل (worktree) |
| checkpoint / rewind | نقطة الاستعادة (checkpoint) / الرجوع (rewind) |
| debugging / root cause / reproduce | تصحيح الأخطاء (debugging) / السبب الجذري (root cause) / إعادة الإنتاج (reproduce) |
| legacy code / refactoring / migration | الشيفرة الموروثة (legacy code) / إعادة الهيكلة (refactoring) / الترحيل (migration) |
| seam / strangler fig | نقطة الفصل (seam) / نمط التينة الخانقة (strangler fig) |
| technical debt | الدين التقني (technical debt) |
| prompt injection / lethal trifecta | حقن الموجّه (prompt injection) / الثالوث القاتل (lethal trifecta) |
| excessive agency | الصلاحيات المفرطة للوكيل (excessive agency) |
| least privilege / sandbox | أقل الصلاحيات (least privilege) / البيئة المعزولة (sandbox) |
| permission / allow-list / deny rule | الصلاحية (permission) / قائمة السماح (allow-list) / قاعدة المنع (deny rule) |
| secret / secrets scanning | السر (secret) / فحص الأسرار (secrets scanning) |
| supply chain / dependency / lockfile | سلسلة التوريد (supply chain) / الاعتمادية (dependency) / ملف القفل (lockfile) |
| hallucinated package / slopsquatting | الحزمة المُهلوَسة (hallucinated package) / السطو على الأسماء المُهلوَسة (slopsquatting) |
| hook / guard hook | الخطاف (hook) / خطاف الحماية (guard hook) |
| slash command / skill / subagent | الأمر المائل (slash command) / المهارة (skill) / الوكيل الفرعي (subagent) |
| Model Context Protocol (MCP) | بروتوكول سياق النموذج (Model Context Protocol, MCP) |
| headless mode | الوضع غير التفاعلي (headless mode) |
| CI / CI pipeline | التكامل المستمر (CI) / خط التكامل المستمر (CI pipeline) |
| parallel agents / orchestrator / worker | الوكلاء المتوازون (parallel agents) / المنسّق (orchestrator) / العامل (worker) |
| architecture decision record (ADR) | سجل القرار المعماري (architecture decision record, ADR) |
| incident / postmortem | الحادثة (incident) / مراجعة ما بعد الحادثة (postmortem) |
| playbook | الدليل العملي (playbook) |
| DORA metrics / lead time / change failure rate | مقاييس DORA / زمن التسليم (lead time) / معدل فشل التغيير (change failure rate) |
| guard metric / vanity metric | مقياس الحماية (guard metric) / مقياس شكلي (vanity metric) |
| deskilling / deliberate practice | تآكل المهارة (deskilling) / الممارسة المقصودة (deliberate practice) |
| eval / personal eval | التقييم (eval) / تقييمك الشخصي (personal eval) |
| governance / policy / accountability | الحوكمة (governance) / السياسة (policy) / المساءلة (accountability) |
| capstone | المشروع الختامي (capstone) |
| lab / grader / hidden tests | المختبر (lab) / المُقيِّم (grader) / الاختبارات الخفية (hidden tests) |
| agent log | سجل الوكيل (agent log) |
| pin (a version) / install | يقيّد الإصدار (pin) / يُنصِّب (install) |
| rotate (a secret) / access token | يدوّر السر (rotate) / رمز الوصول (access token) |
| shell | الصدفة (shell) |
| compile | التصريف (compile): «تُصرَّف الشيفرة», never «تُترجَم» |
| prune (a memory file) | التقليم (prune) |

### Library terms (shared with every course)
Use these forms; the words in the last column are not used for these meanings.

| English | Arabic | Avoid |
|---|---|---|
| accuracy / precision / recall | الصحة الإجمالية / الدقة / الشمول (recall@k: الشمول عند k) | الدقة for accuracy; الضبط; الاستدعاء for recall |
| tool call | استدعاء الأداة (plural: استدعاءات الأدوات) | الاستدعاء alone as a metric |
| organization (tenant) / enterprise | المنظمة / المؤسسات | المؤسسة for organization |
| deadline / timeout | الموعد النهائي / المهلة (انتهاء المهلة) | المهلة for deadline; أجل |
| middleware / proxy / reverse proxy | البرمجية الوسيطة / الخادم الوسيط / الخادم الوسيط العكسي | bare الوسيط; الوكيل for proxy |
| backoff / rollback | التأخير الأسي (إعادة المحاولة بتأخير أسي) / التراجع | التراجع الأسي |
| capstone / pilot | المشروع الختامي / التجربة التشغيلية | مشروع التخرّج; التجربة الأولية |
| vendor / provider | المورّد / المزوّد | المزوّد for vendor; البائع |
| total compensation | إجمالي التعويضات | إجمالي المكافآت |
| TTL | مدة البقاء (TTL) | أجل البقاء; مدة الصلاحية |
| postmortem | مراجعة ما بعد الحادثة (the document: تقرير مراجعة ما بعد الحادثة) | تشريح الحادثة |
| offline / online evaluation | التقييم خارج الإنتاج / التقييم في الإنتاج | التقييم دون اتصال |
| false positive / false negative | النتيجة الإيجابية الكاذبة / النتيجة السلبية الكاذبة (plurals: الإيجابيات / السلبيات الكاذبة) | إنذار كاذب; إيجابي كاذب |

## Structure the build depends on (do not break)
- Module heading: `# الوحدة N — العنوان` (N unchanged). Lesson heading: `# N.M — العنوان` (numbers unchanged).
- The line right after each lesson heading, translated exactly like this pattern:
  `*المستوى: 🟡 متوسط* · *المتطلبات: 1.1، 1.2* · *التركيز: Workflow, Verify*`
  (🟢 مبتدئ / 🟡 متوسط / 🔴 متقدم, with no English glosses on this line; keep the same emoji; keep lesson numbers; **focus names stay in English** exactly as in the English line; separate lesson lists with «، »). If the English has no prerequisites, omit that part as the English does.
- Section headings keep their emoji first, translated (the English below is for reference only; headings carry no gloss): `## ⚡ الدرس في دقيقة` (In 60 seconds), `## 🧭 لماذا يهم` (Why it matters), `## 📐 كيف يعمل` (How it works), `### 🟢 الأساسيات` (The essentials), `### 🟡 التعمق أكثر` (Going deeper), `### 🔴 نظرة الخبير` (Expert view), `## 🧰 الأدوات` (The toolkit), `## 🏛️ عمليًا في بنك نجم` (In practice at Najm Bank), `## 🛠️ التمارين` (Exercises), `## ⚠️ أخطاء وفخاخ` (Mistakes and traps), `## 🧾 الخلاصة` (Recap), `## ✍️ اختبر نفسك` (Check yourself), `## 📚 المراجع` (References) (14.2: `## ✍️ الامتحان التدريبي`, Practice exam). Same number of `#`/`##`/`###` headings in the same order as the English.
- **🧰 tables:** the first cell of every row must START with the same bold English name as the English row, exactly (e.g. `**Tool use loop** — …`, `**Prompt caching** — …`). Translate everything after the bold name and the other cells. Header row: `| الأداة أو الممارسة أو النمط (Tool, practice or pattern) | ما هي وماذا تفعل (What it is and does) | متى تلجأ إليها (When to reach for it) |`.
- **Quizzes:** keep the question numbers; options stay labelled `- A.` `- B.` `- C.` `- D.` in Latin letters and in the same order; `<details><summary>الإجابة</summary>` then a blank line, then `**X.**` with the SAME correct letter as the English; letters cited in explanations stay the same Latin letters. Same number of questions and `<details>` blocks. In 14.2 keep the focus/lesson tag in English, e.g. `*(Verify · 5.2)*`.
- **Code blocks stay byte-identical** (code, YAML, shell, config, Gherkin). Comments and string literals inside code stay in English.
- **Mermaid diagrams:** keep the syntax and node IDs exactly and the same number of lines; `flowchart LR` / `direction LR` becomes `RL` in the Arabic file (`scripts/qa/arabic_rules.py` checks this). Labels are bilingual, the convention every lesson uses: the Arabic label, then `<br/>` and the English label in parentheses, e.g. `A["موجّه النظام<br/>(System prompt)"]`. These are the only parentheses inside a label.
- **Links:** keep external URLs unchanged. Relative links to other courses in the library point to their Arabic pages: `index.html` → `index.ar.html`, `index.en.html` → `index.ar.html`, `learning-path.html` → `learning-path.ar.html`, `assessment.html` → `assessment.ar.html` (keep the `#…` part). Translate the link text.
- Keep unchanged: inline `code`, numbers, `---` separators, tables' column counts.
- `*Done when:*` → `*يكتمل عندما:*`.

## Verify
Run: `python3 ainative/check_ar.py <english file> <arabic file>` until it prints ✓. It checks headings, the level/focus lines, section emoji order, 🧰 bold names, quiz letters, details blocks, code and mermaid blocks, links and that the text is really Arabic.
