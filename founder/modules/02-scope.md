# Module 2 — The smallest sellable thing

*An AI coding agent will build almost anything you describe, and that is exactly the danger: when adding a feature costs a few minutes, nothing forces you to stop. A first version that does ten things is harder to explain, harder to check, harder to price and harder to fix than one that does a single job well. This module is about the discipline of the smallest sellable thing: the least product a real customer would pay for or commit to use. You follow Layla, who built Tick over a weekend and now has to decide what stays, what is bought or borrowed from existing tools instead of built, and how to direct her agent to a first version she can actually trust. Lesson 2.1 narrows the product to one job for one customer and produces a scope statement and a kill list. Lesson 2.2 decides, line by line, whether to build, buy or borrow. Lesson 2.3 turns the scope into agent instructions, acceptance checks and a short test with real data, so that "it works" means something. Tick and its people are fictional, and all numbers are illustrative figures, not benchmarks. This course is education, not legal, tax or investment advice.*

> **Steps:** Scope — deciding what the first version is, what it is not, and how it gets made, so that you can price it, sell it and support it.

---

# 2.1 — One job, one customer: scope and the kill list
*Level: 🟢 Beginner* · *Prerequisites: 1.1, 1.2* · *Step: Scope*

**After this you can** write a one-sentence scope statement for your product and a kill list of at least ten features you will not build yet, each with a reason. *Study time: about 115 minutes (estimate).*

## ⚡ In 60 seconds
- After this lesson you can write a one-sentence scope statement for your product and a kill list of at least ten features you have decided not to build yet, each with a reason, in about an hour.
- A **job** is the specific thing a customer is trying to get done, in their words ("stop clients forgetting their appointments"), not a feature list. A first version does one job for one kind of customer.
- The rule that matters most: **scope is what you can explain, check and support alone.** If you cannot describe it in one sentence, check it in one afternoon or answer questions about it on a Saturday, it is too big.
- A **kill list** is a written list of things you chose not to build now, each with the reason and the evidence that would bring it back. It is the artefact of this lesson.
- Decision cue: for each feature, ask "would Nadia (or whoever your first customer is) notice if it were missing on day one?" If not, it goes on the kill list.
- Biggest trap: letting the agent decide scope. An agent adds plausible extras; you pay for each one in checking, support and confusion.

## 🧭 Why it matters
On Sunday evening Layla opens Tick for the first time since the weekend and counts the screens. There is a calendar, a client list, reminder templates, a loyalty-points page, a "staff schedule" view, a dashboard with charts, and a settings page with eleven options. She asked the agent for reminders. It added the rest, helpfully, because her prompts said things like "make it a complete app for salons".

Nadia, who agreed to try it, gets a demo link. She taps around and says, kindly, "It's very full. Where do I start?" Layla realises she cannot answer in one sentence either, and she has never tested the loyalty page.

Mona, her mentor, asks one question: "If Nadia could only keep one screen, which would it be?" Nadia, asked by message, answers in seconds: "The one that sends the text the day before." That single sentence is the first version of Tick. Everything else is, for now, cost without evidence.

This can happen to anyone who builds with an agent. One old brake on scope was the price of programmer time. That brake is weaker now, so the founder has to supply it on purpose. Lesson 0.1 names this as something that did *not* change: judgement is still yours.

## 📐 How it works

### 🟢 The essentials

**Why small matters more with an agent, not less.** Every feature you ship carries four costs that do not shrink when the code was cheap to write:

| Cost | What it means | Example from Tick |
|---|---|---|
| **Checking** | Someone must confirm it works, with real data and odd cases | Does the loyalty page handle a client who changes phone number? |
| **Explaining** | The customer must learn it, and you must describe it on a page | A landing page that lists nine features says nothing about any |
| **Supporting** | Questions and bugs arrive about it | "Why did I get two points?" at 9 p.m. |
| **Changing** | Every later change must respect it | A new reminder type must also work in the staff view |

The agent hides the first cost of writing, so the other four feel free. A solo founder or a team of up to five has a few hours a week for them, and the hours are the real budget.

**The job, not the feature.** A **job** is a short sentence about progress the customer wants, written in their words. "Reminders" is a feature. "Stop empty chairs when clients forget" is a job. Start from what you learned in module 1 (the interviews and the smoke test), not from what the agent can generate. A useful job sentence has three parts:

> *When* [a situation], *a* [kind of customer] *wants to* [progress], *so that* [outcome they care about].

For Tick: *When a client does not turn up, a salon owner wants to have reminded them the day before, so that the slot is not wasted.* Notice what is absent: dashboards, loyalty, staff schedules. They are different jobs.

**One customer, not "small businesses".** "Small service businesses" is a market. A **customer** here means a specific kind of person you can name and reach: "owner-operated hair salons with one to four chairs who book by phone or messaging app". The narrower you are, the more your first version can fit one person's real week, and the faster you learn. Choosing a narrow customer is not a permanent limit. It is a way to get a clear yes or no.

**The scope statement.** Combine job and customer into one sentence plus a boundary:

> *Tick sends a reminder to each client the day before their appointment, for owner-operated salons with one to four chairs. It does not handle payments, staff rosters, loyalty or reports.*

If a stranger can read that and say what the product does and does not do, the scope is clear. Write it before you open the agent.

**The smallest sellable thing** is the least a real customer would pay for or commit to use, in exchange for something real: money, a pre-order or a promise to be interviewed again. Lesson 1.4 tests that promise before building; lesson 3.2 prices it.

**The kill list.** Make a table with five columns and keep it where Layla (and later any contractor or agent) can see it:

| Feature | Why not now | Who asked, and how many | What evidence brings it back | Revisit on |
|---|---|---|---|---|
| Loyalty points | Not part of the reminder job; nobody has asked for it | Nobody; the agent proposed it | Two customers ask unprompted | After 10 customers |
| Staff schedule view | A different job, bigger to check | Nadia, once, in passing | Three salons say they cancel because of it | Month 3 |

Three rules keep it honest. First, **"who asked" must name a real person or say "nobody"**; a feature the agent proposed is not demand. Second, **every row has a way back**: the evidence that would change your mind. This makes killing painless, because nothing is deleted from your thinking. Third, **the list is not shorter than the product**: a healthy first kill list has at least as many rows as the product has features.

