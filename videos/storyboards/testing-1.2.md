# Storyboard: Software Testing: Zero to Hero in the AI Era, lesson 1.2

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 3 of 3 for this course.** A measured, surprising fact: 100,000 random pairs found zero differences against an off-by-one bug, while one boundary test catches it. It is the clearest visual case for test design, cut to boundary value analysis only.

## Random Dots Never Hit the Line (lesson 1.2)
**Why this lesson:** it shows, not tells, why volume and randomness do not replace test design.
**Target viewer:** beginners and developers who believe more tests or random tests mean better coverage.
**Length:** about 70 s

| # | Seconds | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-10 | A starter suite of 24 tests runs five times, once per seeded bug; two runs go red, three stay green | Bug switches flipping; ticks stay green on three | 24 tests, 5 bugs, 3 missed | A starter suite of 24 tests is run against five seeded bugs. It catches two. Three slip through. | تُشغَّل حزمة من 24 اختبارًا على خمسة عيوب مزروعة عمدًا، فتكشف اثنين ويفلت ثلاثة. |
| 2 | 10-20 | Test points cluster in the middle of an input area; the bugs sit at the edges | Darts all landing near the bullseye | Tests in the middle, bugs at the edges | None of the tests is wrong. They sit in the middle of the input space, where the bugs are not. | لا يوجد اختبار خاطئ، لكنها كلها في منتصف مساحة المدخلات، والعيوب ليست هناك. |
| 3 | 20-34 | 100,000 random dots rain across a square; a hair-thin line marks 'sent today + amount = 50,000.00'; counter ends at 'differences: 0' | Rain that never touches a wire | 100,000 random pairs: 0 differences | So try volume. A hundred thousand random pairs against the off-by-one daily-limit bug. Differences found: zero. | فلنجرّب الكثرة إذن: مئة ألف زوج عشوائي في مواجهة عيب الخطأ بواحد في الحد اليومي. عدد الاختلافات: صفر. |
| 4 | 34-46 | Zoom on the line; label 'about 1 in 5 million' and '~2% chance in 100,000' | Microscope zoom on the thin line | Exactly 50,000.00 | The bug needs the total to equal exactly fifty thousand. A random pair lands there about once in five million tries. | فالعيب لا يظهر إلا حين يساوي المجموع خمسين ألفًا بالضبط، وزوج عشوائي يصيب ذلك مرة واحدة تقريبًا في كل خمسة ملايين محاولة. |
| 5 | 46-58 | A single test point placed exactly on the line; terminal shows one FAILED line while every 'mid' test passes | A pin dropped precisely on the wire, sparks fly | One boundary test: FAILED | One boundary test, aimed at the edge, turns red at once, while every middle test stays green. | أما اختبار حدّي واحد موجَّه إلى الحافة فيتحوّل إلى الأحمر فورًا، بينما تبقى اختبارات المنتصف كلها خضراء. |
| 6 | 58-70 | Motif: bug switch, red tick; question | Tick pulses | Pick tests by the shape of the rule | Test design means choosing a few tests that can fail for the right reasons. Open lesson 1.2 and plant a bug to prove it. | تصميم الاختبارات يعني أن تختار عددًا قليلًا من الاختبارات القادرة على الفشل للسبب الصحيح. افتح الدرس 1.2 وازرع عيبًا لتثبت ذلك. |

**Closing takeaway:** randomness and volume miss boundaries; aim at the edges and prove the test turns red. **Call to action:** open lesson 1.2.

**Re-check before production:** the figures (100,000 pairs, zero differences, about 1 in 5 million, about 2%) are from 01-foundations.md:310. The skeptic did not independently verify the 2% figure, so recompute it before animating. The Arabic lesson uses the calque 'صفر اختلافات' (01-foundations.ar.md:310); the VO above uses natural wording.
