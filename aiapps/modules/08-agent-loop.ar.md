# الوحدة 8 — حلقة الوكيل بإتقان

*خطِّط ونفِّذ ولاحِظ وكرِّر: هذا كل ما يفعله الوكيل، وفي الحلقة نفسها يخطئ الوكلاء. قدّمت لك الوحدة 1 أصغر حلقة وقدّمت الوحدة 3 بروتوكول الأدوات الذي تقوم عليه. وهذه الوحدة هي الفرق بين حلقة تنجح في عرض تجريبي وحلقة تستطيع تركها تعمل في الثانية صباحًا. الدرس 8.1 هو الدرس المفاهيمي: تشريح الحلقة وفق نمط ReAct، وطرق التوقف الست، وما يُفعل مع كل `stop_reason`، والتأمل الذاتي والتخطيط — متى يُجديان ومتى يضيفان كلفة فحسب — وأخطاء الأدوات، وكيف ينمو السياق مع الحساب، وأنماط الإخفاق التي يصادفها المبتدئون أولًا، وقابلية المراقبة التي تحتاجها الحلقة، ومتى تستخدم مشغّل الأدوات في حزمة التطوير أو Claude Agent SDK بدلًا من حلقتك الخاصة، وقائمة فحص الحلقة الآمنة. أما الدرس 8.2 فهو المختبر: حلقة من الصفر بحدّ صارم للخطوات، وميزانية رموز، وموعد نهائي بالساعة الفعلية، وكشف انعدام التقدم (no-progress detection)، وسجل تتبّع JSONL، وأداة إعادة تشغيل، وتسليم إلى شخص حين ينطلق أحد الحواجز، واختبار يجعل كل حاجز ينطلق. يعمل المختبر دون اتصال على المحاكي (mock) في عدّة المختبر وعلى واجهة البرمجة الحقيقية دون أي تغيير. وتحصل استعلامات التذاكر والزملاء في نجم ديسك على أول حواجزها.*

> **الطبقة:** Agents — الحلقة التي تتيح للنموذج أن يتصرف بنفسه، والحدود والفحوص وعمليات التسليم التي تُبقيه آمنًا.

---

# 8.1 — خطِّط ونفِّذ ولاحِظ وكرِّر: التأمل الذاتي وشروط التوقف وأولى أنماط الإخفاق
*المستوى: 🟡 متوسط* · *المتطلبات: 1.2، 3.2* · *الطبقة: Agents*

**بعد هذا الدرس تستطيع** أن تفحص حلقة وكيل بحثًا عن شروط التوقف الستة، وتحدّد حدّ الخطوات وميزانية الرموز من معادلة الرموز، مع جدول للتوقف. *مدة الدراسة: قراءة نحو 15 دقيقة، وعمل تطبيقي نحو 90 دقيقة (تقدير).*

## ⚡ الدرس في دقيقة
- **حلقة الوكيل (agent loop)** تسأل النموذج، وتقرأ `stop_reason`، وتنفّذ الأداة التي طلبها، وتعيد النتيجة، ثم تكرر (asks the model, reads stop_reason, runs the tool it asked for, returns the result and repeats; ReAct, Yao et al., 2022). النموذج يقترح؛ و**شيفرتك أنت تقرر متى تتوقف.**
- **ستة مخارج:** نجاح متحقَّق منه، وحدّ الخطوات (step cap)، وميزانية الرموز (token budget)، وموعد نهائي بالساعة الفعلية (wall-clock deadline)، وكشف انعدام التقدم، وتسليم إلى شخص. وكل حاجز ينتهي بتسليم لا بانهيار.
- عالِج **كل `stop_reason`**؛ وتوقف عند القيم المجهولة؛ ولا تنفّذ أي أداة من دور مقطوع أو مرفوض.
- تنمو كلفة الإدخال مع **مربّع عدد الخطوات**. قلّص نتائج الأدوات.
- **التأمل الذاتي (Reflection)** لا يُجدي إلا بمعلومة جديدة؛ و**التخطيط أولًا** يُجدي حين تكون الخطوات متوقعة.
- إشارة القرار: خطوات ثابتة فسير عمل — الدرس 5.1؛ ومسار تحدده نتائج الأدوات فحلقة محدودة.

## 🧭 لماذا يهم
في الأسبوع الخامس من التجربة التشغيلية لنجم ديسك ترتّب مها، قائدة فريق هندسة الموثوقية، محادثات الأسبوع الماضي بحسب الكلفة، وهذا افتراضي. إحداها خارج المألوف تمامًا: 50 استدعاءً للنموذج، وقرابة مليون رمز إدخال، أي نحو 75 ضعف المحادثة العادية. وكانت إجابتها صحيحة: «التذكرة 4471 قيد المعالجة.» لم يشتكِ أحد، فلم ينظر أحد. وحلقة لجين لم تسجّل إلا النص النهائي، فالسبب تخمين: كان TicketHub بطيئًا وظل النموذج يطلب التذكرة نفسها. وكان حدّ الخطوات عندها 50 «للاحتياط». وقد صمد الحدّ، وكان أغلى رقم في الملف.

يقول فهد: «حدّ الخمسين أمنية وُضع عليها رقم.» قبل أن تُطلَق أي حلقة تجيب على الورق عن أربعة أسئلة: كم من الوقت يجوز أن تعمل، وكم يجوز أن تنفق، وهل تتجه إلى مكان ما، ومن يتسلّم الأمر حين تتوقف؟ يقدّم هذا الدرس الحساب، ويبني الدرس 8.2 الحلقة.

## 📐 كيف يعمل

### 🟢 الأساسيات

**الحلقة (The loop).** تستدعي *حلقة الوكيل* النموذج مرة بعد مرة، وفي كل مرة تُرفق نتائج الطلب الذي صدر في الاستدعاء السابق، إلى أن يتحقق شرط التوقف. وقد سمّى Yao وزملاؤه (Yao et al., 2022) هذا النمط *ReAct*: يتناوب النموذج بين التفكير والفعل عبر الأدوات، ويقرأ *الملاحظة* التي ينتجها كل فعل. الدورة الواحدة هي **التخطيط** — أي تقرير الإجراء التالي، و**الفعل** — يُصدر النموذج `tool_use` وتنفّذه شيفرتك، و**الملاحظة** — يعود `tool_result`، و**التكرار**. وتُسمّى الدورة *خطوة*، وتسلسل الخطوات *مسار التنفيذ (trajectory)*، والشيفرة المحيطة بالنموذج *إطار التشغيل (harness)*.

```mermaid
flowchart TD
    G["الهدف والحدود<br/>(Goal and limits)"] --> C{"هل تجتاز الحواجز؟ الخطوات والرموز والوقت<br/>(Guards pass? steps, tokens, time)"}
    C -->|"لا (no)"| H["التسليم إلى شخص<br/>(Hand off to a person)"]
    C -->|"نعم (yes)"| M["استدعاء النموذج<br/>(Call the model)"]
    M --> R{"قراءة سبب التوقف<br/>(Read stop_reason)"}
    R -->|"نهاية الدور (end_turn)"| V{"هل تجتاز الإجابة الفحص؟<br/>(Answer passes the check?)"}
    V -->|"نعم (yes)"| D["تم<br/>(Done)"]
    V -->|"لا (no)"| H
    R -->|"طلب أداة (tool_use)"| N{"هل هو الاستدعاء نفسه كما قبل؟<br/>(Same call as before?)"}
    N -->|"نعم (yes)"| H
    N -->|"لا (no)"| T["تشغيل الأداة وتقليص النتيجة<br/>(Run the tool, trim the result)"]
    T --> O["الملاحظة: إلحاق النتيجة<br/>(Observe: append the result)"]
    O --> C
    R -->|"توقف الدور مؤقتًا (pause_turn)"| C
    R -->|"تجاوز حد الرموز أو رفض أو سبب مجهول (max_tokens, refusal, unknown)"| H
```

**تُنفَّذ الحواجز قبل كل استدعاء**، لأن الاستدعاء الخاطئ يكون ثمنه قد دُفع بالفعل، و**كل مسار عدا «تم» ينتهي عند تسليم إلى شخص**.

**ست طرق للتوقف.** الحلقة التي لا تملك سوى الأولى فاتورة بلا سقف.