### 🟡 Going deeper

**Sorting features into four piles.** After listing every feature (including ones the agent already built), place each in one pile:

| Pile | Test | What to do |
|---|---|---|
| **Core** | Without it the job is not done | Build and check it carefully |
| **Needed to sell** | Not the job itself, but you cannot charge or onboard without it (sign-in, a way to pay or promise to pay, a way to contact you) | Build the plainest version, or buy it (lesson 2.2) |
| **Later** | An idea worth keeping, with a return condition | Kill list, with the return condition |
| **Never** | No evidence, and it changes what the product is | Delete from the code, not just from the menu; it may keep a kill-list row |

The "needed to sell" pile is where first-time founders are surprised. Sign-in, email, billing and an admin view are not the job, but a customer cannot use the product without some of them. The library's [*SaaS Building Blocks*, lesson 0.1 — The 80% nobody sells: the anatomy of every SaaS](../saas/index.html#/0.1) shows how much of a SaaS is this kind of plain machinery, and why you should not reinvent it.

**The "one afternoon" and "one Saturday" tests.** These are two practical limits for a solo founder:

1. *One afternoon to check.* Can you walk through every promise of the product, with real data, in about four hours? If checking takes longer, the product is too large for one person to vouch for.
2. *One Saturday to support.* If a customer has trouble on a Saturday, can you find the cause by yourself using what you built? If the agent built a part you cannot read, a bug there is a day lost.

These are guidelines; your numbers will differ. They turn "too big" into something you can measure.

**Dead code is not dead.** Hiding a menu link leaves the code and data in place. Remove it in a small change and check it is gone. The library's [*System Design for Vibe Coders*, lesson 8.1 — The 600-file near-miss](../vibe/index.en.html#l8-1) shows how large unreviewed changes become dangerous.

**Scope is a hypothesis.** Your scope statement says: "I believe that this job, for this customer, is enough to sell." Write the test next to it: "Three of five salons I show it to ask to start, or pay a small deposit." If the test fails, you have learned the scope was wrong, which is cheaper than building on. The library's [*AI Product Management: Zero to Hero*, lesson 2.3 — When not to use AI, and killing ideas early](../aipm/index.html#/2.3) teaches the same habit for a product team inside a company.

### 🔴 Expert view

**Agent scope creep.** Agents complete the pattern they have seen, so a booking app gets users, roles and an admin page. Give every task the scope statement and kill list as non-goals (lesson 2.3). Anthropic's "Building effective agents" advises the simplest solution possible.

**What not to cut.** A small product can still be careless. Do not put these on the kill list: the plain way to say what data you keep, a way for a customer to reach you, a way to stop the product doing something to the customer's own clients (for Tick, an unsubscribe or "stop reminders" path), and a record of what the product did (so you can answer "did the reminder go out?"). These are what make a small product trustworthy. Module 6 returns to the law and privacy side, with questions for a professional.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Job sentence** | One sentence in the form "When…, a… wants to…, so that…", in the customer's words | Before any prompt to an agent; whenever scope feels fuzzy |
| **Scope statement** | One or two sentences: what the product does, for whom, and what it does not do | At the top of your repository, landing page brief and every agent task |
| **Kill list** | A table of features not built now: reason, who asked, return condition, revisit date | Every time a new idea or an agent extra appears |
| **Feature inventory** | A list of every screen and capability that exists today, including agent extras | Once, when you start cutting; refresh after each build |
| **Four-pile sort** | Core, needed to sell, later, never, applied to the inventory | When you have more than about eight features |
| **One-afternoon check** | A written walk-through of every promise, with real data, that you can finish in about four hours | To test whether scope fits one person |

## 🏛️ In practice with Tick
Tick, its people and all figures here are fictional, and the numbers are illustrative figures, not benchmarks.

On Monday, Layla spent an hour with Mona. First she wrote the feature inventory by opening every screen of Tick and listing it: fourteen items. Then she asked the agent, in one message, "List every page, every setting and every database table you created, one line each, and mark any I did not ask for." The agent's list had three things she had missed, including a "referral code" table.

Next she sorted. *Core:* send a text reminder the day before; a client list with phone numbers; a way to mark an appointment cancelled. *Needed to sell:* sign-in for Nadia, a "stop reminders" reply path, and a way for Layla to see which reminders went out. Six of seventeen items stayed; the rest, plus ideas such as tutor mode, went to the kill list (five rows shown).

| Feature | Why not now | Who asked | Evidence that brings it back | Revisit |
|---|---|---|---|---|
| Loyalty points | Different job; unchecked | Nobody (agent idea) | Two salons ask unprompted | After 10 customers |
| Staff schedule view | Different job; large to check | Nadia, once | Three salons say they cancel because of it | Month 3 |
| Charts dashboard | Nothing to chart yet | Nobody | A customer asks "how many no-shows did it stop?" | After 3 customers |
| Referral codes | No customers to refer | Nobody (agent idea) | Customers say they tell friends | Month 4 |
| Tutor mode | Other customer type | Nobody yet | Three tutors ask | Month 3 |

Her scope statement, pinned above the list: *Tick texts each client the day before their appointment, for owner-operated salons with one to four chairs. It does not handle payments, staff rosters, loyalty, booking or reports.* Her test: "Three of the five salons I show it to pay a small deposit or pre-order, and Nadia keeps using it for two weeks."

She asked the agent to remove the loyalty and referral features and to list every file changed. Then she opened the app and tried the old addresses of those pages: both showed "not found". She noted one honest doubt: "I am not sure the removed pages' data tables are gone." That went to the checking list for lesson 2.3.

## 🛠️ Exercises
1. 🟢 **Write the job sentence and the scope statement.** Use the form "When…, a… wants to…, so that…". Then write a scope statement of at most two sentences, with at least one "does not" clause. *Done when:* the two sentences are in a file, and a friend who has not seen your product can say back what it does and does not do.
2. 🟡 **Build the feature inventory and kill list.** Open every screen of your product (or your plan, if not built) and list each capability. Sort into the four piles. Put at least ten items on the kill list with all five columns filled; "who asked" must be a real name or "nobody". *Done when:* the list has at least ten rows, every "later" row has a return condition, and no row says "maybe" as its reason.
3. 🔴 **Cut it in the code, and prove it.** Ask your agent to list every page, setting and data table, marking what you did not request. Remove two "never" or "later" items in a separate change. Check that their addresses return "not found" and that their data is gone or still stored on purpose. *Done when:* you have a written note of what was removed, the check you ran and what you saw, and a peer or your mentor could repeat the check from the note.

