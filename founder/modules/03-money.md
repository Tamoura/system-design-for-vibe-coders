# Module 3 — Money

*A product that people use is not yet a business. A business is a product where, on average, what a customer pays is more than what it costs to serve them, and where the cash arrives before the cash runs out. AI makes the first version cheap to build and can make every later month surprisingly expensive to run, because each use of a model has a cost. This module is the founder's money toolkit, in plain words. Lesson 3.1 works out what one customer costs and earns you, including the cost of AI models. Lesson 3.2 turns that into a price, a way to test it and a way to change it without hurting the customers you already have. Lesson 3.3 follows the cash itself: how long your money lasts, how invoices work, and what to bring to an accountant. You follow Layla and Tick. Tick and its people are fictional, and every number is an illustrative figure, not a benchmark. This course is education, not legal, tax, accounting or investment advice: rules differ by country and change, and wherever the money touches tax or the law, the lesson gives you the questions to ask a qualified professional, not answers.*

> **Steps:** Price — working out what it costs to serve a customer, what to charge, and whether your cash lasts, so that selling in the next module rests on numbers you understand.

---

# 3.1 — Unit economics in plain words, including AI and model costs
*Level: 🟡 Intermediate* · *Prerequisites: 1.4, 2.2* · *Step: Price*

## ⚡ In 60 seconds
- After this lesson you can fill in a one-page **unit-economics sheet** for one customer per month: what the customer pays, what each part costs to serve, what is left, and how many months it takes to earn back what it cost to win them. Allow about two hours.
- **Unit economics** means the money story of one customer (the "unit"): revenue in, cost to serve out, and cost to acquire them. If one customer does not work on paper, a thousand will not work either.
- The rule that matters most: **count every use as a cost.** Messages, payments, storage and AI model calls all cost something each time they run. Free to build is not free to run.
- AI cost behaves differently from hosting cost: it grows with how much each customer uses the product, not with how many customers you have. A few heavy users can cost more than many light ones.
- Decision cue: if your margin disappears when one customer uses the product ten times more than average, you do not have a price yet, you have a hope.
- Biggest trap: using last month's vendor price from memory, or leaving out your own time. Read the pricing page on the day and write the date.

## 🧭 Why it matters
Layla's pilot in lesson 1.4 worked: Nadia and one other salon owner paid the pilot deposit, and three more booked calls, before the full version existed. Layla is delighted, and then Mona asks a plain question: "When Nadia pays you, what is left?"

Layla knows Tick sends text reminders and, since last week, uses an AI model to write friendlier reminder wording for each client. She does not know what either costs per salon. The agent built the wording feature in an afternoon and she has never opened the model vendor's bill. Mona does not give her the answer. She asks her to open the pricing pages, write down the date, and work it out on one sheet of paper.

The result is not a disaster, and not a triumph. It is a number she can finally reason about: a margin she can see, a customer who would hurt it, and a part of the bill she did not know was there. The library's [*AI Product Management: Zero to Hero*, lesson 8.2 — Unit economics: cost to serve, pricing models and margins](../aipm/index.html#/8.2) covers cost to serve inside a company. This lesson is the founder's version: small, hand-checkable, and tied to the decision of what to charge in lesson 3.2.

## 📐 How it works

### 🟢 The essentials

**The sheet has three parts.** For one customer in one month, write down:

1. **Revenue.** What this customer pays you per month. If they pay yearly, divide by twelve.
2. **Cost to serve.** What it costs you each month to deliver the product to that customer.
3. **Cost to acquire.** What it cost you, once, to win that customer.

**Gross margin** is revenue minus cost to serve, often shown as a percentage of revenue. It is the money left to pay for everything else: your tools, your time, your own pay, and winning the next customer. **Contribution per month** is the same number in currency, not percent. A business with a thin or negative gross margin cannot fix it by growing; it only loses money faster.

**Two kinds of cost.** A **variable cost** rises with each use or each customer: a text message sent, a payment fee, an AI model call. A **fixed cost** is paid whether you have one customer or fifty: a domain name, a monthly tool subscription, hosting at a basic level. For unit economics, put variable costs in "cost to serve" and keep fixed costs on a separate list. Lesson 3.3 uses the fixed list to find break-even.

**The honest list of variable costs for a product like Tick.** Go through the whole path of one customer's month and write a line for each:

| Cost line | What triggers it | How to find the number |
|---|---|---|
| **Messages** | Each reminder sent | Messaging vendor's pricing page: the unit (per message, per segment, per country) and the date |
| **AI model calls** | Each time the model writes, summarises or answers | Model vendor's pricing page: price per amount of text processed (tokens), input and output priced separately |
| **Payment fees** | Each payment taken | Payment provider's pricing page: often a percentage plus a fixed amount per payment, but read yours |
| **Storage and bandwidth** | Data stored, files served | Hosting or storage pricing page; usually small at the start |
| **Support time** | Each question or problem | Your own minutes per customer per month, at an honest hourly rate |

Never copy these prices from memory or from an article. Vendors change plans, units and limits. Open the pricing page, write the date and the unit, and compute for your volume.

