# Storyboard: Building AI Applications & Agents: Zero to Hero, lesson 14.2

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 3 of 3 for this course.** A clear causal chain (529, then six calls per question, then the rate limit, then a 20-minute outage) that motion graphics can show far better than prose, with a fix the viewer can watch replayed.

## How a blip became an outage (lesson 14.2)

**Why this lesson:** the retry storm is a cause-and-effect chain you can rewind and replay with the fix in place.
**Target viewer:** someone taking an agent from pilot to production.
**Length:** about 75 s.

| # | Seconds | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-8 | A clock at Sunday 07:02; the provider returns '529 overloaded' | A brief red flicker on the provider node | "Sunday 07:02 · 529 overloaded" | "One Sunday morning the provider answers: overloaded. A brief blip." | «صباح أحد، يردّ المزوّد: مثقل بالطلبات. عطل عابر لا أكثر.» |
| 2 | 8-22 | One request particle splits into six | Particles fire instantly, with no gap between them | "5 retries, no wait = 6 calls per question" | "The wrapper retries five times with no wait, so every question becomes six calls." | «يعيد الغلاف المحاولة خمس مرات دون انتظار، فيصبح كل سؤال ستة استدعاءات.» |
| 3 | 22-35 | Thousands of particles hit a wall labelled 'rate limit' | They pile up; an outage timer runs to 20:00 | "Blip → 20-minute outage" | "The burst hits the rate limit, and a brief overload becomes a twenty-minute outage." | «يصطدم هذا السيل بحدّ المعدّل، فيتحوّل عطل قصير إلى انقطاع لعشرين دقيقة.» |
| 4 | 35-50 | Rewind effect; the same spike replays | Retries now spread out with random gaps (jitter) and stop at a cap | "Retry with jitter, a cap, one layer" | "Rewind. Retry with jitter and a cap, in one layer only, and never retry a request that was simply wrong." | «لنُعِد المشهد. أعِد المحاولة بفواصل عشوائية وبحدّ أقصى، في طبقة واحدة فقط، ولا تُعِد طلبًا خاطئًا من أصله.» |
| 5 | 50-62 | A circuit breaker switch flips open; a fallback path lights up | The spike flattens into a low line | "Circuit breaker + tested fallback" | "A circuit breaker stops the flood, and a tested fallback answers in the meantime." | «قاطع الدائرة يوقف السيل، وبديل مُختبَر يجيب في أثناء ذلك.» |
| 6 | 62-75 | Title card and the lesson link | The particles settle into an even stream | "Test your retry code against a provider that misbehaves" | "Nobody had tested the retry code. Open lesson 14.2 and break it on purpose." | «لم يختبر أحد شيفرة إعادة المحاولة. افتح الدرس 14.2 واكسرها عمدًا.» |

**Closing takeaway:** retries without wait or cap turn a blip into an outage; jitter, a cap, one layer, a circuit breaker and a tested fallback keep it a blip.
**Call to action:** open lesson 14.2.

**Re-check before production:**
- Confirm the current meaning of HTTP 529 in the provider's error docs, and the lesson's 'never a 400' retry rule.
- Label the incident as hypothetical.
- If a cost beat is added, keep it to the lesson's own wording ('a lower price per token, a higher cost per resolved ticket') with no prices on screen.