| الشرط | السؤال | كيف تحدد حجمه |
|---|---|---|
| **النجاح** | هل تحقق الهدف؟ | `end_turn` **و** فحص في الشيفرة: معرّفات التذاكر الواردة في الهدف تظهر في الإجابة؛ ويجتاز JSON التحقق |
| **حدّ الخطوات** | كم استدعاءً للنموذج؟ | قاعدة عملية: من 1.5 إلى 2 ضعف عدد الخطوات عند المئين 95 في تشغيلات التقييم الناجحة |
| **ميزانية الرموز** | كم يجوز أن ينفق التشغيل الواحد؟ | الحساب أدناه؛ ويُفحص قبل كل استدعاء |
| **الموعد النهائي بالساعة الفعلية** | كم سينتظر الشخص؟ | وعد الواجهة، مضافًا إليه مهلة على كل استدعاء وكل أداة |
| **كشف انعدام التقدم** | هل تتجه إلى مكان ما؟ | الأداة نفسها بالمدخل نفسه مرتين؛ والخطأ نفسه مرتين |
| **التسليم (Hand-off)** | من يتسلّم الأمر؟ | طابور مسمّى وحزمة: الهدف وسبب التوقف وما جُرِّب |

الحدّ الذي لا ينطلق أبدًا لم يُختبر؛ والذي ينطلق في كثير من التشغيلات العادية حجمه خاطئ.

**كل `stop_reason`.** يمكن أن ينتهي الدور بخمس طرق:

| `stop_reason` | ما تفعله الحلقة |
|---|---|
| `end_turn` | اقرأ كتلة النص وشغّل الفحص. **النص الفارغ استسلام صامت: إخفاق.** |
| `tool_use` | نفّذ **كل** كتلة `tool_use`؛ وأجب في رسالة مستخدم **واحدة** |
| `max_tokens` | الرد مقطوع. **لا تنفّذ** آخر استدعاء أداة: فقد يكون مدخله نصف مكتوب. ارفع الحدّ أو سلّم إلى شخص |
| `refusal` | رفض مصنِّف أمان أو النموذج نفسه الإجابة. لا تعد إرساله دون تغيير؛ سجّل `stop_details` (`category` و`explanation`)؛ وقد يكون null؛ ولا تنفّذ أي أداة وسلّم إلى شخص |
| `pause_turn` | توقف دور أداة على الخادم مؤقتًا، كالبحث في الويب مثلًا. أعد إرسال المحادثة والدور الموقوف في آخرها؛ ويُحتسب خطوة |
| أي قيمة أخرى | توقف وسلّم إلى شخص. ويسرد نوع حزمة التطوير أيضًا `stop_sequence` — فقط إن ضبطتَ تسلسلات توقف — و`model_context_window_exceeded` — السياق ممتلئ، فاضغطه أو سلّم |

### 🟡 التعمق أكثر

**ينمو السياق وتنمو الكلفة أسرع.** يعيد كل استدعاء إرسال موجّه النظام وتعريفات الأدوات وكل دور سابق — الدرس 1.1. لنأخذ أحجامًا خيالية: *S* = 1,500 رمز لموجّه النظام والأدوات، و*g* = 100 للهدف، و*o* = 150 رمز إخراج في الخطوة، و*r* = عدد الرموز في كل نتيجة أداة. يقرأ الاستدعاء *n* ما مقداره *S* + *g* + (*n* − 1)(*o* + *r*)، فتقرأ *N* خطوة *N*(*S* + *g*) + (*o* + *r*)·*N*(*N* − 1)/2.

| الخطوات *N* | رموز الإدخال (Input tokens) عند *r* = 600 — مقلَّصة | رموز الإدخال عند *r* = 6,000 — خام |
|---|---|---|
| 4 | 10,900 | 43,300 |
| 10 | 49,750 | 292,750 |
| 20 | 174,500 | 1,200,500 |
| 50 | 998,750 | 7,613,750 |

تحقق من *N* = 10 و*r* = 600: 10 × 1,600 + 750 × 45 = 49,750. وبالأسعار التوضيحية الافتراضية في الدرس 1.1 — دولار واحد لكل مليون رمز إدخال و5 دولارات لكل مليون رمز إخراج؛ وليست سعر أي نموذج — يساوي ذلك 0.057 دولار، مقابل 0.300 دولار مع النتائج الخام: أي أكثر بنحو 5.2 مرة لعشر الخطوات نفسها. ومضاعفة الخطوات من 10 إلى 20 تضرب الإدخال في 3.5، ويكلّف التشغيل ذو الخمسين خطوة 1.04 دولار مقابل 0.014 دولار للتشغيل العادي ذي الأربع خطوات، أي نحو 75 ضعفًا. وتلك كانت محادثة مها.

**النتائج الكبيرة.** قلّص النتيجة *قبل* أن تدخل السجل: اقتطعها وقل ذلك صراحة مثل `[cut: 4,812 characters in all]`، أو أعِد حقولًا لا سجلات كاملة، أو لخِّصها بنموذج رخيص — وهو استدعاء مدفوع قد يُسقط التفصيل الأهم — أو أعِد معرّفًا للصفحة الثانية. ثم اترك السجل بحاله: ففي النماذج الحالية قد يُبطل تعديل الأدوار السابقة كتل التفكير فيها — خطأ 400 حيث يُفرض ذلك — ويُعيد بدء التخزين المؤقت للموجّه؛ ولمسح النتائج القديمة استخدم الإصدارات التجريبية على الخادم: تحرير السياق (context editing) والضغط (compaction). ويخفّض التخزين المؤقت (Caching) — الدرس 14.2 — سعر البادئة المُعاد إرسالها لا السياق ولا الخطوات.

**التأمل الذاتي والتصحيح الذاتي (Reflection and self-correction)** ثلاثة أمور مختلفة. (1) *تصحيح استدعاء أداة* انطلاقًا من `is_error`: رخيص، لذا ينبغي أن تقول الأخطاء ما هو الصالح — الدرس 3.1. (2) *فحص الإجابة بشيء خارج النموذج*: مخطط أو بحث عن استشهاد أو اختبار. (3) *أن تطلب من النموذج أن يفكر مرة أخرى دون أي جديد.* وقد استكشفت Self-Refine (Madaan et al., 2023) وReflexion (Shinn et al., 2023) النقد ثم المراجعة (critique-and-revise)؛ أما التصحيح الذاتي للاستدلال دون عون خارجي فلم يُجدِ بصورة موثوقة في دراسة لاحقة (Huang et al., 2023). **لا يستحق التأمل الذاتي كلفته إلا حين يأتي بمعلومة جديدة.** ضع له سقف جولة واحدة وقِسه — الدرس 12.1.

**التخطيط.** *التخطيط المتداخل* — أي ReAct — يقرر كل خطوة بعد آخر ملاحظة: يتكيّف، لكن المسار والكلفة يتفاوتان. أما *التخطيط ثم التنفيذ (Plan-then-execute)* فيكتب الخطوات أولًا وينفّذها بالترتيب ولا يعيد التخطيط إلا عند الإخفاق، مع سقف لإعادات التخطيط: فالكلفة متوقعة ويستطيع شخص اعتماد الخطة أولًا، لكنه هشّ حين يختلف الواقع عن الخطة. «أعد ضبط وصولي إلى VPN» له شكل ثابت: سير عمل — الدرس 5.1. و«لماذا ينقطع VPN عندي باستمرار؟» يتوقف على ما تعيده الأدوات: حلقة متداخلة بسقف. و«جهّز تسليم الأحد» يناسبه التخطيط ثم التنفيذ، فتقرأ يارا الخطة أولًا. ويخطط التفكير التكيفي (Adaptive thinking) داخل الاستدعاء أصلًا؛ فأضف استدعاء تخطيط فقط ليقرأه شخص.

**أخطاء الأدوات والتعافي منها.**

| الخطأ | من يتعافى | كيف |
|---|---|---|
| مدخل غير صالح من النموذج | النموذج | `is_error` يسمّي الصالح — ضعيف: `Error`؛ وقوي: `ticket_id must be four digits, like "4471"; you sent "ticket 4471"`؛ وحاجز انعدام التقدم يوقف التكرار |
| لا شيء موجود | لا أحد: إنها بيانات | `No ticket 9999 found` نتيجة عادية |
| عابر: انتهاء مهلة أو 503 | **شيفرتك** | أعِد المحاولة بتأخير أسي (backoff) وإزاحة عشوائية (jitter) ضمن الموعد النهائي؛ ثم قل «غير متاح، لا تعد المحاولة» |
| رفض الصلاحية | شخص | دون إعادة محاولة؛ وسلّم إلى شخص |
| فشل كتابة | شيفرتك | لا تكرار بلا مفتاح عدم التأثر بالتكرار |

لا ينبغي أن يكون النموذج آلية إعادة المحاولة عندك: فكل إعادة محاولة استدعاء كامل. وبعد *k* إخفاقات متتالية يوقف **قاطع الدائرة (circuit breaker)** استدعاء تلك الأداة، ويتدهور التشغيل أو يسلّم إلى شخص — الدرس 7.1.