**Tokens, in plain words.** A **token** is a small piece of text, roughly a short word or part of a word, that an AI model reads or writes. Model vendors commonly charge per amount of text processed, with the text you send in (**input**) and the text the model writes back (**output**) priced separately, and with discounts for certain features such as reusing earlier text (caching). Anthropic's pricing page, one example among several vendors, is organised this way: a price per million tokens for input, for output, and for cached input. Whatever vendor you use, check its page for its own units. The library's [*AI Product Management: Zero to Hero*, lesson 1.2 — Capabilities and limits: errors, hallucination, context, latency and cost](../aipm/index.html#/1.2) explains tokens and context from the product side.

**Cost to acquire.** Add up what it took to win your first customers: your hours (at an honest rate, even if you pay yourself nothing), any ads, any tool you bought only for selling, any free months you gave. Divide by the number of customers won. For a first batch of five, this is rough, and that is fine. It is better to be roughly right than precisely unknown.

**Payback.** **Payback period** is how many months of contribution it takes to earn back the acquisition cost: acquisition cost divided by monthly contribution. Short payback means the business gets its money back quickly.

**Churn and lifetime.** **Churn** is the share of customers who leave in a month. If 5 in 100 leave each month, churn is 5 percent, and the average customer stays about 1 divided by 0.05, or 20 months. This is a rough rule, and with few customers it is a guess, not a forecast.

### 🟡 Going deeper

**Why AI cost is different.** Hosting, messages and payments mostly track the number of customers or events. Model cost tracks **how much text goes through the model**. That depends on four things you control:

- **Prompt size.** Everything you send in each call is billed as input. A long instruction, a pasted customer record or a whole conversation history is paid for on every call.
- **Output length.** Longer answers cost more, and output may be priced differently from input.
- **Number of calls per task.** Retries, "regenerate", checking steps and agents that call tools several times multiply the cost of one task.
- **Which model you choose.** Vendors offer larger and smaller models at very different prices. The library's [*Building AI Applications & Agents*, lesson 14.2 — Cost, latency and reliability engineering: budgets, caching, routing, retries and SLOs](../aiapps/index.html#/14.2) goes deep on budgets and routing; here you only need the founder's habit of measuring one real task.

**Measure, do not guess.** The simplest method is to run one typical task, look at how many tokens went in and out (the vendor's usage dashboard or the response itself shows this), and multiply by the vendor's current prices. Do it for a typical customer and again for a heavy one.

**Conversations grow.** In a chat feature, each new message usually resends the earlier conversation, so a ten-message chat costs far more than ten times a one-message chat. If you offer a chat or an assistant, price and cap it with this in mind.

**A margin check you can run in your head.** After computing contribution, test three "what ifs" on your sheet: a heavy customer (ten times the average use), a price rise from the vendor (double any one line), and a free customer (revenue zero, cost unchanged). If any one of them pushes the total below zero, decide now whether to cap use, change the plan or change the price.

### 🔴 Expert view

**Spending limits protect cash.** Check whether each vendor offers a budget alert or a hard limit on usage-based bills, turn it on if it does, and note the limit in your sheet. A runaway loop in an agent, or one abusive account, can otherwise produce a large bill before you notice. The library's [*System Design for Vibe Coders*, lesson 5.2 — Rate Limiting That Survives a CDN](../vibe/index.en.html#l5-2) explains how to limit how much one user can consume.

**Vendor price changes are a business risk.** The library's [*System Design for Vibe Coders*, lesson 11.4 — Cost Engineering](../vibe/index.en.html#l11-4) covers the engineering levers for cutting model cost; your job is to decide which margin is acceptable. If one model vendor's price or behaviour change would wreck your margin, write that on the sheet as a risk, with what you would do: switch model, raise the price, cap use. For how metering and usage-based billing are implemented, the library's [*SaaS Building Blocks*, lesson 3.3 — Usage-based billing and metering](../saas/index.html#/3.3) is the engineering companion.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Unit-economics sheet** | One page for one customer per month: revenue, each variable cost with its source and date, contribution, acquisition cost, payback | After lesson 2.2 and before you set a price; redo whenever a vendor changes its plan |
| **Cost-to-serve ledger** | A table of every variable cost line with unit, source page, date checked and your volume assumption | When you add any feature that triggers a paid service or an AI call |
| **Token-count test** | One typical task and one heavy task run through the model, with input and output tokens read from the usage view and multiplied by the current prices | Before you price any feature that calls a model |
| **Heavy-user stress test** | The three "what ifs": ten times the use, a doubled vendor price, a free customer | Before you publish a price or a free plan |
| **Spending-limit note** | The budget alerts and hard limits you set at each usage-billed vendor | The same day you add a usage-billed vendor |
| **Acquisition-cost log** | Hours, money and free months spent to win each customer, at an honest hourly rate | From the first outreach; review after each batch of customers |

Tools are examples, not endorsements. A plain spreadsheet is enough for all of them.

## 🏛️ In practice with Tick
Tick, its people and all numbers are fictional; the figures are illustrative, not benchmarks.

Layla opened the vendors' pricing pages with Mona, wrote the date beside each unit and built the sheet. She planned to charge 29 per salon per month, a figure she picked quickly and tests properly in lesson 3.2.

| Line | Working (per salon per month) | Amount |
|---|---|---|
| Revenue | 1 salon at the planned price | 29.00 |
| Messages | 200 reminders at an illustrative 0.05 each | 10.00 |
| AI wording | 200 messages, about 600 tokens in and 100 out each; illustrative prices of 3 per million input and 15 per million output tokens | 0.36 + 0.30 = 0.66 |
| AI retries and regenerations | Assume the model is called twice per message on average, so double the line above | 1.32 in total for AI |
| Payment fee | An illustrative 3 percent plus 0.30 per payment on 29.00 | 1.17 |
| **Cost to serve** | 10.00 + 1.32 + 1.17 | 12.49 |
| **Contribution** | 29.00 − 12.49 | 16.51 (56.9 percent) |
| Support time | Layla's 20 minutes a month at an honest 15 per hour | 5.00 |
| **Contribution after time** | 16.51 − 5.00 | 11.51 (39.7 percent) |

Then the acquisition side. Winning the first five salons took about 40 hours of Layla's time at the same honest 15 per hour, 600 in all, so 120 per customer. Payback on contribution before time: 120 divided by 16.51 is about 7.3 months. With support time included: 120 divided by 11.51 is about 10.4 months. With an illustrative steady churn of 5 percent a month, the average stay is about 20 months, so the customer earns back the acquisition cost, but not by a wide margin.

Then she ran the stress test. If a salon used the AI wording ten times more (a heavy user who regenerates constantly), the AI line becomes 13.20 and cost to serve 24.37, leaving contribution of 4.63, still positive but thin. If the model vendor doubled its prices, the AI line goes from 1.32 to 2.64, a small change. The messaging line, 10.00, was the one that mattered: it was most of the cost, and it grew with every salon's client list. Layla had worried about AI cost, the part that felt new, while the old-fashioned cost was bigger.

Mona asked what Layla would do if a large salon sent 2,000 reminders. Layla's answer, written on the sheet, was a plan limit and a per-message charge above an included amount, an idea she takes into lesson 3.2. She also set a spending limit at both usage-billed vendors, and noted both pricing pages with the date.

## 🛠️ Exercises
1. 🟢 **List your cost lines.** Walk through one customer's month in your product and write every variable cost: messages, payments, storage, AI calls, your own time. *Done when:* a list exists with at least five lines, each naming the vendor or activity that triggers it and the pricing unit.
2. 🟡 **Fill the unit-economics sheet.** Open each pricing page, write the date and compute revenue, cost to serve, contribution and margin for one typical customer, then compute payback from your own acquisition-cost log. *Done when:* the sheet is saved, every price has a source and a date, and a friend can recompute the margin from it with a calculator.
3. 🔴 **Stress-test it.** Run a real typical task and a heavy task through your model, read the token counts, and apply the three "what ifs" (ten times the use, a doubled vendor price, a free customer). Set a spending limit or budget alert at each usage-billed vendor. *Done when:* the test results are in the sheet, you can say which what-if hurts most, and the limits or alerts are on and noted.

## ⚠️ Mistakes and traps
- **Leaving out your own time.** If the margin only works at zero hours, it is not a margin. Instead, count your support and sales time at an honest hourly rate, even when you pay yourself nothing.
- **Quoting vendor prices from memory.** Prices and units change. Instead, read the pricing page on the day, write the date and recompute when the vendor announces a change.
- **Averaging the heavy users away.** One user who regenerates all day can cost more than ten quiet ones. Instead, stress-test with ten times the average use and decide on a cap.
- **Forgetting that chat history is resent.** Long conversations cost far more than their last message suggests. Instead, measure a real long conversation and cap its length or cost.
- **Treating "the agent made a spreadsheet" as proof.** Confident numbers can be invented. Instead, ask where each number came from and check it against the source page.
- **Ignoring spending limits.** A usage-billed vendor with no limit turns a bug or an abusive account into a bill. Instead, turn on budget alerts or hard limits the day you add the vendor.

## 🧾 Recap
- Unit economics is the money story of one customer: revenue, cost to serve, and cost to acquire.
- Count every variable cost, including messages, payments, AI model calls and your own time, with the vendor's pricing unit and the date you read it.
- AI cost grows with how much text goes through the model, so measure a real typical task and a heavy one.
- Gross margin is what is left after cost to serve; payback is acquisition cost divided by monthly contribution.
- Stress-test the sheet: ten times the use, a doubled vendor price, a free customer.
- Turn on spending limits, and treat a vendor price change as a business risk written on the sheet.

## ✍️ Check yourself

**1. Layla wants to know whether Tick makes money on Nadia. Which figure best describes Tick's gross margin on Nadia?**

- A. The total of every cost Layla has paid since the weekend she began building, including early tool trials.
- B. Nadia's monthly payment minus what it costs each month to serve her, such as messages and fees.
- C. The total number of reminders Tick sent for Nadia's salon in the month just ended.
- D. Nadia's monthly payment divided by the number of hours Layla spent on Tick that month.

<details><summary>Answer</summary>

**B.** Gross margin is revenue minus the cost to serve that customer. Option A mixes fixed and one-off costs of building into one customer's month, C counts activity rather than money, and D is revenue per hour, which tells you nothing about cost. (Section: The essentials.)

</details>

**2. Layla's agent writes a unit-economics spreadsheet with a vendor price she does not recognise. What should she do?**

- A. Keep the figure, because the agent says it read it from the vendor's own page and sounds sure.
- B. Replace it with the price she remembers from an article last year.
- C. Round it to the nearest whole number so that the sheet looks cleaner.
- D. Check it on the vendor's current pricing page and note the date and unit.

<details><summary>Answer</summary>

**D.** Prices and units change, and agents can state invented numbers with confidence, so check the source and record the date. A trusts the agent without a check, B swaps in a number from memory, and C changes the number without making it more correct. (Section: The essentials and Going deeper.)

</details>

**3. Tick adds a chat assistant that answers salon owners' questions. Which statement about its model cost is most accurate?**

- A. Long chats can cost far more, since earlier text is usually resent with each new message the assistant answers.
- B. It costs the same per message however long the conversation has run, so only message count matters.
- C. It costs nothing extra once the first version has been built and tested by Layla.
- D. It depends only on how many salons have signed up, not on how much each one uses it.

<details><summary>Answer</summary>

**A.** Model cost follows the amount of text processed, and a conversation's history is typically sent again with each turn. B ignores that growth, C forgets that each use is billed, and D confuses model cost with per-customer costs such as a fixed subscription. (Section: Going deeper.)

</details>

**4. On Layla's sheet, which stress test would show the effect of one salon that regenerates reminder wording all day?**

- A. Doubling the price Layla charges every salon each month.
- B. Removing the payment fee line from the cost to serve.
- C. Running the sheet again with ten times the average model use.
- D. Counting only the first month of acquisition cost for that salon.

<details><summary>Answer</summary>

**C.** A heavy-user test multiplies the use that triggers the cost and shows whether contribution stays positive. A changes revenue rather than the heavy use, B hides a real cost, and D looks at acquisition, not at the cost to serve. (Section: Going deeper, A margin check you can run in your head.)

</details>

**5. Layla's contribution is 16.51 per month and her acquisition cost is 120 per customer. What is her payback period, and what does it mean?**

- A. About 20 months, which is how long the average customer is expected to stay at 5 percent churn.
- B. About 7.3 months: acquisition cost divided by monthly contribution.
- C. About 56.9 months, which is her gross margin percentage read as a number of months.
- D. About 120 months, which is the acquisition cost divided by one.

<details><summary>Answer</summary>

**B.** Payback is acquisition cost divided by monthly contribution: 120 divided by 16.51 is about 7.3. A is the churn-based lifetime, a different figure, C reads a percentage as months, and D divides by the wrong number. (Section: The essentials; Tick example.)

</details>

## 📚 References
- Anthropic, "Pricing", Claude API documentation: shows that model usage is priced per million tokens, with input, output and cached input priced separately. https://platform.claude.com/docs/en/about-claude/pricing (page opened; prices are not quoted here because they change).
- For prices, units and limits of any vendor: the vendor's own pricing page, read on the day you decide (not cited here, because they change).
- Library lessons linked above: *AI Product Management: Zero to Hero*, *Building AI Applications & Agents*, *System Design for Vibe Coders* and *SaaS Building Blocks*.

---

# 3.2 — Pricing: choose, test and change a price
*Level: 🟡 Intermediate* · *Prerequisites: 3.1* · *Step: Price*

## ⚡ In 60 seconds
- After this lesson you can write a one-page **price test plan** with three price points, who will see each, what counts as a signal, and a rule for what you will do next, and then run it with at least twelve real prospects over about two weeks.
- A **price** is a claim about value: "this is worth at least this much to you". Too low is a signal too. It can say "this is a toy".
- The rule that matters most: **a price needs a floor, a ceiling and a test.** The floor is your cost (lesson 3.1). The ceiling is the value to the customer. The test is real people deciding whether to pay.
- Common pricing shapes: one flat monthly price, tiers, per seat, usage-based, or a mix. Pick the one where your cost and the customer's value both grow in the same direction.
- Decision cue: a price you have never been told "no" to is probably too low. A price everyone refuses is too high, or the value is not clear.
- Biggest trap: choosing the price out of fear, copying a competitor without knowing their costs, or giving an endless discount and calling it a price.

## 🧭 Why it matters
After the pilot in lesson 1.4, Layla quoted Nadia 9 per month, a figure she picked out of nervousness. Nadia accepted it without a word. Layla took that as proof the price was right. Mona was not so sure. "Nobody argued," she said. "What does that tell you?"

Layla's sheet from lesson 3.1 says that at 29 she keeps about 16.51 per salon after variable costs, and that at 9 she would keep less than zero: 9 minus 12.49 is negative. The low price would lose money on every salon. A price set by nerves had been hiding a cost problem.

Mona asked a second question: "What does a missed appointment cost Nadia?" Nadia, when Layla asked, said a missed haircut is about 40 lost, and four a month is normal. That is a number from the customer's side, and it changes the conversation: Tick is not "a 9 app", it is a way to recover some of a monthly loss. This lesson is about moving from a price chosen by fear to one chosen by cost, value and evidence, and then about changing it fairly.

## 📐 How it works

### 🟢 The essentials

**Three inputs, in order.**

1. **Floor: your cost.** From lesson 3.1: cost to serve, plus a share of fixed costs and your time. Below the floor you lose money on each customer.
2. **Ceiling: the customer's value.** What is the result worth to them? For Tick, a recovered appointment is worth its price to the salon. Ask in interviews (lesson 1.2) what the problem costs them now, in their words and numbers.
3. **Reference points: alternatives.** What do they use today (paper, a spreadsheet, a competitor, doing it by hand) and what does that cost them? These shape what feels reasonable, not what is possible.

Your price sits between floor and ceiling. Where exactly is a judgement you improve by testing.

**Three common ways to pick a number, and what is wrong with each alone.**

| Method | How it works | Weakness |
|---|---|---|
| **Cost-plus** | Cost plus a margin you want | Ignores what the product is worth; leaves money on the table or overshoots |
| **Competitor-based** | Near what similar products charge | You do not know their costs, customers or whether their price works |
| **Value-based** | A fraction of the value you create for the customer | Needs honest knowledge of the customer's numbers |

Use cost-plus as the floor, competitors as a reference, and value as the guide for where in the range to start.

**Pricing shapes.** Choose one for your first version, and keep it simple.

| Shape | How it charges | Works well when | Watch out for |
|---|---|---|---|
| **Flat price** | One monthly price | Cost per customer is similar for everyone | One heavy customer can break the margin |
| **Tiers** | Two or three packages | Customers differ clearly in size or needs | Too many tiers confuse; keep it to three at most |
| **Per seat** | Price per user | Value grows with the number of users | Customers share one login to avoid the cost |
| **Usage-based** | Pay for what is used (per message, per result) | Your cost and their value both grow with use | Bills vary, which customers dislike; metering must be accurate |
| **Hybrid** | A base price including an allowance, then usage above it | You want predictability plus protection from heavy use | Needs a clear explanation on one page |

If your cost grows with usage, as Tick's messages do, protect the margin with an allowance and a clear charge above it, or with a plan limit. The library's [*SaaS Building Blocks*, lesson 3.2 — Plans, limits and entitlements: turning pricing into code](../saas/index.html#/3.2) shows how a price becomes limits in the product, and [*SaaS Building Blocks*, lesson 3.1 — Subscriptions and payments: checkout, webhooks, the customer portal](../saas/index.html#/3.1) shows how payments are collected.

**Weak versus strong price page.**

| Weak | Strong |
|---|---|
| "Only 9! Cheapest around!" | "29 a month per salon. Includes 200 reminders. Extra reminders 0.08 each. Cancel any time." |
| "Contact us for pricing" (for a tiny product) | One visible price and what it includes |
| "Unlimited everything" | A stated allowance and what happens above it |

(Illustrative figures, not benchmarks.)

### 🟡 Going deeper

**How to test a price without deceiving anyone.** You want real evidence: a person deciding whether to pay, not a person saying "sounds fair". Options, from weakest to strongest:

1. **Ask** in an interview: "What would you expect this to cost?" and "At what price would it be too expensive to consider?" Answers are a rough guide only, because people say what they think is polite.
2. **Show a price, ask for a commitment.** On the smoke-test page or in a conversation (lesson 1.4), show one price and ask for a pre-payment, a deposit or a signed letter of intent. This is the strongest signal.
3. **Show different prospects different prices.** Give each prospect one honest price. Do not show one person two prices for the same thing and do not misstate what other customers pay. Consumer-protection and competition law about price differences varies by country; if you plan to vary prices on a public page, ask a lawyer: may I charge different prospects different prices?

**Sample size, honestly.** Twelve conversations do not give statistics. They show direction. If four people see 19 and all four pay, four see 29 and three pay, and four see 49 and none pay, that is a signal to try 29 to 39 next, not proof of the best price. Write down, before the test, what result would make you move the price up, hold it or move it down.

**Free trials, pilots and discounts.** A free trial gives the customer time to see the value but does not tell you they will pay. A **paid pilot** (a short, discounted, paid trial with a clear end) tells you much more. A **founder discount** is fine if it has an end date and is written down: "25 percent off for the first six months, then the standard price". A discount without an end date becomes the price.

**Annual plans.** Offering a yearly price lower than twelve times the monthly price brings cash earlier (lesson 3.3), but it creates an obligation: if the product fails, customers may expect a refund. Lesson 6.1 covers the refund promise. Do not sell annual plans before the product is stable enough to deserve them.

**Your AI cost sets a floor, and a use limit sets a safety.** If a feature costs more the more it is used, include an allowance, charge above it or make it a higher tier, and cap use so no account costs more than it pays.

### 🔴 Expert view

**Willingness to pay is not one number.** Different customers value the same thing differently: a salon with six chairs loses more to no-shows than a solo stylist. Tiers by size, or per-chair pricing, follow that difference. Segment first (lesson 1.1), then price each segment, instead of averaging them into one confusing price.

**Changing a price after you have customers.** Raising a price is normal; doing it carelessly costs trust.

- **Check your promise.** What did your terms and your page say about price changes and notice? Ask a lawyer what notice or consent a price rise for existing customers needs. Your agreement, and in some places the law, may require it.
- **Give notice.** Write to customers early, in plain words: the new price, the date, the reason, and what stays the same.
- **Consider keeping early customers on the old price for a stated period.** It is a choice, not a rule. If you do it, write the end date.
- **Change new sign-ups first.** Raise the price for new customers, see what happens, then decide about existing customers.
- **Never change a price silently.** Existing invoices and agreed terms still apply; the new price starts from the date you stated.

**Lowering a price** is rarely the best response to a "no". First ask why: unclear value, wrong customer, wrong shape. A discount hides the answer.

**Do not game the test.** Fake scarcity ("only 3 left"), invented testimonials and hidden fees are deceptive, may breach consumer-protection rules, and also ruin the evidence you are collecting.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Price test plan** | One page: hypothesis, three price points, who sees each, what counts as a signal, and the rule for what you do next | Before showing any price to a prospect |
| **Price page brief** | One screen that states the price, what it includes, the allowance and what happens above it, and how to cancel | When you write or revise a pricing page |
| **Value worksheet** | The customer's own numbers: what the problem costs them each month and what a result is worth, in their words | After interviews, before choosing a price point |
| **Pricing-shape chooser** | A small table comparing flat, tiers, per seat, usage-based and hybrid against your cost and their value | When you pick the shape of the price |
| **Price-change notice** | A short template: the new price, the date, why, what does not change, and what early customers keep | Before any change reaches existing customers |
| **Discount rules** | A written list of what discounts you will give, for how long, and to whom | Before you offer your first discount |

## 🏛️ In practice with Tick
Tick, its people and all numbers are fictional; the figures are illustrative, not benchmarks.

Layla replaced her nervous 9 with a test. Her floor from lesson 3.1 was a cost to serve of 12.49, so anything under about 20 would leave almost nothing for her fixed costs. Her ceiling came from Nadia's numbers: about 40 per missed appointment and about four missed a month, so roughly 160 a month at risk. If Tick halved the misses, that was about 80 recovered. At 29, Tick cost the salon a little over a third of that.

Her **price test plan**, in short:

- **Hypothesis:** salon owners will pay 29 a month for Tick, including 200 reminders, if they believe it recovers missed appointments.
- **Price points:** 19, 29 and 49 per month, each with the same 200 reminders included and 0.08 for each extra one.
- **Who:** twelve salon and tutor owners from her interviews and waiting list, four per price point, each shown one price only, in a short video call or message with the same description.
- **Ask:** a first month paid in advance with a clear cancel-any-time promise, or a signed letter saying they would pay on a stated start date.
- **Signal rules written beforehand:** if at least two of four pay at 49, try 49 to 59 next; if at least two of four pay at 29 and fewer at 49, hold 29; if fewer than two pay at 29, look at the value story before lowering the price.
- **After the test:** anyone who paid keeps that price for a stated period or is refunded, with the end date written down before the test starts.
- **Honesty line:** each person sees one real price, with no invented discounts and no fake scarcity.

The result, after two weeks: at 19, four of four paid; at 29, three of four paid; at 49, one of four paid. As her plan said, the five who paid kept their price for a stated period or took a refund. Layla felt 19 had been "easy", but at 19 the contribution would be about 19 minus 12.49, or roughly 6.8 before time (the payment fee is smaller at a lower price), which would leave about 1.8 after her support time of 5.00 and almost nothing toward fixed costs. She chose 29, with a founder offer of 25 percent off the first six months for the first ten salons, written on the page with its end date. She sent Nadia, who had agreed to 9, a short note: the first six months stay at 9, then the standard price starts on a date she gave, and Nadia kept her place as the first design partner. Layla knew 9 is below her floor of 12.49; she accepted that loss on one salon, for a stated end date, as the cost of a design partner. Mona's comment: "You wrote the date down. That is the part people skip."

She also wrote down what the test could not tell her: twelve people is a small group, they mostly came from her own network and may be kinder than strangers, and she would repeat the test with cold prospects in module 4.

## 🛠️ Exercises
1. 🟢 **Write your floor and ceiling.** From your unit-economics sheet (lesson 3.1), write your floor price. From one customer conversation, write the monthly value of the result in their words and numbers. *Done when:* both numbers are written with the source of each, and the price you are considering sits between them.
2. 🟡 **Write a price test plan.** Choose three price points and a pricing shape, describe who sees each, the exact ask, and write the signal rules before you start. *Done when:* the plan is one page and a peer can read the rules and say what you will do for each result without asking you.
3. 🔴 **Run it and write the change notice.** Test with at least twelve real prospects, record who paid or committed at each price, then write the notice you would send existing customers if the price changes, with date, reason and what stays the same. *Done when:* a results table exists with one row per prospect, the decision you made against your rules is written down, and the notice is drafted.

## ⚠️ Mistakes and traps
- **Pricing out of fear.** A price nobody argues with is often a price that is too low. Instead, check it against your floor and the customer's own numbers.
- **Copying a competitor's price.** You do not know their costs, customers or whether the price works. Instead, treat it as a reference and test your own.
- **Testing with opinions.** "That sounds fair" costs the person nothing. Instead, ask for a payment, a deposit or a signed letter at a stated price.
- **Deciding after the result.** If you pick the rule after you see the numbers, you will like whatever happened. Instead, write the signal rules before the test.
- **Discounts with no end date.** They become the price and are hard to remove. Instead, write the end date and the standard price on the offer.
- **Changing the price silently, or in a way your terms do not allow.** It costs trust and may breach your agreement. Instead, give notice in plain words, and check your terms (lesson 6.1).

## 🧾 Recap
- A price has a floor (your cost), a ceiling (the customer's value) and needs a test with real people.
- Use cost-plus for the floor, competitors as a reference and value as the guide; do not use any one alone.
- Choose the simplest shape that makes your cost and their value grow together, and protect the margin with an allowance or a limit.
- Test by asking for a payment or a commitment, show each prospect one honest price, and write the signal rules first.
- Twelve conversations show direction, not proof; repeat the test with strangers.
- Change prices openly: give notice, check your terms, and write the date and what stays the same.

## ✍️ Check yourself

**1. Layla's first price for Tick was 9 per month and her cost to serve is 12.49. What does this show?**

- A. The price is a bargain that every salon will welcome, so Layla should keep it.
- B. The price depends on competitors, so Layla's own costs are not relevant to it.
- C. The price sits below the floor, so each salon would cost Layla money to serve.
- D. The price is right, because Nadia accepted it without any argument at all.

<details><summary>Answer</summary>

**C.** The floor is the cost to serve; a price under it loses money on every customer. A and D read a lack of argument as proof, and B ignores that cost sets the lower limit whatever competitors charge. (Section: The essentials.)

</details>

**2. Which pricing test gives Layla the strongest evidence about a 29 price?**

- A. Asking a salon owner to prepay one month at 29.
- B. Asking a salon owner whether 29 sounds fair for the service.
- C. Asking a friend to guess what other salon owners would pay.
- D. Reading a competitor's page and assuming 29 is about right for her.

<details><summary>Answer</summary>

**A.** A real payment or commitment shows a decision, while opinions and guesses cost nothing to give. B, C and D are all cheap signals and can reflect politeness or assumptions. (Section: Going deeper.)

</details>

**3. Tick's cost rises with every reminder a salon sends. Which price shape best protects Layla's margin?**

- A. A flat price with unlimited reminders for every salon, whatever their volume or cost.
- B. A price per chair, with no limit on how many reminders each chair sends.
- C. A free plan that grows into a paid plan only after a year of use.
- D. A flat price with an included allowance, then a charge for extra reminders.

<details><summary>Answer</summary>

**D.** A hybrid shape keeps the price predictable and still charges for use that drives cost. A leaves heavy use unpaid, B ties price to chairs, not to the cost driver, and C delays revenue while costs run. (Section: The essentials, pricing shapes.)

</details>

**4. After two weeks Layla sees three of four prospects pay at 29, four of four at 19 and one of four at 49. How should she treat this?**

- A. As proof that 29 is the best possible price for every salon, so she can stop testing there.
- B. As a direction to compare with her written rules and repeat with strangers later.
- C. As proof that 19 is best, because it is the price that every prospect accepted.
- D. As meaningless, because twelve people cannot tell her anything about the price.

<details><summary>Answer</summary>

**B.** Twelve conversations show direction, not statistics, and the rules written beforehand tell her what to do. A overstates a small test, C ignores how little 19 leaves after her time and fixed costs, and D discards useful evidence. (Section: Going deeper, Sample size, honestly.)

</details>

**5. Layla wants to raise the price for salons that already pay. What is the sound approach?**

- A. Change the amount on the next invoice and explain only if someone complains about it.
- B. Raise the price only for the customer who argues least, with no notice to the rest.
- C. Give clear notice of the price, date and reason, after checking her terms.
- D. Wait until every customer cancels, then start again with the new price.

<details><summary>Answer</summary>

**C.** A fair change is announced, dated and checked against the agreement, and early customers can be kept on the old price for a stated period. A is a silent change, B treats customers unequally for convenience, and D is not a plan. (Section: Expert view, Changing a price after you have customers.)

</details>

## 📚 References
- Neil Davidson, *Don't Just Roll the Dice: A usefully short guide to software pricing* (Red Gate Software, 2009). Background on software pricing. Full citation only; no link confirmed.
- Madhavan Ramanujam and Georg Tacke, *Monetizing Innovation* (Wiley, 2016). Background on pricing a product before building it. Full citation only; no link confirmed.
- For consumer-protection, competition and price-notice rules in your country: your national consumer or competition authority's guidance pages (not cited here, because they differ by country and change).
- Library lessons linked above: *SaaS Building Blocks* and *AI Product Management: Zero to Hero*.

---

# 3.3 — Cash, runway and invoicing: what to ask your accountant
*Level: 🟡 Intermediate* · *Prerequisites: 3.1, 3.2* · *Step: Price*

## ⚡ In 60 seconds
- After this lesson you can build a six-month **cash table**, compute your **runway** in months, and write a one-page **question list for an accountant** that you could send before a first meeting. Allow about three hours.
- **Cash** is the money in your account. **Profit** is revenue minus costs over a period. A business can show a profit and still run out of cash, because customers pay late, or because annual bills arrive in one month.
- **Runway** is how many months your cash lasts at your current **net burn** (money going out minus money coming in each month). Runway = cash divided by net burn.
- The rule that matters most: **watch cash, not feelings.** Update the table monthly, and decide pay, hiring and spending from it.
- This is education, not accounting or tax advice. Invoices, sales tax, registration and company structure differ by country. This lesson gives you the vocabulary, the table and the questions; the rules are for a qualified accountant to explain.
- Biggest trap: paying yourself, buying tools or taking on usage-billed vendors without checking how many months of runway they cost.

## 🧭 Why it matters
Layla now has a price and a margin. On a Sunday she opens her bank app and sees a balance she has been avoiding. She has paid Sam for the logo and landing page, three tool subscriptions have renewed, and the model vendor billed her for last month's use in one lump. She has no idea how long the remaining money will last, or what happens if two salons pay a month late.

Nadia asks for an invoice. Layla has been sending a message that says "9, thanks!" and a payment link. Nadia's accountant needs something more formal. Layla does not know what an invoice must contain where Nadia lives, and she does not want to guess.

Mona introduces Hana, an accountant, and gives Layla a rule: "Do not turn up with a shoebox. Turn up with a table and a list of good questions." This lesson builds both. Hana appears only to show what a professional is asked. She is fictional, and nothing she says here is a rule for your country.

## 📐 How it works

### 🟢 The essentials

**Cash is not profit.** Look at three words side by side.

| Word | Meaning | Example |
|---|---|---|
| **Revenue** | What customers owe or pay you for a period | Ten salons at 29 is 290 |
| **Profit** | Revenue minus all costs for the period | 290 minus costs |
| **Cash** | Money actually in your account | What the balance says today |

A customer who has been invoiced but has not paid is revenue but not cash. An annual tool subscription paid in one month is cash out in that month, even though it covers twelve. The cash table tracks the money that really moves.

**Burn and runway.** **Gross burn** is all the money you spend each month. **Net burn** is what you spend minus what you take in. **Runway** is cash divided by net burn, expressed in months. If net burn is zero or negative (you earn as much as you spend), runway is not a limit at all, though the table should still be watched.

Use net burn in the formula, but look at both numbers. High gross burn with high revenue is fragile if a few customers leave.

**The cash table.** A simple table with one column per month and these rows:

1. **Opening cash.**
2. **Money in:** customer payments, by when they actually arrive.
3. **Money out, variable:** costs that rise with customers (lesson 3.1).
4. **Money out, fixed:** tools, hosting, domain names, subscriptions, a contractor's fee.
5. **Your own pay,** if you take any. Write it as its own row, even if it is zero.
6. **Net change** and **closing cash.**

Then add runway as a final cell: closing cash divided by that month's net burn.

**Break-even** is the number of customers at which monthly contribution (per-customer margin from lesson 3.1) covers monthly fixed costs. Fixed costs divided by contribution per customer, rounded up. This tells you the size you need before the business stops using up cash; it is not a promise that you will reach it.

**Invoices, in plain words.** An **invoice** is a document that asks a customer to pay for something you supplied, stating what, how much, to whom and by when. Many payment providers send receipts automatically; an invoice may be separate, and the rules about what counts as a valid invoice differ by country. Common contents include an invoice number, a date, your details, the customer's details, a description of what was supplied, the amount, and payment terms. If a sales tax, value-added tax (VAT) or goods-and-services tax applies, it may need its own line or registration number. Whether it applies to you, at what rate and from which sales threshold is for an accountant in your country to tell you.

**Payment terms.** "Due on receipt", "14 days" or "30 days" are common wordings. Longer terms delay your cash. For a small business, shorter terms and paying by card in advance are friendlier to the cash table.

### 🟡 Going deeper

**How cash really arrives.** Payment providers usually do not pay out the instant a customer pays. They may hold payouts for a period, deduct fees, and in some cases pause payouts for review. Read your provider's payout schedule and terms, and put the real arrival day in the table. Refunds and disputed payments (often called chargebacks) take money back, sometimes with a fee. Ask your provider how they work in your country; do not assume.

**Usage-billed vendors send the bill after the use.** Model vendors and messaging vendors may bill monthly in arrears, or by topping up a balance. A month of heavy use can produce a larger bill than the month before. Put each such vendor on its own row, forecast it from your unit-economics sheet, and turn on spending limits (lesson 3.1).

**Currency.** If you sell in one currency and pay vendors in another, exchange rates move your real margin. Note the currencies on the cash table. Your accountant can tell you how your country treats foreign-currency receipts and costs.

**Annual plans and deposits.** A customer paying for a year up front gives you cash now, but it is not all earned yet, and you may owe part back if they leave. Keep it visible in the table as received and not yet earned. How it is recorded for accounting and tax is a question for your accountant.

**Pay yourself on purpose.** Your own pay is the biggest line in many small companies and the one most often left out. Decide it from runway: how many months of cash will remain if you take this amount? Whether and how a founder can be paid depends on the legal form of the business and the tax rules where you live. That is for your accountant and, for the form itself, a lawyer.

**Keep the money separate.** Many accountants advise keeping business money and personal money in separate accounts and keeping every receipt and invoice. Ask what is needed where you are.

**Records.** Keep a folder of invoices you issued, invoices you received, bank statements and payout reports from your payment provider, each with a date. Many countries require businesses to keep records for a number of years; ask your accountant how long and in what form.

### 🔴 Expert view

**Stress your runway.** One runway number is a guess. Compute three: the base case, a "late customers" case (everyone pays 30 days later, so a month's receipts shift), and a "lost customers" case (a quarter of customers leave). Decide in advance what you will do if runway falls under a threshold you choose, such as six months: cut a cost, raise the price, or stop paying yourself.

**Separate the business from yourself legally and financially.** Whether you are a sole trader or a company, and what that means for personal liability, tax, banking and contracts, differs by country. This is a lawyer and accountant conversation, and it is for the capstone and lesson 6.1 to prepare questions for; this lesson only says that how you register changes how money may be received, paid and taxed.

**Funding is outside this lesson.** Money from investors or lenders is a separate topic, not advice to take it or avoid it, and it is touched only in the capstone. Here, the cash table simply shows how long you can go without it.

**What to bring to the accountant, and what to ask.** Hana would rather see ten minutes of preparation than an hour of explaining. Bring:

- The cash table and the unit-economics sheet.
- A sample invoice and a list of the places your customers are and the currencies they pay in.
- A list of every vendor, what you pay each, the currency and whether it is monthly, annual or by use.
- Your payment provider's payout reports and fee terms.
- A plain description of what you sell (subscription software, with AI-written text) and whether you plan to sell to businesses, individuals or both.

Questions to ask (adapt them to your country):

1. What business form could suit a one-person software service where I live, and what does each change for tax, liability and banking? (Which parts need a lawyer?)
2. Do I need to register for sales tax, VAT or a similar tax, from what level of sales, and does it apply to customers in other countries?
3. What must my invoices contain here, and does a payment provider's receipt count?
4. How should annual prepayments, deposits, refunds and chargebacks be recorded?
5. What records do I keep, for how long and in what form?
6. How is a founder paid, and how are costs paid in other currencies treated?
7. Which dates matter this year for filing and payment?

An accountant can answer these; this course cannot, and nothing here should be read as doing so. The library's [*AI Product Management: Zero to Hero*, lesson 8.2 — Unit economics: cost to serve, pricing models and margins](../aipm/index.html#/8.2) goes further on margins for AI products inside a company.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Cash table** | Six to twelve months of money in, money out, closing cash and runway, updated monthly | Before any spend or pay decision; update monthly |
| **Runway stress test** | Three cases (base, late customers, lost customers) with your trigger for action | After the first cash table, and when costs or prices change |
| **Invoice template** | A draft invoice with the common contents, to be checked by an accountant for your country | Before you issue the first formal invoice |
| **Vendor payment list** | Every vendor, amount, currency, billing day and whether it is monthly, annual or by use | When you add or change a vendor |
| **Records folder** | Dated copies of invoices issued and received, bank statements and payout reports | From day one; review monthly |
| **Accountant question list** | The questions above with your documents, sent before the first meeting | Before you meet an accountant, and each year |

## 🏛️ In practice with Tick
Tick, its people and all numbers are fictional; the figures are illustrative, not benchmarks.

Layla built a **cash table** with the numbers from lessons 3.1 and 3.2, using the standard price of 29 for every salon and leaving out the founder offer and Nadia's 9 to keep the sums simple. Opening cash was 3,000 after paying Sam. Fixed costs were 250 a month: 150 for tools, 60 for hosting and 40 for small extras. Variable cost was 12.49 per salon, her price 29, so contribution was 16.51 per salon. She took no pay for now and wrote that as a row with zero. She assumed customers pay in the month they sign (an assumption she marked as the first thing to check).

| Month | Salons | Money in | Variable cost | Fixed cost | Net change | Closing cash |
|---|---|---|---|---|---|---|
| 1 | 3 | 87.00 | 37.47 | 250.00 | −200.47 | 2,799.53 |
| 2 | 5 | 145.00 | 62.45 | 250.00 | −167.45 | 2,632.08 |
| 3 | 7 | 203.00 | 87.43 | 250.00 | −134.43 | 2,497.65 |
| 4 | 9 | 261.00 | 112.41 | 250.00 | −101.41 | 2,396.24 |
| 5 | 11 | 319.00 | 137.39 | 250.00 | −68.39 | 2,327.85 |
| 6 | 13 | 377.00 | 162.37 | 250.00 | −35.37 | 2,292.48 |

At month 2, net burn was 167.45, so runway was 2,632.08 divided by 167.45, about 15.7 months. Break-even: 250 divided by 16.51 is about 15.1, so 16 salons. That excludes Layla's own time: at the after-time contribution of 11.51 it is 250 divided by 11.51, about 22 salons. The table also leaves out the founder offer, so real early months are worse. She was not yet at break-even in month 6, and the table did not promise she would get there. It did show her that growth at that pace costs about 700 in total over six months, and that she could afford it.

Then Layla ran two stress cases. If she paid herself 1,000 a month from month 1, net burn would be over 1,100 and runway under three months: she decided not to. If all salons paid 30 days late, her month-1 receipts would arrive in month 2, and she would be short for a month, which she could cover but would not enjoy.

She sent Hana a one-page list: the cash table, a sample invoice, her vendor list and the seven questions above, and asked for a first meeting. She asked, for example, what an invoice must contain where Nadia's salon is, and whether she needed to register for a sales tax and from what level of sales. Hana's reply was an agenda for the meeting and a list of documents to bring, not answers. Layla wrote the answers into the invoice template and the records folder after the meeting, and noted that what Hana tells her applies only to her situation and her country.

## 🛠️ Exercises
1. 🟢 **List your cash in and out.** Write one month of money in and money out as you expect them, with each vendor and its billing day, and a row for your own pay (even if zero). *Done when:* a one-month table exists with every row filled and every vendor on it.
2. 🟡 **Build the six-month cash table and compute runway.** Use your unit-economics sheet and your price, compute net change, closing cash, runway and break-even customers. *Done when:* the six-month table is saved, runway and break-even are calculated, and the main assumption (when customers pay) is written next to it.
3. 🔴 **Stress it and prepare the accountant meeting.** Run the late-customers and lost-customers cases with a threshold that triggers action, then write the question list with the documents you would bring. *Done when:* three runway numbers exist, the trigger is written, and the question list is complete enough that you could send it by message today.

## ⚠️ Mistakes and traps
- **Confusing profit with cash.** An unpaid invoice is not in your account. Instead, track money by the date it arrives.
- **Leaving your own pay out of the table.** It is often the largest cost. Instead, write the row, even at zero, and decide pay from runway.
- **Ignoring payout delays, refunds and fees.** What the customer pays is not what lands. Instead, read your payment provider's payout and fee terms and use real arrival dates.
- **Forgetting that usage bills arrive afterwards.** A heavy month can be a large invoice. Instead, forecast each usage-billed vendor and set spending limits.
- **Copying an invoice or a tax rule from another country.** Rules differ and change. Instead, ask an accountant what applies where you and your customers are.
- **Arriving at the accountant with a shoebox.** You pay for explaining and miss the questions. Instead, bring the table, the sample invoice, the vendor list and the question list.

## 🧾 Recap
- Cash is money in the account; profit is revenue minus costs; a business can run out of cash while showing a profit.
- Runway is cash divided by net burn in months; break-even is fixed costs divided by contribution per customer.
- A cash table with real arrival dates, your own pay and each vendor's billing day is the one tool to check monthly.
- Stress the runway: late payments and lost customers, and decide your action trigger in advance.
- Invoices, sales tax, registration, pay and records depend on your country; teach yourself the vocabulary and bring questions to a qualified accountant.
- Prepare for the meeting with documents and a written question list.

## ✍️ Check yourself

**1. Layla's customers have been invoiced for the month but none has paid yet. How should she treat this in her cash table?**

- A. As cash already received, since the invoice has been sent and the work is done.
- B. As revenue owed to her, in cash only when paid.
- C. As a cost, because sending invoices takes up her time during that month.
- D. As profit that she can spend freely, because the amounts are all agreed.

<details><summary>Answer</summary>

**B.** An unpaid invoice is revenue owed but not cash, and the table tracks money by arrival date. A confuses owed money with money held, C mislabels revenue as a cost, and D forgets that spending needs cash. (Section: The essentials.)

</details>

**2. Layla has 2,632.08 in cash and a net burn of 167.45. What is her runway, and what does it mean?**

- A. About 10.5 months, because only the fixed costs of 250 count.
- B. About 8.4 months, because full costs of 312.45 count with no revenue.
- C. About 15.7 months, how long her cash lasts.
- D. About 0.06 months, because she has far more burn than cash.

<details><summary>Answer</summary>

**C.** Runway is cash divided by net burn: 2,632.08 divided by 167.45 is about 15.7 months. A divides by the fixed costs alone, B ignores revenue, and D inverts the division. (Section: The essentials, Burn and runway.)

</details>

**3. Nadia's accountant asks for a formal invoice. What should Layla do?**

- A. Copy the layout of an invoice from a template she found online for another country.
- B. Ask her accountant what an invoice must contain.
- C. Send the payment provider's receipt and assume it counts as an invoice.
- D. Write whatever looks professional, as only the amount really matters.

<details><summary>Answer</summary>

**B.** Requirements differ by country and change, so a qualified person should say what applies. A and C assume rules that may not apply, and D ignores required contents such as dates, details and tax lines where they apply. (Section: The essentials, Invoices, in plain words.)

</details>

**4. Layla's late-customers case shows a short cash gap in month 1. What is the right use of this result?**

- A. Ignore it, since the table's base case already looks comfortable enough for her.
- B. Take a larger customer discount, so that the gap closes immediately.
- C. Stop recording payments, so that the gap no longer appears in the table.
- D. Set a threshold and an action in advance, before the gap opens.

<details><summary>Answer</summary>

**D.** A stress test is useful because you decide what to do before it happens. A ignores the risk the case exists to show, B gives away price for cash without checking the refund and margin effects, and C hides the problem. (Section: Expert view, Stress your runway.)

</details>

**5. Which question belongs on Layla's list for the accountant?**

- A. Do I need to register for sales tax or VAT, and from what level of sales in my country?
- B. Which investors should I approach first, and how much should I ask them for this year?
- C. What is the right price for Tick, given that Nadia is happy to pay 29 each month?
- D. Will Tick reach break-even by month 12, if she keeps growing at the same pace as her table?

<details><summary>Answer</summary>

**A.** Registration thresholds and cross-border treatment depend on the country and are exactly what a qualified professional answers. B is funding advice, outside this lesson, C is her own pricing decision from lesson 3.2, and D is a forecast no accountant can promise. (Section: Expert view, What to bring to the accountant.)

</details>

## 📚 References
- Mike Michalowicz, *Profit First*. Background on keeping business money separate and tracking cash. Author and title only; publisher details and link not confirmed.
- Eric Ries, *The Lean Startup* (Crown Business, 2011). Background on measuring progress with small experiments. Full citation only; no link confirmed.
- For invoice contents, sales tax or VAT registration, record keeping and business forms: your national tax authority's and company registry's small-business guidance pages, and a qualified accountant (not cited here, because they differ by country and change).
- For payout schedules, fees, refunds and disputes: your payment provider's own documentation, read on the day (not cited here, because it changes).
- Library lesson linked above: *AI Product Management: Zero to Hero*.
