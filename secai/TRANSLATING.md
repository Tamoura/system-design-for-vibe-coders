# Arabic edition — translation guide (Secure AI & Application Security: Zero to Hero)

Not published. Every translator follows this.

## Language and English terms
- Modern Standard Arabic, clear and professional, like a well-written bank or national-CERT training manual. Faithful: same meaning, structure, emphasis, lists, tables. Never summarise, add or drop content.
- **English beside every technical term everywhere.** In every paragraph, list item, table cell, heading, quiz question, option and answer, each technical term and key phrase carries its English in parentheses on its first appearance in that unit (a unit = one paragraph, one list item, one table cell, one heading): `حقن SQL (SQL injection)`, `نمذجة التهديدات (threat modelling)`, `أقل الصلاحيات (least privilege)`, `حقن الموجّهات (prompt injection)`, `الصلاحيات المفرطة (excessive agency)`. Aim for roughly one gloss every 4–6 Arabic words in technical text. Gloss whole phrases, never split a construct (`التحكم في الوصول (access control)`, not `التحكم (control) في الوصول`). A space always separates the Arabic word from `(`. Use the English exactly as the English lesson words it.
- Key phrases, rules of thumb, labels and framework step names also get their English: `لا تثق أبدًا بمخرجات النموذج (never trust model output)`, `يكتمل عندما (Done when)`.
- If a gloss ends in punctuation (`?`, `.`, `!`), wrap it in a left-to-right isolate (the characters U+2066 before `(` and U+2069 after `)`), so it displays correctly in right-to-left text.
- Names of standards, frameworks, tools, products, CVEs and cases stay in their English form (OWASP Top 10, OWASP ASVS, MITRE ATT&CK, MITRE ATLAS, STRIDE, CVSS, NIST CSF 2.0, ISO/IEC 27001, SLSA, Semgrep, Log4Shell, CVE-2021-44228, Moffatt v. Air Canada). On first use in a unit you may add a short Arabic rendering before it.
- People: Noura نورة, Ali علي, Mariam مريم, Jassim جاسم, Tariq طارق, Dana دانة, Rania رانيا, Layla ليلى, Sara سارة, Hamad حمد. Najm Bank → بنك نجم (Najm Bank). Systems: Najm Mobile → تطبيق نجم للهاتف (Najm Mobile); Najm Assist → نجم أسيست (Najm Assist); Credit Memo Copilot → مساعد مذكرات الائتمان (Credit Memo Copilot); SME Portal → بوابة الشركات الصغيرة (SME Portal); Smart Alerts → التنبيهات الذكية (Smart Alerts).

## Fixed terms
| English | Arabic |
|---|---|
| application security (AppSec) | أمن التطبيقات (AppSec) |
| AI security | أمن الذكاء الاصطناعي |
| attacker / defender | المهاجم / المدافع |
| asset / threat / vulnerability / risk | الأصل / التهديد / الثغرة / المخاطر |
| attack surface | سطح الهجوم |
| trust boundary | حدّ الثقة |
| threat model(ling) | نموذج التهديدات / نمذجة التهديدات |
| least privilege | أقل الصلاحيات |
| defence in depth | الدفاع المتعدد الطبقات (defence in depth) |
| secure by default | آمن افتراضيًا (secure by default) |
| zero trust | انعدام الثقة (zero trust) |
| authentication / authorisation | المصادقة / التفويض |
| access control | التحكم في الوصول |
| multi-factor authentication (MFA) | المصادقة متعددة العوامل (MFA) |
| session / token | الجلسة / الرمز المميز (token) |
| injection | الحقن |
| cross-site scripting (XSS) | البرمجة النصية عبر المواقع (XSS) |
| cross-site request forgery (CSRF) | تزوير الطلبات عبر المواقع (CSRF) |
| server-side request forgery (SSRF) | تزوير الطلبات من جهة الخادم (SSRF) |
| encryption / hashing / key | التشفير / التجزئة (hashing) / المفتاح |
| secret | السرّ |
| dependency / supply chain | الاعتمادية / سلسلة التوريد |
| misconfiguration | سوء الإعداد (misconfiguration) |
| logging / monitoring / detection | التسجيل / المراقبة / الرصد |
| incident / incident response | الحادثة / الاستجابة للحوادث |
| vulnerability management | إدارة الثغرات |
| penetration test / red team | اختبار الاختراق / الفريق الأحمر |
| prompt injection (direct / indirect) | حقن الموجّهات (المباشر / غير المباشر) (prompt injection) |
| jailbreak | كسر القيود (jailbreak) |
| data poisoning | تسميم البيانات (data poisoning) |
| model extraction / membership inference | استخراج النموذج (model extraction) / استنتاج العضوية (membership inference) |
| excessive agency | الصلاحيات المفرطة (excessive agency) |
| guardrails | الضوابط الوقائية (guardrails) |
| agent / tool | الوكيل (agent) / الأداة (tool) |
| retrieval-augmented generation (RAG) | التوليد المعزّز بالاسترجاع (RAG) |
| large language model (LLM) | النموذج اللغوي الكبير (LLM) |
| security champion | سفير الأمن (security champion) |

