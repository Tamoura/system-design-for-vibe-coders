# الوحدة (Module) 5 — مستخدمون حقيقيون، إساءة حقيقية (Real Users, Real Abuse)

*في اللحظة التي يصبح فيها منتجك (your product) متاحًا، يتوقف عن كونه مقصودًا ممن تخيّلتهم وحدهم.
يزوره كذلك سكربتات (scripts) وكاشطات (scrapers) ومُرسِلو رسائل مزعجة (spammers) وفضوليون — معظمهم آليّ (automated)، ولا أحد
منهم يقرأ شروط الخدمة (terms of service). هذه الوحدة (Module) عن النجاة من هذا الواقع: رفع تكلفة المهاجم (attacker)،
ومعرفة من يتصل بك حقًا، وتشغيل مصادقة (auth) تستطيع إدارتها، وعدم الوثوق بمدخلات (input) لم تنتبه
أنك تثق بها، والتعامل مع البريد (email) بوصفه بنية تحتية إنتاجية (production infrastructure)، والسير على قائمة OWASP
العشرة (Top 10) بوصفها قائمة تحقّق (checklist)، وإبعاد مفاتيح المملكة (keys to the kingdom) عن الأيدي الخطأ.*

---

# 5.1 — أول مهاجم لك هو سكربت (Your First Attacker Is a Script)

## 🔥 قصة من الميدان (The War Story)

خلال 24 ساعة، ربح المنتج (product) 45 حسابًا (accounts) جديدًا. كلها باسم «bob». ولم يكن أيٌّ منها
لشخص حقيقي. كل تسجيل (registration) استخدم بريد (email) *شخصٍ حقيقيٍّ مختلف* — عناوين (addresses) مكشوطة (scraped) من مكان آخر —
وكل تسجيل (registration) أطلق رسالة «فعّل حسابك (your account)» مباشرةً إلى ذلك الغريب البريء.

فوصل 45 شخصًا لم يسمعوا بالمنتج (product) قط رسائلُ تفعيل (verification mail) لم يطلبوها. والأسوأ كان خفيًا عن
لوحة التحكم (dashboard): كل تلك الرسائل خرجت من نطاق الإرسال (sending domain) الخاص بالمنتج (product) نفسه. وفي نظر مزوّدي
البريد (mail providers) المراقبين، بدا المنتج (product) هو المُرسِل المزعج (spammer). وكانت **سمعة المُرسِل (Sender
Reputation)** — درجة الثقة التي تقرر أتصل رسائله إلى صناديق الوارد (inboxes) أم إلى المهملات (junk folders) —
تُحرَق لتشغيل حملة مضايقة (harassment campaign) يخوضها شخص آخر.

كان الحدس الأول خاطئًا: «حُدّ (limit) عدد التسجيلات (registrations)». لكن حدًّا عامًا (global limit) على مستوى الموقع كله
هو نفسه سلاح — فمن يبلغه من المهاجمين (attackers) يكون قد منع المستخدمين (users) *الشرعيين (legitimate)* من التسجيل (signup).
هذا حجب خدمة (denial-of-service) بنيتَه له بنفسك.

كان الإصلاح (fix) الذي وصل متعدد الطبقات (layered). اختبار (test) CAPTCHA (نستخدم Cloudflare Turnstile)
على التسجيل (signup) ونسيان كلمة المرور (forgot-password)، كي يضطر السكربت (script) إلى حل فحص بشري (human-check) قبل أن يكلّفك شيئًا.
وحدٌّ (limit) أضيق لكل عنوان IP (per-IP). والحركة الأهم (the key move): **ميزانية عامة (global budget) على البريد الصادر (outbound email) نفسه** —
أي تحديد معدل (rate limit) الأثر الجانبي (side effect) المكلف والضار (إرسال البريد (email) إلى الغرباء)، لا نقرة
المستخدم (user). يظل المهاجم (attacker) قادرًا على الطرق على نموذج التسجيل (signup form)، لكن الرسائل تتوقف عن
الخروج، ويبقى المستخدمون (users) الحقيقيون قادرين على التسجيل (signup).

**الدرس (lesson) في جملة: حدّد معدل (rate-limit) الأثر الجانبي (side effect) المكلف لا فعل المستخدم (user) — ولا تبنِ حدًا (limit)
عامًا يستطيع المهاجم (attacker) بلوغه ليقفل الباب على الجميع.**

## 📐 المبدأ (The Principle)

### 1. الإساءة (abuse) اقتصاد: ارفع تكلفة المهاجم (attacker's cost) فوق العائد (payoff)

يشغّل المهاجم (attacker) سكربتًا (script) لأنه *رخيص*. مهمتك ليست جعل الإساءة (abuse) مستحيلة، بل جعلها تكلّف
أكثر مما تستحق. كل دفاع (defense) هو زيادة سعر.

```mermaid
flowchart TD
    A["طلب مجهول<br/>يصيب نقطة نهاية مجانية"] --> B{"هل حُلّ<br/>CAPTCHA؟"}
    B -->|لا| X["محظور — يكلّف المهاجم<br/>إنسانًا أو رسمَ حلّال"]
    B -->|نعم| C{"ضمن الحد<br/>لكل IP؟"}
    C -->|لا| X2["مُقيَّد — يحتاج المهاجم<br/>عناوين كثيرة = تكلفة أعلى"]
    C -->|نعم| D{"ضمن ميزانية<br/>الأثر الجانبي؟"}
    D -->|لا| X3["الأثر الجانبي مكبوت<br/>(لا بريد) — والفعل ما زال ينجح"]
    D -->|نعم| E["مسموح"]
```

كل بوابة (gate) ترفع تكلفة مختلفة: فحصًا بشريًا (human-check)، وتكلفة تنوّع العناوين (IP-diversity)، وسقفًا صلبًا (hard ceiling) على
الضرر الذي يحدثه الطوفان (flood). لا يلزم أن تكون أيٌّ منها كاملة. ومعًا تنقل الإساءة (abuse) من
«مجانية وبلا حد (limit)» إلى «مزعجة ومحدودة».

### 2. نقاط النهاية المجانية (free endpoints) الثلاث، والأثر الجانبي (side effect) خلف كل واحدة

كل منتج (product) يكشف حفنةً من نقاط النهاية (endpoints) لمن ليسوا مسجّلي الدخول (logged in). هذه هي خط المواجهة (front line)،
لأنها تكلّفك *أنت* شيئًا في كل مرة تعمل فيها.

| نقطة نهاية مجهولة (anonymous endpoint) | الأثر الجانبي (side effect) المكلف | حدّد معدل (rate-limit)… |
|---|---|---|
| التسجيل (signup) | يرسل بريدًا (email) إلى **طرف ثالث (third party)** | البريد الصادر (outbound email)، لكل IP (per-IP)، + CAPTCHA |
| نسيان كلمة المرور (forgot-password) | يرسل بريدًا (email)؛ ويكشف أي الحسابات (accounts) موجود | ميزانية البريد (email budget) + ردود عامة (generic responses) |
| البحث (search) | يشغّل استعلامًا (query) مكلفًا؛ وقابل للكشط (can be scraped) | تكلفة الاستعلام (query cost)، لكل IP (per-IP) |

لاحظ أن هدف الحد (limit) ليس «الزر» أبدًا. بل الشيء الذي خلف الزر ويؤلم حين يعمل مليون مرة.

### 3. حدّد معدل (rate-limit) الأثر الجانبي (side effect) لا الفعل

هذا هو المبدأ (The Principle) كله. إن قيّدت *فعل التسجيل (signup)*، فسيجبرك مهاجم (attacker) مصمّم على الاختيار بين
السماح له والإقفال على المستخدمين (users) الحقيقيين. أما إن قيّدت *إرسال البريد (email)* — الشيء
الذي يضرّك فعلًا ويضايق الغرباء — فيستطيع المهاجم (attacker) إدارة النموذج (form) بلا فائدة بينما لا
يخرج شيء سيّئ من نظامك، وتظل التسجيلات (registrations) الشرعية (legitimate) في أماكن أخرى تكتمل.

وهنا تحفّظ صادق: الميزانية العامة (global budget) *الواحدة* على البريد الصادر (outbound email) تحمل شكل حجب الخدمة (denial of service)
الذاتي نفسه الذي يحذّر منه هذا الدرس (lesson) — فحين تُستنفد، لا يصل البريد (email) أيضًا إلى مستخدم (user)
حقيقي يسجّل في تلك النافذة الزمنية نفسها، رغم أنه لم يفعل شيئًا خطأ. لذلك اجعل ضابطك
**الأساسي** ميزانيةً (budget) لكل عنوان IP (per-IP) ولكل مستلِم (recipient) (فالمهاجم (attacker) من عنوان (address) واحد، أو الذي يقصف
عنوانًا (address) واحدًا، يُوقَف دون المساس بأحد آخر)، وأبقِ الميزانية العامة (global budget) مجرد شبكة أمان (backstop)
أخيرة، بسقفٍ (ceiling) مرتفع بما يكفي كي لا تبلغه الحركة (traffic) الطبيعية أبدًا. ونبّه (alert) حين تُستنفد
الميزانية العامة (global budget)، لأن ذلك يعني إما أن هجومًا تجاوز الحدود (limits) الأدق، أو أن السقف (ceiling) مضبوط
منخفضًا أكثر من اللازم.

### 4. رفض البريد المؤقت (disposable email) والردود الثابتة

حركتان ختاميتان رخيصتان. ارفض نطاقات البريد المؤقت/المستهلك (disposable/throwaway email) المعروفة عند التسجيل (signup) —
فمعظم الإساءة الآلية (automated abuse) تعتمد عليها. واجعل نسيان كلمة المرور (forgot-password) يعيد **الرد العام (generic response) نفسه**
سواءً وُجد الحساب (account) أم لا («إن كان هذا البريد (email) مسجّلًا، أرسلنا رابطًا»)، كي لا تُستعمل
نقطة النهاية (endpoint) لتعداد (enumerate) أصحاب الحسابات (accounts).

**اقرن ذلك بحالة شهيرة.** أطاح هجوم Dyn على DNS (أكتوبر 2016) بتويتر ونتفليكس
وReddit من الإنترنت — لا باختراقها، بل بتوجيه شبكة (botnet) Mirai، وهي جيش من الكاميرات
ومسجّلات الفيديو المخترَقة، إلى مزوّد DNS (DNS provider) المشترك بينها. والدرس (lesson) المهم هنا: *الأجهزة
الآلية الرخيصة على نطاق واسع قوة في تصميم الأنظمة*. أول مهاجم لك (your first attacker) ليس عبقريًا
بقلنسوة، بل سكربت (script) يعمل على عتاد (hardware) بلا كلفة، يفعل شيئًا واحدًا غبيًا مليون مرة. صمّم
للسكربت (script).

## 🎛️ وجّه وكيلك (Direct Your Agent)

لدى Relay ثلاث نقاط نهاية مجهولة (التسجيل (signup)، ونسيان كلمة المرور (forgot-password)، والبحث (search)). وهي الآن
مجانية. لنُسعّرها.

1. **احصر نقاط النهاية المجانية (free endpoints) وآثارها الجانبية (their side effects).**
   > *«اسرد كل نقطة نهاية (endpoint) في Relay يستطيع متصلٌ مجهول (anonymous caller) غير مصادَق (unauthenticated) أن يبلغها. ولكل
   > واحدة، أخبرني بأغلى ما يحدث حين تعمل — خاصةً أي شيء يرسل بريدًا (email) أو يكتب في قاعدة
   > البيانات (database) — ومن يدفع ثمنه.»*
2. **ضع فحصًا بشريًا (human-check) أمام النماذج (forms) التي ترسل البريد (email).**
   > *«أضف Cloudflare Turnstile (اختبار (test) CAPTCHA) إلى نموذجي التسجيل (signup forms) ونسيان كلمة
   > المرور في Relay. ويجب أن يرفض الخادم (server) الطلب (request) إن كان رمز (token) Turnstile مفقودًا أو
   > غير صالح. وأرني النموذج (form) يفشل بلا تحدٍّ (challenge) محلول.»*
3. **موّل الأثر الجانبي (side effect) لا الفعل.**
   > *«أضف ميزانية يومية عامة (global daily budget) على رسائل التفعيل (verification emails)/إعادة التعيين (reset) الصادرة، مخزّنة في
   > Redis. وحين تُتجاوز الميزانية (budget)، يظل التسجيل (signup) يعيد نجاحًا للمستخدم (user) لكن البريد (email) لا
   > يُرسَل بصمت ويُسجَّل (logged) الحدث. لا تضف حدًا عامًا (global limit) على فعل التسجيل (signup) نفسه — واشرح لماذا
   > سيكون ذلك حجب خدمة ذاتيًا (self-inflicted denial of service).»*
4. **ارفض البريد المؤقت (disposable email) وحصّن إعادة التعيين (reset) من التعداد (enumeration).**
   > *«ارفض التسجيلات (registrations) من نطاقات البريد المؤقت (disposable-email domains) المعروفة. واجعل نسيان كلمة المرور (forgot-password)
   > يعيد الرد العام (generic response) نفسه بالضبط سواءً وُجد الحساب (account) أم لا. وأرني الحالتين تعيدان
   > مخرجات متطابقة.»*
5. **أثبته تحت النار (under fire).**
   > *«اكتب سكربتًا (script) يطلق 200 تسجيل (registration) من عنوان IP (IP address) واحد بـ200 بريد (email) مختلف، مثل طوفان (flood)
   > «bob». وأرني: النموذج (form) يُقيَّد (throttled)، وميزانية البريد (email budget) تحدّ (challenge) من الضرر، ومستخدم (user) حقيقي من
   > عنوان (address) مختلف يظل قادرًا على التسجيل (signup) أثناء الهجوم.»*

