# 1.2 — رحلة الطلب

*الوحدة (Module) 1: تشريح تطبيق حقيقي (Anatomy of a Real App)*

---

## 🔥 قصة من الميدان

أطلق الفريق (team) مجموعة مسارات خادم (server routes) جديدة تحت `/api-next/` — معالجات حديثة (route handlers) تعيش في تطبيق الويب (web app)، منفصلة عمدًا عن الواجهة البرمجية (API) القديمة (Express) التي تملك `/api/`. اختُبرت محليًا (locally): ممتازة. نُشرت (deployed): كل نداء (call) إلى `/api-next/*` يعود بأخطاء (errors) من... الواجهة *القديمة*. كودٌ (code) لا صلة للمسارات (paths) الجديدة به أصبح يجيب عن طلباتها.

لم يكن الخلل (bug) في أيٍّ من الشيفرتين (codebase)، بل في سطر واحد من إعداد الوسيط (proxy config)، وفي افتراضٍ عن طريقة عمل التوجيه (routing):

```nginx
location /api  { proxy_pass http://api_backend; }   # الفخ
```

`location /api` في nginx **مطابقةُ بادئة (prefix match)**. لا تعني «قسم /api من الموقع (site)»، بل *«أي مسار (path) يبدأ بالحروف `/api`»* — ومن ذلك `/api-next/anything`:

```mermaid
flowchart RL
    R1["GET /api/users"] --> L{"location /api<br/><small>مطابقة بادئة</small><br/>(location /api<br/><small>prefix match</small>)"}
    R2["GET /api-next/auto-play-pick"] --> L
    L -->|"تطابق (matches)"| EXPRESS["الواجهة القديمة Express<br/>(Legacy Express API)"]
    L -.->|"لا يصل أبدًا (never reached)"| NEXT["معالجات Next.js<br/>(Next.js route handlers)"]
    style NEXT stroke-dasharray: 5 5
```

الإصلاح حرفٌ واحد — شرطة مائلة في الآخر (trailing slash): `location /api/`، فلا تطابق (matches) إلا مسارات `/api/...`. لكن الدرس (lesson) أكبر من طرائف nginx: **الطلب (request) الذي تُرسله ليس الطلب الذي يستقبله كودك (your code).** فبين المتصفح (browser) ومعالجك (handler) يجلس نصف دزينة من الأجهزة، لكلٍّ منها حق إعادة توجيهه (reroute) أو كتابته (rewrite) أو تخزينه (cache) أو رفضه (refuse) — وكلٌّ منها يضبطه ملفٌ (file) ربما لم تقرأه قط.

إن لم تستطع أن تروي رحلة الطلب كاملة، فكل خلل في تلك الرحلة (journey) سيحطّ في حِجر كودك متنكرًا في هيئة لغز.

---

## 📐 المبدأ

### 1. الرحلة: إحدى عشرة محطة (eleven stops) وستة ملّاك (six owners)

هذا ما يجري فعلًا حين ينقر مستخدم (user) في بلد آخر عنصرًا واحدًا في تطبيقك — المسار كله، معلَّمًا بمالك كل قفزة (hop):

```mermaid
sequenceDiagram
    autonumber
    participant DB as MongoDB
    participant R as Redis
    participant APP as التطبيق / الواجهة (App / API)
    participant NG as nginx<br/>(خادمك) (nginx<br/>(your VPS))
    participant CDN as حافة CDN<br/>(كلاودفلير) (CDN edge<br/>(Cloudflare))
    participant DNS as محلّل DNS (DNS resolver)
    participant B as المتصفح (Browser)
    B->>DNS: أين relay.app؟ (where is relay.app?)
    DNS-->>B: 104.x.x.x (عنوان الـCDN لا عنوانك) (104.x.x.x (the CDN, not you))
    B->>CDN: GET /item/42 (مصافحة TLS أولًا) (GET /item/42 (TLS handshake first))
    alt إصابة في كاش الحافة (edge cache HIT)
        CDN-->>B: استجابة مخزّنة — خادمك لا يسمع بها أصلًا (cached response — your server never hears about it)
    else إخفاق (MISS)
        CDN->>NG: GET /item/42 (+ ترويسات CF: العنوان الحقيقي والبلد) (GET /item/42 (+ CF headers: real IP, country))
        NG->>APP: proxy_pass ← كتلة location المطابقة (proxy_pass → matched location block)
        APP->>R: GET مفتاح الكاش item:42 (GET cache key item:42)
        alt إصابة في Redis (Redis HIT)
            R-->>APP: JSON مخزّن (cached JSON)
        else إخفاق (MISS)
            APP->>DB: findOne(...)
            DB-->>APP: الوثيقة (document)
            APP->>R: SETEX item:42
        end
        APP-->>NG: 200 + Cache-Control
        NG-->>CDN: الاستجابة (قد تُعاد كتابة الترويسات هنا) (response (headers may be rewritten here))
        CDN-->>B: الاستجابة (وتُخزَّن في الحافة إن سُمح) (response (cached at edge if allowed))
    end
```