## Structure the build depends on (do not break)
- Module heading: `# الوحدة N — العنوان` (N unchanged). Lesson heading: `# N.M — العنوان` (numbers unchanged).
- The line right after each lesson heading, translated exactly like this pattern:
  `*المستوى (Level): 🟡 متوسط (Intermediate)* · *المتطلبات (Prerequisites): 1.1، 1.2* · *المرحلة (Phase): Build, Test*`
  (🟢 مبتدئ (Beginner) / 🟡 متوسط (Intermediate) / 🔴 متقدم (Advanced); keep the same emoji; keep lesson numbers; **phase names stay in English** exactly as in the English line; separate lesson lists with «، »). If the English has no prerequisites, omit that part as the English does.
- Section headings keep their emoji first, translated: `## ⚡ الدرس في دقيقة (In 60 seconds)`, `## 🧭 لماذا يهم (Why it matters)`, `## 📐 كيف يعمل (How it works)`, `### 🟢 الأساسيات (The essentials)`, `### 🟡 التعمق أكثر (Going deeper)`, `### 🔴 نظرة الخبير (Expert view)`, `## 🧰 الأدوات (The toolkit)`, `## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)`, `## 🛠️ التمارين (Exercises)`, `## ⚠️ أخطاء وفخاخ (Mistakes and traps)`, `## 🧾 الخلاصة (Recap)`, `## ✍️ اختبر نفسك (Check yourself)`, `## 📚 المراجع (References)` (12.3: `## ✍️ الامتحان التدريبي (Practice exam)`). Same number of `#`/`##`/`###` headings in the same order as the English.
- **🧰 tables:** the first cell of every row must START with the same bold English name as the English row, exactly (e.g. `**STRIDE** — …`, `**Parameterised queries** — …`). Translate everything after the bold name and the other cells. Header row: `| الضابط أو المعيار أو الأداة (Control, standard or tool) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |`.
- **Quizzes:** keep the question numbers; options stay labelled `- A.` `- B.` `- C.` `- D.` in Latin letters and in the same order; `<details><summary>الإجابة</summary>` then a blank line, then `**X.**` with the SAME correct letter as the English; letters cited in explanations stay the same Latin letters. Same number of questions and `<details>` blocks. In 12.3 keep the phase/lesson tag in English, e.g. `*(Build · 2.1)*`.
- **Code blocks stay byte-identical** (code, payload examples, config). Comments inside code stay in English.
- **Mermaid diagrams:** keep the syntax, the direction line and node IDs exactly; translate only the label text into Arabic (no English in the labels, no parentheses inside labels). The build adds the English and flips the direction for Arabic afterwards.
- Keep unchanged: inline `code`, URLs and link targets, numbers, `---` separators, tables' column counts.
- `*Done when:*` → `*يكتمل عندما (Done when):*`.

## Verify
Run: `python3 secai/check_ar.py <english file> <arabic file>` until it prints ✓. It checks headings, the level/phase lines, section emoji order, 🧰 bold names, quiz letters, details blocks, code and mermaid blocks, links and that the text is really Arabic.
