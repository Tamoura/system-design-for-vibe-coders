# Storyboard: Building AI Applications & Agents: Zero to Hero, lesson 8.1

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 1 of 3 for this course.** This is the best single mechanism in the course. A counter-intuitive twist (the safety cap is the cost) comes with concrete numbers from the lesson's own table, and the takeaway will not date: input cost grows with the square of the steps, and your code decides when to stop.

## The most expensive number in the file (lesson 8.1)

**Why this lesson:** a single twist carries a lasting idea. The step cap that 'held' was the cost, because every step re-sends everything before it.
**Target viewer:** an engineer or consultant about to ship a first agent loop.
**Length:** about 85 s.

| # | Seconds | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-8 | A cost-sorted list of conversations; one bar shoots off the chart | The bar keeps growing past the frame | "75× a normal conversation" | "One conversation cost about seventy-five times a normal one. And its answer was right." | «محادثة واحدة كلّفت نحو خمسة وسبعين ضعف المحادثة العادية، وكان جوابها صحيحًا.» |
| 2 | 8-20 | A loop: Ask model → read stop_reason → run tool → return result | An arrow circles the four boxes and speeds up | "The agent loop" | "An agent loop asks the model, runs the tool it asked for, hands back the result, and repeats." | «حلقة الوكيل تسأل النموذج، وتنفّذ الأداة التي طلبها، وتعيد إليه النتيجة، ثم تكرّر.» |
| 3 | 20-33 | A message stack sent into the model on each lap | The stack gets taller each lap: system prompt, tools, every earlier turn | "Every call re-sends everything" | "Each call re-sends the system prompt, the tools and every earlier turn. So each step reads more than the last." | «كل استدعاء يعيد إرسال موجّه النظام والأدوات وكل الأدوار السابقة، فتقرأ كل خطوة أكثر مما قرأته سابقتها.» |
| 4 | 33-48 | Area chart of input tokens vs steps (trimmed results) | The area curves upward; labels pop in: 4 → 10,900; 10 → 49,750; 20 → 174,500; 50 → 998,750 | "Cost grows with the square of the steps" | "Double the steps from ten to twenty and the input grows three and a half times." | «ضاعِف الخطوات من عشر إلى عشرين، فيتضاعف الإدخال ثلاث مرات ونصفًا.» |
| 5 | 48-60 | A step counter climbing to 50; a stamp: "CAP HELD" | The stamp turns into a price tag | "The cap of 50 held" | "Her step cap was fifty, to be safe. It held, and it was the most expensive number in the file." | «كان حدّ الخطوات خمسين، احتياطًا. وقد صمد الحدّ، وكان أغلى رقم في الملف.» |
| 6 | 60-75 | Six gates around the loop light up one by one | Each gate closes and routes to a person icon | "Six exits: success · step cap · token budget · deadline · no progress · hand-off" | "The model proposes; your code decides when to stop. Six exits, and every one ends in a hand-off, never a crash." | «النموذج يقترح، وشيفرتك تقرّر متى تتوقف. ستة مخارج، وكلها تنتهي بتسليم إلى إنسان، لا بانهيار.» |
| 7 | 75-85 | Title card and the lesson link | The loop shrinks into a small, bounded box | "Bound the loop. Trim the results." | "Decide how long it may run, how much it may spend, and who takes over. Open lesson 8.1 to do the arithmetic." | «حدّد كم يعمل، وكم يُنفق، ومن يتسلّم بعده. افتح الدرس 8.1 لتجري الحساب بنفسك.» |

**Closing takeaway:** input cost grows with the square of the steps; a cap is not a plan; every guard ends in a hand-off.
**Call to action:** open lesson 8.1, then break the loop on purpose in lab 8.2.

**Re-check before production:**
- Label the story and numbers as hypothetical with fictional sizes (S = 1,500, g = 100, o = 150, r = 600). The 75× compares $1.04 with $0.014 at the lesson's toy prices, not any model's price.
- The Arabic cost formula at 08-agent-loop.ar.md:79 is missing (o + r). Fix it before any Arabic on-screen maths.
- In Arabic captions use الأجل for deadline, not مهلة (see 08-agent-loop.ar.md:273).