### 🔴 نظرة الخبير

**أولى أنماط الإخفاق.** يظهر كل منها في سجل التتبّع ويوقفه حاجز.

| الإخفاق | ما يظهره التتبّع | الحاجز أو الإصلاح |
|---|---|---|
| **حلقة لا نهائية** | الخطوات تتصاعد حتى السقف؛ والمدخلات تكبر | حدّ الخطوات وميزانية الرموز والموعد النهائي |
| **إغراق الأدوات بالاستدعاءات** | أداة واحدة تُستدعى عشرين مرة | سقف لاستدعاءات الأدوات؛ وأداة قائمة |
| **استسلام صامت** | `end_turn` ونص فارغ؛ والواجهة تقول «تم» | النص الفارغ يفشل؛ وسلّم إلى شخص |
| **وسائط أدوات مختلَقة** | `is_error` ومعرّفات أو أسماء أدوات مخترعة | تحقق في الشيفرة — `strict: true` يضبط الشكل لا المعرّف |
| **إنهاء مبكر** | `end_turn` بعد استعلام واحد من ثلاثة | فحص في الشيفرة يتأكد من تغطية كل جزء |
| **الإفراط في الفعل** | كتابة لم يطلبها أحد | لا أداة لها؛ وموافقة على الكتابات — الوحدة 13. وكما أُفيد في يوليو 2025، حذف وكيل برمجة قاعدة بيانات إنتاج |
| **تجاهل `is_error`** | الاستدعاء الفاشل نفسه مرة أخرى | حاجز انعدام التقدم |

**قابلية المراقبة التي تحتاجها الحلقة.** لكل خطوة: رقم الخطوة، و`stop_reason`، ورموز الإدخال والإخراج والمخزَّنة مؤقتًا، وزمن الاستجابة (latency)، ومعرّف الطلب (request id) وهو `resp._request_id`، واسم الأداة ومدخلها، وحجم النتيجة، و`is_error`، والحاجز الذي انطلق. سجّل استدعاء الأداة *قبل* تنفيذه كي يترك أي تجمّد أثرًا. ولكل تشغيل: معرّف التشغيل (run id)، والهدف بعد إخفاء البيانات، والخطوات والرموز والزمن الفعلي، والسبب النهائي. راقب **الذيل** — الخطوات عند المئين 95 وخليط أسباب التوقف ومعدل انطلاق الحواجز والرموز لكل محادثة محلولة — ونبّه على المعدلات لا على تشغيل منفرد. قد تحمل النتائج بيانات شخصية: سجّل الأحجام، أو أخفِ البيانات قبل الاقتطاع — الوحدة 13؛ وتحدد سارة مدة الاحتفاظ. ويمكن أن تُصدر حزمة التطوير امتدادات OpenTelemetry — إصدار تجريبي (beta)، وما تزال اصطلاحات GenAI تتطور. وكل تشغيل فاشل حالة تقييم مستقبلية — الوحدة 12.

