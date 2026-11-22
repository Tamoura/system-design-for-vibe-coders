# Module 2 — From idea to first product

*Module 1 asked whether Qafila's product is worth building: who it serves, what evidence says they have the problem, and whether each delivery can pay its way. This module is about turning that understanding into something real people use, without wasting the few weeks and the little money a young company has. It stays at Qafila's Launch stage: four people, 15 pilot shops, about 150 deliveries a day, and a first version that Faisal deploys by hand once a week. First you learn to frame the next idea as a set of assumptions and to test the riskiest ones cheaply, before anyone writes code. Then you learn to cut a product down to the smallest version that is still useful and teaches you something, and to choose the right kind of prototype for each question. Last, you learn how a small team chooses its technology: what to build, what to buy or rent, what the cloud provider takes care of and what it does not, and how to write the decision down so the next person understands it. Each lesson leaves an artefact: an assumption map with a test plan, a story map with a scope list, and a technology decision log.*

> **Steps:** Discover, Design — test what must be true before building, shape the smallest product that does the job and teaches you something, and choose technology you can run, afford and leave.

---

# 2.1 — Discovery: framing a problem and testing assumptions
*Level: 🟢 Beginner* · *Prerequisites: 1.2* · *Step: Discover*

**After this you can** turn a product idea into an assumption map of ten or more assumptions sorted by importance and evidence, pick the one to test first, and write a test plan with a pass line decided before the test runs. *Study time: reading about 20 min, hands-on about 95 min (estimate).*

## ⚡ In 60 seconds
- **Discovery** is the work of finding out what to build before building it: which problem matters, which solution might solve it, and what must be true for that solution to work.
- An **assumption** is something the team treats as true without enough evidence. Every idea rests on many. The dangerous ones are important and poorly supported.
- An **assumption map** sorts them on two scales, how much the idea depends on each one and how much evidence you have, so you test the riskiest first.
- The rule that matters most: **decide what result would prove you wrong before you run the test.**
- Decision cue: if a test costs more than a day or two at Launch, look for a cheaper one: a conversation, existing records, or doing the job by hand for a week.
- Biggest trap: "testing" by building the whole feature and then reading whatever happens as success.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

It is the fourth month of the Launch pilot: four people (Maha, Faisal, Salma, who looks after shops and couriers, and a part-time helper), 15 pilot shops, about 150 deliveries a day. Lesson 1.2 showed that shops phone couriers because the courier does not know *when the order will be ready*.

Faisal arrives with a plan: an "order ready" button, a pickup alert for couriers, a live courier map for shops and predicted ready times, all in four weeks. Maha asks: "What has to be true for this to work, and which of those things do we actually know?" They write fourteen sticky notes. They have real evidence for two.

If shops will not press a button during the rush, four weeks are gone. Discovery spends a few days to protect them.

## 📐 How it works

### 🟢 The essentials

**Problem space and solution space.** The **problem space** is about people: who they are, what goes wrong, what it costs them (lesson 1.2). The **solution space** is about what you might build. Write each idea as a pair: *the problem it addresses* and *the solution proposed*. If the problem half is vague, go back to lesson 1.2.