الختام (Finish): *«أودع (commit) برسالة `05-1-abuse-defense`.»*

> 🔧 **تحت الغطاء (Under the hood)** (اختياري (optional)): Turnstile تحقّقٌ من الرمز (token) على الخادم (`POST` إلى
> `siteverify` بمفتاحك السري (secret))؛ وميزانية البريد (email budget) `INCR` في Redis على مفتاح يومي (daily key) مع
> `EXPIRE`، تُفحَص قبل نداء الإرسال لا قبل المعالِج (handler)؛ ورفض النطاقات المؤقتة (disposable domains) قائمة
> مفحوصة عند التحقق (validation).

## ✅ تحقق منه (Verify It)

- [ ] تستطيع تسمية نقاط Relay المجهولة (Relay's anonymous endpoints) الثلاث، ولكل واحدة الأثر الجانبي (side effect) المكلف الذي
      يحميه الحد (limit) — *الأثر الجانبي (side effect)*، لا الزر.
- [ ] نموذج التسجيل (signup form) يفشل ظاهريًا حين لا يُحلّ CAPTCHA.
- [ ] شغّلت طوفان (flood) «bob» بنفسك ورأيت البريد الصادر (outbound email) يُحدّ بسقف (capped) بينما يظل مستخدم (user) حقيقي
      على عنوان (address) آخر قادرًا على التسجيل (signup).
- [ ] نسيان كلمة المرور (forgot-password) يعيد مخرجات متطابقة تمامًا لبريد (email) حقيقي وآخر وهمي.
- [ ] تستطيع إعادة رواية حادثة (incident) «bob» وشرح لماذا كان الحد العام (global cap) على التسجيل (signup) سيهدي
      المهاجم (attacker) حجب خدمة (denial-of-service) بدلًا من إيقاف واحد.

## 🧾 بطاقة الخلاصة (Recap card)

- أول مهاجم لك (your first attacker) سكربت (script): رخيص، آليّ، يفعل شيئًا واحدًا غبيًا مليون مرة.
- الدفاع (defense) عن الإساءة (abuse) اقتصاد — ارفع التكلفة فوق العائد (payoff)؛ ولا يلزم أن تكون أي بوابة (gate) كاملة.
- حدّد معدل (rate-limit) **الأثر الجانبي (side effect)** المكلف (البريد (email)، الاستعلام (query))، لا فعل المستخدم (user) أبدًا.
- الحد العام (global cap) على الفعل حجب خدمة (denial-of-service) بنيتَه للمهاجم (attacker).
- CAPTCHA + حد (limit) لكل IP (per-IP) + ميزانية أثر جانبي (side-effect budget) + رفض البريد المؤقت (disposable email) = دفاع بعمق (defense in depth) لنقاط النهاية المجانية (free endpoints).

## 📚 المراجع ومزيد من القراءة (References & further wandering)

- ‏OWASP: **«صدّ هجمات التخمين (Blocking Brute Force Attacks)»** ومشروع **التهديدات الآلية لتطبيقات الويب (Automated Threats to Web Applications)** — فهرس ما تفعله السكربتات (scripts) بك فعلًا.
- وثائق (docs) Cloudflare Turnstile — اختبار (test) CAPTCHA المستخدم (user) هنا؛ والتحقق على الخادم (server) هو الجزء المهم.
- تغطية Krebs on Security لشبكة **Mirai وهجوم Dyn** (2016) — الأجهزة الرخيصة على نطاق واسع قوةً في تصميم الأنظمة.
- ورقة (cheat sheet) OWASP **«نسيان كلمة المرور (forgot-password)»** — الردود العامة ومقاومة التعداد (enumeration resistance) بالتفصيل.
- The System Design Primer (مفتوح المصدر (open source)) — قسم **الأمان / تحديد المعدل (security / rate limiting)** للخريطة (map) الأوسع.

---

# 5.2 — تحديد معدل ينجو من CDN (Rate Limiting That Survives a CDN)

## 🔥 قصة من الميدان (The War Story)

كان مُحدِّد المعدل (rate limiter) يعمل بإتقان. وتلك كانت المشكلة.

وردت بلاغات أن مستخدمين (users) شرعيين (legitimate) — أناسًا عاديين بحركة (traffic) متواضعة — يتلقّون
`429 Too Many Requests`. لا مهاجمين، بل زوّارًا اعتياديين، محظورين من موقع لا يتعرض
لأي حِمل (load) غير معتاد. وبدت أرقام المحدِّد (limiter) نفسه مقلقة: حفنة من عناوين IP (IP addresses) يولّد كلٌّ
منها حجم طلبات (request volumes) هائلًا، يفوق أي حد (limit) معقول لكل مستخدم (user). ففعل المحدِّد (limiter) ما أُمر به تمامًا
وألقى 429.

لكن تلك «الحفنة من العناوين» لم تكن مستخدمين (users). كانت عناوين (addresses) **Cloudflare**.

وإليك الفخّ. كان المنتج (product) خلف CDN. فكل طلب من كل شخص على الأرض يصل إلى الخادم الأصلي (origin server)
*من الـCDN*، وبقدر ما ترى مقبس الشبكة (network socket) في الأصل (origin)، جاءت حركة العالم كلها من مجموعة
صغيرة من عناوين حافة (edge) الـCDN. وقد ربط المحدِّد (limiter) عدّاداته (counters) بعنوان المقبس (socket IP) ذاك. فلم يكن
يحدّ لكل مستخدم (user) أصلًا — بل كان يحدّ لكل عقدة (node) CDN، ما يعني أن **الكوكب كله شارك حفنة
من دِلاء تحديد المعدل (rate-limit buckets)**. فتملأ منطقةٌ (region) مزدحمة الدلو (bucket)، ويتلقّى الجميع خلف تلك العقدة (node)
429.

وكان تحته خطأ أهدأ. عاشت العدّادات (counters) في ذاكرة عملية التطبيق (app process memory). فكل نشر (deploy) يعيدها إلى الصفر،
ومع تشغيل أكثر من نسخة (instance) واحدة من التطبيق (app)، عدّت كلُّ نسخة على حدة — فالمستخدم (user) نفسه
يصيب نسختين (two instances) فيحصل على عدّتين مستقلتين (two independent counters). فلم يكن الحد (limit) مشتركًا ولا دائمًا.

كان الإصلاح (fix) على جزأين. اربط المحدِّد (limiter) بـ**عنوان العميل الحقيقي (real client IP) الذي يمرّره الـCDN في
ترويسة (header)** (`CF-Connecting-IP`)، لا بعنوان المقبس (socket IP). وانقل العدّادات (counters) إلى **Redis**،
وهو مخزن مشترك (shared store) تقرأه كل النسخ (all instances) وينجو من النشر (deploy). توقّف المستخدمون (users) الشرعيون عن تلقّي
429، وأخيرًا صار الحد (limit) يعني ما افترضه الجميع.

**الدرس (lesson): خلف أي وسيط (proxy)، «عنوان العميل (client IP)» ليس ما يراه مقبسك (your socket) — بل ادّعاءٌ يجب أن تختار
قراءته عمدًا، وأن تدافع عنه من التزوير (forgery) عمدًا.**

## 📐 المبدأ (The Principle)

### 1. الهوية عند الحافة (Identity at the edge): ما معنى «عنوان العميل (client IP)» أصلًا

في اللحظة التي تضع فيها أي شيء بين المستخدم (user) وتطبيقك — CDN أو موزّع حِمل (load balancer) أو وسيط (proxy)
عكسي (reverse proxy) — يتوقف خادمك عن مخاطبة المستخدم (user) مباشرة، ويخاطب الوسيط (proxy). فيصبح عنوان المقبس (socket IP) عنوان (address)
*الوسيط (proxy)*.

```mermaid
flowchart RL
    U1["المستخدم أ<br/>العنوان الحقيقي 1.1.1.1"] --> CDN["حافة CDN<br/>العنوان 104.16.0.5"]
    U2["المستخدم ب<br/>العنوان الحقيقي 2.2.2.2"] --> CDN
    U3["المستخدم ج<br/>العنوان الحقيقي 3.3.3.3"] --> CDN
    CDN -->|"عنوان المقبس = 104.16.0.5<br/>لهم جميعًا"| O["الخادم الأصلي"]
    CDN -.->|"CF-Connecting-IP: العنوان الحقيقي<br/>في ترويسة"| O
```

عنوان العميل الحقيقي (real client IP) ما زال موجودًا — يضعه الـCDN في ترويسة طلب (`CF-Connecting-IP`،
أو `X-Forwarded-For` المعيارية). لكن على كودك أن *يعرف أن يقرأ تلك الترويسة (header) بدل
المقبس (socket)*. اقرأ المقبس وقد جمعت الإنترنت كلها في حفنة دِلاء (buckets).

### 2. العدّادات الموزّعة (Distributed counters) تحتاج تخزينًا مشتركًا (shared storage)

تحديد المعدل (rate limit) عدّاد (counter): «قدّم هذا المعرِّف N طلبًا (request) في الدقيقة الأخيرة». ومكان عيش ذلك
العدّاد (counter) يقرر أهو حدّ (limit) حقيقي أم لا.

| أين يعيش العدّاد (counter) | ما الذي ينكسر |
|---|---|
| في ذاكرة عملية التطبيق (app process memory) | يُصفَّر مع كل نشر؛ وكل نسخة (instance) تعدّ على حدة — لا حدّ (limit) مشترك |
| في نسخة (instance) واحدة فقط | يعمل حتى تتوسع (scale) إلى نسختين (two instances)، ثم ينقسم بصمت |
| في مخزن مشترك (Redis) | عدّة (count) واحدة حقيقية عبر كل النسخ (all instances)، وتنجو من النشر (deploy) ✓ |

في اللحظة التي تشغّل فيها أكثر من نسخة (instance) من تطبيقك — وكل نظام إنتاجي (production system) حقيقي يفعل —
يكفّ العدّاد (counter) في الذاكرة (in-memory) عن كونه حدًّا (limit). يصير اقتراحًا تتجاهله كل نسخة (instance) على حدة. (هذا
الفخّ نفسه يعود في الدرس (lesson) 10.1 بوصفه سبب قتل حالة العملية (process state) للتوسع الأفقي (horizontal scaling).)

### 3. الترويسة (header) ادّعاء — قابلة للتزوير (forgeable) إن كان الأصل (origin) قابلًا للوصول مباشرة (reachable directly)

وهنا لسعة الذيل. `CF-Connecting-IP` مجرد ترويسة (header) يضيفها الـCDN. فإن استطاع مهاجم (attacker)
الوصول إلى **خادمك الأصلي (your origin server) مباشرة** — متجاوزًا الـCDN — أرسل تلك الترويسة (header) بنفسه بأي
قيمة يشاء، وزوّر «عنوان (address) عميل (client)» مختلفًا في كل طلب ليتفادى حدّك (limit) لكل IP (per-IP) كليًا.

فالترويسة (header) موثوقة فقط إن تحقق أمران: أن يكون الـCDN هو *الطريق الوحيد* إلى أصلك (your origin)
(دخول (ingress) عبر الـCDN حصرًا، مفروضًا عند الجدار الناري (firewall))، وأن **تجرّد (strips) حافتك (your edge) أي نسخة واردة (inbound copy)**
من الترويسة (header) قبل أن تضع نسختها. لا تثق بالترويسة إلا بعد أن تجعل تزويرها (forge it) مستحيلًا.
(مشكلة الترويسة (header) القابلة للتزوير (forgeable) هذه تعود في 5.4 درسًا (lesson) عامًا عن المدخلات (inputs) التي لم
تنتبه أنك تثق بها، ثم في 11.1 بوصفها دخولًا عبر الـCDN حصرًا (CDN-only origin ingress).)

### 4. افشل مفتوحًا (fail open) لا مغلقًا

إن تعذّر بلوغ مخزن العدّادات المشترك (Redis) لحظةً، ماذا يفعل المحدِّد (limiter) — يحظر
الجميع أم يمرّر الطلبات (requests) دون عدّ؟ بالنسبة لمحدِّد (limiter) *إساءة (abuse) عام*: **افشل مفتوحًا (fail open)**؛ فمحدِّدٌ
يفشل مغلقًا (fails closed) يحوّل ومضة Redis (Redis blip) إلى عطل (outage) كامل. المحدِّد (limiter) حاجزُ أمان (guardrail)، لا جدارٌ حامل (load-bearing wall)؛ فليتدهور (degrade)
إلى «بلا حدّ (limit) لحظةً» بدل «معطّل».

**لكن هناك استثناء مهم: محدِّدات المصادقة (auth limiters) تفشل *مغلقة*.** فالمحدِّد (limiter) الذي يقيّد (throttled) محاولات
الدخول (login attempts)، وتخمينات إعادة تعيين كلمة المرور (password-reset)، ومحاولات الرمز لمرة واحدة (one-time code)، هو دفاع (defense) ضد القوة
الغاشمة (Brute Force)، لا ميزة راحة. فإن فشل مفتوحًا (fail open)، صارت ومضة Redis (Redis blip) نافذةً مفتوحة
لحشو بيانات الاعتماد (credential stuffing)، في اللحظة التي تكون فيها أقل قدرة على الملاحظة. لذلك، عند أخطاء
المخزن (store)، يجب أن يرفض محدِّد الدخول (login limiter) أو الرمز (token) أو إعادة التعيين (يفشل مغلقًا (fails closed))، أو يتراجع
إلى حدّ (limit) **محلي** صارم داخل العملية (مثلًا بضع محاولات في الدقيقة لكل نسخة (instance))، كي لا يختفي
السقف (ceiling) بالكامل أبدًا. القاعدة: *محدِّدات الإساءة العامة (general abuse limiters) تفشل مفتوحة (fail open)؛ وأي شيء يحرس سرًّا (secret)
يفشل مغلقًا (fails closed).*

## 🎛️ وجّه وكيلك (Direct Your Agent)

‏Relay خلف CDN (من الوحدة (Module) 3). ومحدِّد معدله (its rate limiter)، إن وُجد، مربوط على الأرجح بمفتاح (key) خاطئ.
لنُصلحه كما فعلت الحادثة (incident).

1. **اكتشف على أي شيء يربط المحدِّد (limiter) فعلًا.**
   > *«أرني كيف يعرّف محدِّد معدل (rate limiter) Relay العميل (client). أهو عنوان المقبس (socket IP) أم ترويسة (header) من
   > الـCDN؟ إن كان عنوان المقبس (socket IP)، فاشرح ما يحدث لذلك المفتاح (key) ما إن يصل كل طلب عبر
   > الـCDN.»*
2. **اربط على عنوان العميل الحقيقي (real client IP).**
   > *«غيّر المحدِّد (limiter) ليربط على ترويسة عنوان العميل الحقيقي (real-client-IP header) من الـCDN
   > (`CF-Connecting-IP`، وعند غيابها `X-Forwarded-For`). وأرني مستخدمَين (users) مختلفَين
   > محاكَيين خلف الـCDN يحصلان على عدّتين مستقلتين (two independent counters) بدل مشاركة واحدة.»*
3. **انقل العدّادات (counters) إلى تخزين مشترك (shared storage) ودائم.**
   > *«انقل عدّادات (counters) تحديد المعدل (rate limiting) من ذاكرة العملية (process memory) إلى Redis كي تشارك كل النسخ (all instances) عدّة (count)
   > واحدة وتنجو من النشر (deploy). أثبته: ابلغ الحد (limit)، ثم انشر من جديد (redeploy)، وأرني أن العدّة (count) لم
   > تُصفَّر.»*
4. **أغلق ثغرة التزوير (forgery hole).**
   > *«اجعل Relay يجرّد أي نسخة واردة (inbound copy) من ترويسة عنوان العميل الحقيقي (real-client-IP header) عند الحافة (edge) قبل
   > الوثوق بها، ووثّق أن الأصل (origin) يجب ألا يقبل حركةً إلا من الـCDN. وأرني طلبًا (request) يزوّر (forges)
   > الترويسة (header) يجري تجاهله.»*
5. **افشل مفتوحًا (fail open) عند أخطاء المخزن (store errors).**
   > *«إن تعذّر بلوغ Redis، فليسمح المحدِّد (limiter) بالطلب (فشل مفتوح (fail open)) ويسجّله، لا أن يلقي
   > 429 على الجميع. حاكِ تعطّل Redis (Redis down) وأرني الطلبات (requests) ما زالت تنجح.»*

الختام (Finish): *«أودع (commit) برسالة `05-2-cdn-rate-limit`.»*

> 🔧 **تحت الغطاء (Under the hood)** (اختياري (optional)): مع `express-rate-limit`، اجعل `keyGenerator` على
> ترويسة عنوان العميل (client-IP header) الموثوقة ومرّر `store` من Redis (مثل `rate-limit-redis`) مع
> `passOnStoreError: true`؛ وعند الوسيط (proxy)، ألغِ أي `X-Forwarded-For`/`CF-Connecting-IP`
> يرسله العميل (client) قبل إضافة نسختك.

## ✅ تحقق منه (Verify It)

- [ ] رأيت محدِّد Relay (Relay's limiter) قبل الإصلاح (fix) يجمع عدة (count) مستخدمين (users) في دلو (bucket) واحد لأنه ربط على عنوان (address)
      الـCDN.
- [ ] مستخدمان مختلفان خلف الـCDN يحصلان الآن على عدّتين مستقلتين (two independent counters).
- [ ] بلغت الحد (limit)، ونشرت من جديد، ونجت العدّة (count) — دليلًا على أنها في Redis لا في ذاكرة
      العملية.
- [ ] طلبٌ يزوّر (forges) ترويسة عنوان العميل (client-IP header) يُتجاهَل، وتستطيع شرح لماذا يجعل الدخول عبر
      الـCDN حصرًا الترويسة (header) موثوقة.
- [ ] تستطيع إعادة رواية حادثة (incident) الدلو المشترك (shared-bucket) و429 وتسمية الخطأين: المفتاح (key) الخاطئ
      (المقبس (socket) مقابل الترويسة (header)) والتخزين الخاطئ (الذاكرة (memory) مقابل Redis).

## 🧾 بطاقة الخلاصة (Recap card)

- خلف CDN، عنوان المقبس (socket IP) هو عنوان (address) الـCDN — اربط الحدود (limits) على ترويسة عنوان العميل الحقيقي (real-client-IP header).
- عدّادات (counters) الذاكرة (memory) تُصفَّر مع النشر (deploy) ولا تُشارَك عبر النسخ (instances)؛ استخدم مخزنًا مشتركًا (Redis).
- ترويسة عنوان العميل (client-IP header) قابلة للتزوير (forgeable) ما لم يكن الأصل (origin) عبر الـCDN حصرًا وتُجرَّد (strips) النسخ الواردة (inbound copies).
- افشل مفتوحًا (fail open): محدِّدٌ (limiter) يفشل مغلقًا (fails closed) يحوّل ومضة مخزن (store blip) إلى عطل (outage).
- «عنوان العميل (client IP)» دائمًا ادّعاءٌ مضبوط ما إن يجلس شيء أمام تطبيقك.

## 📚 المراجع ومزيد من القراءة (References & further wandering)

- ‏MDN: ترويستا **`X-Forwarded-For`** و**`Forwarded`** — ما تمرّره الوسائط (proxies) فعلًا وكيف تقرؤه.
- وثائق (docs) Cloudflare: **«استعادة عناوين الزوّار الأصلية (Restoring original visitor IPs)»** (`CF-Connecting-IP`) — الترويسة (header) نفسها من هذه الحادثة (incident).
- وثائق (docs) `express-rate-limit` — `keyGenerator` والمخازن الخارجية (external stores) ومزالق الثقة بالوسيط (trust-proxy pitfalls).
- كتاب Google SRE: **«التعامل مع الحِمل الزائد (Handling Overload)»** و**«معالجة الأعطال المتتالية (Addressing Cascading Failures)»** — لماذا يجب أن تتدهور (degrade) الحواجز (guardrails) لا أن تفشل مغلقة (fail closed).
- ورقة (cheat sheet) OWASP **«حجب الخدمة (denial of service)»** — تحديد المعدل (rate limiting) دفاعًا (defense) وأنماط فشله (failure modes).

---

# 5.3 — مصادقة تستطيع تشغيلها (Auth That You Can Operate)

## 🔥 قصة من الميدان (The War Story)

عمل نظام المصادقة (auth system) في كل اختبار (test). نجح تسجيل الدخول (login)، وثبتت الجلسات (sessions)، وتحقّقت الرموز (tokens). ثم
طلب مستخدم (user) إعادة تعيين كلمة المرور (password reset) في الإنتاج (production) — فكان الرابط (URL) في الرسالة يشير إلى
`http://localhost:3000`. وهو عنوان (address) يعني «هذا الجهاز بالذات»، عديم الفائدة لأي أحد
سوى المطوّر (developer). فكل رسالة إعادة تعيين (reset email) أرسلها المنتج (product) كانت طريقًا مسدودًا.

كان الكود (code) بريء المظهر. بُني رابط إعادة التعيين (reset link) من متغير بيئة (environment variable) — سمّه `CLIENT_URL`.
وكان `CLIENT_URL` *مضبوطًا* في الإنتاج (production). لكن وظيفته الحقيقية **إعداد (configuration) CORS**: إخبار
المتصفح (browser) أي أصلٍ (origin) مسموح له باستدعاء الـAPI. ولهذا الغرض، في هذا النشر (deployment)، كانت قيمته
عنوانًا (address) محليًا. متغير (variable) واحد يخدم بهدوء **جمهورين (Audiences)** مختلفين تمامًا —
سياسة أمان (security policy) المتصفح (browser)، والإنسان الذي ينقر رابطًا في رسالة — والقيمة الصحيحة لأحدهما
قمامة للآخر.

لم يكتب أحد خطأً. أعاد أحدهم استعمال متغير (variable) موجود سلفًا لأنه «يحتوي رابطًا». وكان
الإصلاح (fix) إعطاء الروابط (links) الموجّهة للمستخدم (user) متغيرها (its own variable) الخاص بوظيفة واحدة — `PUBLIC_SITE_URL`
— وتدوين أي متغير (variable) يقرأ كل مستهلك (consumer).

**الدرس (lesson): لكل متغير بيئة (environment variable) *جمهور (audience)*. ومتغير (variable) واحد يخدم جمهورين (two audiences) سيكون خاطئًا لأحدهما في
النهاية — ولن تعرف حتى يعرف مستخدم (user) حقيقي.**

## 📐 المبدأ (The Principle)

للمصادقة (auth) نصفان: التعمية (cryptography) (محلولة غالبًا، اشترِها ولا تخترعها) و*التشغيل (operations)* (حيث تفشل
المنتجات الحقيقية). هذا الدرس (lesson) عن مصادقة (auth) تشغّلها دون أن تُستدعى (paged) إليها.

### 1. أين يعيش الرمز (token): كوكيز httpOnly (httpOnly cookies) لا localStorage

حين يسجّل المستخدم (user) الدخول، يعيد الخادم (server) رمزًا (token) يثبت هويته — عادةً **رمز JWT مميز
(Token)**: كتلة موقّعة (signed blob) يتحقق منها الخادم (server) دون قراءة قاعدة البيانات (database). والسؤال الذي
يقرر موقفك الأمني (security posture) هو *أين يحفظه المتصفح (browser)*.

| التخزين | مقروء من JavaScript؟ | العاقبة |
|---|---|---|
| `localStorage` | نعم | أي سكربت مُحقَن (injected script) (ثغرة XSS (XSS bug)، تبعية (dependency) سيئة) يسرق الرمز (token) |
| كوكي (cookie) httpOnly | **لا** | لا يقرؤه السكربت (script)؛ والمتصفح (browser) يرفقه تلقائيًا |

الرموز (tokens) في `localStorage` رائحة سيئة (smell): بيت القصيد أن سرقة رمز الجلسة (session token) نهاية اللعبة،
و`localStorage` يسلّمه لأي سكربت (script) يعمل على صفحتك. ضعه في **كوكي httpOnly (httpOnly cookie)** — غير مرئي
لـJavaScript، يُرسَل تلقائيًا، مقرونًا برايتي (flags) `Secure` و`SameSite`.

### 2. رموز تحديث دوّارة (rotating refresh tokens) مع كشف إعادة الاستخدام (reuse detection)

تريد رموز وصول (access tokens) قصيرة العمر (short-lived) (كي ينتهي المسروق سريعًا) *و*مستخدمين (users) يظلون مسجّلين
أسابيع. والجواب رمزان: **رمز وصول (Access Token)** قصير العمر (short-lived) و**رمز تحديث (Refresh
Token)** طويل العمر (long-lived) يسكّ رموز وصول (access tokens) جديدة.

والترقية التشغيلية **التدوير (rotation) مع كشف إعادة الاستخدام (reuse detection)**: كلما استُعمل رمز التحديث (refresh token)،
أُبطل (invalidated) وصُدر جديد. فإن قُدّم رمزٌ (token) *قديمٌ سبق تدويره* مرة أخرى، فذلك يعني أن طرفين
يحملانه — المستخدم (user) الحقيقي واللص (thief). فيحرق النظام السلسلة (chain) كلها ويفرض تسجيل دخول جديد (fresh login).

```mermaid
sequenceDiagram
    autonumber
    participant S as الخادم
    participant U as المستخدم
    U->>S: تحديث بالرمز R1
    S-->>U: وصول جديد + تدوير ← R2 (R1 ميت الآن)
    Note over U,S: لاحقًا، يعيد لصٌّ تشغيل R1 المسروق
    U->>S: تحديث بالرمز R1 (مُدوَّر سلفًا)
    S-->>U: كُشفت إعادة الاستخدام ← احرق السلسلة، افرض دخولًا جديدًا
```

أنت لا تمنع السرقة — بل تجعلها *قابلة للكشف ومحدودة (detectable and bounded)*. الرمز (token) المسروق يشتري للمهاجم (attacker)
دقائق لا شهورًا، واستعماله يطلق إنذارًا (alarm).

### 3. المصادقة الثنائية (2FA)

كلمة المرور (password) عامل (factor) واحد: شيء تعرفه. تضيف المصادقة الثنائية (2FA) عاملًا ثانيًا (a second factor): شيء
*تملكه* (رمز (token) من تطبيق مصادقة (authenticator app)، مفتاح عتادي (hardware key)). وهي أعلى ترقية أمان للحساب (account-security upgrade) رافعةً، لأنها
تهزم الهجوم الأشيع — كلمات المرور (passwords) المسروقة أو المعاد استعمالها. قدّمها (تطبيقات TOTP،
رموز احتياطية (backup codes))؛ وافرضها على المشرفين (admins).

### 4. لكل متغير بيئة (environment variable) جمهور (audience)

عودةً إلى القصة، معمّمة. لقيم الإعداد (configuration values) *مستهلكون*، ويحتاج المستهلكون (consumers) المختلفون قيمًا
مختلفة. وإعادة استعمال متغير (variable) واحد عبر جماهير (audiences) هو مكافئ الإعداد (config) لإعادة Knight Capital
استعمال راية (flag) قديمة بمعنى جديد.

| المتغير (variable) | الجمهور (audience) | مثال القيمة الصحيحة |
|---|---|---|
| `CLIENT_URL` | ‏CORS: أي أصلٍ (which origin) يستدعي الـAPI | أصل تطبيق المتصفح (the browser app's origin) |
| `PUBLIC_SITE_URL` | روابط (URLs) ينقرها البشر في الرسائل | `https://relay.app` |
| `API_BASE_URL` | عميل (client) الموبايل (mobile)/الويب المستدعي للـAPI | `https://api.relay.app` |

قبل أن تعيد استعمال متغير (variable) «لأنه يحتوي رابطًا»، اسأل: *من يقرأ هذا، وهل يحتاجون كلهم
القيمة نفسها؟* (هذه الحادثة (incident) نفسها مشكلة بريد (email) أيضًا — تعود في الدرس (lesson) 5.5، لأن رابط
إعادة تعيين (reset) إلى العدم فشلُ بريد (email) وفشلُ مصادقة (auth) معًا.)

## 🎛️ وجّه وكيلك (Direct Your Agent)

يحتاج Relay إلى جلسات (sessions) تشغّلها وإعدادٍ (config) تدقّقه.

1. **انقل الرموز (tokens) إلى كوكيز httpOnly (httpOnly cookies).**
   > *«أكّد أين يخزّن Relay رمز (token) مصادقته في المتصفح (browser). إن كان في localStorage، فانقله
   > إلى كوكي httpOnly (httpOnly cookie) وSecure وSameSite وأرني أن الرمز (token) لم يعد قابلًا للوصول (access) من
   > JavaScript في الطرفية (console).»*
2. **أضف رموز تحديث دوّارة (rotating refresh tokens) مع كشف إعادة الاستخدام (reuse detection).**
   > *«أعطِ Relay رموز وصول (access tokens) قصيرة العمر (short-lived) مع رموز تحديث (refresh tokens) طويلة العمر (long-lived) تتدوّر مع كل
   > استعمال. فإن قُدّم رمز تحديث (refresh token) مُدوَّر سلفًا مرة أخرى، أبطل السلسلة (chain) كاملة وافرض
   > دخولًا جديدًا (re-login). وأظهِر كشف إعادة الاستخدام (reuse detection) يعمل.»*
3. **قدّم المصادقة الثنائية (2FA) وافرضها على المشرفين (admins).**
   > *«أضف مصادقة ثنائية (two-factor authentication) قائمة على TOTP مع رموز احتياطية (backup codes). واجعلها اختيارية
   > للمستخدمين (users) وإلزامية لحسابات المشرفين (admin accounts). وأرني دخول مشرف (admin) محجوبًا حتى يُقدَّم العامل (factor)
   > الثاني.»*
4. **ابنِ جدول جمهور المتغيرات (env-var audience table).**
   > *«اسرد كل متغير بيئة (environment variable) يقرؤه Relay، ولكل واحد: أي مسارات كود (code paths) تستهلكه وأي جمهور (audience)
   > تخدمه (سياسة CORS، روابط (URLs) للمستخدم (user)، أساس الـAPI، داخلي (internal)). واعلم أي متغير (variable) واحد
   > يقرؤه جمهوران مختلفان — فذلك خطأ رابط إعادة التعيين (reset link) إلى localhost بانتظاره.»*
5. **اقسم المتغير (variable) المعاد استعماله.**
   > *«أعطِ الروابط (links) الموجّهة للمستخدم (user) متغيرها (its own variable) الخاص (`PUBLIC_SITE_URL`) منفصلًا عن
   > متغير أصل CORS (CORS origin variable). وأظهِر رسالة إعادة تعيين (reset email) مبنية بالرابط (URL) العام الصحيح.»*

الختام (Finish): *«أودع (commit) برسالة `05-3-operable-auth`.»*

> 🔧 **تحت الغطاء (Under the hood)** (اختياري (optional)): رمز الوصول (access token) ~15 دقيقة، والتحديث ~30–180 يومًا منزلقًا (sliding)؛
> خزّن معرّف (id) *عائلة (family)* رمز تحديث (refresh token) وjti دوّارًا؛ وعند إعادة تشغيل jti متقاعد (retired)، احذف
> العائلة. الكوكيز (cookies): `HttpOnly; Secure; SameSite=Lax`. TOTP عبر أي مكتبة مصادقة (authenticator library)
> معيارية؛ خزّن الرموز الاحتياطية (backup codes) مجزّأة (hashed).

### مطالبة المراجعة الأمنية (Security review prompt)

> *«عدّد كل متغير بيئة (environment variable) يقرؤه هذا الكود (code) وكل موضع يُستهلك فيه. ولكل واحد، سمِّ الجمهور (audience).
> ثم أجب: هل يخدم أي متغير (variable) جمهورين (two audiences) قد يحتاجان قيمتين مختلفتين في الإنتاج (production)؟»*

## ✅ تحقق منه (Verify It)

- [ ] رمز (token) مصادقة (auth) Relay في كوكي httpOnly (httpOnly cookie) — حاولت قراءته من طرفية المتصفح (browser console) فلم تستطع.
- [ ] رأيت كشف إعادة استخدام (reuse detection) رمز التحديث (refresh token) يحرق سلسلة (chain) ويفرض دخولًا جديدًا (re-login).
- [ ] لا يستطيع حساب مشرف (admin account) تسجيل الدخول (login) دون العامل الثاني (second factor).
- [ ] جدول جمهور المتغيرات (env-var audience table) موجود ويعلّم أي متغير (variable) بجمهورين (two audiences).
- [ ] تستطيع إعادة رواية حادثة (incident) رابط إعادة التعيين (reset link) إلى localhost وشرح معنى «الجمهور (audience)»
      لـ`CLIENT_URL` مقابل `PUBLIC_SITE_URL`.

## 🧾 بطاقة الخلاصة (Recap card)

- الرموز (tokens) في كوكي httpOnly (httpOnly cookie) لا localStorage — رمزٌ (token) يقرؤه أي سكربت (script) مسروقٌ سلفًا.
- رموز وصول (access tokens) قصيرة + رموز تحديث دوّارة (rotating refresh tokens) مع كشف إعادة الاستخدام (reuse detection): السرقة تصبح قابلة للكشف ومحدودة (detectable and bounded).
- المصادقة الثنائية (2FA) أعلى ترقيات الحساب (account) رافعةً؛ افرضها على المشرفين (admins).
- لكل متغير بيئة (environment variable) جمهور (audience)؛ ومتغير (variable) يخدم جمهورين (two audiences) سيكون خاطئًا لأحدهما.
- الجزء الصعب في المصادقة (auth) ليس التعمية (cryptography) — بل تشغيلها دون أن تستدعي الإنذار (alarm) على نفسك.

## 📚 المراجع ومزيد من القراءة (References & further wandering)

- ورقتا (cheat sheets) OWASP **«إدارة الجلسات (Session Management)»** و**«المصادقة (auth)»** — المرجع التشغيلي لهذا الدرس (lesson) تحديدًا.
- ‏MDN: **`Set-Cookie`** — `HttpOnly` و`Secure` و`SameSite` بوضوح.
- ‏RFC 6749 (**OAuth 2.0**) وRFC 7519 (**JWT**) — المعياران (specs) خلف الرموز (tokens)، حين تريد الحقيقة الأساس.
- مدونات Auth0/Okta الهندسية عن **تدوير رموز التحديث (refresh token rotation) وكشف إعادة الاستخدام (reuse detection)** — النمط بتفصيل الإنتاج (production).
- ورقة (cheat sheet) OWASP **«المصادقة متعددة العوامل (Multifactor Authentication)»** — TOTP والرموز الاحتياطية (backup codes) ومسارات الاسترداد (recovery flows).

---

# 5.4 — مدخلات لم تدرك أنك تثق بها (Input You Didn't Realize You Were Trusting)

## 🔥 قصة من الميدان (The War Story)

أظهر تدقيق أمني (security audit) لأحد التطبيقات ثلاثة نتائج (findings) تشترك في عمود فقري: **الكود (code) يثق بشيء
يتحكم فيه العميل (client)، دون أن ينتبه أنه يثق به.**

الأول وسيطُ بثٍّ للوسائط (media-streaming proxy). لتشغيل الصوت، كان التطبيق (app) يجلب الملف عبر نقطة نهاية (endpoint) على
الخادم (server) تتبع عمليات إعادة التوجيه (redirects) وتوقّع (signs) الرابط (URL) النهائي. بريءٌ بما يكفي — حتى تلاحظ
أنه يتبع إعادة التوجيه (redirect) *إلى أي مكان*، ويوقّع ما يهبط عليه. فمهاجمٌ (attacker) يستطيع التأثير في
وجهة إعادة التوجيه (redirect target) يجعل الخادم (server) يجلب ويوقّع عنوانًا (address) **داخليًا (internal)**: نقطة بيانات وصف (metadata endpoint)
المزوّد السحابي (cloud provider) (التي تسلّم بيانات اعتماد (credentials))، أو Redis المحلي، أو لوحة مشرف (admin panel) لا تُبلَغ
إلا من الداخل. هذا **تزوير الطلب من جهة الخادم (SSRF)**: تحوّل الخادم (server) إلى نائبٍ
مخدوع (confused deputy) يرسل طلبات (requests) نيابةً عن المهاجم (attacker)، من داخل شبكتك الموثوقة (trusted network). والمفتاح السري (signing secret) الذي
يُفترض أن يحمي تلك الروابط (links) كان به عيب هادئ: إن لم يُضبط، **رجع (fell back) بصمت** — أولًا إلى
مفتاح (key) آخر، وأخيرًا إلى نصٍّ برمجيٍّ ثابتٍ (hardcoded literal) للمطوّر (developer) في المصدر (source). فعُطّلت البِنية الأمنية (security primitive)
بقيمة افتراضية (default) ولم يعلم أحد.

الثاني نقطةُ قياسٍ عن بُعد (telemetry endpoint) مجهولة — نبضٌ (heartbeat) لـ«نشاط حي» بلا مصادقة (auth) ولا تحديد معدل (rate limit) ولا
مخطط (schema) ولا حدود طول (length caps)، مربوطٌ بمعرّف جلسة (session ID) يختاره العميل (client). يستطيع أي أحد استدعاءها مليون
مرة، وتضخيم أرقام الاستخدام، وتلويث تصنيفات (rankings) «الرائج (trending)» التي تغذّيها تلك الأرقام،
وإغراق المخزن (datastore). فالمقاييس (metrics) التي تقود قرارات المنتج (product) كانت **قابلة للكتابة من المهاجم (attacker-writable)**.

الثالث إدراكُ الدرس (lesson) 5.2 من الجهة الأمنية: ترويسة (header) «عنوان العميل الحقيقي (real client IP)» التي يثق بها
المحدِّد (rate limiter) **قابلة للتزوير (forgeable)** إن استطاع أحد بلوغ الأصل (origin) مباشرة. مدخلٌ (input) موثوق يستطيع المهاجم (attacker)
ضبطه.

**الدرس (lesson): اصنع جردًا (inventory) لكل مدخل (input) تثق به مما يتحكم فيه العميل (client) — الروابط (links) التي تجلبها،
والترويسات (headers) التي تقرؤها، والمقاييس (metrics) التي تصنّف بها — لأن كل واحد سطحُ هجومٍ (attack surface) لم تصنّفه
كذلك.**

## 📐 المبدأ (The Principle)

### 1. جرد المدخلات العدائية (adversarial-input inventory)

يحرس معظم المطوّرين المدخلات (inputs) *البديهية* — حقول النموذج (form fields)، جسم الطلب (request body). أما الخطيرة فهي
المدخلات (inputs) التي لا تعدّها مدخلات (input).

```mermaid
flowchart TD
    C["أي شيء يستطيع العميل التأثير فيه"] --> U["روابط تجلبها<br/>← SSRF"]
    C --> H["ترويسات تقرؤها<br/>← هوية مزوّرة"]
    C --> M["مقاييس تعدّها/تصنّفها<br/>← قرارات مسمومة"]
    C --> F["أسماء ملفات، إعادة توجيه،<br/>معرّفات تتبعها ← عبور"]
    U --> G["مرّرها عبر دالة جلب<br/>واحدة محميّة من SSRF"]
    H --> G2["لا تثق بها إلا بعد<br/>أن تجعل التزوير مستحيلًا"]
    M --> G3["عامل مدخلات التصنيف<br/>كعدائية: حُدَّ، تحقّق، صادِق"]
```

لكل معالِج (handler)، اطرح السؤال الثابت: **«اسرد كل موضع يثق فيه هذا المعالِج بشيء يتحكم فيه
العميل (client).»** روابط (URLs)، ترويسات (headers)، معرّفات (IDs)، عدّات، وجهات إعادة توجيه (redirect targets). كل واحد سطرٌ في جردك (your inventory).

### 2. SSRF: الخادم (server) نائبًا مخدوعًا (confused deputy)

يجلس خادمك *داخل* شبكتك الموثوقة (your trusted network). يستطيع بلوغ ما لا يبلغه العموم — نقاط الوصف (metadata endpoints)،
الخدمات الداخلية (internal services)، قواعد البيانات (databases). وثغرة SSRF (SSRF bug) تدع المهاجم (attacker) يستعير ذلك الموقع: لا
يستطيع بلوغ `169.254.169.254` (عنوان الوصف السحابي (cloud metadata address))، لكن خادمك يستطيع، فيجعل خادمك
يفعلها.

والدفاع (defense) دالةُ جلبٍ (fetch function) واحدة محميّة يمرّ *كل* طلب صادر (outbound request) عبرها — واحدةٌ تحلّ الوجهة، وترفض
نطاقات IP الخاصة/الداخلية (private/internal)، وتعيد الفحص **عند كل قفزة إعادة توجيه (redirect hop)** (فالرابط (URL) العام قد
يعيد التوجيه إلى داخلي (internal) بـ302). والكلمة الحاسمة *كل*: البِنية الأمنية (security primitive) لا تنفع إلا إن
استعملها كل مسار كود (code path). فجلبٌ خام (raw fetch) واحد يتجاوز الحارس هو الثغرة (hole) كلها.

### 3. مفتاحٌ (key) يرجع افتراضيًا مفتاحٌ مطفأ (secret that's off)

الرجوع الصامت (silent fallback) للمفتاح السري (signing secret) درسٌ (lesson) بذاته. يجب أن **تفشل الأسرار (secrets) مغلقة (fail closed)**: إن لم يُضبط
المفتاح (key)، *يرفض الفعل العمل* — لا أن يستبدل بصمت قيمة أضعف ويمضي. فالرجوع إلى نصٍّ
للمطوّر (developer) يعني أن الحماية تبدو حاضرة في الكود (code) وغائبة في الواقع. (هذا تمهيدٌ لحجة 5.7
كاملة: لا تدع سرًّا (secret) يتدهور (degrade) إلى قيمة افتراضية (default) أبدًا.)

### 4. البيانات التي تقود القرارات مدخلٌ عدائي (adversarial input)

إن أثّر رقمٌ في قرار منتج (product) — ما «الرائج (trending)»، من «الأنشط»، أي محتوى يُروَّج — فذلك الرقم
مدخلٌ (input) يريد المهاجمون (attackers) التحكم فيه. ونقطةُ كتابةٍ مجهولةٌ بلا حدٍّ (limit) ولا تحقّق تغذّي
تصنيفًا (ranking) رافعةٌ مجانية على منتجك (your product). مدخلات (input) التصنيف تحتاج مصادقةً (auth) أو على الأقل حدودًا (limits) لكل
IP، وحدود طول (length caps) ومخطط (schema)، وحدود عدديّة (cardinality limits). (ثغرة القياس (telemetry hole) هذه نفسها تعود في 7.5 فشلًا
*تحليليًا (analytics)* وفي 10.4 حضورًا لحظيًا (realtime presence) يجب أن تحدّه.)

**اقرن ذلك بحالة عامة.** كان اختراق (breach) Capital One عام 2019 — أكثر من 100 مليون سجل (records) —
في جوهره SSRF: جدارٌ ناريٌ مضبوطٌ خطأً (misconfigured firewall) سمح لمهاجم (attacker) ببلوغ نقطة الوصف السحابي (cloud metadata endpoint) عبر طلب من
جهة الخادم (server) ونهب بيانات الاعتماد (credentials). الشكل نفسه تمامًا كوسيط الوسائط (media proxy)، بأثرٍ على مستوى
دولة. SSRF ليست غريبة؛ بل من أشد فئات (categories) «لم أعرف أني أثق بذلك» ضررًا.

## 🎛️ وجّه وكيلك (Direct Your Agent)

لدى Relay نقاط نهاية مجهولة (anonymous endpoints) وهو يجلب روابط (URLs). لنُنمذج تهديد (threat-model) المدخلات (inputs) التي يثق بها دون
انتباه.

1. **خذ جرد المدخلات العدائية (adversarial inputs).**
   > *«لكل نقطة نهاية مجهولة (anonymous endpoint) في Relay، اسرد كل قيمة يتحكم فيها العميل (client) ثم نتصرف بناءً
   > عليها: روابط (URLs) نجلبها، ترويسات (headers) نقرؤها للهوية (identity)، معرّفات (IDs) نبحث عنها، عدّات نزيدها،
   > وجهات إعادة توجيه (redirect targets) نتبعها. هذا جرد مدخلاتنا العدائية (adversarial-input inventory) — أرِه جدولًا.»*
2. **مرّر كل الجلب الصادر (outbound fetches) عبر دالة واحدة محميّة.**
   > *«جد كل موضع يرسل فيه Relay طلبًا صادرًا (outbound request). مرّرها كلها عبر `safeFetch` واحدة
   > ترفض نطاقات IP الخاصة/الداخلية (private/internal IP ranges) وتعيد فحص الوجهة عند كل قفزة إعادة توجيه (redirect hop). وأرني
   > محاولة جلب عنوان (address) داخلي (كنقطة الوصف (metadata endpoint) أو localhost) تُرفَض.»*
3. **اجعل المفتاح السري (signing secret) يفشل مغلقًا (fails closed).**
   > *«جد أي سرٍّ (secret) في Relay يرجع بصمت إلى قيمة أخرى أو نصٍّ افتراضي حين لا يُضبط.
   > غيّره ليرفض الإقلاع (أو يرفض الفعل) إن كان السر (secret) مفقودًا. وأرني التطبيق (app) يرفض
   > بدلًا من العمل بقيمة مطوّر افتراضية (dev default).»*
4. **حصّن نقطة القياس المجهولة (anonymous telemetry endpoint).**
   > *«نقطة النشاط/النبض (activity/heartbeat endpoint) في Relay: أضف حدودًا (limits) لكل IP (per-IP)، ومخططًا (schema) صارمًا بحدود طول (length caps)،
   > وحدًّا (limit) لعدد الجلسات المميزة (distinct sessions) التي تتتبعها. وأرني طوفانًا (flood) من أحداث (events) مزوّرة (forged) يُرفَض
   > بدلًا من تضخيم العدّات.»*
5. **أغلق ثغرة (hole) الترويسة (header) القابلة للتزوير (forgeable) من 5.2.**
   > *«أكّد أن ترويسة عنوان العميل الحقيقي (real-client-IP header) لا يمكن تزويرها (forge it): الأصل (origin) يقبل حركة (traffic) الـCDN
   > حصرًا، والنسخ الواردة (inbound copies) من الترويسة (header) تُجرَّد (strips) عند الحافة (edge).»*

الختام (Finish): *«أودع (commit) برسالة `05-4-trusted-input`.»*

> 🔧 **تحت الغطاء (Under the hood)** (اختياري (optional)): `safeFetch` تحلّ DNS، وترفض نطاقات RFC 1918
> والاسترجاع (loopback) والرابط المحلي (link-local) و`169.254.169.254`، وتضبط `redirect: 'manual'` وتعيد
> التحقق من كل `Location`؛ والأسرار (secrets) تُقرأ عبر `requireEnv()` ترمي عند الغياب لا
> `?? 'dev-secret'`؛ والقياس (telemetry) مُتحقَّق منه بمدقّق مخطط (schema validator) وحدٍّ (limit) لكل IP (per-IP) قائم على `INCR`.

### المطالبة الثابتة (Standing prompt)

> *«راجع هذا المعالِج (handler) كمهاجم (as an attacker): اسرد كل مدخل (input) أتحكم فيه ثم تتصرف بناءً عليه، ولكل واحد،
> ما الذي أستطيع بلوغه أو تزويره أو حقنه (inject) أو استنزافه (exhaust).»*

## ✅ تحقق منه (Verify It)

- [ ] جرد المدخلات العدائية (adversarial-input inventory) موجود لنقاط Relay المجهولة (Relay's anonymous endpoints) — روابط (URLs)، ترويسات (headers)، معرّفات (IDs)،
      عدّات، إعادة توجيه (redirect).
- [ ] كل جلب صادر (outbound fetch) يمرّ عبر دالة واحدة محميّة، ورأيتها ترفض عنوانًا (address) داخليًا (internal).
- [ ] مفتاح توقيع (signing secret) مفقود يجعل Relay يرفض العمل — بلا رجوع صامت (silent fallback).
- [ ] طوفانٌ (flood) من أحداث قياس مزوّرة (forged telemetry events) يُرفَض بدلًا من تضخيم الأرقام.
- [ ] تستطيع إعادة رواية نتيجة (finding) وسيط SSRF (SSRF proxy) وتسمية المدخلات (inputs) الثلاثة التي كان التطبيق (app)
      يثق بها دون إدراك (وجهة إعادة التوجيه (redirect target)، المفتاح (key) المفقود، معرّف الجلسة (session ID) الذي
      يختاره العميل (client)).

## 🧾 بطاقة الخلاصة (Recap card)

- احصر كل مدخل (input) يتحكم فيه العميل (client): روابط (URLs) تجلبها، ترويسات (headers) تقرؤها، مقاييس (metrics) تصنّف بها.
- SSRF يحوّل خادمك إلى نائبٍ مخدوع (confused deputy) داخل شبكتك — احرس كل جلب صادر (outbound fetch)، وأعِد فحص كل إعادة توجيه (redirect).
- البِنية الأمنية (security primitive) تنفع فقط إن استعملها *كل* مسار كود (code path) — جلبٌ خام (raw fetch) واحد هو الثغرة (hole) كلها.
- يجب أن تفشل الأسرار (secrets) مغلقة؛ فالرجوع الصامت (silent fallback) إلى قيمة افتراضية (default) حمايةٌ غير موجودة.
- الأرقام التي تقود قرارات المنتج (product) مدخلٌ عدائي (adversarial input) — حُدّها (limit) وتحقّق منها وصادِقها.

## 📚 المراجع ومزيد من القراءة (References & further wandering)

- ورقة (cheat sheet) OWASP **«الوقاية من تزوير الطلب من جهة الخادم (Server Side Request Forgery Prevention)»** — نمط الجلب المحمي (guarded-fetch) بالتفصيل.
- تغطية Krebs on Security وتحليلات (postmortems) **اختراق (breach) Capital One 2019** — SSRF إلى الوصف (metadata) بحجم 100 مليون سجل (million records).
- **قائمة OWASP لأمان الـAPI العشرة (OWASP API Security Top 10)** — «الاستهلاك غير المقيّد للموارد (Unrestricted Resource Consumption)» و«الوصول المعطوب على مستوى الكائن (Broken Object Level Authorization)» يقابلان نتيجة (finding) القياس (telemetry).
- أكاديمية PortSwigger لأمن الويب، **مختبرات (labs) SSRF** — عملية، مجانية، وقد أنجزها مهاجمك (your attacker).
- وثائق (docs) خدمة الوصف السحابي (AWS IMDSv2 / GCP metadata) — لماذا `169.254.169.254` جوهرةُ أهداف SSRF.

---

# 5.5 — البريد بنية تحتية إنتاجية (Email Is Production Infrastructure)

## 🔥 قصة من الميدان (The War Story)

ثلاثة أعطال بريد (email failures)، منصةٌ (platform) واحدة، ولم يبدُ أيٌّ منها مشكلة بريد (email) بادئ الأمر.

الأول: كان البريد الصادر (outbound mail) **يفشل بصمت**. عملت أداة النشرة (newsletter tool) ولم ترسل شيئًا؛ واختفت
الرسائل المعامَلاتية (transactional emails). كان مزوّد SMTP (SMTP provider) يرفض كل رسالة لأن **عنوان المُرسِل (From) لم
يكن صندوقًا مملوكًا (owned mailbox)** على الحساب (account) — يفرض المزوّدون ملكية المُرسِل (sender ownership) لمحاربة الانتحال (spoofing)،
وهذا العنوان (address) لم يكن مما يسمح الحساب (account) بالإرسال منه. وفوق ذلك خطأ توقيت (timing bug): قُرئ عنوان
المُرسِل **عند تحميل الوحدة (Module Load)**، قبل تعبئة الإعداد (config)، فرأى الكود (code) قيمة
فارغة وأرسل من لا شيء.

الثاني خطأُ رابط إعادة التعيين (reset link) إلى localhost من الدرس (lesson) 5.3 — رسائل إعادة تعيين (reset emails) مبنية
من متغير (environment variable) CORS، توجّه المستخدمين (users) إلى رابط لا يعني شيئًا خارج جهاز المطوّر (developer).

الثالث طوفان (flood) «bob» من الدرس (lesson) 5.1 — مهاجمٌ (attacker) يسجّل غرباء ليقصفهم برسائل تفعيل (verification emails)، محرقًا
**سمعة المُرسِل (sender reputation)** للمنصة (platform) أثرًا جانبيًا (side effect).

انظر إلى النمط: سياسة تسليم (deliverability policy)، وخطأ توقيت إعداد (config-timing bug)، وخطأ جمهور (audience) متغير (variable)، ومتجه إساءة (abuse vector) — كلها
«بريد» فقط بمعنى أن البريد (email) هو ما انكسر. **البريد ليس ميزة (feature) تستدعيها؛ بل بنية تحتية (infrastructure)
تشغّلها**، لها سمعة (reputation) وطبقة سياسة (policy layer) وسطح إساءة (abuse surface)، تمامًا كقاعدة بياناتك (database) أو CDN.

## 📐 المبدأ (The Principle)

### 1. البريد المعامَلاتي (transactional mail) مقابل التسويقي (marketing)

نوعان من البريد (email)، وظيفتان وأنماط فشل مختلفة.

| | معامَلاتي (transactional) | تسويقي (marketing) / نشرة (newsletter) |
|---|---|---|
| الغرض | فعل مستخدم (user) واحد ← رسالة واحدة (إعادة تعيين (reset)، إيصال (receipt)، تفعيل (verification)) | متلقّون (recipients) كثر، حملة (campaign) واحدة |
| التوقيت | فوري، شبه متزامن (synchronous) | مُجمَّع (batched)، في الخلفية (background) |
| ضرر الفشل | *ذلك* المستخدم (user) لا يستطيع إعادة التعيين (reset)/التفعيل (verification) | السمعة (reputation)، إلغاء الاشتراك (unsubscribes)، بلاغات السخام (spam complaints) |
| يجب أن يكون | سريعًا، موثوقًا، آمنًا | **متكافئ الأثر (idempotent)، مُزال التكرار (deduplicated)، مُقيَّدًا (throttled)** |

خلط النوعين هو كيف ترسل النشرة (newsletter) نفسها خمس مرات، أو تجعل إعادة تعيين (reset) كلمة مرور (password) تنتظر
خلف دفعة تسويقية (marketing batch).

### 2. سمعة المُرسِل (sender reputation) مورد مشترك قابل للتلف (shared, damageable resource)

يقيّم مزوّدو البريد (mail providers) نطاق إرسالك (sending domain). أرسل إلى أناس حقيقيين يريدون بريدك (your mail) فيصل إلى الوارد (inboxes)؛
أرسل سخامًا (spam) أو ارتدّ (bounce) كثيرًا أو تُعلَّم رسائلك مهملات (junk)، فتهبط درجتك — وحينها يذهب **كل**
بريدك (your mail)، بما فيه إعادات تعيين كلمة المرور (password resets) الحرجة، إلى المهملات (junk). السمعة (reputation) مشتركة عبر كل ما
ترسله وتتلفها أسوأ سلوكياتك. أحرقها هجوم «bob» عمدًا. وتحرقها نشرةٌ مهملة (careless newsletter) سهوًا.

```mermaid
flowchart RL
    A["رسائل تفعيل<br/>إلى غرباء (إساءة)"] --> R["سمعة<br/>المُرسِل"]
    B["نسبة ارتداد عالية<br/>(قائمة سيئة)"] --> R
    C["بلاغات سخام"] --> R
    R -->|"تهبط الدرجة"| D["كل البريد ← مهملات<br/>بما فيه إعادات تعيين كلمة المرور"]
```

حماية السمعة (reputation) هي لماذا العناوين المملوكة وسجلات المصادقة (SPF وDKIM وDMARC) وحدود (limits)
الإساءة (abuse) ليست ترفًا اختياريًا (optional) — بل ما يبقي بريدك (your mail) الحرج قابلًا للتسليم (deliverable).

**ملاحظة إذا كان مستخدموك في العالم العربي.** قابلية التسليم (deliverability) ليست واحدة في كل مكان، بل تختلف بحسب مزوّد صندوق البريد (inbox provider)، والمزيج في منطقتنا يعتمد بشدة (heavily) على Gmail إضافةً إلى صناديق إقليمية وصناديق مزوّدي الإنترنت (ISP)، حيث يسقط النطاق المُرسِل الجديد في السخام (Spam) بسرعة. لهذا نتيجتان عمليتان: (1) سجلات المصادقة (authentication records) الثلاثة أعلاه (SPF وDKIM وDMARC) ليست اختيارية هنا — أرسل بدونها وستُصنّف صناديق البريد (mailboxes) العربية بريدك (your mail) سخامًا من اليوم الأول بصمت؛ (2) إذا أرسلت محتوى عربيًا، فاجعل الرسالة نظيفة وثنائية اللغة فعلًا (عنوان جيد (good subject line)، وإلغاء اشتراك حقيقي، وبلا روابط مختصرة (link-shorteners))، لأن البريد (email) التسويقي (marketing) العربي يخضع لفلترة (filtering) صارمة. المزوّد الذي *تشتريه* (Resend أو SES أو Postmark) يتولى السباكة (plumbing) التقنية، لكن السمعة (reputation) تبقى مسؤوليتك في السوق الذي تُرسل إليه فعلًا.

### 3. مسارات التفعيل وإعادة التعيين (Verification and reset flows) أسطحٌ أمنية (security surfaces)

الروابط (links) في هذه الرسائل مفاتيح (keys). رابط إعادة التعيين (reset link) بيان اعتماد مؤقت (temporary credential)؛ فإن أشار إلى
مكان خاطئ (5.3)، أو سُجّل في مكانٍ بسياسة احتفاظ (retention policy) (مخزنُ تشخيصٍ (diagnostic store) يحفظ الروابط (links) الخام
نتيجةُ تدقيقٍ (audit finding) حقيقية)، أو أمكن طلبه بلا حدٍّ (limit) ضد غرباء (5.1)، فإن *البريد (email)* هو الثغرة (hole)
الأمنية (security bug). عامل مسارات (flows) إعادة التعيين (reset)/التفعيل (verification) بعناية نموذج تسجيل الدخول (login form) نفسه.

### 4. النشرات (newsletters) مهامٌ خلفية (background jobs) — فاجعلها متكافئة الأثر (idempotent)

نشرةٌ (newsletter) إلى 50 ألف شخص مهمةٌ خلفية (background job) (الوحدة (Module) 7.4، الوحدة 10.2)، والمهام الخلفية (background jobs)
تُعاد (retried) وتُقاطَع وتُشغَّل من جديد. فإن لم يكن الإرسال **متكافئ الأثر (Idempotent)** —
آمنًا للتشغيل مرتين — فإن انهيارًا (crash) في المنتصف وإعادةَ تشغيل يعني أن 25 ألفًا يتلقّونها
مرتين. والدفاعات (defenses): خطوةُ «طالبْ بهذا المتلقّي (recipient)» ذرّية (atomic) كي لا يرسل عاملان (workers) معًا للشخص نفسه،
وسجلٌّ دائم (durable record) لمن أُرسل إليه سلفًا، وتهدئةٌ (cooldown) لكل بريد (email) كي لا تُطلق الإعاداتُ مرتين.

## 🎛️ وجّه وكيلك (Direct Your Agent)

يرسل Relay بريدًا معامَلاتيًا (تفعيل (verification)، إعادة تعيين (reset)) ونشرةً (newsletter) واحدة. لنشغّل البريد (email) كبنية (infrastructure)
تحتية.

1. **عدّد كل مسار كود (code path) يرسل بريدًا (email).**
   > *«اسرد كل موضع في Relay يرسل بريدًا (email). ولكل واحد: ما الذي يطلقه، من يتلقّاه، ما
   > عنوان المُرسِل (From address)، وما تكلفته إن أطلقه مهاجم (attacker) مليون مرة.»*
2. **أصلح عنوان المُرسِل (From address) وتوقيته.**
   > *«اجعل كل البريد (email) يُرسَل من صندوق مملوك (owned mailbox) واحد على نطاق إرسالنا (our sending domain). اقرأ عنوان (address)
   > المُرسِل عند *وقت الإرسال (send time)* لا عند تحميل الوحدة (module load) — وأرني أنه ما زال صحيحًا بعد
   > إعداد (config) يُحمَّل متأخرًا. وأكّد ضبط SPF/DKIM/DMARC للنطاق.»*
3. **أعطِ الروابط (links) أساسها (base URL) الخاص.**
   > *«ابنِ كل رابط موجّه للمستخدم (user) في البريد (email) من `PUBLIC_SITE_URL` (الجمهور (audience) من 5.3)،
   > لا من متغير (variable) CORS أبدًا. وأرني رابط إعادة تعيين (reset link) يشير إلى الموقع العام الحقيقي.»*
4. **تهدئة (cooldown) وردود عامة (generic responses) على إعادة التعيين (reset)/التفعيل (verification).**
   > *«أضف تهدئةً (cooldown) لكل بريد (email) كي لا يُرسَل للعنوان (address) نفسه إعادةُ تعيين (reset) كل ثوانٍ، وأبقِ رد
   > نسيان كلمة المرور (forgot-password) عامًا. وأرني الطلب (request) السريع الثاني يُقيَّد (throttled).»*
5. **اجعل النشرة (newsletter) مهمة (job) متكافئة الأثر (idempotent).**
   > *«حوّل النشرة (newsletter) إلى مهمة خلفية (background job) بمطالبة ذرّية (atomic) لكل متلقٍّ (recipient) وسجلِّ إرسالٍ دائم، كي لا
   > تُرسل إعادة تشغيلها بعد انهيار (crash) نسخةً مكررة (duplicate) لأحد. قاطِعها في المنتصف، أعِد
   > تشغيلها، وأرني صفر إرسالات مكررة (double-sends).»*

الختام (Finish): *«أودع (commit) برسالة `05-5-email-infra`.»*

> 🔧 **تحت الغطاء (Under the hood)** (اختياري (optional)): اقرأ From عند وقت الإرسال (send time) من الإعداد (config) لا من ثابت على
> مستوى الوحدة (module-level const)؛ أزِل التكرار (dedup) بفهرس فريد (unique index) على `(campaignId, recipientId)` كي يفشل
> الإدراج (insert) الثاني بدل إرسال ثانٍ؛ والتهدئة (cooldown) بمفتاح (key) Redis لكل بريد (email) مع `EXPIRE`؛
> وSPF/DKIM/DMARC سجلات DNS (DNS records) على نطاق الإرسال (sending domain).

### المطالبة الثابتة (Standing prompt)

> *«عدّد كل مسار كود (code path) يرسل بريدًا (email)، ولكل واحد، ما تكلفته حين يُساء استعماله — من
> يُراسَل، وكم مرة، ومن تدفع سمعته (reputation) الثمن.»*

## ✅ تحقق منه (Verify It)

- [ ] لديك القائمة الكاملة لمسارات إرسال بريد (email) Relay وتكلفة إساءتها (abuse cost).
- [ ] البريد (email) يُرسَل من صندوق مملوك (owned mailbox)، وعنوان المُرسِل (From address) صحيح حتى حين يُحمَّل الإعداد (config)
      متأخرًا.
- [ ] رابط إعادة تعيين (reset link) في رسالة حقيقية يشير إلى الموقع العام، لا localhost.
- [ ] قاطعت النشرة (newsletter) في منتصف تشغيلها، أعدتها، ولم يتلقَّ أحد نسخة مكررة (duplicate).
- [ ] تستطيع إعادة رواية أعطال البريد (email incidents) الثلاثة وقول لماذا كان كلٌّ «بريدًا (email)» فقط بمعنى
      أن البريد (email) انكسر.

## 🧾 بطاقة الخلاصة (Recap card)

- البريد (email) بنية تحتية (infrastructure) تشغّلها لا دالة تستدعيها — له سياسة وسمعة (reputation) وسطح إساءة (abuse surface).
- أرسل من صندوق مملوك (owned mailbox)؛ اقرأ عنوان المُرسِل (From address) عند وقت الإرسال (send time) لا عند تحميل الوحدة (module load).
- سمعة المُرسِل (sender reputation) مشتركة وقابلة للتلف — الإساءة (abuse) أو القائمة السيئة تُغرق حتى إعادات تعيين (resets) كلمة مرورك.
- روابط إعادة التعيين/التفعيل (reset/verify links) بيانات اعتماد مؤقتة (temporary credentials)؛ أعطها الأساس الصحيح (right base URL) ولا تسجّلها للأبد.
- النشرات (newsletters) مهام خلفية (background jobs): إرسالٌ متكافئ الأثر (idempotent)، إزالة تكرار (dedup) ذرّية (atomic) لكل متلقٍّ (recipient)، تهدئة (cooldown).

## 📚 المراجع ومزيد من القراءة (References & further wandering)

- شروحات **SPF وDKIM وDMARC** (dmarc.org، وثائق (docs) مشرفي بريد (postmaster) Google/Microsoft) — المصادقة (auth) التي تحمي نطاق إرسالك (your sending domain).
- وثائق (docs) **سمعة المُرسِل (sender reputation) / مشرف البريد (postmaster)** لدى مزوّدك (Google Postmaster Tools، Microsoft SNDS) — كيف تُحسب الدرجة التي لا تراها.
- ورقتا (cheat sheets) OWASP **«نسيان كلمة المرور (forgot-password)»** و**«تعداد الحسابات (Account Enumeration)»** — مسارات إعادة التعيين (reset flows) أسطحًا أمنية (security surfaces).
- مادة تكافؤ الأثر (idempotency) والمهام الخلفية (background jobs) في **الدرس (lesson) 7.4** و**الدرس 10.2** — النشرة (newsletter) بوصفها المهمة القابلة للإعادة (retryable job) النموذجية.
- ‏RFC 5321 (**SMTP**) — البروتوكول (protocol) تحته، حين تكفّ رسالة الارتداد (bounce message) عن أن تكون مفهومة.

---

# 5.6 — قائمة OWASP العشرة (OWASP Top 10)، مُسقَطة على تطبيق حقيقي (Mapped to a Real App)

## 🔥 قصة من الميدان (The War Story)

جرى تدقيق أمني (security audit) كامل على المنصة (platform) المرجعية، قُيّم كما يفعل مختبِر اختراق (pentester): مقابل **قائمة
OWASP العشرة (Top 10)**، وهي إجماع الصناعة على أخطر عشرة مخاطر لتطبيقات الويب. والمدهش لم يكن
شدة (severity) النتائج (findings) — بل كم كانت *عادية*. لا شيء غريبًا. كل نتيجة (finding) فئةٌ (category) على القائمة، جالسةٌ
على مرأى في تطبيق (app) يعمل ويُشحَن:

- وسيط بثٍّ (streaming proxy) يجلب ويوقّع روابط داخلية (internal URLs) — **A10، SSRF** (الدرس (lesson) 5.4).
- مفتاح توقيع (signing secret) يرجع بصمت إلى قيمة افتراضية ثابتة (hardcoded default) — **A05، سوء الإعداد الأمني (Security Misconfiguration)** (5.4، 5.7).
- لا تتبّع أخطاء (error tracking) على الخادم (server) أصلًا، فالأعطال غير مرئية — **A09، فشل التسجيل والمراقبة الأمنية (Security Logging & Monitoring Failures)** (الوحدة (Module) 7).
- كل CI يعمل على جهاز شخصي حامل لبيانات اعتماد (credential-bearing) ينفّذ كود (code) طلبات دمج (pull request) غير موثوق، وإجراءات طرف ثالث (third-party actions) مثبّتة (pinned) بـ*وسم (tag)* (متغير (mutable)) لا بـSHA (ثابت) — **A08، فشل سلامة البرمجيات والبيانات (Software & Data Integrity Failures)** / سلسلة التوريد (supply chain) (الوحدة (Module) 8.4).

أربع نتائج (findings)، أربع فئات (categories) من العشرة، صفر ثغرات يوم-صفر (zero-days). **قائمة العشرة (Top 10) ليست امتحانًا
تنجح فيه مرة — بل قائمة تحقّق (checklist) تسير عليها كل مرة، لأن الأعطال التي تسمّيها هي العادية
الشائعة التي تُشحَن في تطبيقات حقيقية بُنيت بسرعة.**

## 📐 المبدأ (The Principle)

### 1. العشرة (Top 10) قائمةَ تحقّقٍ (checklist) عملية لا شهادة (certificate)

قائمة OWASP العشرة (OWASP Top 10) *تُحدَّث دوريًا (periodically updated)* بفئات (categories) المخاطر التي تسبّب الاختراقات (breaches) فعلًا. لا
تحصل على «اعتماد (certified) OWASP». بل تستعملها سيرًا: لكل فئة (category)، أين قد تظهر في *تطبيقي*؟ وهذه
القائمة مُسقَطة على حيث تميل للظهور في كود (code) بناه وكيل (agent):

| # | الفئة (category) | أين تختبئ في تطبيق (app) مبنيّ بالفايب |
|---|---|---|
| A01 | التحكم المعطوب بالوصول (Broken Access Control) | نقطة نهاية (endpoint) تنسى فحص *مَن* يسأل؛ معرّفات (IDs) تزيدها لرؤية بيانات غيرك |
| A02 | فشل التعمية (Cryptographic Failures) | أسرار (secrets) في الكود (code)؛ تجزئة (hashing) ضعيفة/غائبة؛ رموز (tokens) في localStorage (5.3) |
| A03 | الحقن (Injection) | مدخلٌ (input) غير مُنقّى (unsanitised) في استعلام (query)/أمر؛ `String + input` من الوكيل (agent) |
| A04 | التصميم غير الآمن (Insecure Design) | غياب تحديد المعدل (rate limits)، لا نموذج إساءة (abuse model) — الدرس (lesson) 5.1 كله |
| A05 | سوء الإعداد الأمني (Security Misconfiguration) | أسرار (secrets) ترجع لقيم افتراضية (5.4)؛ تنقيح (debug) مفعّل في الإنتاج (production)؛ CORS متساهل (permissive) |
| A06 | المكوّنات المعطوبة (Vulnerable Components) | تبعيات (dependencies) قديمة بثغرات (vulnerabilities) CVE معروفة (الوحدة (Module) 8.4) |
| A07 | فشل المصادقة (Auth Failures) | جلسات (sessions) ضعيفة، لا 2FA، حسابات (accounts) قابلة للتعداد (enumerable) (5.3) |
| A08 | سلامة البرمجيات/البيانات (Software/Data Integrity) | إجراءات CI غير مثبّتة (unpinned)، خط بناء (build pipeline) غير موثوق (8.4) |
| A09 | فشل التسجيل والمراقبة (Logging & Monitoring Failures) | لا تتبّع أخطاء (error tracking) — أعمى في الإنتاج (الوحدة (Module) 7) |
| A10 | SSRF | جلب روابط (URLs) يؤثر فيها العميل (5.4) |

لاحظ كم من هذه الوحدة (Module) على القائمة سلفًا. العشرة (Top 10) هي الخريطة (map)، وهذه الدورة هي التضاريس (terrain).

### 2. المراجعة الأمنية (security review) تمريرةٌ (pass) بذاتها

أهم نقطة عملية: **المراجعة الأمنية (security review) منفصلة عن مراجعة الصحة (correctness review).** المراجع الذي يفحص (reviewer checking) «هل
يعمل؟» ذهنيّته (mindset) مختلفة عمّن يسأل «ماذا أستطيع أن أبلغ أو أزوّر أو أحقن أو أستنزف؟».
شغّلهما تمريرتين (passes). التدقيق الذي وجد النتائج (findings) الأربع أعلاه كان مسحًا أمنيًا (security sweep) مخصّصًا — لم
تكن أيٌّ منها لتفشل اختبارًا وظيفيًا (functional test)، ونجا معظمها من مراجعة الطلبات (PR review) الاعتيادية أشهرًا.

```mermaid
flowchart RL
    PR["طلب دمج"] --> C["تمريرة الصحة<br/>«هل يؤدي الغرض؟»"]
    PR --> S["تمريرة الأمان<br/>«ماذا يستطيع المهاجم؟»"]
    C --> M["دمج"]
    S --> M
    S -.->|"تجد SSRF، المفتاح<br/>الافتراضي، النقطة المفتوحة"| M
```

### 3. نظافة سلسلة التوريد (Supply-chain hygiene): تطبيقك غالبًا كودٌ (code) لم تكتبه

نتيجةُ (finding) A08 — إجراءات CI من طرف ثالث (third party) مثبّتة (pinned) بوسم (tag) على مشغّل (runner) حامل لبيانات اعتماد (credentials) — تستحق
عادةً بذاتها. بناؤك يشغّل كود (code) آخرين. **ثبّت إجراءات البناء (Pin build actions) بـSHA** (وسمٌ (tag) مثل `@v3`
يمكن نقله ليشير إلى كود خبيث (malicious code)؛ وSHA لا يمكن)، وأودِع (commit) **ملفات القفل (Lockfiles)**
واحترمها (كي يجلب `install` النسخ التي دقّقتها (versions you audited) بالضبط، لا الأحدث)، وشغّل **بوابة (gate) تدقيق
تبعيات (dependency-audit gate)** في CI تفشل عند الثغرات (vulnerabilities) الحرجة المعروفة. هذا مدخل (input) الوحدة (Module) 8.4، حيث تنال سلسلة (chain)
التوريد درسها.

**اقرن ذلك بحالة عامة.** عطل (outage) Cloudflare في يوليو 2019 — قاعدة WAF (WAF rule) واحدة بتعبير نمطي (regex)
كارثي رفع معالجات (CPU) حافتهم كلها إلى السقف (ceiling) وأعاد 502 عبر جزء كبير من الويب نحو 27 دقيقة —
هو سوء إعداد أمني (A05) على مستوى عالمي: سطرُ إعدادٍ (config) واحد، نُشر في كل مكان دفعة، بلا
طرح متدرّج (staged rollout) ولا مفتاح إيقاف (kill switch). فئات (categories) العشرة (Top 10) ليست مشاكل تطبيقات صغيرة. بل الأشكال نفسها في
كل حجم.

## 🎛️ وجّه وكيلك (Direct Your Agent)

شغّل تدقيقًا ذاتيًا (self-audit) مهيكلًا بالعشرة (Top 10) على Relay. هذه التمريرة الأمنية (security pass) الثابتة مُجسَّدة.

1. **سِر (secret) على العشرة (Top 10) مقابل Relay.**
   > *«سِر (secret) على قائمة OWASP العشرة (OWASP Top 10) فئةً (category) فئة. ولكل واحدة، أخبرني أين قد تظهر في Relay
   > وهل نحن معرّضون حاليًا. أعطني جدولًا: الفئة (category)، تعرّضنا (exposure)، الشدّة (severity).»*
2. **أصلح أعلى ثلاث نتائج (findings).**
   > *«خذ أعلى ثلاث نتائج (findings) شدّةً (severity) وأصلحها. ولكل واحدة، أرني قبل/بعد وبرهانًا أن الثغرة (hole)
   > مغلقة.»*
3. **أضف بوابة تدقيق تبعيات (dependency-audit gate) إلى CI.**
   > *«أضف خطوة CI تشغّل تدقيق تبعيات (dependency audit) وتُفشل البناء عند الثغرات (vulnerabilities) الحرجة المعروفة.
   > أثبته: ازرع تبعية (dependency) بثغرة (hole) CVE حرجة (critical CVE) معروفة، شاهد CI يفشل، أزلها، شاهده ينجح.»*
4. **ثبّت إجراءات البناء (Pin build actions) بـSHA.**
   > *«غيّر كل إجراء CI من طرف ثالث (third party) من وسم (`@v3`) إلى SHA إيداع (commit) مثبّت (pinned). واشرح لماذا
   > الوسم متغير (tag is mutable) وSHA ليس كذلك.»*
5. **افصل المراجعة الأمنية (security review) عن مراجعة الصحة (correctness review).**
   > *«راجع هذا التغيير مرة ثانية، كمهاجم (as an attacker) فقط: ماذا أستطيع أن أبلغ أو أزوّر أو أحقن
   > أو أستنزف؟ لا تعلّق على أن الميزة (feature) تعمل — بل على ما يستطيع المهاجم (attacker) فعله فقط.»*

الختام (Finish): *«أودع (commit) برسالة `05-6-owasp-audit`.»*

> 🔧 **تحت الغطاء (Under the hood)** (اختياري (optional)): بوابة التدقيق (audit gate) `npm audit --audit-level=high`
> (أو `pnpm audit` / Snyk / Dependabot) مهمةً (job) تفشل في CI؛ وتثبيت SHA يستبدل
> `uses: actions/checkout@v4` بـ`uses: actions/checkout@<sha 40 محرفًا>`؛ وسير
> العشرة (Top 10) ملفُ تحقّقٍ مُودَع في المستودع (repo)، يُعاد كل تدقيق.

### المطالبة الأمنية الثابتة (Standing security prompt)

> *«راجع هذا التغيير كمهاجم (as an attacker): ماذا أستطيع أن أبلغ أو أزوّر أو أحقن أو أستنزف؟ أعطني
> سيناريو فشل (failure scenario) ملموسًا لكل نتيجة (finding) — أي مدخل (input) يكسرها؟»*

## ✅ تحقق منه (Verify It)

- [ ] جدول سير العشرة (Top 10) موجود لـRelay، بتعرّض (exposure) وشدّة (severity) لكل فئة (category).
- [ ] أعلى ثلاث نتائج (findings) مُصلَحة ورأيت كل ثغرة (hole) تُبرهَن مغلقة.
- [ ] بوابة تدقيق التبعيات (dependency-audit gate) مُبرهَنة: تفشل عند نسخة (instance) سيئة مزروعة وتنجح بعدها.
- [ ] كل إجراء CI من طرف ثالث (third party) مثبّت (pinned) بـSHA، وتستطيع قول لماذا الوسم (tag) لا يكفي.
- [ ] تستطيع إعادة رواية نتائج (findings) التدقيق الأربع وتسمية فئة (category) العشرة (Top 10) لكلٍّ منها.

## 🧾 بطاقة الخلاصة (Recap card)

- قائمة OWASP العشرة (OWASP Top 10) قائمةُ تحقّقٍ (checklist) تسير عليها كل مرة، لا شهادةً (certificate) تنالها مرة.
- نتائج (findings) التدقيق الحقيقية فئات (categories) عادية — SSRF، أسرار (secrets) افتراضية، لا مراقبة، CI غير مثبّت (unpinned) — لا ثغرات يوم-صفر (zero-days).
- المراجعة الأمنية (security review) تمريرة (pass) منفصلة عن مراجعة الصحة (correctness review)؛ شغّلها بذهنية (mindset) مهاجم (attacker).
- نظافة سلسلة التوريد (supply-chain hygiene): ثبّت إجراءات البناء (Pin build actions) بـSHA، احترم ملفات القفل (lockfiles)، ضع بوابة تدقيق تبعيات (dependency-audit gate).
- معظم هذه الدورة هي العشرة (Top 10) بصيغة تضاريس (terrain) — الفئات (categories) تُسقَط مباشرة على الشقوق التي تعرفها.

## 📚 المراجع ومزيد من القراءة (References & further wandering)

- **قائمة OWASP العشرة (OWASP Top 10)** (owasp.org/Top10) — القائمة نفسها، بكل فئة (category) مشروحة وموصولة بالوقاية (prevention).
- **معيار OWASP للتحقق من أمان التطبيقات (ASVS)** — الأخ الأكبر المفصّل القابل للاختبار (test) للعشرة (Top 10).
- **سلسلة أوراق (Cheat Sheet Series) OWASP** — صفحة مركّزة لكل خطر؛ الرفيق العملي للقائمة.
- تحليل (postmortem) Cloudflare **«تفاصيل عطل (outage) Cloudflare في 2 يوليو 2019»** — سوء إعداد (A05) على مستوى عالمي، مكتوبٌ ببراعة.
- **إرشاد (guidance) GitHub لتثبيت الإجراءات بـSHA إيداع (commit SHA) كامل** — إصلاح (fix) سلسلة التوريد (supply chain) من نتيجة (finding) A08.

---

# 5.7 — الأسرار والإعداد (Secrets and Configuration): مفاتيح المملكة (keys to the kingdom)

## 🔥 قصة من الميدان (The War Story)

في 2016، ترك مهندسو Uber بيانات اعتماد (credentials) Amazon Web Services داخل كودٍ (code) مخزّن في
مستودع (repository) GitHub **خاص**. بدا «خاص» آمنًا. لم يكن. حصل المهاجمون (attackers) على وصول (access) للمستودع (repo)،
ووجدوا المفاتيح (keys) جالسةً في المصدر (source)، واستعملوها لبلوغ بيانات **57 مليون** راكب وسائق.

ثم اتخذت Uber القرار الأسوأ. بدل الإفصاح (disclosing) عن الاختراق (breach)، دفعت للمهاجمين (attackers) 100 ألف دولار
ليصمتوا وألبسته زيّ «مكافأة ثغرة (bug bounty)». وحين خرج الأمر — وهذه الأمور تخرج دائمًا — **كلّف
التستّر (cover-up) أكثر من الاختراق (breach)**: عقوبات تنظيمية (regulatory penalties)، وتسوية (settlement)، وإدانة جنائية لمدير أمن الشركة (chief security officer).
تحوّل سرٌّ (secret) في مستودع (repository) إلى مشكلة بتسعة أرقام وسجلٍّ جنائي شخصي.

ولدينا الشكل نفسه مصغّرًا في بنكنا. مفتاح توقيع (signing secret) **رجع بصمت إلى نصٍّ برمجيٍّ ثابتٍ (hardcoded literal)
للمطوّر (developer)** حين لم يُضبط (الدرس (lesson) 5.4) — مفتاحٌ (key) جالسٌ في المصدر (source)، معطِّلًا الحمايةَ نفسها
التي يُفترض أن يوفّرها. وخطأ جمهور المتغير (env-var audience) (5.3)، حيث كسرت إعادةُ استعمال قيمةِ
إعدادٍ (configuration value) واحدة عبر غرضين إعاداتِ تعيين كلمة المرور (password resets). الأسرار (secrets) والإعداد (config) المادة نفسها: قيمٌ
تقرر من يدخل.

**الدرس (lesson): سرٌّ (secret) في مستودع (repository) تسريبٌ (leak) بمهلة. و«مستودع خاص (private repo)» ليس مدير أسرار (secret manager). وهذه أشيع طريقة
تُخترَق بها تطبيقات الفايب، لأن الوكلاء (agents) يثبّتون (hardcode) مفتاحًا (key) في لحظة ليختفي الخطأ.**

## 📐 المبدأ (The Principle)

### 1. ما السرّ (secret) فعلًا

السرّ (secret) **أي شيء يمنح وصولًا (access)**: مفاتيح API (API keys)، وكلمات مرور قواعد البيانات (database passwords)، ورموز التوقيع (signing tokens)،
وأسرار عملاء (client secrets) OAuth، ومفاتيح توقيع الويب-هوك (webhook signing keys). إن كانت حيازة القيمة تتيح لك فعل ما لا
تستطيعه بدونها، فهي سرٌّ (secret) ويجب معاملتها كذلك. الاختبار (test) ليس «هل تبدو عشوائية» — بل «هل
تفتح بابًا».

### 2. القوانين الأربعة للأسرار (The four laws of secrets)

```mermaid
flowchart TD
    S["سرّ"] --> L1["1. لا في المستودع أبدًا<br/>سجل git للأبد —<br/>إيداعٌ واحد تسريب"]
    S --> L2["2. لا في حِزم العميل أبدًا<br/>كل ما يُشحَن إلى<br/>متصفح/تطبيق عامّ"]
    S --> L3["3. مفصولة لكل بيئة<br/>مفاتيح dev/staging/prod تختلف<br/>— تسريب dev ليس اختراق prod"]
    S --> L4["4. قابلة للتدوير في دقائق<br/>ستسرّب واحدًا —<br/>الخطة تدوير لا أمل"]
```

**القانون (Law) 1 — لا في المستودع (repo) أبدًا.** سجل (history) git دائم. إيداع (commit) سرٍّ (secret) و«إزالته» في الإيداع
التالي لا يزيله — يبقى في السجل (history)، مقروءًا لأي أحد استنسخ (clones) المستودع (repo) يومًا. 57 مليون سجل (million records)
من Uber هي القانون (Law) 1.

**القانون (Law) 2 — لا في حِزم العميل (client bundles) أبدًا.** كل ما تشحنه إلى متصفح (browser) أو تطبيق (app) موبايل عامٌّ —
يستطيع المستخدمون (users) قراءته وتفكيكه (decompile) وفحصه. فمفتاحٌ (key) مُترجَم (compiled) داخل بناء واجهةٍ (frontend build) مفتاحٌ منشور.
والتضمين وقت البناء (build-time inlining) يجعل هذا *سهلًا سهوًا* (الدرس (lesson) 4.5: `.env.local` مُتجاهَل (gitignored) خبز قيمة
خاطئة في تطبيق (app) مشحون، غير مرئية في أي فرق (diff)). إن كان يعمل على العميل (client)، فلا يستطيع حمل
سرّ (secret).

**القانون (Law) 3 — مفصولة لكل بيئة (environment).** dev وstaging وprod ينال كلٌّ أسراره الخاصة. حينها
يكون مفتاح (key) dev المسرّب إزعاجًا لا اختراقًا (breach)، وتستطيع تدوير (rotate) بيئة (environment) دون مسّ الأخريات.

**القانون (Law) 4 — قابلة للتدوير (rotatable) في دقائق.** ستسرّب سرًّا (secret) في النهاية — لقطةُ شاشة (screenshot)، سطرُ
سجل (log line)، إعدادٌ (config) ملصوق. والسؤال أتدويره عملية خمس دقائق أم مشروع يومين. صمّم للتدوير (rotation) *قبل*
أن تحتاجه: مكانٌ واحد لتغيير القيمة، وكل مستهلك (consumer) يقرأ منه.

### 3. أين تعيش الأسرار (secrets) فعلًا

لا في المستودع (repo) ولا في الحِزمة (bundle) — فأين؟ في **متغيرات بيئة (environment variables) يوفّرها مدير أسرار (secret manager)**: مخزن
أسرار المضيف (host's secrets store)، أو خزنة (vault) مخصصة. يقرؤها التطبيق (app) وقت التشغيل (runtime)؛ ولا تلمس شجرة المصدر (source tree) أبدًا.
وتضيف **سلكًا كاشفًا (tripwire)**: ماسحُ أسرار (gitleaks، فحص أسرار (secrets) GitHub) في خطاف ما قبل
الإيداع (pre-commit hook) وفي CI، كي *يُحظَر* المفتاح المثبّت (hardcoded key) قبل إيداعه بدل اكتشافه في تدقيق (audit).

### 4. هذا هو نمط فشل (failure mode) مبرمج الفايب (vibe-coder) الأول

قلها بوضوح، فهي أهم جملة في الوحدة (Module): **الوكلاء (agents) يثبّتون المفاتيح (hardcode keys) ليجعلوا الأمور تعمل.**
يصطدم الوكيل (agent) بخطأ مصادقة (auth error)، وأسرع طريق لعلامة خضراء (green checkmark) لصق المفتاح (key) في المصدر (source). سيفعلها بمرح
وتكرار، ما لم توقفه آليًا — بخطاف ماسح (scanner hook) (مبدأ 8.1: القواعد بسرعة الوكيل (agent) يجب أن تكون
آلية لا محفوظة) وقاعدة CLAUDE.md يعيد قراءتها كل جلسة (session).

## 🎛️ وجّه وكيلك (Direct Your Agent)

لدى Relay على الأرجح سرٌّ (secret) في المكان الخطأ. جِده، وانقله، واجعل التسريبات (leaks) رخيصة النجاة.

1. **امسح سجل git (git history) كاملًا.**
   > *«امسح سجل git (git history) كامل لـRelay — لا الملفات الحالية فقط — بحثًا عن أي شيء يشبه
   > سرًّا (secret): مفاتيح API (API keys)، كلمات مرور (passwords)، رموز (tokens)، سلاسل اتصال (connection strings). أبلغ عن كل إصابة (hit) مع الإيداع (commit)
   > الذي فيها. تذكّر أن سرًّا (secret) في السجل (history) مسرّبٌ ولو لم يكن في الكود (code) الحالي.»*
2. **انقل كل سرٍّ (secret) حي إلى مدير أسرار المضيف (host's secret manager).**
   > *«انقل كل سرٍّ (secret) حي من المستودع (repo) وأي ملف إعداد (config file) إلى مدير أسرار المضيف (host's secret manager) / متغيرات
   > البيئة (environment). يقرؤها التطبيق (app) وقت التشغيل (runtime). وأرني أن المستودع (repo) لا يحوي سرًّا (secret) حيًا وأن
   > التطبيق (app) ما زال يعمل.»*
3. **أضف مسح أسرار (secret scan) ما قبل الإيداع (pre-commit).**
   > *«أضف خطاف ما قبل إيداع (pre-commit hook) وخطوة CI يشغّلان ماسح أسرار (مثل gitleaks) ويحظران
   > الإيداع (commit)/البناء إن كُشف سرّ (secret). ثم ازرع مفتاحًا (key) وهميًا في إيداع اختبار (test commit) وأرني الخطاف (hook)
   > يحظره.»*
4. **أثبت نظافة حِزم العميل (client bundles).**
   > *«أرني كل موضع قد يظهر فيه سرٌّ (secret) فيما نشحنه إلى المتصفحات (browsers) أو تطبيق (app) الموبايل (mobile) —
   > نقّب (grep) في الحِزمة المبنيّة (built bundle)، لا المصدر (source). يجب أن تكون فارغة. وإن بدت أي قيمة مُضمَّنة
   > وقت البناء سرًّا (secret)، فأشِر إليها (انظر 4.5).»*
5. **دوّر مفتاحًا (key) حقيقيًا كاملًا، وقِس الوقت.**
   > *«اختر سرًّا (secret) حقيقيًا واحدًا ودوّره كاملًا: ولّد قيمة جديدة، ضعها في مدير
   > الأسرار (secrets)، أكّد أن التطبيق (app) يلتقطها، أبطل (invalidate) القديمة. وقِس الكل — الهدف أقل من 15
   > دقيقة.»*
6. **اكتب الذاكرة (Write the memory).**
   > *«أضف إلى CLAUDE.md: لا تثبّت سرًّا (never hardcode a secret) لإصلاح (fix) خطأ أبدًا — قف واسأل. كل سرٍّ (secret) يعيش في
   > مدير أسرار المضيف (host's secret manager). الأسرار (secrets) تفشل مغلقة (fail closed)، ولا ترجع لقيمة افتراضية (default) أبدًا.»*

الختام (Finish): *«أودع (commit) برسالة `05-7-secrets-config`.»*

> 🔧 **تحت الغطاء (Under the hood)** (اختياري (optional)): `gitleaks detect` على السجل (history) و`gitleaks protect` في
> خطاف ما قبل الإيداع (pre-commit hook)؛ والأسرار (secrets) عبر مخزن بيئة المضيف (host's env store) أو خزنة (vault)، تُقرأ عبر `requireEnv()`
> ترمي عند الغياب (لا `?? 'default'`)؛ ونقّب في حِزمة الإنتاج (production bundle) عن أنماط المفاتيح (keys) فحصًا
> بعد البناء (صدى مدقّق 4.5 للمُنتَج (artifact verifier)).

## ✅ تحقق منه (Verify It)

- [ ] شغّلت مسح سجل git (git history) ورأيت مخرجاته — تعرف أأودع Relay سرًّا (secret) يومًا أم لا.
- [ ] مفتاحٌ (key) وهميٌّ مزروع في إيداع اختبار (test commit) يحظره خطاف ما قبل الإيداع (pre-commit hook).
- [ ] دوّرت مفتاحًا (key) حقيقيًا كاملًا في أقل من 15 دقيقة.
- [ ] طلبت من الوكيل (agent) إظهار كل موضع قد يظهر فيه سرٌّ (secret) في حِزمة العميل (client bundle) المشحونة، فعاد
      فارغًا.
- [ ] تستطيع إعادة رواية قصة Uber 2016 — بما فيها لماذا كلّف التستّر (cover-up) أكثر — وذكر
      القوانين الأربعة للأسرار (The four laws of secrets) عن ظهر قلب.

## 🧾 بطاقة الخلاصة (Recap card)

- السرّ (secret) أي شيء يمنح وصولًا (access)؛ الاختبار (test) «هل يفتح بابًا»، لا «هل يبدو عشوائيًا».
- أربعة قوانين: لا في المستودع (repo)، لا في حِزم العميل (client bundles)، مفصولة لكل بيئة (per environment)، قابلة للتدوير (rotatable) في دقائق.
- سجل git (git history) للأبد — إيداعٌ واحد تسريب (leak)، ولو «أزلته» في الإيداع (commit) التالي.
- الأسرار (secrets) تعيش في مدير أسرار (secret manager) وتحرسها سلكٌ كاشفٌ (tripwire) في ما قبل الإيداع (pre-commit) وCI.
- اختراق (breach) مبرمج الفايب (vibe-coder) الأول: الوكلاء (agents) يثبّتون المفاتيح (hardcode keys) ليختفي الخطأ — أوقفه آليًا.

## 📚 المراجع ومزيد من القراءة (References & further wandering)

- ملفات (filings) FTC وDOJ عن **اختراق (breach) Uber 2016** وإدانة مدير الأمن (CSO) — القصة، في السجل الأولي (primary record).
- **gitleaks** (github.com/gitleaks/gitleaks) ووثائق (docs) **فحص أسرار (secrets) GitHub** — الأسلاك الكاشفة (tripwires) التي يثبّتها هذا الدرس (lesson).
- ورقة (cheat sheet) OWASP **«إدارة الأسرار (Secrets Management)»** — أين يجب أن تعيش الأسرار (secrets) وكيف تُدوَّر.
- **تطبيق العوامل الاثني عشر (Twelve-Factor App)**، العامل (factor) الثالث (**الإعداد (config)**) — انضباط الإعداد-في-البيئة (config-in-the-environment)، في صفحة واحدة.
- الدرس (lesson) **4.5** (تحقّق من المُنتَج لا المصدر (verify the artifact, not the source)) و**5.4** (أسرار تفشل مغلقة (secrets that fail closed)) — الحادثتان اللتان يعمّمهما هذا الدرس.

---

*التالي: الوحدة (Module) 6 — خادمٌ (backend) واحد، عملاء (clients) كثر. يتوقف منتجك (your product) عن كونه موقعًا واحدًا ويصبح
تطبيق (app) ويب، وتطبيق iOS، وتطبيق Android، وتطبيق تلفاز — كلها تخاطب خادمًا واحدًا (one backend) لا
يستطيع تحديثها كلها بالسرعة نفسها.*