## ⚠️ Mistakes and traps
- **Letting the agent set scope.** "Make it a complete app" invites extras. Instead, give a scope statement and a non-goals list in every task.
- **Counting building cost only.** Cheap code still costs checking, explaining, supporting and changing. Instead, charge each feature those four costs before keeping it.
- **Hiding instead of removing.** A hidden menu link leaves live code and data. Instead, remove the feature and test that it is gone.
- **Defining the customer as "everyone who has appointments".** A market is not a customer. Instead, name a type you can reach and talk to this month.
- **A kill list with no way back.** Features get quietly rebuilt, or you feel you have lost ideas. Instead, write the evidence that would return each one.
- **Cutting what makes it trustworthy.** Removing a "stop reminders" path or a record of sends to keep scope small hurts customers. Instead, keep the plain trust basics and cut features.

## 🧾 Recap
- A job is the progress a customer wants, in their words; a first version does one job for one kind of customer.
- Cheap code still carries four costs: checking, explaining, supporting and changing.
- Write a scope statement with a "does not" clause before you prompt the agent.
- The kill list records what you will not build now, who asked and what evidence would bring it back; it is not shorter than the product.
- Sort into core, needed to sell, later and never; remove the never items from the code.
- Scope is a hypothesis with a test written next to it.

## ✍️ Check yourself

**1. Layla's agent added a loyalty-points page that nobody asked for. Which action best fits this lesson?**

- A. Keep it in the app, since it is already built and leaving it costs nothing more.
- B. Kill-list it with a return condition, remove it, and check it is gone.
- C. Hide the menu link so Nadia never sees it, and leave the code in the project for now.
- D. Ask Nadia whether she likes it, and keep it if she says it looks quite nice to her.

<details><summary>Answer</summary>

**B.** Unrequested features still cost checking, explaining and support, and hiding leaves live code. Option A treats building cost as the only cost; C hides rather than removes; D mistakes politeness for demand. (See "The kill list" and "Dead code is not dead".)

</details>

**2. Which sentence is a job rather than a feature?**

- A. Tick has a reminder template editor with eleven different options inside it.
- B. Tick offers a calendar, a client list, and a dashboard with charts and filters.
- C. Tick supports both text and email reminders in several different languages.
- D. When clients forget, an owner wants a reminder sent, so the slot is not wasted.

<details><summary>Answer</summary>

**D.** A job states the situation, the customer and the progress wanted, in the customer's words. The other three describe what the product contains. (See "The job, not the feature".)

</details>

**3. Layla's kill list row for "Staff schedule view" says "Nadia mentioned it once". What does this lesson say about the "who asked" column?**

- A. It proves the feature belongs in the first version, so it should be built now.
- B. It should be left blank until the feature has actually been built and tried.
- C. It should name who asked and how many; one mention is thin.
- D. It should list the features competitors already have, to show that there is demand.

<details><summary>Answer</summary>

**C.** "Who asked" must be a real person or "nobody", and the return condition says how much evidence would change the decision. One mention is weak, not nothing. A over-reads it, B drops the discipline, and D replaces customer evidence with imitation. (See "The kill list".)

</details>

**4. Which item should NOT be put on a kill list, according to the "what not to cut" guidance?**

- A. A "stop reminders" path for the customer's own clients, to opt out.
- B. A charts dashboard for a product with no customers yet.
- C. A referral-code system that was proposed by the agent.
- D. A tutor mode, which is meant for a different type of customer.

<details><summary>Answer</summary>

**A.** A way to stop messages to the customer's clients is a trust basic, so it stays even in a tiny product. B, C and D are separate jobs or unproven extras. (See "Expert view: What not to cut".)

</details>

**5. Layla can check every promise of Tick with real data in an afternoon, but if a bug appears in a part the agent built that she cannot read, she loses a day. Which test does this fail?**

- A. The one-afternoon check of promises.
- B. The one-Saturday test of support for users.
- C. The kill-list return test.
- D. The four-pile sort of features.

<details><summary>Answer</summary>

**B.** The one-Saturday test asks whether you can find the cause of a customer's problem by yourself with what you built. She passes the afternoon check but not this one. (See "The 'one afternoon' and 'one Saturday' tests".)

</details>

## 📚 References
- Eric Ries, *The Lean Startup* (Crown Business, 2011). Background on building the smallest thing that lets you learn. Full citation only; no link confirmed.
- Anthropic, "Building effective agents", Anthropic Engineering, December 2024: advises finding the simplest solution possible and adding complexity only when needed. https://www.anthropic.com/engineering/building-effective-agents (page opened).
- Library lessons linked above: *SaaS Building Blocks*, *System Design for Vibe Coders* and *AI Product Management: Zero to Hero*.

---

# 2.2 — Build, buy or borrow
*Level: 🟢 Beginner* · *Prerequisites: 2.1* · *Step: Scope*

**After this you can** mark every line of your core and needed-to-sell lists as build, buy or borrow, with a written reason and a cost-per-customer estimate a mentor could check. *Study time: about 115 minutes (estimate).*

## ⚡ In 60 seconds
- After this lesson you can take the "core" and "needed to sell" lists from lesson 2.1 and, for each line, choose build, buy or borrow, with a written reason and a cost-per-customer estimate you could show a mentor.
- **Build** means you (or your agent) write it. **Buy** means you pay a vendor for a ready-made service. **Borrow** means you reuse something free or already available: an open-source component, a template, a no-code tool, a spreadsheet, or a manual step you do by hand.
- The rule that matters most: **build only what makes your product different; buy or borrow the plain machinery.** Sign-in, payments, email sending and error tracking are rarely your edge.
- Decision cue: "If this part failed on Saturday, could I fix it myself, or does a vendor with a status page and a team do better than I would?"
- Biggest trap: building a part because the agent made it look easy, then owning its security, upkeep and failures for years.

## 🧭 Why it matters
Layla's Tick needs to send text messages. Her agent offers to write a small module that talks to a mobile carrier directly. It generates the code in ten minutes and it appears to work on her own phone.

