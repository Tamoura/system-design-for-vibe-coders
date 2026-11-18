# Storyboard: Building AI Applications & Agents: Zero to Hero, lesson 1.1

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 2 of 3 for this course.** One mechanism (a stateless function that is resent the whole list) explains three bugs at once. The core idea is the foundation of the course and will not date.

## The model forgot? Your code did. (lesson 1.1)

**Why this lesson:** one idea solves three real-looking bugs, and every later module builds on it.
**Target viewer:** a builder whose first chatbot 'forgets', gets cut off, or costs too much.
**Length:** about 75 s.

| # | Seconds | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-10 | Three chat notifications pop in | Each bubble shakes like an alert | "It forgot my laptop model" · "It stopped mid-sentence" · "Input tokens 20× output?" | "Three complaints arrive in the same week. Two ideas explain all three." | «ثلاث شكاوى تصل في الأسبوع نفسه، وفكرتان تفسّرانها كلها.» |
| 2 | 10-22 | A box labelled 'LLM' with a list going in and one message coming out | The box empties after every call | "A model is a function" | "A language model is a function: a list of messages in, the next message out. It keeps nothing between calls." | «النموذج اللغوي دالّة: قائمة رسائل تدخل، والرسالة التالية تخرج. ولا يحتفظ بشيء بين استدعاء وآخر.» |
| 3 | 22-35 | Code line `history = []` and the list being wiped | The laptop-model message dissolves before reaching the box | "Memory is what your code resends" | "The handler started every request with an empty list, so the model never saw the laptop model." | «كان المعالج يبدأ كل طلب بقائمة فارغة، فلم يرَ النموذج طراز الحاسوب قط.» |
| 4 | 35-50 | A twenty-turn chat; the full list is resent on each call | An input-token meter climbs much faster than the output meter | "You pay for the whole history, again" | "In a twenty-turn chat each call resends every earlier turn. That is why input dwarfs output." | «في محادثة من عشرين دورًا، يعيد كل استدعاء إرسال كل الأدوار السابقة؛ لذلك يفوق الإدخال الإخراج بكثير.» |
| 5 | 50-60 | A max_tokens=400 bar filling with 'thinking' before any answer text | The bar runs out and the answer is cut off | "Thinking counts as output" | "And four hundred output tokens were spent on thinking before the first word of the answer." | «وأُنفقت أربعمئة رمز إخراج على التفكير قبل أول كلمة من الجواب.» |
| 6 | 60-68 | Five labels orbit the call: system · messages · max_tokens · stop_reason · usage | Labels snap into a checklist | "Know five things on every call" | "On every call, know five things: system, messages, max tokens, stop reason and usage." | «في كل استدعاء اعرف خمسة أشياء: موجّه النظام، والرسائل، والحدّ الأقصى للرموز، وسبب التوقف، والاستهلاك.» |
| 7 | 68-75 | Title card and the lesson link | The list glows as 'what the model knows' | "Print the list first" | "When something forgets, costs too much or gets cut off, print the list first. Open lesson 1.1." | «إذا نسي شيئًا أو كلّف كثيرًا أو انقطع، فاطبع القائمة أولًا. افتح الدرس 1.1.» |

**Closing takeaway:** everything the model 'knows' about the conversation is the list your code sends.
**Call to action:** open lesson 1.1 and draw the resend table yourself.

**Re-check before production:**
- Leave out the temperature caveat (01-llm-app.md:18) and any words-per-token ratio. The '750 words is about 1,000 tokens' rule at 01-llm-app.md:44 is outdated for current models.
- Label the Najm Desk scene as hypothetical, with fictional numbers.
- Confirm that thinking tokens still count toward max_tokens and output billing on the models shown.
