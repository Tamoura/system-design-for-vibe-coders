# Arabic edition — translation guide (Cloud & DevOps: Zero to Hero)

Not published. Every translator follows this.

## Language and English terms
- Modern Standard Arabic, clear and professional, like a well-written university or professional training manual. Faithful: same meaning, structure, emphasis, lists, tables. Never summarise, add or drop content.
- **English beside every technical term everywhere.** In every paragraph, list item, table cell, heading, quiz question, option and answer, each technical term and key phrase carries its English in parentheses on its first appearance in that unit (a unit = one paragraph, one list item, one table cell, one heading): `البنية التحتية بوصفها شيفرة (infrastructure as code)`, `الإطلاق الكناري (canary release)`, `هدف مستوى الخدمة (service level objective, SLO)`, `ميزانية الأخطاء (error budget)`, `المناوبة (on-call)`. Aim for roughly one gloss every 4–6 Arabic words in technical text. Gloss whole phrases, never split a construct. A space always separates the Arabic word from `(`. Use the English exactly as the English lesson words it.
- Key phrases, rules of thumb, labels and framework step names also get their English, e.g. `يكتمل عندما (Done when)`.
- If a gloss ends in punctuation (`?`, `.`, `!`), wrap it in a left-to-right isolate (the characters U+2066 before `(` and U+2069 after `)`), so it displays correctly in right-to-left text.
- Names of tools, products, standards, companies, platforms, programming languages and commands stay in their English form (Linux, Docker, Kubernetes, Helm, Terraform, OpenTofu, Argo CD, Flux, GitHub Actions, GitLab CI, Prometheus, Grafana, OpenTelemetry, AWS, Azure, Google Cloud, vLLM, Backstage, kubectl). On first use in a unit you may add a short Arabic rendering before it.
- People: Salem سالم, Yousef يوسف, Maha مها, Tariq طارق, Noura نورة, Jassim جاسم, Hamad حمد, Mona منى. Najm Bank → بنك نجم (Najm Bank). Najm Mobile API → واجهة برمجة تطبيق نجم للهاتف (Najm Mobile API); Najm Assist → نجم أسيست (Najm Assist); internal developer platform → منصة المطوّرين الداخلية (internal developer platform).

## Fixed terms
| English | Arabic |
|---|---|
| cloud / region / availability zone | السحابة (cloud) / المنطقة (region) / منطقة التوافر (availability zone) |
| platform engineering | هندسة المنصات (platform engineering) |
| site reliability engineering (SRE) | هندسة موثوقية المواقع (SRE) |
| container / image / registry | الحاوية (container) / الصورة (image) / السجل (registry) |
| cluster / pod / node | العنقود (cluster) / الحجيرة (pod) / العقدة (node) |
| infrastructure as code (IaC) | البنية التحتية بوصفها شيفرة (infrastructure as code, IaC) |
| state / drift | الحالة (state) / الانحراف (drift) |
| pipeline / CI/CD | خط التسليم (pipeline) / التكامل والتسليم المستمران (CI/CD) |
| artefact | الأثر البرمجي (artefact) |
| release / rollback | الإطلاق (release) / التراجع (rollback) |
| blue-green / canary | الأزرق والأخضر (blue-green) / الكناري (canary) |
| observability / telemetry | قابلية المراقبة (observability) / القياس عن بُعد (telemetry) |
| logs / metrics / traces | السجلات (logs) / المقاييس (metrics) / التتبّعات (traces) |
| SLI / SLO / error budget | مؤشر مستوى الخدمة (SLI) / هدف مستوى الخدمة (SLO) / ميزانية الأخطاء (error budget) |
| on-call / incident / postmortem | المناوبة (on-call) / الحادثة (incident) / مراجعة ما بعد الحادثة (postmortem) |
| autoscaling | التوسّع التلقائي (autoscaling) |
| disaster recovery / RTO / RPO | التعافي من الكوارث (disaster recovery) / RTO / RPO |
| least privilege | أقل الصلاحيات (least privilege) |
| cost allocation / FinOps | توزيع التكلفة (cost allocation) / FinOps |
| model serving / LLM gateway | تقديم النماذج (model serving) / بوابة النماذج اللغوية (LLM gateway) |

## Structure the build depends on (do not break)
- Module heading: `# الوحدة N — العنوان` (N unchanged). Lesson heading: `# N.M — العنوان` (numbers unchanged).
- The line right after each lesson heading, translated exactly like this pattern:
  `*المستوى (Level): 🟡 متوسط (Intermediate)* · *المتطلبات (Prerequisites): 1.1، 1.2* · *المرحلة (Phase): Build, Deploy*`
  (🟢 مبتدئ (Beginner) / 🟡 متوسط (Intermediate) / 🔴 متقدم (Advanced); keep the same emoji; keep lesson numbers; **phase names stay in English** exactly as in the English line; separate lesson lists with «، »). If the English has no prerequisites, omit that part as the English does.
- Section headings keep their emoji first, translated: `## ⚡ الدرس في دقيقة (In 60 seconds)`, `## 🧭 لماذا يهم (Why it matters)`, `## 📐 كيف يعمل (How it works)`, `### 🟢 الأساسيات (The essentials)`, `### 🟡 التعمق أكثر (Going deeper)`, `### 🔴 نظرة الخبير (Expert view)`, `## 🧰 الأدوات (The toolkit)`, `## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)`, `## 🛠️ التمارين (Exercises)`, `## ⚠️ أخطاء وفخاخ (Mistakes and traps)`, `## 🧾 الخلاصة (Recap)`, `## ✍️ اختبر نفسك (Check yourself)`, `## 📚 المراجع (References)` (7.3: `## ✍️ الامتحان التدريبي (Practice exam)`). Same number of `#`/`##`/`###` headings in the same order as the English.
- **🧰 tables:** the first cell of every row must START with the same bold English name as the English row, exactly (e.g. `**Docker** — …`, `**Canary release** — …`). Translate everything after the bold name and the other cells. Header row: `| الأداة أو الممارسة أو الخدمة (Tool, practice or service) | ما هي وماذا تفعل (What it is and does) | متى تلجأ إليها (When to reach for it) |`.
- **Quizzes:** keep the question numbers; options stay labelled `- A.` `- B.` `- C.` `- D.` in Latin letters and in the same order; `<details><summary>الإجابة</summary>` then a blank line, then `**X.**` with the SAME correct letter as the English; letters cited in explanations stay the same Latin letters. Same number of questions and `<details>` blocks. In 7.3 keep the phase/lesson tag in English, e.g. `*(Deploy · 4.2)*`.
- **Code blocks stay byte-identical** (code, SQL, YAML, shell, config). Comments inside code stay in English.
- **Mermaid diagrams:** keep the syntax, the direction line and node IDs exactly; translate only the label text into Arabic (no English in the labels, no parentheses inside labels). The build adds the English and flips the direction for Arabic afterwards.
- **Links:** keep external URLs unchanged. Relative links to other courses in the library point to their Arabic pages: `index.html` → `index.ar.html`, `index.en.html` → `index.ar.html`, `learning-path.html` → `learning-path.ar.html`, `assessment.html` → `assessment.ar.html` (keep the `#…` part). Translate the link text.
- Keep unchanged: inline `code`, numbers, `---` separators, tables' column counts.
- `*Done when:*` → `*يكتمل عندما (Done when):*`.

## Verify
Run: `python3 cloud/check_ar.py <english file> <arabic file>` until it prints ✓. It checks headings, the level/phase lines, section emoji order, 🧰 bold names, quiz letters, details blocks, code and mermaid blocks, links and that the text is really Arabic.
