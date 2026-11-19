# Storyboard: Secure AI & Application Security: Zero to Hero, lesson 9.1

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 3 of 3 for this course.** A vivid zero-click leak whose fix is clear and durable: make the renderer safe whatever the model says.

## The image that leaks: never trust model output
**Lesson:** 9.1 Guardrails and output handling: never trust model output
**Why this lesson:** It shows a data leak that needs no click from the customer, and reinforces the series motif that a request is not a control.
**Target viewer:** a developer building a chat or assistant UI on an LLM.
**Length:** about 80 s

| # | Sec | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over EN | Voice-over AR |
|---|---|---|---|---|---|---|
| 1 | 0-10 | A banking chat answers in rich text: bold fees, lists, links | A friendly chat bubble | Rich answers | A bank's assistant answers in rich text, and the app renders the model's Markdown straight into the page. | مساعد البنك يجيب بنصٍّ منسّق، والتطبيق يعرض ما يكتبه النموذج مباشرة في الصفحة. |
| 2 | 10-22 | A dispute note with hidden instructions enters the model's context | A note with a faint second layer of writing | Hidden instructions | In a staging test, a dispute note with hidden instructions reaches the model. | في اختبارٍ على بيئة التجهيز، تصل إلى النموذج ملاحظةُ اعتراضٍ تخفي تعليماتٍ في داخلها. |
| 3 | 22-36 | The model writes a Markdown image whose address carries the customer's recent transactions | Transactions are packed into a URL like letters into an envelope | An 'image' with data in its address | The model writes an image whose address points to an outside server, with the customer's transactions packed into it. | فيكتب النموذج صورةً عنوانها خادمٌ خارجي، وقد حُشرت فيه معاملات العميل الأخيرة. |
| 4 | 36-46 | The app auto-fetches; an arrow leaves the app; the 'no clicks' cursor stays still | The envelope flies out of the building | Zero clicks | The app fetches the image automatically, and the data leaves without the customer clicking anything. | يجلب التطبيق الصورة تلقائيًا، فتخرج البيانات دون أن ينقر العميل على شيء. |
| 5 | 46-58 | A system-prompt line 'Never output images or HTML' with a red 'request' tag | A polite sign on an open gate | That's a request, not a control | Adding 'never output images' to the prompt is a request, not a control. | أن تضيف إلى التعليمات «لا تُخرج صورًا أبدًا» طلبٌ، وليس وسيلة حماية. |
| 6 | 58-72 | Replay: the same model text, but the renderer allow-list blocks the fetch | A gate closes at the exit, not at the model | Fix it at the sink | Fix it where the output is used: the renderer loads images only from allowed sources, whatever the model says. | عالِج الأمر حيث تُستخدم المخرجات: المكوّن الذي يعرض الصفحة لا يحمّل الصور إلا من مصادر مسموح بها، أيًّا كان ما يقوله النموذج. |
| 7 | 72-80 | End card with the decision cue | A question mark resolving to 'nothing that matters' | Worst output? Nothing that matters. | Ask: if the model wrote the worst possible output, what would happen? Design so the answer is nothing that matters. Open lesson 9.1. | اسأل: لو كتب النموذج أسوأ ما يمكن، فماذا سيحدث؟ صمّم النظام بحيث يكون الجواب: لا شيء يُذكر. افتح الدرس 9.1. |

**Closing takeaway:** Model output is untrusted input; the control sits at the sink, not in the prompt.
**Call to action:** Open lesson 9.1.
**Re-check before production:** the lesson's general claim that researchers demonstrated Markdown image exfiltration against public assistants between 2023 and 2025, and that vendors restricted image sources (name no vendor without a source); keep 'LLM05' and other OWASP codes out of the script because of the 2026 renumbering.
