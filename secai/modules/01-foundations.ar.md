# الوحدة 1 — التفكير بعقلية المدافع (Thinking like a defender)

*المهاجمون (Attackers) لا يقرؤون وثائق التصميم (design documents) الخاصة بك. إنهم يبحثون عن الموضع الذي وثقتَ فيه بشيءٍ ما كان ينبغي أن تثق به (trusted something you should not have). تمنحك هذه الوحدة العادات الثلاث (three habits) التي تعتمد عليها كل وحدة لاحقة. تحوّل نمذجة التهديدات (threat modelling) النظامَ إلى مخططٍ لتدفقات البيانات (data flows) وحدود الثقة (trust boundaries)، ثم تسأل بصورةٍ منهجية (systematically) عمّا قد يسوء (what can go wrong) عند كل عبور (crossing). وتضمن المبادئ الأمنية (security principles)، وهي أقل الصلاحيات (least privilege) والدفاع المتعدد الطبقات (defence in depth) والإعدادات الافتراضية الآمنة (secure defaults) وانعدام الثقة (zero trust)، ألّا يتحول خطأٌ برمجي واحد (one bug) إلى اختراق (breach) حين يسوء شيءٌ فعلًا. ويحدد تقييم المخاطر (risk rating) ما يُصلَح أولًا (what to fix first) حين تكون القائمة أطول من الوقت المتاح. ستتابع عليًّا خلال شهره الأول في فريق أمن التطبيقات والذكاء الاصطناعي (Application & AI Security team) في بنك نجم (Najm Bank): ينمذج تهديدات أول أداة (first tool) يستطيع نجم أسيست (Najm Assist) استدعاءها، ويعترض على حجم الوصول (how much access) الذي ينبغي أن يحصل عليه المساعد، ويحوّل قائمةً متراكمة (backlog) من 4,100 ملاحظة للماسحات (scanner findings) إلى قائمةٍ قصيرة (short list) تستطيع نورة الدفاع عنها أمام حمد.*

> **المراحل (Phases):** Plan, Design, Build, Operate — رؤية النظام كما يراه المهاجم (as an attacker would) قبل بنائه، وتصميمه بحيث تبقى الإخفاقات صغيرة (failures stay small)، وترتيب المخاطر (ranking risk) بحيث يذهب الجهد إلى حيث يكون الضرر أرجح (harm is likeliest).

---

# 1.1 — نمذجة التهديدات: تدفقات البيانات وحدود الثقة وSTRIDE (Threat modelling: data flows, trust boundaries and STRIDE)
*المستوى (Level): 🟢 مبتدئ (Beginner)* · *المتطلبات (Prerequisites): 0.1، 0.2* · *المرحلة (Phase): Plan, Design*