**Finding the assumptions.** Take one idea and ask, "For this to work, what must be true?" Write each answer as a short statement that could turn out to be false. Lesson 1.1 introduced four product risks (Marty Cagan's four risks); use them as prompts so you do not only list technical worries:

| Risk | The question | Example assumption for "order ready" |
|---|---|---|
| **Value** | Will people want it enough to change what they do? | "Counter staff will mark orders ready instead of phoning the courier." |
| **Usability** | Can they use it, in their real situation? | "Staff can mark an order ready in under five seconds with one hand, during the rush." |
| **Feasibility** | Can we build and run it with what we have? | "The courier app can show a ready time within a few seconds of the shop pressing the button." |
| **Viability** | Does it work for the business? | "Fewer phone calls will keep shops paying after the free pilot." |

Add a fifth prompt: **could this harm anyone?** For example, "couriers will not feel pushed to ride faster by a countdown".

**The assumption map.** Draw a square with two axes:

- **Importance** (up the side): if this assumption is wrong, does the idea fail? High means "the idea collapses"; low means "we would adjust a detail".
- **Evidence** (along the bottom, from none on the left to strong on the right): how much evidence do we already have? Use the grades from lesson 1.2: none, opinion, story, observed behaviour, commitment.

Place each note. The **top-left corner** (important, little evidence) holds your **riskiest assumptions**: test those first. Important, well-evidenced ones can be accepted for now; unimportant ones can wait. This is a widely used practice (the Strategyzer article in the References describes one version). Some versions, including that one, flip the evidence axis so the riskiest corner is on the right; what matters is *important plus little evidence*.

**From assumption to test.** For the one or two riskiest assumptions, write a **test plan** in six short parts, in this course's own layout:

- **Assumption:** the belief under test, written so it could turn out false.
- **Cheapest test:** the least costly action that produces real evidence.
- **Evidence we will record:** what gets counted or observed, and where it is written down.
- **Pass line (decided now):** the number or observation that counts as support.
- **Decision date and decider:** when you stop, and who makes the call.
- **If it fails:** what you will change or drop.

The pass line is the heart of it. Without it, any result reads as success: "only 4 of 10 used it, but they loved it".

### 🟡 Going deeper

**A ladder of tests, cheapest first.** Not every question needs software. Climb only as high as you must.

| Test | What you do | Rough cost at Launch |
|---|---|---|
| **Look at records** | Pull orders, call logs, messages you already have | Hours |
| **Ask about the past** | Short interviews about the last time (lesson 1.2) | Hours |
| **Observe** | Watch the real situation when it happens | A morning or two |
| **Concierge test** | Do the job by hand for a few customers, openly | Days |
| **Wizard of Oz test** | It looks automatic; people do the work behind it | Days |
| **Smoke test** | Offer something before it exists; see who commits | Days |
| **Prototype test** | A sketch or clickable mock in front of users (lesson 2.2) | Hours to days |
| **Coded slice** | The thinnest working version for a few customers | Weeks |

In a **concierge test** the customer knows a person does the work; a **Wizard of Oz test** hides the people behind a screen. At Qafila's scale the concierge version is usually enough. For smoke tests, see [*Founder's Playbook for AI-First Builders*, lesson 1.4 — Smoke tests: a landing page and a pre-sale before you build](../founder/index.html#/1.4).

**Good pass lines.** A pass line should be:

- **Specific:** "at least 8 of 10 lunch orders marked ready without a reminder", not "staff use it". For waiting times, teams often use the **median** (the middle value when all the waits are sorted), because one very long wait does not distort it.
- **Tied to behaviour,** not opinion ("staff liked it").
- **Set where a fail would change your plan.** If you would build it whatever happens, the test is theatre.
- **Honest about sample size.** Two shops for a week give a signal, not proof.

**Three possible results.** **Pass:** move the assumption to the evidence side. **Fail:** change or drop the idea; that is discovery working. **Unclear:** the decider named in the plan calls it. Discovery is continuous: a test or two every week.

### 🔴 Expert view

**Stay with the problem, not your first solution.** For "couriers do not know when the order will be ready", options include a ready button, a fixed prep time per shop, or a courier who waits inside. List at least three before testing one, or you are only testing your favourite.

**The riskiest beliefs often hide in viability.** Eric Ries calls the beliefs a whole venture rests on "leap-of-faith assumptions" (*The Lean Startup*). What kills a young company is more often "they will pay" or "it will stay cheap to run" than usability. Put one on every map.

**Confirmation bias in test design.** Pilot shops are keener than average (lesson 1.2); include a lukewarm one.

**Ethics and personal data.** Tell people they are part of a test, keep only what you need, delete it afterwards, and ask someone who knows the local data-protection rules what you may keep.

**Discovery with AI.** An assistant can suggest assumptions you missed, but supplies no evidence about your customers: grade its notes "none". For discovery on AI features specifically, see [*AI Product Management*, lesson 2.1 — Discovery for AI: jobs, workflows and where AI fits](../aipm/index.html#/2.1).

**The memorable rule.** Decide what result would prove you wrong before you run the test.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Problem–solution pair** | The problem an idea addresses and the solution proposed, one line each | Whenever someone proposes a feature |
| **Assumption list** | "For this to work, it must be true that…" statements across five prompts | For any idea bigger than a day's work |
| **Assumption map** | Importance up the side, evidence along the bottom; test the top-left first | To choose what to test |
| **Test plan** | Assumption, cheapest test, evidence recorded, pass line, decision date and decider, if it fails | Before every test |
| **Test ladder** | Tests from records to coded slice, cheapest first | To pick the cheapest real evidence |

## 🏛️ In practice at Qafila
Maha, Faisal and Salma map the "order ready" idea in one hour. Illustrative and fictional.

> **Assumption map: "order ready" button and pickup alert (Launch, month 4)**
>
> | # | Assumption | Risk | Importance | Evidence now |
> |---|---|---|---|---|
> | 1 | Counter staff will say when an order will be ready, during the rush, unprompted | Value / usability | High | None |
> | 2 | Knowing the ready time will make couriers arrive closer to it | Value | High | Story (two couriers said so) |
> | 3 | If couriers arrive on time, shops will stop phoning them | Value | High | Story (grocer's assistant, lesson 1.2) |
> | 4 | The courier app can show a ready time within a few seconds | Feasibility | Medium | Observed (Faisal's quick spike: a throwaway experiment in code) |
> | 5 | Fewer calls will keep shops paying after the pilot | Viability | High | None |
> | 6 | A countdown will not push couriers to ride unsafely | Harm | High | None |
> | 7 | Shops want their own live courier map (today's map is only on the admin page) | Value | Low | Opinion (two shop owners asked) |
>
> **Riskiest:** 1. Number 6 is also important and unsupported; Salma will ask four couriers this week. Number 5 is just as risky, but it depends on number 1 and cannot be tested until a post-pilot price exists; Maha will ask three shops for a written pre-commitment in month 5.
>
> **Test plan 1**
> - **Assumption:** counter staff will tell us the ready time for most rush orders, without reminders.
> - **Cheapest test:** a one-week concierge test at two bakeries, both told it is manual: staff send Salma a chat message ("order 12, ready in 10"); she forwards it to the courier.
> - **Evidence we will record:** the share of rush orders with a message, and with a shop-to-courier call (Salma's log, a counter tally sheet).
> - **Pass line (decided now):** each bakery messages at least 8 of every 10 rush orders and calls fall below 1 in 4 orders.
> - **Decision date and decider:** next Thursday; Maha and Salma. Two shops for a week is a signal, not proof.
> - **If it fails:** find a cheaper way for staff to report, before any code.
>
> **Result.** Bakery A: 9 of 10 messaged, calls on 1 in 8 orders: pass. Bakery B: 5 of 10; staff forgot when the queue was long: fail. **Learned:** it works only if marking an order ready costs almost nothing; typing is too much. Next: a one-tap version on paper (lesson 2.2).

Faisal wanted Bakery B counted as a pass because "the owner loved the idea". Maha pointed at the pass line; the owner's view was logged as opinion.

## 🛠️ Exercises
**🟢 List and sort assumptions.** Choose an idea for a product or feature you use (or take Qafila's idea that "customers will tip couriers through the app"). Write at least ten assumptions, at least two for each of value, usability, feasibility and viability, and one about possible harm. Then mark each one high, medium or low importance and grade its evidence (none, opinion, story, observed, commitment).
*Done when:* ten or more falsifiable statements each have an importance mark and an evidence grade, and the riskiest two are circled.

<details><summary>Model answer and self-check</summary>

**Model answer.** Tips idea, all ten: "Customers will tip in the app rather than in cash" (value, high, none); "Shops will not object to a tip prompt" (value, medium, none); "Tipping takes under ten seconds" (usability, medium, none); "Customers trust the app with a small extra payment" (usability, high, none); "We can pass tips on without handling card data ourselves" (feasibility, high, story); "Couriers can see tips received the same day" (feasibility, low, none); "Provider fees leave the courier most of the tip" (viability, high, none); "Tips make couriers likelier to stay with Qafila" (viability, medium, opinion); "Couriers will not favour orders from tipping shops" (harm, high, none); "Customers will not feel pressured into tipping" (harm, medium, none). Circled: in-app rather than cash, and fees.

**Self-check.**
- Is every statement falsifiable ("customers will…"), not a vague hope ("tips are good")?
- Did you include viability and harm, not only usability and features?

</details>

**🟡 Write a test plan with a pass line.** Take the riskiest assumption from the first exercise. Write the six-part test plan using the cheapest test on the ladder that would produce behaviour, not opinion.
*Done when:* the test costs three days or less, and the plan has evidence with a named record, a numeric pass line, a date, a decider, and what you will do if it fails.

<details><summary>Model answer and self-check</summary>

**Model answer.** *Assumption:* customers will tip in the app rather than in cash. *Cheapest test:* for one week, deliveries from three shops carry a printed card linking to a simple tip page run by a payment provider; couriers are told it is a test. *Evidence we will record:* link tips versus cash tips couriers report (tally sheet, provider dashboard). *Pass line:* at least 1 in 10 deliveries gets a link tip, and link tips outnumber cash. *Decision date and decider:* next Thursday; Maha. *If it fails:* drop in-app tips for the pilot. Illustrative.

**Self-check.**
- Would a fail actually change your plan?
- Does the measure count something people did, not something they said?

</details>

**🔴 Map, test and decide on a real idea.** Pick a small change in your own life or a personal project (a habit app, a club's sign-up process, an open-source tool's feature request). Build an assumption map, run one real test from the bottom three rungs of the ladder (records, interviews, observation) within a week, and write the decision.
*Done when:* eight or more assumptions are mapped, one test was run with its pass line written first, and a decision note says pass, fail or unclear and what happens next.

<details><summary>Model answer and self-check</summary>

**Model answer (extract: the tested assumption only; the full map has eight).** A sign-up sheet for a weekend football group instead of the chat thread. Tested: "the chat fails to show who is coming", by reading eight weeks of the thread. Pass line: someone asked "who is coming?" after confirmations in over half the weeks. Result: 6 of 8; pass. Next: try the sheet for three weeks.

**Self-check.**
- Was the pass line written down before you looked at the data?
- Did the result move at least one assumption on the map?

</details>

## ⚠️ Mistakes and traps
- **Building to test.** Weeks of code to learn what a one-week concierge test could show. Climb the ladder from the bottom.
- **A pass line written after the results.** Any result then looks like success. Write it first.
- **Testing the comfortable assumptions.** Test the top-left corner, even when it holds viability or harm.
- **Only friendly participants.** Include a lukewarm shop where you can.
- **Skipping consent because it is "only a test".** Tell people; keep and then delete the minimum data.

## 🧾 Recap
- Discovery finds what to build before building it; keep the problem separate from the solution.
- List assumptions using value, usability, feasibility, viability and harm as prompts.
- Map them by importance and evidence; test the important, poorly evidenced ones first.
- Use the cheapest test that shows behaviour, with a pass line written first.
- Rule: decide what result would prove you wrong before you run the test.

## ✍️ Check yourself
**1. Faisal proposes building the ready button, pickup alert, a courier map for shops and ready-time prediction in four weeks. What should the team do first?**

- A. Build the button first, because it is the simplest piece, then decide on the rest from usage.
- B. Write down what the plan relies on, then check first the beliefs it most needs and can least back up.
- C. Survey all 15 pilot shops about which of the four features they would like most this month.
- D. Agree a four-week plan with weekly demos, so shops can comment on each feature as it is built.

<details><summary>Answer</summary>

**B.** Testing the riskiest assumptions first protects four weeks of work. A builds before testing anything, C collects opinions, and D commits all four weeks before learning whether the core assumption holds. See "The assumption map".

</details>

**2. Four notes from Qafila's map are below, each with its importance and evidence. Which should the team test first?**

- A. "Staff will understand the word 'ready' on a button": low importance, no evidence yet.
- B. "The courier app can show a ready time within seconds": medium importance, observed in a spike.
- C. "If couriers arrive on time, shops will stop phoning them": high importance, one story.
- D. "Counter staff will report ready times during the rush, unprompted": high importance, no evidence.

<details><summary>Answer</summary>

**D.** It is both important and unsupported, the riskiest corner. C is important too, but it already has some evidence, and it only matters if staff report ready times at all. A would not sink the idea, and B is already partly observed. See "The assumption map".

</details>

**3. Bakery B sent ready-time messages for 5 of 10 rush orders, below the pass line of 8 of 10, but its owner said she loved the idea. How should the team record the result?**

- A. As a fail on the pass line, with the owner's view logged separately as opinion.
- B. As a pass, because the owner's enthusiasm shows the idea has value for that shop.
- C. As unclear, and rerun the test until the bakery reaches the pass line set earlier.
- D. As a pass for Bakery B, because the average across both bakeries was close enough.

<details><summary>Answer</summary>

**A.** The behaviour missed a pass line set in advance; the owner's view is weaker evidence. B lets opinion override behaviour, C reruns hoping for a different answer, and D changes the rule after the results. See "Good pass lines".

</details>

**4. Salma wants to learn whether shops will report ready times without building anything. Which test is the best fit?**

- A. A coded version of the button for all pilot shops, measured over a month of real orders.
- B. A survey asking shops how often they would use a ready button during the lunch rush.
- C. A concierge test: shops message ready times to Salma, who passes them on by hand.
- D. A smoke test offering a paid premium plan that includes a ready button next month.

<details><summary>Answer</summary>

**C.** A concierge test shows real behaviour within days, without code. A builds first, B gathers predictions, and D tests willingness to pay, a different assumption. See "A ladder of tests".

</details>

**5. Which pass line is best for the experiment "couriers will arrive closer to the ready time if they know it"?**

- A. At least 8 of 10 couriers rate the ready times 4 out of 5 or higher in a survey after two weeks.
- B. Median courier wait at the counter falls from about 9 to under 4 minutes within two weeks.
- C. Courier wait at the counter is under 9 minutes on at least one day in the two-week test.
- D. Couriers arrive on time more often than before, as judged by the shop owners at the end.

<details><summary>Answer</summary>

**B.** It measures behaviour, against a baseline, at a level that could fail. A has numbers but measures opinion, C has numbers but is so weak it can hardly fail, and D is a vague judgement after the fact. See "Good pass lines".

</details>

## 📚 References
- Strategyzer, "How assumptions mapping can focus your teams on running experiments that matter" (David J. Bland): https://www.strategyzer.com/library/how-assumptions-mapping-can-focus-your-teams-on-running-experiments-that-matter (4 August 2020; an excerpt from *Testing Business Ideas*) — mapping desirability, feasibility and viability hypotheses by importance and evidence; its evidence axis runs from "have evidence" to "no evidence", so the riskiest quadrant is top right. Strategyzer also publishes a similar "Test Card" (Alex Osterwalder, 5 March 2015: https://www.strategyzer.com/library/validate-your-ideas-with-the-test-card); the test plan in this lesson is this course's own layout.
- Bland, D. J. and Osterwalder, A., *Testing Business Ideas: A Field Guide for Rapid Experimentation* (Wiley, 2019); Open Library record: https://openlibrary.org/books/OL28004111M (paperback, 12 November 2019).
- Ries, E., *The Lean Startup* (Crown Business, 2011); the book's page, https://theleanstartup.com/book, uses the term "leap-of-faith assumptions".
- Torres, T., *Continuous Discovery Habits* (Product Talk, 2021): https://www.producttalk.org/continuous-discovery-habits/ — interviewing customers and testing assumptions as a weekly habit.
- Library course: [*Founder's Playbook for AI-First Builders*, lesson 1.4 — Smoke tests: a landing page and a pre-sale before you build](../founder/index.html#/1.4).
- Library course: [*AI Product Management*, lesson 2.1 — Discovery for AI: jobs, workflows and where AI fits](../aipm/index.html#/2.1).

---

# 2.2 — The smallest useful product: scope, prototypes and learning
*Level: 🟢 Beginner* · *Prerequisites: 2.1* · *Step: Discover, Design*

**After this you can** draw a story map for one product or feature, cut a first slice that does the job end to end for one group, write a scope list of what is in, next and out, and choose the right kind of prototype for each open question. *Study time: reading about 20 min, hands-on about 115 min (estimate).*

## ⚡ In 60 seconds
- A first product should be the **smallest useful product**: the least that does real users' job from start to finish and teaches you what you most need to learn next.
- "Minimum viable product" (MVP) is the popular name for a similar idea, often misread as "a cheap, buggy version 1". Small does not mean careless.
- A **story map** lays out the user's steps left to right with details underneath, so you can slice thinly across the whole journey.
- A **prototype** lets you learn before building the real thing: a sketch, a clickable mock, a person doing the job, a thin coded slice. Match it to the question.
- The rule that matters most: **cut across the whole journey, not down one step.**
- Biggest trap: cutting what users never see but rely on: data protection, a way to undo, someone who notices when it breaks.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

Lesson 2.1's test showed shops will report ready times only if it costs them almost nothing. Faisal now wants to build "properly": a ready button, predicted ready times, a live map for shops, alerts, a shop history screen and a weekly report. Five weeks.

Maha remembers the first version: Faisal spent nearly three weeks on a courier rating screen and a polished order history, which have barely been opened since. So the question is not "what could we build?" but "what is the least that does the shop's job end to end, and what will it teach us?"

## 📐 How it works

### 🟢 The essentials

**What "minimum viable product" means.** The term was popularised by Eric Ries and the "lean startup" movement that grew from his book (a way of building new products through short cycles of build, measure and learn). In a 2009 blog post he defined the MVP as the version of a new product that lets a team collect the maximum amount of **validated learning** (what you learn from evidence of real behaviour) about customers with the least effort. The key word is *learning*. It is often misused in two opposite ways:

| Misuse | What happens | Better |
|---|---|---|
| "MVP" means a shoddy version 1 | You learn that broken software annoys people, which you knew | Small in scope, solid in what it does |
| "MVP" grows into everything imagined | Months pass with nothing in users' hands | Cut until it hurts, then check it still does the job |

Henrik Kniberg's widely shared drawing, which goes from a skateboard to a scooter, a bicycle, a motorcycle and on to a car, makes the point: each early version should get a person somewhere, not be one wheel of a car. In his 2016 post on it he suggested other names, such as "earliest testable product". This course says **smallest useful product**, to keep both words in view.

**Three tests for a first product.** A smallest useful product:

1. **Does one job end to end for one group,** in one situation: "counter staff, during the rush, get an order collected when it is ready".
2. **Teaches you the next most important thing:** you can name the assumption it tests (lesson 2.1).
3. **Is safe to use:** it keeps data safe, can be undone, and someone knows when it breaks.

**Story maps.** Jeff Patton described this practice in articles from 2005 and 2008 and set it out at length in his book *User Story Mapping* (O'Reilly, 2014). Across the top, left to right, write the user's **activities** in order: the **backbone**. Under each, write smaller **tasks**, most important first. Then draw horizontal lines to cut **slices**: the first slice takes the most essential item under *each* activity, so it covers the whole journey thinly.

The first slice is sometimes called a **walking skeleton** (a term Patton himself credits to Alistair Cockburn): ugly, slow and partly manual, but it works end to end.

**The scope list.** After slicing, write **In** (this release), **Next** (if the learning goes well) and **Out** (not now, with one line on why). The Out list is the most valuable: it ends the weekly re-opening of the same debate and shows people their request was heard. For a founder's version of the same habit, see [*Founder's Playbook for AI-First Builders*, lesson 2.1 — One job, one customer: scope and the kill list](../founder/index.html#/2.1).

### 🟡 Going deeper

**Choosing a prototype.** Code to answer a question a sketch could answer wastes time; a sketch to answer a question about real behaviour gives false comfort.

| Prototype | Answers questions about | Cannot tell you |
|---|---|---|
| **Paper sketch** (screens drawn by hand) | Whether people understand the flow and find the key action | Real behaviour over time |
| **Clickable mock** (linked screen images) | Layout, wording, order of steps | How it works under a real rush |
| **Concierge** (a person does the job openly) | Whether people value and use the service | Whether software can do it at scale |
| **Wizard of Oz** (looks automated; people behind) | Value when automation matters to the user | Feasibility of the automation |
| **Coded slice** (thinnest real software, few users) | Real behaviour, feasibility, what breaks | Whether the wider market wants it |

**Fidelity** is how close a prototype is to the finished product. Paper invites honest criticism; a polished mock invites comments on colours. Start low.

**Testing a prototype with users.** In a **usability test** a person tries a real task while you watch quietly. Give a task, not a tour ("A customer just ordered two cakes. Let the courier know"). Test in the real setting; note hesitation and errors; do not explain.

How many people? Jakob Nielsen's article "Why You Only Need to Test with 5 Users" (Nielsen Norman Group, 2000) argued that a round of about five users finds most usability problems (about 85% in his model), and that several small rounds with fixes between beat one large test. The article itself says this holds only for comparable users; distinct user groups each need their own testers. Treat it as a habit, not a law.

**Do things by hand behind the product.** At Launch, much of what looks like software can be people, like Maha's morning courier checks (lesson 1.1). Write the manual work down, know its cost (lesson 1.3), and automate it once it is worth it.

**Learning goals and exit criteria.** Each release of a smallest useful product should carry two lines:

- **Learning goal:** "We will learn whether…" (the assumption being tested).
- **Decision point:** "After [time], we will continue, change or stop, based on [measure]."

### 🔴 Expert view

**What not to cut.** Scope is cut from features, not from care. Even the smallest product should:

- **Protect data.** Backups that have been restored at least once; personal data kept to what is needed.
- **Be reversible.** A way to switch a feature off or roll back a release. See [*Founder's Playbook for AI-First Builders*, lesson 5.1 — A launch you can undo](../founder/index.html#/5.1) and, for the engineering, [*SaaS Building Blocks*, lesson 6.3 — Feature flags and experiments](../saas/index.html#/6.3).
- **Have an owner when it breaks.** Someone who will notice and respond, even if that is one person's phone.

**Throwaway or keep?** A coded slice that works tends to stay, because people rely on it. Decide before you build. If you keep it, list the shortcuts you took (**technical debt**: work postponed that must be done later; lesson 9.3). If not, set a date to throw it away.

**Scope by question, not by feature.** Describe a release by the questions it answers ("Will staff tap one button as they take an order?"). A feature that answers none goes to Next or Out.

**AI prototyping.** AI assistants make mocks and slices fast to produce, so the scope list and learning goal matter more: you can now build the wrong thing quicker. See [*AI Product Management*, lesson 5.2 — Prototyping fast and working with ML and AI engineers](../aipm/index.html#/5.2).

**The memorable rule.** Cut across the whole journey, not down one step.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Story map** | Activities left to right, tasks under each, horizontal slices | Before scoping a product or sizeable feature |
| **Scope list** | In, Next and Out, each with a reason | After slicing; at every planning session |
| **Prototype chooser** | The prototype matched to the question | Before building anything "to see if it works" |
| **Usability test script** | A task, a quiet observer, notes, about five people per round | When people must find something new |
| **Release goal note** | Learning goal and decision point | With every release |

## 🏛️ In practice at Qafila
Maha, Faisal and Salma build a story map on a wall. Illustrative and fictional.

> **Story map: getting a shop's order collected when it is ready (Launch, month 4)**
>
> | Shop takes order | Shop says when it will be ready | Courier sees ready time | Courier arrives | Hand-over | Delivered |
> |---|---|---|---|---|---|
> | *Slice 1:* log order (exists) | *Slice 1:* tap "ready in 5 / 10 / 15" on the order row | *Slice 1:* ready time shown on next pickup (no alert) | *Slice 1:* courier decides when to leave | *Slice 1:* courier taps "collected" (exists) | *Slice 1:* "delivered" (exists) |
> | *Out:* predicted prep times | *Out:* per-item prep times | *Out:* live courier map for shops | *Out:* route optimisation | *Out:* photo proof | *Out:* shop feedback on couriers |
>
> **In:** slice 1. **Next:** a courier alert before the ready time, "courier on the way" for shops. **Out (for now):** prediction, a map for shops, shop feedback on couriers, weekly report: none tests the riskiest assumption, and the map and prediction would take most of five weeks.
>
> **Paper test.** Salma tested a sketch with five counter staff at lunch: 3 of 5 looked for the buttons on another screen. Change: larger buttons on the order row itself. Second round, five more staff: all found them within seconds. Then a coded slice for three shops for two weeks.
>
> **Release goal note.** Learning goal: will counter staff tap a ready time for most rush orders, and will courier waits at the counter fall? Decision point: after two weeks at three shops; continue if at least 8 in 10 rush orders get a ready time and the median counter wait (the middle value when all waits are sorted) falls by a third against a baseline week. Counter waits are not recorded today, so each counter keeps a tally sheet of courier arrival and pickup times for the baseline week and the two test weeks.
>
> **Kept despite small scope:** the existing nightly backup (restored once last month as a test), a switch to hide the buttons if something goes wrong, and Salma's phone as the number shops call.

Faisal called the predicted ready time "the clever part". It went on the Out list with the note "needs ready-time data; slice 1 starts collecting it". Slice 1 was estimated at eight working days and took eleven, including the paper tests.

## 🛠️ Exercises
**🟢 Draw a story map.** For an everyday service (booking a sports court, ordering office lunch), write a backbone of five to seven activities and at least three tasks under each, most important first.
*Done when:* the backbone runs from first need to job done, and each column has at least three tasks ordered by importance.

<details><summary>Model answer and self-check</summary>

**Model answer (extract: two of the seven columns shown).** Booking a sports court. Backbone: find a court → check availability → book a slot → pay → get reminded → play → cancel or rebook. Under "check availability": today's free slots (top); filter by time; price per slot. Under "pay": at the venue (top); online; split with friends.

**Self-check.**
- Does the backbone start with the user's need and end with the job done?
- Are the tasks under each activity ordered by what matters most to the user, not by what is easiest to build?

</details>

**🟡 Cut a first slice and write the scope list.** Using your story map (or Qafila's above), draw the first slice: one item under each activity, so the journey works end to end. Write the In, Next and Out lists with one reason for every Out item, and a release goal note.
*Done when:* the slice touches every activity, the Out list has three or more items with reasons, and the goal note names an assumption and a decision point with a measure and a date.

<details><summary>Model answer and self-check</summary>

**Model answer.** First slice: one venue's page, linked from the club chat → today's free slots → book by name and phone → pay at the venue → message the day before → play → cancel by reply. Next: online payment. Out: split payment (complex, few asked), loyalty points (no evidence), league tables (different job). Goal note: "Will players book online instead of phoning? After four weeks, continue if half of bookings come online."

**Self-check.**
- Could a real user complete the whole job with only the first slice, even if parts are manual?
- Is every Out item there for a reason you could explain to the person who asked for it?

</details>

**🔴 Run a five-person paper prototype test.** Sketch the screens for the key action of your first slice and write one realistic task. Test with five people as close to your users as you can find, saying nothing while they try. Record hesitations and failures, change the sketch, and test with at least three more.
*Done when:* you have notes from at least eight sessions across two rounds, a list of the problems found in round one, the change you made for each, and whether round two showed the change worked.

<details><summary>Model answer and self-check</summary>

**Model answer.** Task: "Book the 7 pm court for Thursday." Round one (five people): three missed the day selector; two did not see 7 pm was taken (faint colour); one asked whether to pay now. Changes: days as large buttons, taken slots marked "taken", "pay at the venue" under the Book button. Round two (three people): all booked in under a minute.

**Self-check.**
- Did you give a task rather than explain the screens?
- Did you stay quiet and record hesitation, not just success or failure?

</details>

## ⚠️ Mistakes and traps
- **Building one step perfectly.** A beautiful order screen the courier cannot see teaches nothing. Slice across the journey.
- **Cutting care instead of features.** Keep data protection, reversibility and an owner.
- **High-fidelity mocks too early.** People discuss colours, not the flow. Start on paper.
- **No Out list.** The same features are argued about weekly. Write them down with reasons.
- **Prototypes that quietly become the product.** Decide throwaway or keeper; if a keeper, list the shortcuts.

## 🧾 Recap
- A smallest useful product does one job end to end for one group, teaches you something important, and is safe to use.
- "MVP" means learning with least effort, not careless software or everything at once.
- A story map shows the whole journey; the first slice is the thinnest version that works end to end.
- Match the prototype to the question; test in small rounds and fix between them.
- Rule: cut across the whole journey, not down one step.

## ✍️ Check yourself
**1. Faisal's five-week plan includes the ready button, predicted ready times, a live map for shops, alerts, a shop history screen and a weekly report. Which first slice best follows this lesson?**

- A. A ready-time button on the order row and the time on the courier's next pickup.
- B. A live courier map for shops first, because two shop owners have already asked for one.
- C. Predicted ready times first, because that is the hardest piece and carries most risk.
- D. The shop history screen and weekly report, so shops can see the value Qafila brings.

<details><summary>Answer</summary>

**A.** It is the thinnest slice across the whole journey and tests the riskiest assumption. B rests on two opinions, C builds deep in one step first, and D adds reporting before the core job works. See "Story maps".

</details>

**2. Salma wants to know whether counter staff can find and tap the ready buttons quickly during the rush. Which prototype fits that question best?**

- A. A Wizard of Oz test in which Salma sets ready times herself behind a working screen.
- B. A concierge test in which shops send ready times to Salma by chat message all week.
- C. A paper sketch of the order row, tested at the counter by five staff during lunch.
- D. A coded slice released to all 15 pilot shops and watched for a month before deciding.

<details><summary>Answer</summary>

**C.** A paper sketch in the real setting answers a findability question quickly and cheaply. A and B test value, and D costs far more than the question needs. See "Choosing a prototype".

</details>

**3. To save time on slice 1, Faisal proposes skipping the switch that hides the buttons and pausing the nightly backup. What does this lesson say?**

- A. Accept both, because a smallest useful product cuts scope to what users actually see.
- B. Keep both; the slice can be small, but a backup and an off switch are part of using it safely.
- C. Keep the backup but drop the switch, because the next weekly release is the team's way to undo.
- D. Drop the backup but keep the switch, because the pilot shops' order data can be typed in again.

<details><summary>Answer</summary>

**B.** Data protection and reversibility must not be cut. A confuses small with careless, C leaves no quick undo before the next weekly release, and D risks losing shops' data. See "What not to cut".

</details>

**4. After the first paper test, 3 of 5 staff looked for the buttons on another screen. What is the best next step?**

- A. Run the same sketch with ten more staff, to be sure the problem is real before changing.
- B. Build the coded slice as drawn, since 2 of 5 staff found the buttons without any help.
- C. Add a short training note for shops, explaining where to find the buttons on the order screen.
- D. Change the sketch to put the buttons on the order row, then test with more staff.

<details><summary>Answer</summary>

**D.** Small rounds with a fix in between are the point of quick prototype testing. A repeats a known problem, B ships something most people could not find, and C asks busy staff to learn around a design problem instead of fixing it. See "Testing a prototype with users".

</details>

**5. Faisal says slice 1 already counts as an MVP "because it is cheap and still a bit buggy". Which reply fits this lesson's sense of an MVP?**

- A. "Agreed: a first version is meant to be rough, and we will polish it once shops start paying."
- B. "Not yet: it only becomes an MVP once it has every feature on the plan, so shops see it all."
- C. "It is one if it tests our riskiest belief for little effort; the bugs are a separate thing to fix."
- D. "It is one only once shops would pay for it now; until then it is a prototype for the pilot."

<details><summary>Answer</summary>

**C.** In Eric Ries's definition, an MVP is about learning the most for the least effort; small scope never excuses careless work. A treats "rough" as the point, B describes the misuse where an MVP grows into everything, and D makes revenue the test instead of learning. See "What 'minimum viable product' means".

</details>

## 📚 References
- Ries, E., *The Lean Startup* (Crown Business, 2011); book page: https://theleanstartup.com/book — the MVP definition is from his post "Minimum Viable Product: a guide", Startup Lessons Learned, 3 August 2009: http://www.startuplessonslearned.com/2009/08/minimum-viable-product-guide.html
- Kniberg, H., "Making sense of MVP (Minimum Viable Product)", Crisp blog, 25 January 2016: https://blog.crisp.se/2016/01/25/henrikkniberg/making-sense-of-mvp — the skateboard, scooter, bicycle, motorcycle and car drawing, and the names "Earliest Testable/Usable/Lovable Product".
- Patton, J., *User Story Mapping: Discover the Whole Story, Build the Right Product* (O'Reilly, 2014; with Peter Economy). Patton's earlier post "The new user story backlog is a map" (8 October 2008): https://jpattonassociates.com/the-new-backlog/ — backbone, release slices, and "walking skeleton" credited to Alistair Cockburn.
- Nielsen, J., "Why You Only Need to Test with 5 Users", Nielsen Norman Group, 18 March 2000: https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/ — five users find about 85% of problems; the formula "only holds for comparable users".
- Library course: [*Founder's Playbook for AI-First Builders*, lesson 2.1 — One job, one customer: scope and the kill list](../founder/index.html#/2.1).
- Library course: [*Founder's Playbook for AI-First Builders*, lesson 5.1 — A launch you can undo](../founder/index.html#/5.1).
- Library course: [*SaaS Building Blocks*, lesson 6.3 — Feature flags and experiments](../saas/index.html#/6.3).
- Library course: [*AI Product Management*, lesson 5.2 — Prototyping fast and working with ML and AI engineers](../aipm/index.html#/5.2).

---

# 2.3 — Choosing technology: build, buy, cloud and SaaS
*Level: 🟢 Beginner* · *Prerequisites: 2.2* · *Step: Design*

**After this you can** sort the parts of a product into build, buy, rent or do by hand, explain what a cloud provider looks after and what stays your job, weigh an option by total cost and how hard it is to leave, and record the choice in a short decision record. *Study time: reading about 20 min, hands-on about 90 min (estimate).*

## ⚡ In 60 seconds
- A product mixes parts you **build**, parts you **buy or rent** (cloud services, SaaS, outside APIs), **open-source** parts (software whose code is published for anyone to use and change under a licence) and parts done **by hand** for now.
- **Build what makes you different; buy or rent the rest.** Login, maps, messages and payments rarely make a young product different.
- **Cloud** means renting computing over the network and paying for use. With **managed services** the provider runs components like the database. Security stays shared: your data, access and settings are yours.
- Judge an option by **total cost** (time to learn, run and leave it), not its price tag.
- The rule that matters most: **choose what you can run, afford and leave, and write down why.**
- Biggest trap: exciting new technology for parts that do not need it.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

When a courier's location stops updating, Salma asks Faisal why locations live in a separate database. Early on he picked a fashionable new one "built for location data". It needs its own backups, monitoring and fixes, only he understands it, and it has cost about two weeks.

Then Salma asks: "Where is the list of why we chose each thing?" There is none; every choice is in Faisal's head. And two shops have asked to pay couriers through the app, a bigger choice still. Maha decides to write down every technology decision that matters, past and future, in one place.

## 📐 How it works

### 🟢 The essentials

**Five ways to get any part of a product.**

| Option | Qafila example | Trade-off |
|---|---|---|
| **Build** your own software | Matching orders, ready times and couriers | Full control; you maintain it forever |
| **Assemble open source** and run it | A phone-number library (ready-made code you include in your own) | Free to use; you patch it (install fixes) and update it |
| **Use a managed cloud service** | The main database | Little to run; tied to that provider |
| **Rent a SaaS product or outside API** | Maps, text messages | Fastest; you depend on their prices and uptime (the share of time a service works) |
| **Do it by hand** for now | Maha's morning courier checks | Cheapest to start; does not grow with volume |

**Software as a service (SaaS)** is software you use over the internet on a subscription, run by its provider. An **API** (application programming interface) is a defined way for one program to ask another to do something, such as "send this text message".

**Build what makes you different.** Ask of each part: "Would a customer choose us because of how we do this?" For Qafila, coordinating shops and couriers around ready times might qualify; sending a text message, drawing a map or storing a password does not. Building those takes time from the part that matters and usually gives a worse result. For a one-person founder's version of this choice, see [*Founder's Playbook for AI-First Builders*, lesson 2.2 — Build, buy or borrow](../founder/index.html#/2.2).

**What "cloud" means.** A widely used definition, published by the US National Institute of Standards and Technology (NIST) in 2011 as Special Publication 800-145, names five essential characteristics (on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service) and three service models:

| Service model | You rent | You still look after |
|---|---|---|
| **Infrastructure as a service (IaaS)** | Virtual machines (software computers sharing a physical one), storage, networks | Operating system (the base software, such as Linux), software, data, settings |
| **Platform as a service (PaaS)** | A platform for your code or data, such as a managed database | Your code, data and settings |
| **Software as a service (SaaS)** | A finished application | Your data and who has access |

Further down the table, you run less and can change less. **Managed services** (mostly the PaaS row) suit small teams: the provider handles routine work such as patching and scheduled backups.

**Shared responsibility.** Cloud providers describe a **shared responsibility model**. One large provider's page puts it as security "of" the cloud (its facilities and infrastructure, the provider's job) and security "in" the cloud (data, access, configuration, the customer's job), with the split depending on the services chosen. In plain words: **the provider keeps the building secure; you decide who has keys.** For the engineering detail, see [*Cloud & DevOps: Zero to Hero*, lesson 1.2 — Cloud fundamentals: regions, zones, compute, storage, managed services and shared responsibility](../cloud/index.html#/1.2).

### 🟡 Going deeper

**Total cost, not price.** A rented service shows a price; a self-built part looks free. Count:

| Cost line | Question |
|---|---|
| **Money** | How does the price grow with volume? |
| **Time to set up** | How many days, including learning? |
| **Time to run** | Who patches, monitors and fixes it? |
| **Knowledge risk** | How many people understand it? |
| **Cost to leave** | How long and painful is a move? |

At Launch, people's time is the scarcest resource: a small monthly fee that saves Faisal a day a week is cheap.

**Boring technology.** Dan McKinley's 2015 essay "Choose Boring Technology" argued that a team can afford only a few new, unfamiliar technologies at once; he described them as a small budget of "innovation tokens" ("about three", in his telling). Well-known technologies have known failure modes and many people who understand them. Faisal's location database spent a token on a part that did not need one.

**One app, one repository, to start.** A **repository** stores code and its history (lesson 3.1). Martin Fowler's 2015 article "MonolithFirst" observed that, in the cases he had heard of, almost all successful systems built from many separate services (**microservices**) began as one application (a **monolith**) that grew too big and was broken up, and recommended starting with one. Qafila keeps one repository until Scale-up (Module 8).

**Lock-in and the exit question.** **Lock-in** is how hard it is to leave a provider; some is the price of speed. Ask: can you **export your data**, and have you tried? Is the provider called from **one place in your code**? Can it change **prices or terms** at short notice? Where is data **stored and processed**, and does that matter under the data-protection rules where you operate (a question for someone who knows them)?

For more on vendor costs and lock-in, see [*Founder's Playbook for AI-First Builders*, lesson 7.2 — Costs, vendors and lock-in](../founder/index.html#/7.2).

**A quick supplier check.** Before relying on an outside service, spend half an hour on its charges, uptime history, support, data export and use of your customers' data (more in Module 10).

### 🔴 Expert view

**Easy to undo or hard to undo?** A text-message provider called from one module (one self-contained part of the code) is easy to undo: decide quickly. Where customer data lives, or the database everything depends on, is hard to undo, because moving it means a **migration** (moving data or systems from one place to another): slow down, ask more people, test first.

**Never handle what you do not have to.** Card payments carry rules and risks far beyond their technical difficulty; payment providers exist so that a small company never stores card details itself. When Qafila adds payments at Traction it will use one, and ask someone qualified: "which payment and data-protection rules apply to us, and which does the provider take on?"

**Secrets belong outside the code.** Keys and passwords go in a secret store, each with the least access it needs. Qafila learns this the hard way at Scale-up (Module 8).

**Decision records.** An **architecture decision record (ADR)** is a short note on one significant decision. Michael Nygard proposed a lightweight format in a 2011 article, "Documenting Architecture Decisions": a **title**, the **context**, the **decision**, its **status** (proposed, accepted, deprecated or superseded) and its **consequences**, good and bad. Records live with the code; a changed mind gets a new record that supersedes the old. This lesson adds **options considered** and **how to undo it**. To practise writing one with an AI critic, see [*A Practical Guide to Becoming an AI-Native Engineer*, lesson 11.2 — Lab: an ADR with a critic, docs checked against code and a postmortem that sticks to the facts](../ainative/index.html#/11.2).

**AI in technology choices.** An assistant's knowledge of prices and terms may be wrong or dated: check the provider's pages, and never paste secrets into it.

**The memorable rule.** Choose what you can run, afford and leave, and write down why.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Parts sheet** | Each part of the product with its option and a reason | When starting, and for each new part |
| **Total-cost table** | Money, set-up, running, knowledge risk, cost to leave | Comparing options for one part |
| **Supplier check** | Half an hour on pricing, uptime, support, export, data use | Before relying on an outside service |
| **Decision record (ADR)** | Title, context, options, decision, status, consequences, how to undo | For decisions hard to undo or often asked about |
| **Secret store** | The provider's place for keys and passwords, outside the code | From the first day any key exists |

## 🏛️ In practice at Qafila
Maha and Faisal spend an afternoon writing a parts sheet and the decision log, starting with past decisions. Illustrative and fictional.

> **Parts sheet (Launch, month 5)**
>
> | Part | Option | Why |
> |---|---|---|
> | Order, ready-time and courier matching | **Build** | What makes Qafila different |
> | Merchant app, courier app, admin web page | **Build**, one repository, one application | One thing to deploy weekly |
> | Main database | **Managed service** from the one cloud provider | Backups and patching handled |
> | Courier locations | **Managed service** | Decision 004 |
> | Maps; text messages to couriers | **Rent APIs** | Specialist jobs |
> | Staff login to the admin page | **Managed service** | Never build password handling |
> | Courier assignment checks | **By hand** (Maha, mornings) | Cheap at 150 deliveries a day |
> | Shop payments to couriers | **Not yet** | Decision 006 |
>
> **Decision log (extract)**
>
> **004 — Move courier locations into the main database.** *Status:* accepted (supersedes 002). *Context:* the separate database needs its own backups and monitoring, only Faisal understands it, and it has cost about two weeks; at about 150 deliveries a day the main database handles locations easily in Faisal's test. *Options considered:* keep and document it; move it; rent a tracking service. *Decision:* move it. *Consequences:* one less system; review at Traction. *How to undo:* old database kept read-only for a month.
>
> **006 — Shop payments to couriers through the app.** *Status:* proposed, not before Traction. *Context:* two shops asked; no payments today. *Options considered:* build card handling (rejected: rules and risk far beyond four people); a payment provider; cash for now. *Decision:* cash during the pilot; at Traction a payment provider, after a supplier check and advice on which rules apply. *Consequences:* shops wait; Qafila never holds card data.

Faisal winced at writing 004 about his own choice; Maha reminded him the log is about the system, not blame. Salma read it in twenty minutes and finally understood how Qafila fitted together.

## 🛠️ Exercises
**🟢 Make a parts sheet.** For an app you know well or a project of your own, list at least eight parts (sign-in, payments, messages, search, data storage, the core feature, support…). Choose an option for each, with one line of reason.
*Done when:* every part has an option and a reason, and only the one or two parts that make the product different are marked "build".

<details><summary>Model answer and self-check</summary>

**Model answer.** A study-group booking app. Matching students to rooms by course and time: build (the difference). Sign-in: managed service. Data: managed database. Calendar invites and messages: rent APIs. Room availability: by hand (the librarian updates a sheet daily). Search: the database's built-in search. Support: a shared inbox (SaaS). Usage reports: a rented analytics tool.

**Self-check.**
- Did you build only the parts that make the product different?
- Did you mark anything "by hand", and is that sensible at the product's current size?

</details>

**🟡 Compare two options by total cost.** For one part from your sheet, compare two realistic options (for example a self-run open-source search engine versus the database's built-in search). Fill in the total-cost table for both without inventing prices: use low, medium or high, and say what you would check.
*Done when:* both options have all five lines, and you state your choice for a four-person team and what would change your mind.

<details><summary>Model answer and self-check</summary>

**Model answer.** Self-run open-source search engine: money low (plus a server); set-up medium; running medium; knowledge risk high; leaving easy. The database's built-in search: all low except cost to leave (medium). Choice: built-in search, until quality complaints grow or data outgrows it (checked in the provider's documentation).

**Self-check.**
- Did you avoid inventing prices or limits, and say where you would check them?
- Did running time and knowledge risk count as much as money?

</details>

**🔴 Write two decision records.** Write one record for a choice that is easy to undo and one for a choice that is hard to undo, using the seven lines (title, context, options considered, decision, status, consequences, how to undo it). Use your project, or Qafila's choices of text-message provider and where customer data is stored.
*Done when:* each record fits on half a page with two or more options and one negative consequence, and the hard-to-undo record names who was consulted and one question for an expert.

<details><summary>Model answer and self-check</summary>

**Model answer.** Easy: "007 — Rent a text-message API for courier alerts." Context: couriers need alerts; we send no text messages today. Options: API A, API B, a self-hosted gateway. Decision: API A, called from one module. Status: accepted. Consequences: fast; per-message cost grows; one more supplier. Undo: change one module, about a day. Hard: "008 — Store data in the cloud region nearest our customers." Context: customer data must live somewhere, and rules may restrict where. Options: nearest region; a cheaper distant one. Decision: nearest, pending advice. Status: proposed, pending advice. Consulted: Maha, Faisal, an outside adviser. Expert question: "Do the rules where we operate restrict where this data may be stored or processed?" Consequences: possibly higher cost. Undo: a planned migration, weeks of work.

**Self-check.**
- Did you spend noticeably more care on the hard-to-undo decision?
- Does each record say how to undo it, honestly?

</details>

## ⚠️ Mistakes and traps
- **Building commodity parts.** In-house login, maps or payments take weeks and are rarely better.
- **Spending innovation tokens on plumbing.** Use well-known technology for routine jobs.
- **"The cloud handles security."** Your data, access and settings are yours. Learn the split.
- **Comparing price tags only.** Running time and the cost of leaving often outweigh the bill.
- **Decisions that live in one head.** Write short decision records.
- **Guessing at legal answers.** Write the question down and ask someone qualified.

## 🧾 Recap
- Each part can be built, assembled from open source, run as a managed service, rented, or done by hand for now.
- Build what makes you different; buy or rent the rest, using well-known technology for routine parts.
- Managed services suit small teams; security is shared, and data, access and settings are yours.
- Judge options by total cost, including time and the cost to leave; slow down for decisions hard to undo.
- Rule: choose what you can run, afford and leave, and write down why.

## ✍️ Check yourself
**1. Faisal wants to build Qafila's own text-message system because the rented API "costs money every month". What is the strongest response?**

- A. Agree, because owning the system removes a monthly cost and a supplier from the business.
- B. Agree, if Faisal can finish it within two weeks and write documentation for the others.
- C. Disagree, because no customer picks Qafila for its messaging, and his weeks are better spent elsewhere.
- D. Disagree, because a rented service is always more reliable than one a small team builds.

<details><summary>Answer</summary>

**C.** Messages are a commodity part, and Faisal's time should go to what makes Qafila different. A and B ignore the cost of running it forever, and D overstates with "always". See "Build what makes you different".

</details>

**2. Qafila's main database is a managed service from its cloud provider. Which task is still Qafila's responsibility?**

- A. Physical security of the data centre buildings where the database servers are kept.
- B. Deciding who can access the database and keeping the access keys out of the code.
- C. Fixing the servers and the software the provider runs the managed database on.
- D. Replacing failed disks in the storage that holds the database's files and backups.

<details><summary>Answer</summary>

**B.** Access, configuration and data stay with the customer. A, C and D are the provider's infrastructure, security "of" the cloud. See "Shared responsibility".

</details>

**3. Faisal's location database needs its own backups and monitoring, and only he understands it. Which idea best explains the problem?**

- A. It used one of the team's few innovation tokens on a part that did not need one.
- B. It broke the monolith rule, because every database must be inside the main application.
- C. It was a SaaS product, so Qafila had no control over its prices or its terms of use.
- D. It was open source, so it could not be trusted for a product with paying customers.

<details><summary>Answer</summary>

**A.** Unfamiliar technology adds learning, running and knowledge risk. B misstates the monolith idea, C is wrong because Faisal ran it himself, and D wrongly treats open source as untrustworthy. See "Boring technology".

</details>

**4. Two shops ask to pay couriers by card through the Qafila app during the pilot. What does this lesson suggest?**

- A. Build a simple card form in the main application now, so the two shops need not wait.
- B. Keep card numbers in the managed database, already backed up and access-controlled.
- C. Sign up this week with the cheapest payment provider, since pilot volume is small.
- D. Keep cash for now; later use a payment provider and ask an expert which rules apply.

<details><summary>Answer</summary>

**D.** A payment provider means Qafila never holds card data, and the rules are a question for someone qualified. A and B mean Qafila handles card data itself (B also leans on the provider for a risk that stays Qafila's), and C skips the supplier check and the question of which rules apply. See "Never handle what you do not have to".

</details>

**5. Which pair of decisions deserves the most care before it is made, according to this lesson?**

- A. The maps API and the text-message provider, because couriers rely on both on every delivery.
- B. Where customer data is stored and the main database, because the whole product rests on both.
- C. The staff login service and the phone-number library, because both handle personal details.
- D. The analytics tool and the support inbox, because both collect information about the shops.

<details><summary>Answer</summary>

**B.** Both are hard to undo: moving either means a migration of all the product's data. A and C can each sit behind one module and be swapped in days, and D are rented tools whose data can be exported and moved. See "Easy to undo or hard to undo?".

</details>

## 📚 References
- Mell, P. and Grance, T., *The NIST Definition of Cloud Computing*, NIST Special Publication 800-145, September 2011: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf — five essential characteristics, three service models, four deployment models.
- Amazon Web Services, "Shared Responsibility Model": https://aws.amazon.com/compliance/shared-responsibility-model/ — security "of" the cloud versus "in" the cloud; responsibilities vary with the services used. Named as one provider's description, not an endorsement.
- McKinley, D., "Choose Boring Technology", 30 March 2015: https://mcfunley.com/choose-boring-technology — "Let's say every company gets about three innovation tokens."
- Fowler, M., "MonolithFirst", 3 June 2015: https://martinfowler.com/bliki/MonolithFirst.html — "Almost all the successful microservice stories have started with a monolith that got too big and was broken up".
- Nygard, M., "Documenting Architecture Decisions", Cognitect blog, 15 November 2011: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions — title, context, decision, status, consequences; records kept in the project repository.
- Library course: [*Founder's Playbook for AI-First Builders*, lesson 2.2 — Build, buy or borrow](../founder/index.html#/2.2).
- Library course: [*Founder's Playbook for AI-First Builders*, lesson 7.2 — Costs, vendors and lock-in](../founder/index.html#/7.2).
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 1.2 — Cloud fundamentals: regions, zones, compute, storage, managed services and shared responsibility](../cloud/index.html#/1.2).
- Library course: [*Running IT as a Business*, lesson 5.3 — Third-party, SaaS and open-source components in the product](../itbiz/index.html#/5.3) (the manager's view of the same choices).
- Library course: [*A Practical Guide to Becoming an AI-Native Engineer*, lesson 11.2 — Lab: an ADR with a critic, docs checked against code and a postmortem that sticks to the facts](../ainative/index.html#/11.2).