عُدَّ الملّاك (owners): جهاز المستخدم، وDNS مزوّده (ISP)، وشركة (company) الـCDN، وإعداد (config) وسيطك، وكود تطبيقك، ومخازن بياناتك (data stores). **بلاغ «خلل في الخادم الخلفي (backend)» قد ينشأ عند أي سهم من الأسهم المرقّمة (numbered arrows) الأحد عشر.** ومعظم بؤس التنقيح (debugging) بحثٌ في المحطة (stop) الثامنة عن مشكلة تسكن الثالثة.

### 2. كل قفزة تضيف كمونًا — احفظ السلّم

رتبٌ تقريبية لرحلة ذهاب وإياب (round trip) من المستخدم إلى الأصل (انظر أرقام الكمون (latency numbers) الشهيرة لجف دين في المراجع (references)؛ هذه نسخة طلب الويب):

| القفزة | الكلفة النموذجية (Typical cost) | ملاحظة (Note) |
|---|---|---|
| استعلام (lookup) DNS (بارد) | 20–120 مللي ثانية (ms) | ثم يُخزَّن مدة TTL |
| مصافحة TLS (TLS handshake) | جولة أو جولتان | الـCDN ينهيها (terminates) قرب المستخدم |
| المستخدم ← حافة CDN (CDN edge) | 5–50 مللي ثانية | الحواف في كل مكان؛ هذه هبة الـCDN |
| الحافة (edge) ← خادمك الأصل (origin) | 50–300 مللي ثانية | عبور القارات (crossing continents)؛ القفزة التي وُجد الكاش ليقتلها |
| nginx ← التطبيق (app) | أقل من مللي ثانية | الجهاز نفسه (same machine) |
| التطبيق ← Redis (إصابة) | ~1 مللي ثانية | لهذا ينجح الكاش |
| التطبيق ← MongoDB (بفهرس) | 1–10 مللي ثانية | لهذا تهم الفهارس (الدرس 2.5) |
| التطبيق ← MongoDB (مسح كامل) | 100 مللي ثانية–10 ثوانٍ | لهذا تُسقط الاستعلاماتُ غير المفهرسة (unindexed queries) المواقع (sites) |

من الجدول تسقط نتيجتان مباشرتان. الأولى: إصابةُ كاشِ (cache hit) CDN (المحطة 4) توفّر أغلى قفزتين (hops) في القائمة — وهذا كل اقتصاد (economics) الوحدة 3. والثانية: القفزة الوحيدة القادرة على النمو الصامت أربعَ مراتب عشرية هي قفزة قاعدة البيانات (database) — ولهذا تُختم الوحدة 2 بخطط الاستعلام (query plans).

### 3. أين مات طلبي؟ — شجرة التشخيص

حين ينكسر شيء، امشِ الرحلة *من الخارج إلى الداخل* (outside-in) مستبعدًا الملّاك واحدًا واحدًا:

```mermaid
flowchart TD
    S["العَرَض: طلب يفشل أو يعود خاطئًا<br/>(Symptom: request fails or is wrong)"] --> Q1{"جرّب curl على الأصل مباشرة<br/>(متجاوزًا الـCDN) — أصحيح؟<br/>(curl the ORIGIN directly<br/>(bypass CDN) — correct?)"}
    Q1 -->|"نعم (yes)"| EDGE["المشكلة عند الحافة:<br/>كاش CDN، قواعد الجدار، DNS<br/><small>حوادث 3.2 و4.3 والجدار الذي حجب أدواتنا</small><br/>(Problem is edge-side:<br/>CDN cache, WAF/bot rules, DNS<br/><small>incidents 3.2, 4.3, and the WAF that blocked our own tooling</small>)"]
    Q1 -->|"لا (no)"| Q2{"اضرب عملية التطبيق مباشرة<br/>(منفذ localhost) — أصحيح؟<br/>(hit the APP PROCESS directly<br/>(localhost port) — correct?)"}
    Q2 -->|"نعم (yes)"| PROXY["المشكلة في الوسيط:<br/>مطابقة location، عمال عالقون، upstream خاطئ<br/><small>حوادث: فخ /api، العامل العالق، الإعدادات الشقيقة</small><br/>(Problem is the proxy:<br/>location matching, stale workers, wrong upstream<br/><small>incidents: /api prefix trap, stale worker, sibling configs</small>)"]
    Q2 -->|"لا (no)"| Q3{"هل تُظهر سجلات التطبيق الطلبَ<br/>بالوسائط المتوقعة؟<br/>(app logs show the request<br/>with expected params?)"}
    Q3 -->|"لا (no)"| ROUTE["لم يبلغ معالجك أصلًا:<br/>وسيطات، مصادقة، تحليل الجسم<br/>(Never reached your handler:<br/>middleware, auth, body parsing)"]
    Q3 -->|"نعم (yes)"| DATA{"استعلم المخزن مباشرة —<br/>هل البيانات صحيحة؟<br/>(query the store directly —<br/>is the DATA right?)"}
    DATA -->|"نعم (yes)"| CODE["منطقك أنت. أخيرًا:<br/>خلل كود حقيقي.<br/>(Your logic. Finally,<br/>an actual code bug.)"]
    DATA -->|"لا (no)"| STORE["كاش قديم أو بيانات فاسدة:<br/>الإبطال، الهجرات<br/><small>حادثتا 3.3 و2.2</small><br/>(Stale cache or bad data:<br/>invalidation, migrations<br/><small>incidents 3.3, 2.2</small>)"]
```

احفظ الشكل لا الصناديق (boxes): **نصّف بالطبقات (bisect by layer)، واختبر الطبقة (layer) التي تحت قبل أن تتهم الطبقة التي كتبتها.** بنك الحوادث (incident bank) مليء بأيام ضاعت في الترتيب المعاكس.

### 4. الترويسات جوازُ سفر الطلب — ويُعاد ختمها

كل قفزة قد تختم ترويسات (headers) أو تنزعها (strip) أو تزوّرها (forge). ثلاثٌ من بنك الحوادث صرتَ تعرف خطرها:

- `CF-Connecting-IP` — ادعاء (claim) الـCDN عن عنوان العميل الحقيقي (real client IP)؛ لا يوثق به *إلا* إذا عجز المهاجمون (attackers) عن بلوغ الأصل مباشرة (الدرس 5.2).
- `Vary` — ادعاء تطبيقك عن تباين الكاش (cache variance)؛ وقد تجاهله الـCDN (الدرس 3.2).
- `Cache-Control` — قابلة للتفاوض (negotiable) عند كل قفزة: التطبيق يضعها، وnginx قد يبدّلها (ذلك كان الإصلاح الدائم لتسميم الكاش)، والـCDN يعيد تفسيرها.

القاعدة العامة: **الترويسة (header) رسالةٌ بين قفزتين (message between two hops) محددتين، لا حقيقة.** لكل ترويسة تعتمد عليها، اعرف أي قفزة تكتبها وأي قفزات قد تعيد كتابتها.

---

## 🎛️ وجّه وكيلك (Direct Your Agent)

اجعل رحلة طلبات (requests) Relay مرئيةً (observable) قبل أن توجد حركة (traffic) أصلًا. أنت توجّه، والوكيل (agent) يبني، وأنت تشاهد الدليل (evidence) يصل.

1. **اختم كل طلب (Stamp every request).** قل لوكيلك:
   > *«أعطِ كل طلب وارد معرّفًا فريدًا (unique ID)، وأعده في ترويسة `X-Request-Id`، وضمّنه كل سطر سجل (log line) يخص الطلب. ثم نفّذ طلبًا واحدًا وأرني: الترويسة في الاستجابة (response)، وأسطر السجل (log lines) المطابقة.»*