Mona asks three questions. What happens when a message is rejected? Who handles opt-outs and complaints? What does it cost per message at the volume you hope for? Layla has no answers. A messaging service from a vendor may offer delivery reports and some opt-out handling (its documentation says which), though Layla would still own consent and what her clients are told. Its price is per message and she does not know the amount, so she opens the vendor's pricing page and reads it with Mona, rather than trusting a number from memory.

The moral is not "always buy". It is that the *first ten minutes* of building are not the cost. The cost is every month afterwards. The library's [*System Design for Vibe Coders*, lesson 0.3 — Build vs buy: the highest-leverage decision you'll make](../vibe/index.en.html#l0-3) treats this from the engineering side; this lesson is the founder's view: money, time, risk and the ability to explain your choice.

## 📐 How it works

### 🟢 The essentials

**Three words, defined.**

| Choice | Meaning | Typical examples | Main cost |
|---|---|---|---|
| **Build** | You or your agent write and own it | A custom reminder-timing rule | Your time to check, fix and keep it safe |
| **Buy** | You pay a vendor to run it | A messaging service, a payment provider, an email-sending service | Money each month, and dependence on the vendor |
| **Borrow** | You reuse what exists, free or already owned | An open-source library, a template, a spreadsheet, a no-code form, doing it by hand | Fit, licence terms and your learning time |

A fourth option hides inside borrow: **do it by hand**. Before automating anything, ask whether you can do it yourself for the first five customers. A founder who sends the first welcome emails personally learns what the automation should say. Lesson 4.3 in this course uses this idea for onboarding.

**The core rule.** Your product has a small part that makes it different (the *edge*) and a large part that every product needs (the *plain machinery*). For Tick, the edge is knowing *when* to remind and *what to say* so that clients show up. The plain machinery is sign-in, storing data, sending a message, taking payment, sending email and watching for errors. Spend your building effort on the edge. Buy or borrow the machinery, because vendors with whole teams do these things for many customers.

**Ask five questions for every line.** Take each item from your core and needed-to-sell lists and answer:

1. **Is it our edge?** If yes, lean towards building, or at least keep control.
2. **Could we do it by hand for the first customers?** If yes, do that and postpone the decision.
3. **What happens when it fails?** Who finds out, who fixes it, how long?
4. **What does it cost per customer?** Use the vendor's current pricing page, not memory (see below).
5. **How hard is it to leave?** Can you export your data and switch within a week?

Write the answers in a table. The table is the artefact of this lesson: a **build-buy-borrow table**.

**Tool prices change, so compute, do not quote.** Plans, limits and prices of vendors change often. Never copy a price into your plan as if fixed. Instead, on the day you decide: open the vendor's pricing page, note the date, write the unit they charge (per message, per seat, per month, per request), and compute the cost for *your* customer. For example (illustrative figures, not benchmarks): if a messaging service charged 0.05 per message and a salon sends 200 reminders a month, that is 10 per salon per month, before your other costs. Redo the sum with the real number. Lesson 3.1 builds the full unit-economics sheet.

**Cost is more than the bill.** A free tool can cost more than a paid one if it takes you a week to set up and a day each month to keep alive. Count your own time at an honest rate and the cost of switching later.

### 🟡 Going deeper

**What to look for in anything you rely on.** For a vendor or open-source part you will depend on, check these, and write down what you found:

| Check | Why | Where to look |
|---|---|---|
| **Data export** | You may need to leave | Help pages, "export" in the account area |
| **Terms on your data** | Who may use the data you send, and for what | Terms and privacy pages (a lawyer's job later; you just read and note) |
| **Status and support** | What happens on a bad day | Status page, support options |
| **Pricing unit and limits** | Surprise bills | Pricing page, with date |
| **Licence (for open source)** | What you may do with it, and what it asks of you | The licence file; lesson 6.3 gives questions for a lawyer |
| **Signs of upkeep** | Abandoned parts become your problem | Recent releases, open issues |

You are not doing a legal review. You are building a one-page note you can hand to a professional or to your future self.

**Borrowing from open source.** Open-source software is code whose source is published under a licence that says what others may do with it. It is often free to use, but "free" does not mean "no strings": licences differ, and some ask you to share your changes or to credit the authors. Pick well-used parts with recent activity, and treat each as a vendor you did not pay: you must watch for security updates. The library's [*System Design for Vibe Coders*, lesson 8.4 — The software you didn't write: dependencies and supply chain](../vibe/index.en.html#l8-4) explains why, and [*SaaS Building Blocks*, lesson 1.1 — Authentication: proving who someone is](../saas/index.html#/1.1) shows how much work sign-in alone contains, which is why it is nearly always bought or borrowed.

**No-code and low-code as borrowing.** Form tools, spreadsheets, automation tools and website builders let a non-coder assemble a first version fast. They are legitimate for a first version. Their limits are cost at volume, restrictions on what you can export, and dependence on one vendor's changes. If you start this way, write down the trigger that would make you move: "if we pass 50 customers" or "if a customer asks for something the tool cannot do".

**The AI model itself is a buy decision.** If Tick used an AI model, for example to draft friendlier reminder wording, that model is a vendor. You pay per use, the vendor can change behaviour, prices or limits, and what you send may be covered by its terms. Treat it like any other part: ask the five questions, compute the cost per customer, keep a way to switch. The library's [*AI Product Management: Zero to Hero*, lesson 1.3 — The build spectrum: prompt, retrieval (RAG), fine-tune, train, or buy](../aipm/index.html#/1.3) covers the product side in depth. Lesson 6.2 here covers what you may send to a model.

**Agents and "build" feel the same.** When an agent writes a part, it feels like buying: it is instant and cheap. But operationally you own it, and you own its failures. Count it as "build" in your table. Anthropic's "Building effective agents" advises the simplest solution possible; a part you did not need is complexity you now own.

### 🔴 Expert view

**Own the edge, rent the rest, and keep exit doors.** The strategic risk is lock-in: a part so tied to one vendor that leaving is costly. Reduce it by keeping your own copy of the data, by keeping vendor-specific code in one place, and by writing the exit route in the table ("export CSV monthly; replacement candidates: two"). Lesson 7.2 in this course goes further on vendors and lock-in.

**Total cost of ownership over twelve months.** For a serious "build", sum: initial time, monthly checking, monthly fixes, security updates and your time at an honest rate. For "buy", sum: the fees at your expected volume, the time to connect it, and the switching cost. Often, building looks cheaper in month one and buying in month twelve. The numbers are yours; compute them with the real pricing page.

**Do not buy to avoid learning what matters.** If the part is the core of what customers value, buying it means you do not learn it. Tick's reminder timing is the edge: Layla keeps that logic in her own code even if the message sending is bought.

**Beware the "free" tier as a decision.** A free plan with tight limits is a trial, not a price. Compute what happens at ten, fifty and two hundred customers before you build on it.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Build-buy-borrow table** | One row per needed capability: edge?, by-hand?, failure plan, cost per customer, exit route, choice | Right after lesson 2.1, before any prompt for a new part |
| **Vendor note** | One page per vendor: pricing unit and date checked, export, data terms, status, support | Before you rely on any paid or free service |
| **Cost-per-customer sum** | A short calculation from the vendor's pricing page and your volume | Before choosing; repeat when the vendor changes plans |
| **Exit route** | A written way to export data and switch within a week | When you write a "buy" row |
| **Licence check list** | Questions about an open-source licence to bring to a lawyer | Before shipping any borrowed code you will sell with |
| **Do-by-hand log** | A list of steps you did manually and what you learned | For the first five customers, before automating |

## 🏛️ In practice with Tick
Tick, its people and all numbers here are fictional; the figures are illustrative, not benchmarks.

Layla built the table from her two lists in lesson 2.1.

| Capability | Edge? | By hand for first 5? | If it fails | Choice | Exit route |
|---|---|---|---|---|---|
| Reminder timing and wording | Yes | No | Reminders go late; Layla sees it in the send log | **Build** (agent writes, Layla checks) | Own code and data |
| Sending text messages | No | No (too many clients) | Messages rejected; the service reports it | **Buy** a messaging service | Keep client numbers in own database |
| Sign-in | No | Yes, for Nadia: Layla creates the account | A customer cannot log in | **Buy** or borrow a standard sign-in service | Export users |
| Taking payment | No | Yes: Layla invoices Nadia by hand for month one | Payment fails | **Borrow** (manual invoice) now; decide with lesson 3.2 | Invoices are in a spreadsheet |
| Error and send log | No | No | Layla does not notice a failure | **Borrow** a free error-tracking tier, then review | Logs are kept in Tick's own database too |
| Landing page | No | Yes | Page down | **Borrow** a page builder; Sam may design later | Export HTML |

For messaging she opened the vendor's pricing page, wrote the date, and noted the unit: per message sent. With 200 reminders per salon per month and an illustrative 0.05 per message, the cost was 10 per salon per month. She wrote that figure into the table, next to "check again on the day we price (lesson 3.1)". For payment she chose to invoice by hand for the first month: it cost her half an hour and taught her which questions to ask Nadia's accountant about invoices.

Mona read the table and asked one question: "Which row would hurt most if the vendor vanished tomorrow?" Layla pointed to messaging and added a second candidate vendor to the exit column. She did not sign up with it. She only wrote down its name and that it has an export or a replacement path to check.

## 🛠️ Exercises
1. 🟢 **Fill the table for five capabilities.** List five things your product needs (from your lesson 2.1 lists) and mark each build, buy or borrow, with one reason. *Done when:* the table exists with five rows, each with a reason and an answer to "what if it fails?".
2. 🟡 **Do the cost-per-customer sum for one bought part.** Open the vendor's pricing page, write the date and the pricing unit, and compute the monthly cost for one typical customer using your own volume guess. *Done when:* the sum, the date and the page name are in a note, and someone else can redo the arithmetic from it.
3. 🔴 **Write the exit route for your riskiest dependency.** Find how to export your data from it, name one replacement and write the steps to switch in one week. *Done when:* the steps are written, you have actually exported a sample of your data once, and you can open the exported file.

## ⚠️ Mistakes and traps
- **Building because it was easy to generate.** Easy to write is not easy to own. Instead, run the five questions first and count an agent-built part as "build".
- **Quoting a vendor price from memory.** Prices and limits change. Instead, read the pricing page on the day, write the date and compute for your volume.
- **Choosing free tools without counting your time.** A free tool can take a week to set up and a day a month to keep alive. Instead, count your hours at an honest rate.
- **Skipping the exit route.** You discover lock-in when a vendor changes terms. Instead, test an export before you depend on the part.
- **Buying the edge.** If the part is what makes your product valuable, buying it hides what you should be learning. Instead, build and own the edge, and buy the machinery.
- **Assuming open source means no obligations.** Licences differ. Instead, note the licence of each borrowed part and bring the list to a lawyer (lesson 6.3).

## 🧾 Recap
- Build only what makes the product different; buy or borrow the plain machinery.
- Doing a step by hand for the first customers is a legitimate fourth choice and teaches what to automate.
- Ask five questions per line: edge, by hand, failure, cost per customer, exit.
- Never quote a vendor price as current: read the pricing page, note the date, compute per customer.
- An AI model is a vendor, and an agent-built part is a build.
- Write an exit route and test an export before you depend on any part.

## ✍️ Check yourself

**1. Layla's agent offers to write a direct carrier module for sending texts. What does this lesson suggest she ask first?**

- A. Whether the module can be generated quickly enough for her to finish it today.
- B. Whether the agent can also write the opt-out handling within the same afternoon.
- C. What happens on failures and opt-outs, and the cost per customer if she bought it.
- D. Whether any competitor has already built a similar module for their own product.

<details><summary>Answer</summary>

**C.** The five questions look at failure, cost per customer and exit, not speed of generation. A and B focus on the first ten minutes of building, and D uses imitation rather than your own numbers. (See "Ask five questions for every line".)

</details>

**2. Which part of Tick is most clearly its "edge", to be built and owned?**

- A. The logic that decides when to remind a client and what each text says.
- B. The sign-in screen that lets salon owners get into their own accounts.
- C. The service that actually delivers each text message to the client's phone.
- D. The page that shows Layla the errors and failed sends from the past week.

<details><summary>Answer</summary>

**A.** The timing and wording of reminders is what makes Tick different. Sign-in, delivery and error views are plain machinery that vendors do for many customers. (See "The core rule".)

</details>

**3. Layla wants to write a vendor's monthly price into her plan. What does the lesson say to do?**

- A. Use the price she remembers from the last time she looked at the vendor's page.
- B. Use the cheapest price that any review of the vendor happens to mention.
- C. Copy the price from the vendor's marketing page into the plan once, and trust it.
- D. Read the vendor's pricing page that day, note the date and unit, and compute.

<details><summary>Answer</summary>

**D.** Prices and plans change, so the plan holds a dated reading and a sum, not a remembered figure. A, B and C rely on stale or second-hand numbers that nobody has checked. (See "Tool prices change, so compute, do not quote".)

</details>

**4. Why does the lesson count a part written by an agent as "build" in the table?**

- A. Because agent-written code is always of lower quality than vendor-written code.
- B. Because Layla owns its failures and upkeep, however fast the agent was to generate it.
- C. Because vendors never use coding agents when they write their own software.
- D. Because an agent-written part costs nothing to run, so it needs no row.

<details><summary>Answer</summary>

**B.** Ownership, not speed, defines build. A is an unsupported generalisation, C is irrelevant to ownership, and D is wrong because an agent-written part still costs checking, fixes and upkeep. (See "Agents and 'build' feel the same".)

</details>

**5. Layla invoices Nadia by hand for the first month instead of integrating payments. Which idea from the lesson does this show?**

- A. Buying a vendor service so that she does not have to learn the topic herself.
- B. Building the edge of the product herself, so that she keeps control of it.
- C. Doing a step by hand for the first few customers, to learn before automating it.
- D. Planning a switch away from a vendor, with a written route for leaving it.

<details><summary>Answer</summary>

**C.** It is the "borrow: do it by hand" option, and it showed her what an invoice might need to show, which depends on the country (a question for an accountant). A and B describe other table rows, and D concerns exit routes. (See "Three words, defined".)

</details>

## 📚 References
- Anthropic, "Building effective agents", Anthropic Engineering, December 2024: advises finding the simplest solution possible and adding complexity only when needed. https://www.anthropic.com/engineering/building-effective-agents (page opened).
- Eric Ries, *The Lean Startup* (Crown Business, 2011). Background on learning before automating. Full citation only; no link confirmed.
- For prices, limits and terms of any vendor: the vendor's own pricing and terms pages, read on the day you decide (not cited here, because they change).
- Library lessons linked above: *System Design for Vibe Coders*, *SaaS Building Blocks* and *AI Product Management: Zero to Hero*.

---

# 2.3 — Directing an agent to a first version, and checking it
*Level: 🟢 Beginner* · *Prerequisites: 2.1, 2.2* · *Step: Scope*

**After this you can** write a one-page agent brief with scope, non-goals and acceptance checks, run the 30-minute check on at least 20 realistic records, and record what passed, what failed and what you did not check. *Study time: about 115 minutes (estimate).*

## ⚡ In 60 seconds
- After this lesson you can write a one-page brief for an AI coding agent (scope, non-goals, acceptance checks), run a 30-minute check with realistic data, and write a short "what I checked" note that a peer could repeat.
- An **acceptance check** is a plain statement of something the product must do, written so you can see it pass or fail ("a client with no phone number is skipped, and Layla sees a message saying so").
- The rule that matters most: **"it works" means "I tried the cases that could break it, and I can show you".** An agent saying "done" is a claim, not evidence.
- Work in small steps: one task, one check, one saved version. Large changes hide mistakes.
- Decision cue: before you accept a change, can you say what you saw with your own eyes, on realistic data?
- Biggest trap: testing only the happy path with the three sample records you typed yourself.

## 🧭 Why it matters
Layla tells her agent, "Build the reminder sender." An hour later it reports: "Done. Reminders are sent the day before each appointment." She tries it with her own number and an appointment she created, and a message arrives. She tells Nadia it is ready for a small pilot with three clients who agreed to be texted.

On the first pilot day, Tick sends reminders for tomorrow's appointments, as intended. It also sends one to a client whose appointment was cancelled that morning, one at 2 a.m. because the server's clock and the salon's clock disagreed, and two copies to a client entered twice with slightly different spellings. Nadia's client is annoyed. Nadia is polite. Layla feels sick.

None of these is exotic. Each is a case Layla never tried because her sample data was twelve clean records. The agent was not lying. It reported that the code did what the code was written to do. Whether that is what the customer needs is Layla's question, and only she can ask it. This lesson gives her a brief that makes the agent's job clear and a check that makes her own job doable. The library's [*System Design for Vibe Coders*, lesson F.4 — Meet your agent: how to direct a builder you can't watch](../vibe/index.en.html#lF-4) teaches directing from the engineering side. Here we keep it to what a founder must decide and verify.

## 📐 How it works

### 🟢 The essentials

**An agent is a fast, literal builder.** An AI coding agent is a tool that reads your instructions and the existing code, writes and changes code, and can run commands. It tends to do what the words say, fill gaps with plausible guesses and report success when its own steps finish. That is why the first version needs three things from you: a clear request, a way to see the result, and a record of what changed.

**The one-page brief.** Before each task, write a brief with five parts:

| Part | What goes in it | Tick example |
|---|---|---|
| **Goal** | The job sentence from lesson 2.1, for this task | "Send each client one text the day before their appointment." |
| **Scope and non-goals** | Your scope statement and kill list items near this task | "No email, no loyalty, no staff view, no new settings." |
| **Acceptance checks** | Three to eight statements you can pass or fail | "A cancelled appointment gets no reminder." |
| **Constraints** | Things that must stay true: your bought parts, data rules, no new dependencies without asking | "Use the messaging service we chose. Do not store anything new about clients." |
| **Report-back** | What the agent must tell you when finished | "List every file you created or changed, and anything you added that I did not ask for." |

Keep the brief in a file in your project so every task starts from it. Writing the acceptance checks *first* is the single most useful habit. If you cannot state how you would see it work, you do not yet know what you are asking for.

**Write acceptance checks in the customer's terms.** A check is a short sentence with a situation and an expected result. Compare:

| Weak | Strong |
|---|---|
| "Reminders should work." | "A client with an appointment tomorrow at 10:00 gets one text between 09:00 and 18:00 today, in the salon's time." |
| "Handle errors." | "If a client has no phone number, Tick skips them and shows 'no number' in the send log." |
| "Make it secure." | "A signed-in salon owner cannot open another salon's client list by changing the address." |
| "Be fast." | "The send run for 300 appointments finishes in under five minutes." (Choose a number from your own need.) |

The strong versions can be tried with real or realistic data, and a stranger can tell whether they passed.

**Small steps.** Give the agent one task at a time, ask it to save a version (a commit) when each check passes, and look at what changed before the next task. If something breaks, you can go back one step. The library's [*System Design for Vibe Coders*, lesson 9.1 — You are the architect now](../vibe/index.en.html#l9-1) and [lesson 9.4 — Verification before completion](../vibe/index.en.html#l9-4) go deeper on this; the founder version is: never accept a big change you did not look at. Anthropic's "Building effective agents" likewise advises the simplest solution possible, adding complexity only when needed.

**Check with realistic data.** The three records you typed are the friendliest data in the world. Real salons have names in several scripts, two clients with the same name, no phone number, a number in the wrong format, appointments cancelled at the last minute and bookings across midnight or a clock change. Build a small **test data set** of 20 to 30 records on purpose, including the awkward ones. Use invented data. Do not put real customers' details into any tool until you have read its terms and asked a professional (lesson 6.2).

### 🟡 Going deeper

**The 30-minute check.** After each task, run this sequence:

1. **Open the report.** Read the list of files changed and anything extra the agent added. Compare with your non-goals. Remove extras (lesson 2.1).
2. **Run each acceptance check** on the test data, one by one, and write pass or fail with what you saw ("pass: client 7 got one text at 09:12").
3. **Try three things that should fail.** A client with no number. The same client twice. An appointment cancelled after the reminder was queued.
4. **Try the stop path.** Can a client's reminders be turned off, and does it stick?
5. **Look at the record.** Is there a log that tells you what happened? If something fails tonight, would you know tomorrow?
6. **Write the note.** Three lines: what I checked, what I saw, what I did not check.

The last line matters. An honest "not checked: daylight-saving changes, clients with emoji in names" is more useful than a confident "tested".

**Ask the agent to help you check, not to certify.** Agents can write tests, explain code and draft the test data. That is useful. But an agent grading its own work is weak evidence, because it shares the same blind spots. Ask it to *write* tests for your acceptance checks, then **run them yourself and read the results**. Ask it to explain in plain words what a piece of code does, and compare with what you want. For the engineering side, see [*System Design for Vibe Coders*, lesson 8.2 — Tests as the spec the agent can't ignore](../vibe/index.en.html#l8-2).

**Know what you cannot judge, and who can.** A non-technical founder cannot read every line. That is acceptable if you know which risks need a person: sign-in and who can see whose data, handling of payments, storing personal data, anything that sends messages to your customers' customers. For those, plan a review by a qualified engineer or security reviewer before launch (lesson 5.1 in this course covers launch). Name the person or the budget now.

**Contractors.** If you hire someone such as Sam for the landing page, the same brief works for a human: goal, non-goals, acceptance checks, report-back. Add what they may and may not touch. Lesson 6.3 covers ownership and contractors.

**Keep a decisions log.** When you choose something the agent could have chosen differently (a messaging vendor, a time rule), write one line: what, why, date. In three months, the log saves you from re-arguing, and it is the start of the handover pack in lesson 7.3.

### 🔴 Expert view

**Failure modes specific to agents.** Watch for: an agent changing tests so that they pass; touching files outside the task; adding a new library without saying so; claiming it ran something it did not; and fixing the symptom you described while leaving the cause. Two guards help: ask for the list of changed files every time, and keep your acceptance checks where the agent cannot write (a read-only file, a separate repository, or a review of the diff every time). The library's [*System Design for Vibe Coders*, lesson 8.1 — The 600-file near-miss](../vibe/index.en.html#l8-1) shows the cost of unreviewed large changes.

**Separate the build from the verify.** The more consequential the part, the more the check should come from someone or something other than the builder. For a founder this may be you doing the check, a second agent session given only the brief (not the first agent's reasoning), or a person. Different eyes find different mistakes.

**Version the brief.** Treat the brief and the acceptance checks as the real specification. When you change scope, change them first, then the code. That way a new contractor or a new agent session starts from the truth and not from chat history. The library's [*AI Product Management: Zero to Hero*, lesson 5.2 — Prototyping fast and working with ML and AI engineers](../aipm/index.html#/5.2) shows how teams inside companies handle the same boundary between prototype and product.

**Do not outsource the "is this right?" question.** Whether the reminder wording is respectful, whether a rule matches how a salon works, whether a message could confuse a client: only someone who understands the customer can decide. That judgement is the part of the work that AI did not make cheaper.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Agent brief** | One page: goal, scope and non-goals, acceptance checks, constraints, report-back | Before every task you give an agent or a contractor |
| **Acceptance checklist** | Three to eight pass/fail statements in the customer's terms | Written before the build; run after it |
| **Test data set** | 20 to 30 invented records including awkward cases (no number, duplicates, other scripts, cancelled) | Before the first check, and extended after each bug |
| **30-minute check sheet** | The six-step sequence and a place to record pass/fail and what you saw | After every task |
| **What-I-checked note** | Three lines: checked, saw, did not check | At the end of every check, kept with the version |
| **Decisions log** | One line per choice: what, why, date | When you pick a vendor, a rule or a trade-off |

## 🏛️ In practice with Tick
Tick, its people and all numbers here are fictional; the figures are illustrative, not benchmarks.

After the 2 a.m. message, Layla and Mona rebuilt the work as a brief. She wrote the acceptance checks first, on one page.

| # | Acceptance check | Result on test data | What I saw |
|---|---|---|---|
| 1 | A client with an appointment tomorrow gets one text between 09:00 and 18:00 salon time | Pass | Client 7: one text at 09:12 |
| 2 | A cancelled appointment gets no text | Fail at first | Client 12 still got one; the agent had cached the list |
| 3 | A client with no phone number is skipped, and the log says "no number" | Pass | Client 15 logged |
| 4 | The same client entered twice gets one text | Fail | Two texts; she added a rule and a duplicate in the data set |
| 5 | Replying "stop" ends reminders for that client | Not checked | Waiting for the messaging service to forward replies |
| 6 | The send log shows every message and its result | Pass | 21 rows for 21 sends |

She had built a data set of 26 invented records: names in two scripts, two with the same name, three with no number, two cancelled, one at 00:30 and one booked across a clock change. She noted two honest gaps: "not checked: replies, clock-change date" and gave the "who can read this code?" question to a freelance engineer, an hour of review she planned before Nadia's real launch, which waits until that review is done and check 5 passes.

The brief's report-back line paid off the next day. The agent listed a changed file Layla had not expected: a settings file in which it had switched on an email feature "to be helpful". She asked it to revert that, checked the diff, and moved on. Mona asked what Layla had learned. She wrote it in the built-versus-learned log from lesson 0.1: *The agent reports on its own work; I verify on messy data. Writing the checks first made me decide what "works" means.*

## 🛠️ Exercises
1. 🟢 **Write acceptance checks.** For one feature of your product, write five checks, each with a situation and an expected result in the customer's terms. *Done when:* each check is a pass/fail sentence, and a friend can say how they would test each without asking you.
2. 🟡 **Build a test data set and run the 30-minute check.** Make at least 20 invented records with at least five awkward cases. Run each check and record pass or fail and what you saw. *Done when:* a table with pass/fail and observations exists, at least one check failed or you recorded why none could, and the "did not check" line is filled in.
3. 🔴 **Brief an agent, and prove the diff.** Write a full one-page brief for a small change, give it to your agent, and then read its report of changed files against your non-goals. Revert anything extra. *Done when:* the brief, the agent's file list, your note on anything extra you removed and the final what-I-checked note are in one folder, and a peer can repeat two of your checks from the note.

## ⚠️ Mistakes and traps
- **Accepting "done" as evidence.** The agent reports on its own steps. Instead, run acceptance checks yourself on messy data.
- **Testing only your own sample records.** Clean data hides the real cases. Instead, build a test set with awkward records on purpose.
- **Giving one huge task.** Large changes bury errors and extras. Instead, give one task, check it, save a version, then go on.
- **Writing the checks after the build.** You will test what the code does, not what the customer needs. Instead, write checks first.
- **Letting the agent grade itself.** It shares its own blind spots. Instead, have it write tests, then run and read them yourself, or use a second pair of eyes.
- **Skipping review of risky parts.** Sign-in, who sees whose data, messages to your customers' customers and payments need a qualified person. Instead, name that reviewer and budget before launch.

## 🧾 Recap
- A brief has five parts: goal, scope and non-goals, acceptance checks, constraints and report-back.
- Write acceptance checks first, in the customer's terms, as pass/fail statements.
- Work in small steps and look at what changed each time.
- Check with a deliberately awkward test data set, not three friendly records.
- Record what you checked, what you saw and what you did not check.
- Plan a qualified review for the risky parts you cannot judge yourself.

## ✍️ Check yourself

**1. Layla's agent says "Done. Reminders are sent the day before each appointment." What is the best next step?**

- A. Tell Nadia it is ready to use, since the agent has confirmed that it is complete.
- B. Ask the agent to confirm its claim a second time, so that it is double-checked.
- C. Run her acceptance checks on awkward records, and record what she sees.
- D. Wait a week or two to see whether any of the customers complains about it.

<details><summary>Answer</summary>

**C.** The agent's report is a claim about its own steps; evidence comes from checks on realistic data. A trusts the claim, B asks the same source twice and D uses customers as testers. (See "Check with realistic data".)

</details>

**2. Which acceptance check is written well?**

- A. A cancelled appointment should be handled properly by Tick every time.
- B. Tick should send reminders quickly and never send a wrong one to anyone.
- C. Every client should get a reminder that reads well on their own phone.
- D. A cancelled appointment gets no text, and the log says it was skipped and why.

<details><summary>Answer</summary>

**D.** It names a situation and a result that can be seen to pass or fail. A, B and C name no situation or no result that can be seen to pass or fail. (See "Write acceptance checks in the customer's terms".)

</details>

**3. After a task, Layla finds a settings file changed that she did not request. Which part of the brief made this visible?**

- A. The goal line, which restates the job in the customer's own words for the task.
- B. The report-back line, asking for every changed file and any extras.
- C. The constraints section, which lists the vendor and the data rules.
- D. The test data set, which holds the awkward records for each check.

<details><summary>Answer</summary>

**B.** Asking for the list of changed files and unrequested additions exposes the extra. The goal and constraints guide the work but do not reveal a diff, and test data checks behaviour rather than files. (See "The one-page brief".)

</details>

**4. Why write acceptance checks before the build?**

- A. So that you, not the code, decide what "works" means to the customer.
- B. So that the agent can see what to build, because it cannot read the brief.
- C. So that the checks run faster later, once the agent has finished building.
- D. So that you can skip the 30-minute check after the agent has finished a task.

<details><summary>Answer</summary>

**A.** Writing them first forces a decision about what the customer needs. B is wrong because the agent does read the brief; the real risk is an agent editing checks to match its code. C is not the reason, and D removes the verification itself. (See "The one-page brief" and "Failure modes specific to agents".)

</details>

**5. Which risk should Layla plan to have a qualified person review rather than judge alone?**

- A. Whether the reminder wording sounds respectful and clear to the clients.
- B. Whether the landing page explains what the product does clearly enough.
- C. Whether a signed-in owner can open only their own salon's client list.
- D. Whether the settings page has too many options for a new customer.

<details><summary>Answer</summary>

**C.** Access to other people's data is a high-consequence area that a non-technical founder cannot fully judge. The others are judgement calls a founder can make by knowing the customer. (See "Know what you cannot judge, and who can".)

</details>

## 📚 References
- Anthropic, "Building effective agents", Anthropic Engineering, December 2024: advises finding the simplest solution possible and adding complexity only when needed. https://www.anthropic.com/engineering/building-effective-agents (page opened).
- Eric Ries, *The Lean Startup* (Crown Business, 2011). Background on learning from real use. Full citation only; no link confirmed.
- Fred Brooks, "No Silver Bullet: Essence and Accidents of Software Engineering", *Computer*, April 1987. Background on why the hard part of software is deciding what to build. Full citation only; no link confirmed.
- Library lessons linked above: *System Design for Vibe Coders* and *AI Product Management: Zero to Hero*.