**حلقتك الخاصة أم مشغّل الأدوات أم حزمة تطوير؟**
- **حلقتك الخاصة** (الدرس 8.2): كل حاجز في شيفرة بسيطة تستطيع اختبارها سطرًا سطرًا، دون اعتماد على إصدار تجريبي؛ وهي نحو مئة سطر تتولى صيانتها.
- **مشغّل الأدوات التجريبي** (`client.beta.messages.tool_runner` و`@beta_tool`): المسار الذي توصي به حزمة التطوير لوكلاء الأدوات المخصصة. يُنتج كل رسالة قبل تنفيذ أدواتها، فتستطيع أن تسجّل وأن تقيّد الآثار الجانبية داخل دالة الأداة وأن تحدّ الحلقة بـ `max_iterations` — تحقق من حزمة التطوير الحالية. ويتوقف استئناف المشغّل للدور `pause_turn` بنفسه على إصدار حزمة التطوير، إذ كانت الإصدارات الأقدم تنهي التشغيل بصمت: راجع [سجل تغييرات حزمة التطوير](https://github.com/anthropics/anthropic-sdk-python/blob/main/CHANGELOG.md). وتبقى الميزانية والموعد النهائي وانعدام التقدم والتسليم على عاتقك.
- **Claude Agent SDK:** إطار تشغيل Claude Code على هيئة مكتبة، وهي حزمة منفصلة عن `anthropic`، فيها أدوات ملفات وصدفة وصلاحيات وخطافات ووكلاء فرعيون (subagents)؛ وتناسب الوكلاء الذين يعدّلون الملفات وينفّذون الشيفرة في صندوق رملي.
- **Managed Agents** (تجريبي): تستضيف Anthropic الحلقة والصندوق الرملي. تحقق من التوفر وإقامة البيانات. وأيًّا اخترت، تعلّم الحلقة اليدوية أولًا.

**قائمة فحص الحلقة الآمنة.**
1. حدّ للخطوات وميزانية رموز تُفحص قبل كل استدعاء وموعد نهائي للتشغيل، بأحجام مستمدة من تشغيلات مقيسة؛ ومهلة على كل استدعاء وأداة.
2. كشف انعدام التقدم: الاستدعاء نفسه والخطأ نفسه.
3. معالجة كل `stop_reason`؛ ولا أدوات من دور مقطوع أو مرفوض.
4. التحقق من النجاح في الشيفرة؛ والإجابة الفارغة تفشل.
5. قصّ النتائج قبل دخولها سجلًّا يقبل الإلحاق فقط؛ والأدوات لا ترفع استثناءات أبدًا؛ وإعادات المحاولة العابرة في الشيفرة؛ والكتابات مقيَّدة ببوابة، ولا أداة لما يجب ألا يحدث أبدًا.
6. سطر تتبّع لكل خطوة، وسطر توقف لكل تشغيل، والبيانات الشخصية مخفاة أو محذوفة.
7. كل حاجز ينتهي بتسليم إلى شخص، واختبار يجعل كلًّا منها ينطلق.

## 🧰 الأدوات
| الأداة أو الممارسة أو النمط | ما هي وماذا تفعل | متى تلجأ إليها |
|---|---|---|
| **Step cap** — حدّ الخطوات | حدّ صارم للتكرارات؛ ويقيّد أيضًا إعادات المحاولة | كل حلقة |
| **Token budget** — ميزانية الرموز | سقف رموز لكل تشغيل يُفحص قبل كل استدعاء | كل حلقة |
| **Wall-clock deadline** — الموعد النهائي بالساعة الفعلية | حدّ زمني للتشغيل مع مهلة لكل استدعاء وأداة | أي شيء ينتظره شخص |
| **No-progress detector** — كاشف انعدام التقدم | يتوقف حين يعود الاستدعاء نفسه أو الخطأ نفسه | كل حلقة فيها أدوات قراءة |
| **Human hand-off** — التسليم إلى إنسان | حزمة: الهدف والسبب وما جُرِّب إلى طابور مسمّى | كل حاجز |
| **Loop card** — بطاقة الحلقة | صفحة واحدة لكل حلقة: الحدود وجدول التوقف والطابور والاختبارات | قبل إطلاق الحلقة |

## 🏛️ عمليًا في بنك نجم
المُخرَج هو **بطاقة الحلقة** لمسار التذاكر والزملاء في نجم ديسك، تملكها لجين ويراجعها فهد. ولا تُطلَق حلقة دونها. وهي تحلّ محل حلقة لجين ذات حدّ الخمسين. ومتطلب هند: أن تجيب خلال 30 ثانية أو تسلّم إلى شخص. وكل القيم أدناه خيالية.

| الحدّ | القيمة | السبب |
|---|---|---|
| حدّ الخطوات | 6 | التشغيلات العادية تأخذ خطوتين أو ثلاثًا؛ وأبطأ تشغيل تقييم ناجح أخذ 4؛ 1.5 × 4 = 6 |
| ميزانية الرموز | 25,000 | ست خطوات بنتائج من 600 رمز تقرأ 20,850 رمز إدخال، مع نحو 900 رمز إخراج |
| الموعد النهائي | 30 ثانية | وعد نافذة المحادثة؛ ولكل استدعاء مهلته أيضًا |
| التكرارات | 2 | يُرفض استدعاء القراءة المطابق الثاني: فهو لا يضيف شيئًا |
| حجم النتيجة | 2,000 حرف | سجل التذكرة نحو 120 |

| سبب التوقف (Stop reason) | ما يقرؤه الشخص | وجهة الحزمة |
|---|---|---|
| `done` | الإجابة | لا أحد |
| `iteration_cap` و`token_budget` و`timeout` و`no_progress` و`failed_check` و`empty_answer` | «لم أستطع إنهاء هذا. مررته إلى مكتب الخدمة مع كل ما جرّبته: المرجع 3f2a9c01» | طابور مكتب الخدمة |
| `refusal` و`max_tokens` و`unknown_stop` | الرسالة نفسها | طابور مكتب الخدمة؛ ويراجعه فريق نورة أسبوعيًا |
| `model_error` | رسالة الوضع المتدهور في الدرس 7.1 | طابور مكتب الخدمة |

**منصتك.** قبل أن تُطلَق حلقة على منصتك الخاصة، املأ ما يلي:

| السؤال | إجابتك |
|---|---|
| إلى أين يذهب التسليم، ومن المناوب له؟ | |
| أين تُحفظ سجلات التتبّع، ومن يحق له قراءتها، ولكم من الوقت؟ | |
| أي مفتاح إيقاف طارئ يوقف كل الحلقات دون نشر؟ | |

## 🛠️ التمارين
- 🟢 **دقّق حلقة.** دون اتصال. اقرأ `labs/m01/agent.py`. لكل شرط من شروط التوقف الستة اكتب موجود أو مفقود مع رقم السطر؛ ولكل `stop_reason` اكتب ما يفعله. *يكتمل عندما:* يسرد جدول الأمرين معًا، وتسمّي جملة واحدة الحاجز المفقود الذي كان سيكلّف مها أكثر من غيره.
- 🟡 **حدّد حجم الحدود.** دون اتصال. بالصيغة احسب رموز الإدخال لـ 3 و6 و12 خطوة مع نتائج من 300 رمز و3,000 رمز. اختر حدًّا للخطوات وميزانية؛ واكتب جدول التوقف. *يكتمل عندما:* ستة أرقام، وحدّان مع أسبابهما، وجدول توقف يعيد فيه سبب واحد المحاولة بدل التسليم.
- 🔴 **قِس ولا تخمّن.** *يحتاج إلى واجهة البرمجة الحقيقية* وسقف الإنفاق من الدرس 0.2. شغّل `labs/m03/tools_agent.py` على اثني عشر هدفًا — أربعة تحتاج أداة واحدة وأربعة أداتين وأربعة لا تحتاج شيئًا — بالنموذجين `claude-sonnet-5-5` و`claude-haiku-5-5` مع ضبط `TRACE_FILE`. *يكتمل عندما:* يحتوي `NOTES.md`، لكل نموذج، على الوسيط والحد الأقصى للخطوات — اثنا عشر تشغيلًا قليلة جدًا لحساب مئين — والرموز مقابل الصيغة، وحدّ مقترح للخطوات، والتاريخ ومعرّفات النماذج.

## ⚠️ أخطاء وفخاخ
- **حدّ الخمسين «للاحتياط».** خمسون خطوة تكلّف نحو 75 تشغيلًا عاديًا. حدّد حجم الحدّ من الخطوات المقيسة.
- **اعتبار `end_turn` نجاحًا.** فالإجابة الفارغة أو الجزئية تنتهي بالطريقة نفسها. افحص في الشيفرة.
- **تنفيذ أدوات من دور مقطوع أو مرفوض.** فالمدخل نصف المكتوب يظل مدخلًا.
- **تسجيل الإجابة النهائية وحدها.** تتبّع كل خطوة.

## 🧾 الخلاصة
- خطِّط ونفِّذ ولاحِظ وكرِّر: النموذج يقترح، وشيفرتك تقرر متى تتوقف، عبر ستة مخارج تنتهي كلها بتسليم إلى شخص.
- عالِج كل `stop_reason`؛ ولا تنفّذ أداة من دور مقطوع أو مرفوض.
- ينمو الإدخال مع مربّع عدد الخطوات؛ فقلّص نتائج الأدوات.
- يحتاج التأمل الذاتي إلى معلومة جديدة؛ وتزيل حزمة التطوير شيفرة لا مسؤولية.

## ✍️ اختبر نفسك

**1. يُظهر تتبّع مها أن `get_ticket_status` استُدعيت سبع مرات متتالية بالمدخل نفسه. حدّ الخطوات 50 وميزانية الرموز 200,000. أي حاجز يوقفها أبكر وأرخص؟**

- A. حدّ الخطوات، مخفَّضًا من 50 إلى 40 خطوة
- B. الموعد النهائي بالساعة الفعلية البالغ 30 ثانية لكل تشغيل
- C. فحص انعدام التقدم على الاستدعاءات المتطابقة
- D. ميزانية الرموز البالغة 200,000 رمز لكل تشغيل

<details><summary>الإجابة</summary>

**C.** يدل الاستدعاء المطابق الثاني على أنه لن يأتي جديد، فيتوقف التشغيل عند الخطوة 2. أما الحواجز الأخرى فتنطلق بعد إنفاق المال. 🟢 ست طرق للتوقف.

</details>

**2. يحمل رد `stop_reason: "max_tokens"` وينتهي بكتلة `tool_use` يتوقف مدخلها في منتصف قيمة. ماذا ينبغي أن تفعل الحلقة؟**

- A. توقف دون تنفيذها؛ وارفع الحدّ أو سلّم إلى شخص
- B. نفّذ الأداة بالمدخل الجزئي على أي حال
- C. أصلح JSON في الشيفرة ثم نفّذ الأداة
- D. أعد إرسال الرد ليكمله النموذج

<details><summary>الإجابة</summary>

**A.** قد يُحلَّل المدخل المقطوع مع ذلك على أنه كائن جزئي صالح، فتنفيذه تصرّف على تخمين. أما إعادة إرساله فتخص `pause_turn`. 🟢 كل `stop_reason`.

</details>

**3. تعيد حلقة إرسال سجلها في كل استدعاء. مع نتائج من 600 رمز، تقرأ 10 خطوات نحو 50,000 رمز إدخال. فكم تقرأ 20 خطوة تقريبًا؟**

- A. نحو 100,000، لأن عدد الخطوات تضاعف
- B. نحو 175,000، لأن كل استدعاء أطول
- C. نحو 250,000، لأن الكلفة تنمو كالمكعّب
- D. نحو 50,000، لأن التخزين المؤقت يغطيه

<details><summary>الإجابة</summary>

**B.** ينمو الإدخال مع مربّع عدد الخطوات: 174,500 مقابل 49,750، أي نحو 3.5 أضعاف. ويغيّر التخزين المؤقت السعر لا العدد. 🟡 ينمو السياق.

</details>

**4. تضيف نجم ديسك استدعاء «راجع إجابتك» إلى كل تشغيل. درجة التقييم لم تتغير، وكلفة التشغيل ارتفعت بمقدار الثلث. ماذا يقترح الدرس؟**

- A. شغّل المراجعة على نموذج أكبر في كل تشغيل
- B. شغّل المراجعة مرتين، كي يُلتقط عدد أكبر من الأخطاء
- C. أبقِها لأن فحصًا إضافيًا لا يمكن إلا أن يفيد
- D. أبقِها فقط حيث يقدّم فحص في الشيفرة تغذية راجعة

<details><summary>الإجابة</summary>

**D.** يُجدي التأمل الذاتي حين يأتي بمعلومة جديدة كمخطط أو بحث أو اختبار. أما المرور الأعمى فيضيف استدعاءً كاملًا دونها. 🟡 التأمل الذاتي والتصحيح الذاتي.

</details>

**5. تريد هند وكيلًا يعدّل مجلدًا من أدلة التشغيل وينفّذ سكربتًا في صندوق رملي. تبدأ لجين بكتابة أدوات ملفات وصدفة لحلقتها الخاصة. ما الذي ينبغي أن تنظر فيه أولًا؟**

- A. مشغّل الأدوات التجريبي كي لا تكتب الحلقة
- B. حدّ خطوات أعلى كي تنتهي التعديلات
- C. Claude Agent SDK الذي يضم إطار تشغيله هذه الأدوات أصلًا
- D. `tool_choice` إجباري كي تستدعي كل خطوة أداة

<details><summary>الإجابة</summary>

**C.** تحزم Agent SDK إطار تشغيل Claude Code بما فيه أدوات الملفات والصدفة. أما مشغّل الأدوات فيوفر عليك الحلقة لا الأدوات؛ وأحدث النماذج ترفض `tool_choice` الإجباري. 🔴 حلقتك الخاصة أم مشغّل الأدوات أم حزمة تطوير؟

</details>

## 📚 المراجع
- Anthropic، «Building effective agents»: https://www.anthropic.com/engineering/building-effective-agents
- Claude API، التعامل مع أسباب التوقف (Handling stop reasons): https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons؛ ونظرة عامة على استخدام الأدوات (Tool use overview): https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview؛ والأخطاء: https://platform.claude.com/docs/en/api/errors
- Claude API، التفكير المحفوظ (Preserved thinking): https://platform.claude.com/docs/en/build-with-claude/preserved-thinking؛ وتحرير السياق: https://platform.claude.com/docs/en/build-with-claude/context-editing؛ والضغط: https://platform.claude.com/docs/en/build-with-claude/compaction؛ وOpenTelemetry: https://platform.claude.com/docs/en/manage-claude/opentelemetry
- Managed Agents: https://platform.claude.com/docs/en/managed-agents/overview؛ وحزمة Anthropic Python SDK، ومنها مشغّل الأدوات (tool runner): https://github.com/anthropics/anthropic-sdk-python؛ وClaude Agent SDK: ابدأ من https://docs.anthropic.com/
- الأوراق البحثية المذكورة أعلاه، وتُعثر عليها بالعنوان: Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (2022)؛ Madaan et al., "Self-Refine" (2023)؛ Shinn et al., "Reflexion" (2023)؛ Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet" (2023).
- [*اختبار البرمجيات (Software Testing)*، الدرس 7.2 — اختبار RAG واستخدام الأدوات والوكلاء](../testing/index.ar.html#/7.2)؛ [*أمن الذكاء الاصطناعي وأمن التطبيقات (Secure AI & Application Security)*، الدرس 9.2 — الوكلاء والأدوات: الصلاحيات المفرطة وأدوات أقل الصلاحيات وMCP](../secai/index.ar.html#/9.2)
- **اقرأ هذا الأسبوع، الوحدة 8.** Grokking AI Applications، الفصل 6: https://www.manning.com/ (ابحث بالعنوان). Gulli، *Agentic Design Patterns*، الفصل 4 والفصل 6: المسودة المجانية المذكورة في الدرس 0.1. Microsoft، *AI Agents for Beginners*، الدرسان 06-07: https://github.com/microsoft/ai-agents-for-beginners

---

# 8.2 — المختبر: حلقة وكيل من الصفر في نحو 95 سطرًا، بحدّ صارم وتسجيل كامل للتتبّع
*المستوى: 🟡 متوسط* · *المتطلبات: 3.2، 8.1* · *الطبقة: Agents, Production*

**بعد هذا الدرس تستطيع** أن تبني حلقة وكيل في نحو 95 سطرًا بحدّ للخطوات وميزانية للرموز وموعد نهائي (deadline) وكشف لانعدام التقدم، ثم تجعل كل حاجز يعمل وتُظهره في سجل التتبّع JSONL. *مدة الدراسة: قراءة نحو 10 دقيقة، وعمل تطبيقي نحو 6 ساعة (تقدير).*

## ⚡ الدرس في دقيقة
- تبني حلقة الدرس 8.1 في ملف واحد دون أي إطار عمل، في نحو 95 سطرًا من منطق الحلقة: **حدّ الخطوات** و**ميزانية الرموز** و**الموعد النهائي** و**كشف انعدام التقدم** وكل `stop_reason`، والنجاح تفحصه الشيفرة.
- يكتب كل تشغيل **سجل تتبّع JSONL (JSONL trace)** — الخطوة والأداة والمدخل وحجم النتيجة والرموز وزمن الاستجابة؛ وتحكيه أداة **إعادة التشغيل** كقصة.
- ينتهي كل حاجز (guard) بـ**حزمة تسليم**: الهدف وسبب التوقف وما جُرِّب.
- توجيهات المحاكي تجعل الإخفاقات تقع عند الطلب؛ و**اختبار لكل حاجز** يثبت أنه ينطلق.
- يحاكي المحاكي الإخفاقات؛ أما النماذج الحقيقية فتخفق بطرق مختلفة.

## 🧭 لماذا يهم
بعد محادثة الخمسين خطوة تطلب مها من لجين أمرًا واحدًا: أن تُظهر ما فعله الوكيل ولماذا توقف، وهذا افتراضي. كانت الحلقة القديمة تحتفظ بالنص النهائي فقط. وبعد أسبوعين يلصق أحد الموظفين «ref 3f2a9c01» في رسالة إلى يارا. فتشغّل أداة إعادة التشغيل وتستطيع أن تقول: طلب الوكيل التذكرة 4471 مرتين، وأُوقف، ولدى مكتب الخدمة الحزمة. وهذا ما يبنيه هذا المختبر.

## 📐 كيف يعمل

### 🟢 الأساسيات

**شغّله.** شغّل المحاكي بسيناريو هذا المختبر. وللواجهة الحقيقية تبقى الشيفرة نفسها: أوقف المحاكي، وألغِ ضبط `ANTHROPIC_BASE_URL`، وصدِّر مفتاحك الحقيقي — سقف الإنفاق أولًا، الدرس 0.2.

```bash
cd aiapps/labkit
python -m labkit.mock_server --port 8787 --playbook playbooks/m08_lab.json &
export ANTHROPIC_BASE_URL=http://127.0.0.1:8787 ANTHROPIC_API_KEY=mock TRACE_FILE=m08_trace.jsonl
python labs/m08/agent_loop.py "Is ticket 4471 done yet? And what about 4472?"
python labs/m08/replay.py m08_trace.jsonl
pytest tests/test_m08_labs.py
```

**اقرأ تشغيلًا أولًا.** يجمّع `labs/m08/replay.py` (42 سطرًا، ومختبَر) أسطر JSONL بحسب معرّف التشغيل ويطبع سطرًا لكل حدث: وهو الأداة التي استخدمتها يارا. ويضع علامة على أي تشغيل بلا سطر `stop`، أي عملية ماتت. اقرأ شيفرته لاحقًا. ومخرجاته:

```text
run de885b3e: Is ticket 4471 done yet? And what about 4472?   (limits: 6 steps, 25000 tokens, 30.0 s)
  step 1  model tool_use  in=159 out=20 total=179  20 ms
          tool  get_ticket_status {"ticket_id": "4471"} -> 113 chars, ok, 0 ms
          tool  get_ticket_status {"ticket_id": "4472"} -> 72 chars, ok, 0 ms
  step 2  model end_turn  in=232 out=53 total=464  3 ms
  DONE
  2 steps, 464 tokens, 0.0 s
```

طلبت الخطوة 1 أداتين؛ وأُجيب عنهما في رسالة واحدة. وقرأت الخطوة 2 ما مقداره 232 رمز إدخال مقابل 159 لأنها أعادت إرسال النتائج — وهو النمو الذي شرحه الدرس 8.1.

### 🟡 التعمق أكثر

**الحلقة جزءًا جزءًا.** تضم الأسطر من 75 إلى 168 (94 سطرًا) الدالة `run_tool` وفحص الاكتمال والدالة `run`؛ والباقي إعدادات وتتبّع وسطر أوامر. أهذه أول مرة تقابل فيها `@dataclass` أو `namedtuple` أو دالة معرَّفة داخل أخرى مثل `stop`؟ انظر جدول بايثون في الدرس 0.2.

```python
# labs/m08/agent_loop.py
"""Lab 8.2: an agent loop from scratch: four guards, every stop_reason, a JSONL trace, a hand-off.
  python labs/m08/agent_loop.py "Is ticket 4471 done yet?"
  environment: MAX_STEPS, TOKEN_BUDGET, TIMEOUT_S, TRACE_FILE"""
import json
import os
import re
import sys
import time
import uuid
from collections import Counter, namedtuple
from dataclasses import asdict, dataclass
from pathlib import Path

import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from labkit.tools import get_ticket_status, lookup_employee  # noqa: E402  fake, read-only tools

MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")
SYSTEM = ("You help IT service desk staff. "
          "Use the tools for tickets and colleagues; never guess them.")
TOOLS = {   # name -> (description, its one argument, function): all the model can make happen
    "get_ticket_status": (
        "Look up one IT ticket by number. Call this whenever asked about a ticket.",
        "ticket_id", get_ticket_status),
    "lookup_employee": (
        "Look up a colleague by first name: team and email. "
        "Call this for any question about a colleague.",
        "name", lookup_employee),
}


def definition(name, description, key):
    """What the model sees of one tool: name, description, one required string argument."""
    schema = {"type": "object", "properties": {key: {"type": "string"}}, "required": [key]}
    return {"name": name, "description": description, "input_schema": schema}


DEFINITIONS = [definition(n, d, k) for n, (d, k, _) in TOOLS.items()]


@dataclass(frozen=True)
class Limits:                                    # every number is a decision
    max_steps: int = int(os.environ.get("MAX_STEPS", 6))             # guard 1: model calls
    token_budget: int = int(os.environ.get("TOKEN_BUDGET", 25_000))  # guard 2: tokens, all calls
    timeout_s: float = float(os.environ.get("TIMEOUT_S", 30))        # guard 3: clock, whole run
    max_repeats: int = 2                         # guard 4: same call this often = no progress
    result_chars: int = 2_000                    # most a tool result may add to the context


# A namedtuple is a tuple with named fields: res.ok, res.reason... handoff is what a person receives
Result = namedtuple("Result", "ok reason answer steps tokens handoff")


class Trace:
    """One JSON object per line. Strings are clipped: tool output can hold personal data."""

    def __init__(self, path=None):
        self.path, self.run_id, self.events = path, uuid.uuid4().hex[:8], []

    def log(self, event, **fields):
        fields = {k: v[:300] if isinstance(v, str) else v for k, v in fields.items()}
        head = {"run": self.run_id, "seq": len(self.events) + 1, "ts": round(time.time(), 3)}
        self.events.append({**head, "event": event, **fields})
        if self.path:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(self.events[-1], ensure_ascii=False, default=str) + "\n")


def ms(since):
    return round((time.monotonic() - since) * 1000)


def run_tool(name, args):
    """The gap: the model proposes, this function disposes. Never raises: every outcome is text."""
    if name not in TOOLS:
        return f"unknown tool {name!r}; the tools are: {', '.join(TOOLS)}", True
    _, key, fn = TOOLS[name]
    if set(args) != {key} or not isinstance(args[key], str):
        got = json.dumps(args)[:80]
        return f"{name} takes exactly one string argument named {key!r}; got {got}", True
    try:
        return str(fn(args[key])), False
    except Exception as e:                       # a raising tool must not end the run
        return f"{name} failed: {e}", True


def mentions_every_ticket(goal, answer):
    """A completion check in plain code. Returns a problem, or None."""
    missing = [t for t in re.findall(r"\b\d{4}\b", goal) if t not in answer]
    return f"the answer never mentions {', '.join(missing)}" if missing else None


def run(goal, lim=Limits(), client=None, trace=None, check=None):
    client = client or anthropic.Anthropic(timeout=30.0)    # the SDK retries transient errors twice
    trace = trace or Trace()
    t0, spent, last_in, seen = time.monotonic(), 0, 0, Counter()
    messages = [{"role": "user", "content": goal}]
    trace.log("start", goal=goal, model=MODEL, **asdict(lim))

    def stop(reason, step, text="", why=""):     # the only exit: one "stop" line per run
        ok, secs = reason == "done", round(time.monotonic() - t0, 1)
        keys = ("step", "tool", "input", "result", "refused")
        tried = [{k: e[k] for k in keys if k in e} for e in trace.events if e["event"] == "tool"]
        packet = None if ok else {"run": trace.run_id, "reason": reason, "why": why, "goal": goal,
                                  "steps": step, "tokens": spent, "seconds": secs,
                                  "tried": tried, "last_text": text[:300]}
        trace.log("stop", step=step, reason=reason, why=why, tokens=spent, seconds=secs,
                  answer=text, handoff=packet)
        sorry = (f"I could not finish this ({reason}). I passed it to the Service Desk "
                 f"with everything I tried: ref {trace.run_id}.")
        return Result(ok, reason, text if ok else sorry, step, spent, packet)

    for step in range(1, lim.max_steps + 1):                 # guard 1: the hard cap
        if time.monotonic() - t0 > lim.timeout_s:             # guard 3: before every call
            return stop("timeout", step - 1, why=f"more than {lim.timeout_s} s on the clock")
        if spent + last_in > lim.token_budget:                # guard 2: the next call re-sends this
            why = f"{spent} spent, and the next call needs {last_in}+ of {lim.token_budget}"
            return stop("token_budget", step - 1, why=why)
        t1 = time.monotonic()
        try:
            resp = client.messages.create(model=MODEL, max_tokens=1024,
                                          output_config={"effort": "low"},
                                          system=SYSTEM, tools=DEFINITIONS, messages=messages)
        except anthropic.APIError as e:                   # the SDK's retries are spent: hand off
            trace.log("model_error", step=step, error=type(e).__name__,
                      status=getattr(e, "status_code", None), ms=ms(t1))
            return stop("model_error", step - 1, why=f"{type(e).__name__} after the SDK's retries")
        used = resp.usage
        last_in, spent = used.input_tokens, spent + used.input_tokens + used.output_tokens
        trace.log("model", step=step, stop_reason=resp.stop_reason, input_tokens=used.input_tokens,
                  output_tokens=used.output_tokens, total_tokens=spent, ms=ms(t1),
                  request_id=resp._request_id)
        messages.append({"role": "assistant", "content": resp.content})   # the WHOLE content list
        text = next((b.text for b in resp.content if b.type == "text"), "")
        if resp.stop_reason == "end_turn":
            if not text.strip():
                return stop("empty_answer", step, why="end_turn with no text: a silent give-up")
            problem = check(goal, text) if check else None    # "done" needs the code to agree
            return stop("failed_check" if problem else "done", step, text, why=problem or "")
        if resp.stop_reason == "pause_turn":              # paused: send it back; the cap counts it
            continue
        if resp.stop_reason != "tool_use":                    # max_tokens, refusal, or a new value
            known = resp.stop_reason in ("max_tokens", "refusal")
            why = f"stop_reason={resp.stop_reason} {resp.stop_details or ''}".strip()
            return stop(resp.stop_reason if known else "unknown_stop", step, text, why=why)
        results = []                                      # cut-off and refused turns never get here
        for block in (b for b in resp.content if b.type == "tool_use"):
            call = (block.name, json.dumps(block.input, sort_keys=True))
            seen[call] += 1
            if seen[call] >= lim.max_repeats:                 # guard 4: the same call again
                trace.log("tool", step=step, tool=block.name, input=block.input,
                          refused="same call again")
                why = f"{block.name} asked for again with the same input"
                return stop("no_progress", step, text, why=why)
            t2 = time.monotonic()
            out, is_error = run_tool(block.name, block.input)
            trace.log("tool", step=step, tool=block.name, input=block.input, result_chars=len(out),
                      result=out, is_error=is_error, ms=ms(t2))
            shown = out[:lim.result_chars]
            if len(out) > lim.result_chars:
                shown += f" [cut: {len(out)} characters in all]"
            results.append({"type": "tool_result", "tool_use_id": block.id,
                            "content": shown, "is_error": is_error})
        messages.append({"role": "user", "content": results})  # ONE message: a result per tool_use
    why = f"{lim.max_steps} steps used and no final answer"
    return stop("iteration_cap", lim.max_steps, why=why)


if __name__ == "__main__":
    goal = " ".join(sys.argv[1:]) or "Is ticket 4471 done yet? And what about 4472?"
    trace = Trace(os.environ.get("TRACE_FILE", "m08_trace.jsonl"))
    res = run(goal, trace=trace, check=mentions_every_ticket)
    print(res.answer)
    if res.handoff:
        print(json.dumps(res.handoff, indent=2, ensure_ascii=False))
```

1. **`run_tool`** هي الفجوة. لا ترفع استثناءً أبدًا، ولا تعرف سوى أداتي قراءة — بديلان عن TicketHub وPeopleCore — فالنموذج *لا يستطيع* إغلاق تذكرة.
2. **`stop`** هي المخرج الوحيد؛ والتشغيل الفاشل يبني حزمة التسليم من التتبّع.
3. **تُنفَّذ الحواجز قبل الاستدعاء**: الحدّ الأقصى هو حلقة `for` نفسها، ثم الموعد النهائي، ثم ميزانية الرموز، مع اعتبار مدخل الاستدعاء الأخير حدًّا أدنى لأن السجل لا يفعل سوى أن ينمو. ويُفحص الموعد النهائي *بين* الخطوات، فقد يتجاوزه استدعاء بطيء واحد. و`timeout=30.0` الخاص بالعميل يحدّ محاولة واحدة، وتعيد حزمة التطوير المحاولة مرتين افتراضيًا عند انتهاء المهلة، فقد تستغرق الخطوة نحو ثلاثة أمثال ذلك؛ ولتشديده مرّر عميلك الخاص: `run(goal, client=anthropic.Anthropic(timeout=10.0, max_retries=1))`.
4. **لكل `stop_reason` فرع.** غياب النص هو `empty_answer`؛ وفشل فحص الشيفرة هو `failed_check`؛ و`pause_turn` يكرر الحلقة؛ أما `max_tokens` و`refusal` والقيم المجهولة فتتوقف *قبل* أن تعمل أي أداة.
5. **كشف انعدام التقدم** يعدّ الأزواج المتطابقة من (الأداة، المدخل) ويرفض الثاني *قبل* تنفيذه. وتُقتطع النتائج الطويلة قبل دخولها السياق؛ ويحتفظ التتبّع بالحجم الحقيقي. ويُكتب سطر الأداة بعد عودتها؛ فإن كانت الأدوات قد تتجمّد فسجّل سطرًا قبل الاستدعاء.

### 🔴 نظرة الخبير

**اجعله يفشل عند الطلب.** يبرمج السيناريو حركات النموذج للأهداف الخاصة بـ Noura و`close` و`handover` و`4479` و`4480`؛ أما التوجيهات فلا تحتاج سكربتًا. ثم عُدّ أسباب التوقف — ويحتوي الملف أيضًا على التشغيل الأول أعلاه:

```bash
for g in "Check ticket 4474, then find the colleague Noura so I can forward it." "Please close ticket 4472." \
         "Are tickets 4471 and 4473 resolved? [mock:loop]" "Is ticket 4471 done yet? [mock:giveup]" \
         "Summarise tickets 4477 and 4478 for the shift handover." "What is the status of ticket 4479?" \
         "What is the status of ticket 4480?" "Is ticket 4471 done yet? [mock:overloaded]"; do
  python labs/m08/agent_loop.py "$g" > /dev/null
done
TIMEOUT_S=2 python labs/m08/agent_loop.py "Is ticket 4471 done yet? [mock:slow]" > /dev/null
MAX_STEPS=1 python labs/m08/agent_loop.py "Is ticket 4471 done yet?" > /dev/null
TOKEN_BUDGET=300 python labs/m08/agent_loop.py "Is ticket 4471 done yet?" > /dev/null
python -c "import json, collections; print(collections.Counter(e['reason'] for e in map(json.loads, open('m08_trace.jsonl')) if e['event'] == 'stop'))"
```

```text
Counter({'done': 4, 'no_progress': 2, 'empty_answer': 1, 'failed_check': 1, 'model_error': 1, 'timeout': 1, 'iteration_cap': 1, 'token_budget': 1})
```

| الهدف أو الإعداد | ما يحاكيه | يتوقف بوصفه |
|---|---|---|
| الهدف الأول؛ وسلسلة Noura | تشغيلات عادية | `done` |
| `close ticket 4472` | **الإفراط في الفعل**: لا أداة كهذه | `done` مع `is_error` واحد |
| `[mock:loop]` | نموذج عالق | `no_progress` |
| `[mock:giveup]` | **استسلام صامت** | `empty_answer` |
| `shift handover` | **إنهاء مبكر**: تذكرة واحدة من اثنتين | `failed_check` |
| `4479` | **وسيط مختلَق** ثم إصلاح | `done` مع `is_error` واحد |
| `4480` | **تجاهل `is_error`** | `no_progress` |
| `[mock:overloaded]` | خطأ 5xx (529) في كل مرة | `model_error` |
| `TIMEOUT_S=2` و`[mock:slow]` | استدعاء مدته 3 ثوانٍ | `timeout` |
| `MAX_STEPS=1`؛ `TOKEN_BUDGET=300` | حدود منخفضة جدًا | `iteration_cap`؛ `token_budget` |

شغّل المحاكي بـ `MOCK_FAIL_EVERY=3` بدلًا من ذلك فيفشل كل طلب ثالث: تخفي إعادات المحاولة في حزمة التطوير ذلك ولا يكشفه إلا زمن الاستجابة. وهذه حزمة التسليم الخاصة بتشغيل `[mock:loop]`، مقتطعة بعد `tried`:

```bash
python labs/m08/agent_loop.py "Are tickets 4471 and 4473 resolved? [mock:loop]" | head -10
```

```text
I could not finish this (no_progress). I passed it to the Service Desk with everything I tried: ref 8e654913.
{
  "run": "8e654913",
  "reason": "no_progress",
  "why": "get_ticket_status asked for again with the same input",
  "goal": "Are tickets 4471 and 4473 resolved? [mock:loop]",
  "steps": 2,
  "tokens": 383,
  "seconds": 0.0,
  "tried": [
```

يسرد `tried` كل استدعاء ومدخله ونتيجته والتكرار المرفوض. ويخزّن سطر `stop` الحزمة أيضًا.

التشغيل نفسه كما تقرؤه يارا، من `replay.py`، دون أي استدعاء للنموذج لإنتاجه:

```text
run 8e654913: Are tickets 4471 and 4473 resolved? [mock:loop]   (limits: 6 steps, 25000 tokens, 30.0 s)
  step 1  model tool_use  in=159 out=10 total=169  23 ms
          tool  get_ticket_status {"ticket_id": "4471"} -> 113 chars, ok, 0 ms
  step 2  model tool_use  in=204 out=10 total=383  4 ms
          tool  get_ticket_status {"ticket_id": "4471"} -> REFUSED (same call again)
  STOPPED by no_progress: get_ticket_status asked for again with the same input -> handed to a person
  2 steps, 383 tokens, 0.0 s
```

اقرأه من الأعلى إلى الأسفل: طلب النموذج 4471، وحصل على الجواب، وطلبه ثانيةً، فرفض الحاجز التكرار قبل أن تعمل الأداة.

**اختبار لكل حاجز.** يجعل `tests/test_m08_labs.py` كل حاجز ينطلق أمام المحاكي، مع عميل مزيّف لما لا يستطيع المحاكي إنتاجه: `refusal` و`pause_turn` و`stop_reason` غير معروف.

**تحفظات صادقة.** *يعمل دون اتصال:* كل حاجز، والتتبّع، وإعادة التشغيل، والحزمة، والاختبارات. *يحتاج إلى واجهة البرمجة الحقيقية:* هل يكرر النموذج الاستدعاء حرفيًا — فقد يغيّر النموذج الحقيقي المدخل، وهو ما يفوّته حاجز المطابقة التامة — وهل يتعافى من `is_error`، وهل تجتاز إجابته فحصك، وزمن الاستجابة والرموز الحقيقيان — فأعداد المحاكي تقديرية. التوجيهات *تحاكي* الإخفاقات، والسيناريو *يبرمج* حالات التعافي: فالأخضر دون اتصال يثبت شيفرتك وحدها. وفخ آخر في الواجهة الحقيقية: حين يكون التخزين المؤقت للموجّه (prompt caching) مفعّلًا، يعدّ `usage.input_tokens` الذيل غير المخزَّن مؤقتًا فقط، فأضف حقلي التخزين المؤقت إلى الميزانية.

## 🧰 الأدوات
| الأداة أو الممارسة أو النمط | ما هي وماذا تفعل | متى تلجأ إليها |
|---|---|---|
| **Tool trace** — سجل تتبّع الأدوات | سجل JSONL لاستدعاءات النموذج والأدوات، وسطر توقف واحد لكل تشغيل؛ وتحكيه إعادة التشغيل كقصة | كل تشغيل وكل حادثة |
| **Hand-off packet** — حزمة التسليم | الهدف والسبب وما جُرِّب ومعرّف التشغيل إلى طابور مسمّى | كل حاجز ينطلق |
| **Guard test** — اختبار الحاجز | حقن الأخطاء — توجيهات وسيناريوهات وعملاء مزيّفون — يجعل الحاجز ينطلق، ويثبت ذلك بإزالة الحاجز | كل حلقة |

## 🏛️ عمليًا في بنك نجم
**المُسلَّم الأسبوعي.** أودِع المجلد `week-08/` ومعه `labs/m08/` واختبارات ناجحة؛ وأعداد الأسباب وحزمة لكل إخفاق من الإخفاقات أعلاه؛ وبطاقة الحلقة من الدرس 8.1؛ و`NOTES.md` وفيه إجاباتك عن الاختبار وملاحظات «اقرأ هذا الأسبوع».

**جلسة المجموعة — 60 دقيقة.** (1) تبادلوا سجل تتبّع؛ ويشرح زميلك التشغيل باستخدام `replay.py` وحده (15). (2) «اهزم الحاجز»: جِد هدفًا يفوّته كشف انعدام التقدم (15). (3) قارنوا نتائج الواجهة الحقيقية (15). (4) اتفقوا على حزمة واحدة (15).

**ابنه باستخدام Claude Code.** *لا Claude Code لديك؟ نفّذ خطوات المواصفة بيدك وشغّل فحوصها بنفسك (الدرس 0.3).* أعطِ هذه المواصفة إلى Claude Code في وضع التخطيط — راجع وثائق Claude Code الحالية — وراجع الخطة قبل أن يعدّل أي شيء:

```text
Goal: refactor labs/m08/agent_loop.py into a small package, labs/m08/agentkit/, with Limits, Trace,
run_tool and run in separate modules; agent_loop.py stays the command line and re-exports every
name the tests use.
Context: Python 3.11, anthropic>=1,<2, the mock in aiapps/labkit (read its README), labs/m08/*.py and
tests/test_m08_labs.py.
Constraints:
- Behaviour must not change: guards, stop reasons, trace fields, the hand-off packet.
- Guards run BEFORE the model call. Only anthropic.APIError is caught around it.
- ONE user message with a tool_result for EVERY tool_use id. No tools run from max_tokens, refusal
  or unknown stops. No temperature, prefill, forced tool_choice, new dependencies or keys.
- Do NOT edit the tests, weaken a guard or delete a branch to make anything pass.
Acceptance: pytest passes unchanged; replay.py reads traces written before and after.
Plan first; move one module at a time; run the tests after each move.
```

**تحقق قبل أن تقبله.**
- شغّل الاختبارات، ثم **أزل كل حاجز بدوره** — الحدّ الأقصى والموعد النهائي والميزانية وانعدام التقدم وفحص الإجابة الفارغة وكل فرع من فروع `stop_reason` — وتأكد من أن اختبارًا يفشل في كل مرة. والحاجز الذي لا يلاحظه أي اختبار ليس حاجزًا.
- اقرأ الفرق بحثًا عن حاجز نُقل إلى ما بعد الاستدعاء، و`except Exception` حوله، وحقول تتبّع أُعيدت تسميتها. وأعد تشغيل مصفوفة الإخفاقات وقارن الأعداد.

## 🛠️ التمارين
- 🟢 **اجعل كل حاجز ينطلق.** دون اتصال. باستخدام الجدول، تسبّب في `done` وستة أسباب توقف مختلفة واقرأ كلًّا منها في `replay.py`. *يكتمل عندما:* يحتوي `NOTES.md` على أعداد الأسباب، ولكل سبب الأمر والسطر الذي أوقفه.
- 🟡 **سُدّ ثغرة إغراق الأدوات.** دون اتصال. أضف `max_tool_calls` إلى `Limits` بقيمة افتراضية هي 8؛ وتوقف بالسبب `tool_budget` عند تجاوزها. *يكتمل عندما:* يفشل اختبار بعميل مزيّف يطلب عشر تذاكر في رد واحد دون تغييرك وينجح معه.
- 🔴 **هل ينجو مع نموذج حقيقي؟** *يحتاج إلى واجهة البرمجة الحقيقية* وسقف الإنفاق. شغّل عشرة أهداف — منها التذكرة 9999 وتذكرتان وعبارة «close ticket 4472» — بالنموذجين `claude-sonnet-5-5` و`claude-haiku-5-5`. *يكتمل عندما:* يحتوي `NOTES.md`، لكل نموذج، على أسباب التوقف والخطوات والرموز الفعلية وزمن الاستجابة، وتتبّع واحد مفاجئ، والتاريخ ومعرّفات النماذج.

## ⚠️ أخطاء وفخاخ
- **فحص الحاجز بعد الاستدعاء.** تدفع أولًا وتتوقف ثانيًا.
- **`except Exception` حول استدعاء النموذج.** فهي تخفي أخطاءك البرمجية. التقط `anthropic.APIError`، ونبّه على `status` بقيمة 400 أو 401: فذلك خطؤك أو مفتاحك لا انقطاع في الخدمة.
- **الوثوق بالتعافي دون اتصال.** فالسيناريو برمج الإصلاح؛ وقد لا يجده نموذج حقيقي.
- **تسمية الاقتطاع «تنقيحًا».** الاقتطاع إلى 300 حرف ليس إخفاءً للبيانات.

## 🧾 الخلاصة
- ملف واحد دون إطار عمل: حواجز قبل كل استدعاء، ومخرج واحد، وسطر توقف واحد لكل تشغيل.
- لكل `stop_reason` فرع؛ والدور المقطوع أو المرفوض لا ينفّذ أي أداة.
- يسجل التتبّع الخطوة والأداة والمدخل وحجم النتيجة والرموز وزمن الاستجابة؛ وتحكي إعادة التشغيل القصة.
- ينتهي كل حاجز بحزمة تسليم؛ وتثبت الاختبارات أن كل حاجز ينطلق.

## ✍️ اختبر نفسك

**1. الميزانية 20,000 رمز. بعد الخطوة 3 أنفقت الحلقة 14,000، وقرأ الاستدعاء الأخير 7,000 رمز إدخال. ماذا يحدث في بداية الخطوة 4؟**

- A. يُنفَّذ الاستدعاء لأن 14,000 دون 20,000
- B. تتوقف الحلقة بـ`token_budget` دون استدعاء
- C. تقلّص الحلقة السجل ليلائم الميزانية ثم تستدعي
- D. يُنفَّذ الاستدعاء ثم يُفحص المجموع

<details><summary>الإجابة</summary>

**B.** يعيد الاستدعاء التالي إرسال 7,000 رمز على الأقل، و14,000 + 7,000 يتجاوز 20,000، فيُوقَف دون أن يُدفع ثمنه. 🟡 الحلقة جزءًا جزءًا.

</details>

**2. ينتهي تشغيل بـ `[mock:giveup]` بالقيمة `stop_reason: "end_turn"` وقائمة `content` فارغة. ماذا يعيد المختبر؟**

- A. `done`، فيمرّر إجابة فارغة
- B. `failed_check`، يرفعه فحص الشيفرة
- C. `iteration_cap`، حين تنفد الخطوات
- D. `empty_answer` مع حزمة تسليم

<details><summary>الإجابة</summary>

**D.** `end_turn` بلا نص هو استسلام صامت: إخفاق مع حزمة. 🟡 الحلقة جزءًا جزءًا.

</details>

**3. مع `TIMEOUT_S=2` و`[mock:slow]` تُظهر إعادة التشغيل استدعاءً مدته نحو 3,000 ms ثم `STOPPED by timeout`. لماذا لم يُقطع الاستدعاء عند ثانيتين؟**

- A. لا يُفحص الموعد النهائي إلا فيما بين الخطوات
- B. يتجاهل المحاكي إعداد `TIMEOUT_S`
- C. رفعت حزمة التطوير المهلة لتناسبه
- D. يعدّ الموعد النهائي الرموز لا الثواني

<details><summary>الإجابة</summary>

**A.** تُقرأ الساعة قبل كل استدعاء؛ ولا يحدّ الاستدعاء الواحد إلا `timeout` الخاص بالعميل. 🟡 الحلقة جزءًا جزءًا.

</details>

**4. يعيد Claude Code هيكلة الحلقة وما زالت كل الاختبارات تنجح. أي فحص يُظهر على أفضل وجه أن الحواجز ما زالت تنطلق؟**

- A. شغّل هدفًا واحدًا على المسار السعيد واقرأ الإجابة
- B. عُدّ الأسطر وتحقق من أنها نقصت
- C. أزل كل حاجز بدوره وانظر اختبارًا يفشل
- D. اقرأ أسماء الملفات الجديدة وسلاسل التوثيق

<details><summary>الإجابة</summary>

**C.** نجاح الاختبارات لا يثبت أن الحواجز مختبَرة؛ أما إزالة حاجز ومشاهدة اختبار يفشل فيثبت ذلك. 🏛️ تحقق قبل أن تقبله.

</details>

**5. لا تتلقى يارا سوى «ref 3f2a9c01». ماذا ينبغي أن تحمل الحزمة كي تواصل دون أن يبدأ المستخدم من جديد ودون بيانات شخصية أكثر مما تحتاجه الحالة؟**

- A. السبب وآخر جملة للنموذج فقط
- B. الهدف والسبب واستدعاءات الأدوات المجرَّبة
- C. المحادثة كاملة مع كل نتيجة أداة دون اقتطاع
- D. ملخص يكتبه النموذج بعد الإخفاق

<details><summary>الإجابة</summary>

**B.** الهدف وسبب التوقف وما جُرِّب تأتي مباشرة من التتبّع. أما التفريغ الكامل فينسخ بيانات شخصية بلا فائدة؛ والملخص الذي يكتبه النموذج ادعاء جديد غير موثَّق. 🔴 اجعله يفشل عند الطلب.

</details>

## 📚 المراجع
- Claude API، التعامل مع أسباب التوقف: https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons؛ والأخطاء: https://platform.claude.com/docs/en/api/errors؛ ونظرة عامة على استخدام الأدوات: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- حزمة Anthropic Python SDK — إعادات المحاولة والمهل والأخطاء المنمّطة: https://github.com/anthropics/anthropic-sdk-python
- Python، `dataclasses`: https://docs.python.org/3/library/dataclasses.html؛ و`time.monotonic`: https://docs.python.org/3/library/time.html
- README عدّة المختبر، وفيه المحاكي والتوجيهات والسيناريوهات (directives, playbooks): https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/aiapps/labkit
- [*اختبار البرمجيات*، الدرس 7.2 — اختبار RAG واستخدام الأدوات والوكلاء](../testing/index.ar.html#/7.2)