2. **سجّل طرف الرحلة (Log the far end).**
   > *«سجّل الفعل (method) والمسار والحالة (status) والمدة (duration) وإصابة/إخفاق (hit/miss) كل نداء مخزن (store call). أرني سطرًا مثالًا (example line) واشرح كل حقل (field) بجملة.»*
3. **امشِ طلبًا واحدًا (Walk one request).** افتح التطبيق بنفسك وانقر شيئًا واحدًا ثم:
   > *«هذا ما نقرته ومتى. جِد ذلك الطلب بعينه بمعرّفه وامشِ بي في كل قفزة قطعها بالترتيب.»*
   أي قفزة بقيت غامضة *عليك أنت* فهي واجبك — اسأل حتى تتضح.
4. **أعد تمثيل فخ البادئة (Reproduce the prefix trap) — عمدًا.**
   > *«ضع وسيطًا محليًا (local proxy) أمام التطبيق فيه كتلة (block) `location /api` بلا شرطة أخيرة، وأضف مسار `/api-next/ping`، وأرني الابتلاع (swallow): الاستجابة الخاطئة، ثم أصلح الشرطة (slash) وأرني الصحيحة.»*
   مشاهدة القبل والبعد مرةً خيرٌ من قراءة عنها عشرًا.
5. **سجّل خط أساس الكمون (latency baseline).**
   > *«قِس طلبًا مخزّنًا (cached request) وآخر غير مخزّن (DNS وTLS والمجموع) واكتب الأرقام في `docs/latency-baseline.md` بتاريخ اليوم.»*
   كل نقاش أداء (performance) لاحق في الدورة (course) يقارن بهذا الملف.

الختام (Finish): *«أودع (commit) برسالة `01-2-journey-traced`.»*

> 🔧 **تحت الغطاء (Under the hood)** (اختياري): المعرّف (ID) `crypto.randomUUID()` في أول الوسيطات (~10 أسطر)؛ والتوقيتات (timings) من صيغ `curl -w`؛ والفخ أيُّ `location` بادئةٍ (prefix) في nginx بلا شرطة أخيرة.

### السياق وحاجز الأمان

**نمط الفشل (failure mode):** الوكيل الذي ينقّح فشلَ طلبٍ يبدأ *من الكود* — لأنه ما يراه. سيسعد بإعادة هيكلة (refactor) معالجٍ ساعةً كاملة والمشكلةُ الحقيقية إعادةُ كتابةٍ في الوسيط (proxy rewrite) لا سبيل له إلى رؤيتها. أنت مالك (owner) الطبقات (layers) التي لا يراها الوكيل — فصرّح بذلك.

**السياق (context) الذي تعطيه:**

> مسار الطلب (request path): المتصفح ← كلاودفلير (Cloudflare) ← nginx (الإعدادات (configs) في ‎/etc/nginx/sites-*‎) ← التطبيق على المنفذ (port) 3000. عند تنقيح أي مشكلة «طلب يفشل / استجابة خاطئة»، حدّد أولًا أيَّ قفزة تفشل: curl على الأصل مباشرة (origin-direct)، ثم localhost، ثم سجلات (logs) التطبيق بمعرّف الطلب (request ID) — قبل اقتراح أي تعديل كود.

**أسئلة المراجعة (review questions) لأي تغيير في التوجيه أو الوسيطات (middleware):**

1. «امشِ بهذا الطلب من المتصفح إلى المعالج: أي كتلة location تطابقه؟ وماذا تطابق غيرَه؟» (فخاخ البوادئ)
2. «أي ترويسات يثق بها هذا الكود؟ وأي قفزة تكتب كلًّا منها؟»
3. «لو عادت هذه الاستجابة خاطئةً لمستخدم واحد، أي سطر سجل وأي معرّف طلب يثبتان أين أخطأت؟»

**حاجز الأمان (guardrail) الذي تثبّته:** اختبار جدول توجيه — سكربت (script) يمرّر curl على كل عائلة مسارات (route family) عبر الرزمة المحلية (local stack) كاملةً (بالوسيط (proxy)، لا التطبيق وحده) ويؤكد أي عملية (process) أجابت. كان سيلتقط ابتلاع `/api-next` في CI بدل الإنتاج (production).

