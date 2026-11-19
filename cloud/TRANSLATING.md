# Arabic edition — translation guide (Cloud & DevOps: Zero to Hero)

Not published. Every translator follows this.

## Language and English terms
- Modern Standard Arabic, clear and professional, like a well-written university or professional training manual. Faithful: same meaning, structure, emphasis, lists, tables. Never summarise, add or drop content.
- **English beside each technical term once per lesson.** A technical term carries its English in parentheses at its first use in each lesson, and not again in that lesson: `البنية التحتية بوصفها شيفرة (infrastructure as code)`, `الإطلاق الكناري (canary release)`, `هدف مستوى الخدمة (service level objective, SLO)`, `ميزانية الأخطاء (error budget)`, `المناوبة (on-call)`. Gloss technical terms only, never plain phrases. Gloss whole phrases, never split a construct. A space always separates the Arabic word from `(`. Use the English exactly as the English lesson words it. In quiz options, add a gloss only where the English option needs it, so the glosses never point at the key. Never nest parentheses. Keep product, standard and acronym names in Latin letters with no parentheses. Parentheses that hold formulas, numbers, option letters (A)–(D), citations or section pointers such as `(🟢 الأساسيات.)` are content, not glosses: they always stay.
- Fixed labels keep the English given in this guide, e.g. `يكتمل عندما (Done when)`.
- If a gloss ends in punctuation (`?`, `.`, `!`), wrap it in a left-to-right isolate (the characters U+2066 before `(` and U+2069 after `)`), so it displays correctly in right-to-left text.
- Names of tools, products, standards, companies, platforms, programming languages and commands stay in their English form (Linux, Docker, Kubernetes, Helm, Terraform, OpenTofu, Argo CD, Flux, GitHub Actions, GitLab CI, Prometheus, Grafana, OpenTelemetry, AWS, Azure, Google Cloud, vLLM, Backstage, kubectl). On first use in a unit you may add a short Arabic rendering before it.
- People: Salem سالم, Yousef يوسف, Maha مها, Tariq طارق, Noura نورة, Jassim جاسم, Hamad حمد, Mona منى. Najm Bank → بنك نجم (Najm Bank). Najm Mobile API → واجهة برمجة تطبيق نجم للهاتف (Najm Mobile API); Najm Assist → نجم أسيست (Najm Assist); internal developer platform → منصة المطوّرين الداخلية (internal developer platform).

## Fixed terms
| English | Arabic |
|---|---|
| cloud / region / availability zone | السحابة (cloud) / المنطقة (region) / منطقة التوافر (availability zone); «zone B» is «منطقة التوافر B», never «المنطقة B» |
| platform engineering | هندسة المنصات (platform engineering) |
| site reliability engineering (SRE) | هندسة موثوقية المواقع (SRE) |
| container / image / registry | الحاوية (container) / الصورة (image) / السجل (registry) |
| cluster / pod / node | العنقود (cluster) / الحجيرة (pod) / العقدة (node) |
| infrastructure as code (IaC) | البنية التحتية بوصفها شيفرة (infrastructure as code, IaC) |
| state / drift | الحالة (state) / الانحراف (drift) |
| pipeline / CI/CD | خط التسليم (pipeline) / التكامل والتسليم المستمران (CI/CD) |
| artefact | الأثر البرمجي (artefact) |
| release / rollback / backoff | الإطلاق (release) / التراجع (rollback) / التأخير الأسي (backoff; exponential backoff: إعادة المحاولة بتأخير أسي); never «التراجع» or «مهلة» for backoff |
| blue-green / canary | الأزرق والأخضر (blue-green) / الكناري (canary) |
| observability / telemetry | قابلية المراقبة (observability) / القياس عن بُعد (telemetry) |
| logs / metrics / traces | السجلات (logs) / المقاييس (metrics) / التتبّعات (traces) |
| SLI / SLO / error budget | مؤشر مستوى الخدمة (SLI) / هدف مستوى الخدمة (SLO) / ميزانية الأخطاء (error budget) |
| on-call / incident / postmortem | المناوبة (on-call) / الحادثة (incident) / مراجعة ما بعد الحادثة (postmortem) |
| autoscaling | التوسّع التلقائي (autoscaling) |
| page (on-call) / ticket / dashboard | الاستدعاء (page) / تذكرة عمل (ticket) / لوحة متابعة (dashboard); «استدعاء» otherwise only for API, tool or function calls |
| lead time for changes | زمن إنجاز التغييرات (lead time for changes); never «مهلة» |
| timeout / deadline | المهلة (timeout; expiry: انتهاء المهلة) / الموعد النهائي (deadline); never «المهل الزمنية» |
| TTL | مدة البقاء (TTL); never «مدة الصلاحية» |
| proxy / reverse proxy | الخادم الوسيط (proxy) / الخادم الوسيط العكسي (reverse proxy); never «الوكيل» (= agent) |
| organisation / enterprise | المنظمة (organisation: cloud, GitHub or company org) / المؤسسات (enterprise, the customer segment); never «المؤسسة» for organisation |
| provider / vendor | المزوّد (cloud or model provider) / المورّد (vendor; vendor-neutral: محايد تجاه المورّدين); «مورد» without shadda is «resource» |
| idempotence / idempotency key | عدم التأثر بالتكرار (idempotence) / مفتاح عدم التأثر بالتكرار (idempotency key) |
| scrape / scrape interval | يجمع (scrapes) / فترة الجمع (scrape interval) |
| pilot | التجربة التشغيلية (pilot); «pilot light» (DR) stays الشعلة التجريبية |
| false positive / false alarm | النتيجة الإيجابية الكاذبة (plural: الإيجابيات الكاذبة) / الإنذار الكاذب (false alarm) |
| capstone | المشروع الختامي (capstone) |
| book titles | keep the English title in italics, e.g. *The Site Reliability Workbook*; do not translate it |
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
- **Mermaid diagrams:** keep the syntax and node IDs exactly; where the English runs `LR`, the Arabic runs `RL` (`flowchart RL`, `direction RL`); translate only the label text into Arabic (no English in the labels, no parentheses inside labels).
- **Links:** keep external URLs unchanged. Relative links to other courses in the library point to their Arabic pages: `index.html` → `index.ar.html`, `index.en.html` → `index.ar.html`, `learning-path.html` → `learning-path.ar.html`, `assessment.html` → `assessment.ar.html` (keep the `#…` part). Translate the link text.
- Keep unchanged: inline `code`, numbers, `---` separators, tables' column counts.
- `*Done when:*` → `*يكتمل عندما (Done when):*`.

## Verify
Run: `python3 cloud/check_ar.py <english file> <arabic file>` until it prints ✓. It checks headings, the level/phase lines, section emoji order, 🧰 bold names, quiz letters, details blocks, code and mermaid blocks, links and that the text is really Arabic.
