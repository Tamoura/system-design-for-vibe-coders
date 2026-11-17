# الوحدة 1 (Module 1) — الهوية والوصول (Identity & Access)

*كل SaaS يجب أن يجيب عن ثلاثة أسئلة في كل طلب (request): من أنت، وإلى أي عميل (customer) تنتمي، وهل يُسمح لك بفعل هذا؟ تبني هذه الوحدة هذه الإجابات بالترتيب: المصادقة (authentication)، ثم الهيكل القائم على المنظمات (organization) والعضويات (membership) الذي يجعل المنتج متعدد المستأجرين (multi-tenant)، ثم التفويض (authorization)، وأخيرًا طبقة المؤسسات (enterprise layer) التي يتوقعها العملاء الكبار (large customers) قبل أن يوقّعوا. أتقن هذه الأربعة مبكرًا، لأن إضافتها لاحقًا تكلّف أكثر بكثير من بقية الدورة كلها مجتمعة.*

> **التطبيق العملي (Practice):** ابدأ من [نسخة البداية من Beacon (Beacon starter)](https://github.com/Tamoura/system-design-for-vibe-coders/tree/beacon/starter)، وحلّ التمارين قبل النظر إلى [الحل المرجعي لهذه الوحدة](https://github.com/Tamoura/system-design-for-vibe-coders/tree/beacon/module-1-solution) (الفرع (branch) `beacon/module-1-solution`).

---

# 1.1 — المصادقة: إثبات هوية الشخص

*المستوى (Level): 🟢 مبتدئ (Beginner)*

## ⚡ الدرس في دقيقة (In 60 seconds)

- المصادقة تثبت من الذي يرسل الطلب. وهي مجموعة من المسارات (flows) (التسجيل (sign-up)، وتسجيل الدخول (login)، والتحقق (verification)، واستعادة كلمة المرور (reset)، والمصادقة متعددة العوامل (MFA)، وتسجيل الخروج)، والمهاجم (attacker) يختار أضعفها.
- القاعدة الأهم: اصنع تجزئة (hash) كلمات المرور (passwords) بـ argon2id أو bcrypt، ولا تخزّن من رموز الجلسات (session tokens) واستعادة كلمة المرور والروابط السحرية (magic-link) إلا تجزئاتها.
- الخيار الافتراضي (default) للنسخة الأولى (v1): مكتبة (library) مثل Better Auth أو Devise أو django-allauth، مع جلسات على الخادم (server-side sessions) داخل كوكي (cookie) `HttpOnly` و`Secure` و`SameSite=Lax`.
- تسجيل الدخول الاجتماعي (social login) يعني مسار رمز التفويض (authorization code flow) مع PKCE، مع ربط الهوية بمعرّف `sub` لدى المزوّد (provider)، وليس بالبريد الإلكتروني (email) وحده أبدًا.
- الفخ الأكبر: الحواف (edges)، مثل روابط استعادة (reset links) تعمل مرتين، ورسائل "البريد غير موجود"، وتسجيل خروج (logout) يكتفي بمسح الكوكي.

## 🧭 لماذا يحتاجه كل SaaS

لم يكن في النموذج الأولي (prototype) من Beacon تسجيل دخول. قائمة واحدة للمراقِبات (monitors)، وصفحة حالة (status page) واحدة، وكل شيء على `localhost`. ثم طلب صديق أن يجرّبه، وخلال ساعة ظهرت أسئلة حقيقية. كيف يعرف Beacon أن الشخص الذي يعدّل مراقِب (monitor) `api.acme.com` من شركة Acme فعلًا؟ كيف يعود غدًا؟ ماذا يحدث عندما ينسى كلمة المرور (password)، أو يسجّل بحساب Google يوم الاثنين ثم يحاول بالبريد الإلكتروني يوم الثلاثاء؟

المصادقة (Authentication، وتُختصر غالبًا إلى **authn**) هي عملية إثبات أن الشخص أو البرنامج الذي يرسل الطلب هو من يدّعي أنه هو. وهي تختلف عن **التفويض** (Authorization أو authz، الدرس 1.3) الذي يقرّر ما يحق لهذه الهوية المثبتة (identity) فعله. تقع معظم الثغرات الأمنية (security bugs) في منتجات SaaS الناشئة على الحدود بين الاثنين، لكن المصادقة تأتي أولًا: إذا كانت الهوية خاطئة، فكل فحص لاحق (check) يفحص الشخص الخطأ.

نموذج تسجيل الدخول (login form) هو الجزء السهل. الأجزاء الصعبة هي الحواف: روابط استعادة كلمة المرور التي يمكن إعادة استخدامها، وكوكيز الجلسة (session cookies) التي تستطيع السكربتات المحقونة (injected scripts) قراءتها، ورسالة "البريد غير موجود" التي تخبر المهاجمين (attackers) من هم عملاؤك، وزر تسجيل خروج لا يُخرج أحدًا.

**المصادقة (authentication) ليست نموذج تسجيل دخول (login form)، بل مجموعة من المسارات (التسجيل (sign-up)، وتسجيل الدخول (login)، والاستعادة (recovery)، والتحقق (verification)، وتسجيل الخروج (logout)) يجب أن تكون كلها بالقوة (strength) نفسها، لأن المهاجم (attacker) يختار أضعفها.**

## 📐 كيف يعمل

### 🟢 الأساسيات

ثلاث أفكار تحمل معظم الثقل: بيانات الاعتماد (credentials)، والجلسات (sessions)، والكوكيز (cookies).

**بيانات الاعتماد** هي ما يقدّمه المستخدم (user) لإثبات هويته. أشهر أنواعها:

| العامل (factor) | مثال | القوة | نقطة الضعف الرئيسية |
|---|---|---|---|
| شيء تعرفه | كلمة المرور | ضعيف وحده | إعادة الاستخدام (reuse)، والتصيّد (phishing)، والتخمين (guessing) |
| شيء تملكه (صندوق البريد) | رابط سحري (magic link)، رابط استعادة (reset link) | متوسط | آمن بقدر أمان صندوق البريد (mailbox) فقط |
| هوية مفوَّضة (delegated identity) | "تسجيل الدخول عبر Google" (OAuth/OIDC) | جيد | أخطاء ربط الحسابات (account-linking) |
| شيء تملكه (جهاز) | تطبيق TOTP (TOTP app)، مفتاح المرور (passkey) | قوي | الاستعادة عند فقدان الجهاز |
| شيء أنت هو | الوجه أو البصمة (fingerprint) لفتح مفتاح المرور | قوي | لا يغادر الجهاز أبدًا، لذلك ليس عاملًا على جهة الخادم (server-side factor) |

**يجب أن تُحفظ كلمات المرور كتجزئة (Hash)، لا أن تُشفَّر (encrypted)، ولا أن تُخزَّن كنص صريح (plain) أبدًا.** التجزئة دالة أحادية الاتجاه (one-way function): يمكنك مقارنة تخمين (guess) بها، لكن لا يمكنك عكسها. التجزئات (hashes) العادية مثل SHA-256 مصممة لتكون سريعة، وهذا بالضبط الخطأ هنا، لأن التجزئة السريعة (fast hash) تسمح لمن يسرق قاعدة بياناتك (database) بتجربة مليارات التخمينات (guesses) في الثانية. أما تجزئات كلمات المرور (password hashes) فهي *بطيئة عمدًا* و*مملّحة* (Salted)، أي أن كل تجزئة تخلط قيمة عشوائية (random value) حتى تنتج كلمات المرور المتطابقة تجزئات مختلفة. استخدم **argon2id** (توصية OWASP الحالية) أو **bcrypt** (أقدم، وموجود في كل مكان، ومقبول). لاحظ أن bcrypt لا ينظر إلا إلى أول 72 بايت (bytes) من المدخلات. كل بيئة شائعة (stack) توفر هذا جاهزًا: `contrib.auth` في Django، و`has_secure_password` في Rails، وواجهة `Hash` في Laravel، و`golang.org/x/crypto` في Go.

**الجلسات** هي طريقة الخادم (server) في تذكّرك بين الطلبات. بروتوكول (protocol) HTTP عديم الحالة (stateless)، لذلك بعد تسجيل دخول ناجح ينشئ الخادم سجل جلسة (session record) ويعطي المتصفح (browser) رمزًا عشوائيًا (random token) لا يمكن تخمينه. كل طلب لاحق يحمل هذا الرمز (token)، والخادم يبحث عنه.

**الكوكيز** تحمل هذا الرمز. أربع خصائص (attributes) مهمة:

- `HttpOnly`: لا تستطيع JavaScript قراءة الكوكي، لذلك لا تستطيع ثغرة (bug) XSS سرقته بسهولة.
- `Secure`: لا يُرسل إلا عبر HTTPS.
- `SameSite=Lax`: لا يرفق المتصفح الكوكي بمعظم الطلبات القادمة من مواقع أخرى (cross-site requests)، وهذا يمنع هجوم CSRF (تزوير الطلبات عبر المواقع) التقليدي الذي يرسل فيه موقع آخر نموذجًا إلى موقعك. الخيار `Strict` أشد، لكنه يكسر تجربة "انقر رابطًا في Slack فتصل وأنت مسجّل الدخول (signed in)".
- `Path=/` مع البادئة (prefix) `__Host-` في الاسم: عندها يرفض المتصفح الكوكي إلا إذا كان `Secure`، وبلا خاصية (attribute) `Domain`، ومع `Path=/`، وهذا يمنع النطاقات الفرعية (subdomains) من الكتابة فوقه.

هذا هو المسار (flow) الكامل لتسجيل الدخول بكلمة مرور:

```mermaid
sequenceDiagram
    participant D as Postgres
    participant A as تطبيق Beacon (Beacon app)
    participant B as المتصفح (Browser)
    B->>A: POST /login بالبريد وكلمة المرور (POST /login with email and password)
    A->>D: جلب المستخدم حسب البريد (Load user by email)
    D-->>A: صف المستخدم مع تجزئة argon2id (User row with argon2id hash)
    A->>A: التحقق من كلمة المرور مقابل التجزئة (Verify password against hash)
    A->>D: إدراج جلسة مع SHA-256 لرمز عشوائي (Insert session with SHA-256 of random token)
    A-->>B: Set-Cookie __Host-session HttpOnly Secure SameSite=Lax
    B->>A: GET /monitors مع الكوكي (GET /monitors with cookie)
    A->>D: البحث عن الجلسة بتجزئة الرمز (Look up session by token hash)
    D-->>A: الجلسة مع user_id وموعد الانتهاء (Session with user_id and expiry)
    A-->>B: 200 قائمة المراقِبات (200 monitor list)
```

قاعدة البيانات تخزّن *تجزئة* رمز الجلسة (session token)، لذلك لا يمكن استخدام نسخة مسرّبة من جدول (table) `sessions` لتسجيل الدخول. هذا رخيص، ومعظم الدروس التعليمية (tutorials) تتجاهله.

```ts
import { randomBytes, createHash } from "node:crypto";

const sha256 = (s: string) => createHash("sha256").update(s).digest("hex");

export async function createSession(userId: string) {
  const token = randomBytes(32).toString("base64url"); // 256 bits of randomness
  await db.session.create({
    data: {
      id: sha256(token),                                  // store only the hash
      userId,
      expiresAt: new Date(Date.now() + 30 * 24 * 3600 * 1000),
    },
  });
  return token; // goes into the cookie, never logged
}

export async function validateSession(token: string) {
  const session = await db.session.findUnique({ where: { id: sha256(token) } });
  if (!session || session.expiresAt < new Date()) return null;
  return session; // optionally slide expiresAt forward here
}
```

**الجلسات (sessions) مقابل JWT.** رمز JWT (JSON Web Token) كتلة موقّعة (signed blob) تحتوي على ادعاءات (Claims) مثل معرّف المستخدم (user id) وموعد الانتهاء (expiry). يستطيع الخادم التحقق منه دون الرجوع إلى قاعدة البيانات، وهذه ميزته ومشكلته في الوقت نفسه: لا يمكنك بسهولة *إلغاء إصداره* (un-issue). إذا سُرق حاسوب محمول أو فُصل موظف (employee)، يبقى JWT صالحًا حتى ينتهي. عندها تضيف الفرق قائمة حظر (denylist)، وهي بحث في قاعدة البيانات (database lookup) مع كل طلب، أي أنها جلسة (session) بخطوات إضافية. لتطبيق ويب (web app) يتحدث مع الخادم الخلفي (backend) الخاص به، **الجلسات على الخادم (server-side sessions) في Postgres أو Redis هي الخيار الافتراضي (The default) المعقول**. يستحق JWT مكانه عندما يجب أن تتحقق من الرمز خدمةٌ (service) *مختلفة* لا تصل إلى مخزن جلساتك (session store)، مثل رمز هوية (ID token) OIDC من Google أو رمز قصير العمر (short-lived token) لواجهة برمجية منفصلة (API). يغطي الدرس 5.2 مفاتيح API (API keys)، وهي شيء آخر مختلف.

**التحقق من البريد الإلكتروني (email verification)** يثبت أن المستخدم يتحكم في العنوان الذي كتبه. أرسل رابطًا أو رمزًا من 6 أرقام (6-digit code)، وإلى أن يُؤكَّد لا تثق بالعنوان في أي شيء مهم: ربط الحسابات (account linking)، أو الدعوات (invitations) (1.2)، أو مطابقة النطاق (domain matching) في SSO (1.4).

### 🟡 التعمق أكثر (Going deeper)

**استعادة كلمة المرور (password reset)** مسار تسجيل دخول متنكّر، لذلك عاملها كذلك. أنشئ رمزًا عشوائيًا، وخزّن تجزئته مع مدة صلاحية قصيرة (من 15 إلى 60 دقيقة)، واجعله صالحًا لمرة واحدة (single-use)، وأرسل رابطًا بالبريد. عند استخدامه، أبطل (invalidate) جلسات المستخدم الأخرى، لأن الاستعادة كثيرًا ما تعني "أظن أن شخصًا آخر داخل حسابي". ويجب أن يكون الرد (response) على "أرسل لي رابط استعادة" متطابقًا سواء كان البريد موجودًا أم لا.

هذه النقطة الأخيرة اسمها **تعداد الحسابات** (Account Enumeration): أي اختلاف في نص الرد أو رمز الحالة (status code) أو حتى التوقيت (timing) يكشف هل البريد مسجّل. يستخدمه المهاجمون لبناء قوائم أهداف (target lists). أصلح الرسائل ("إذا كان هناك حساب، فقد أرسلنا رابطًا")، ونفّذ التجزئة البطيئة (slow hash) حتى عندما يكون المستخدم غير موجود حتى لا يكشف التوقيت شيئًا. إخفاء ذلك في التسجيل أصعب، لأن رسالة "هذا البريد مستخدم" مفيدة للمستخدم. الحل الوسط الشائع أن تقول دائمًا "تفقّد بريدك"، وأن ترسل لصاحب الحساب الموجود رسالة "لديك حساب بالفعل".

**الحماية من التخمين المتكرر (brute-force) وحشو بيانات الاعتماد.** حشو بيانات الاعتماد (Credential Stuffing) هو إعادة تجربة أزواج اسم المستخدم وكلمة المرور المسرّبة من مواقع *أخرى*. الدفاعات، مرتبة تقريبًا حسب قيمتها:

1. حدّد معدل (rate-limit) محاولات الدخول (login attempts) لكل عنوان IP ولكل حساب (الدرس 5.2 يغطي محددات المعدل). فضّل الإبطاء وإضافة CAPTCHA على القفل الصارم للحساب، لأنه يسمح لأي شخص بقفل حسابات عملائك.
2. ارفض كلمات المرور المعروف أنها مسرّبة (known-breached) عند التسجيل والاستعادة. واجهة النطاقات (range API) "Pwned Passwords" من Have I Been Pwned تتيح لك ذلك دون إرسال كلمة المرور إلى أي مكان: ترسل أول 5 أحرف من تجزئة SHA-1 الخاصة بها وتقارن محليًا.
3. اتبع NIST SP 800-63B: فضّل الطول، وتخلَّ عن قواعد التركيب (composition rules) ("رمز واحد (one symbol)، وحرف كبير واحد") وعن التغيير الدوري الإجباري.
4. وفّر المصادقة متعددة العوامل، وشجّع المسؤولين (admins) على استخدامها.

**الروابط السحرية** (Magic Links) ترسل بالبريد رابط دخول لمرة واحدة. تلغي مشكلة إعادة استخدام كلمات المرور، لكنها آمنة بقدر أمان صندوق بريد المستخدم فقط. هناك فخ حقيقي: ماسحات أمان البريد في الشركات تفتح الروابط لفحصها، فتستهلك الرمز ذا الاستخدام الواحد (single-use token) قبل أن ينقر الإنسان. الحل أن يفتح الرابط صفحة فيها زر "تسجيل الدخول" يرسل طلب POST، أو أن ترسل رمزًا قصيرًا (short code) يكتبه المستخدم بدلًا من الرابط.

**تسجيل الدخول الاجتماعي (OAuth 2.0 + OpenID Connect).** OAuth 2.0 (RFC 6749) بروتوكول لتفويض الوصول (delegating access)، وOpenID Connect (OIDC) طبقة هوية رقيقة (identity layer) فوقه تضيف **رمز الهوية**، وهو JWT يقول "هذا هو المستخدم X، وقد تحققت منه Google". المسار الذي تريده هو **مسار رمز التفويض مع PKCE (authorization code flow with PKCE)** (RFC 7636، ويُنطق "pixie"): يعيد Beacon التوجيه (redirects) إلى Google مع `code_challenge` عشوائي مُجزَّأ (hashed)، فتعيد Google التوجيه مع `code` قصير العمر، ثم يستبدل Beacon هذا الرمز مع `code_verifier` الأصلي بالرموز (tokens) عبر قناة خلفية (back channel). يمنع PKCE الاستفادة من رمز تم اعتراضه (intercepted code). ويربط المعامل (parameter) `state` طلب العودة (callback) بالمتصفح الذي بدأ المسار، وهذا يمنع CSRF في تسجيل الدخول. المسار الضمني (Implicit Flow) مُلغى في أفضل الممارسات الحالية (BCP) لأمان OAuth 2.0 (RFC 9700). لا تستخدمه.

الجزء الخطير في تسجيل الدخول الاجتماعي هو **ربط الحسابات (account linking)**. إذا سجّل شخص الدخول عبر GitHub بالبريد `ana@acme.com` وكان هناك حساب بكلمة مرور بالعنوان نفسه، فهل تدمجهما؟ فقط إذا قال المزوّد إن البريد *موثَّق* (verified)، وحتى عندها فضّل "سجّل الدخول بطريقتك الحالية لتربط الحساب". أظهر بحث "nOAuth" عام 2023 تطبيقات سُرقت حساباتها لأنها وثقت بادعاء (claim) `email` قابل للتغيير وغير موثَّق (mutable) قادم من مستأجر (tenant) في Microsoft Entra ID. اربط الهويات (identities) بالمعرّف الثابت للمستخدم لدى المزوّد (`sub`)، ولا تربطها بالبريد أبدًا.

**المصادقة متعددة العوامل (MFA).** العامل الثاني الشائع (second factor) هو **TOTP** (RFC 6238): سرّ مشترك (shared secret) مخزّن في تطبيق مصادقة (authenticator app) يولّد رمزًا من 6 أرقام (6-digit code) كل 30 ثانية. خزّن السر (secret) مشفّرًا، واقبل انحرافًا في الساعة (clock drift) بمقدار خطوة واحدة (one step)، وامنع إعادة استخدام الرمز نفسه، وأصدر دائمًا **رموز استرداد** (Recovery Codes) عند التفعيل (enrolment) (مُجزَّأة، ولمرة واحدة). رموز SMS (SMS codes) أفضل من لا شيء وأضعف من TOTP بسبب هجمات تبديل شريحة SIM (SIM-swap attacks).

**مفاتيح المرور (WebAuthn).** مفتاح المرور زوج مفاتيح عام وخاص ينشئه جهاز المستخدم أو مدير كلمات المرور (password manager) لموقع محدد واحد. لا يخزّن الخادم إلا المفتاح العام (public key). عند تسجيل الدخول يرسل الخادم تحديًا عشوائيًا (challenge)، فيوقّعه الجهاز بعد البصمة أو رمز PIN (PIN)، ثم يتحقق الخادم من التوقيع (signature). مفاتيح المرور **مقاومة للتصيّد** (phishing-resistant): يربط المتصفح كل بيانات اعتماد بنطاقك (ما يسمى "معرّف الطرف المعتمد")، لذلك لا يستطيع موقع مشابه (look-alike site) طلب توقيع لبيانات اعتماد Beacon. قدّمها بجانب البريد الإلكتروني، لا كباب وحيد، إلى أن تلحق أجهزة مستخدميك بها.

### 🔴 على نطاق واسع وللمؤسسات

**إدارة الجلسات (session management) تصبح ميزة (feature).** يتوقع المستخدمون (users) صفحة "أين سجّلت الدخول" تسرد الأجهزة، مع زر "تسجيل الخروج من كل مكان (log out everywhere)". هذا بسيط جدًا مع الجلسات على الخادم (`DELETE FROM sessions WHERE user_id = $1`) ومؤلم مع JWT طويل العمر (long-lived). غيّر (rotate) رمز الجلسة عند تسجيل الدخول وكلما تغيّرت الصلاحيات (privilege)، لتتجنب تثبيت الجلسة (Session Fixation)، وهو أن يزرع المهاجم رمزًا معروفًا في متصفح الضحية قبل أن تسجّل الدخول.

**المصادقة المعزّزة** (Step-up Authentication). بعض الإجراءات (actions) تستحق إثباتًا جديدًا: تغيير بريد الحساب، وتعطيل MFA (disabling MFA)، وإنشاء مفتاح API (API key)، وحذف منظمة (org). سجّل `authenticated_at` في الجلسة، واطلب إعادة المصادقة (re-authentication) إذا مضى عليه أكثر من بضع دقائق.

**سرقة الرموز (token theft) هي الهجوم الحديث.** مع انتشار MFA، صار المهاجمون يسرقون *كوكيز الجلسات* من الأجهزة المصابة (infected machines)، أو يمرّرون عمليات الدخول (logins) عبر وسطاء تصيّد (phishing proxies). ضع الدفاعات في طبقات: مهل خمول (idle timeouts) قصيرة لمناطق الإدارة (admin areas)، وتنبيهات (alerts) عند تغيّر الجهاز، ومفاتيح المرور (التي لا يستطيع الوسطاء تمريرها)، وإلغاء سريع (revocation).

**أين يعيش كود المصادقة (auth code)** هو القرار المعماري (architectural choice) الكبير:

| النهج (approach) | أمثلة | ما تملكه | المقايضة (trade-off) |
|---|---|---|---|
| مكتبة داخل تطبيقك | Better Auth، Auth.js، Devise، django-allauth | كل شيء، في قاعدة بياناتك | أكبر قدر من التحكم، وأنت من يرقّعها (patch) ويشغّلها |
| خادم مصادقة (auth server) تستضيفه بنفسك (self-hosted) | Keycloak، Ory Kratos، Zitadel، Logto، SuperTokens | خدمة منفصلة (separate service) | حدود واضحة (boundary)، وشيء إضافي عليك تشغيله |
| خدمة مُدارة (managed service) | Clerk، Auth0، WorkOS AuthKit، Supabase Auth، Firebase Auth، Stytch | الإعدادات (configuration) | الأسرع، مع تسعير (pricing) لكل مستخدم نشط شهريًا (MAU) وارتباط بالمزوّد (vendor lock-in) |

الارتباط بالمزوّد (Lock-in) يتعلق في الغالب **بتجزئات كلمات المرور (password hashes) ومعرّفات المستخدمين (user IDs)**. تأكد أن المزوّد يصدّر التجزئات بصيغة قياسية، واحتفظ بجدول `users` خاص بك مفتاحه معرّفك أنت، مع معرّف المزوّد (provider id) كعمود (column).

## 🏆 أفضل المستودعات

| المستودع (repo) | ما هو | التقنيات | الترخيص (licence) | اختره عندما (Pick it when) |
|---|---|---|---|---|
| [better-auth/better-auth](https://github.com/better-auth/better-auth) | مكتبة مصادقة (auth library) مستقلة عن الإطار (framework-agnostic) مع إضافات (plugins) للمنظمات (organizations)، و2FA، ومفاتيح المرور (passkeys)، والروابط السحرية | TypeScript | MIT | تبدأ تطبيق TypeScript جديدًا وتريد المصادقة داخل قاعدة بياناتك |
| [nextauthjs/next-auth](https://github.com/nextauthjs/next-auth) | Auth.js، مكتبة المصادقة العريقة القائمة على OAuth لـ Next.js وغيره | TypeScript | ISC | تصون تطبيقًا قائمًا على Auth.js، أما المشاريع الجديدة فلتنظر إلى Better Auth |
| [lucia-auth/lucia](https://github.com/lucia-auth/lucia) | مُلغاة كمكتبة، وصارت الآن دليلًا لتنفيذ الجلسات بنفسك | TypeScript | MIT | تريد فهم الجلسات جيدًا أو كتابة تنفيذ صغير ونظيف |
| [supabase/auth](https://github.com/supabase/auth) | خادم المصادقة وراء Supabase (نسخة متفرعة (fork) من GoTrue الخاص بـ Netlify) | Go | MIT | تستخدم Supabase، أو تريد واجهة مصادقة (auth API) صغيرة قائمة على JWT لتدرسها |
| [ory/kratos](https://github.com/ory/kratos) | خادم هوية بلا واجهة: التسجيل، والدخول، والاستعادة، وMFA، ومفاتيح المرور | Go | Apache-2.0 | تريد خدمة هوية (identity service) منفصلة تعتمد على API أولًا وتستضيفها بنفسك |
| [keycloak/keycloak](https://github.com/keycloak/keycloak) | خادم كامل لإدارة الهوية والوصول مع واجهة إدارة (admin UI) | Java | Apache-2.0 | تحتاج كل شيء (OIDC، SAML، الاتحاد) وتستطيع تشغيل خدمة JVM |
| [logto-io/logto](https://github.com/logto-io/logto) | منصة مصادقة (auth platform) مع واجهة دخول مستضافة، ومنظمات، وSSO للمؤسسات (enterprises) | TypeScript | MPL-2.0 | تريد بديلًا لـ Auth0 تستضيفه بنفسك بواجهة حديثة |
| [supertokens/supertokens-core](https://github.com/supertokens/supertokens-core) | نواة مصادقة (auth core) قابلة للاستضافة الذاتية (self-hosting) مع SDK لأطر عمل (frameworks) كثيرة | Java | Apache-2.0 | تريد SDK بأسلوب الخدمات المُدارة (managed services) لكن على بنيتك التحتية (infrastructure) |
| [pennersr/django-allauth](https://github.com/pennersr/django-allauth) | حزمة (package) Django القياسية للحسابات وتسجيل الدخول الاجتماعي وMFA | Python | MIT | تعمل على Django |
| [heartcombo/devise](https://github.com/heartcombo/devise) | محرك المصادقة (engine) الكلاسيكي في Rails | Ruby | MIT | تعمل على Rails (يأتي Rails 8 أيضًا بمولّد (generator) مدمج أبسط) |

**إن درست مستودعًا واحدًا فقط (If you only study one):** اقرأ **lucia-auth/lucia**. إنه قصير، ويشرح *لماذا* يوجد كل جزء من نظام الجلسات (توليد الرمز (token generation)، والتجزئة، وانتهاء الصلاحية، والتجديد المنزلق (sliding renewal)، وCSRF)، ومكتوب لمن يريد أن يفهم لا لمن يريد أن يضبط الإعدادات (settings) فقط. بعد ذلك اعتمد Better Auth أو المكتبة القياسية (standard library) في إطار عملك وأنت تعرف ما تفعله من الداخل.

**اشترِ أم ابنِ أم استضف بنفسك (Buy, build, or self-host)؟**

- **اشترِ (buy)** (Clerk، Auth0، WorkOS AuthKit، Stytch، Supabase Auth، Firebase Auth) عندما يكون الوصول السريع إلى السوق (time-to-market) هو الأهم وتريد واجهة جاهزة (ready-made UI) وMFA ومفاتيح المرور من اليوم الأول. راقب منحنى التسعير (pricing curve) لكل مستخدم وشروط التصدير (export terms).
- **استضف بنفسك (self-host)** عندما يجب أن تبقى بيانات الهوية في بنيتك التحتية، أو عندما تقدّم منتجًا قابلًا للاستضافة الذاتية (الدرس 7.4) ولا يمكنك الاعتماد على مزوّد SaaS (SaaS provider).
- **ابنِ** (build) فوق مكتبة في معظم منتجات B2B SaaS. تحتفظ بالمستخدمين في Postgres الخاص بك، وتتجنب مع ذلك كتابة التشفير (crypto). لا تكتب بنفسك أبدًا كود تجزئة كلمات المرور (password hashing) أو بروتوكول OAuth.

## 🔍 ادرسه في مشاريع حقيقية (Study it in the wild)

**openstatusHQ/openstatus** مراقِب توفر (uptime monitor) وصفحة حالة مفتوح المصدر (open-source)، أي أنه Beacon حقيقي حرفيًا. وهو مستودع أحادي (Monorepo) بلغة TypeScript. افتح `apps/web`، وافحص ملف `package.json` لترى مكتبة المصادقة التي اختارها، ثم ابحث في الكود عن `auth` و`session`. ما يتقنه هو التناسب (proportion): المصادقة ركن صغير وممل من الكود، وهذا بالضبط مكانها الصحيح في منتج قيمته في المراقبة (monitoring).

**calcom/cal.diy** يُظهر المصادقة على نطاق واسع في مستودع Next.js أحادي (Next.js monorepo): بيانات الاعتماد، وتسجيل الدخول عبر Google، والمصادقة الثنائية (two-factor authentication) (أُزيل منه SAML SSO مع بقية ميزات المؤسسات (enterprise features) حين صارت النسخة مفتوحة المصدر (open-source edition) Cal.diy في 2026). ابحث عن `NextAuth` أو `authOptions` لتجد إعداد (setup) المزوّدين (providers)، وعن `twoFactor` لترى كيف تُضاف TOTP فوق الدخول ببيانات الاعتماد. ويُظهر مخطط (schema) Prisma في `packages/prisma` كيف تقع حقول الهوية (identity fields) على نموذج (model) `User`.

**nextjs/saas-starter** أصغر مثال كامل: بريد وكلمة مرور مع bcrypt، وكوكي جلسة (session cookie) موقّع عبر `jose`، وطبقة وسيطة (Middleware) تحمي المسارات. اقرأه كله في أمسية. يُظهر مقايضة الكوكيز الموقّعة (signed cookies) عديمة الحالة: بسيطة، لكن بلا قائمة إلغاء (revocation list) على الخادم (server-side).

**documenso/documenso** يتعامل مع المصادقة في منتج للهوية فيه معنى قانوني (التوقيعات الإلكترونية). ابحث عن `passkey` و`two-factor` لترى WebAuthn وTOTP، وعن `signin` في تطبيق الويب لتجد المسارات.

**ما الذي تلاحظه (What to notice):**

- أين تُخزَّن الجلسة (صف (row) في قاعدة البيانات (database row)، أو Redis، أو كوكي موقّع) وماذا يعني ذلك لـ "تسجيل الخروج من كل مكان".
- كيف تُربط حسابات OAuth بالمستخدمين: بمعرّف المستخدم لدى المزوّد، أو بالبريد، أو بكليهما، وهل يُفحص "البريد الموثَّق (verified email)".
- هل رموز الاستعادة (reset tokens) والتحقق والروابط السحرية مُجزَّأة عند التخزين وصالحة لمرة واحدة.
- كيف تستجيب نقاط الدخول والاستعادة لبريد غير معروف.
- أين تُفرض (enforced) MFA: في مسار الدخول فقط، أم يُعاد فحصها عند الإجراءات الحساسة (sensitive actions).

## 🛠️ ابنِه في Beacon (Build it into Beacon)

### 🟢 تمرين المبتدئ (Beginner exercise)

أضف التسجيل وتسجيل الدخول بالبريد وكلمة المرور إلى Beacon باستخدام Better Auth (أو Devise، أو django-allauth، أو حزم البداية (starter kits) في Laravel حسب بيئتك). احمِ صفحات `/monitors` بحيث يُعاد توجيه غير المسجّلين إلى `/login`. أضف زر تسجيل خروج يحذف الجلسة من الخادم.

**يكتمل عندما (Done when):**
- تُخزَّن كلمات المرور كتجزئات argon2id أو bcrypt. ابحث في نسخة من قاعدة البيانات (database dump) عن كلمة مرور تجريبية (test password) فلا تجد شيئًا.
- كوكي الجلسة `HttpOnly`، و`Secure` في بيئة الإنتاج (production)، و`SameSite=Lax`.
- بعد تسجيل الخروج، إعادة إرسال (replaying) الكوكي القديم عبر `curl` تُرجع إعادة توجيه (redirect) أو 401.

### 🟡 تمرين المستوى المتوسط (Intermediate exercise)

أضف "تسجيل الدخول عبر GitHub" ومسار استعادة كلمة المرور. اربط هوية GitHub بمستخدم موجود فقط عندما يقول GitHub إن البريد موثَّق *و*يؤكد المستخدم ذلك بتسجيل الدخول بطريقته الحالية. اجعل نقطة طلب الاستعادة (reset-request endpoint) تُرجع الرد نفسه للبريد المعروف وغير المعروف.

**يكتمل عندما (Done when):**
- يستخدم مسار OAuth منحة رمز التفويض مع PKCE ويتحقق من `state`.
- رموز الاستعادة مُجزَّأة في قاعدة البيانات، وتنتهي خلال ساعة، وتفشل عند الاستخدام الثاني.
- الاستعادة المكتملة تُخرج كل الجلسات الأخرى لذلك المستخدم.
- نصوص الردود (response bodies) على "استعد كلمة المرور" متطابقة بايتًا ببايت للبريد الموجود وغير الموجود.

### 🔴 تمرين المستوى المتقدم (Advanced exercise)

أضف مفاتيح المرور وTOTP كعوامل ثانية (second factors)، وصفحة "الأجهزة المسجّل منها (signed-in devices)"، وإعادة مصادقة معزّزة (step-up re-authentication) لإجراءي "إنشاء مفتاح API" و"حذف المنظمة (deleting the org)". حدّد معدل تسجيل الدخول لكل IP ولكل حساب باستخدام Redis.

**يكتمل عندما (Done when):**
- يستطيع المستخدم تسجيل مفتاح مرور والدخول به دون كلمة مرور.
- تفعيل (enabling) TOTP يُصدر عشرة رموز استرداد مُجزَّأة وصالحة لمرة واحدة.
- إلغاء جهاز من صفحة الأجهزة (devices page) يجعل الطلب التالي من ذلك المتصفح غير مُصادَق (unauthenticated).
- عشرون محاولة دخول (login attempt) فاشلة في دقيقة لحساب واحد تؤدي إلى إبطاء أو CAPTCHA، لا إلى قفل دائم (permanent lockout).

## ⚠️ أخطاء يقع فيها المبتدئون (Mistakes juniors make)

- **تخزين JWT في `localStorage`.** أي ثغرة XSS، حتى في سكربت من طرف ثالث (third-party script)، تستطيع قراءته وإرساله. استخدم كوكي `HttpOnly`، ولتطبيق الويب الخاص بك استخدم جلسة على الخادم (server-side session).
- **تجزئة كلمات المرور (password hashing) بـ SHA-256 أو MD5، حتى مع الملح (salt).** إنها سريعة، لذلك تُكسر (cracked) التجزئات المسرّبة بالجملة على بطاقات الرسوميات (GPUs). استخدم argon2id أو bcrypt عبر مكتبة مُصانة (maintained).
- **مطابقة حسابات OAuth بالبريد (email) وحده.** ادعاءات البريد (email claims) غير الموثَّقة أو القابلة للتغيير تسمح للمهاجم بالدخول باسم شخص آخر. خزّن `(provider, provider_user_id)` وعامل البريد كتلميح فقط (hint).
- **رموز (tokens) استعادة وروابط سحرية (magic links) تعيش إلى الأبد أو تعمل مرتين.** الرسائل القديمة تُعاد توجيهها وتُؤرشف وتتسرّب. جزّئها (hash them)، واجعلها تنتهي خلال دقائق، واحذفها عند الاستخدام.
- **كشف وجود الحسابات.** رسالة "لا يوجد مستخدم بهذا البريد" عند الدخول أو الاستعادة تعطي المهاجمين قائمة أهداف (target list) مجانية. استخدم رسالة عامة واحدة وتوقيتًا شبه ثابت.
- **تسجيل خروج (logout) يكتفي بمسح الكوكي (cookie).** إذا بقي الرمز صالحًا على الخادم، فكل من نسخه يبقى داخلًا. احذف صف الجلسة (session row).

## 🧾 الخلاصة (Recap)

- المصادقة مجموعة من المسارات: التسجيل، والدخول، والتحقق، والاستعادة، وMFA، وتسجيل الخروج. أمّنها كلها بالقدر نفسه.
- جزّئ كلمات المرور بـ argon2id أو bcrypt. ولا تخزّن من رموز الجلسات والاستعادة والروابط السحرية إلا تجزئاتها.
- الجلسات على الخادم في كوكي `HttpOnly` و`Secure` و`SameSite=Lax` هي الخيار الافتراضي. أما JWT فللتحقق بين الخدمات (services).
- تسجيل الدخول الاجتماعي يعني رمز التفويض (authorization code) مع PKCE، مع ربط الهوية بمعرّف المستخدم لدى المزوّد، وليس بالبريد وحده أبدًا.
- مفاتيح المرور مقاومة للتصيّد وهي المستقبل. وTOTP مع رموز الاسترداد هو MFA المتين اليوم.
- استخدم مكتبة أو خدمة للتشفير والبروتوكولات (protocols). مهمتك أن تضبط المسارات والحالات الحدّية (edge cases).

## ✍️ اختبر نفسك (Check yourself)

**1. لماذا يُعد SHA-256 اختيارًا خاطئًا لتجزئة كلمات المرور (password hashing)، وماذا تستخدم بدلًا منه؟**

<details><summary>الإجابة (Answer)</summary>

SHA-256 مصمم ليكون سريعًا، لذلك يستطيع المهاجم الذي يسرق قاعدة البيانات تجربة مليارات التخمينات في الثانية. يجب أن تكون تجزئات كلمات المرور بطيئة عمدًا ومملّحة: استخدم argon2id أو bcrypt. راجع "🟢 الأساسيات".

</details>

**2. مِمَّ يحمي PKCE في مسار رمز التفويض (authorization code flow) في OAuth، ومِمَّ يحمي المعامل (parameter) `state`؟**

<details><summary>الإجابة</summary>

يجعل PKCE رمز التفويض المُعترَض عديم الفائدة، لأن استبداله يتطلب `code_verifier` الأصلي الذي لا يملكه إلا Beacon. ويربط المعامل `state` طلب العودة بالمتصفح الذي بدأ المسار، وهذا يمنع CSRF في تسجيل الدخول. راجع "🟡 التعمق أكثر".

</details>

**3. أبلغ عميل (customer) لدى Beacon أن حاسوبه المحمول سُرق، وطلب منك تسجيل خروجه من كل مكان. لماذا يكون هذا سهلًا مع الجلسات على الخادم (server-side sessions) وصعبًا مع JWT طويل العمر (long-lived)؟**

<details><summary>الإجابة</summary>

مع الجلسات على الخادم، تسجيل الخروج من كل مكان هو عملية حذف واحدة لصفوف جلسات (session rows) ذلك المستخدم، ويفشل الطلب التالي بأي كوكي قديم. أما JWT فيبقى صالحًا حتى ينتهي لأن الخادم لا يبحث عنه، لذلك تحتاج إلى قائمة حظر، وهي جلسة بخطوات إضافية. راجع "الجلسات مقابل JWT" و"🔴 على نطاق واسع وللمؤسسات".

</details>

**4. يقول عملاء (customers) Beacon من فرق أمن المعلومات (IT-security) إن روابطهم السحرية (their magic links) "لا تعمل أبدًا": الرابط يقول إنه استُخدم من قبل. ما الذي يحدث، وكيف تصلحه؟**

<details><summary>الإجابة</summary>

ماسحات أمان البريد في الشركات تفتح الروابط لفحصها، فتستهلك الرمز ذا الاستخدام الواحد قبل أن ينقر الإنسان. اجعل الرابط يفتح صفحة فيها زر "تسجيل الدخول" يرسل طلب POST، أو أرسل رمزًا قصيرًا يكتبه المستخدم بدلًا منه. راجع "الروابط السحرية" في "🟡 التعمق أكثر".

</details>

**5. كتب زميل نقطة الاستعادة (reset endpoint) بحيث تُرجع "لا يوجد حساب بهذا البريد (email)" للعناوين غير المعروفة و"تم إرسال رابط الاستعادة (reset link)" لغيرها. ما الذي يتعطّل؟**

<details><summary>الإجابة</summary>

هذا تعداد للحسابات: يستطيع المهاجمون معرفة أي عناوين بريد تخص عملاء Beacon وبناء قوائم أهداف. أرجع رسالة واحدة متطابقة ("إذا كان هناك حساب، فقد أرسلنا رابطًا")، ونفّذ العمل البطيء حتى عندما يكون المستخدم غير موجود حتى لا يكشف التوقيت شيئًا. راجع "🟡 التعمق أكثر" و"⚠️ أخطاء يقع فيها المبتدئون".

</details>

## 📚 المراجع (References)

- OWASP Cheat Sheet Series: Authentication, Password Storage, and Session Management cheat sheets — https://cheatsheetseries.owasp.org (أوراق OWASP المرجعية للمصادقة وتخزين كلمات المرور وإدارة الجلسات)
- NIST SP 800-63B, Digital Identity Guidelines: Authentication and Lifecycle Management — https://pages.nist.gov/800-63-4/ (إرشادات NIST للهوية الرقمية)
- RFC 6749, The OAuth 2.0 Authorization Framework — https://www.rfc-editor.org/rfc/rfc6749
- RFC 7636, Proof Key for Code Exchange (PKCE) — https://www.rfc-editor.org/rfc/rfc7636
- RFC 9700, Best Current Practice for OAuth 2.0 Security — https://www.rfc-editor.org/rfc/rfc9700 (أفضل الممارسات الحالية لأمان OAuth 2.0 (RFC 9700))
- OpenID Connect Core 1.0 — https://openid.net/specs/openid-connect-core-1_0.html
- W3C Web Authentication and the passkeys developer site — https://www.w3.org/TR/webauthn/ and https://passkeys.dev (مواصفة WebAuthn وموقع مطوري مفاتيح المرور)
- Lucia's guide to sessions — https://lucia-auth.com (دليل Lucia للجلسات)

---

# 1.2 — المستخدمون والمنظمات والدعوات: هيكل تعدد المستأجرين

*المستوى: 🟢 مبتدئ* · *المتطلبات (Prerequisites): 1.1*

## ⚡ الدرس في دقيقة (In 60 seconds)

- في B2B SaaS العميل منظمة، وليس شخصًا. ينضم المستخدمون إليها عبر عضويات (memberships) تحمل دورًا (role).
- القاعدة الأهم: كل صف يملكه المستأجر (tenant-owned row) يحمل `org_id` مباشرة، والموارد (resources) ملك للمنظمة، لا للمستخدم أبدًا.
- الخيار الافتراضي للنسخة الأولى (v1): أربعة جداول (tables) (المستخدمون، والمنظمات، والعضويات، والدعوات)، ومنظمة شخصية (personal org) تُنشأ عند التسجيل، ومعرّف المنظمة النصي (Slug) في الرابط (URL).
- عامل معرّف المنظمة (org id) القادم من الرابط أو الكوكي كادعاء: اجلب العضوية مع كل طلب.
- الفخ الأكبر: موارد يملكها المستخدمون، وهذا يحوّل كل ميزة فريق (team feature) لاحقة إلى عملية ترحيل (migration) أو حل ترقيعي (hack).

## 🧭 لماذا يحتاجه كل SaaS

وضعت النسخة الأولى من Beacon الحقل (field) `user_id` على كل مراقِب. عمل ذلك بشكل رائع لمدة أسبوع. ثم سجّلت Priya من Acme، وأنشأت اثني عشر مراقِبًا، وسألت كيف يستطيع زميلها المناوب (on-call) رؤيتها. ثم سألت كيف تزيل متعاقدًا (contractor) دون حذف المراقِبات التي أنشأها. ثم طلب فريق (team) المالية لديها أن تصدر فاتورة (billed) واحدة للشركة، لا فاتورة (invoice) لكل مهندس. ثم ذهبت Priya في إجازة ولم يستطع أحد تغيير أي شيء.

لكل هذه الطلبات السبب الجذري (root cause) نفسه: **العميل (customer) ليس شخصًا، بل مجموعة من الأشخاص.** البرمجيات الموجهة للشركات (B2B) تشتريها الشركات، وتستخدمها الفرق (teams)، وتبقى بعد رحيل أي موظف. إذا كانت الموارد ملكًا للمستخدمين، فكل ميزة فريق تصبح ترقيعًا: كلمات مرور مشتركة (shared passwords)، وسكربتات "انقل كل أشيائي"، وفواتير تُطابق يدويًا.

الحل نموذج بيانات (data model) صغير يصل إليه تقريبًا كل B2B SaaS: **المستخدمون (users)** ينتمون إلى **المنظمات (organizations)** عبر **العضويات (memberships)**، وكل ما ينشئه المنتج ملك للمنظمة. المنظمة هي **المستأجر**، أي وحدة العزل (isolation) والفوترة (billing) والملكية (ownership). يسميها Slack مساحة عمل (Workspace)، وGitHub منظمة، وDub مساحة عمل، وCal.com فريقًا أو منظمة. الاسم يختلف، والشكل لا يختلف.

**الموارد (resources) ملك للمنظمة (organization)، والأشخاص ينتمون إلى المنظمة عبر العضويات (memberships)، ولا شيء ملك للمستخدم (user) إلا بيانات دخوله (its login credentials).**

## 📐 كيف يعمل

### 🟢 الأساسيات

أربعة مصطلحات نعرّفها بعناية لأن المنتجات تستخدمها بشكل غير متسق:

| المصطلح | ما هو | مثال من Beacon |
|---|---|---|
| المستخدم | هوية بشرية تستطيع تسجيل الدخول. عامة، وليست خاصة بعميل. | `priya@acme.com` |
| المنظمة | العميل. تملك البيانات وتدفع الفاتورة. | "Acme Inc" |
| العضوية | الرابط بين مستخدم ومنظمة، ويحمل دورًا. | Priya هي `owner` في Acme |
| الدعوة (Invitation) | عضوية معلّقة لشخص لم يقبل بعد. | دعوة `sam@acme.com` بدور `member` |

تحذير بشأن كلمة **"account"**. في Auth.js وBetter Auth يمثل صف `account` طريقة دخول مرتبطة، مثل "هوية GitHub لهذا المستخدم". في Chatwoot وكثير من تطبيقات Rails، `Account` هو *المستأجر*. وفي أنظمة الفوترة تعني العميل الذي يدفع. عندما تقرأ قاعدة كود (codebase)، اعرف أي معنى تستخدمه قبل أن تثق بحدسك.

هذا هو النموذج الأساسي (core model) في Beacon:

```mermaid
erDiagram
    USER ||--o{ MEMBERSHIP : "يملك (has)"
    ORGANIZATION ||--o{ MEMBERSHIP : "يملك (has)"
    ORGANIZATION ||--o{ INVITATION : "تُصدر (issues)"
    USER ||--o{ INVITATION : "دعا (invited by)"
    ORGANIZATION ||--o{ MONITOR : "تملك (owns)"
    ORGANIZATION ||--o{ STATUS_PAGE : "تملك (owns)"
    MONITOR ||--o{ CHECK_RESULT : "يسجّل (records)"
    USER {
        uuid id PK
        string email UK
        timestamp email_verified_at
    }
    ORGANIZATION {
        uuid id PK
        string slug UK
        string name
        string stripe_customer_id
    }
    MEMBERSHIP {
        uuid org_id FK
        uuid user_id FK
        string role
        timestamp created_at
    }
    INVITATION {
        uuid id PK
        uuid org_id FK
        string email
        string role
        string token_hash
        timestamp expires_at
    }
    MONITOR {
        uuid id PK
        uuid org_id FK
        uuid created_by FK
        string url
    }
    CHECK_RESULT {
        uuid id PK
        uuid org_id FK
        uuid monitor_id FK
        int status_code
    }
```

ثلاث تفاصيل في هذا المخطط (diagram) مقصودة.

أولًا، على `MEMBERSHIP` قيد تفرّد (unique constraint) على `(org_id, user_id)`: دور واحد لكل شخص في كل منظمة. ويمكن أن يكون المستخدم في منظمات كثيرة، وهذا طبيعي للمستشارين والوكالات وأي شخص لديه مشروع جانبي (side project).

ثانيًا، يُحتفظ بـ `MONITOR.created_by` للتاريخ والعرض، لكن الملكية هي `org_id`. عندما يغادر المتعاقد، تبقى مراقِباته.

ثالثًا، يحمل `CHECK_RESULT` الحقل `org_id` مع أنك تستطيع الوصول إلى المنظمة عبر المراقِب. هذه هي **قاعدة tenant_id (the tenant_id rule): كل صف يملكه المستأجر (tenant-owned row) يحمل معرّف المستأجر (tenant id) مباشرة.** وهذا يعني أن كل استعلام (query) يستطيع التصفية (filter) حسب المنظمة دون ربط (Join)، وأن كل فهرس (index) يمكن أن يبدأ بـ `org_id`، وأن غياب `WHERE org_id = ...` يظهر بوضوح في مراجعة الكود (code review). كما يفتح الباب لاحقًا لأمان مستوى الصف (Row-Level Security) في Postgres وللتجزئة الأفقية (Sharding) (الدرس 2.4). تكرار (denormalising) عمود uuid واحد رخيص. أما أن تكتشف أن أكبر جداولك لا يمكن تصفيته حسب المستأجر فليس رخيصًا.

**مساحات العمل الشخصية (personal workspaces).** ماذا يحدث مباشرة بعد التسجيل؟ لديك خياران معقولان. إما أن تنشئ منظمة تلقائيًا ("مساحة عمل Priya") فيصل المستخدم إلى منتج يعمل، أو أن تمرّره بخطوة إعداد (onboarding) قصيرة "سمِّ فريقك". كلاهما يحافظ على الثابت الأساسي (invariant): *لا يوجد شيء اسمه مورد (resource) بلا منظمة.* تجنّب الخيار الثالث، حيث يملك المستخدمون الأفراد الموارد مباشرة وتُضاف الفرق لاحقًا. هذا يعطيك مسارين في الكود (code paths) لكل ميزة إلى الأبد.

### 🟡 التعمق أكثر

**الدعوات (invitations)** تبدو بسيطة وتخفي قرارات كثيرة. دورة حياتها (lifecycle):

```mermaid
stateDiagram-v2
    state "معلّقة" as Pending
    state "مقبولة" as Accepted
    state "ملغاة" as Revoked
    state "منتهية" as Expired
    [*] --> Pending: المسؤول يدعو بريدًا (admin invites email)
    Pending --> Accepted: المدعو يقبل ببريد مطابق (invitee accepts with matching email)
    Pending --> Revoked: المسؤول يلغي (admin cancels)
    Pending --> Expired: مرور expires_at (expires_at passes)
    Pending --> Pending: إعادة الإرسال برمز جديد (resend with new token)
    Accepted --> [*]
    Revoked --> [*]
    Expired --> [*]
```

قواعد الرمز هي نفسها قواعد رموز الاستعادة من الدرس 1.1: عشوائي، ومخزّن كتجزئة، وله مدة صلاحية (expiring) (7 أيام شائعة)، وصالح لمرة واحدة. أما القرارات الخاصة بالدعوات فهي:

- **هل يجب أن يطابق بريدُ المستخدم (user) الذي يقبل البريدَ المدعو (invited email)؟** المطابقة أكثر أمانًا (security): لا يستطيع الشخص الخطأ استخدام دعوة أُعيد توجيهها (forwarded invite). وعدم المطابقة ألطف: للناس عناوين عمل وعناوين شخصية. اختيار Beacon هو اشتراط المطابقة، وإذا كان البريد المسجّل به مختلفًا، يقول ذلك بوضوح ويعرض تبديل الحساب (switch accounts). وإذا سمحت بعدم المطابقة، فعلى الأقل أظهر للمسؤول (admin) من الذي قبل فعلًا.
- **المستخدمون الجدد مقابل الموجودين (New versus existing users).** يجب أن يعمل الرابط نفسه للاثنين. إذا لم يكن للبريد حساب، يأتي التسجيل أولًا ثم القبول، مع ملء البريد مسبقًا (pre-filled) واعتباره موثَّقًا بحكم النقر على الرابط.
- **رسائل الدعوة المزعجة (invite spam).** الدعوات ترسل بريدًا من نطاقك إلى عناوين عشوائية. حدّد معدلها لكل منظمة، ولا تسمح للمستخدمين غير الموثَّقين بإرسالها، وإلا صارت سمعة الإرسال (sending reputation) لديك (الدرس 4.1) أداة تصيّد لشخص آخر.
- **تصعيد الأدوار (role escalation).** يجب ألا يستطيع المسؤول دعوة شخص بدور `owner` إذا كان المسؤولون أنفسهم لا يستطيعون أن يصبحوا مالكين (owners). تحقّق أن الداعي (inviter) يملك على الأقل الدور الذي يمنحه (الدرس 1.3).

قبول الدعوة معاملة (Transaction) صغيرة:

```ts
export async function acceptInvite(rawToken: string, user: { id: string; email: string }) {
  return db.$transaction(async (tx) => {
    const invite = await tx.invitation.findUnique({ where: { tokenHash: sha256(rawToken) } });
    if (!invite || invite.expiresAt < new Date() || invite.acceptedAt) {
      throw new Error("Invitation is invalid or expired");
    }
    if (invite.email.toLowerCase() !== user.email.toLowerCase()) {
      throw new Error("This invitation was sent to a different email");
    }
    await tx.membership.upsert({
      where: { orgId_userId: { orgId: invite.orgId, userId: user.id } },
      create: { orgId: invite.orgId, userId: user.id, role: invite.role },
      update: {}, // already a member: keep the existing role
    });
    await tx.invitation.update({ where: { id: invite.id }, data: { acceptedAt: new Date() } });
    return invite.orgId;
  });
}
```

**التبديل بين المنظمات (org switching).** أين تعيش "المنظمة الحالية (current organization)"؟ هناك تصميمان (two designs) شائعان:

| التصميم (design) | مثال على الرابط | الإيجابيات (pros) | السلبيات (cons) |
|---|---|---|---|
| المنظمة في الرابط | `/acme/monitors/123` | روابط قابلة للمشاركة (shareable links)، ومنظمتان في تبويبين (tabs)، ووضوح في السجلات (logs) | كل مسار (route) يأخذ المعرّف النصي |
| المنظمة في الجلسة | `/monitors/123` مع كوكي "المنظمة الحالية" | روابط أقصر | التبويبات تتعارض، والروابط الملصوقة (pasted links) تتعطل لمن ينتمي لعدة منظمات |

فضّل الرابط. وفي الحالتين، **معرّف المنظمة (org id) القادم من الرابط أو الكوكي (cookie) ادعاء (claim)، وليس حقيقة.** في كل طلب، اجلب العضوية للزوج `(المنظمة، المستخدم الحالي)` وارفض الطلب إذا لم تكن موجودة. هذا البحث الواحد (lookup) هو الأساس الذي يبني عليه الدرس 1.3.

**المغادرة والإزالة والملكية (Leaving, removal and ownership).** اكتب هذه الثوابت (invariants) في الكود، لا في الأمنيات:

- للمنظمة دائمًا مالك (owner) واحد على الأقل. لا يستطيع آخر مالك (last owner) المغادرة (leaving) أو خفض دوره (demoted) حتى ينقل الملكية.
- **نقل الملكية (ownership transfer)** إجراء (action) مقصود ومؤكَّد، ويفضّل أن يتطلب مصادقة معزّزة وبريدًا للطرفين. وغالبًا ما ينقل معه أيضًا مسؤولية الفوترة.
- إزالة عضو (member) تحذف عضويته وتلغي (revokes) كل ما كان يعمل باسمه في تلك المنظمة: رموز API الشخصية الخاصة به، والدعوات المعلّقة (pending invitations) التي أرسلها، والجلسات المخزّنة (cached sessions) المرتبطة بالمنظمة.
- **حذف مستخدم (Deleting a user)** يملك منظمات يجب أن يُمنع، أو يجب أولًا نقل تلك المنظمات أو حذفها. وإلا فإنك تنشئ مستأجرين يتامى (orphaned tenants) لا يستطيع أحد إدارتهم.

**حذف منظمة (deleting an org)** هو أكثر الإجراءات تدميرًا في المنتج. اجعله حذفًا ناعمًا (Soft Delete) مع فترة سماح (grace period) (مثلًا 30 يومًا) تكون فيها المنظمة غير متاحة لكن قابلة للاستعادة (restorable). ألغِ الاشتراك (subscription) فورًا، وأوقف فحوص المراقِبات المجدولة، ثم احذف البيانات نهائيًا (hard-delete) عبر مهمة خلفية (Background Job، الدرس 5.1). هذا يغطي أيضًا تذكرة الدعم (support ticket) "متدرّب حذف بيئة الإنتاج".

**المقاعد (seats).** إذا كان التسعير لكل مقعد (per seat)، فالمقعد (seat) عادةً عضوية، وأحيانًا دعوة معلّقة (pending invitation) أيضًا. قرّر أيهما، واكتب ذلك، واجعل عدد المقاعد استعلامًا على العضويات، لا عدّادًا (counter) تزيده وتنسى إنقاصه. يحوّل الدرس 3.2 هذا إلى استحقاقات (Entitlements) وكميات (quantities) في Stripe. يسعّر Beacon حسب عدد المراقِبات لا المقاعد، وهذا أحد أسباب اختياره: التسعير بالمقاعد (per-seat pricing) يعاقب سلوك "ادعُ كل فريق المناوبة (on-call rotation)" الذي تريده.

### 🔴 على نطاق واسع وللمؤسسات

**التسلسل الهرمي (hierarchy).** يريد العملاء الكبار بنية داخل المستأجر: منظمة مؤسسية (enterprise org) تحتوي فرقًا، لكل فريق مراقِباته وصفحات حالته، وأشخاص في عدة فرق بأدوار (roles) مختلفة. يمثّل Cal.com هذا كمنظمات تحتوي فرقًا. أبقِ *حدود الفوترة والعزل* عند المنظمة في المستوى الأعلى، وعامل الفرق كتجميع للصلاحيات (permissions) (الدرس 1.3)، لا كمستأجرين (tenants) منفصلين.

**الاستحواذ على النطاق (domain capture) والانضمام التلقائي (auto-join).** بعد أن تثبت Acme ملكيتها لـ `acme.com` (الدرس 1.4)، يمكن أن يُعرض على المسجّلين الجدد ببريد `@acme.com` خيار "انضم إلى مساحة عمل Acme" بدلًا من إنشاء منظمة شخصية شاردة، وهي منظمة سيجدها فريق تقنية المعلومات في Acme ويشتكي منها. اعرض هذا للنطاقات الموثَّقة (verified domains) فقط، ولا تعرضه أبدًا لمزوّدي البريد العامين.

**نقل الموارد (resources) بين المنظمات (organizations).** العملاء يندمجون وينقسمون ويعيدون تنظيم أنفسهم. ولأن كل صف يحمل `org_id`، فالنقل تحديث لهذا العمود عبر مجموعة معروفة من الجداول داخل معاملة واحدة، مع إدخال في سجل التدقيق (Audit Log، الدرس 7.3). هنا تردّ قاعدة tenant_id ثمنها مرة ثانية.

**العزل على نطاق واسع (isolation at scale).** مع آلاف المستأجرين، تصبح الأسئلة: أين تعيش بيانات المستأجر (جداول مشتركة (shared tables)، أو مخطط لكل مستأجر (schema per tenant)، أو قاعدة بيانات لكل مستأجر)، وكيف تمنع مستأجرًا ضخمًا واحدًا من إبطاء الجميع، وكيف تلتزم بطلب "بياناتنا تبقى في الاتحاد الأوروبي (EU)". هذه موضوعات الدرس 2.4. والخبر الجيد أن وجود `org_id` على كل صف يبقي كل الخيارات مفتوحة: فمثلًا، يوزّع (shards) Citus جداول Postgres حسب عمود توزيع (distribution column)، ومعرّف المستأجر هو الاختيار النموذجي.

## 🏆 أفضل المستودعات

| المستودع | ما هو | التقنيات | الترخيص | اختره عندما |
|---|---|---|---|---|
| [nextjs/saas-starter](https://github.com/nextjs/saas-starter) | قالب (template) SaaS رسمي ومبسّط لـ Next.js فيه فرق ودعوات وأدوار وسجل نشاط (activity log) | TypeScript, Drizzle, Postgres | MIT | تريد أصغر نسخة مقروءة من الهيكل كاملًا |
| [better-auth/better-auth](https://github.com/better-auth/better-auth) | مكتبة مصادقة توفر إضافة المنظمات (organization plugin) فيها المنظمات والأعضاء (members) والأدوار والدعوات | TypeScript | MIT | تريد أن يُولَّد نموذج المنظمات (organization model) لك، داخل قاعدة بياناتك |
| [boxyhq/saas-starter-kit](https://github.com/boxyhq/saas-starter-kit) | قالب بداية بطابع مؤسسي (enterprise-flavoured): فرق، ودعوات، وSSO، ومزامنة الأدلة (directory sync)، وسجلات تدقيق (audit logs)، وويب هوك (webhook) | TypeScript, Next.js, Prisma | Apache-2.0 | تعرف أنك ستبيع للمؤسسات وتريد نماذج (models) فرق جاهزة لـ SSO |
| [calcom/cal.diy](https://github.com/calcom/cal.diy) | SaaS للجدولة (scheduling) يمثّل مخططه مستخدمين وفرقًا ومنظمات تحتوي فرقًا | TypeScript, Prisma | MIT | تريد رؤية تسلسل هرمي (منظمة ثم فريق ثم عضو) في بيئة إنتاج |
| [dubinc/dub](https://github.com/dubinc/dub) | SaaS لإدارة الروابط (link-management) فيه مساحات عمل (workspaces) بمعرّف نصي ودعوات وحدود للخطط (plan limits) | TypeScript, Prisma | AGPL-3.0 | تريد تصميمًا نظيفًا يضع مساحة العمل في الرابط |
| [documenso/documenso](https://github.com/documenso/documenso) | SaaS للتوقيع الإلكتروني (e-signature) فيه منظمات وفرق ودعوات أعضاء (member invitations) | TypeScript, Prisma | AGPL-3.0 | تريد رؤية نموذج فرق (team model) أُضيف إلى منتج بدأ لمستخدم واحد |
| [logto-io/logto](https://github.com/logto-io/logto) | منصة مصادقة فيها منظمات وأدوار منظمات ودعوات مدمجة | TypeScript | MPL-2.0 | تريد أن تتولى خدمة هوية مستضافة ذاتيًا المنظمات بدلًا من تطبيقك |
| [citusdata/citus](https://github.com/citusdata/citus) | إضافة (extension) لـ Postgres توزّع الجداول على العقد (nodes) حسب عمود | C | AGPL-3.0 | تخطط لنطاق ضخم (huge scale) جدًا من المستأجرين وتريد أن ترى لماذا يهم وجود `org_id` في كل مكان |

**إن درست مستودعًا واحدًا فقط (If you only study one):** **nextjs/saas-starter**. مخططه كله يتسع في شاشة واحدة: المستخدمون، والفرق، وأعضاء الفرق (team members) مع دور، والدعوات، وسجل النشاط. إنه غير مكتمل (لا يوجد نقل ملكية، وفريق واحد لكل مستخدم في الواجهة (UI))، واكتشاف ما ينقصه تمرين جيد بحد ذاته.

**اشترِ أم ابنِ أم استضف بنفسك (Buy, build, or self-host)؟**

- **اشترِ (buy)** عندما تستخدم أصلًا مزوّد مصادقة مُدارًا يتضمن المنظمات. Clerk وWorkOS وAuth0 وStytch وKinde كلها تمثّل المنظمات والعضويات والدعوات. هذا سريع، لكن أهم علاقة تجارية (business relation) لديك تعيش الآن في قاعدة بيانات المزوّد، لذلك انسخ (mirror) المنظمات والعضويات إلى جداولك عبر الويب هوك.
- **استضف بنفسك (self-host)** خادم هوية (identity server) فيه نموذج منظمات (Logto، Zitadel، منظمات Keycloak) إذا كنت تشغّل واحدًا أصلًا للمصادقة.
- **ابنِ (build)** في معظم الحالات. إنها أربعة جداول وعدد قليل من الثوابت، وهي قلب نموذج النطاق (domain model) لديك، وكل مكوّن آخر (component) (الفوترة، والصلاحيات، والتدقيق (audit)، والحدود) يرتبط بها. إضافة المنظمات في Better Auth طريق وسط جيد: جداول مولَّدة، داخل قاعدة بياناتك.

## 🔍 ادرسه في مشاريع حقيقية

**calcom/cal.diy** يُظهر تسلسلًا هرميًا ناضجًا. افتح `packages/prisma` واقرأ نموذجي `Team` و`Membership` في مخطط Prisma (Prisma schema). المنظمات فرق مع إعدادات منظمة إضافية، والفرق الفرعية (child teams) تشير إلى فريق أب (parent)؛ أُزيلت ميزات المنظمات من النسخة مفتوحة المصدر في 2026، لكن المخطط ما زال يُظهر النموذج. لاحظ كيف تحمل العضويات دورًا وعلامة قبول (acceptance flag) معًا، فتتشارك الدعوة المعلّقة والعضو النشط جدولًا واحدًا. ابحث عن `inviteMember` لتتبع مسار الدعوة (invite flow) من بدايته إلى نهايته.

**dubinc/dub** يضع المعرّف النصي لمساحة العمل (workspace slug) في بداية كل رابط في لوحة التحكم (dashboard)، وهذا يجعل روابط الدعم (support links) والعمل بعدة تبويبات بلا ألم. في وقت كتابة هذا الدرس، احتفظ نموذج Prisma لمساحات العمل بالاسم القديم `Project`، وهذا درس واقعي في أن مفردات المنتج (product vocabulary) تتغير أسرع من المخططات (schemas). ابحث عن `ProjectUsers` و`invite` لتجد العضويات والدعوات، ثم انظر كيف تحدد مسارات API (API routes) مساحة العمل وتتحقق من العضوية قبل أن تفعل أي شيء.

**nextjs/saas-starter** يضع كل شيء في ملف مخطط Drizzle واحد. ابحث عن `teamMembers` و`invitations`. اقرأ إجراء التسجيل (sign-up action) لترى كيف ينشئ المستخدم الجديد فريقًا أو ينضم إلى فريق من دعوة في خطوة واحدة.

**documenso/documenso** أضاف الفرق ثم المنظمات إلى منتج بدأ بمستخدمين أفراد يملكون المستندات، لذلك يُظهر مسار الترحيل (migration path) الذي تريد ألا تحتاج إليه. ابحث في مخطط Prisma عن `Organisation` و`Team` (بالتهجئة البريطانية) وانظر كيف تُحدَّد نطاقات (domains) المستندات.

**ما الذي تلاحظه (What to notice):**

- هل ينشئ كل منتج مساحة عمل شخصية (personal workspace) تلقائيًا عند التسجيل، وكيف يشكّل ذلك تجربة البدء (onboarding experience).
- هل تعيش الدعوات المعلّقة في جدولها الخاص أم كعضويات لم تُقبل بعد.
- كيف تُحدَّد "المنظمة الحالية" في كل طلب، وأين يتم التحقق من العضوية.
- أي الجداول تحمل معرّف المستأجر مباشرة، وأيها يعتمد على الربط.
- ماذا يحدث لبيانات المنظمة عند حذفها: حذف متتالٍ (Cascade)، أو حذف ناعم، أو مهام خلفية (background jobs).

## 🛠️ ابنِه في Beacon

### 🟢 تمرين المبتدئ

أضف جدولي (two tables) `organizations` و`memberships`، وانقل `monitors` من الملكية عبر `user_id` إلى الملكية عبر `org_id`، مع الإبقاء على `created_by`. عند التسجيل، أنشئ منظمة شخصية يكون المستخدم فيها `owner`. ضع المعرّف النصي للمنظمة (org slug) في الرابط: `/[orgSlug]/monitors`.

**يكتمل عندما (Done when):**
- لكل صف مراقِب قيمة `org_id` غير فارغة، وكل استعلام على المراقِبات يصفّي بها.
- زيارة `/some-other-org/monitors` من غير عضو تُرجع 404.
- عملية ترحيل تنقل المراقِبات التي يملكها المستخدمون إلى المنظمة الشخصية لكل مستخدم.

### 🟡 تمرين المستوى المتوسط

ابنِ الدعوات: يُدخل المسؤول بريدًا ودورًا، ويتلقى المدعو (invitee) رابطًا بالبريد، والقبول ينشئ عضوية. ادعم الإلغاء وإعادة الإرسال (resend). أضف أداة تبديل (org switcher) تعرض كل المنظمات التي ينتمي إليها المستخدم.

**يكتمل عندما (Done when):**
- رموز الدعوات (invitation tokens) مُجزَّأة، وتنتهي خلال 7 أيام، ولا يمكن إعادة استخدامها.
- دعوة لـ `sam@acme.com` لا يمكن أن يقبلها مستخدم مسجّل الدخول بـ `sam@gmail.com`.
- يستطيع مستخدم بلا حساب التسجيل من رابط الدعوة (invitation link) ويصل إلى داخل المنظمة.
- معدل الدعوات (invitation rate) محدود لكل منظمة.

### 🔴 تمرين المستوى المتقدم

نفّذ المغادرة، وإزالة العضو (member removal)، ونقل الملكية، وحذف المنظمة مع فترة سماح 30 يومًا. أضف سياسة أمان مستوى الصف في Postgres على `monitors` كخط دفاع أخير (backstop)، بحيث لا يُرجع أي استعلام بلا تصفية (filtering) حسب المنظمة شيئًا.

**يكتمل عندما (Done when):**
- لا يستطيع آخر مالك المغادرة أو خفض دوره (demoting him)، والواجهة تشرح السبب.
- نقل الملكية يتطلب إعادة مصادقة ويرسل بريدًا للطرفين.
- المنظمة المحذوفة غير متاحة فورًا، وقابلة للاستعادة لمدة 30 يومًا، وتُحذف نهائيًا (hard-deleted) بعدها عبر مهمة مجدولة (scheduled job).
- مع تفعيل RLS، يُرجع `SELECT * FROM monitors` من دور قاعدة البيانات (database role) الخاص بالتطبيق صفوف (rows) المنظمة الحالية فقط.

## ⚠️ أخطاء يقع فيها المبتدئون

- **موارد يملكها المستخدمون (users).** يبدو هذا أبسط حتى يأتي أول عميل فريق. ضع `org_id` على الموارد من اليوم الأول، حتى لو كان لكل منظمة عضو واحد.
- **الثقة بمعرّف المنظمة (org id) القادم من العميل (coming from the client).** يجب أن يفشل طلب `/acme/monitors` من شخص ليس في Acme. ابحث عن العضوية على الخادم في كل طلب، وأرجع 404 بدلًا من 403 حتى لا تكشف أن المنظمة موجودة.
- **معرّف المستأجر (tenant id) على الجدول (table) الأعلى فقط.** إذا كان `check_results` لا يصل إلى منظمته إلا عبر `monitors`، فسيكتب أحدهم يومًا استعلامًا ينسى الربط. ضع `org_id` على كل جدول يملكه المستأجر (tenant-owned table) واجعله أول عمود (first column) في فهارسك.
- **دعوات (invitations) يستطيع أي شخص يملك الرابط قبولها، وإلى الأبد.** عندها تصبح الروابط المعاد توجيهها (forwarded links) والمسرّبة أبوابًا خلفية (backdoors). اجعلها تنتهي، واربطها بالبريد المدعو، وأظهر للمسؤولين من قبلها.
- **حذف المنظمات نهائيًا (hard-deleting organizations) بشكل متزامن (synchronously).** ينتهي وقت الطلب (times out) مع المستأجرين الكبار، ولا يمكن التراجع عنه. احذف حذفًا ناعمًا، وألغِ الفوترة، ثم احذف نهائيًا في مهمة خلفية (background job).
- **نسيان قاعدة آخر مالك (last-owner rule).** المنظمة بلا مالك تصبح تذكرة دعم لا يحلها إلا الدخول إلى قاعدة البيانات مباشرة (database console).

## 🧾 الخلاصة

- المستأجر هو المنظمة. ينضم إليها المستخدمون عبر عضويات تحمل دورًا.
- كل صف يملكه المستأجر يحمل `org_id` مباشرة. إنه أرخص تأمين في الدورة كلها.
- الدعوات رموز: مُجزَّأة، ولها مدة صلاحية، وصالحة لمرة واحدة، ويُفضَّل ربطها ببريد.
- ضع المنظمة في الرابط وتحقّق من العضوية في كل طلب.
- اكتب الثوابت في الكود: مالك واحد على الأقل، ونقل ملكية مقصود، وحذف ناعم مع فترة سماح.

## ✍️ اختبر نفسك

**1. ما الكيانات الأربعة (entities) الأساسية في هيكل تعدد المستأجرين (the multi-tenant skeleton)، وأيها هو المستأجر (tenant)؟**

<details><summary>الإجابة</summary>

المستخدمون، والمنظمات، والعضويات، والدعوات. المنظمة هي المستأجر: تملك البيانات وتدفع الفاتورة، وينضم إليها المستخدمون عبر عضويات تحمل دورًا. راجع الجدول في "🟢 الأساسيات".

</details>

**2. ما قاعدة tenant_id (the tenant_id rule)، ولماذا يحمل `CHECK_RESULT` الحقل (field) `org_id` مع أنه يستطيع الوصول إلى المنظمة (organization) عبر المراقِب (monitor)؟**

<details><summary>الإجابة</summary>

كل صف يملكه المستأجر يحمل معرّف المستأجر مباشرة. هذا يتيح لكل استعلام التصفية حسب المنظمة دون ربط، ويتيح لكل فهرس أن يبدأ بـ `org_id`، ويجعل غياب تصفية المنظمة واضحًا في المراجعة (review)، ويبقي أمان مستوى الصف والتجزئة الأفقية ممكنين لاحقًا. راجع "🟢 الأساسيات".

</details>

**3. أُزيل متعاقد (contractor) أنشأ 40 من مراقِبات Acme من منظمة (organization) Acme في Beacon. ماذا يجب أن يحدث لتلك المراقِبات (monitors)، ولماذا؟**

<details><summary>الإجابة</summary>

تبقى. الملكية هي `org_id`، أما `created_by` فيُحتفظ به للتاريخ والعرض فقط. إزالة العضو تحذف عضويته وتلغي كل ما كان يعمل باسمه في تلك المنظمة، مثل رموز API الشخصية الخاصة به والدعوات المعلّقة التي أرسلها. راجع "🟢 الأساسيات" و"المغادرة والإزالة والملكية" في "🟡 التعمق أكثر".

</details>

**4. Priya هي المالكة (owner) الوحيدة لمنظمة (organization) Acme في Beacon، ونقرت "مغادرة المنظمة". ماذا يجب أن يفعل Beacon؟**

<details><summary>الإجابة</summary>

يمنع ذلك ويشرح السبب. يجب أن يكون للمنظمة دائمًا مالك واحد على الأقل، لذلك لا يستطيع آخر مالك المغادرة أو خفض دوره حتى تُنقل الملكية، وهو إجراء مقصود ومؤكَّد يتطلب مصادقة معزّزة وبريدًا للطرفين. راجع "🟡 التعمق أكثر".

</details>

**5. صفحة مراقِب (monitor) تُحمَّل عبر `db.monitor.findUnique({ where: { id } })` بعد قراءة المعرّف النصي للمنظمة (org slug) من الرابط. ما الذي يتعطّل؟**

<details><summary>الإجابة</summary>

المعرّف النصي للمنظمة ادعاء وليس حقيقة، والاستعلام يتجاهله، لذلك يستطيع أي شخص قراءة مراقِب أي منظمة بتخمين المعرّف أو تغييره. اجلب العضوية للمنظمة والمستخدم الحالي (current user) في كل طلب، وأرجع 404 عندما تكون غير موجودة، وصفِّ الاستعلام حسب `org_id`. راجع "التبديل بين المنظمات" في "🟡 التعمق أكثر" و"⚠️ أخطاء يقع فيها المبتدئون".

</details>

## 📚 المراجع

- Better Auth documentation, Organization plugin — https://www.better-auth.com/docs (توثيق إضافة المنظمات في Better Auth)
- Clerk documentation, Organizations — https://clerk.com/docs
- WorkOS documentation, which covers organizations, invitations and domain verification — https://workos.com/docs (يغطي المنظمات والدعوات والتحقق من النطاق)
- PostgreSQL documentation, Row Security Policies — https://www.postgresql.org/docs/current/ddl-rowsecurity.html (سياسات (policies) أمان مستوى الصف)
- Citus documentation on multi-tenant applications — https://docs.citusdata.com (التطبيقات متعددة المستأجرين)
- nextjs/saas-starter README — https://github.com/nextjs/saas-starter

---

# 1.3 — التفويض: الأدوار والصلاحيات وسؤال "هل يستطيع هذا المستخدم فعل هذا؟"

*المستوى: 🟡 متوسط (Intermediate)* · *المتطلبات: 1.1، 1.2*

## ⚡ الدرس في دقيقة (In 60 seconds)

- التفويض يقرّر هل يحق لفاعل (subject) تنفيذ إجراء على مورد محدد. يطرح الخادم هذا السؤال في كل طلب، ولا يأخذ الإجابة من العميل (client) أبدًا.
- القاعدة الأهم: افحص الصلاحيات لا أسماء الأدوار (role names)، وضع معرّف المنظمة داخل كل استعلام حتى تصبح كائنات (objects) المستأجرين الآخرين غير موجودة ببساطة.
- الخيار الافتراضي للنسخة الأولى (v1): RBAC لكل منظمة مع خريطة من الأدوار إلى الصلاحيات (role-to-permission map)، ووحدة واحدة (module) فيها `can()` و`requirePermission()`.
- استخدم قائمة سماح (allow-list) لأجسام الطلبات (request bodies) وللردود (responses). الإسناد الجماعي (mass assignment) ثغرة تفويض (authorization bug).
- الفخ الأكبر: الفرض (enforcing) في الواجهة فقط، أو جلب الكائنات بالمعرّف وحده (IDOR).

## 🧭 لماذا يحتاجه كل SaaS

في مارس 2012 أبلغ مطوّر (developer) اسمه Egor Homakov أن تطبيقات Ruby on Rails معرّضة (vulnerable) على نطاق واسع لثغرة **الإسناد الجماعي**: كود مثل `User.update(params[:user])` كان يضبط بكل سرور *أي* عمود يذكره الطلب، بما في ذلك أعمدة (columns) لم يعرضها النموذج (form) أبدًا. وعندما لم يُؤخذ بلاغه بجدية، أثبته على GitHub نفسه. بإضافة حقل زائد إلى إرسال نموذج (form submission)، ربط مفتاح SSH (SSH key) الخاص به بمنظمة Rails ودفع إيداعًا (Commit) إلى مستودع (repository) `rails/rails`. أصلحت GitHub الثغرة (hole) خلال ساعات وعلّقت حسابه ثم أعادته. واستجاب Rails بـ **المعاملات القوية** (Strong Parameters)، التي صارت الخيار الافتراضي في Rails 4: يجب أن يسرد المتحكم (Controller) صراحةً الحقول (fields) التي يحق للطلب ضبطها.

لم ينسَ أحد في GitHub كتابة فحص صلاحية (permission check) لإجراء "أضف مفتاحًا (key) إلى هذا المستودع". كان الفشل أهدأ من ذلك: وثق الخادم بأن العميل لن يرسل إلا ما يعرضه النموذج. هذا هو درس التفويض في حادثة واحدة (one incident). القواعد نادرًا ما تكون معقدة. **ما يفشل هو مكان فرضها وطريقته (enforced).**

لدى Beacon نقطة الضعف نفسها. يجب ألا يُرجع `GET /api/monitors/123` المراقِب 123 إذا كان يخص منظمة أخرى. ويجب ألا يعمل `PATCH /api/members/45 {"role": "owner"}` لعضو عادي (plain member). ويجب ألا يستطيع المشاهد (viewer) حذف صفحة حالة لمجرد أن الزر مخفي في الواجهة بدلًا من أن يكون ممنوعًا على الخادم. تُدرج قائمة OWASP API Security Top 10 (2023) هذه الثغرات تحت: رقم 1 تفويض مستوى الكائن المكسور (Broken Object Level Authorization)، ورقم 3 تفويض مستوى خصائص الكائن (object) المكسور (Broken Object Property Level Authorization، ويشمل الإسناد الجماعي)، ورقم 5 تفويض مستوى الوظيفة المكسور (Broken Function Level Authorization). إنها أكثر ثغرات API (API bugs) شيوعًا في الواقع لأنها غير مرئية في العروض التجريبية (demo).

**التفويض (authorization) سؤال يطرحه الخادم (server) في كل طلب، عن مستخدم (user) وإجراء (action) وكائن (object) محددين، والإجابة (the answer) لا تُؤخذ من العميل (from the client) أبدًا.**

## 📐 كيف يعمل

### 🟢 الأساسيات

لكل فحص تفويض (authorization check) المدخلات نفسها: **فاعل** (Subject، أي من: مستخدم أو مفتاح API)، و**إجراء** (Action، أي ماذا: `monitor.delete`)، و**مورد** (Resource، أي أي كائن: المراقِب 123 في منظمة Acme). والناتج: سماح (allow) أو رفض (deny).

أبسط نموذج صالح للعمل هو **RBAC (التحكم في الوصول القائم على الأدوار (role-based access control))**: لكل عضوية من الدرس 1.2 دور، وكل دور يمنح مجموعة ثابتة من الصلاحيات. هذه مصفوفة Beacon (matrix):

| الصلاحية (permission) | Owner | Admin | Member | Viewer |
|---|---|---|---|---|
| عرض المراقِبات والحوادث (incidents) وصفحات الحالة (status pages) | ✓ | ✓ | ✓ | ✓ |
| إنشاء المراقِبات وتعديلها | ✓ | ✓ | ✓ | |
| تحديث الحوادث | ✓ | ✓ | ✓ | |
| نشر صفحة الحالة وضبط نطاق مخصص (custom domain) | ✓ | ✓ | | |
| دعوة الأعضاء وإزالتهم | ✓ | ✓ | | |
| إدارة الفوترة | ✓ | | | |
| حذف المنظمة ونقل الملكية | ✓ | | | |

أهم قرار تصميمي (design decision) هنا صغير: **افحص الصلاحيات (permissions)، لا الأدوار (roles).** الكود الذي يقول `if (role === "admin")` يجب البحث (search) عنه وتعديله في كل مرة تضيف فيها دورًا. أما الكود الذي يقول `can(member, "monitor.write")` فلا يحتاج إلا إلى تحديث خريطة الأدوار والصلاحيات.

```ts
const PERMISSIONS = {
  owner:  ["monitor.read", "monitor.write", "incident.write", "page.publish",
           "member.manage", "billing.manage", "org.delete"],
  admin:  ["monitor.read", "monitor.write", "incident.write", "page.publish", "member.manage"],
  member: ["monitor.read", "monitor.write", "incident.write"],
  viewer: ["monitor.read"],
} as const;

type Role = keyof typeof PERMISSIONS;
type Permission = (typeof PERMISSIONS)[Role][number];

export function can(role: Role, permission: Permission): boolean {
  return (PERMISSIONS[role] as readonly string[]).includes(permission);
}

export async function requirePermission(orgSlug: string, userId: string, p: Permission) {
  const m = await db.membership.findFirst({ where: { userId, org: { slug: orgSlug } } });
  if (!m) throw new NotFound();          // not a member: do not reveal the org exists
  if (!can(m.role as Role, p)) throw new Forbidden();
  return m;                              // callers use m.orgId for every query
}
```

**أين تفرض (enforced) الفحص.** الواجهة تخفي الأزرار لتجربة أفضل، لكنها لا تفرض شيئًا: أي شخص يستطيع استدعاء الواجهة البرمجية عبر `curl`. الخادم هو المكان الوحيد الذي يُحتسب فيه الفحص.

```mermaid
flowchart RL
    R["طلب مع جلسة أو مفتاح API<br/>(Request with session or API key)"] --> AN["المصادقة: من هذا<br/>(Authenticate: who is this)"]
    AN --> TN["تحديد المنظمة والعضوية<br/>(Resolve org and membership)"]
    TN --> PC["فحص الصلاحية: هل يستطيع الدور تنفيذ الإجراء<br/>(Permission check: can role do action)"]
    PC --> Q["استعلام محصور بـ org_id<br/>(Query scoped by org_id)"]
    Q --> OC["فحص الكائن: هل هذا الصف في المنظمة<br/>(Object check: is this row in the org)"]
    OC --> RES["رد بالحقول المسموح بها فقط<br/>(Response with allowed fields only)"]
    UI["الواجهة تخفي الأزرار<br/>(UI hides buttons)"] -.->|"للراحة فقط (convenience only)"| R
```

يظهر في هذا المسار (pipeline) فحصان منفصلان، والمبتدئون عادةً (juniors) يكتبون واحدًا فقط:

1. **مستوى الوظيفة (function-level)**: هل يحق لهذا الدور تنفيذ هذا الإجراء أصلًا؟ (هل يستطيع المشاهد حذف المراقِبات؟)
2. **مستوى الكائن (object-level)**: هل *هذا الكائن تحديدًا* داخل المستأجر ومرئي لهذا المستخدم؟ (هل المراقِب 123 في Acme؟)

فحص مستوى الكائن (object-level check) هو المكان الذي تعيش فيه ثغرة IDOR. **IDOR (المرجع المباشر غير الآمن للكائن (Insecure Direct Object Reference))** هو الاسم الأقدم لتفويض مستوى الكائن المكسور: تأخذ الواجهة البرمجية معرّفًا من العميل وتجلب الكائن دون أن تفحص لمن هو. الحل المتين ليس استدعاءً منفصلًا "افحص الملكية" يمكن أن ينساه أحد، بل أن تجعل الاستعلام بلا مستأجر مستحيلًا من حيث البنية (structurally):

```ts
// Vulnerable: finds monitor 123 in any org
await db.monitor.findUnique({ where: { id } });
// Safe: a monitor from another org simply does not exist for this query
await db.monitor.findFirst({ where: { id, orgId: membership.orgId } });
```

**الإسناد الجماعي (mass assignment)** هو النسخة الخاصة بمستوى الخصائص (property-level). لا تمرّر جسم الطلب (request body) مباشرة إلى عملية تحديث (update) أبدًا. حلّله بمخطط قائمة سماح (Zod في TypeScript، والمعاملات القوية في Rails، والمسلسِلات (Serializers) ذات الحقول الصريحة في Django REST Framework، و`$fillable` في Laravel) حتى لا يتسلل `orgId` أو `role` أو `createdBy`. والأمر نفسه ينطبق في الاتجاه المعاكس: أرجع كائن نقل بيانات للرد (Response DTO)، لا الصف الخام (raw row)، وإلا فسترسل يومًا ما `password_hash` أو `stripe_customer_id` لأحدهم في رد JSON (JSON response).

### 🟡 التعمق أكثر

**التسلسل الهرمي للأدوار (role hierarchy) وقواعد التصعيد (escalation rules).** يستطيع المسؤولون إدارة الأعضاء، لكن هل يستطيع مسؤول ترقية شخص إلى مالك، أو إزالة مسؤول آخر؟ اكتب القاعدة: *لا يستطيع المستخدم منح الأدوار أو تغييرها أو إزالتها إلا عند مستواه أو دونه، ولا يستطيع أبدًا تغيير دوره هو.* هذه الجملة الواحدة تمنع أشهر ثغرة تصعيد صلاحيات (privilege-escalation bug) في إعدادات الفرق (team settings).

**الأدوار المخصصة (custom roles).** سيطلب عملاء الشركات (business customers) "دور مناوبة (on-call role) يستطيع تحديث الحوادث لكن لا يستطيع تعديل المراقِبات". إذا كان كودك يفحص الصلاحيات أصلًا لا أسماء الأدوار، فالأدوار المخصصة تغيير في البيانات (data change): خزّن الأدوار كصفوف مع قائمة صلاحيات (permission list) لكل منظمة، وأبقِ الأدوار المدمجة (built-in) كقيم افتراضية (defaults)، ولن تتغير دالة (function) `can()` إلا قليلًا.

**ABAC (التحكم في الوصول القائم على السمات (attribute-based access control))** يقرّر باستخدام سمات الفاعل والمورد والسياق (context)، لا الدور وحده. أمثلة من Beacon:

- يستطيع العضو تعديل المراقِبات التي أنشأها، لكن المسؤولين وحدهم يعدّلون مراقِبات الآخرين (`resource.createdBy == subject.id`).
- الوصول إلى API يتطلب أن تكون المنظمة على خطة (plan) Business (`org.plan == "business"`). هذا في الحقيقة استحقاق (entitlement) (الدرس 3.2)، لكنه يعيش في القرار نفسه.
- حذف صفحة حالة ممنوع ما دامت فيها حادثة مفتوحة (open incident).

في ABAC تبدأ جمل `if` المكتوبة يدويًا بالانتشار عبر المعالِجات (handlers). هذه إشارة (signal) لنقل القواعد إلى وحدة واحدة، أو إلى **السياسات ككود** (Policy as Code): قواعد تفويض (authorization rules) مكتوبة بلغة أو صيغة (format) مخصصة، ومحفوظة بإصدارات (versioned) في git، ومختبرة مثل الكود، وتقيّمها مكتبة أو خدمة. بعض أشكالها:

| الأداة (tool) | كيف تُكتب السياسات | تعمل كـ (runs as) |
|---|---|---|
| CASL | قواعد JavaScript (`can("update", "Monitor", { createdBy: user.id })`) | مكتبة داخل تطبيقك، وحتى في المتصفح |
| Casbin | ملف نموذج (model file) (RBAC وABAC وغيرها) مع جدول سياسات (policy table) | مكتبة بلغات كثيرة |
| Cerbos | سياسات موارد (resource policies) بصيغة YAML مع شروط (conditions) | خدمة مستقلة عديمة الحالة (stateless service) أو مدمجة (embedded) |
| Open Policy Agent (OPA) | Rego، لغة استعلام تصريحية | خدمة أو مكتبة، شائعة في البنية التحتية |

**تصفية القوائم (filtering lists).** فحوص الكائن الواحد (single-object checks) سهلة: اجلبه واسأل `can()`. القوائم أصعب. سؤال "أرني كل مراقِب أستطيع رؤيته" لا يُجاب بجلب كل المراقِبات وتصفيتها في الذاكرة، لأن ذلك يكسر الترقيم (Pagination) ويكشف معلومات عبر التوقيت. تحتاج إلى تحويل السياسة (policy) إلى **شرط تصفية في الاستعلام (query filter)**. في RBAC المحصور بالمنظمة (org-scoped)، الشرط (condition) ببساطة `WHERE org_id = $1`. وفي ABAC، يستطيع CASL تحويل القواعد إلى شروط قاعدة بيانات (database conditions)، ولدى Cerbos واجهة "خطة الاستعلام" (Query Plan) التي تُرجع شجرة شروط (condition tree) تترجمها إلى SQL. صمّم سياساتك بحيث يمكن تحويل كل قاعدة إلى جملة (clause) `WHERE`.

### 🔴 على نطاق واسع وللمؤسسات

**ReBAC (التحكم في الوصول القائم على العلاقات (relationship-based access control))** يقرّر بتتبع العلاقات (relationships): تستطيع Ana رؤية صفحة الحالة X لأنها عضو في الفريق Y، وهو محرّر (editor) للمجلد (folder) Z، الذي يحتوي X. هذا ما تحتاجه مشاركة Google Docs وفرق GitHub وصفحات Notion. التصميم المرجعي (reference design) هو ورقة Google عن **Zanzibar** (USENIX ATC 2019). تُخزَّن الصلاحيات كـ **صفوف علاقات** (Relationship Tuples) مثل `status_page:acme-public#editor@team:sre#member`، ويحدد مخطط كيف تتركب العلاقات. من الأنظمة مفتوحة المصدر المستوحاة من Zanzibar: OpenFGA وSpiceDB وPermify وOry Keto. هذا نموذج OpenFGA صغير لـ Beacon:

```text
model
  schema 1.1

type user

type organization
  relations
    define owner: [user]
    define admin: [user] or owner
    define member: [user] or admin

type status_page
  relations
    define org: [organization]
    define editor: [user] or admin from org
    define viewer: [user] or editor or member from org
```

لـ ReBAC تكاليف حقيقية. الصلاحيات تعيش الآن في مخزن بيانات منفصل (datastore) يجب أن يبقى متزامنًا مع قاعدة بياناتك الرئيسية: عندما يُحذف صف عضوية (membership row)، يجب حذف الصف المقابل أيضًا، ويفضّل أن يتم ذلك عبر صندوق صادر معاملاتي (Transactional Outbox، الدرس 5.3). كما تسمّي Zanzibar **مشكلة "العدو الجديد (new enemy)"**: إذا أزلت Bob من صفحة ثم أضفت إليها سرًا، فيجب ألا يسمح فحص صلاحية قديم لـ Bob برؤية السر. تحل Zanzibar هذا برموز اتساق (consistency tokens) ("zookies")، ويسميها SpiceDB باسم ZedTokens. وتصبح تصفية القوائم واجهة مخصصة (dedicated API): `ListObjects` في OpenFGA، و`LookupResources` في SpiceDB. هذه أدوات قوية، ويجب أن تحسب حساب أدائها (performance).

**إلى أي درجة من السلم (ladder) يجب أن يصعد Beacon؟** على الأرجح RBAC مع خريطة صلاحيات (permission map)، وبعض قواعد ABAC (ABAC rules) في وحدة واحدة، ولمدة طويلة. انتقل إلى ReBAC عندما يحتاج العملاء إلى *مشاركة كائنات فردية* بين الفرق، لا مجرد أدوار أكثر. منتجات SaaS ناجحة كثيرة لا تتجاوز أبدًا RBAC لكل منظمة مع أدوار مخصصة.

**تشغيل التفويض (operating authorization).** على نطاق واسع تحتاج أيضًا إلى واجهة إدارة (admin view) تجيب عن "لماذا تستطيع Ana رؤية هذا؟"، وسجلات تدقيق لكل تغيير في الأدوار (الدرس 7.3)، واختبارات آلية (automated tests) تستدعي كل نقطة نهاية (endpoint) بكل دور (اختبار مصفوفة الصلاحيات)، وقاعدة تجعل نقاط النهاية الجديدة (new endpoints) مغلقة عند الفشل (Fail Closed): مرفوضة حتى تسمح بها سياسة صراحةً.

## 🏆 أفضل المستودعات

| المستودع | ما هو | التقنيات | الترخيص | اختره عندما |
|---|---|---|---|---|
| [stalniy/casl](https://github.com/stalniy/casl) | مكتبة تفويض (authorization library) JavaScript تعمل على الخادم والمتصفح مع محوّلات لاستعلامات ORM | TypeScript | MIT | تريد RBAC وABAC داخل تطبيق TypeScript، مع مشاركة القواعد مع الواجهة الأمامية (frontend) |
| [apache/casbin](https://github.com/apache/casbin) | Apache Casbin: مكتبة تفويض قائمة على النماذج (model-driven) مع نسخ بلغات كثيرة | Go (plus ports) | Apache-2.0 | تريد نموذج سياسات (policy model) واحدًا عبر خدمات Go وNode وPython وJava |
| [cerbos/cerbos](https://github.com/cerbos/cerbos) | نقطة قرار سياسات عديمة الحالة مع سياسات YAML وتخطيط الاستعلامات (query planning) | Go | Apache-2.0 | تريد السياسات ككود منفصلة عن كود التطبيق، مع دعم تصفية القوائم |
| [openfga/openfga](https://github.com/openfga/openfga) | خادم ReBAC مستوحى من Zanzibar، ومشروع في CNCF أصله من Auth0/Okta | Go | Apache-2.0 | تحتاج مشاركة على مستوى الكائن (object-level sharing) مع لغة نمذجة (modelling language) سهلة |
| [authzed/spicedb](https://github.com/authzed/spicedb) | قاعدة بيانات صلاحيات (permissions database) مستوحاة من Zanzibar مع ميزات اتساق قوية (strong consistency) | Go | Apache-2.0 | تحتاج ReBAC على نطاق واسع وتهتم بمشكلة العدو الجديد |
| [Permify/permify](https://github.com/Permify/permify) | خدمة تفويض (authorization service) مستوحاة من Zanzibar، صارت الآن جزءًا من FusionAuth | Go | AGPL-3.0 | تريد ReBAC مع قواعد السمات (attribute rules) في خدمة واحدة |
| [open-policy-agent/opa](https://github.com/open-policy-agent/opa) | محرك سياسات (policy engine) عام الغرض يستخدم لغة Rego | Go | Apache-2.0 | تريد محرك سياسات واحدًا لتفويض التطبيق وللبنية التحتية (Kubernetes، CI) |
| [ory/keto](https://github.com/ory/keto) | خادم صلاحيات (permission server) مستوحى من Zanzibar ضمن منظومة (ecosystem) Ory | Go | Apache-2.0 | تشغّل أصلًا Ory Kratos أو Hydra |
| [osohq/oso](https://github.com/osohq/oso) | مكتبة Oso ولغة Polar، وقد أُلغيتا (deprecated) الآن لصالح Oso Cloud | Rust (plus bindings) | Apache-2.0 | كقراءة: توثيقها من أفضل الشروح لأنماط التفويض (authz patterns) |

**إن درست مستودعًا واحدًا فقط (If you only study one):** **stalniy/casl**. يغطي التدرج من الأدوار إلى شروط السمات (attribute conditions) في كود يستطيع مطوّر TypeScript قراءته في فترة ما بعد الظهر، ومحوّلات قواعد البيانات (database adapters) فيه تُظهر عمليًا كيف تتحول قاعدة صلاحية (permission rule) إلى شرط تصفية في الاستعلام، وهي أصعب فكرة في هذا الدرس.

**اشترِ أم ابنِ أم استضف بنفسك (Buy, build, or self-host)؟**

- **اشترِ (buy)** خدمة تفويض مستضافة (Oso Cloud، أو Authzed لـ SpiceDB، أو Auth0 FGA لـ OpenFGA، أو Permit.io) عندما تحتاج ReBAC عبر عدة خدمات ولا تريد تشغيل مخزن بيانات حساس للاتساق (consistency-sensitive).
- **استضف بنفسك (self-host)** OpenFGA أو SpiceDB أو Cerbos أو Permify عندما تكون لديك خدمات كثيرة، أو مشاركة لكل كائن (per-object sharing)، أو سياسات يجب أن يراجعها غير المطورين (non-developers)، وتستطيع تشغيل مكوّن إضافي (extra component) ذي حالة (stateful) أو عديم الحالة.
- **ابنِ (build)** خريطة صلاحيات مع وحدة `can()` (اختياريًا مع CASL أو Casbin) لمعظم منتجات SaaS. RBAC لكل منظمة مع بعض قواعد السمات يغطي غالبية المنتجات لسنوات.

## 🔍 ادرسه في مشاريع حقيقية

**Infisical/infisical** منتج SaaS لإدارة الأسرار (secrets-management)، وعملاؤه يهتمون بشدة بمن يستطيع قراءة ماذا. في وقت كتابة هذا الدرس، يبني الخادم الخلفي فيه الصلاحيات باستخدام CASL، مع مجموعات صلاحيات (permission sets) منفصلة على مستوى المنظمة ومستوى المشروع، وأدوار مخصصة. ابحث عن `casl` أو `ProjectPermission` في الخادم الخلفي لتجد تعريفات الفاعلين (subjects) والإجراءات، ثم اعثر على المكان الذي يغلّف فيه فحص الصلاحية كل استدعاء لخدمة (service call).

**getsentry/sentry** (Django) يستخدم أدوار أعضاء المنظمة التي تُربط بـ **نطاقات** (Scopes) مثل `project:read` و`project:write` و`org:admin`، وهي النطاقات نفسها التي تحصل عليها رموز API (API tokens). ابحث عن `scopes` وعن أصناف (classes) بأسماء مثل `OrganizationPermission` لترى كيف تفرضها أصناف الصلاحيات (permission classes) في Django REST Framework لكل نقطة نهاية. التصميم اللافت هنا مفردات (vocabulary) واحدة يتشاركها البشر ورموز API.

**nextjs/saas-starter** يُظهر أصغر نسخة: دور owner/member على عضوية الفريق (team membership)، وإجراءات خادم (server actions) تفحصه. ابحث عن `role` في الإجراءات. إنه خط أساس (baseline) مفيد لتوسيعه إلى خريطة الصلاحيات أعلاه.

**ما الذي تلاحظه (What to notice):**

- هل يفحص الكود أسماء الأدوار أم الصلاحيات، وما مدى صعوبة إضافة دور.
- أين يحدث فحص مستوى الكائن: في كل معالِج (handler)، أم في طبقة وصول بيانات مشتركة، أم داخل الاستعلام نفسه.
- كيف تُربط رموز API بمفردات الصلاحيات (permission vocabulary) نفسها التي يستخدمها البشر.
- كيف تُصفّى نقاط نهاية (endpoints) القوائم، وهل تأتي التصفية وفحص الكائن الواحد (single-object check) من القواعد نفسها.
- كيف تُخزَّن الأدوار المخصصة (تعداد (enum) في الكود أم صفوف في قاعدة البيانات).

## 🛠️ ابنِه في Beacon

### 🟢 تمرين المبتدئ

أضف أدوار owner/admin/member/viewer من المصفوفة أعلاه. نفّذ `requirePermission()` واستدعِها من كل نقطة نهاية للمراقِبات والحوادث وصفحات الحالة. أخفِ الأزرار في الواجهة بناءً على خريطة الصلاحيات نفسها.

**يكتمل عندما (Done when):**
- كل نقطة نهاية تغيّر البيانات (mutating endpoint) تستدعي `requirePermission()` قبل أن تبدأ العمل.
- المشاهد الذي يستدعي `DELETE /api/monitors/:id` عبر `curl` يحصل على 403.
- كل استعلام على المراقِبات يتضمن `orgId`، وجلب معرّف مراقِب من منظمة أخرى يُرجع 404.

### 🟡 تمرين المستوى المتوسط

أضف التحقق من جسم الطلب (request-body validation) باستخدام Zod (أو ما يعادله في بيئتك) على كل نقطة نهاية للكتابة (write endpoint)، وكائنات DTO (DTOs) للردود على كل نقطة نهاية للقراءة (read endpoint). نفّذ قواعد تغيير الأدوار (role-change rules): لا يستطيع المستخدم إسناد أدوار إلا عند مستواه أو دونه، ولا يستطيع أبدًا تغيير دوره هو. أضف قاعدة ABAC (ABAC rule) واحدة: يستطيع الأعضاء تعديل المراقِبات التي أنشؤوها فقط.

**يكتمل عندما (Done when):**
- إرسال `{"orgId": "<other org>"}` أو `{"role": "owner"}` في جسم الطلب لا يُحدث أي أثر.
- لا يحتوي أي رد من الواجهة البرمجية على أعمدة غير مذكورة في DTO الخاص به.
- لا يستطيع المسؤول ترقية أحد إلى مالك، ولا يستطيع أحد تغيير دوره هو.
- اختبار آلي (automated test) يستدعي كل نقطة نهاية بكل دور ويتحقق من رموز الحالة (status codes) المتوقعة.

### 🔴 تمرين المستوى المتقدم

أضف مشاركة لكل صفحة حالة باستخدام OpenFGA (أو SpiceDB): يمكن جعل فريق أو فرد محرّرًا لصفحة حالة واحدة دون صلاحيات المسؤول (admin rights). أبقِ الصفوف متزامنة مع العضويات باستخدام جدول صندوق صادر (outbox table) تعالجه مهمة خلفية. ابنِ قائمة "صفحات الحالة الخاصة بي" باستخدام `ListObjects`.

**يكتمل عندما (Done when):**
- إزالة عضوية تزيل وصول المستخدم إلى كل صفحات الحالة في تلك المنظمة خلال ثوانٍ.
- نقطة نهاية القائمة تُرجع بالضبط الصفحات التي يسمح بها فحص الكائن الواحد.
- صفحة إدارة تجيب عن "لماذا يستطيع هذا المستخدم تعديل هذه الصفحة؟" بعرض مسار العلاقات (relationship path).

## ⚠️ أخطاء يقع فيها المبتدئون

- **فرض الصلاحيات في الواجهة فقط (Enforcing permissions only in the UI).** الأزرار المخفية ليست أمانًا. يجب أن يحدث كل فحص على الخادم، والواجهة تعيد استخدام خريطة الصلاحيات نفسها للعرض فقط.
- **جلب الكائنات بالمعرّف وحده (IDOR).** `findUnique({ id })` متبوعًا بـ "سنفحص لاحقًا" هو الطريق الذي تُشحن به ثغرات (bugs) IDOR. ضع معرّف المنظمة داخل الاستعلام نفسه حتى يصبح الكائن الغريب (foreign object) غير موجود ببساطة.
- **نشر جسم الطلب (request body) مباشرة في قاعدة البيانات (database).** هذه ثغرة GitHub عام 2012. حلّل المدخلات بمخطط قائمة سماح (allow-list schema)، ولا تقبل أبدًا معرّفات المستأجرين (tenant ids) أو الأدوار أو حقول المالك من جسم الطلب.
- **فحص `role === "admin"` في كل أنحاء الكود.** تصبح إضافة دور واحد تمرين "ابحث وادعُ" (grep-and-pray). افحص الصلاحيات وأبقِ خريطة الأدوار (role map) في مكان واحد.
- **تصفية القوائم (filtering lists) في الذاكرة (in memory).** تحميل 10,000 صف لعرض 20 بطيء ويكشف الأعداد. ادفع شرط التفويض (authorization condition) إلى جملة `WHERE`.
- **إرجاع 403 لكائنات (objects) في مستأجرين (tenants) آخرين.** هذا يؤكد أن المعرّف موجود. أرجع 404 للكائنات خارج مستأجر المستخدم، و403 للكائنات داخله التي لا يستطيع الدور لمسها.

## 🧾 الخلاصة

- التفويض يجيب عن "هل يستطيع هذا الفاعل تنفيذ هذا الإجراء على هذا المورد؟" على الخادم، في كل مرة.
- فحصان: مستوى الوظيفة (هل يحق لهذا الدور فعل هذا؟) ومستوى الكائن (هل هذا الكائن داخل المستأجر؟). IDOR هو غياب الفحص الثاني.
- افحص الصلاحيات، لا الأدوار. عندها تصبح الأدوار المخصصة تغييرًا في البيانات.
- استخدم قائمة سماح للمدخلات والمخرجات. الإسناد الجماعي والردود التي تكشف أكثر من اللازم ثغرات تفويض (authorization bugs) أيضًا.
- السلم: RBAC، ثم ABAC في وحدة سياسات (policy module) واحدة، ثم ReBAC (بأسلوب Zanzibar) فقط عندما تحتاج مشاركة على مستوى الكائن.
- القوائم تحتاج التفويض كشرط تصفية في الاستعلام، لا كحلقة تكرار (loop).

## ✍️ اختبر نفسك

**1. ما الفرق (teams) بين فحص التفويض (authorization check) على مستوى الوظيفة (function-level) وفحصه على مستوى الكائن (object-level)؟**

<details><summary>الإجابة</summary>

فحص مستوى الوظيفة يسأل هل يحق لهذا الدور تنفيذ هذا الإجراء أصلًا (هل يستطيع المشاهد حذف المراقِبات؟). وفحص مستوى الكائن يسأل هل هذا الكائن تحديدًا داخل المستأجر ومرئي لهذا المستخدم (هل المراقِب 123 في Acme؟). ثغرة IDOR هي غياب فحص مستوى الكائن. راجع "🟢 الأساسيات".

</details>

**2. لماذا يجب أن يفحص الكود صلاحيات (permissions) مثل `monitor.write` بدلًا من أسماء أدوار (role names) مثل `admin`؟**

<details><summary>الإجابة</summary>

فحوص أسماء الأدوار تنتشر في أنحاء الكود، ويجب تعديلها كلها كلما أُضيف دور. أما فحوص الصلاحيات (permission checks) فلا تحتاج إلا إلى تحديث خريطة الأدوار والصلاحيات، وهذا يجعل الأدوار المخصصة أيضًا تغييرًا في البيانات. راجع "🟢 الأساسيات" و"الأدوار المخصصة" في "🟡 التعمق أكثر".

</details>

**3. طلب عميل (customer) لدى Beacon دور (role) "مناوبة (on-call)" يستطيع تحديث الحوادث (incidents) لكن لا يستطيع تعديل المراقِبات (monitors). ما حجم هذا العمل حسب التصميم (design) في هذا الدرس؟**

<details><summary>الإجابة</summary>

صغير، إذا كان الكود يفحص الصلاحيات أصلًا. خزّن الأدوار كصفوف مع قائمة صلاحيات لكل منظمة، وأبقِ الأدوار المدمجة كقيم افتراضية، وامنح دور المناوبة `monitor.read` و`incident.write`. لن تتغير دالة `can()` إلا قليلًا. راجع "الأدوار المخصصة" في "🟡 التعمق أكثر".

</details>

**4. يحتاج Beacon قائمة "صفحات الحالة (status pages) الخاصة بي" يرى فيها الأعضاء (members) فقط الصفحات التي يحق لهم عرضها. لماذا لا تحمّل كل الصفحات وتصفّيها بـ `can()` في حلقة (loop)؟**

<details><summary>الإجابة</summary>

التصفية في الذاكرة تكسر الترقيم، وبطيئة، وتكشف الأعداد والتوقيت. حوّل السياسة إلى شرط تصفية في الاستعلام: `WHERE org_id = $1` في RBAC لكل منظمة، أو شروط قاعدة البيانات من CASL أو خطة الاستعلام من Cerbos في ABAC، أو `ListObjects` / `LookupResources` في ReBAC. راجع "تصفية القوائم" في "🟡 التعمق أكثر".

</details>

**5. نقطة نهاية (endpoint) تحديث الأعضاء (members) تنفّذ `db.membership.update({ where: { id }, data: req.body })` بعد التحقق (verification) من أن المستدعي عضو (member). ما الذي يتعطّل؟**

<details><summary>الإجابة</summary>

هذا إسناد جماعي، أي ثغرة GitHub عام 2012: يستطيع عضو عادي إرسال `{"role": "owner"}` أو `orgId` مختلف، وستقبله قاعدة البيانات. حلّل جسم الطلب بمخطط قائمة سماح، وافرض قواعد تغيير الأدوار (عند مستواك أو دونه فقط، ولا تغيّر دورك أبدًا)، واشترط الصلاحية `member.manage`. راجع "🧭 لماذا يحتاجه كل SaaS" و"🟡 التعمق أكثر".

</details>

## 📚 المراجع

- OWASP API Security Top 10 (2023), including API1 Broken Object Level Authorization and API3 Broken Object Property Level Authorization — https://owasp.org/API-Security/ (أهم عشر مخاطر لأمان الواجهات البرمجية)
- OWASP Cheat Sheet Series: Authorization and Mass Assignment cheat sheets — https://cheatsheetseries.owasp.org (أوراق مرجعية للتفويض والإسناد الجماعي)
- "Zanzibar: Google's Consistent, Global Authorization System", USENIX ATC 2019 — https://www.usenix.org/conference/atc19
- Rails guides, Action Controller Overview — https://guides.rubyonrails.org/action_controller_overview.html (المعاملات القوية)
- OpenFGA documentation — https://openfga.dev/docs
- SpiceDB documentation — https://authzed.com/docs
- Cerbos documentation — https://docs.cerbos.dev
- Oso's authorization academy and docs — https://www.osohq.com (أكاديمية التفويض من Oso)

---

# 1.4 — هوية المؤسسات (enterprise identity): SSO وSAML وOIDC وSCIM

*المستوى: 🔴 متقدم (Advanced)* · *المتطلبات: 1.1، 1.2، 1.3*

## ⚡ الدرس في دقيقة (In 60 seconds)

- الدخول الموحد يجعل مزوّد هوية العميل (identity provider) يتولى تسجيل الدخول. وSCIM يجعله ينشئ المستخدمين ويزيلهم عندما ينضم الموظفون (employees) ويغادرون.
- القاعدة الأهم: لا تكتب التحقق (validation) من SAML بنفسك أبدًا، وتحقّق من ملكية النطاق (domain) عبر DNS قبل توجيه عمليات الدخول (routing logins) بناءً عليه.
- الخيار الافتراضي للنسخة الأولى (v1): اشترِ (WorkOS وأمثاله) أو استضف Ory Polis (SAML Jackson) بنفسك، وابنِ فقط الربط بين المنظمة والاتصال (org-to-connection mapping).
- التزويد الفوري (JIT) ينشئ المستخدمين لكنه لا يزيلهم أبدًا. إلغاء التزويد (deprovisioning) يحتاج SCIM، والتعطيل (deactivation) يجب أن يلغي الجلسات (revoke sessions) ومفاتيح API.
- الفخ الأكبر: فرض SSO دون مسار كسر الزجاج (break-glass path)، فتؤدي شهادة منتهية (expired certificate) لدى مزوّد الهوية (IdP) إلى إقفال الباب على الجميع.

## 🧭 لماذا يحتاجه كل SaaS

يصل أول عميل مؤسسي محتمل (enterprise lead) إلى Beacon: شركة من 2,000 موظف تريد 300 مقعد على خطة Business. يعود استبيان الأمان (security questionnaire) وفيه سطران مظلّلان. "هل يدعم المنتج SAML SSO مع Okta؟" و"هل يدعم التزويد عبر SCIM (SCIM provisioning)؟" إذا كانت إجابة أي منهما لا، تتوقف الصفقة (deal) عند هذا الحد.

العميل لا يتعمّد التعقيد. فريق تقنية المعلومات لديه يدير آلاف الموظفين عبر مئات التطبيقات. عندما ينضم شخص، يريدون أن يحصل على الوصول إلى كل شيء عبر تسجيل دخول واحد، مع تطبيق سياسة MFA (MFA policy) الخاصة بالشركة. وعندما يُفصل شخص الساعة 4 عصرًا، يريدون أن يُقفل كل تطبيق، بما فيه Beacon، الباب في وجهه بحلول 4:01، دون أن يتذكر أحد الدخول إلى صفحة إعدادات (settings page) Beacon. **الدخول الموحد (SSO، Single Sign-On)** يتولى نصف تسجيل الدخول. و**SCIM (نظام إدارة الهوية (identity) عبر النطاقات (domains))** يتولى نصف الانضمام والمغادرة.

بدون هذين، يحتفظ الموظفون السابقون لدى العميل الكبير بحسابات Beacon عاملة لشهور، ويلاحظ المدققون (auditors) ذلك. ومعهما، لم تعد مجرد تطبيق، بل جزءًا منضبطًا من البنية التحتية للهوية (identity infrastructure) لديهم.

**هوية المؤسسات (enterprise identity) تعني أن مزوّد هوية العميل (the customer's IdP)، لا قاعدة بياناتك (database)، هو من يقرّر من يستطيع تسجيل الدخول (login) ومن ما زال يعمل هناك.**

## 📐 كيف يعمل

### 🟢 الأساسيات

المفردات أولًا:

- **IdP (مزوّد الهوية (IdP)، Identity Provider)**: النظام الذي يحتفظ بموظفي العميل ويصادق (authenticates) عليهم. Okta، وMicrosoft Entra ID (سابقًا Azure AD)، وGoogle Workspace، وJumpCloud، وOneLogin.
- **SP (مزوّد الخدمة (SP)، Service Provider)**، ويُسمى **RP (الطرف المعتمد (relying party)، Relying Party)** في OIDC: التطبيق الذي يثق بمزوّد الهوية. وهو هنا Beacon.
- **الاتصال** (Connection): علاقة ثقة (trust relationship) مضبوطة واحدة بين منظمة واحدة في Beacon ومزوّد هوية واحد، وتحتفظ ببيانات تعريف مزوّد الهوية (Metadata) أو شهاداته (certificates) أو بيانات اعتماد العميل (client credentials).
- **SAML 2.0**: المعيار الأقدم (standard) القائم على XML (من OASIS، عام 2005). وهو المهيمن في المؤسسات.
- **OIDC (OpenID Connect)**: معيار JSON وJWT من الدرس 1.1، ويُستخدم هنا مع مزوّد الهوية الخاص بالعميل بدلًا من تسجيل الدخول الاستهلاكي (consumer login) عبر Google.

| | SAML 2.0 | OIDC |
|---|---|---|
| الصيغة | تأكيد (Assertion) XML موقّع | رمز هوية JWT موقّع (signed) |
| النقل (transport) | إرسال POST من المتصفح إلى رابط ACS (ACS URL) الخاص بك | إعادة توجيه مع رمز، ثم تبادل الرموز (token exchange) عبر قناة خلفية (back-channel) |
| الإعداد | تبادل ملف بيانات تعريف XML (معرّف الكيان (entity id)، رابط ACS، الشهادة) | رابط المُصدِر (issuer URL)، ومعرّف العميل (client id)، وسرّ العميل (client secret) |
| أين تراه | Okta، وEntra ID، وADFS، ومعظم المؤسسات الكبيرة | الإعدادات الأحدث، وGoogle Workspace، وEntra ID أيضًا |
| الخطر الرئيسي (main risk) | ثغرات التحقق من توقيع XML | أخطاء في ضبط (misconfigured) فحص المُصدِر أو الجمهور (audience) |

مسار SAML الذي يبدأ من مزوّد الخدمة (SP-initiated)، وهو المسار الذي يجب أن تدعمه أولًا:

```mermaid
sequenceDiagram
    participant I as مزوّد هوية العميل Okta (Customer IdP Okta)
    participant B as Beacon مزوّد الخدمة (Beacon SP)
    participant U as متصفح الموظف (Employee browser)
    U->>B: إدخال البريد ana@bigco.com في صفحة الدخول (Enter email ana@bigco.com on login page)
    B->>B: البحث عن اتصال SSO للنطاق bigco.com (Look up SSO connection for bigco.com)
    B-->>U: إعادة توجيه إلى مزوّد الهوية مع AuthnRequest موقّع وRelayState (Redirect to IdP with signed AuthnRequest and RelayState)
    U->>I: اتباع إعادة التوجيه (Follow redirect)
    I->>U: عرض صفحة دخول مزوّد الهوية مع MFA الشركة (Show IdP login with company MFA)
    U->>I: المصادقة (Authenticate)
    I-->>U: نموذج HTML يرسل SAMLResponse تلقائيًا (HTML form auto-posting SAMLResponse)
    U->>B: POST SAMLResponse إلى رابط ACS (POST SAMLResponse to ACS URL)
    B->>B: التحقق من التوقيع والمُصدِر والجمهور والنافذة الزمنية وInResponseTo (Verify signature, issuer, audience, time window, InResponseTo)
    B->>B: إيجاد أو إنشاء المستخدم والعضوية في منظمة BigCo (Find or create user and membership in BigCo org)
    B-->>U: ضبط كوكي الجلسة وإعادة التوجيه إلى لوحة التحكم (Set session cookie and redirect to dashboard)
```

الخطوة الموسومة "التحقق" هي مكان الخطر. للتحقق من SAML (SAML validation) تاريخ طويل من الثغرات، لأن توقيعات XML (XML signatures) يمكن أن تغطي جزءًا من المستند (document) بينما يقرأ الكود جزءًا آخر (التفاف توقيع XML، XML Signature Wrapping). مكتبات (libraries) واسعة الاستخدام مثل ruby-saml أصدرت إصلاحات حرجة (critical fixes) لتجاوز التوقيع (signature-bypass) حتى في 2024 و2025. **لا تحلّل SAML ولا تتحقق منه بنفسك أبدًا.** استخدم مكتبة أو خدمة مُصانة، وأبقِها محدّثة (patched)، وافحص كل واحد مما يلي:

- التوقيع صالح وصادر عن الشهادة (certificate) المضبوطة *لهذا الاتصال*، لا عن أي شهادة يحملها الرد.
- `Issuer` يساوي معرّف كيان مزوّد الهوية لهذا الاتصال.
- `Audience` يساوي معرّف كيان مزوّد الخدمة في Beacon، و`Destination` أو `Recipient` يساوي رابط ACS.
- `NotBefore` و`NotOnOrAfter` متحققان، مع هامش صغير لانحراف الساعة (clock-skew).
- `InResponseTo` يطابق طلبًا أرسله Beacon فعلًا، ومعرّف التأكيد (assertion id) لم يُرَ من قبل (حماية من إعادة الإرسال).

**الدخول الذي يبدأ من مزوّد الهوية (IdP-initiated login)** (IdP-initiated)، حيث ينقر المستخدم أيقونة (tile) Beacon في لوحة Okta، يصل دون `InResponseTo` للمطابقة. كثير من العملاء يتوقعونه. ادعمه عن قصد، مع حماية صارمة من إعادة الإرسال، أو حوّله إلى مسار يبدأ من مزوّد الخدمة.

**ربط تسجيل الدخول (login) بمنظمة** يُسمى **اكتشاف النطاق الأصلي** (Home Realm Discovery): يكتب المستخدم بريده، فيستخرج Beacon النطاق ويبحث عن الاتصال الذي يتولاه. وهذا لا يعمل بأمان إلا إذا أثبتت المنظمة ملكيتها للنطاق.

### 🟡 التعمق أكثر

**التحقق من النطاق (domain verification).** قبل أن تستطيع Acme المطالبة بـ `acme.com`، تثبت ملكيتها بإضافة سجل DNS (DNS record) من نوع TXT (DNS TXT record) يولّده Beacon، مثل `beacon-verification=3f9a...`. يفحص Beacon السجل عبر DNS، ثم يعيد فحصه دوريًا (periodically). بدون هذه الخطوة، يستطيع أي شخص إنشاء منظمة والمطالبة بـ `bigbank.com`، وتوجيه عمليات دخول موظفي BigBank عبر مزوّد هوية يتحكم فيه. لا تسمح أبدًا بالمطالبة بنطاقات البريد العامة (public email domains) مثل `gmail.com`.

**التزويد الفوري (JIT، Just-in-Time Provisioning).** في أول مرة تسجّل فيها `ana@acme.com` الدخول عبر SSO، ينشئ Beacon مستخدمها وعضويتها في اللحظة نفسها، مستخدمًا الدور الافتراضي (default role) المضبوط للاتصال. هذا بسيط، وبه تبدأ معظم منتجات SaaS. لكن فيه ثغرة خطيرة (gap) واحدة: **JIT يستطيع إنشاء المستخدمين (users) لكنه لا يزيلهم أبدًا.** عندما تغادر Ana شركة Acme، تتوقف ببساطة عن تسجيل الدخول، وأي جلسة Beacon قائمة، مع أي مفتاح API أنشأته، يستمر في العمل حتى ينتهي شيء ما.

**ربط السمات والمجموعات (attribute and group mapping).** تأكيدات (assertions) SAML ورموز هوية (ID tokens) OIDC يمكن أن تحمل سمات: الاسم، والبريد، وغالبًا عضوية المجموعات (group membership) (`groups: ["sre", "beacon-admins"]`). اسمح لمسؤول العميل بربط مجموعات مزوّد الهوية (IdP groups) بأدوار Beacon ("أعضاء `beacon-admins` مسؤولون"). طبّق هذا الربط عند كل تسجيل دخول، لا في المرة الأولى فقط، حتى تنتقل تغييرات الأدوار في مزوّد الهوية.

**SCIM 2.0** يسدّ ثغرة إلغاء التزويد (deprovisioning gap). إنه واجهة REST *تعرضها أنت* و*يستدعيها مزوّد الهوية*، ويعرّفها RFC 7643 (المخطط الأساسي (core schema) للمستخدمين والمجموعات) وRFC 7644 (البروتوكول). يدفع مزوّد الهوية التغييرات فور حدوثها في دليله (directory):

| الحدث في مزوّد الهوية (IdP event) | طلب SCIM (SCIM request) إلى Beacon | إجراء Beacon |
|---|---|---|
| إسناد المستخدم (assigned) إلى تطبيق Beacon | `POST /scim/v2/Users` | إنشاء المستخدم والعضوية |
| تغيّر الاسم أو البريد | `PUT` أو `PATCH /scim/v2/Users/{id}` | تحديث المستخدم |
| إلغاء إسناد المستخدم (unassigned) أو تعليقه (suspended) | `PATCH` يضبط `active` على false | تعطيل العضوية، وإلغاء الجلسات والرموز |
| حذف المستخدم | `DELETE /scim/v2/Users/{id}` | إزالة العضوية |
| إنشاء مجموعة أو تغيّر أعضائها | `POST` أو `PATCH /scim/v2/Groups` | إعادة حساب ربط الأدوار (role mappings) |
| مزوّد الهوية يطابق البيانات (reconciles) | `GET /scim/v2/Users?filter=userName eq "ana@acme.com"` | إرجاع المستخدم المطابق |

تحصل كل منظمة على رابط SCIM أساسي (base URL) خاص بها ورمز حامل (Bearer Token)، يُخزَّن مُجزَّأً، ويولّده مسؤول في إعدادات Beacon ويلصقه في مزوّد الهوية. ومعالِج إلغاء التزويد هو الجزء الأهم:

```ts
// PATCH /scim/v2/Users/:id  (auth: per-org SCIM bearer token)
export async function patchScimUser(org: Org, scimId: string, body: ScimPatch) {
  const member = await db.membership.findFirst({ where: { orgId: org.id, scimId } });
  if (!member) return scimError(404, "User not found");

  for (const op of body.Operations) {
    // IdPs differ: some send { path: "active", value: false },
    // others send { value: { active: false } } with no path.
    const active = op.path === "active" ? op.value : op.value?.active;
    if (active === false || active === "False") {
      await db.$transaction([
        db.membership.update({ where: { id: member.id }, data: { deactivatedAt: new Date() } }),
        db.session.deleteMany({ where: { userId: member.userId, orgId: org.id } }),
        db.apiKey.updateMany({ where: { createdBy: member.userId, orgId: org.id },
                               data: { revokedAt: new Date() } }),
      ]);
      await audit(org.id, "scim.user.deactivated", { userId: member.userId });
    }
  }
  return scimUser(await reload(member));
}
```

لاحظ أن الجلسات محصورة بالمنظمة (scoped). فقد تنتمي Ana أيضًا إلى مساحة عمل شخصية أو إلى منظمة عميل آخر، ومزوّد هوية Acme (Acme's IdP) له سلطة على Acme فقط. ولاحظ أيضًا التسامح مع اللهجات (dialects) المختلفة: عمليًا، كل مزوّد هوية رئيسي يفسّر SCIM بطريقة مختلفة قليلًا، لذلك اختبر مع كل مزوّد تدّعي دعمه.

**فرض SSO (enforcing SSO).** بعد أن يعمل SSO، سيريد مسؤول العميل (customer admin) *اشتراطه (require)*: لا يعود بإمكان المستخدمين على النطاق الموثَّق (verified domain) تسجيل الدخول إلى منظمة Acme بكلمة مرور أو عبر Google. افرضه عند حدود المنظمة (org boundary)، أي عند تحديد العضوية (resolving membership)، لا في صفحة الدخول (login page) فقط. والمستخدم الذي سجّل الدخول بكلمة مرور قبل تفعيل الفرض (enforcement) يجب أن يُجبر على المرور عبر SSO في طلبه التالي لتلك المنظمة.

**وصول كسر الزجاج** (Break-glass Access). إذا تعطّل مزوّد هوية العميل أو أُسيء ضبطه، وكان SSO مفروضًا، فلن يستطيع أحد الدخول لإصلاح الاتصال. احتفظ بمسار **كسر الزجاج (break-glass)**: مالك أو مالكان محددان بالاسم يُسمح لهما بالدخول بكلمة مرور مع MFA قوية حتى مع الفرض، مع تسجيل تدقيق (audit logging) واضح وبريد لكل المالكين كلما استُخدم.

### 🔴 على نطاق واسع وللمؤسسات

**عدة مزوّدي هوية لكل مستأجر (multiple IdPs per tenant).** الشركات تستحوذ على شركات أخرى. قد يكون لدى BigCo موظفون في Okta وشركة تابعة (subsidiary) استُحوذ عليها حديثًا ما زالت على Entra ID، وكلاهما يحتاج منظمة Beacon نفسها. مثّل الاتصالات (connections) كقائمة لكل منظمة، لكل منها نطاقاتها الموثَّقة، ووجّه حسب النطاق أثناء اكتشاف النطاق الأصلي. ويمكن أن يبقى المتعاقدون (contractors) على نطاقات خارجية على الدخول بكلمة مرور مع MFA كاستثناء صريح (explicit exception).

**أن تكون مزوّد خدمة (SP) لا يرتبط بمزوّد هوية بعينه (IdP-agnostic SP).** لكل مزوّد هوية خصوصياته (quirks): جداول تدوير الشهادات، وصيغ NameID، وأسماء السمات (attribute names)، ولهجات SCIM (SCIM dialects). لهذا نادرًا ما يكون SSO "مجرد إضافة مكتبة". إنه منتج صغير بشاشات إعداد ذاتية الخدمة، ورفع لبيانات التعريف (metadata upload)، وزر اختبار الاتصال (test-connection button)، ورسائل خطأ (error messages) واضحة ("الجمهور في الرد كان X، والمتوقع Y")، وأدلة تشغيل للدعم (support runbooks). بوابات الإدارة (admin portals) من WorkOS وOry Polis موجودة لأن بناء هذه الشاشات هو معظم العمل.

**عمر الجلسة (session lifetime) مقابل حالة مزوّد الهوية (IdP).** يثبت SSO الهوية عند الدخول. لكنه لا يخبر Beacon عندما يعطّل مزوّد الهوية الحساب لاحقًا. هذا ما يغطيه SCIM. وبدون SCIM، اجعل جلسات SSO (SSO sessions) أقصر (ساعات لا أسابيع) حتى يعيد المستخدمون المصادقة (re-authenticate) مع مزوّد الهوية كثيرًا. بعض العملاء سيطلبون الأمرين معًا.

**ضريبة SSO (SSO tax).** كثير من مزوّدي SaaS (SaaS vendors) يضعون SSO في أعلى خطة (top tier) فقط، وغالبًا بزيادة كبيرة في السعر (markup)، ويسرد الموقع المجتمعي sso.tax أمثلة على ذلك. يرى المختصون بالأمن (security people) أن SSO ضابط أمني (security control) أساسي لا يجب أن يكون رفاهية. ويرد المزوّدون (vendors) بأن عملاء SSO يجلبون تكاليف حقيقية (إعداد لكل عميل، ودعم لمزوّدي الهوية (IdPs)، ومراجعات أمنية) وأنه أوضح إشارة إلى مشترٍ مؤسسي (enterprise buyer). يضع Beacon الخدمة SSO في خطة Business بسعر 199 دولارًا شهريًا، وهو حل وسط معقول. وأيًا كان اختيارك، لا تتقاضَ مالًا مقابل MFA، وفكّر في جعل الدخول عبر Google Workspace أو OIDC رخيصًا مع إبقاء SAML وSCIM في الخطة الأعلى.

**طلبات مؤسسية (enterprise requests) أخرى** ستواجهها بعد ذلك: سجلات تدقيق لكل تسجيل دخول وكل تغيير في الصلاحيات (الدرس 7.3)، وقوائم سماح لعناوين IP (IP allow-lists)، وأعمار جلسات مخصصة لكل منظمة، ووصول الدعم (support access) "سجّلني باسم مستخدم هذا العميل" الذي يحترم هو نفسه SSO ويخضع للتدقيق (الدرس 7.1).

## 🏆 أفضل المستودعات

| المستودع | ما هو | التقنيات | الترخيص | اختره عندما |
|---|---|---|---|---|
| [ory/polis](https://github.com/ory/polis) | Ory Polis: جسر من SAML إلى OAuth (SAML-to-OAuth bridge) مع مزامنة أدلة SCIM | TypeScript | Apache-2.0 | تريد إضافة SAML SSO وSCIM إلى تطبيقك دون تعلّم تفاصيل SAML الداخلية (internals) |
| [keycloak/keycloak](https://github.com/keycloak/keycloak) | خادم IAM كامل يتوسط (brokers) بين SAML وOIDC ويتحد (federates) مع LDAP | Java | Apache-2.0 | تريد وسيط هوية (identity broker) ناضجًا تستضيفه بنفسك وتستطيع تشغيل خدمة JVM |
| [zitadel/zitadel](https://github.com/zitadel/zitadel) | منصة هوية (identity platform) متعددة المستأجرين فيها منظمات وSAML وOIDC وميزات SCIM | Go | AGPL-3.0 | نموذج المستأجرين (tenancy model) لديك يتوافق مع منظماتها وتقبل AGPL |
| [goauthentik/authentik](https://github.com/goauthentik/authentik) | مزوّد هوية تستضيفه بنفسك مع مسارات مرنة وSAML وOIDC وLDAP وSCIM | Python, Go | MIT | تريد تشغيل مزوّد هوية خاص بك، أو اختبار مزوّد الخدمة لديك مقابله محليًا |
| [ory/hydra](https://github.com/ory/hydra) | خادم OAuth 2.0 وOIDC معتمد (certified) يفوّض (delegates) تسجيل الدخول إلى تطبيقك | Go | Apache-2.0 | تحتاج أن تكون أنت مزوّد OIDC، مثلًا لعملاء الواجهة البرمجية (API clients) الخاصة بك |
| [logto-io/logto](https://github.com/logto-io/logto) | منصة مصادقة فيها منظمات وموصلات (connectors) SSO للمؤسسات | TypeScript | MPL-2.0 | تريد SSO للمؤسسات بجانب الدخول العادي (regular sign-in) في منتج واحد تستضيفه بنفسك |
| [boxyhq/saas-starter-kit](https://github.com/boxyhq/saas-starter-kit) | قالب بداية Next.js يربط SAML SSO ومزامنة الأدلة وسجلات التدقيق والويب هوك (webhooks) بالفرق | TypeScript | Apache-2.0 | تريد رؤية جانب مزوّد الخدمة (SP side) في SSO وSCIM مربوطًا بنموذج فرق حقيقي |
| [panva/openid-client](https://github.com/panva/openid-client) | عميل معتمد لطرف معتمد (relying-party client) في OAuth 2 وOIDC لبيئات تشغيل JavaScript (runtimes) | TypeScript | MIT | تنفّذ اتصالات OIDC (OIDC connections) لكل مستأجر (per-tenant) بنفسك |

**إن درست مستودعًا واحدًا فقط (If you only study one):** **ory/polis** (سابقًا SAML Jackson). إنه يحل بالضبط مشكلة جانب مزوّد الخدمة التي لدى Beacon: يحوّل اتصال SAML لكل مستأجر (per tenant) إلى مسار OAuth 2.0 عادي يفهمه تطبيقك أصلًا، ويضيف مزامنة أدلة SCIM خلف واجهة بسيطة (simple interface). قراءته تعلّمك كيف تُمثَّل الاتصالات والمستأجرون والمنتجات، وهو ما تستخدمه Dub وFormbricks وPapermark لدعم (support) SAML لديها.

**اشترِ أم ابنِ أم استضف بنفسك (Buy, build, or self-host)؟**

- **اشترِ (buy)** WorkOS أو Auth0/Okta (Enterprise Connections) أو Clerk (SSO للمؤسسات) أو Stytch عندما تبدأ صفقات المؤسسات (enterprise deals) بالوصول وتريد بوابة إدارة (admin portal) يضبط فيها فريق تقنية المعلومات لدى العميل SSO وSCIM بنفسه. هذا هو الخيار الأكثر شيوعًا، وتسعيره لكل اتصال (per connection)، لذلك يتماشى مع الإيرادات (revenue).
- **استضف بنفسك (self-host)** Ory Polis أو Keycloak أو Zitadel أو authentik عندما يجب أن تبقى البيانات في بنيتك التحتية، أو عندما تقدّم نسخة للاستضافة الذاتية (self-hosted edition)، أو عندما لا يناسب التسعير لكل اتصال هوامش أرباحك (margins).
- **ابنِ (build)** الطبقة الرقيقة (thin layer) فقط: ربط المنظمة بالاتصال، والتحقق من النطاق، وقواعد الفرض وكسر الزجاج، ومنطق تحويل SCIM إلى عضويات (SCIM-to-membership logic). لا تكتب أبدًا تحققك الخاص من توقيع XML في SAML.

## 🔍 ادرسه في مشاريع حقيقية

**boxyhq/saas-starter-kit** يربط SAML Jackson (الآن Ory Polis) بنموذج فرق في Next.js. اقرأ `lib/jackson.ts` ومجلد `lib/jackson/sso` لتجد الإعداد، وطريقة تسمية المستأجرين، ومعالجة طلب العودة (callback handling)، وتتبّع كيف يصبح دخول SSO (SSO login) مستخدمًا في الفريق الصحيح. ثم افتح `lib/jackson/dsyncEvents.ts` لترى كيف تتحول أحداث مزامنة أدلة SCIM إلى عضويات في الفرق.

**dubinc/dub** يضيف SAML SSO لمساحات العمل فيه. ابحث عن `saml` و`jackson` في `apps/web`، وانظر كيف تتيح صفحة إعدادات مساحة العمل (workspace settings) للمسؤول ضبط اتصال، وكيف يتفاعل الفرض مع خيارات الدخول (login options) الموجودة.

**Infisical/infisical** يدعم SAML وOIDC وLDAP وSCIM لأن مشتريه فرق أمن (security teams). ابحث عن `scim` لتقرأ تنفيذ خادم SCIM (SCIM server) حقيقيًا، بما في ذلك طريقة معالجة إلغاء التزويد، وعن `saml` لترى ضبط الاتصال لكل منظمة وفرض SSO.

**getsentry/sentry** يدعم منذ زمن طويل SSO للمنظمات عبر مزوّدي مصادقة (auth providers) قابلين للتركيب، بما فيهم SAML2. ابحث عن `saml2` و`AuthProvider` لترى كيف تُربط منظمة واحدة بمزوّد واحد وكيف تُربط هويات الأعضاء به.

**ما الذي تلاحظه (What to notice):**

- كيف يُحدَّد المستأجر أثناء SSO: نطاق البريد (email domain)، أو المعرّف النصي للمنظمة في الرابط، أو صفحة دخول مخصصة لـ SSO.
- ماذا يحدث عند أول دخول عبر SSO: إنشاء المستخدم عبر JIT، وأي دور يُسند، وهل يُربط مستخدم كلمة مرور موجود أم يُمنع.
- كيف يؤثر تعطيل SCIM (SCIM deactivation) على الجلسات ورموز API، لا على صف العضوية فقط.
- كيف يُفرض "اشتراط SSO (requiring SSO)"، وهل يوجد أي تجاوز للمالكين.
- أين يحدث التحقق من SAML فعلًا، ويجب أن يكون دائمًا داخل مكتبة مُصانة (maintained library).

## 🛠️ ابنِه في Beacon

### 🟢 تمرين المبتدئ

شغّل authentik أو Keycloak محليًا عبر Docker كمزوّد هوية للاختبار. استضف SAML Jackson (Ory Polis) بنفسك واربط منظمة واحدة في Beacon بمزوّد الهوية المحلي. اسمح لمستخدم بالدخول عبر SSO والوصول إلى المنظمة الصحيحة.

**يكتمل عندما (Done when):**
- يستطيع مستخدم أُنشئ في مزوّد الهوية المحلي تسجيل الدخول إلى Beacon دون كلمة مرور لـ Beacon.
- يصل المستخدم إلى المنظمة التي تملك الاتصال، بالدور الافتراضي.
- يُرفض رد SAML المُتلاعب به (tampered) أو المنتهي، مع خطأ واضح (clear error) في السجلات.

### 🟡 تمرين المستوى المتوسط

أضف التحقق من النطاق عبر سجل DNS من نوع TXT، واكتشاف النطاق الأصلي في صفحة الدخول، والتزويد عبر JIT (JIT provisioning) مع ربط مجموعات مزوّد الهوية بالأدوار، وإعداد "فرض SSO" للمنظمة مع استثناء كسر الزجاج (break-glass exception) للمالكين.

**يكتمل عندما (Done when):**
- لا تستطيع المنظمة ضبط SSO لنطاق حتى يُتحقق من سجل TXT (TXT record).
- كتابة بريد على نطاق موثَّق توجّه تلقائيًا إلى مزوّد هوية تلك المنظمة.
- مع تفعيل الفرض، يُرفض الدخول بكلمة مرور إلى تلك المنظمة للجميع باستثناء (exception) المالكين المعيّنين لكسر الزجاج، وكل دخول بكسر الزجاج يُدقَّق ويُرسل عنه بريد.
- تغيير مجموعة المستخدم في مزوّد الهوية يغيّر دوره في Beacon عند الدخول التالي.

### 🔴 تمرين المستوى المتقدم

نفّذ خادم SCIM 2.0 للمستخدمين والمجموعات (أو استخدم مزامنة الأدلة في Ory Polis واستهلك أحداثها). اربطه بمزوّد الهوية المحلي وبمستأجر مطوّر (developer tenant) حقيقي لدى مزوّد هوية (Okta وMicrosoft Entra ID كلاهما يوفر مستأجرين مجانيين للمطورين). ادعم اتصالين (two connections) على منظمة واحدة، يُوجَّه بينهما حسب النطاق.

**يكتمل عندما (Done when):**
- إسناد مستخدم إلى Beacon في مزوّد الهوية ينشئ عضويته دون أن يسجّل الدخول.
- تعطيل مستخدم في مزوّد الهوية ينهي جلساته في Beacon لتلك المنظمة ويلغي مفاتيح API الخاصة به خلال دقيقة.
- `GET /scim/v2/Users?filter=userName eq "..."` يُرجع النتائج بصيغة رد القائمة (list-response format) في RFC 7644.
- يعمل الاتصالان معًا، والبريد من أي من النطاقين يصل إلى مزوّد الهوية الصحيح.

## ⚠️ أخطاء يقع فيها المبتدئون

- **كتابة التحقق من SAML (SAML validation) يدويًا.** تمكّن التفاف توقيع XML من تجاوز التحقق (bypassing validation) في مكتبات معروفة. استخدم مكتبة أو خدمة مُصانة وحدّثها مثل أي اعتماد أمني (security dependency) آخر.
- **السماح لأي منظمة (organization) بالمطالبة بأي نطاق (domain).** بدون التحقق عبر DNS، يستطيع المهاجم توجيه عمليات دخول شركة أخرى إلى مزوّد هوية يتحكم فيه. تحقّق من النطاقات، وأعد الفحص دوريًا، وامنع نطاقات البريد العامة.
- **معاملة JIT كتزويد (as provisioning).** JIT لا يزيل أحدًا أبدًا. إذا طلب العميل إلغاء التزويد، فهو يقصد SCIM، أو على الأقل أعمار جلسات (session lifetimes) SSO قصيرة.
- **تعطيل العضوية (deactivating the membership) دون الجلسات والرموز (tokens).** يستمر تبويب المتصفح (browser tab) المفتوح ومفتاح API للموظف المفصول في العمل. ألغِ كل ما يرتبط بذلك المستخدم في تلك المنظمة داخل المعاملة نفسها.
- **فرض SSO (enforcing SSO) دون كسر الزجاج (break-glass).** في أول مرة تنتهي فيها شهادة مزوّد هوية العميل، لن يستطيع أحد الدخول لإصلاحها، ولا العميل نفسه. احتفظ بوصول احتياطي (backup access) مُدقَّق للمالكين.
- **ربط مستخدم SSO (SSO user) بالبريد (email) وحده، عبر المنظمات (organizations).** مزوّد الهوية لا يتحدث إلا باسم نطاقاته الموثَّقة ومنظمته. خزّن معرّف الفاعل (subject id) الخاص بالاتصال (NameID أو `sub`) على الهوية، ولا تسمح أبدًا لمزوّد هوية مستأجر بإدخال شخص إلى مستأجر آخر (another tenant).

## 🧾 الخلاصة

- SSO يتعلق بتسجيل الدخول، وSCIM يتعلق بدورة حياة الموظف (employee lifecycle). المؤسسات تريد الاثنين.
- SAML وOIDC كلاهما يعني أن مزوّد هوية العميل يصادق، وأن Beacon يتحقق من تأكيد أو رمز موقّع لاتصال محدد.
- تحقّق من النطاقات قبل توجيه عمليات الدخول حسب النطاق، ولا تكتب التحقق من SAML بنفسك أبدًا.
- JIT ينشئ المستخدمين. وSCIM وحده، أو الجلسات القصيرة (short sessions)، يزيلهم. والتعطيل يجب أن ينهي الجلسات والرموز.
- الفرض يحتاج مسار كسر الزجاج، والعملاء الكبار يحتاجون عدة مزوّدي هوية (multiple IdPs) لكل منظمة.
- معظم الفرق تشتري أو تستضيف Ory Polis بنفسها، ولا تبني إلا قواعد ربط المستأجرين (tenant-mapping rules).

## ✍️ اختبر نفسك

**1. ماذا يتولى SSO، وماذا يتولى SCIM، ولماذا تريد المؤسسات (enterprises) الاثنين؟**

<details><summary>الإجابة</summary>

يتولى SSO تسجيل الدخول: مزوّد هوية العميل يصادق الموظفين بسياسة MFA الخاصة به. ويتولى SCIM دورة حياة الموظف: مزوّد الهوية يدفع الانضمامات والتغييرات والمغادرات إلى Beacon. SSO وحده لا يستطيع أن يخبر Beacon بأن شخصًا ما فُصل. راجع "🧭 لماذا يحتاجه كل SaaS".

</details>

**2. اذكر أربعة أشياء يجب أن يفحصها Beacon عندما يتلقى رد SAML.**

<details><summary>الإجابة</summary>

التوقيع صالح وصادر عن الشهادة المضبوطة لهذا الاتصال، و`Issuer` يساوي معرّف كيان مزوّد الهوية، و`Audience` يساوي معرّف كيان مزوّد الخدمة في Beacon مع `Destination` أو `Recipient` مساويًا لرابط ACS، و`NotBefore` و`NotOnOrAfter` متحققان، و`InResponseTo` يطابق طلبًا أرسله Beacon ومعرّف التأكيد ليس إعادة إرسال. أي أربعة من هذه. راجع "🟢 الأساسيات".

</details>

**3. تستخدم BigCo الدخول الموحد (SSO) مع التزويد عبر JIT (JIT provisioning) دون SCIM. غادرت Ana الشركة يوم الجمعة. ما الذي ما زال يعمل لها في Beacon يوم الاثنين، وكيف تسدّ الثغرة (hole)؟**

<details><summary>الإجابة</summary>

JIT لا يزيل أحدًا أبدًا، لذلك تستمر أي جلسة Beacon قائمة وأي مفتاح API أنشأته في العمل حتى ينتهي شيء ما. أضف SCIM حتى يلغي تعطيل مزوّد الهوية عضويتها وجلساتها ومفاتيح API الخاصة بها في تلك المنظمة، أو على الأقل أبقِ جلسات SSO قصيرة. راجع "التزويد الفوري" و"SCIM 2.0" في "🟡 التعمق أكثر".

</details>

**4. سجّلت منظمة (organization) جديدة وطالبت بالنطاق (domain) `bigbank.com` لـ SSO حتى يسجّل موظفو BigBank الدخول (login) عبر مزوّد الهوية (IdP) الخاص بها. ما الذي يجب أن يشترطه Beacon أولًا، ولماذا؟**

<details><summary>الإجابة</summary>

التحقق من النطاق: تضيف المنظمة سجل DNS من نوع TXT يولّده Beacon، ثم يفحصه Beacon ويعيد فحصه دوريًا. بدون ذلك، يستطيع أي شخص توجيه عمليات دخول شركة أخرى عبر مزوّد هوية يتحكم فيه. ويجب ألا يُسمح أبدًا بالمطالبة بنطاقات البريد العامة مثل `gmail.com`. راجع "التحقق من النطاق" في "🟡 التعمق أكثر".

</details>

**5. فعّلت Acme خيار "فرض SSO (enforcing SSO)" لمنظمتها (its organization) دون أي استثناءات. بعد أشهر انتهت شهادة مزوّد الهوية (IdP certificate) لديها. ما الذي يتعطّل؟**

<details><summary>الإجابة</summary>

لا يستطيع أحد تسجيل الدخول إلى منظمة Acme، بمن فيهم المسؤولون الذين يحتاجون إلى إصلاح الاتصال. احتفظ بمسار كسر الزجاج: مالك أو مالكان محددان بالاسم يُسمح لهما بالدخول بكلمة مرور مع MFA قوية تحت الفرض، مع تسجيل تدقيق واضح وبريد لكل المالكين عند كل استخدام. راجع "وصول كسر الزجاج" في "🟡 التعمق أكثر".

</details>

## 📚 المراجع

- OASIS SAML 2.0 specifications — https://docs.oasis-open.org/security/saml/v2.0/ (مواصفات SAML 2.0)
- OpenID Connect Core 1.0 — https://openid.net/specs/openid-connect-core-1_0.html
- RFC 7643, SCIM: Core Schema — https://www.rfc-editor.org/rfc/rfc7643 (المخطط الأساسي لـ SCIM)
- RFC 7644, SCIM: Protocol — https://www.rfc-editor.org/rfc/rfc7644 (بروتوكول SCIM)
- OWASP Cheat Sheet Series: SAML Security cheat sheet — https://cheatsheetseries.owasp.org (الورقة المرجعية لأمان SAML)
- Ory documentation, including Ory Polis — https://www.ory.sh/docs
- WorkOS documentation on SSO and Directory Sync — https://workos.com/docs (الدخول الموحد ومزامنة الأدلة)
- The SSO Wall of Shame — https://sso.tax

التالي: **الوحدة 2 (Module 2) — البيانات**، حيث تلتقي الجداول المحصورة بالمنظمة (org-scoped tables) من هذه الوحدة بـ Postgres والترحيلات (migrations) وتخزين الملفات (file storage) والبحث.