---

## ✅ تحقق منه (Verify It)

لا قراءة كود مطلوبة — لا تقبل الدرس إلا حين:

- [ ] نقرتَ شيئًا واحدًا في التطبيق العامل (running app)، وأراك الوكيل أثرَ **ذلك الطلب (request) بعينه** في السجلات، مُهتديًا بالمعرّف الذي رأيته أنت في ترويسة الاستجابة.
- [ ] شاهدتَ فخ البادئة (prefix trap) حيًّا: الإجابة الخاطئة قبل الشرطة والصحيحة بعدها. رأيت الاستجابتين بنفسك لا ملخصًا عنهما.
- [ ] ملف `docs/latency-baseline.md` موجود ومؤرَّخ، ورقم الطلب المخزّن أصغر بوضوح من غير المخزّن (uncached) — وتستطيع قول *السبب* في جملة.
- [ ] بالاستعانة بالمخطط التسلسلي (sequence diagram) تستطيع رواية المحطات الإحدى عشرة من الذاكرة (memory) — وتسمية ما تملكه أنت منها وما يملكه غيرك.
- [ ] حاجز جدول التوجيه (routing-table guardrail) يعمل في CI: اطلب من الوكيل كسر التوجيه عمدًا في فرع (branch) وأرِك الفحص (check) يفشل، ثم ينجح بعد التراجع (revert).

---

## 🧾 بطاقة الخلاصة (Recap card)

- إحدى عشرة محطة وستة ملّاك؛ «خلل الخادم الخلفي (backend bug)» قد موجود في أيًّا منها.
- نصّف من الخارج إلى الداخل (Bisect outside-in): الأصل مباشرة، فالعملية مباشرة (process-direct)، فالسجلات، فالبيانات (data) — والكود آخرًا.
- احفظ سلّم الكمون (latency ladder)؛ قفزة قاعدة البيانات وحدها تنمو عشرة آلاف ضعف.
- الترويسات رسائل بين قفزتين (hop-to-hop messages) لا حقائق؛ اعرف من يكتب ومن يعيد الكتابة.
- ‏`location /api` تطابق `/api-next`. الشرطات المائلة الأخيرة (Trailing slashes) تحمل أوزانًا.

## 📚 المراجع ومزيد من القراءة (References & further wandering)

- MDN: **نظرة عامة على HTTP** و**التخزين المؤقت (caching) في HTTP** — [developer.mozilla.org/docs/Web/HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP). المرجع الأوضح لكل ترويسة في هذا الدرس.
- ‏RFC 9110: **دلالات HTTP (HTTP Semantics)** (2022) — العقد الفعلي الذي يفترض بكل قفزة احترامه (وقد أرانا الدرس 3.2 أنها لا تفعل دائمًا).
- جف دين: **أرقام الكمون التي على كل مبرمج معرفتها (Latency Numbers Every Programmer Should Know)** — النسخة التفاعلية المحدّثة سنويًا لكولن سكوت: [colin-scott.github.io/.../interactive_latency.html](https://colin-scott.github.io/personal_website/research/interactive_latency.html).
- ‏W3C: **Trace Context** — [w3.org/TR/trace-context](https://www.w3.org/TR/trace-context/) — المعيار (standard) الذي يكبر إليه `X-Request-Id` عندك؛ وتطبّقه **OpenTelemetry** ([opentelemetry.io](https://opentelemetry.io)).
- وثائق (docs) nginx: **كيف يعالج nginx الطلب (How nginx processes a request)** وتوجيه `location` — قراءة الدقائق الخمس التي تقيك فخ البادئة.
- مركز تعلم كلاودفلير: **ما شبكة CDN؟** — [cloudflare.com/learning/cdn](https://www.cloudflare.com/learning/cdn/what-is-a-cdn/) — مخططات واضحة لطوبولوجيا الحافة (edge topology) في هذا الدرس.

*الحوادث المصدرية (Source incidents): [بنك الحوادث — النشر (deploy) والبنية التحتية (infrastructure)](../../war-stories/incident-bank.md)*