## ⚡ الدرس في دقيقة (In 60 seconds)
- **نمذجة التهديدات (Threat modelling)** تفكيرٌ منظَّم (structured thinking) فيما قد يسوء في نظامٍ ما *قبل بنائه أو تغييره (before it is built or changed)*، كي تدخل الإصلاحات (fixes) في التصميم (design) لا في تقرير حادثة (incident report).
- تجيب عن أربعة أسئلة (four questions): *ماذا نعمل عليه؟ ما الذي قد يسوء؟ ماذا سنفعل حيال ذلك؟ هل أحسنّا العمل؟* ⁦(What are we working on? What can go wrong? What are we going to do about it? Did we do a good job?)⁩ وفق إطار آدم شوستاك (Adam Shostack's framework).
- ابدأ **بمخطط تدفق البيانات (data flow diagram, DFD)**: من يتحدث إلى من (who talks to whom)، وأين تستقر البيانات (where data rests)، وأين تقع **حدود الثقة (trust boundaries)**. تعيش معظم التهديدات الخطيرة (serious threats) حيث تعبر البيانات حدًّا (where data crosses a boundary).
- استخدم **STRIDE**، أي انتحال الهوية (Spoofing) والعبث (Tampering) والإنكار (Repudiation) والإفصاح عن المعلومات (Information disclosure) وحجب الخدمة (Denial of service) ورفع الصلاحيات (Elevation of privilege)، قائمةَ تحقق (checklist) عند كل عنصر (element) وكل عبور (crossing).
- مؤشر القرار (Decision cue): طبّق نمذجة التهديدات (threat-model) على أي تغيير يضيف عبورًا لحدٍّ (boundary crossing)، أو مخزن بيانات (data store)، أو طرفًا ثالثًا (third party)، أو نوعًا جديدًا من المستخدمين (new kind of user)، أو نموذجًا (model) أو أداةً لوكيل (agent tool).
- أكبر فخ (Biggest trap): تهديداتٌ عامة (generic threats) مثل «المخترقين» ("hackers") و«حجب الخدمة الموزّع» ("DDoS") بلا مخطط (diagram) ولا مالك (owner) ولا اختبار (test). كل تهديدٍ مهم يحتاج إلى إجراء تخفيف (mitigation) ومالكٍ وفحص (check).

## 🧭 لماذا يهم (Why it matters)
يوشك فريق طارق أن يمنح نجم أسيست (Najm Assist) أول أداةٍ حقيقية (first real tool) له: **تجميد البطاقة (freeze a card)**. حتى الآن كان المساعد (assistant) يجيب فقط عن الأسئلة من جدول الرسوم (fee schedule). وبدءًا من السباق التالي (next sprint)، يستطيع العميل أن يكتب «فقدتُ بطاقتي، جمّدها» ("I lost my card, freeze it") فيستدعي المساعد خدمة البطاقات (card service). تطلب نورة من علي، وقد مضت على التحاقه بالعمل ثلاثة أسابيع، أن ينمذج تهديداتها (threat-model it) قبل مراجعة التصميم (design review) يوم الخميس.

كانت مسودة علي الأولى (first draft) قائمة: «قد يهاجم المخترقون (hackers) واجهة البرمجة (API). حجب الخدمة الموزّع (DDoS). قد يهلوس الذكاء الاصطناعي (hallucinate). تسرّب البيانات (data leak).» كل بندٍ صحيحٌ على كل نظام (true of every system)، ولا يخبر أيٌّ منها طارق بما ينبغي أن يبنيه على نحوٍ مختلف (build differently). تعيدها نورة إليه (Noura hands it back): «ارسم كيف تنتقل الرسالة (how a message travels) من إبهام العميل (customer's thumb) إلى النظام المصرفي الأساسي (core banking) ثم تعود. ضع علامةً على كل نقطةٍ نفقد عندها القدرة على الوثوق بما يصل (trust what arrives). ثم مُرّ على STRIDE عند كل واحدةٍ منها (go through STRIDE at each one).»

تكشف المسودة الثانية مشكلاتٍ حقيقية (real problems). فهوية العميل (customer's identity) لا تصل إلى خدمة البطاقات إلا حقلًا (field) يكتبه النموذج اللغوي (language model) في استدعاء الأداة (tool call). ولا شيء يسجّل أن المساعد، لا نقرة العميل نفسه (customer's own tap)، هو من جمّد البطاقة. ورسالةٌ تقول «وجمّد أيضًا بطاقة أخي، المنتهية بـ 4411» ("also freeze my brother's card, the one ending 4411") ليست إلا نصًّا (just text)، وقد يتصرف النموذج بناءً عليها. إصلاح كل ذلك على السبّورة (whiteboard) أرخص من إصلاحه بعد الإطلاق (after launch)، ولهذا أدرجت قائمة OWASP Top 10 *التصميم غير الآمن (Insecure Design)* فئةً مستقلة (category of its own) منذ إصدارها لعام 2021، ولهذا يطلب إطار تطوير البرمجيات الآمنة (Secure Software Development Framework) الصادر عن NIST، أي SP 800-218، من الفرق استخدام نمذجة المخاطر (risk modelling)، مثل نمذجة التهديدات (threat modelling)، في أثناء التصميم (during design).

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**الأسئلة الأربعة (The four questions).** صاغ آدم شوستاك (Adam Shostack) العمل في أربعة أسئلة (four questions)، عرضها أول مرة (first set out) بكلماتٍ مختلفة قليلًا (in slightly different words) في كتابه *Threat Modeling: Designing for Security* عام 2014، ويبني عليها بيان نمذجة التهديدات (Threat Modeling Manifesto) لعام 2020. وهي بصيغتها الحالية (current form):

1. **ماذا نعمل عليه؟ ⁦(What are we working on?)⁩** نموذجٌ للنظام (model of the system)، وعادةً ما يكون مخططًا (diagram).
2. **ما الذي قد يسوء؟ ⁦(What can go wrong?)⁩** التهديدات (threats)، تُكتشف بصورةٍ منهجية (found systematically)، مثلًا باستخدام STRIDE.
3. **ماذا سنفعل حيال ذلك؟ ⁦(What are we going to do about it?)⁩** لكل تهديد: التخفيف (mitigate) أو الإزالة (eliminate) أو النقل (transfer) أو القبول (accept).
4. **هل أحسنّا العمل؟ ⁦(Did we do a good job?)⁩** راجِع النموذج (check the model)، وتحقّق من أن إجراءات التخفيف (mitigations) قد بُنيت وأنها تعمل (were built and work).

تكفي سبّورةٌ (whiteboard) والأشخاص الذين يعرفون النظام (the people who know the system) وساعةٌ واحدة (an hour) لجولةٍ أولى (first pass).

**مخططات تدفق البيانات (Data flow diagrams).** يبيّن **مخطط تدفق البيانات (data flow diagram, DFD)** كيف تتحرك البيانات عبر النظام (how data moves through a system)، باستخدام خمسة أنواعٍ من العناصر (five kinds of element):

| العنصر (Element) | ما يمثّله (What it represents) | مثال من نجم أسيست (Najm Assist example) |
|---|---|---|
| **كيان خارجي (External entity)** | شخصٌ أو نظامٌ خارج سيطرتك (outside your control) | العميل (customer)؛ مزوّد النموذج اللغوي الكبير المستضاف (hosted LLM provider) |
| **عملية (Process)** | شيفرةٌ تحوّل البيانات أو تعمل عليها (transforms or acts on data) | منسّق أسيست (Assist orchestrator)؛ خدمة أدوات البطاقات (card tools service) |
| **مخزن بيانات (Data store)** | حيث تستقر البيانات (where data rests) | قاعدة بيانات النظام المصرفي الأساسي (core banking database)؛ سجل التدقيق (audit log) |
| **تدفق بيانات (Data flow)** | بياناتٌ تتحرك بين العناصر (data moving between elements) | «رسالة محادثة» ("Chat message")؛ «استدعاء أداة: تجميد البطاقة» ("tool call: freeze card") |
| **حدّ الثقة (Trust boundary)** | خطٌّ يتغير عنده مستوى الثقة (level of trust changes) | من الإنترنت إلى شبكة البنك (Internet to bank network)؛ من البنك إلى مزوّد النموذج اللغوي (bank to LLM vendor) |

**حدّ الثقة (trust boundary)** هو أي موضعٍ تنتقل فيه البيانات بين أجزاءٍ تعمل بصلاحياتٍ مختلفة (different privileges)، أو تنتمي إلى أطرافٍ مختلفة (different parties)، أو تقوم على افتراضاتٍ مختلفة (different assumptions). هاتف العميل ليس ملكًا للبنك (the customer's phone is not the bank's)، ولا خوادم مزوّد النموذج اللغوي (LLM vendor's servers) كذلك. والأهم في ميزات الذكاء الاصطناعي (AI features): **مخرجات النموذج ليست جديرةً بالثقة (the model's output is not trustworthy)** رغم أن النموذج يعمل لصالحك (even though the model works for you)، لأن نصًّا لا تتحكم فيه (text you do not control) يشكّلها، كما في الدرس 8.2.

القاعدة المترتبة على ذلك (The rule that follows): **كل تدفقٍ يعبر حدّ ثقةٍ يُفحَص في الجهة المستقبِلة (every flow that crosses a trust boundary is checked on the receiving side).** من أرسله (who sent it)؟ تلك هي المصادقة (authentication). هل يُسمح له بذلك (may they do this)؟ ذلك هو التفويض (authorisation). هل هو سليم البنية وضمن الحدود (well formed and within limits)؟ ذلك هو التحقق (validation). هل ما نعيده آمن (is what we send back safe)؟ تلك هي معالجة المخرجات (output handling).

**STRIDE.** ابتكر لورين كونفيلدر (Loren Kohnfelder) وبراريت غارغ (Praerit Garg) نموذج STRIDE في مايكروسوفت (Microsoft) عام 1999. كل حرفٍ فيه نوعٌ من التهديد (type of threat) يكسر خاصيةً أمنية واحدة (one security property):

| التهديد (Threat) | الخاصية المكسورة (Property broken) | مثال من نجم أسيست (Najm Assist example) | إجراء التخفيف المعتاد (Typical mitigation) |
|---|---|---|---|
| انتحال الهوية (**S**poofing) | المصادقة (Authentication) | يحمل استدعاء الأداة (tool call) معرّف عميل (customer ID) كتبه النموذج | الهوية (identity) من الجلسة الموثَّقة (verified session)، لا من النموذج أبدًا (never from the model) |
| العبث (**T**ampering) | السلامة (Integrity) | يُعدَّل معرّف البطاقة (card ID) بين التطبيق والبوابة (gateway) | TLS؛ التحقق من جهة الخادم (server-side validation) |
| الإنكار (**R**epudiation) | عدم الإنكار (Non-repudiation) | «لم أجمّد تلك البطاقة قط» ("I never froze that card")، والسجلات (logs) لا تستطيع إثبات أن ذلك تمّ عبر أسيست (came through Assist) | سجل تدقيق يكشف العبث (tamper-evident audit log): من، وماذا، ومتى، وعبر أي قناة (which channel) |
| الإفصاح عن المعلومات (**I**nformation disclosure) | السرية (Confidentiality) | تصل بطاقات عميلٍ آخر (another customer's cards) إلى سياق النموذج (model's context) فيكررها (are repeated) | اجلب بيانات العميل المسجِّل دخوله (signed-in customer) فقط؛ وأرسل إلى النموذج الحد الأدنى (the minimum) |
| حجب الخدمة (**D**enial of service) | التوافر (Availability) | رسائل طويلة جدًا (very long messages) ترفع تكاليف النموذج (model costs) وتبطئ الخدمة (slow the service) | حدود الحجم (size limits)؛ حدود المعدل (rate limits)؛ ميزانيات رموز لكل عميل (per-customer token budgets) |
| رفع الصلاحيات (**E**levation of privilege) | التفويض (Authorisation) | يُستدرَج أسيست (talked into) إلى *إلغاء تجميد (unfreezing)* بطاقة، وهو ما لم يُصمَّم لفعله قط (never meant to do) | قائمة سماحٍ للأدوات (tool allow-list): التجميد فقط؛ وإلغاء التجميد (unfreeze) يتطلب إعادة المصادقة (re-authentication) في التطبيق |

STRIDE أداةُ تذكير (a prompt)، لا نظريةٌ كاملة للهجمات (complete theory of attacks). وقيمته أنه يمنعك من نسيان فئاتٍ كاملة (whole categories): يفكر المبتدئون (newcomers) في التسريبات (leaks) والانقطاعات (outages)، وكثيرًا ما ينسون الإنكار (repudiation).

**المُخرَج (The output)** وثيقةٌ قصيرة (short document): المخطط (diagram)؛ وقائمة التهديدات (threat list) بحقول المعرّف (ID)، والعنصر أو التدفق (element or flow)، وفئة STRIDE، وإجراء التخفيف (mitigation)، والمالك (owner)، والحالة (status)؛ وافتراضاتك (assumptions)؛ وقراراتك (decisions). يعرض قسم 🏛️ قالب بنك نجم (Najm's template).

### 🟡 التعمق أكثر (Going deeper)

**STRIDE لكل عنصر (STRIDE per element).** لا ينطبق كل تهديدٍ على كل عنصر (not every threat applies to every element). وتربط إرشادات دورة حياة التطوير الآمن (Security Development Lifecycle) من مايكروسوفت، التي شاعت عبر كتاب شوستاك (Shostack's book)، بينها على هذا النحو (maps them):
- **الكيانات الخارجية (External entities):** انتحال الهوية (spoofing) والإنكار (repudiation).
- **العمليات (Processes):** الستة جميعًا (all six).
- **تدفقات البيانات (Data flows):** العبث (tampering) والإفصاح عن المعلومات (information disclosure) وحجب الخدمة (denial of service).
- **مخازن البيانات (Data stores):** العبث (tampering) والإفصاح عن المعلومات (information disclosure) وحجب الخدمة (denial of service)، إضافةً إلى الإنكار (repudiation) إذا كان المخزن يحتفظ بالسجلات (holds logs).

امشِ على المخطط عنصرًا عنصرًا (element by element) واطرح الأسئلة ذات الصلة فقط (only the relevant questions). عندئذٍ يصبح كل سؤالٍ متجاوَز (skipped question) إما قرارًا مسجّلًا (recorded decision)، مثل «لا ينطبق، لأن…» ⁦("not applicable, because…")⁩، وإما فجوةً ظاهرة (visible gap).

**مخطط أداة تجميد البطاقة (The diagram for the freeze-card tool).** كل صندوقٍ منطقةُ ثقة (trust zone). وكل سهمٍ يعبر حافة منطقةٍ (zone's edge) يخضع لمراجعة STRIDE (STRIDE pass).

```mermaid
flowchart RL
    subgraph U["غير موثوق: جهاز العميل والإنترنت (Untrusted: customer device and internet)"]
        C["العميل<br/>(Customer)"]
        APP["تطبيق نجم للهاتف<br/>(Najm Mobile app)"]
    end
    subgraph B["شبكة البنك (Bank network)"]
        GW["بوابة واجهات البرمجة<br/>(API gateway)"]
        ORC["منسّق أسيست<br/>(Assist orchestrator)"]
        TOOLS["خدمة أدوات البطاقات<br/>(Card tools service)"]
        CORE["قاعدة بيانات النظام المصرفي الأساسي<br/>(Core banking database)"]
        LOG["سجل التدقيق<br/>(Audit log)"]
    end
    subgraph V["مزوّد النموذج اللغوي (LLM provider)"]
        LLM["النموذج اللغوي المستضاف<br/>(Hosted language model)"]
    end
    C -->|"يكتب رسالة (types message)"| APP
    APP -->|"اتصال مشفّر مع رمز الجلسة (HTTPS with session token)"| GW
    GW -->|"الرسالة ومعرّف العميل (message and customer ID)"| ORC
    ORC -->|"الموجّه والسياق (prompt and context)"| LLM
    LLM -->|"الرد واستدعاء الأداة (reply and tool call)"| ORC
    ORC -->|"طلب تجميد البطاقة (freeze card request)"| TOOLS
    TOOLS --> CORE
    TOOLS --> LOG
```

تبرز ثلاثة عبورات (Three crossings stand out). **من التطبيق إلى البوابة (App to gateway)** حدٌّ تقليدي للويب وواجهات البرمجة (classic web and API boundary)، تتناوله الوحدات 2 إلى 4. **من البنك إلى المزوّد (Bank to vendor)** يثير أسئلة حماية البيانات (data-protection questions) التي تملكها سارة، مسؤولة حماية البيانات (DPO): أي بيانات العملاء تغادر البنك، وما الذي يحق للمزوّد الاحتفاظ به؟ **من النموذج إلى المنسّق (Model to orchestrator)** هو العبور الجديد: يحمل «الرد واستدعاء الأداة» ("reply and tool call") تعليماتٍ (instructions) من نموذجٍ قرأ نصًّا غير موثوق (untrusted text).

**حدود الثقة في الشيفرة (Trust boundaries in code).** أكثر أخطاء التصميم شيوعًا (most common design bug) في أدوات الوكلاء (agent tools) هو الوثوق بقيمٍ عبرت حدّ النموذج (crossed the model boundary):

```python
# VULNERABLE: identity and authority both come from the model's tool call
def freeze_card_tool(args: dict, session) -> str:
    card = cards.get(args["card_id"])
    if card.customer_id == args["customer_id"]:   # the model chose both the card and the customer
        cards.freeze(card.id)
        return "Card frozen"
    return "Not allowed"
```

```python
# FIXED: identity comes from the verified session; the model only names a card
def freeze_card_tool(args: dict, session) -> str:
    customer_id = session.customer_id                  # from the login token, not the model
    card = cards.get_for_customer(customer_id, args["card_id"])
    if card is None:
        return "I can't find that card on your account."
    if not session.has_confirmed("freeze", card.id):   # customer taps Confirm in the app
        return "Please confirm the freeze in the app."
    cards.freeze(card.id)
    audit.log(event="card.freeze", customer=customer_id, card=card.id, channel="assist")
    return "Card frozen."
```

يعالج الإصلاح ثلاثة صفوفٍ من STRIDE دفعةً واحدة (three STRIDE rows at once): انتحال الهوية (spoofing)، إذ تأتي الهوية من الجلسة (identity from the session)؛ ورفع الصلاحيات (elevation of privilege)، إذ يقتصر الأمر على بطاقات العميل نفسه وبعد التأكيد فقط (own cards only, after confirmation)؛ والإنكار (repudiation)، عبر سجل تدقيقٍ يسمّي القناة (an audit record that names the channel).

**طرقٌ أخرى لاكتشاف التهديدات (Other ways to find threats).**
- **أشجار الهجوم (Attack trees)**، التي قدّمها بروس شناير (Bruce Schneier) عام 1999، تضع هدف المهاجم (attacker's goal) في الجذر (root)، مثل «تجميد بطاقة عميلٍ آخر» ("freeze another customer's card")، ثم تتفرع إلى الطرق الموصلة إليه (the ways to reach it).
- **حالات إساءة الاستخدام (Abuse cases)** قصص مستخدمين (user stories) من جهة المهاجم (attacker's side): «بصفتي محتالًا، أريد أن يقرأ لي أسيست رصيد شخصٍ آخر» ("As a fraudster, I want Assist to read me someone else's balance"). وتدخل مباشرةً في قائمة الأعمال المتراكمة (backlog).
- **LINDDUN**، من جامعة KU Leuven، يفعل للخصوصية (privacy) ما يفعله STRIDE للأمن (security)، بتهديداتٍ مثل *ربط* السجلات (*linking* records) و*تحديد هوية* الأشخاص (*identifying* people). ستطلبه سارة في الميزات المتعلقة بالبيانات الشخصية (personal-data features).
- **مكتبات التهديدات (Threat libraries)** مثل MITRE ATT&CK، ولأنظمة الذكاء الاصطناعي (AI systems) MITRE ATLAS، تتيح لك مطابقة إجاباتك مع ما فعله المهاجمون فعلًا (what attackers have actually done)، كما في الوحدة 8.

### 🔴 نظرة الخبير (Expert view)

**انمذج تهديدات التغيير، لا الكون (Threat-model the change, not the universe).** نموذجٌ لـ«البنك بأكمله» ("the whole bank") لا يكتمل أبدًا ولا يقرؤه أحد. انمذج كل ميزةٍ أو تغيير (each feature or change) في جلسةٍ قصيرة وقت التصميم (short design-time session)، واحتفظ بمخططٍ واحد للنظام (one system diagram) يحدّثه نموذج كل ميزة. محفّزات نورة (Noura's triggers): حدّ ثقةٍ جديد (new trust boundary)، أو مخزنٌ لبياناتٍ شخصية أو مالية (store of personal or financial data)، أو طرفٌ ثالث (third party)، أو صلاحيةٌ (privilege) أو نوعُ مستخدمٍ جديد (kind of user)، أو نموذجٌ أو أداةٌ أو مصدرُ استرجاعٍ جديد (new model, tool or retrieval source).

**أبقِ النموذج مع الشيفرة (Keep the model with the code).** خزّن المخطط وجدول التهديدات (threat table) في المستودع (repository)، وراجع التغييرات في طلب السحب نفسه (same pull request) الذي يضم الشيفرة، واربط كل إجراء تخفيفٍ بتذكرته (ticket) واختباره (test). وتناسب أدوات نمذجة التهديدات كشيفرة (threat-modelling-as-code tools)، مثل OWASP pytm وThreagile، الفرقَ التي تراجع كل شيءٍ كشيفرة (review everything as code).

**السؤال الرابع هو الذي تتجاوزه الفرق (Question four is the one teams skip).** هل كان النموذج صحيحًا (Was the model right): هل راجعه من يبنون النظام ويشغّلونه؟ هل بُنيت إجراءات التخفيف (Were the mitigations built)؟ هل تعمل (Do they work)؟ يصبح كل تهديدٍ عالي المخاطر (high-risk threat) **حالةَ اختبارٍ أمني (security test case)**: «يُرفض استدعاء الأداة الذي يسمّي بطاقة عميلٍ آخر» ("a tool call naming another customer's card is refused") ويُشغَّل مع كل بناء (every build).

**الذكاء الاصطناعي يغيّر المخطط (AI changes the diagram).** ارسم **النموذج منطقةَ ثقةٍ مستقلة (model as its own trust zone)**. وارسم **كل مصدرٍ للنص (every source of text)** يقرؤه، لا المستخدم وحده (not only the user): في مساعد مذكرات الائتمان (Credit Memo Copilot)، قد يحمل كل مستندٍ مسترجَع (retrieved document) تعليماتٍ مخفية (hidden instructions)، وهذا حقن الموجّهات غير المباشر (indirect prompt injection) الذي يتناوله الدرسان 8.2 و9.3. ولكل أداة، اسأل: *ما أسوأ ما يمكن أن تفعله هذه الأداة إذا تحكّم المهاجم بالنموذج تحكمًا كاملًا؟* ⁦(what is the worst this tool can do if an attacker fully controls the model?)⁩ فإن كانت الإجابة غير مقبولة، فأصلح صلاحيات الأداة (tool's permissions) وأضف موافقةً بشرية (human approval)؛ ولا تعتمد على الموجّه (do not rely on the prompt)، كما في الدرس 9.2.

**الناس قبل المنهج (People over method).** أحضِر المهندس الذي كتب الشيفرة، وشخصًا يشغّلها (someone who runs it)، وشخصًا من فريق المنتج (product person)، وآخر من الأمن (security). وتسهّل ألعاب البطاقات (card games)، مثل Elevation of Privilege التي ألّفها آدم شوستاك وأصدرتها مايكروسوفت، وOWASP Cornucopia، الجلساتِ الأولى (first sessions).

## 🧰 الأدوات (The toolkit)
| الضابط أو المعيار أو الأداة (Control, standard or tool) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |
|---|---|---|
| **Four-question framework** — إطار الأسئلة الأربعة، لشوستاك (Shostack) | ماذا نعمل عليه، وما الذي قد يسوء، وماذا سنفعل حياله، وهل أحسنّا العمل (What are we working on, what can go wrong, what will we do about it, did we do a good job) | تنظيم أي جلسةٍ لنمذجة التهديدات (threat-modelling session)، من 30 دقيقة إلى مراجعةٍ كاملة (full review) |
| **Data flow diagram** — مخطط تدفق البيانات | الكيانات والعمليات والمخازن والتدفقات وحدود الثقة (entities, processes, stores, flows and trust boundaries) في صفحةٍ واحدة (on one page) | الخطوة الأولى في كل نموذج تهديدات (threat model)؛ ويُحدَّث عند تغيّر النظام (when the system changes) |
| **STRIDE** — لكونفيلدر وغارغ (Kohnfelder and Garg) في مايكروسوفت (Microsoft) | ستة أنواعٍ من التهديدات (six threat types)، كلٌّ منها مرتبطٌ بالخاصية الأمنية التي يكسرها (security property it breaks) | طرح سؤال «ما الذي قد يسوء؟» ⁦("what can go wrong?")⁩ بصورةٍ منهجية عند كل عنصرٍ وعبور (each element and crossing) |
| **Attack trees** — أشجار الهجوم، لشناير (Schneier) | هدف المهاجم مفكَّكًا إلى الطرق الموصلة إليه (an attacker's goal broken down into the ways to reach it) | تحليلٌ معمّق (deep analysis) لهدفٍ واحد عالي القيمة (high-value goal)، مثل تحويل الأموال (moving money) |
| **LINDDUN** — من جامعة KU Leuven | فئات تهديدات الخصوصية (privacy threat categories) مطبَّقةً على تدفقات البيانات (data flows) | الميزات المبنية حول البيانات الشخصية (personal data)، بالتعاون مع مسؤول حماية البيانات (DPO) |
| **OWASP Threat Dragon** — أداة OWASP لرسم التهديدات | أداةٌ مجانية مفتوحة المصدر (free, open-source tool) لرسم مخططات تدفق البيانات (DFDs) وتسجيل التهديدات (recording threats) | مخططٌ مشترك ذو إصدارات (shared, versioned diagram) دون أداةٍ تجارية (commercial tool) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
تصبح مسودة علي الثانية (Ali's second draft) **TM-ASSIST-004: أداة «تجميد البطاقة» في نجم أسيست (Najm Assist "freeze card" tool)**، وتجعل نورة صيغتها معيارًا للفريق (team standard).

**الترويسة (Header).** *النطاق (Scope):* يطلب العميل من أسيست تجميد بطاقة؛ فيستدعي أسيست خدمة أدوات البطاقات (card tools service). *خارج النطاق (Out of scope):* إلغاء التجميد (unfreeze)، الذي يبقى في التطبيق خلف إعادة مصادقةٍ قوية (strong re-authentication). *الافتراضات (Assumptions):* تتحقق البوابة (gateway) من رموز الجلسات (session tokens)؛ ولا يحتفظ مزوّد النموذج اللغوي (LLM vendor) بالموجّهات (prompts) مدةً أطول مما يسمح به العقد (contract)، وعلى سارة التأكيد (Sara to confirm). *المشاركون (Participants):* طارق، وعلي، ونورة، ومالك المنتج (product owner) التابع لرانيا، وجاسم. *المخطط (Diagram):* الإصدار الثالث من مخطط تدفق البيانات (DFD v3) في المستودع (repository).

| المعرّف (ID) | العنصر أو التدفق (Element or flow) | STRIDE | التهديد (Threat) | إجراء التخفيف (Mitigation) | المالك (Owner) | يُتحقَّق منه عبر (Verified by) |
|---|---|---|---|---|---|---|
| T1 | النموذج ← المنسّق (Model → orchestrator) | S, E | يسمّي استدعاء الأداة (tool call) بطاقةً أو عميلًا غير العميل المسجِّل دخوله (signed-in customer) | معرّف العميل (customer ID) من الجلسة (from the session)؛ ويجب أن تعود البطاقة إلى ذلك العميل (card must belong to that customer) | طارق | اختبار (Test): تُرفض بطاقة عميلٍ آخر (another customer's card is refused) |
| T2 | المنسّق ← أدوات البطاقات (Orchestrator → card tools) | E | يُستدرَج النموذج (model is talked into) إلى استدعاء أداةٍ ما كان ينبغي أن تُتاح له (a tool it should not have) | قائمة السماح (allow-list) تضم `freeze_card` والأدوات المخصصة للقراءة فقط (read-only tools) لا غير | طارق | اختبار (Test): لا يمكن الوصول إلى `unfreeze` (unreachable) |
| T3 | أدوات البطاقات ← النظام المصرفي الأساسي (Card tools → core banking) | R | يعترض العميل على التجميد (disputes the freeze)؛ ولا دليل على القناة (no proof of channel) | حدث تدقيق (audit event): العميل، والبطاقة، والقناة، ومعرّف التأكيد (confirmation ID)، والوقت | طارق | عيّنة سجلات (log sample) يراجعها جاسم |
| T4 | المنسّق ← مزوّد النموذج اللغوي (Orchestrator → LLM provider) | I | تصل أرقام البطاقات الكاملة (full card numbers) أو بيانات عملاء آخرين إلى المزوّد (vendor) | أرسل آخر أربعة أرقام (last four digits) وبيانات العميل المسجِّل دخوله (signed-in customer) فقط | سارة، طارق | عيّنة من سجل الموجّهات (prompt log sample) |
| T5 | التطبيق ← البوابة (App → gateway) | D | سيولٌ من الرسائل الطويلة (floods of long messages) تستنزف ميزانية النموذج (model budget) | حدٌّ قدره 2,000 حرف (2,000-character limit)؛ وحدود للمعدل والرموز لكل عميل (per-customer rate and token limits) | طارق | اختبار حمل (load test) في بيئة ما قبل الإنتاج (staging) |
| T6 | النموذج ← المنسّق (Model → orchestrator) | T, E | تعليماتٌ إضافية (extra instructions) في رسالة: «وجمّد البطاقة 4411 أيضًا» ("also freeze card 4411") | شاشة تأكيد (confirmation screen) مبنية من بيانات الخادم (server data) تعرض البطاقة بعينها (exact card) | مالك المنتج (Product owner) | حالةٌ للفريق الأحمر (red-team case) من فريق مريم |

**القرارات المسجّلة (Decisions recorded).** يبقى إلغاء التجميد (unfreeze) خارج أسيست: هذا خطرٌ جرى تجنّبه (avoided) لا تخفيفه (not mitigated). وتقبل رانيا المخاطر المتبقية (residual risk) في T6 إلى حين جولة الفريق الأحمر (red-team round) لدى مريم، مع تاريخ انتهاء (expiry date). ويُعاد فتح النموذج (reopened) كلما أُضيفت أداة (whenever a tool is added).

## 🛠️ التمارين (Exercises)
- 🟢 ارسم مخطط تدفق بيانات (DFD) لتطبيقٍ بنيته بنفسك (an application you built yourself)، أو لتطبيقٍ تدريبي معرَّض للثغرات عمدًا (deliberately vulnerable training app) يعمل على جهازك (running on your own machine)، مثل OWASP Juice Shop. ضمّنه أنواع العناصر الخمسة كلها (all five element types) وحدّد كل حدّ ثقة (trust boundary). *يكتمل عندما (Done when):* يُدرَج كل سهمٍ يعبر حدًّا مع ما تفحصه الجهة المستقبِلة (what the receiving side checks)، أو «لا شيء بعد» ("nothing yet").
- 🟡 تتيح بوابة الشركات الصغيرة (SME Portal) في بنك نجم لمستخدم الشركة (company user) رفع فاتورةٍ بصيغة PDF (invoice PDF). تُخزَّن في مخزن كائنات (object store)، وتُفحَص بحثًا عن الفيروسات (scanned for viruses)، ثم يقرؤها محلّلٌ (parser) يملأ المبالغ (amounts). ارسم مخطط تدفق البيانات (DFD) وطبّق STRIDE لكل عنصر (per element). *يكتمل عندما (Done when):* يكون لديك 12 تهديدًا على الأقل، واحدٌ على الأقل لكل فئةٍ من فئات STRIDE (STRIDE category)، لكلٍّ منها إجراء تخفيف (mitigation) والعنصر الذي يؤثر فيه (the element it affects).
- 🔴 في شيفرتك أو في مختبرٍ محلي (local lab)، ابنِ ميزةً صغيرة تعتمد على نموذجٍ لغوي كبير (LLM feature) بأداةٍ واحدة (with one tool)، أو أعد استخدام واحدة (or reuse one)، مثل مساعد مهام (to-do assistant) يستطيع حذف العناصر (delete items). انمذج تهديدات الحدّ بين النموذج والأداة (model-to-tool boundary)، ثم اكتب اختباراتٍ آلية (automated tests) لأخطر ثلاثة تهديدات وشغّلها. *يكتمل عندما (Done when):* يرسل كل اختبارٍ استدعاء أداةٍ خبيثًا (malicious tool call)، مثل حذف عنصرٍ يخص مستخدمًا آخر، وينجح لأن شيفرتك ترفضه (your code refuses it)، لا لأن النموذج اختار ألّا يجري الاستدعاء (the model chose not to make the call).

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **قائمةٌ بلا مخطط (A list without a diagram).** التهديدات العامة (generic threats) لا تغيّر شيئًا. ارسم التدفقات والحدود (flows and boundaries) أولًا، ثم ابحث عن التهديدات عند كل عبور (each crossing).
- **الوثوق بداخل الشبكة (Trusting the inside of the network).** عبارة «إنه داخلي» ("It's internal") افتراضٌ (assumption)، لا ضابط (control). حدّد الحدود الداخلية (internal boundaries) أيضًا.
- **معاملة النموذج جزءًا من شيفرتك (Treating the model as part of your code).** مخرجات النموذج (model output) تعبر حدّ ثقة (trust boundary). تحقّق منها وفوّضها (validate and authorise) كما تفعل مع طلبٍ قادم من الإنترنت (request from the internet).
- **محاولة غلي المحيط (Boiling the ocean).** نموذجٌ للبنية بأكملها (whole estate) لا ينتهي أبدًا. انمذج كل تغيير (each change)؛ وأبقِ مخططًا واحدًا للنظام محدَّثًا (keep one system diagram current).
- **لا مالك، ولا اختبار، ولا مراجعة لاحقة (No owner, no test, no revisit).** إجراء التخفيف (mitigation) بلا مالكٍ واختبار مجرد أمنية (a wish). أغلق الحلقة (close the loop) بالسؤال الرابع (question four)، وأعد فتح النموذج حين ينطلق محفّز (when a trigger fires).

## 🧾 الخلاصة (Recap)
- تجيب نمذجة التهديدات (threat modelling) عن أربعة أسئلة (four questions): ماذا نعمل عليه، وما الذي قد يسوء، وماذا سنفعل حياله، وهل أحسنّا العمل (what are we working on, what can go wrong, what will we do about it, did we do a good job).
- مخطط تدفق البيانات (data flow diagram) مع حدود الثقة (trust boundaries) هو الأساس (foundation). وكل تدفقٍ يعبر حدًّا يفحصه المستقبِل (checked by the receiver).
- يربط STRIDE ستة أنواعٍ من التهديدات (six threat types) بست خصائص أمنية (six security properties). طبّقه لكل عنصر (per element).
- في ميزات الذكاء الاصطناعي (AI features)، النموذج منطقة ثقةٍ قائمة بذاتها (its own trust zone): مخرجاته مدخلاتٌ غير موثوقة (untrusted input) للأدوات والأنظمة اللاحقة (tools and downstream systems).
- يكتمل نموذج التهديدات (threat model) عندما يكون لكل تهديدٍ مهم إجراء تخفيفٍ ومالكٌ واختبار (a mitigation, an owner and a test)، وحين يعيش مع الشيفرة (lives with the code).

## ✍️ اختبر نفسك (Check yourself)

**1. يسرد أول نموذج تهديدات (threat model) أعدّه علي لأداة تجميد البطاقة (freeze-card tool) «المخترقين» ("hackers") و«حجب الخدمة الموزّع» ("DDoS") و«هلوسة الذكاء الاصطناعي» ("AI hallucination") و«تسرّب البيانات» ("data leak"). ما الخطوة التالية الأكثر فائدة (MOST useful next step)؟**

- A. إضافة تهديداتٍ (add threats) من قائمةٍ عامة (public list) حتى يبلغ عددها 50 على الأقل (at least 50)
- B. رسم مخطط تدفق البيانات مع حدود الثقة (data flow diagram with trust boundaries)، ثم تطبيق STRIDE على كل عنصرٍ وعبور (each element and crossing)
- C. مطالبة مزوّد النموذج اللغوي (LLM vendor) بشهادته الأمنية (security certificate)
- D. منح كل تهديدٍ مدرج درجةً باستخدام CVSS (score with CVSS)

<details><summary>الإجابة</summary>

**B.** من دون مخطط (diagram) تبقى التهديدات عامة (generic). يبيّن مخطط تدفق البيانات (DFD) أين تتغير الثقة (where trust changes)، ويكتشف STRIDE تهديداتٍ محددة (specific threats) هناك. يضيف الخيار A كمًّا (volume) لا فهمًا (insight)؛ ويقيّم D تهديداتٍ أغمض من أن تُقيَّم (too vague to rate). انظر: 🟢 الأساسيات (The essentials)؛ 🧭 لماذا يهم (Why it matters).

</details>

**2. تقول عميلةٌ إنها لم تجمّد بطاقتها قط (never froze her card). ولا يستطيع الفريق معرفة ما إذا جُمّدت عبر نجم أسيست (Najm Assist)، أم زر التطبيق (app's button)، أم موظف مركز الاتصال (call-centre agent). إلى أي فئةٍ من فئات STRIDE (STRIDE category) تنتمي هذه الفجوة (gap)؟**

- A. انتحال الهوية (Spoofing)
- B. العبث (Tampering)
- C. الإنكار (Repudiation)
- D. حجب الخدمة (Denial of service)

<details><summary>الإجابة</summary>

**C.** الإنكار (Repudiation) يعني أن شخصًا يستطيع إنكار فعلٍ (deny an action) ولا تستطيع أنت إثبات العكس (prove otherwise). وإجراء التخفيف (mitigation) هو سجل تدقيق (audit record) يبيّن من فعل ماذا، ومتى، وعبر أي قناة (through which channel). أما الخيار A، انتحال الهوية (Spoofing)، فيعني أن شخصًا يتظاهر بأنه هي (pretending to be her). انظر: 🟢 الأساسيات (The essentials).

</details>

**3. يتضمن استدعاء الأداة الذي يصدره النموذج (model's tool call) كلًّا من `card_id` و`customer_id`، وتتحقق الأداة من أن البطاقة تعود (the card belongs) إلى ذلك `customer_id`. لماذا تبقى هذه مشكلة (still a problem)؟**

- A. ينبغي أن يستخدم الفحص (the check should use) تاريخ انتهاء صلاحية البطاقة (card's expiry date) بدلًا من ذلك (instead)
- B. لا مشكلة، لأن النموذج أُعطي معرّف العميل الصحيح (correct customer ID) في موجّهه (prompt)
- C. ينبغي أن تتخطى الأداة فحص الملكية (ownership check) لتبقى سريعة (to stay fast)
- D. عبرت القيمتان كلتاهما حدّ الثقة الخاص بالنموذج (model's trust boundary)، لذا لا يثبت الفحص إلا أن قيمتين اختارهما النموذج متطابقتان (two model-chosen values agree)؛ ويجب أن يأتي معرّف العميل (customer ID) من الجلسة الموثَّقة (verified session)

<details><summary>الإجابة</summary>

**D.** يشكّل النص غير الموثوق (untrusted text) مخرجات النموذج (model output)، لذا يستطيع نموذجٌ موجَّه (steered model) أن يسمّي بطاقة عميلٍ آخر مع معرّف ذلك العميل، فينجح الفحص. يجب أن تأتي الهوية (identity) من الجلسة (session)؛ والنموذج يسمّي البطاقة فقط (only names a card). ويفترض الخيار B أن النموذج يكرر دائمًا ما قيل له (always repeats what it was told). انظر: 🟡 التعمق أكثر (Going deeper).

</details>

**4. باستخدام STRIDE لكل عنصر (STRIDE per element)، ما أنواع التهديدات التي تُراعى عادةً لتدفق بيانات (data flow)، مثل السهم من منسّق أسيست (Assist orchestrator) إلى مزوّد النموذج اللغوي (LLM provider)؟**

- A. انتحال الهوية والإنكار (Spoofing and repudiation)
- B. العبث والإفصاح عن المعلومات وحجب الخدمة (Tampering, information disclosure and denial of service)
- C. الستة جميعًا (All six)
- D. رفع الصلاحيات فقط (Elevation of privilege only)

<details><summary>الإجابة</summary>

**B.** يمكن تعديل تدفق البيانات (data flow) أو قراءته أو حجبه (altered, read or blocked). وينطبق انتحال الهوية والإنكار (Spoofing and repudiation) على الكيانات الخارجية والعمليات (external entities and processes)؛ أما الستة جميعًا (C) فتنطبق على العمليات (processes). انظر: 🟡 التعمق أكثر (Going deeper).

</details>

**5. بعد ثلاثة أشهرٍ من الإطلاق، تسأل نورة عن نموذج تهديدات تجميد البطاقة (freeze-card threat model): «هل أحسنّا العمل؟» ⁦("Did we do a good job?")⁩ ماذا تتضمن الإجابة القوية (strong answer)؟**

- A. دليلًا (evidence) على أن كل إجراء تخفيفٍ عالي المخاطر (high-risk mitigation) قد بُني ويُفحَص باختبارٍ أو بحالةٍ للفريق الأحمر (test or red-team case)، وعلى أن النموذج يعكس التغييرات منذ الإطلاق (reflects changes since launch)
- B. بيانًا من المزوّد (statement from the vendor) بأن نموذجه آمن (its model is safe)
- C. عدد التهديدات المكتشفة في الجلسة الأصلية (original session)
- D. تأكيدًا (confirmation) على أن الوثيقة قد اعتُمدت (document was approved)

<details><summary>الإجابة</summary>

**A.** يسأل السؤال الرابع (question four) عمّا إذا كان النموذج صحيحًا، وعمّا إذا كانت إجراءات التخفيف (mitigations) موجودةً وتعمل (exist and work). أما عدّ التهديدات (C) أو الموافقات (D) فيقيس النشاط (activity) لا الحماية (protection). انظر: 🔴 نظرة الخبير (Expert view).

</details>

## 📚 المراجع (References)
- شوستاك ⁦(Shostack, A.)⁩ عام 2014، كتاب *Threat Modeling: Designing for Security*، دار Wiley
- بيان نمذجة التهديدات (Threat Modeling Manifesto)، 2020 — https://www.threatmodelingmanifesto.org
- ورقة OWASP المختصرة لنمذجة التهديدات (OWASP Threat Modeling Cheat Sheet) — https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html
- أداة OWASP Threat Dragon — https://owasp.org/www-project-threat-dragon/
- قائمة OWASP Top 10، فئة التصميم غير الآمن (Insecure Design) — https://owasp.org/Top10/
- وثيقة NIST SP 800-218، إطار تطوير البرمجيات الآمنة (Secure Software Development Framework, SSDF)، الإصدار 1.1؛ وكانت مراجعةٌ للإصدار 1.2 قيد المسودة (in draft) وقت الكتابة عام 2026، فتحقّق من الإصدار الحالي (check the current version) — https://csrc.nist.gov/pubs/sp/800/218/final
- شناير ⁦(Schneier, B.)⁩ عام 1999، مقالة «أشجار الهجوم» ("Attack Trees")، مجلة *Dr. Dobb's Journal*، ديسمبر 1999
- منهجية LINDDUN لنمذجة تهديدات الخصوصية (privacy threat modelling) — https://linddun.org
- إطار MITRE ATLAS — https://atlas.mitre.org

---

# 1.2 — المبادئ الأمنية: أقل الصلاحيات، والدفاع المتعدد الطبقات، والإعدادات الافتراضية الآمنة، وانعدام الثقة (Security principles: least privilege, defence in depth, secure defaults, zero trust)
*المستوى (Level): 🟢 مبتدئ (Beginner)* · *المتطلبات (Prerequisites): 1.1* · *المرحلة (Phase): Design, Build*

## ⚡ الدرس في دقيقة (In 60 seconds)
- المبادئ الأمنية (Security principles) قواعد تصميم (design rules) تظل فاعلةً حين لا تستطيع التنبؤ بالهجوم المحدد (specific attack). يعود معظمها إلى ورقةٍ نشرها سالتزر وشرودر (Saltzer and Schroeder) عام 1975، وما زالت هذه المبادئ تحدد ما إذا كان خطأٌ برمجي واحد (one bug) سيتحول إلى اختراق (breach).
- **أقل الصلاحيات (Least privilege):** كل شخصٍ وخدمةٍ ورمزٍ مميز (token) ووكيل ذكاءٍ اصطناعي (AI agent) يحصل فقط على الوصول الذي يحتاجه (only the access it needs)، وللمدة التي يحتاجها فقط (only as long as it needs it).
- **الدفاع المتعدد الطبقات (Defence in depth):** عدة طبقاتٍ مستقلة (several independent layers)، بحيث لا يكفي إخفاقٌ واحد (one failure is not enough). **الإعدادات الافتراضية الآمنة (Secure defaults):** ارفض ما لم يُسمح به صراحةً (deny unless explicitly allowed)، وأخفِق بالإغلاق (fail closed) حين ينكسر فحصٌ ما (when a check breaks).
- **انعدام الثقة (Zero trust):** لا يُوثَق بأي طلبٍ بسبب مصدره في الشبكة (where it comes from on the network)؛ فكل طلبٍ تتم مصادقته وتفويضه (authenticated and authorised)، وفق NIST SP 800-207.
- مؤشر القرار (Decision cue): اسأل «إذا اختُرق هذا المكوّن أو أخفق هذا الفحص، فإلى أي مدى يمكن أن ينتشر الضرر، وما الذي يوقفه؟» ⁦("if this component is compromised or this check fails, how far can the damage spread, and what stops it?")⁩
- أكبر فخ (Biggest trap): منح خدمةٍ جديدة أو وكيل ذكاءٍ اصطناعي (AI agent) وصولًا واسعًا (broad access) «مؤقتًا» ("for now"). نادرًا ما يُسترَد وصول الراحة (convenience access)، ويمكن توجيه وكيلٍ يملك وصولًا واسعًا بالنص (steered by text) إلى إساءة استخدامه (misusing it).

## 🧭 لماذا يهم (Why it matters)
في يوليو 2019، أعلن بنك Capital One أن جهةً خارجية (outsider) حصلت على بياناتٍ تتعلق بنحو 100 مليون شخص في الولايات المتحدة ونحو 6 ملايين في كندا. وتصف الروايات العامة (public accounts)، ومنها بيانات البنك (bank's statements) والقضية الجنائية اللاحقة (later criminal case)، سلسلةً من الخطوات (a chain). فقد أمكن دفع جدار حماية تطبيقات ويب (web application firewall) سيئ الإعداد (misconfigured) إلى إرسال طلباتٍ نيابةً عن المهاجم (on the attacker's behalf)، وهذا تزوير الطلبات من جهة الخادم (server-side request forgery)، انظر 2.3. ووصل أحد الطلبات إلى **خدمة البيانات الوصفية للمثيل (instance metadata service)** لدى مزوّد السحابة (cloud provider)، فسلّمت بيانات اعتمادٍ مؤقتة (temporary credentials) للدور (role) الخاص بجدار الحماية. وكان ذلك الدور قادرًا على سرد وقراءة كثيرٍ من حاويات التخزين (storage buckets) التي لا حاجة لجدار حمايةٍ إلى قراءتها. وعلم البنك بالاختراق من بلاغٍ خارجي (outside tip).

لم يتسبب في ذلك عيبٌ غريب واحد (single exotic flaw). فقد كان الدور أوسع من مهمته (broader than its job)، وهذا يخص **أقل الصلاحيات (least privilege)**. وكانت خدمة البيانات الوصفية (metadata service) في ذلك الوقت تجيب عن الطلبات البسيطة دون إثباتٍ إضافي (without extra proof)، وهذا يخص **الإعدادات الافتراضية الآمنة (secure defaults)**؛ وقد قدّمت AWS إصدارًا يعتمد على رمز الجلسة (session-token version)، هو IMDSv2، في وقتٍ لاحق من عام 2019. وأدى مكوّنٌ واحد مخترَق (one compromised component) مباشرةً إلى بياناتٍ بالجملة (bulk data)، وهذا يخص **الدفاع المتعدد الطبقات (defence in depth)**. غيِّر أيًّا منها، وتصبح النتيجة أصغر (the outcome is smaller).

والآن إلى بنك نجم. يقترح طارق أن يعيد حساب الخدمة (service account) الخاص بنجم أسيست (Najm Assist) استخدام نطاق واجهة البرمجة (API scope) الخاص بالواجهة الخلفية للتطبيق المحمول (mobile backend) «حتى لا نضطر إلى إعادة التوصيل لكل أداةٍ جديدة» ("so we don't have to re-plumb it for every new tool"). إنه أسرع (quicker)، لكنه سيمنح نموذجًا يستطيع العملاء توجيهه بالنص (customers can steer with text) القدرةَ على قراءة حسابات أي عميل وبدء التحويلات (start transfers). ردّ نورة (Noura's reply): «أخبرني بما يجب أن يستطيع أسيست فعله. سيحصل على ذلك بالضبط، ولا شيء غيره.» ⁦(Tell me what Assist must be able to do. It gets exactly that, and nothing else.)⁩

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

في عام 1975، نشر جيروم سالتزر (Jerome Saltzer) ومايكل شرودر (Michael Schroeder) ورقة «حماية المعلومات في أنظمة الحاسوب» ("The Protection of Information in Computer Systems"). وما زالت مبادئ التصميم الثمانية (eight design principles) فيها، وهي الاقتصاد في الآلية (economy of mechanism)، والإعدادات الافتراضية الآمنة من الإخفاق (fail-safe defaults)، والوساطة الكاملة (complete mediation)، والتصميم المفتوح (open design)، وفصل الصلاحيات (separation of privilege)، وأقل الصلاحيات (least privilege)، وأقل آليةٍ مشتركة (least common mechanism)، والقبول النفسي (psychological acceptability)، العمودَ الفقري للتصميم الآمن (backbone of secure design). وإليك أكثرها استخدامًا لدى البنّائين (builders)، إضافةً إلى ثلاث إضافاتٍ لاحقة (three later additions):

| المبدأ (Principle) | المعنى المبسّط (Plain meaning) | مخالفةٌ نموذجية (Typical violation) |
|---|---|---|
| **أقل الصلاحيات (Least privilege)** | الوصول المطلوب فقط، وللمدة المطلوبة فقط (only the access needed, only as long as needed) | حساب مسؤولٍ (admin account) واحد تتشاركه كل التطبيقات |
| **الدفاع المتعدد الطبقات (Defence in depth)** | طبقاتٌ مستقلة (independent layers)، فلا يكون إخفاقٌ واحد قاتلًا (no single failure is fatal) | «جدار الحماية يحميه» ("The firewall protects it")، ولا شيء خلفه يتحقق |
| **الإعدادات الافتراضية الآمنة من الإخفاق (Fail-safe defaults)** | ارفض ما لم يُسمح به صراحةً (deny unless explicitly allowed)؛ آمنٌ منذ التشغيل الأول (safe out of the box) | وضع التصحيح (debug mode) أو كلمات مرورٍ افتراضية (default passwords) تُشحن «مؤقتًا» ("for now") |
| **الإخفاق الآمن (Fail securely)** | حين يقع خطأٌ في فحصٍ ما (when a check errors)، تكون الإجابة «لا» ("no") | `except: allow` |
| **الوساطة الكاملة (Complete mediation)** | تحقّق من الصلاحية (check authority) في كل وصول (every access) | علامة «مسؤول» مخزّنة مؤقتًا (cached "is admin" flag) يوثَق بها لساعات (trusted for hours) |
| **فصل الصلاحيات (Separation of privilege)** | الإجراءات عالية المخاطر (high-risk actions) تتطلب شرطين أو شخصين (two conditions or two people) | مهندسٌ واحد يغيّر شيفرة الدفع (payment code) وينشرها (deploys) وحده |
| **تقليص سطح الهجوم (Minimise attack surface)** | نقاط دخولٍ أقل (fewer entry points) للدفاع عنها | نقاط نهايةٍ اختبارية منسية (forgotten test endpoints) تعمل في بيئة الإنتاج (production) |
| **الاقتصاد في الآلية (Economy of mechanism)** | أبقِ شيفرة الأمن صغيرةً بما يكفي لمراجعتها (small enough to review) | خمسة فحوصٍ مكتوبة يدويًا (hand-written checks) متعارضة |
| **التصميم المفتوح (Open design)** | لا اعتماد على جهل المهاجمين بالتصميم (attackers not knowing the design) | «لا أحد يعرف عنوان صفحة الإدارة هذا» ("Nobody knows this admin URL") |
| **القبول النفسي (Psychological acceptability)** | الأمن الصعب جدًا يُتجاوَز (gets bypassed) | قواعد مؤلمة إلى حدّ (rules so painful) أن الموظفين يتشاركون كلمات المرور (share passwords) |

يطبّق قسم 🏛️ معظمها على نجم أسيست (Najm Assist). وأربعةٌ منها تؤدي معظم العمل اليومي (daily work).

**أقل الصلاحيات (Least privilege)** تحدّ مما يكسبه المهاجم من أي اختراقٍ منفرد (any one compromise). طبّقها على الأشخاص، والخدمات، والرموز المميزة (tokens)، وأدوار السحابة (cloud roles)، ومستخدمي قواعد البيانات (database users)، وخطوط الأنابيب (pipelines)، ووكلاء الذكاء الاصطناعي (AI agents)، وفي الزمن (in time) كما في النطاق (scope): فالوصول المطلوب لساعةٍ ينبغي أن ينتهي بعد ساعة، وهذا هو **الوصول في الوقت المناسب (just-in-time access)**.

```sql
-- VULNERABLE: Assist's database user can read and change everything
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA core TO assist_svc;

-- FIXED: no table access; two functions that check card ownership inside
-- (SECURITY DEFINER functions owned by a separate role, each with a fixed search_path)
REVOKE ALL ON ALL TABLES IN SCHEMA core FROM assist_svc;
REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA core FROM PUBLIC;  -- PostgreSQL lets everyone run functions by default
ALTER DEFAULT PRIVILEGES IN SCHEMA core REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;  -- and future ones
GRANT EXECUTE ON FUNCTION core.list_my_cards(uuid) TO assist_svc;
GRANT EXECUTE ON FUNCTION core.freeze_card(uuid, uuid) TO assist_svc;
```

سطرا `FROM PUBLIC` هما نفساهما درسٌ في الإعدادات الافتراضية الآمنة (secure-defaults lesson): تحقّق مما تسمح به منصتك افتراضيًا (out of the box)، للكائنات الموجودة (existing objects) وللجديدة منها (new ones).

**الدفاع المتعدد الطبقات (Defence in depth)** يفترض أن كل طبقةٍ ستُخفق أحيانًا (will sometimes fail). ويجب أن تكون الطبقات **مستقلة (independent)**: فحصان يثق كلاهما بمعرّف العميل نفسه القادم من النموذج (same customer ID from the model) طبقةٌ واحدة، لا طبقتان (one layer, not two).

**الإعدادات الافتراضية الآمنة والإخفاق بالإغلاق (Secure defaults and failing closed).** تعمل معظم الأنظمة بإعداداتها الافتراضية (defaults)، لذا يجب أن تكون الحالة الآمنة (safe state) هي ما تحصل عليه حين لا تفعل شيئًا (by doing nothing)، ويجب أن تنتهي الأخطاء (errors) إلى «الرفض» ("deny").

```python
# VULNERABLE: fails open; any error in the policy service grants access
def can_view_invoice(user, invoice) -> bool:
    try:
        return policy.check(user, "invoice:read", invoice)
    except Exception:
        return True   # "don't block customers if the policy service is slow"
```

```python
# FIXED: fails closed, and the failure is visible
def can_view_invoice(user, invoice) -> bool:
    try:
        return policy.check(user, "invoice:read", invoice) is True
    except Exception:
        log.warning("policy check failed; denying", extra={"user": user.id, "invoice": invoice.id})
        metrics.increment("authz.fail_closed")
        return False
```

يحمي `is True` من فحصٍ يُرجع شيئًا يُقيَّم «صحيحًا» ("truthy") لكنه ليس قرارًا (not a decision)، مثل كائن خطأ (error object). وللإخفاق بالإغلاق (failing closed) كلفة (cost)، إذ لا فواتير ما دامت خدمة السياسات (policy service) متوقفة؛ عالج ذلك بالتكرار الاحتياطي (redundancy)، لا بإيقاف الأمن (switching security off).

**انعدام الثقة (Zero trust).** كانت الشبكات التقليدية (traditional networks) تثق بكل ما هو داخل المحيط (inside the perimeter): نموذج «القلعة والخندق» ("castle and moat"). أما **انعدام الثقة (zero trust)**، كما عرّفه NIST SP 800-207 عام 2020، فيُسقط هذا الافتراض. لا يحصل أي مستخدمٍ أو جهازٍ أو خدمةٍ على ثقةٍ ضمنية (implicit trust) من موقعه في الشبكة (network location)؛ فكل طلبٍ إلى مورد (resource) تتم مصادقته وتفويضه (authenticated and authorised)، باستخدام سياسةٍ (policy) يمكنها أن تزن الهوية (identity) وسلامة الجهاز (device health) والسياق (context). وبالنسبة لفريق تطبيقات (application team)، تصادق الخدمات بعضها على بعض (services authenticate to each other)، مثلًا عبر TLS المتبادل (mutual TLS)، حتى داخل العنقود (inside the cluster)، ويُفوَّض كل استدعاءٍ للمورد المحدد (specific resource)، و**تفترض وقوع الاختراق (assume breach)**: صمّم كأن المهاجم في الداخل فعلًا، وقيّد ما يمكنه الوصول إليه (limit what they can reach).

### 🟡 التعمق أكثر (Going deeper)

**الدفاع المتعدد الطبقات لإجراءٍ واحد (Defence in depth for one action).** تحمي هذه الطبقات (layers) إجراء «جمّد بطاقتي» ("freeze my card") في نجم أسيست. وكلٌّ منها ضابطٌ منفصل (separate control) يستطيع وحده إيقاف تجميدٍ خاطئ (wrong freeze):

```mermaid
flowchart RL
    A["رسالة العميل<br/>(Customer message)"] --> B["الحافة: تشفير النقل وجدار حماية التطبيقات وحدود المعدل<br/>(Edge: TLS, WAF, rate limits)"]
    B --> C["المصادقة: جلسة وجهاز صالحان<br/>(Authentication: valid session and device)"]
    C --> D["سياسة الأدوات: التجميد فقط، ولا إلغاء تجميد أو دفع أبدًا<br/>(Tool policy: freeze only, never unfreeze or pay)"]
    D --> E["التفويض: البطاقة تعود إلى هذا العميل<br/>(Authorisation: card belongs to this customer)"]
    E --> F["تأكيد يُعرض في التطبيق<br/>(Confirmation shown in the app)"]
    F --> G["خدمة البطاقات بحقوق قاعدة بيانات بأقل الصلاحيات<br/>(Card service with least-privilege database rights)"]
    G --> H["سجل التدقيق وتنبيه مركز العمليات الأمنية عند حجم غير معتاد<br/>(Audit log and SOC alert on unusual volume)"]
```

نموذج «الجبن السويسري» ("Swiss cheese") للحوادث، الذي وضعه جيمس ريزن (James Reason)، هو الصورة المعيارية (standard picture): لكل طبقةٍ ثقوب (holes)، ولا يمر الضرر إلا حين تصطف الثقوب (the holes line up). والاستقلالية (independence) تمنعها من الاصطفاف. فإذا أخذ فحص التفويض (authorisation check) وشاشة التأكيد (confirmation screen) وسجل التدقيق (audit log) جميعها معرّف البطاقة (card ID) من مخرجات النموذج (model's output) دون مقارنته بالجلسة (session)، فإن استدعاء أداةٍ واحدًا متلاعبًا به (one manipulated tool call) يمر عبر الثلاثة.

**انعدام الثقة في المعمارية (Zero trust in architecture).** يصف SP 800-207 **نقطة قرار السياسة (policy decision point, PDP)**، التي تقرر ما إذا كان الطلب مسموحًا، و**نقطة إنفاذ السياسة (policy enforcement point, PEP)**، التي تقع في مسار الطلب (request path) وتطبّق ذلك القرار. في بنك نجم، تتولى بوابة واجهات البرمجة (API gateway) ووكيلٌ وسيط (proxy) أمام كل خدمةٍ الإنفاذَ (enforce)؛ وتتولى خدمة التفويض المركزية (central authorisation service) القرار (decides). وينظّم نموذج نضج انعدام الثقة (Zero Trust Maturity Model) الصادر عن CISA، في إصداره 2.0 لعام 2023، الرحلةَ في خمس ركائز (five pillars)، هي الهوية (identity)، والأجهزة (devices)، والشبكات (networks)، والتطبيقات وأحمال العمل (applications and workloads)، والبيانات (data)، وفي مراحل (stages) من «تقليدي» ("traditional") إلى «مثالي» ("optimal"). انعدام الثقة اتجاهٌ للسير (direction of travel)، لا منتج (not a product). واحذر ممن يبيعه في صندوق (selling it in a box).

**أقل الصلاحيات عمليًا (Least privilege in practice).** تتراكم الصلاحيات بمرور الوقت (permissions pile up over time)، وهذا هو **زحف الصلاحيات (privilege creep)**. الأدوات العملية (working tools):
- **ابدأ من الصفر (Start from zero)** وأضف الصلاحيات كلما فشلت الاختبارات (as tests fail)، بدلًا من البدء على نطاقٍ واسع ثم التقليص (starting broad and trimming).
- **حدّد النطاق بالمورد والإجراء (Scope by resource and action)**: «تجميد بطاقات العميل المسجِّل دخوله» ("freeze cards of the signed-in customer")، لا «واجهة البطاقات: وصولٌ كامل» ("card API: full access").
- **بيانات اعتمادٍ قصيرة العمر (Short-lived credentials)** لكل حمل عمل (per workload) بدلًا من المفاتيح طويلة العمر (long-lived keys)، كما في الدرس 5.2.
- **رفع الصلاحيات في الوقت المناسب (Just-in-time elevation)** للأشخاص: ساعتان من الوصول إلى بيئة الإنتاج (production access)، بموافقةٍ وتسجيل (approved and logged)، ثم ينتهي. واحتفظ بحساب **كسر الزجاج (break-glass)** للطوارئ، مختبَرًا ومراقَبًا عن كثب (tested, closely watched).
- **مراجعات الوصول (Access reviews)** و**تقارير الصلاحيات غير المستخدمة (unused-permission reports)** من أدوات مزوّد السحابة لديك (cloud provider's tooling).

**آمنٌ بالتصميم (Secure by design).** منذ عام 2023، نشرت CISA ووكالاتٌ شريكة (partner agencies) في عدة دول إرشادات «آمن بالتصميم» ("Secure by Design") التي تحث صانعي البرمجيات (software makers) على شحن منتجاتٍ آمنة منذ التشغيل الأول (secure out of the box): لا كلمات مرورٍ افتراضية (no default passwords)، والمصادقة متعددة العوامل (multi-factor authentication) مفعّلةٌ افتراضيًا، وسجلات الأمن (security logs) بلا كلفةٍ إضافية. واختبارٌ مفيد لأي فريق منصة (platform team): هل كنا سنشحن هذا للعملاء بإعداداتنا الافتراضية الحالية (today's defaults)؟

**وكلاء البرمجة بالذكاء الاصطناعي يحتاجون إلى القواعد نفسها (AI coding agents need the same rules).** يستخدم مطورو بنك نجم وكلاء برمجةٍ بالذكاء الاصطناعي (AI coding agents) يستطيعون تشغيل أوامر الطرفية (shell commands). شغّلهم في بيئةٍ معزولة (sandbox) لا تطالها أي بيانات اعتمادٍ للإنتاج (production credentials)، مع قائمة سماحٍ قصيرة (short allow-list) بالأوامر التي تعمل دون موافقة (without approval)، ومراجعةٍ بشرية (human review) قبل الدمج (merging)، كما في الدرس 6.3. فالوكيل الذي يملك صلاحياتك الكاملة (full permissions) يمكن توجيهه بتعليمةٍ مخفية في ملفٍ يقرؤه (instruction hidden in a file it reads).

### 🔴 نظرة الخبير (Expert view)

**النائب المرتبك (The confused deputy).** وصفت ورقة نورم هاردي (Norm Hardy) عام 1988 برنامجًا يملك صلاحيةً لغرضٍ ما (authority for one purpose) فخُدع لاستخدامها لصالح شخصٍ آخر (for someone else). ووكلاء الذكاء الاصطناعي (AI agents) نوّابٌ مرتبكون بطبيعة بنائهم (confused deputies by construction): يتصرفون ببيانات اعتماد (credentials)، نيابةً عن مستخدم (on behalf of a user)، موجَّهين بنصٍ قد يأتي من طرفٍ ثالث (third party). والإصلاح أن يحمل الوكيل **صلاحية المستخدم (user's authority)**، لا صلاحيته الخاصة. يُفوَّض كل استدعاء أداةٍ على أنه «هذا العميل، عبر أسيست» ("this customer, through Assist")، برموزٍ مميزة مفوَّضة (delegated) وضيقة النطاق (narrowly scoped) وقصيرة العمر (short-lived)؛ وتبادل الرموز في OAuth 2.0 (OAuth 2.0 Token Exchange)، المعرَّف في RFC 8693، أحد هذه الأنماط (one pattern)، كما في الدرس 3.2. عندها لا يستطيع الوكيل أبدًا أن يفعل أكثر مما يستطيعه المستخدم (never do more than the user could). ويطبّق الدرس 9.2 ذلك على تصميم الأدوات (tool design) وMCP.

**المبادئ تتعارض، والحكم يفصل بينها (Principles conflict; judgement settles it).** تضيف الطبقات الإضافية تعقيدًا (complexity)، والتعقيد يولّد الأخطاء (breeds bugs). وأقل الصلاحيات الصارمة (strict least privilege) تبطئ الفرق وتستدعي الالتفافات (invites workarounds). والإخفاق بالإغلاق (failing closed) قد يضر بالتوافر (availability). سمِّ المفاضلة (name the trade-off) في مراجعة التصميم (design review) واحسم الأمر بنطاق الضرر (blast radius): كلما زادت قدرة الإجراء على إيذاء العملاء أو تحريك الأموال (move money)، زاد ما يستحقه من احتكاك (friction).

**النموذج ليس حدًّا أمنيًا (The model is not a security boundary).** موجّه النظام (system prompt) الذي يقول «لا تكشف أبدًا بيانات العملاء الآخرين» ("never reveal other customers' data") طلبٌ (request)، لا ضابط (control). يمكن لحقن الموجّهات (prompt injection) أن يتجاوزه، ويمكن أن يتسرب (it can leak)، وهذا ما يغطيه OWASP LLM07، تسريب موجّه النظام (System Prompt Leakage). وكل قاعدةٍ مهمة تُفرَض في الشيفرة خارج النموذج (enforced in code outside the model): في الأداة (tool)، أو طبقة البيانات (data layer)، أو البوابة (gateway).

**اجعل المبادئ قابلةً للقياس (Make principles measurable).** عُدّ حسابات الخدمة ذات الصلاحيات الشاملة (service accounts with wildcard permissions)، والصلاحيات غير المستخدمة منذ 90 يومًا (unused for 90 days)، والاستدعاءات الداخلية غير المصادَق عليها (unauthenticated internal calls)، والعمر الوسيط لبيانات الاعتماد (median lifetime of credentials). يطلب حمد، رئيس أمن المعلومات (CISO)، ثلاثةً منها كل ربع سنة (every quarter).

## 🧰 الأدوات (The toolkit)
| الضابط أو المعيار أو الأداة (Control, standard or tool) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |
|---|---|---|
| **Saltzer and Schroeder design principles** — مبادئ التصميم لسالتزر وشرودر | مبادئ التصميم الآمن لعام 1975 (1975 secure-design principles)، ومنها أقل الصلاحيات (least privilege) والإعدادات الافتراضية الآمنة من الإخفاق (fail-safe defaults) والوساطة الكاملة (complete mediation) | مراجعات التصميم (design reviews)؛ وحسم معنى التصميم «الجيد بما يكفي» ("good enough") |
| **Least privilege** — أقل الصلاحيات | الحد الأدنى من الوصول لأقصر وقت (minimum access for the minimum time)، لكل هويةٍ ومورد (per identity and resource) | كل حساب خدمة (service account) أو دور (role) أو رمزٍ مميز (token) أو خط أنابيب (pipeline) أو وكيل ذكاءٍ اصطناعي (AI agent) جديد |
| **Defence in depth** — الدفاع المتعدد الطبقات | طبقاتٌ مستقلة (independent layers)، فلا يكون إخفاقٌ واحد اختراقًا (one failure is not a breach) | أي إجراءٍ أو مخزن بياناتٍ عالي القيمة (high-value action or data store) |
| **Fail-safe defaults** — الإعدادات الافتراضية الآمنة من الإخفاق | ارفض ما لم يُسمح به صراحةً (deny unless explicitly allowed)؛ وأخفِق بالإغلاق عند الأخطاء (fail closed on errors) | شيفرة التفويض (authorisation code)، والإعدادات (configuration)، والمسارات الجديدة (new routes) والتخزين (storage) |
| **Zero trust architecture** — معمارية انعدام الثقة، وفق NIST SP 800-207 | لا ثقة ضمنية من موقع الشبكة (no implicit trust from network location)؛ وكل طلبٍ تتم مصادقته وتفويضه (authenticated and authorised) | تصميم الاتصال بين الخدمات (service-to-service design)؛ والوصول عن بُعد (remote access)؛ والشبكات الداخلية المسطّحة (flat internal networks) |
| **CISA Zero Trust Maturity Model** — نموذج نضج انعدام الثقة من CISA | خمس ركائز ومراحل نضج (five pillars and maturity stages) لبرنامج انعدام الثقة (zero-trust programme) | خرائط الطريق (roadmaps) وقياس التقدم (measuring progress) |
| **Just-in-time access** — الوصول في الوقت المناسب | رفع صلاحياتٍ محدودٌ زمنيًا، بموافقة، ومسجَّل (time-limited, approved, logged elevation of privilege) | وصول الأشخاص إلى بيئة الإنتاج (production) والبيانات الحساسة (sensitive data) |
| **Secure by Design** — آمنٌ بالتصميم، من CISA وشركائها (CISA and partners) | إرشاداتٌ (guidance) لمنتجاتٍ آمنة منذ التشغيل الأول (secure out of the box) | ضبط الإعدادات الافتراضية (setting defaults) للمنصات والقوالب والمنتجات (platforms, templates and products) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
تحوّل نورة المبادئ إلى **مراجعة التصميم الآمن في بنك نجم: عشرة أسئلة (Najm Secure Design Review: ten questions)**، تُرفق بكل وثيقة تصميم (design document). ويجيب فريق طارق عنها لطبقة الأدوات (tool layer) في نجم أسيست (Najm Assist).

| # | المبدأ (Principle) | السؤال (Question) | طبقة أدوات نجم أسيست: الإجابة والدليل (Najm Assist tool layer: answer and evidence) |
|---|---|---|---|
| 1 | أقل الصلاحيات (Least privilege) | ما الذي تستطيع كل هويةٍ فعله بالضبط، ولماذا؟ ⁦(What exactly can each identity do, and why?)⁩ | سرد بطاقات العميل نفسه (list own cards)، وتجميد بطاقته (freeze own card)، وقراءة جدول الرسوم (read fee schedule). ملف الصلاحيات (permission file) في المستودع (repository) |
| 2 | أقل الصلاحيات زمنيًا (Least privilege in time) | ما بيانات الاعتماد طويلة العمر (long-lived credentials)؟ | لا شيء (None). تنتهي رموز أحمال العمل (workload tokens) خلال 15 دقيقة |
| 3 | الدفاع المتعدد الطبقات (Defence in depth) | سمِّ ضابطين مستقلين (two independent controls) يوقف كلٌّ منهما أسوأ نتيجة (worst outcome) | فحص الملكية (ownership check) في خدمة البطاقات؛ وشاشة تأكيدٍ مبنية من بيانات الخادم (server data) |
| 4 | الإعدادات الافتراضية الآمنة من الإخفاق (Fail-safe defaults) | ما الإعداد الافتراضي (default) لمسارٍ أو أداةٍ أو حاوية تخزينٍ جديدة (new route, tool or bucket)؟ | الرفض (Deny). يجب أن تكون الأدوات في قائمة السماح (allow-list)؛ ويمنع التكامل المستمر (CI) الحاويات العامة (public buckets) |
| 5 | الإخفاق الآمن (Fail securely) | ماذا يحدث حين يُخفق فحصٌ ما (a check fails)؟ | يُرفض التجميد (freeze refused)؛ ويُوجَّه العميل إلى الزر داخل التطبيق (in-app button) |
| 6 | الوساطة الكاملة (Complete mediation) | أين يُتحقق من الصلاحية (authority checked) في كل استدعاء (every call)؟ | في خدمة البطاقات (card service)؛ لا موافقات مخزّنة مؤقتًا (no cached approvals) |
| 7 | فصل الصلاحيات (Separation of privilege) | ما الإجراءات التي تتطلب شخصين أو عاملين (two people or factors)؟ | إلغاء التجميد يتطلب إعادة المصادقة داخل التطبيق (in-app re-authentication)؛ وتغييرات الموجّهات (prompt changes) تتطلب موافِقَين اثنين (two approvers) |
| 8 | سطح الهجوم (Attack surface) | ما الذي يمكن إزالته؟ | أُوقفت نقطة نهاية المحادثة القديمة من الإصدار v1 (old v1 chat endpoint retired) |
| 9 | انعدام الثقة (Zero trust) | هل يُوثَق بأي استدعاءٍ لأنه «داخلي» ("internal")؟ | لا. TLS المتبادل (mutual TLS) إضافةً إلى رمزٍ مميز لكل طلب (per-request token) |
| 10 | سهولة الاستخدام (Usability) | هل سيتجاوز الناس هذا (bypass this)؟ | تأكيدٌ بنقرةٍ واحدة (one-tap confirmation)؛ ويُتتبَّع التخلي عن العملية (abandonment tracked) |

**قاعدةٌ أُضيفت إلى معيار الهندسة في بنك نجم (Rule added to Najm's engineering standard):** «تُصمَّم وكلاء الذكاء الاصطناعي وأدواتهم (AI agents and their tools) بحيث إذا تحكّم المهاجم بالنموذج تحكمًا كاملًا (fully controls the model)، تقتصر أسوأ نتيجةٍ (worst outcome) على ما كان العميل المسجِّل دخوله (signed-in customer) يستطيع فعله أصلًا، ويتطلب كل إجراءٍ ذي أثر (consequential action) تأكيدًا صريحًا من العميل (customer's explicit confirmation).» ويوقّعها حمد بصفته رئيس أمن المعلومات (CISO).

## 🛠️ التمارين (Exercises)
- 🟢 اختر مشروعًا تملكه. اسرد كل بيانات الاعتماد (credential) التي يستخدمها، من مستخدمي قواعد البيانات (database users) وأدوار السحابة (cloud roles) ومفاتيح واجهات البرمجة (API keys) ورموز التكامل المستمر (CI tokens)، وما يستطيع كلٌّ منها فعله وما يحتاجه فعلًا (what it actually needs). *يكتمل عندما (Done when):* يكون لديك جدول «الممنوح مقابل المطلوب» (granted-versus-needed table) لكل بيانات اعتماد، مع تعليم صلاحيةٍ واحدة على الأقل للإزالة (marked for removal).
- 🟡 في قاعدة شيفرتك (codebase)، ابحث عن معالجة أخطاء (error handling) حول فحص مصادقةٍ أو تفويض (authentication or authorisation check)، مثل `except` مجرّد (bare) أو `catch` فارغ (empty). أعد كتابة واحدٍ منها ليُخفق بالإغلاق (fail closed)، واكتب اختبارًا يحاكي إخفاق الفحص (simulates the check failing). *يكتمل عندما (Done when):* يثبت الاختبار أن الوصول مرفوض (access is denied) وأن سطر سجلٍ (log line) أو مقياسًا (metric) يسجّل الإخفاق.
- 🔴 في مختبرٍ محلي (local lab)، صمّم الوصول لوكيلٍ (agent) بثلاث أدوات، للقراءة والتغيير والحذف (read, change, delete)، يعمل نيابةً عن مستخدمين مسجِّلين دخولهم (logged-in users). حدّد نقاط القرار والإنفاذ (decision and enforcement points)، وكيف تصل هوية المستخدم (user's identity) إلى كل أداة، وطبقتين مستقلتين (two independent layers) توقفان «حذف بيانات مستخدمٍ آخر» ("delete another user's data"). *يكتمل عندما (Done when):* لا تستطيع بيانات اعتماد الوكيل الخاصة (agent's own credentials) فعل أكثر مما يستطيعه المستخدم، وتُظهر اختباراتك أن كل طبقةٍ تمنع الحذف حين تُعطَّل الأخرى (when the other is switched off).

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **«واسعٌ الآن، ونضيّق لاحقًا» ⁦("Broad for now, tighten later.")⁩** «لاحقًا» نادرًا ما يأتي (Later rarely comes). ابدأ من الصفر (start from zero) وأضف فقط ما تُظهر الاختبارات أنه مطلوب (what tests show is needed).
- **طبقاتٌ تتشارك افتراضًا (Layers that share an assumption).** ثلاثة فحوصٍ تثق بالقيمة غير الموثَّقة نفسها (same unverified value) فحصٌ واحد. اجعل الطبقات مستقلة (make layers independent).
- **الإخفاق بالفتح من أجل التوافر (Failing open for availability).** يجب ألّا يتحول انقطاع خدمة السياسات (policy-service outage) إلى انقطاعٍ أمني (security outage). أخفِق بالإغلاق (fail closed)، وعالج التوافر بالتكرار الاحتياطي (redundancy).
- **الوثوق بـ«الداخلي» (Trusting "internal").** الوجود داخل الشبكة ليس هوية (not an identity). صادِق وفوّض الاستدعاءات بين الخدمات (authenticate and authorise service-to-service calls).
- **قواعد الأمن في الموجّه فقط (Security rules only in the prompt).** يمكن إقناع النموذج بالتخلي عنها (talked out of them). افرضها في الشيفرة خارج النموذج (in code outside the model).

## 🧾 الخلاصة (Recap)
- ما زالت مبادئ سالتزر وشرودر (Saltzer and Schroeder's principles) لعام 1975 تحدد ما إذا كان الخطأ البرمجي (bug) سيصبح اختراقًا (breach).
- أقل الصلاحيات (Least privilege) تحدّ من نطاق الضرر (blast radius). طبّقها على الأشخاص والخدمات والرموز المميزة (tokens) وخطوط الأنابيب (pipelines) ووكلاء الذكاء الاصطناعي (AI agents)، في النطاق وفي الزمن (in scope and in time).
- لا ينجح الدفاع المتعدد الطبقات (Defence in depth) إلا حين تكون الطبقات مستقلة (independent). والإعدادات الافتراضية الآمنة (secure defaults) والإخفاق بالإغلاق (failing closed) يجعلان النتيجة الآمنة هي التي لا تتطلب جهدًا (the effortless one).
- يزيل انعدام الثقة (Zero trust)، وفق NIST SP 800-207، الثقةَ المبنية على موقع الشبكة (network location): كل طلبٍ تتم مصادقته وتفويضه (authenticated and authorised).
- وكلاء الذكاء الاصطناعي (AI agents) نوّابٌ مرتبكون بطبيعة تصميمهم (confused deputies by design). امنحهم صلاحية المستخدم المحددة النطاق (user's scoped authority)، وافرض القواعد في الشيفرة لا في الموجّهات (in code, not prompts).

## ✍️ اختبر نفسك (Check yourself)

**1. يريد طارق أن يعيد حساب الخدمة (service account) الخاص بنجم أسيست استخدام النطاق الكامل لواجهة البرمجة (full API scope) الخاص بالواجهة الخلفية للتطبيق المحمول (mobile backend) «كي تصبح إضافة الأدوات الجديدة أسرع» ("so new tools are quicker to add"). أي مبدأٍ يخالفه هذا، وما التصميم الأفضل (better design)؟**

- A. التصميم المفتوح (Open design)؛ انشر النطاق (publish the scope) كي تمكن مراجعته (so it can be reviewed)
- B. أقل الصلاحيات (Least privilege)؛ امنح فقط الإجراءات التي يحتاجها أسيست الآن، محصورةً في العميل المسجِّل دخوله (scoped to the signed-in customer)، وأضف المزيد عبر المراجعة (through review)
- C. الاقتصاد في الآلية (Economy of mechanism)؛ استخدم رموزًا مميزةً أقل (fewer tokens)
- D. القبول النفسي (Psychological acceptability)؛ فذلك سيزعج المطورين (annoy developers)

<details><summary>الإجابة</summary>

**B.** النموذج الذي يستطيع العملاء توجيهه بالنص (steer with text) يجب أن يحمل الحد الأدنى من الصلاحية (minimum authority). والنطاق الواسع «لما قد نحتاجه لاحقًا» ("for later") يحوّل استدعاء أداةٍ واحدًا متلاعبًا به (one manipulated tool call) إلى تحويلٍ مالي (transfer) أو تسرّب بيانات (data leak). انظر: 🟢 الأساسيات (The essentials)؛ 🧭 لماذا يهم (Why it matters).

</details>

**2. يستدعي فحص الفواتير (invoice check) في بوابة الشركات الصغيرة (SME Portal) خدمةَ سياسات (policy service). وحين تنتهي مهلة الخدمة (times out)، تُرجع الشيفرة `True` كي لا يُحجب العملاء. ما التغيير الصحيح (correct change)؟**

- A. زيادة المهلة (increase the timeout) كي تقل مرات الإخفاق (fails less often)، مع الاستمرار في إرجاع `True`
- B. تخزين الإجابة الأخيرة مؤقتًا إلى الأبد (cache the last answer forever)
- C. إرجاع `False` عند أي خطأ، وتسجيل الإخفاق وعدّه (log and count the failure)، ومعالجة التوافر بالتكرار الاحتياطي (fix availability with redundancy)
- D. إزالة فحص السياسة (policy check) كي تصبح الصفحات أسرع (make pages faster)

<details><summary>الإجابة</summary>

**C.** يجب أن تنتهي الأخطاء إلى «الرفض» ("deny")، وهذا هو الإخفاق الآمن (fail securely). مشكلة التوافر (availability problem) حقيقية، لكن التكرار الاحتياطي (redundancy) هو ما يحلها، لا إيقاف الأمن (switching security off). أما A فما زال يُخفق بالفتح (fails open)، وإن بوتيرةٍ أقل. انظر: 🟢 الأساسيات (The essentials).

</details>

**3. أي عبارةٍ تصف انعدام الثقة (zero trust) على أفضل وجه (best describes) كما عرّفه NIST SP 800-207؟**

- A. لا يُسمح لأي مستخدمٍ أبدًا بالوصول إلى أي شيء (no user is ever allowed access)
- B. منتج جدار حماية (firewall product) يحجب كل حركة الإنترنت (internet traffic)
- C. الوثوق بالحركة الداخلية (internal traffic) وفحص الحركة الخارجية (external traffic)
- D. لا ثقة ضمنية مبنية على موقع الشبكة (no implicit trust based on network location)؛ وكل طلبٍ إلى موردٍ تتم مصادقته وتفويضه باستخدام السياسة (using policy)

<details><summary>الإجابة</summary>

**D.** يزيل انعدام الثقة (Zero trust) فكرة أن الوجود «في الداخل» ("inside") يكسب الثقة. وهو لا يعني رفض كل شيء (denying everything)، أي الخيار A، وهو معماريةٌ (architecture) لا منتج (product)، خلافًا للخيار B. أما C فهو نموذج المحيط القديم (old perimeter model) الذي يحل محله. انظر: 🟢 الأساسيات (The essentials)؛ 🟡 التعمق أكثر (Going deeper).

</details>

**4. لدى نجم أسيست ثلاثة ضوابط (three controls) ضد تجميد البطاقة الخطأ: فحص الملكية (ownership check)، وشاشة التأكيد (confirmation screen)، وتنبيه التدقيق (audit alert). وتأخذ الثلاثة جميعًا معرّف البطاقة (card ID) من استدعاء الأداة (tool call) الذي يصدره النموذج دون مقارنته بالجلسة (session). ما نقطة الضعف (weakness)؟**

- A. الطبقات ليست مستقلة (not independent)، لذا تمر قيمةٌ واحدة متلاعبٌ بها (one manipulated value) عبر الثلاثة
- B. الطبقات قليلةٌ جدًا (too few layers)؛ أضف رابعة (add a fourth)
- C. يجب إزالة تنبيه التدقيق (audit alert) لتبسيط التصميم (simplify the design)
- D. لا شيء؛ ثلاث طبقاتٍ تكفي (three layers are enough)

<details><summary>الإجابة</summary>

**A.** يحتاج الدفاع المتعدد الطبقات (Defence in depth) إلى طبقاتٍ تُخفق لأسبابٍ مختلفة (fail for different reasons). وهذه الثلاث تتشارك مُدخلًا واحدًا غير موثَّق (one unverified input)، لذا فإن طبقةً رابعة بالمُدخل نفسه (B) لا تغيّر شيئًا. انظر: 🟡 التعمق أكثر (Going deeper).

</details>

**5. لماذا يُسمّى وكيل الذكاء الاصطناعي (AI agent) الذي يعمل ببيانات اعتماد خدمةٍ واسعة خاصةٍ به (own broad service credentials) «نائبًا مرتبكًا» ("confused deputy")؟**

- A. لأن النماذج تعطي أحيانًا إجاباتٍ خاطئة (wrong answers)
- B. لأنه يملك صلاحيةً لغرضٍ ما (authority for one purpose) ويمكن توجيهه بنص شخصٍ آخر (someone else's text) إلى استخدامها لغرضٍ آخر؛ والإصلاح أن يتصرف بصلاحية المستخدم المحددة النطاق (user's scoped authority)
- C. لأن لديه موجّهَي نظام (two system prompts)
- D. لأنه لا يستطيع قراءة قوائم التحكم في الوصول (access-control lists)

<details><summary>الإجابة</summary>

**B.** يستخدم النائب المرتبك (confused deputy) الذي وصفه هاردي (Hardy) صلاحيته الخاصة (own privilege) لصالح الطرف الخطأ (wrong party). وبصلاحية المستخدم المفوَّضة والمحددة النطاق وقصيرة العمر (delegated, scoped, short-lived authority)، لا يستطيع الوكيل أبدًا أن يفعل أكثر مما يستطيعه المستخدم. أما A فيتعلق بالموثوقية (reliability) لا بالصلاحية (authority). انظر: 🔴 نظرة الخبير (Expert view).

</details>

## 📚 المراجع (References)
- سالتزر وشرودر ⁦(Saltzer, J. H. and Schroeder, M. D.)⁩ عام 1975، ورقة «حماية المعلومات في أنظمة الحاسوب» ("The Protection of Information in Computer Systems")، مجلة *Proceedings of the IEEE* 63(9)
- وثيقة NIST SP 800-207، معمارية انعدام الثقة (Zero Trust Architecture)، 2020 — https://csrc.nist.gov/pubs/sp/800/207/final
- وكالة CISA، نموذج نضج انعدام الثقة (Zero Trust Maturity Model)، الإصدار 2.0 (Version 2.0)، 2023 — https://www.cisa.gov/zero-trust-maturity-model
- وكالة CISA، آمنٌ بالتصميم (Secure by Design) — https://www.cisa.gov/securebydesign
- هاردي ⁦(Hardy, N.)⁩ عام 1988، ورقة «النائب المرتبك» ("The Confused Deputy")، مجلة *ACM SIGOPS Operating Systems Review* 22(4)
- المواصفة RFC 8693، تبادل الرموز في OAuth 2.0 (OAuth 2.0 Token Exchange) — https://www.rfc-editor.org/rfc/rfc8693
- قائمة OWASP لأهم عشرة مخاطر في تطبيقات النماذج اللغوية الكبيرة لعام 2025 (OWASP Top 10 for LLM Applications 2025) — https://genai.owasp.org

---

# 1.3 — تقييم المخاطر وترتيب أولوياتها: الاحتمالية والأثر وCVSS (Rating and prioritising risk: likelihood, impact and CVSS)
*المستوى (Level): 🟢 مبتدئ (Beginner)* · *المتطلبات (Prerequisites): 1.1، 1.2* · *المرحلة (Phase): Plan, Operate*

## ⚡ الدرس في دقيقة (In 60 seconds)
- تجمع **المخاطر (Risk)** بين مدى احتمال وقوع أمرٍ سيئ، أي **الاحتمالية (likelihood)**، ومقدار الضرر الذي يُحدثه، أي **الأثر (impact)**. لا يمكنك أبدًا إصلاح كل شيءٍ دفعةً واحدة (fix everything at once)، لذا فالمهمة هي إصلاح الأشياء الصحيحة أولًا (fix the right things first).
- يقيّم **CVSS**، أي نظام تقييم الثغرات الشائع (Common Vulnerability Scoring System) الصادر عن FIRST، **الخطورة (severity)** التقنية للثغرة (vulnerability) من 0 إلى 10. وتؤكد FIRST أنه يقيس الخطورة (measures severity)، لا المخاطر على مؤسستك (not risk to your organisation). نُشر الإصدار 4.0 في نوفمبر 2023؛ وما زال الإصدار 3.1 مستخدمًا على نطاقٍ واسع (widely used).
- أضف **أدلة الاستغلال (exploitation evidence)**: يسرد **كتالوج الثغرات المستغلة المعروفة (Known Exploited Vulnerabilities, KEV)** من CISA العيوبَ التي تُهاجَم في الواقع (attacked in the wild)، ويقدّر **EPSS** احتمال نشاط الاستغلال (probability of exploitation activity) خلال الأيام الثلاثين التالية (next 30 days).
- أضف **السياق (context)**: هل يمكن الوصول إلى الأصل (asset) من الإنترنت (reachable from the internet)، وهل يحتفظ ببيانات العملاء (customer data) أو يحرّك الأموال (move money)، وما الضوابط (controls) التي تعترض الطريق أصلًا؟
- مؤشر القرار (Decision cue): ما كان «مستغَلًّا معروفًا، ومكشوفًا، وقيّمًا» ("known exploited, exposed and valuable") يذهب إلى رأس القائمة (goes to the top)، أيًّا كان ما تقوله درجة CVSS (CVSS score).
- أكبر فخ (Biggest trap): الفرز حسب CVSS وحده (sorting by CVSS alone)، فتقضي الفرق شهورًا على ملاحظاتٍ «حرجة» ("critical") لا يستطيع أحدٌ الوصول إليها، بينما تنتظر ثغرةٌ «عالية» ("high") مستغلة على حافة الإنترنت (internet edge).

## 🧭 لماذا يهم (Why it matters)
أنهت ماسحات (scanners) علي أول تشغيلٍ كامل لها (first full run) على منصة السحابة (cloud platform) في بنك نجم: 4,100 ملاحظةٍ مفتوحة (open findings)، منها 620 مصنّفة حرجة (Critical). وخطته أن يصلحها بترتيب درجات CVSS (CVSS order). يشير طارق إلى أنه، بوتيرة فريقه (at his team's pace)، ستستغرق الملاحظات الحرجة (Criticals) وحدها معظم عام (most of a year).

تطرح نورة ثلاثة أسئلة. أيٌّ من هذه يستغله أحدٌ فعلًا (actually exploiting)؟ أي الأنظمة يمكن الوصول إليها من الإنترنت (reached from the internet)؟ أيها يحتفظ ببيانات العملاء (customer data) أو يستطيع تحريك الأموال (move money)؟ تعيد الإجابات ترتيب كل شيء. فمعظم الثغرات ذات الدرجة 10.0 تقع في مكتبةٍ (library) تستخدمها مهمةٌ دفعية داخلية (internal batch job) بلا مستمِعٍ شبكي (network listener). وفي المقابل، ثمة ثغرةٌ بدرجة 7.5 في جهاز VPN للوصول عن بُعد (remote-access VPN appliance) مدرجةٌ في قائمة CISA للثغرات المستغلة (CISA's exploited list). ولدى فريق مريم ملاحظةٌ في بوابة الشركات الصغيرة (SME Portal) لم تصل قط إلى لوحة المتابعة (dashboard) لأنها بلا معرّف CVE (no CVE): يستطيع مستخدم شركةٍ تنزيل فواتير شركةٍ أخرى بتغيير رقمٍ في الرابط (URL).

يبيّن التاريخ العام (public history) حجم الرهان (the stakes). في عام 2017، اختُرقت Equifax عبر ثغرةٍ معروفة (known vulnerability) في Apache Struts، هي CVE-2017-5638. ووفقًا للتقارير العامة (public reports) والمراجعات اللاحقة للحكومة الأمريكية (later US government reviews)، كان إصلاحٌ (a fix) قد نُشر قبل نحو شهرين من دخول المهاجمين أول مرة (first got in). ووصفت لجنة التجارة الفيدرالية الأمريكية (US Federal Trade Commission) الاختراق لاحقًا بأنه طال نحو 147 مليون شخص. لم يكن الإخفاق في المعرفة (not knowing)؛ بل في إنجاز الإصلاح الصحيح في الوقت المناسب (getting the right fix done in time).

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**المخاطر = الاحتمالية × الأثر (Risk = likelihood × impact).** نادرًا ما يكون الأمر ضربًا حرفيًا (literal multiplication)، لكن الفكرة صحيحة: عيبٌ خطير (severe flaw) لا يستطيع أحدٌ الوصول إليه أقل مخاطرةً من عيبٍ متوسط على الباب الأمامي (moderate flaw on the front door). تبدأ معظم الفرق **بمصفوفة المخاطر (risk matrix)**: قيّم الاحتمالية والأثر بمنخفض (Low) أو متوسط (Medium) أو مرتفع (High)، واقرأ المخاطر الإجمالية (overall risk) من الشبكة (grid).

| | الأثر (Impact): منخفض (Low) | الأثر (Impact): متوسط (Medium) | الأثر (Impact): مرتفع (High) |
|---|---|---|---|
| **الاحتمالية (Likelihood): مرتفعة (High)** | متوسطة (Medium) | مرتفعة (High) | حرجة (Critical) |
| **الاحتمالية (Likelihood): متوسطة (Medium)** | منخفضة (Low) | متوسطة (Medium) | مرتفعة (High) |
| **الاحتمالية (Likelihood): منخفضة (Low)** | ملاحظة (Note) | منخفضة (Low) | متوسطة (Medium) |

تأتي هذه الشبكة من **منهجية OWASP لتقييم المخاطر (OWASP Risk Rating Methodology)**، وهي طريقةٌ شائعة لتقييم الملاحظات الخاصة بالتطبيقات (application-specific findings)، مثل عيوب التصميم (design flaws) وأخطاء التحكم في الوصول (access-control bugs)، التي ليس لها معرّف CVE. وهي تمنح العوامل (factors) درجاتٍ من 0 إلى 9: ثمانية عوامل **للاحتمالية (likelihood)** تخص المهاجم والعيب (the attacker and the flaw)، مثل مستوى المهارة (skill level) والدافع (motive) وسهولة الاكتشاف (ease of discovery)؛ وعوامل **للأثر (impact)** إما تقنية (technical)، أي فقدان السرية (confidentiality) أو السلامة (integrity) أو التوافر (availability) أو المساءلة (accountability)، وإما تجارية (business)، أي مالية (financial) أو متعلقة بالسمعة (reputation) أو بعدم الامتثال (non-compliance) أو بالخصوصية (privacy). احسب متوسط كل مجموعة (average each set): من 0 إلى أقل من 3 منخفض (Low)، ومن 3 إلى أقل من 6 متوسط (Medium)، ومن 6 إلى 9 مرتفع (High). وحيث تعرف الأثر التجاري (business impact)، تنص المنهجية على استخدامه بدلًا من الأثر التقني (technical impact).

**CVE وCWE.** يسمّي معرّف **CVE** (Common Vulnerabilities and Exposures) ثغرةً واحدة معروفة علنًا (publicly known vulnerability) في منتجٍ محدد (specific product)، مثل CVE-2021-44228، أي Log4Shell. ويسمّي مُدخل **CWE** (Common Weakness Enumeration) *نوعًا* من العيوب (a *type* of flaw). ليس لخطأ بوابة الشركات الصغيرة (SME Portal) معرّف CVE لأنه في شيفرة بنك نجم نفسه (Najm's own code)، لكن له مُدخل CWE: هو CWE-639، «تجاوز التفويض عبر مفتاحٍ يتحكم فيه المستخدم» ("Authorization Bypass Through User-Controlled Key").

**CVSS.** يقدّم **نظام تقييم الثغرات الشائع (Common Vulnerability Scoring System)** درجة خطورةٍ (severity score) معيارية ومحايدة تجاه المورّدين (standard, vendor-neutral)، تكون عادةً لمعرّف CVE منشور (published CVE). وتتولى صيانته FIRST، أي منتدى فرق الاستجابة للحوادث والأمن (Forum of Incident Response and Security Teams). تجيب الدرجة الأساسية (base score) عن هذا السؤال: بصرف النظر عن نشر أي مؤسسةٍ بعينها (any one organisation's deployment)، وبافتراض أسوأ حالةٍ معقولة (reasonable worst case)، ما مدى سوء هذه الثغرة تقنيًا (technically)؟ ويستخدم الإصداران 3.1 و4.0 النطاقات نفسها (same bands): **منخفضة (Low)** 0.1–3.9، و**متوسطة (Medium)** 4.0–6.9، و**مرتفعة (High)** 7.0–8.9، و**حرجة (Critical)** 9.0–10.0، أما 0.0 فتعني لا شيء (None).

تأتي الدرجة مع **سلسلة متجه (vector string)** تسرد قيم المقاييس (metric values)، والمتجه يخبرك أكثر مما يخبرك الرقم (tells you more than the number). وهذا هو خطأ الشبكة الكلاسيكي في أسوأ حالاته (classic worst-case network bug) في CVSS v3.1:

```text
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H      base score 9.8 (Critical)
AV:N  attack vector: network          AC:L  attack complexity: low
PR:N  privileges required: none       UI:N  user interaction: none
S:U   scope: unchanged                C, I, A:H  high impact on confidentiality, integrity, availability
```

اقرأه جملةً (Read it as a sentence): «يمكن الوصول إليه عبر الشبكة (reachable over the network)، وهو سهل، ولا يحتاج إلى حساب (no account) ولا إلى أي فعلٍ من الضحية (no action by a victim)، ويتيح للمهاجم قراءة كل ما يعالجه المكوّن أو تغييره أو تعطيله (read, change or disrupt everything the component handles).» وقد سجّلت Log4Shell الدرجة 10.0 لأن متجهها وسم النطاق (scope) أيضًا بأنه متغيّر (changed): أي أن الضرر يمتد إلى ما وراء المكوّن المعرَّض (beyond the vulnerable component).

وهذا خطأ فواتير بوابة الشركات الصغيرة (SME Portal invoice bug)، مقيَّمًا بالطريقة نفسها:

```text
CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N      base score 6.5 (Medium)
```

إنه «متوسط» ("Medium") فقط، لأنه يحتاج إلى تسجيل دخول (needs a login)، أي PR:L، ويقتصر على قراءة البيانات (only reads data). لكن بالنسبة لبنكٍ يأتمنه عملاؤه من الشركات (business customers) على فواتيرهم (trust it with their invoices)، فهو من أخطر الملاحظات في القائمة (one of the most serious findings on the list). وتلك الفجوة هي الدرس: **CVSS يقيّم الخطأ، وعليك أنت أن تقيّم المخاطر (CVSS rates the bug; you must rate the risk).**

**أدلة الاستغلال (Exploitation evidence).**
- يسرد **كتالوج CISA KEV**، الذي بدأ عام 2021، الثغراتِ التي تتوافر أدلةٌ موثوقة على استغلالها في الواقع (reliable evidence of exploitation in the wild). ويجب على الوكالات المدنية الفيدرالية الأمريكية (US federal civilian agencies) إصلاح البنود المدرجة ضمن مواعيد نهائية (deadlines) تحددها توجيهات CISA (CISA directives)، علمًا بأن التوجيه BOD 26-04 حلّ في يونيو 2026 محل التوجيه الأصلي BOD 22-01، بمواعيد نهائية تزن أيضًا التعرّض (exposure) والأتمتة (automation) والأثر التقني (technical impact)، فتحقّق من النص الحالي (check the current text)؛ أما سائر الجهات (everyone else) فيمكنها استخدامه قائمةً مجانية بعنوان «أصلِح هذا أولًا» ("fix this first").
- يمنح **EPSS**، أي نظام التنبؤ بتقييم الاستغلال (Exploit Prediction Scoring System) الصادر أيضًا عن FIRST، كل معرّف CVE احتمالًا يُحدَّث يوميًا (daily-updated probability)، من 0 إلى 1، لرصد نشاط استغلال (exploitation activity will be observed) خلال الأيام الثلاثين التالية (in the next 30 days). ومعظم معرّفات CVE تسجّل درجاتٍ منخفضة جدًا (score very low).

يسأل CVSS: «ما مدى السوء إن استُغلت؟» ⁦("how bad if exploited?")⁩. ويسأل EPSS: «ما مدى احتمال استغلالها قريبًا؟» ⁦("how likely to be exploited soon?")⁩. ويقول KEV: «مستغلةٌ بالفعل» ("already exploited").

**ما تفعله بالمخاطر (What you do with a risk).** **خفّفها (Mitigate)** بإصلاحها أو بإضافة ضابط (add a control)، أو **تجنّبها (avoid)** بإزالة الميزة (remove the feature)، أو **انقلها (transfer)** بعقدٍ أو تأمين (contract or insurance)، أو **اقبلها (accept)** عن وعي (consciously)، مع مالك أعمالٍ مسمّى (named business owner)، وسببٍ (reason)، وتاريخ انتهاء (expiry date). وعبارة «لم نصل إليها» ("We didn't get to it") ليست قبولًا (not acceptance).

### 🟡 التعمق أكثر (Going deeper)

**تقييم ملاحظةٍ لا CVE لها (Rating a finding with no CVE).** يقيّم علي خطأ فواتير بوابة الشركات الصغيرة (SME Portal) بمنهجية OWASP (OWASP method):
- **الاحتمالية (Likelihood):** مستوى المهارة (skill level) 3، أي «بعض المهارات التقنية» ("some technical skills") بما يكفي لتعديل رقمٍ في الرابط (URL)؛ والدافع (motive) 4؛ والفرصة (opportunity) 7، إذ يكفي أي حسابٍ في بوابة الشركات الصغيرة (any SME Portal account)؛ والحجم (size) 6، أي جميع المستخدمين المصادَق عليهم (all authenticated users)؛ وسهولة الاكتشاف (ease of discovery) 7؛ وسهولة الاستغلال (ease of exploit) 5؛ والوعي (awareness) 4، فهي ليست علنيةً بعد (not yet public)؛ ورصد التسلل (intrusion detection) 8، إذ تُسجَّل ولا تُراجَع (logged, not reviewed). المتوسط 5.5: **متوسطة (Medium)**.
- **الأثر التجاري (Business impact):** الضرر المالي (financial damage) 3، والضرر بالسمعة (reputation damage) 5، وعدم الامتثال (non-compliance) 5، إذ هو خرقٌ لحماية البيانات (data-protection breach)؛ وانتهاك الخصوصية (privacy violation) 7، إذ تَرِد أسماء آلاف الأشخاص في الفواتير (thousands of people named on invoices). المتوسط 5.0: **متوسط (Medium)**.

الاحتمالية المتوسطة والأثر المتوسط (Medium likelihood and Medium impact) يعطيان **متوسطة (Medium)**. لكن نورة تعترض (Noura objects): لقد دفن حساب المتوسط (averaging) عامل الخصوصية (privacy factor). والمنهجية تدعو المؤسسات إلى تكييفها (tailor it)، مثلًا بإضافة عوامل أو بترجيح (weighting) أهمها للعمل، لذا يضيف بنك نجم قاعدة حدٍّ أدنى (floor rule) خاصةً به: *إذا سجّل انتهاك الخصوصية (privacy violation) أو عدم الامتثال (non-compliance) 7 أو أكثر لبيانات العملاء، فالأثر مرتفع (impact is High).* والاحتمالية المتوسطة مع الأثر المرتفع تعطيان **مرتفعة (High)**، فيدخل الإصلاح في السباق الحالي (current sprint).

**CVSS v4.0.** نشرت FIRST الإصدار 4.0 في نوفمبر 2023. التغييرات الرئيسية (main changes):
- أربع مجموعات مقاييس (four metric groups): **الأساسية (Base)**، و**التهديد (Threat)** أي نضج الاستغلال (exploit maturity)، و**البيئية (Environmental)** أي متطلباتك ونشرك (your requirements and deployment)، و**التكميلية (Supplemental)** أي معلوماتٌ إضافية، مثل السلامة (Safety)، لا تغيّر الدرجة (does not change the score).
- تسمياتٌ (labels) تبيّن ما دخل في الدرجة (what went into a score): **CVSS-B** للأساسية فقط (base only)، و**CVSS-BT**، و**CVSS-BE**، و**CVSS-BTE**. والدرجات المنشورة (published scores) تكون عادةً CVSS-B.
- مقياسٌ أساسي جديد (new base metric) هو **متطلبات الهجوم (Attack Requirements)**، أي AT؛ وحلّت محلّ **النطاق (Scope)** آثارٌ منفصلة (separate impacts) على **النظام المعرَّض (vulnerable system)**، أي VC وVI وVA، وعلى **الأنظمة اللاحقة (subsequent systems)**، أي SC وSI وSA.

```text
CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N      CVSS-B 9.3 (Critical)
```

استخدم الحاسبة الرسمية (official calculator) من FIRST، وسجّل الإصدار دائمًا (always record the version): فدرجة 9.8 في v3.1 ودرجة 9.3 في v4.0 قد تصفان العيب نفسه (the same flaw). والمقاييس **البيئية (Environmental)** هي حيث يلتقي CVSS بمخاطرك (where CVSS meets your risk)، مثل «لا يمكن الوصول إليها إلا داخليًا» ("only reachable internally")؛ ومعظم الفرق تطبّق هذه الفكرة عبر فئات الأصول (asset tiers) بدلًا من ذلك.

**قاعدةٌ لترتيب الأولويات (A prioritisation rule).** قارن فرزًا يعتمد على CVSS وحده (CVSS-only sort) بفرزٍ يستخدم أدلة الاستغلال والسياق (exploitation evidence and context):

```python
# NAIVE: severity only
backlog.sort(key=lambda f: f.cvss_base, reverse=True)
```

```python
# BETTER: exploitation evidence, exposure and asset value, then severity (thresholds illustrative)
def priority(f) -> str:
    exploited = f.cve in kev_catalogue or f.seen_by_soc
    important = f.asset.internet_facing or f.asset.tier == 1   # tier 1: customer data or money movement
    severe = f.cvss_base >= 7.0 or f.owasp_risk in ("High", "Critical")
    if exploited:
        return "P1" if important else "P2"
    if severe and (important or f.epss >= 0.1):                 # epss is 0.0 for findings with no CVE
        return "P2"
    if f.cvss_base >= 4.0 or f.owasp_risk == "Medium" or f.asset.tier == 1:
        return "P3"
    return "P4"
```

والمنطق نفسه في صورة مسار قرار (decision flow):

```mermaid
flowchart TD
    A["ملاحظة جديدة<br/>(New finding)"] --> B{"مستغلة معروفًا: كتالوج الثغرات المستغلة أو أدلة مركز العمليات الأمنية<br/>(Known exploited: KEV or SOC evidence)"}
    B -->|"نعم (Yes)"| C{"أصل مكشوف على الإنترنت أو من الفئة الأولى<br/>(Internet-facing or tier 1 asset)"}
    C -->|"نعم (Yes)"| P1["الأولوية 1: التخفيف خلال 72 ساعة<br/>(P1: mitigate within 72 hours)"]
    C -->|"لا (No)"| P2["الأولوية 2: التخفيف خلال 14 يومًا<br/>(P2: mitigate within 14 days)"]
    B -->|"لا (No)"| D{"خطيرة، ومكشوفة أو من الفئة الأولى أو باحتمال استغلال مرتفع<br/>(Severe, and exposed, tier 1 or high EPSS)"}
    D -->|"نعم (Yes)"| P2
    D -->|"لا (No)"| E{"خطورة متوسطة أو الفئة الأولى<br/>(Medium severity or tier 1)"}
    E -->|"نعم (Yes)"| P3["الأولوية 3: الإصلاح خلال 60 يومًا<br/>(P3: fix within 60 days)"]
    E -->|"لا (No)"| P4["الأولوية 4: الإصدار المخطط التالي<br/>(P4: next planned release)"]
```

يحاكي هذا **SSVC**، أي تصنيف الثغرات الخاص بأصحاب المصلحة (Stakeholder-Specific Vulnerability Categorization)، الصادر عن مركز تنسيق CERT (CERT Coordination Center) في جامعة كارنيغي ميلون (Carnegie Mellon) والذي كيّفته CISA: فبدلًا من رقم، يستخدم شجرة قرار (decision tree) تقوم على حالة الاستغلال (exploitation status)، والأثر التقني (technical impact)، وقابلية الأتمتة (automatability)، والأثر على المهمة والرفاه (mission and well-being impact)، وتنتهي بإحدى النتائج: المتابعة (Track)، أو المتابعة المشدّدة (Track*)، أو الانتباه (Attend)، أو التصرّف (Act).

### 🔴 نظرة الخبير (Expert view)

**لمصفوفات المخاطر عيوبٌ معروفة (Risk matrices have known flaws).** بيّنت ورقة توني كوكس (Tony Cox) عام 2008، «ما الخطأ في مصفوفات المخاطر؟» ⁦("What's Wrong with Risk Matrices?")⁩، أن المصفوفات قد ترتّب المخاطر ترتيبًا غير متسق (rank risks inconsistently)، لأنها تضغط القيم المتصلة (continuous values) في عددٍ قليل من الخانات (a few bins). استخدمها لبدء النقاشات وفرز القوائم الطويلة (start conversations and sort long lists)، لا أداةً للقياس الدقيق (precise measurement).

**المخاطر الكمية (Quantitative risk).** في القرارات المكلفة (expensive decisions)، قدّر نطاقاتٍ (estimate ranges). يُنمذج **FAIR**، أي تحليل عوامل مخاطر المعلومات (Factor Analysis of Information Risk) المنشور معاييرَ لدى The Open Group، المخاطرَ على أنها معدل تكرار أحداث الخسارة (how often loss events happen) مضروبًا في حجمها (how large they are)، مجمَّعةً بالمحاكاة (combined by simulation). ومخرجاته، مثل «احتمال 1 من 10 سنويًا لخسائر تتجاوز مبلغًا محددًا» ("a 1-in-10 chance per year of losses above a stated amount")، تتحدث بلغة مجلس إدارة حمد (Hamad's board)، وبلغة القواعد والجهات الرقابية (rules and supervisors) التي تتوقع إدارةً موثّقة لمخاطر تقنية المعلومات والاتصالات (documented ICT risk management)، مثل لائحة DORA الأوروبية لأعمال بنك نجم في أوروبا، ومصرف قطر المركزي (QCB) في الداخل، كما في الدرس 11.2. والخطر هو الدقة الزائفة (false precision): تخميناتٌ تدخل، وتخميناتٌ تبدو واثقة تخرج (guesses in, confident-looking guesses out).

**لم يُصمَّم CVSS لملاحظات الذكاء الاصطناعي (CVSS was not designed for AI findings).** نادرًا ما يكون لمسار حقن موجّهات (prompt-injection path) في نجم أسيست (Najm Assist) أو لخطر تسميمٍ (poisoning risk) في التنبيهات الذكية (Smart Alerts) معرّف CVE، وخطورته تعتمد على ما يُسمح للنظام بفعله (what the system may do). قيّمه بالعاقبة (by consequence): *ما الذي يستطيع مهاجمٌ يتحكم في مخرجات النموذج أن يجعل أدواتنا تفعله؟* ⁦(what can an attacker who controls the model's output make our tools do?)⁩ فالحقن نفسه (the same injection) مجرد إزعاج (nuisance) في روبوت محادثةٍ لأسئلة الرسوم (fee-questions chatbot)، وأولويةٌ من الفئة P1 في وكيلٍ يستطيع تحريك الأموال (agent that can move money). لذا فإن قاعدة التصميم (design rule) من الدرس 1.2 تضع أيضًا سقفًا لتقييم المخاطر (caps the risk rating).

**مصادر البيانات مدخلات، لا عرّافات (Feeds are inputs, not oracles).** قد تتأخر سجلات CVE أو تكون ناقصة (late or incomplete)؛ ففي عام 2024، أعلنت قاعدة البيانات الوطنية للثغرات (National Vulnerability Database) التابعة لـNIST علنًا عن تراكمٍ متزايد (growing backlog) في إثراء (enriching) معرّفات CVE الجديدة. استخدم مصادر متعددة (several sources) وسجّل المصدر الذي اعتمد عليه كل قرار (which one each decision relied on).

**قِس البرنامج، لا الكومة (Measure the programme, not the pile).** يكبر حجم قائمة الأعمال المتراكمة (backlog size) مع كل ماسحٍ جديد (new scanner). تتبّع زمن المعالجة (time to remediate) حسب الأولوية مقارنةً بالموعد النهائي (against the deadline)، وحالات قبول المخاطر المنتهية (expired risk acceptances). ويبني الدرس 10.3 عملية إدارة الثغرات الكاملة (full vulnerability-management process).

## 🧰 الأدوات (The toolkit)
| الضابط أو المعيار أو الأداة (Control, standard or tool) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |
|---|---|---|
| **CVSS** — من FIRST، بالإصدارين v4.0 وv3.1 | درجة خطورةٍ تقنية معيارية من 0 إلى 10 (standard 0–10 technical severity score) مع سلسلة متجه (vector string) | توصيل خطورة الثغرات المعروفة ومقارنتها (communicating and comparing the severity of known vulnerabilities) |
| **EPSS** — من FIRST | احتمالٌ يومي (daily probability) لأن يشهد معرّف CVE نشاط استغلال (exploitation activity) خلال الأيام الثلاثين التالية | ترتيب قوائم CVE المتراكمة الكبيرة (large CVE backlogs) حسب الاحتمالية (by likelihood) |
| **CISA KEV catalogue** — كتالوج الثغرات المستغلة المعروفة | قائمةٌ بالثغرات التي تتوافر أدلةٌ على استغلالها في الواقع (evidence of exploitation in the wild) | المرشّح الأول لـ«أصلِح الآن» ("fix now")، لا سيما على الأصول المكشوفة (exposed assets) |
| **SSVC** — من CERT/CC وCISA | شجرة قرار (decision tree) تنطلق من الاستغلال والأثر والمهمة (exploitation, impact and mission) إلى المتابعة (Track) أو الانتباه (Attend) أو التصرّف (Act) | تحويل إشاراتٍ كثيرة (many signals) إلى إجراءٍ متسق (consistent action) |
| **OWASP Risk Rating Methodology** — منهجية OWASP لتقييم المخاطر | عوامل الاحتمالية والأثر (likelihood and impact factors) تُقيَّم من 0 إلى 9 وتُجمع في مصفوفة (combined in a matrix) | الملاحظات التي لا CVE لها (findings with no CVE): عيوب التصميم (design flaws)، والتحكم في الوصول (access control)، والأخطاء المنطقية (logic bugs) |
| **Risk register** — سجل المخاطر | كل خطرٍ مع تقييمه (rating)، ومعالجته (treatment)، ومالكه (owner)، وتاريخ مراجعته (review date) | تتبّع المخاطر المفتوحة والمقبولة (open and accepted risks) للقادة والمدققين (leaders and auditors) |
| **FAIR** — من The Open Group | نموذجٌ كمي (quantitative model) لتكرار الخسارة وحجمها (loss frequency and size)، في صورة نطاقات (as ranges) | القرارات المكلفة (expensive decisions)؛ وتقارير مجلس الإدارة بلغة المال (board reporting in money) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
تنشر نورة وجاسم **معيار ترتيب أولويات الثغرات في بنك نجم، الإصدار 1 (Najm Vulnerability Prioritisation Standard v1)**. يعتمده حمد، ويربطه فريق الحوكمة (governance team) لدى ليلى بالالتزامات التنظيمية (regulatory obligations). إنه نسخةٌ أولى (first cut): يدمجه الدرس 10.3 في معيار إدارة الثغرات الكامل (full Vulnerability Management Standard) للبنك، الذي يضيف فئة أولويةٍ P0 (P0 tier)، ويراجع المواعيد النهائية (revises the deadlines)، ويضيف قواعد الإفصاح (disclosure rules).

**الجزء A: الأولويات والمواعيد النهائية (Part A: priorities and deadlines)**، وهي للتوضيح فقط (illustrative): حدّد مواعيدك وفق شهيتك للمخاطر (risk appetite) وتوقعات الجهات الرقابية لديك (your regulators' expectations).

| الأولوية (Priority) | المعايير، ويكفي أحدها (Criteria, any one) | التخفيف خلال (Mitigate within) | الإصلاح خلال (Fixed within) | من يحق له قبول المخاطر (Who may accept the risk) |
|---|---|---|---|---|
| **P1** | مستغلةٌ معروفًا (known exploited) على أصلٍ مكشوف على الإنترنت (internet-facing) أو من الفئة 1 (tier 1)؛ أو دليلٌ على أن بيانات عميلٍ قد وصلت بالفعل إلى عميلٍ آخر (customer data has already reached another customer) | 72 ساعة | 14 يومًا | رئيس أمن المعلومات (CISO) فقط، مع ضوابط تعويضية مكتوبة (written compensating controls) |
| **P2** | مستغلةٌ معروفًا في مكانٍ آخر (known exploited elsewhere)؛ أو خطيرة (severe)، أي CVSS 7.0+ أو OWASP مرتفعة أو حرجة (High or Critical)، ومكشوفة (exposed) أو من الفئة 1 (tier 1) أو EPSS 0.1+ | 14 يومًا | 30 يومًا | مالك نظام الأعمال (business system owner) ونورة |
| **P3** | ليست P1 أو P2، وCVSS 4.0+ أو OWASP متوسطة (Medium) أو أعلى؛ أو أي ملاحظةٍ أخرى على أصلٍ من الفئة 1 (tier 1 asset) | — | 60 يومًا | مالك نظام الأعمال (business system owner) |
| **P4** | كل ما عدا ذلك (everything else) | — | الإصدار التالي (next release)؛ 180 يومًا كحدٍّ أقصى (at most) | قائد الهندسة (engineering lead) |

**الفئات (Tiers).** تحتفظ الفئة 1 (Tier 1) ببيانات العملاء أو تستطيع تحريك الأموال (move money): تطبيق نجم للهاتف (Najm Mobile) وواجهة البرمجة الخاصة به (its API)، وبوابة الشركات الصغيرة (SME Portal)، والنظام المصرفي الأساسي (core banking)، وأدوات نجم أسيست (Najm Assist's tools). وتحتفظ الفئة 2 (Tier 2) ببيانات البنك الحساسة (sensitive bank data): مساعد مذكرات الائتمان (Credit Memo Copilot)، والتنبيهات الذكية (Smart Alerts). والفئة 3 (Tier 3) هي البقية (the rest).

**الجزء B: القواعد (Part B: rules).** تُقيَّم الملاحظات التي لا CVE لها (findings with no CVE) بمنهجية OWASP (OWASP method) مضافًا إليها الحد الأدنى للخصوصية في بنك نجم (Najm's privacy floor). وتُقيَّم ملاحظات الذكاء الاصطناعي (AI findings) بأسوأ نتيجةٍ للأدوات (worst tool outcome) إذا تحكّم المهاجم بالنموذج. ويُدرَج كل قبولٍ (acceptance) في سجل المخاطر (risk register) مع مالك (owner) وسبب (reason) وضوابط تعويضية (compensating controls) وتاريخ انتهاء (expiry)، بحدٍّ أقصى قدره 90 يومًا لـP1 وP2، و12 شهرًا لـP3 وP4؛ وتُعاد فتح حالات القبول المنتهية تلقائيًا (expired acceptances reopen automatically). ويطّلع حمد على الأداء مقابل المواعيد النهائية (deadline performance) شهريًا.

**الجزء C: سجل قبول المخاطر، مثال (Part C: risk acceptance record, example)**

| الحقل (Field) | المثال (Example) |
|---|---|
| الملاحظة (Finding) | VULN-2026-0412: معرّف CVE في مكتبة PDF (PDF library) تستخدمها مهمة النشر الداخلية لجدول الرسوم (internal fee-schedule publishing job)؛ CVSS-B 9.3؛ غير مدرجةٍ في KEV (not in KEV)؛ احتمال EPSS منخفض (low EPSS) |
| لماذا لم تُصلَح في الوقت المحدد (Why not fixed in time) | يُفسد الإصدار المُصلَح (fixed version) تخطيط النص العربي (Arabic text layout)؛ ومن المقرر صدور إصدارٍ مختبَر (tested release) خلال 12 أسبوعًا، أي بعد الموعد النهائي البالغ 60 يومًا (past the 60-day deadline) |
| التعرّض والضوابط (Exposure and controls) | لا مستمِع شبكي (no network listener)؛ الفئة 3 (tier 3)؛ حاويةٌ معزولة (isolated container) بلا وصولٍ صادر إلى الإنترنت (no outbound internet)؛ تقبل الملفات الموقَّعة (signed files) من فريق المنتج فقط |
| الأولوية، والمالك، والمعتمِد، وتاريخ الانتهاء (Priority, owner, approver, expiry) | P3؛ طارق؛ مالك أعمال منتجات التجزئة (Retail Products business owner)؛ 2027-01-15 |

## 🛠️ التمارين (Exercises)
- 🟢 اكتب كل متجهٍ (vector) جملةً واضحة واحدة (one plain sentence) مع نطاق خطورته (severity band): `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` (9.8) و`CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` (7.8). وقل أيهما أكثر إلحاحًا (more urgent) على خادم ويبٍ عام (public web server)، وأيهما أكثر إلحاحًا على مشغّل تكاملٍ مستمر مشترك (shared CI runner) تشغّل فيه خطوط أنابيب (pipelines) كثيرٍ من المطورين شيفرتها. *يكتمل عندما (Done when):* تذكر كل جملةٍ من أين يعمل المهاجم (where the attacker works from)، وما الوصول الذي يحتاجه (what access they need)، وما الذي يحصل عليه (what they get)، وتستطيع أن تشرح لماذا لا يعني «محلي» ("local") «آمن» ("safe") على جهازٍ مشترك (shared machine).
- 🟡 أجرِ تدقيقًا للاعتماديات (dependency audit) على مشروعٍ تملكه (a project you own)، مثلًا باستخدام `npm audit` أو `pip-audit` أو OWASP Dependency-Check. ولأعلى 15 ملاحظة حسب CVSS (top 15 findings by CVSS)، تحقّق من KEV وEPSS، وقرّر ما إذا كانت الشيفرة المعرَّضة قابلةً للوصول (vulnerable code is reachable)، وأعد الترتيب (re-rank) بقاعدة هذا الدرس. *يكتمل عندما (Done when):* يكون لديك جدولٌ بالترتيب القديم (old rank) والترتيب الجديد (new rank) وسببٍ من سطرٍ واحد (one-line reason)، وإما أن تكون ملاحظةٌ واحدة قد تحركت خمسة مراكز أو أكثر، وإما أن تكون قد دوّنت سبب عدم حدوث ذلك.
- 🔴 خذ ملاحظةً لا CVE لها (finding with no CVE) من تطبيقك، أو من OWASP Juice Shop يعمل محليًا (running locally). قيّمها بمنهجية OWASP (OWASP method)، واحسب درجتها بـCVSS v4.0 في حاسبة FIRST (FIRST's calculator)، واكتب مذكرةً من صفحةٍ واحدة (one-page note) عن سبب اختلاف النتيجتين وأيهما ينبغي أن يقود الأولوية (drive priority). *يكتمل عندما (Done when):* تسمّي المذكرة العامل المسبّب للاختلاف (factor behind the difference) وتنتهي بمُدخلٍ في سجل المخاطر (risk-register entry): المالك (owner)، والمعالجة (treatment)، وتاريخ المراجعة (review date).

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **معاملة CVSS على أنه المخاطر (Treating CVSS as risk).** تقيّم الدرجة الأساسية لـCVSS (CVSS base score) الخطورة (severity) بمعزلٍ عن نشرك (independent of your deployment). أضف أدلة الاستغلال والسياق (exploitation evidence and context) قبل تحديد الأولوية.
- **تجاهل الملاحظات التي لا CVE لها (Ignoring findings without a CVE).** أخطاء التحكم في الوصول والأخطاء المنطقية (access-control and logic bugs) الخاصة بك لا تظهر أبدًا في مصادر البيانات (feeds). قيّمها بمنهجية OWASP (OWASP method)، في الطابور نفسه (same queue).
- **متوسطاتٌ تخفي أسوأ عامل (Averages that hide the worst factor).** قد يصل خرقٌ لحماية البيانات (data-protection breach) عند حساب المتوسط إلى «متوسط» ("Medium"). دع العوامل الحرجة (critical factors) تضع حدًّا أدنى (set a floor).
- **قبول المخاطر بالصمت (Risk acceptance by silence).** الملاحظة المتأخرة (overdue finding) ليست مقبولة. القبول يحتاج إلى مالك (owner)، وسبب (reason)، وضوابط تعويضية (compensating controls)، وتاريخ انتهاء (expiry).
- **الخلط بين إصدارات CVSS (Mixing CVSS versions).** سجّل الإصدار (record the version) واستخدم الحاسبة الرسمية (official calculator).

## 🧾 الخلاصة (Recap)
- تجمع المخاطر (Risk) بين الاحتمالية والأثر (likelihood and impact)؛ وترتيب الأولويات (prioritising) يعني اختيار ما يُصلَح أولًا (what to fix first).
- يقيس CVSS، بإصداره 4.0 منذ نوفمبر 2023 وإصداره 3.1 الذي ما زال شائعًا، الخطورة التقنية (technical severity)، لا مخاطرك (not your risk). اقرأ المتجه، لا الرقم وحده (read the vector, not just the number).
- يضيف KEV، أي ما استُغل بالفعل (already exploited)، وEPSS، أي ما يُرجَّح استغلاله قريبًا (likely to be exploited soon)، عنصرَ الاحتمالية (likelihood)؛ ويضيف تعرّض الأصل وقيمته (asset exposure and value) السياقَ (context).
- قيّم الملاحظات التي لا CVE لها (findings without a CVE)، بما فيها ملاحظات الذكاء الاصطناعي (AI findings)، بمنهجية OWASP (OWASP method) أو بالعاقبة في أسوأ الحالات (worst-case consequence) ضمن معماريتك (your architecture).
- عالج كل خطرٍ عن قصد (treat every risk deliberately): خفّفه أو تجنّبه أو انقله أو اقبله (mitigate, avoid, transfer or accept)، وامنح كل قبولٍ مالكًا وتاريخ انتهاء (an owner and an expiry).

## ✍️ اختبر نفسك (Check yourself)

**1. في قائمة علي المتراكمة (backlog) ثغرةٌ بدرجة CVSS 9.8 في مكتبةٍ لا تستخدمها إلا مهمةٌ دفعية داخلية (internal batch job) بلا مستمِعٍ شبكي (network listener)، وثغرةٌ بدرجة CVSS 7.5 في جهاز VPN المكشوف على الإنترنت (internet-facing VPN appliance) المدرج في كتالوج KEV من CISA (CISA's KEV catalogue). أيهما يأتي أولًا، ولماذا؟**

- A. ثغرة 9.8، لأن درجتها أعلى (higher score)
- B. كلتاهما معًا (both at once)، لأن كلتيهما فوق 7.0
- C. ثغرة 7.5، لأنها معروفٌ أنها مستغلة (known to be exploited) وتقع على أصلٍ مكشوف (exposed asset)
- D. لا هذه ولا تلك (neither)، حتى تتوافر درجات EPSS (EPSS scores)

<details><summary>الإجابة</summary>

**C.** الاستغلال المعروف (known exploitation) على أصلٍ مكشوف على الإنترنت (internet-facing asset) يتقدم على درجةٍ أعلى في مكوّنٍ لا يستطيع أحدٌ الوصول إليه (component nobody can reach). يعامل الخيار A الخطورة على أنها مخاطر (treats severity as risk)؛ وينتظر D تنبؤًا (prediction) بينما يُظهر KEV الاستغلال فعلًا. انظر: 🟢 الأساسيات (The essentials)؛ 🟡 التعمق أكثر (Going deeper).

</details>

**2. يسأل حمد لماذا يُصنَّف خطأ بوابة الشركات الصغيرة (SME Portal) الذي يتيح لشركةٍ قراءة فواتير شركةٍ أخرى (lets one company read another company's invoices) «متوسطًا» ("Medium") فقط، بدرجة CVSS 6.5. ما أفضل تفسير (best explanation)؟**

- A. الدرجة خاطئة (the score is wrong) وينبغي تغييرها يدويًا (by hand) إلى 9.0
- B. يقيّم CVSS الخطورة التقنية (technical severity) بمعزلٍ عن أي نشرٍ بعينه (any one deployment)، لا المخاطر على بنك نجم (risk to Najm)؛ ومع احتساب الأثر التجاري والتعرّض (business impact and exposure)، فهي مخاطر ذات أولويةٍ عالية (high-priority risk)
- C. الملاحظات المتوسطة (Medium findings) لا تحتاج إلى إصلاح
- D. لا يمكن تقييم الأخطاء التي لا CVE لها (bugs without a CVE cannot be rated)

<details><summary>الإجابة</summary>

**B.** المتجه صحيح (the vector is right)، لكن CVSS يقيس الخطورة لا المخاطر (severity, not risk)، والحد الأدنى للخصوصية في بنك نجم (Najm's privacy floor) يجعلها مرتفعة (High). وتعديل الدرجة الأساسية (editing the base score)، أي الخيار A، يخفي المنطق (hides the reasoning)؛ وD خاطئ، لأن منهجية OWASP (OWASP method) موجودةٌ لهذه الملاحظات تحديدًا. انظر: 🟢 الأساسيات (The essentials)؛ 🟡 التعمق أكثر (Going deeper).

</details>

**3. باستخدام منهجية OWASP لتقييم المخاطر (OWASP Risk Rating Methodology)، يبلغ متوسط عوامل الاحتمالية (likelihood factors) لملاحظةٍ ما 6.25، ومتوسط عوامل الأثر التجاري (business impact factors) 4.5. ما الخطورة الإجمالية (overall severity)؟**

- A. منخفضة (Low)
- B. متوسطة (Medium)
- C. مرتفعة (High)
- D. حرجة (Critical)

<details><summary>الإجابة</summary>

**C.** الدرجة 6.25 احتماليةٌ مرتفعة (High likelihood) لأنها بين 6 و9؛ والدرجة 4.5 أثرٌ متوسط (Medium impact) لأنها من 3 إلى أقل من 6. والاحتمالية المرتفعة مع الأثر المتوسط تعطيان مرتفعة (High). أما حرجة (Critical)، أي الخيار D، فتحتاج إلى أن يكون كلاهما مرتفعًا (both to be High). انظر: 🟢 الأساسيات (The essentials).

</details>

**4. أي مصدرٍ صُمّم للإجابة (designed to answer) عن سؤال «ما مدى احتمال أن يشهد هذا المعرّف CVE نشاط استغلالٍ خلال الأيام الثلاثين التالية؟» ⁦("how likely is it that this CVE will see exploitation activity in the next 30 days?")⁩**

- A. EPSS
- B. الدرجة الأساسية لـCVSS (CVSS base score)
- C. CWE
- D. كتالوج KEV من CISA (CISA KEV catalogue)

<details><summary>الإجابة</summary>

**A.** يقدّم EPSS احتمالًا يُحدَّث يوميًا (daily-updated probability) لنشاط الاستغلال (exploitation activity) خلال 30 يومًا. أما CVSS (B) فيقيس الخطورة (severity)، ويسمّي CWE (C) نوع ضعف (weakness type)، ويسجّل KEV (D) الاستغلال الذي رُصد فعلًا (exploitation already seen) بدلًا من التنبؤ به (rather than predicting it). انظر: 🟢 الأساسيات (The essentials).

</details>

**5. لا يستطيع فريق طارق إصلاح ملاحظةٍ من الأولوية P2 (P2 finding) ضمن موعدها النهائي البالغ 30 يومًا (30-day deadline) لأن تصحيح المورّد (vendor's patch) يكسر تكاملًا حرجًا (critical integration). ما الذي يجعل قبول المخاطر صالحًا (valid risk acceptance) في بنك نجم؟**

- A. ترك الملاحظة مفتوحةً حتى يعمل التصحيح (until the patch works)
- B. تعليقٌ في التذكرة (ticket) يقول «مقبول» ("accepted")
- C. مُدخلٌ في سجل المخاطر (risk-register entry) يعتمده المالكون المناسبون (right owners)، مع السبب، والضوابط التعويضية (compensating controls)، وتاريخ انتهاءٍ لا يتجاوز 90 يومًا
- D. خفض درجة CVSS للملاحظة (lowering the finding's CVSS score) كي تصبح من الأولوية P3

<details><summary>الإجابة</summary>

**C.** القبول قرارٌ واعٍ ومسجَّل (conscious, recorded decision) يتخذه المالك المناسب (right owner)، مع ضوابط وتاريخ نهاية (end date). أما A فهو قبولٌ بالصمت (acceptance by silence)؛ وD يزوّر التقييم (falsifies the rating) بدلًا من معالجة المخاطر (treating the risk). انظر: 🟢 الأساسيات (The essentials)؛ 🏛️ عمليًا (In practice).

</details>

## 📚 المراجع (References)
- منظمة FIRST، نظام تقييم الثغرات الشائع (Common Vulnerability Scoring System) v4.0: المواصفة ودليل المستخدم والحاسبة (specification, user guide and calculator) — https://www.first.org/cvss/
- منظمة FIRST، وثيقة مواصفة CVSS v3.1 (CVSS v3.1 Specification Document) — https://www.first.org/cvss/v3.1/specification-document
- منظمة FIRST، نظام التنبؤ بتقييم الاستغلال (Exploit Prediction Scoring System, EPSS) — https://www.first.org/epss/
- وكالة CISA، كتالوج الثغرات المستغلة المعروفة (Known Exploited Vulnerabilities Catalog) — https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- مركز CERT/CC، تصنيف الثغرات الخاص بأصحاب المصلحة (Stakeholder-Specific Vulnerability Categorization, SSVC) — https://certcc.github.io/SSVC/
- منهجية OWASP لتقييم المخاطر (OWASP Risk Rating Methodology) — https://owasp.org/www-community/OWASP_Risk_Rating_Methodology
- قائمة MITRE CWE — https://cwe.mitre.org
- كوكس ⁦(Cox, L. A.)⁩ عام 2008، ورقة «ما الخطأ في مصفوفات المخاطر؟» ⁦("What's Wrong with Risk Matrices?")⁩، مجلة *Risk Analysis* 28(2)
- مجموعة The Open Group، معايير Open FAIR (Open FAIR standards) — https://www.opengroup.org
