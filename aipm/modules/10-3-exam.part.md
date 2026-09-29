# 10.3 — Practice exam: 60 scenario questions
*Level: 🔴 Advanced* · *Prerequisites: Modules 0–9* · *Stage: Discover, Define, Design, Build, Evaluate, Launch, Grow, Lead*

## ⚡ In 60 seconds
- This is a **60-question practice exam** covering the whole course, grouped by the eight lifecycle stages: Discover, Define, Design, Build, Evaluate, Launch, Grow and Lead (7–8 questions each). Most questions are short scenarios at Najm Bank or a neutral company.
- **Give yourself 90 minutes, in one sitting, with no notes.** Write each answer down before you open its answer block. Your score is the number you got right.
- Every question has one best answer. Several options will sound reasonable. Pick the one a careful AI product manager would choose **first** or **most**, given exactly what the scenario says.
- Every answer explains why the right option is right and why the most tempting wrong option is wrong. It ends with the stage and the lesson to review, for example *(Evaluate · 6.1)*.
- **Course rule of thumb:** 48 or more correct (80%) means you have the product judgement this course aims for. This is our guide, not a certification standard. This course is not affiliated with any certification body.

## 🧭 Why it matters
Faisal finished the course in three weeks and felt ready. Then Rania asked him four quick questions in a corridor: what he would measure first on Najm Assist, when he would stop an A/B test, who owns the decision to let SME Instant Finance decline an application on its own, and what happens to the Credit Memo Copilot when the model vendor ships a new version. He knew the words but not the answers. Knowing a framework is not the same as reaching for the right one when a situation is described in three sentences.

That is what this exam tests. The questions are not about definitions. They describe a situation, often a messy one, and ask what you would do. They are written so that a reader who skimmed will find two answers attractive, and a reader who understood will see why one of them is wrong.

## 📐 How it works
### 🟢 The essentials
The exam has eight sections, one per lifecycle stage. Each question tests one lesson. The table shows the spread.

| Stage | Questions | Main lessons tested |
|---|---|---|
| Discover | 1–8 | 0.2, 1.1, 2.1, 2.2, 2.3 |
| Define | 9–15 | 1.3, 3.1, 3.3, 5.1 |
| Design | 16–23 | 4.1, 4.2, 4.3 |
| Build | 24–30 | 1.2, 3.2, 5.2, 5.3 |
| Evaluate | 31–38 | 6.1, 6.2, 6.3 |
| Launch | 39–45 | 7.1, 7.2, 7.3 |
| Grow | 46–53 | 8.1, 8.2, 8.3 |
| Lead | 54–60 | 9.1, 9.2, 9.3, 9.4, 10.2 |

### 🟡 Going deeper
Read the last sentence of each question first. It tells you what is being asked: the *first* step, the *best* option, the *most likely* cause, or what is *wrong*. Then read the scenario and underline the facts that matter: who the user is, what is at stake if the product is wrong, what data exists, and what has already been tried.

### 🔴 Expert view
The distractors follow patterns you have met throughout the course. Watch for the answer that jumps to technology before the problem is clear, the one that measures cost but not quality, the one that trusts an offline score as proof of real-world value, the one that hands a high-stakes decision to a model with no human path, and the one that sounds thorough but comes in the wrong order.

## 🧰 The toolkit
| Tool or framework | What it is and does | When to reach for it |
|---|---|---|
| **Stage map** | The eight lifecycle stages used as a lens on each question | To place a scenario before choosing an answer |
| **Error log** | A list of every wrong or guessed answer, with the lesson to review and the trap you fell for | Straight after marking the exam |
| **Trap checklist** | The five distractor patterns in "Expert view" above | When two options both look right |

## 🏛️ In practice at Najm Bank
Rania runs this exam with every new AI product manager in their first month. She does not care much about the score. She cares about the error log. The team uses one shared template:

| # | My answer | Correct | Stage · lesson | Trap I fell for | What I will re-read |
|---|---|---|---|---|---|
| 12 | A | D | Define · 5.1 | Jumped to technology | 5.1 "Going deeper" |
| 37 | C | A | Evaluate · 6.3 | Read results before checking the test was valid | 6.3 on sample ratio mismatch |

## 🛠️ Exercises
- 🟢 **Sit the exam.** Take all 60 questions in 90 minutes without notes. *Done when:* you have a score and an answer written down for every question.
- 🟡 **Build your error log.** For every wrong or guessed answer, fill in one row of the template above. *Done when:* each row names a trap and a section to re-read.
- 🔴 **Write your own.** For your two weakest stages, write two new scenario questions each, set at Najm Bank or your own organisation, with an answer that explains the best distractor. *Done when:* a colleague answers them and at least one finds a distractor tempting.

## ⚠️ Mistakes and traps
- **Opening answers as you go.** It turns an exam into reading practice. Write all your answers first.
- **Counting lucky guesses as knowledge.** Mark any answer you were not sure about as wrong in your error log, even if it was right.
- **Picking the most complete-sounding option.** Many questions ask what to do *first*. The complete plan is often the wrong answer.
- **Answering for the company you know instead of the one described.** Use only the facts in the scenario.

## ✍️ Practice exam

### Discover

**1. Khalid, Head of Retail Lending, tells Faisal: "Our competitors all have AI in their apps. Put AI in our lending journey this quarter." What should Faisal do first?**

- A. Shortlist three model vendors and ask each for a demo on lending data
- B. Map the lending journey with customers and staff to find the jobs and pain points where AI could change an outcome
- C. Build a chatbot for the lending page, since a chatbot is the fastest way to show AI to customers
- D. Write a PRD for an AI loan assistant so engineering can start estimating

<details><summary>Answer</summary>

**B.** Discovery starts from the job the user is trying to get done and the workflow where it happens, not from the technology. Only once you know where the pain is can you judge whether AI fits. A is tempting because it feels like progress, but choosing vendors before knowing the problem means you will evaluate them on the wrong tasks. C and D both commit to a solution nobody has validated. *(Discover · 2.1)*

</details>

**2. Faisal scores three candidate use cases on a 1–5 scale for business value only, and ranks "AI declines for SME invoice finance" first. Rania sends the scorecard back. What is the best fix?**

- A. Replace the scale with a 1–10 scale so the differences are clearer
- B. Ask Khalid to confirm the ranking, since he owns the business outcome
- C. Keep the ranking but add a note that the top idea needs extra testing
- D. Score each use case on value, feasibility and risk, and treat very high risk as a gate that must be resolved before ranking

<details><summary>Answer</summary>

**D.** A use-case scorecard needs at least three lenses: value (is it worth it), feasibility (do we have the data, skills and technology) and risk (what harm if it is wrong). Automated credit declines are high value but also high risk, so risk has to be scored and can block the idea on its own. B is tempting because Khalid owns the value, but his sign-off does not add the missing feasibility and risk dimensions. A only changes the scale. *(Discover · 2.2)*

</details>

**3. Najm Bank's fee for an early loan settlement is set by a published tariff: a fixed formula based on balance and remaining term. A team proposes an LLM feature that "works out the fee" when customers ask. What is the best recommendation?**

- A. Calculate the fee with ordinary code from the tariff, and use AI at most to explain the result in plain language
- B. Use the LLM, but lower the temperature so it calculates consistently
- C. Fine-tune a model on past fee calculations so it learns the formula
- D. Use the LLM and add a disclaimer that the fee is an estimate

<details><summary>Answer</summary>

**A.** When the answer is fully determined by a known rule, deterministic software is cheaper, faster, exact and auditable. A probabilistic model adds error for no gain. B is tempting, but lower temperature reduces randomness; it does not make a language model a reliable calculator. D pushes the model's errors onto the customer in a matter where the bank's number is binding. *(Discover · 2.3)*

</details>

**4. In Teresa Torres's Opportunity Solution Tree, Hessa has written the outcome "Increase the share of SME invoice-finance requests completed in the app". What should come directly beneath it?**

- A. A list of AI features the team could build
- B. The experiments the team will run this sprint
- C. Opportunities: customer needs, pains and desires discovered in research, such as "I don't know which invoices qualify"
- D. The model options the team could use, ranked by accuracy

<details><summary>Answer</summary>

**C.** The tree runs from outcome, to opportunities (needs and pains found through research), to solutions, to experiments that test those solutions. Opportunities sit between the outcome and any solution so the team does not jump from a goal straight to a feature. A is the most tempting because features feel concrete, but listing them directly under the outcome skips the step that tells you which problem each feature solves. *(Discover · 2.1)*

</details>

**5. Faisal is about to run a four-week pilot of an AI tool that suggests next steps to SME relationship managers. Rania asks him to add one thing to the pilot plan before it starts. What is it most likely to be?**

- A. A list of extra features to add if the pilot goes well
- B. A press release draft, so marketing is ready
- C. Kill criteria agreed in advance: the result below which the idea stops, for example fewer than a set share of suggestions being used
- D. A longer pilot period, since four weeks is never enough for AI

<details><summary>Answer</summary>

**C.** Agreeing the stop condition before the data arrives protects the team from moving the goalposts once they are attached to the idea. Killing weak ideas early is how an AI portfolio stays affordable. D is tempting, and sometimes a pilot needs to run longer, but a longer pilot without a decision rule only delays the same argument. *(Discover · 2.3)*

</details>

**6. Khalid compares the Credit Memo Copilot to the bank's loan origination system: "We paid for the system once. Why does the copilot's bill grow every month?" What is the best explanation?**

- A. Each AI request consumes paid compute or tokens, so cost rises with usage, unlike most traditional software where extra use is almost free
- B. The vendor is overcharging and procurement should renegotiate
- C. The model is still training on Najm's data, which will stop after a year
- D. AI software always costs more than traditional software in total

<details><summary>Answer</summary>

**A.** A defining feature of AI products, especially generative ones, is a real marginal cost per use: every call to the model costs money. That is why AI products need a cost-per-task model and pricing that tracks usage. B might sometimes be true, but it does not explain the pattern. C is wrong: calling a model does not usually train it. D is an unsupported generalisation. *(Discover · 0.2)*

</details>

**7. Hessa's research for a new "savings coach" in Najm Assist shows that customers say they want it, but none of the eight customers she interviewed has ever used the bank's existing savings goals feature. Which of Marty Cagan's four big risks does this evidence mainly raise?**

- A. Feasibility risk
- B. Usability risk
- C. Business viability risk
- D. Value risk: whether customers will actually choose to use it

<details><summary>Answer</summary>

**D.** Cagan's four risks are value (will they use or buy it), usability (can they figure out how), feasibility (can we build it) and business viability (does it work for the business, including legal and financial constraints). What people say they want and what they do differ, and here behaviour suggests they may not value the feature. B is tempting because the old feature may have been hard to use, but the evidence is about demand, not about difficulty. *(Discover · 2.1)*

</details>

**8. The fraud team wants to improve Smart Alerts, which flags suspicious card transactions from structured data: amount, merchant, location and time. Which approach is the best starting fit?**

- A. A large language model that reads each transaction and writes a judgement
- B. A classic machine-learning classifier trained on labelled past fraud cases
- C. An autonomous agent that investigates each transaction with tools
- D. A generative image model that visualises spending patterns

<details><summary>Answer</summary>

**B.** Scoring structured records into "fraud" or "not fraud", at high volume and low latency, is what classic supervised machine learning does well. It is cheaper and faster per transaction than an LLM and is measurable with precision and recall. A is tempting because LLMs are new and flexible, but generating text about every transaction adds cost and latency and does not suit a high-volume scoring task. *(Discover · 1.1)*

</details>

### Define

**9. Faisal's first spec for the Credit Memo Copilot says: "The draft memo should be accurate and helpful." Dana says she cannot build or test against it. What should replace it?**

- A. Measurable quality bars tied to an evaluation, for example "on the golden set of 200 past cases, no more than a set rate of drafts contain a figure that differs from the source financials"
- B. A longer description of what "accurate" means to relationship managers
- C. A requirement to use the most accurate model on public benchmarks
- D. A statement that relationship managers will check every draft, so accuracy is their responsibility

<details><summary>Answer</summary>

**A.** In an AI spec, evals are the requirements: each quality expectation needs a metric, a dataset it is measured on and a threshold. That gives Dana something to build towards and gives the team a clear launch bar. C is tempting because it sounds rigorous, but public benchmarks do not measure your task on your data. D confuses a safeguard with a requirement. *(Define · 5.1)*

</details>

**10. Dana plans to train SME Instant Finance on five years of past invoice-finance decisions and their repayment outcomes. What is the most important data-readiness problem to raise?**

- A. Five years is too little data for any model
- B. The data must first be moved to a new cloud platform
- C. Repayment outcomes exist only for requests the bank approved, so the model learns nothing about how rejected applicants would have behaved
- D. Invoice data is structured, so it cannot be used by AI

<details><summary>Answer</summary>

**C.** This is a classic label problem in lending: outcomes are only observed for approved applicants, so the training data is biased by the old decision process. The team has to know this and plan for it before promising performance. A is tempting because more data often helps, but there is no rule that five years is too little; whether the data is fit for purpose matters more than its age. D is false. *(Define · 3.1)*

</details>

**11. The Credit Memo Copilot must answer questions about Najm's credit policy manual, which is updated several times a year, and it must show which section each answer came from. Which approach from the build spectrum fits best?**

- A. Train a new model from scratch on the policy manual
- B. Retrieval-augmented generation: retrieve the relevant policy sections at question time and have the model answer from them, with citations
- C. Fine-tune a model on the current manual and fine-tune again after each update
- D. Put a summary of the manual in the system prompt

<details><summary>Answer</summary>

**B.** RAG suits knowledge that changes and answers that must cite sources: update the documents and the answers update, and the retrieved passages give the citations. C is the tempting distractor. Fine-tuning mainly shapes behaviour, style and format; it is a poor way to keep facts current, it has to be repeated with every change, and it does not give you citations. D loses the detail. *(Define · 1.3)*

</details>

**12. Faisal's spec for Najm Assist lists everything the assistant should do. In review, Layla asks what is missing. What is the most important gap?**

- A. A list of every question customers might ask
- B. The model name and version to use
- C. The target number of daily conversations
- D. What the assistant must not do and how it must behave then: topics it declines, such as personalised investment advice, and when and how it hands over to a human

<details><summary>Answer</summary>

**D.** An AI behaviour spec has to define out-of-scope behaviour, refusals and escalation as carefully as the happy path, because a probabilistic system will receive requests you did not plan for. B is tempting because engineers need it, but the model is an implementation choice that may change; the behaviour the product must guarantee is the requirement. A is impossible to complete. *(Define · 5.1)*

</details>

**13. Tariq suggests using two years of Najm Assist chat transcripts to improve the assistant's answers. What should Faisal do before any transcript is used?**

- A. Anonymise the transcripts by deleting customer names, then proceed
- B. Check with Sara, the Data Protection Officer, whether this new use is compatible with the purpose the data was collected for and has a lawful basis, and what minimisation is needed
- C. Proceed, because the bank already holds the data
- D. Ask the model vendor whether it is allowed

<details><summary>Answer</summary>

**B.** Holding data does not mean you may use it for any purpose. Reusing customer conversations for product improvement raises purpose limitation, lawful basis and minimisation questions under laws such as GDPR and Qatar's PDPPL, and the PM owns getting that answer before building. A is tempting, but deleting names is rarely enough to anonymise free-text chats, which often contain account numbers and other identifiers; that is part of what Sara should assess. *(Define · 3.3)*

</details>

**14. For Smart Alerts, a missed fraud costs the customer money and trust, while a false alarm costs a moment of annoyance and, if repeated, alert fatigue. How should the product team treat this when defining the product?**

- A. Treat the relative cost of each error type as a product decision, document it in the spec, and use it to set the alert threshold
- B. Leave the threshold to the data science team, since it is a technical parameter
- C. Maximise overall accuracy, which balances both errors automatically
- D. Minimise false alarms first, since customers complain about them most

<details><summary>Answer</summary>

**A.** Which error is worse, and by how much, is a business and user judgement. The PM should make it explicit so the threshold reflects it. C is the tempting one, but overall accuracy is misleading when fraud is rare: a model that never alerts can be highly "accurate" and useless. B hands a product trade-off to the team least placed to weigh customer harm against annoyance on their own. *(Define · 5.1)*

</details>

**15. Najm Bank wants an internal assistant, Staff GenAI, to help employees draft emails, summarise documents and search internal policies. Nothing about it is unique to banking. What is the most sensible default?**

- A. Train a proprietary model so the bank owns the technology
- B. Fine-tune an open-weight model before evaluating any existing product
- C. Buy or license an enterprise product that meets the bank's security and data requirements, and spend the effort on adoption and integration
- D. Build from scratch so the assistant can later be sold to other banks

<details><summary>Answer</summary>

**C.** When a capability is generic and not a source of advantage, buying is usually faster and cheaper, and the product work moves to fit, security, adoption and integration. Build where you differentiate. B is tempting because it sounds like a middle path, but it commits engineering effort before anyone has checked whether an existing product already meets the need. *(Define · 1.3)*

</details>

### Design

**16. Which level of automation fits the Credit Memo Copilot best at launch?**

- A. Act: the copilot submits memos to the credit committee automatically
- B. Decide: the copilot recommends approve or decline and the decision stands unless someone objects
- C. Suggest: the copilot only lists facts, and the relationship manager writes every word
- D. Draft: the copilot prepares a memo that the relationship manager reviews, edits and signs as their own

<details><summary>Answer</summary>

**D.** Drafting saves the relationship manager time on the heavy writing while keeping a named, accountable person in charge of a high-stakes credit document. A and B remove the human judgement that credit decisions require. C is the tempting cautious choice, but it gives up most of the value when a well-designed draft-and-review flow can manage the risk. *(Design · 4.1)*

</details>

**17. In early testing, relationship managers expect the Credit Memo Copilot to know about client meetings that were never written down. They lose trust when it cannot. Which design change addresses the cause?**

- A. Add more animations while the draft is generated
- B. Set expectations at the start: show clearly what the copilot can and cannot see and how well it performs, for example "Drafts from the credit file and financial statements only"
- C. Hide the copilot's limitations so users are not put off
- D. Make the copilot's tone more confident

<details><summary>Answer</summary>

**B.** Microsoft's Guidelines for Human-AI Interaction begin with making clear what the system can do and how well it can do it. Mismatched expectations are a design problem, and the fix is to set them before users form their own. D is tempting because confident text feels trustworthy, but confidence that is not earned makes the eventual failure worse. *(Design · 4.2)*

</details>

**18. Najm Assist sometimes misunderstands the transaction a customer is asking about. What is the most important recovery pattern to design in?**

- A. Ask the customer to rate the answer from 1 to 5
- B. Apologise and end the conversation
- C. Make correction easy: show which transaction the assistant understood, and let the customer pick the right one in one tap
- D. Retry the same answer with different wording

<details><summary>Answer</summary>

**C.** AI will be wrong sometimes, so good design makes errors visible and cheap to fix. Showing the assistant's interpretation and supporting efficient correction are core human-AI interaction guidelines. A is tempting because it collects feedback, but a rating does not help the customer who is stuck right now. *(Design · 4.2)*

</details>

**19. Najm Assist is growing into an agent. Customers will be able to say "freeze my card" or "dispute this transaction". What is the most important design rule for these actions?**

- A. Before any consequential action, show exactly what will happen and ask for explicit confirmation, and make reversible actions easy to undo
- B. Carry out the action immediately, since speed is the point of an agent
- C. Allow only questions, never actions, to keep the risk at zero
- D. Ask the customer to confirm every message, including simple questions

<details><summary>Answer</summary>

**A.** When an agent acts on a customer's account, the customer must stay in control: a clear preview, confirmation for actions with consequences, and an undo where possible. Freezing a card is also time-critical, so the confirmation should be fast, not a barrier. C is tempting but gives up the value of the agent entirely. D adds so much friction that people will stop reading the prompts. *(Design · 4.3)*

</details>

**20. Relationship managers ask how they can trust a figure in a drafted credit memo. What is the most useful explanation to design for this product?**

- A. A technical description of how the model works
- B. A confidence percentage next to the whole memo
- C. A statement that the model is highly accurate
- D. A citation on each key figure and claim, linking to the exact place in the source document it came from

<details><summary>Answer</summary>

**D.** Good explanations help the user decide whether to rely on an output. For a document built from sources, the most useful explanation is a traceable link from each claim to its source, so the reviewer can check it in seconds. B is tempting because it looks precise, but a single score for a whole memo does not tell the reviewer which part to check, and model confidence scores are often poorly calibrated. *(Design · 4.2)*

</details>

**21. Three months after launch, Dana notices that relationship managers now approve 98% of Copilot drafts with no edits, including drafts she knows contain errors. What is the best design response?**

- A. Nothing: high acceptance proves the product works
- B. Remove the copilot, since users cannot be trusted with it
- C. Counter automation bias: highlight low-confidence or unverified sections, require the reviewer to confirm key figures, and track edit rates on known-error cases
- D. Add a disclaimer at the bottom of each memo

<details><summary>Answer</summary>

**C.** When people rubber-stamp AI output, the human review the product relies on stops working. This is automation bias. The design answer is well-placed friction on the parts that matter, not friction everywhere. A is the tempting distractor: acceptance rate alone cannot tell good drafts apart from unchecked ones, and here there is evidence that errors are passing. D is a disclaimer, which people stop reading. *(Design · 4.1)*

</details>

**22. A customer has asked Najm Assist the same question about a blocked transfer three times and is getting frustrated. What should the design do?**

- A. Keep trying new wordings until the customer is satisfied
- B. Offer a hand-over to a human agent, and pass the conversation and what has been tried so the customer does not repeat themselves
- C. Show a link to the FAQ page
- D. End the chat and ask the customer to call the contact centre

<details><summary>Answer</summary>

**B.** A conversational product needs a clear path to a person, triggered by signals such as repetition or frustration, and the hand-over must carry context. C is tempting because it is cheap, but the customer has already shown the self-service answers are not solving their problem. D abandons the context and makes the customer start again. *(Design · 4.3)*

</details>

**23. In *Moffatt v. Air Canada* (2024), a tribunal held the airline responsible for what its website chatbot told a customer about a fare policy. What is the main design lesson for Najm Assist?**

- A. Answers about policies, fees and commitments must be grounded in the bank's approved sources, and the assistant must not improvise terms it cannot back up
- B. Customer-facing chatbots should be avoided in regulated industries
- C. A disclaimer that the chatbot may be wrong removes the company's responsibility
- D. The chatbot should refer every question to the website

<details><summary>Answer</summary>

**A.** The case shows that customers can treat what an assistant says as the company speaking. For policy and fee answers, the design must tie responses to approved content and decline or escalate where it cannot. C is tempting, but the case is widely read as a warning that a company cannot simply disown what its own chatbot says. B overreacts; D gives up the product's value. *(Design · 4.3)*

</details>

### Build

**24. Before building an AI model, Faisal wants to test whether SME owners would use an "instant quote" for invoice finance. What is the cheapest credible test?**

- A. Build the model and release it to 5% of customers
- B. Run a survey asking SME owners if they would like instant quotes
- C. A Wizard of Oz test: customers use a real-looking quote screen while trained staff produce the quotes behind it
- D. Ask Dana how accurate a model could be

<details><summary>Answer</summary>

**C.** A Wizard of Oz prototype lets you watch real behaviour with a real-feeling experience before you spend on the model, so you learn about value first. B is tempting because it is cheap too, but it measures stated intent, which often differs from what people do. A spends the most before learning anything about demand. *(Build · 5.2)*

</details>

**25. An engineer changes one sentence in the Credit Memo Copilot's system prompt to fix a formatting issue and deploys it on a Friday. On Monday, drafts are missing the risk section. What practice would have prevented this?**

- A. Treat prompts as product code: version them, review changes and run the eval suite before any prompt change is released
- B. Allow only the PM to edit prompts
- C. Never change a prompt after launch
- D. Write longer prompts so small changes matter less

<details><summary>Answer</summary>

**A.** Prompts, context and tool descriptions are part of the product surface. Small wording changes can shift behaviour, so they need the same version control, review and regression testing as code. B is tempting because it adds an owner, but one person reviewing by eye still cannot see a regression across hundreds of cases; the eval suite can. C freezes the product. *(Build · 5.3)*

</details>

**26. In the first sprint planning session for SME Instant Finance, what is the most valuable thing Faisal can bring to Dana's data science team?**

- A. A decision on which algorithm to use
- B. A demand that the model be 99% accurate
- C. A fixed delivery date for the final model
- D. The business context: the decision the model supports, the relative cost of each error type, real example cases, and the constraints such as latency and explainability

<details><summary>Answer</summary>

**D.** A PM working with ML and AI engineers adds most by defining the problem, the stakes and the constraints, and then letting the experts choose the method. B is tempting because it sounds like a clear quality bar, but a single accuracy number with no link to error costs or a baseline is neither meaningful nor achievable on demand. A is the data scientists' call. *(Build · 5.2)*

</details>

**27. Najm Assist's agent will get tools to read balances, freeze cards and file disputes. Tariq proposes connecting it through one integration account with full access to the core banking API "to keep things simple". What should Faisal push for?**

- A. Full access, but with extra logging
- B. Least privilege: separate, narrowly scoped tools for each action, acting only on the signed-in customer's own accounts, with limits on what each can do
- C. Remove all tools until the model is perfect
- D. Let the model choose which API calls to make at run time

<details><summary>Answer</summary>

**B.** Tools define what an agent can do in the world, so they are product surface and a security boundary. Narrow, well-described tools limit the damage from a model error or a prompt injection. Standards such as the Model Context Protocol make connecting tools easier, but they do not decide what access is appropriate. A is tempting, but logging records the damage rather than preventing it. *(Build · 5.3)*

</details>

**28. To make the Credit Memo Copilot "know everything", an engineer proposes putting the whole 600-page credit policy manual into every request. What is the main problem?**

- A. Every request becomes slower and more expensive, and models can miss relevant details buried in very long contexts; retrieving the relevant sections is usually better
- B. It is impossible, because no model accepts more than a few pages
- C. It makes the model forget its training
- D. There is no problem, as long as the model's context window is large enough

<details><summary>Answer</summary>

**A.** Context is not free. Cost and latency grow with the tokens you send on every request, and answer quality can drop when the relevant detail is a small part of a very long input. D is the tempting distractor: fitting in the window does not mean it is a good design. B is false; context windows vary by model and have grown, which is exactly why the trade-off, not a hard limit, is the question. *(Build · 1.2)*

</details>

**29. Tariq sets the Credit Memo Copilot's temperature very low when it extracts figures from financial statements. What does this achieve?**

- A. It stops the model from hallucinating
- B. It reduces the model's cost per request
- C. It makes the model more creative in its summaries
- D. It makes outputs more consistent from run to run, which suits extraction, but it does not guarantee they are correct

<details><summary>Answer</summary>

**D.** Temperature controls how much randomness goes into choosing each next token. Low temperature makes outputs more repeatable, which suits extraction tasks, but a model can be consistently wrong. A is the tempting distractor: it is a common belief, but checking against the source is still required. B is wrong; temperature does not change the price of a request. *(Build · 1.2)*

</details>

**30. Faisal wants the Credit Memo Copilot to get better over time. Which signal should he design the product to capture first?**

- A. The number of times the copilot is opened each day
- B. A pop-up survey after every memo
- C. The edits relationship managers make to each draft before they sign it, linked to the section and the source data
- D. The length of each draft

<details><summary>Answer</summary>

**C.** A learning product captures feedback in the normal course of work. The edits experts make are rich, specific and free to collect. They show what was wrong and what right looks like, and they feed error analysis and future evals. B is tempting because it asks directly, but surveys after every task get ignored or answered carelessly. A measures usage, not quality. *(Build · 3.2)*

</details>

### Evaluate

**31. Dana is building a golden set to evaluate the Credit Memo Copilot. Which approach is best?**

- A. Use the 200 most recent memos, whatever they contain
- B. Choose a fixed set of real cases that represents the normal mix plus known hard cases, with expected outputs checked by experienced credit officers
- C. Ask the model to generate test cases and expected answers
- D. Use only the hardest cases, so the score is conservative

<details><summary>Answer</summary>

**B.** A golden set should represent the real distribution, include the edge cases that matter, have trusted reference answers, and stay stable so scores are comparable over time. A is tempting because it is easy and recent, but it may miss rare, high-stakes cases and has no checked reference answers. C risks the model grading its own blind spots. D gives a score that does not reflect normal use. *(Evaluate · 6.1)*

</details>

**32. The new Smart Alerts model has a precision of 0.9 and a recall of 0.4 on fraud. What does this mean?**

- A. It catches 90% of fraud, but 40% of its alerts are false
- B. It is 90% accurate overall
- C. 40% of customers will receive an alert
- D. When it raises an alert it is usually right, but it misses about 60% of actual fraud

<details><summary>Answer</summary>

**D.** Precision is the share of alerts that are real fraud (0.9). Recall is the share of real fraud that gets an alert (0.4), so about 60% of fraud goes unflagged. A is the classic mix-up of the two. B confuses precision with accuracy. Whether this trade-off is acceptable depends on the error costs defined for the product. *(Evaluate · 6.1)*

</details>

**33. The Copilot scores 81% on the golden set, below the 90% launch bar. Faisal proposes switching to a bigger model. What should the team do first?**

- A. Error analysis: read the failing cases, group them by cause, and fix the largest group
- B. Switch to the bigger model and re-run the evals
- C. Lower the launch bar to 80%
- D. Add more cases to the golden set until the score rises

<details><summary>Answer</summary>

**A.** A single score does not say what is wrong. Reading and categorising failures often reveals causes a bigger model will not fix, such as retrieval missing a document, a prompt instruction being ignored, or a data format problem. B is tempting and sometimes right, but without knowing the causes you are spending money on a guess. C and D move the target instead of improving the product. *(Evaluate · 6.1)*

</details>

**34. Dana uses an LLM as a judge to compare two versions of a memo draft. It prefers whichever draft is shown first more often than chance would explain. What should she do?**

- A. Always show the new version first
- B. Replace the judge with a larger model and stop checking
- C. Run each comparison twice with the order swapped, and count only consistent verdicts or treat conflicts as ties
- D. Stop using LLM-as-judge entirely

<details><summary>Answer</summary>

**C.** Position bias is one of the known biases of LLM judges, along with verbosity bias and self-preference, described in work such as Zheng et al. (2023). Swapping the order controls for it. D is tempting as a safe choice, but it throws away a scalable tool when the bias has a standard fix. B assumes a bigger model is free of bias without checking. *(Evaluate · 6.2)*

</details>

**35. Before trusting an LLM judge to score thousands of Najm Assist answers each week, what is the most important step?**

- A. Write a very detailed judge prompt
- B. Compare the judge's scores with expert human ratings on a sample, measure how often they agree, and refine until agreement is acceptable
- C. Use the same model that generates the answers, so the judge understands them
- D. Run the judge on a small sample and check that the scores look reasonable

<details><summary>Answer</summary>

**B.** An LLM judge is itself a model that must be evaluated. Calibrating it against human judgement, using clear rubrics and measuring agreement, tells you whether its scores mean anything. A helps but proves nothing on its own. D is the tempting distractor: "looks reasonable" is not a measure. C risks self-preference bias. *(Evaluate · 6.2)*

</details>

**36. Before Najm Assist can take actions for customers, Layla asks for red-teaming. Which exercise fits best?**

- A. A survey of customer satisfaction with the beta
- B. Running the golden set a second time
- C. A load test to check the system handles peak traffic
- D. A structured attempt, by people briefed to act as attackers, to make the assistant break its rules: prompt injection, off-topic misuse, and trying to trigger actions on the wrong account

<details><summary>Answer</summary>

**D.** Red-teaming is deliberate adversarial testing to find failures that normal evaluation will not show. The Chevrolet dealer chatbot that was talked into "agreeing" to sell a car for $1 (Dec 2023) shows what untested manipulation looks like in public. B is tempting because it is an evaluation, but a golden set checks expected behaviour on normal cases, not what an adversary can make the system do. *(Evaluate · 6.2)*

</details>

**37. In an A/B test of a new Najm Assist design, the plan was a 50/50 split, but the treatment group has noticeably fewer users than control. The treatment is winning on the main metric. What should the team do?**

- A. Stop and investigate the imbalance before reading the results, because a sample ratio mismatch usually means something is broken in assignment or logging
- B. Ship the treatment, since it is winning
- C. Re-weight the groups statistically and report the result
- D. Extend the test until the groups are the same size

<details><summary>Answer</summary>

**A.** Kohavi, Tang and Xu (*Trustworthy Online Controlled Experiments*, 2020) treat sample ratio mismatch as a warning that the experiment itself is not trustworthy, for example because some treatment users crashed out or were not logged. B is the tempting distractor, but a win from a broken test is not evidence. C and D do not fix the underlying cause. *(Evaluate · 6.3)*

</details>

**38. A test of a new Smart Alerts model improves the main metric, fraud caught per thousand customers. The pre-agreed guardrail metric, customer complaints about blocked cards, has risen beyond its limit. What is the right call?**

- A. Ship, since the main metric improved
- B. Ship to half of customers as a compromise
- C. Do not ship as is: a breached guardrail means the change causes harm the team agreed not to accept, so investigate and adjust
- D. Replace the guardrail metric with one that did not move

<details><summary>Answer</summary>

**C.** Guardrail metrics exist to stop a win on the main metric from hiding unacceptable harm elsewhere. Agreeing them in advance is what makes them binding. A is tempting because the main goal improved, but it ignores the rule the team set. D is moving the goalposts after the result. *(Evaluate · 6.3)*

</details>

### Launch

**39. Faisal plans to launch SME Instant Finance to sole traders in the EU next month. The model has passed its evals. Which step is most clearly missing?**

- A. A marketing campaign
- B. A second round of offline evaluation
- C. A plan to measure adoption
- D. The governance gate: Layla's team must confirm the risk tier and required controls, since credit decisions about individuals can be high-risk under the EU AI Act

<details><summary>Answer</summary>

**D.** Launch readiness includes governance, not just model quality. Creditworthiness assessment of natural persons is listed as high-risk under the EU AI Act, and a sole trader is a natural person, so the classification and its obligations must be settled before launch. B is tempting because more testing feels safe, but the evals have passed; the missing piece is the approval and controls. The detail belongs to the *AI Governance: Zero to Hero* course. *(Launch · 7.1)*

</details>

**40. On launch day for Najm Assist, which preparation is most often forgotten by product teams?**

- A. The press release
- B. Contact-centre readiness: scripts for common AI errors, a way to see what the assistant told the customer, and a clear escalation path
- C. A launch party for the team
- D. A new logo for the assistant

<details><summary>Answer</summary>

**B.** When an AI product gets something wrong, customers call. Agents need to see the conversation, know how to correct it and know where to escalate. Without this, every AI error turns into a slow, frustrating complaint. A matters for awareness, but it does nothing to handle the problems that will arrive. *(Launch · 7.1)*

</details>

**41. After an update, a parcel company's customer chatbot swore at a customer and criticised the company, and screenshots spread widely (the DPD case, Jan 2024). What launch control would most directly have limited the damage?**

- A. A tested way to switch the AI feature off quickly or fall back to a safe mode, and regression tests before every update
- B. A longer privacy policy
- C. A more expensive model
- D. A larger marketing budget to repair the brand

<details><summary>Answer</summary>

**A.** Every AI launch needs a kill switch or fallback that the team has actually tested, and updates need regression evaluation before release. Together these shorten both the chance and the lifetime of an embarrassing failure. C is tempting because a stronger model may behave better, but it does not remove the need to test changes or to switch off quickly when something goes wrong. *(Launch · 7.1)*

</details>

**42. Marketing wants to launch the Credit Memo Copilot internally with the line "Perfect credit memos in one click." What should Faisal do?**

- A. Approve it, since internal launches do not need careful wording
- B. Remove all mention of AI
- C. Rewrite it to promise what the product reliably does, such as "A first draft in minutes, with sources for every figure, for you to review and sign", and check every claim in the demo
- D. Add "beta" to the line and keep the rest

<details><summary>Answer</summary>

**C.** Positioning sets expectations, and expectations drive trust. Overclaiming invites users to stop checking, and a public mistake in a demo can dominate the story, as with the factual error in Google's Bard launch demo (Feb 2023). D is tempting, but a "beta" label does not fix a promise of perfection or the missing message that the user must review. *(Launch · 7.2)*

</details>

**43. A neutral software company sells an AI support agent to other businesses. Its costs grow with every conversation, and its customers care about problems solved, not about seats. Which pricing signal fits best?**

- A. A one-time licence fee
- B. A fixed price per employee seat
- C. Free forever, funded by advertising
- D. Outcome-based pricing, such as a price per resolved conversation, with clear rules on what counts as resolved

<details><summary>Answer</summary>

**D.** Outcome-based pricing ties revenue to the value the customer sees and to the cost that grows with use. Intercom priced its Fin agent per resolution from 2023, and others followed with per-conversation models; exact prices change. B is tempting because seat pricing is familiar in software, but it breaks when AI does the work that seats used to represent, and it does not track per-use cost. *(Launch · 7.2)*

</details>

**44. Three months after Staff GenAI launched, only a small share of employees use it weekly, and most of them are in IT. What is the best next step?**

- A. Send an all-staff email reminding people it exists
- B. Find champions in each department, collect concrete use cases for their real tasks, and train people inside their own workflows
- C. Make its use mandatory
- D. Switch to a better model

<details><summary>Answer</summary>

**B.** Enterprise AI adoption is a change-management problem. People adopt a tool when they see how it helps with their own work, shown by colleagues they trust. A is tempting because it is quick, but awareness is rarely the barrier. C creates compliance without value. D assumes the model is the problem without evidence. *(Launch · 7.3)*

</details>

**45. Before rolling out the Credit Memo Copilot to all relationship managers, which enablement step matters most?**

- A. Train them on what the copilot does well and where it fails, and make clear that they remain responsible for the memo they sign
- B. Give them a video of the model's architecture
- C. Send them the vendor's marketing brochure
- D. Wait until they ask for training

<details><summary>Answer</summary>

**A.** Users of a draft-and-review product need to know where to look hard and who is accountable. That knowledge keeps the human review meaningful. B is tempting because it sounds thorough, but understanding the architecture does not tell a relationship manager which sections to check. *(Launch · 7.3)*

</details>

### Grow

**46. A neutral company reports that its AI assistant now handles most customer chats and has cut service costs. What should a careful PM ask before calling it a success?**

- A. How many tokens the assistant uses per day
- B. Whether competitors have similar numbers
- C. What happened to quality: resolution rates, repeat contacts, complaints and satisfaction, compared with human-handled chats
- D. How quickly the assistant replies

<details><summary>Answer</summary>

**C.** Cost savings are only half the picture. Klarna announced in 2024 that its assistant handled a large share of chats, and in 2025 said it would bring more human service back, which is a reminder to measure quality alongside cost. D is tempting because speed matters, but a fast answer that does not solve the problem only moves the contact elsewhere. *(Grow · 8.1)*

</details>

**47. Using Google's HEART framework, which metric is an example of the "Task success" category for the Credit Memo Copilot?**

- A. The share of drafts that reach the credit committee without the reviewer needing to rewrite a section
- B. The number of relationship managers who opened the copilot this month
- C. The share of users who still use it after three months
- D. Satisfaction survey scores

<details><summary>Answer</summary>

**A.** HEART (Rodden, Hutchinson and Fu, 2010) covers Happiness, Engagement, Adoption, Retention and Task success. Task success is about whether users complete what they came to do, efficiently and correctly. B is adoption, C is retention and D is happiness. B is the most tempting because it is the easiest number to get, but it says nothing about whether the work got done well. *(Grow · 8.1)*

</details>

**48. Rania asks Faisal to propose a North Star metric for the Credit Memo Copilot. Which is best?**

- A. Number of drafts generated
- B. Tokens processed per month
- C. Average user rating of drafts
- D. Hours saved per credit application with memo quality at or above the agreed bar

<details><summary>Answer</summary>

**D.** A North Star metric should capture the value delivered to users and the business, and resist gaming. Pairing time saved with a quality condition prevents speed at the expense of good credit memos. A is tempting because it grows with use, but drafts generated can rise while value falls, for example if people regenerate bad drafts repeatedly. *(Grow · 8.1)*

</details>

**49. Tariq estimates that each Credit Memo Copilot memo needs 5 model calls, each averaging 8,000 input tokens and 1,000 output tokens. Using illustrative prices of $3 per million input tokens and $15 per million output tokens, what is the model cost per memo?**

- A. About $0.04
- B. About $0.20
- C. About $0.12
- D. About $1.95

<details><summary>Answer</summary>

**B.** Input: 5 × 8,000 = 40,000 tokens × $3 per million = $0.12. Output: 5 × 1,000 = 5,000 tokens × $15 per million = $0.075. Total ≈ $0.195. C is the tempting distractor because it counts only input tokens. A real cost-per-task model would also add retries, retrieval, guardrail calls and infrastructure. The prices here are illustrative, not current market rates. *(Grow · 8.2)*

</details>

**50. A neutral software company added an "unlimited AI" feature to its flat monthly subscription. A small group of heavy users now costs more to serve than they pay. What is the best response?**

- A. Remove the AI feature for everyone
- B. Raise the price for all customers by the same amount
- C. Redesign pricing so it reflects usage, for example fair-use limits in the base plan and a premium tier or usage-based pricing for heavy use
- D. Ignore it, since heavy users are a small group

<details><summary>Answer</summary>

**C.** When each use has a real cost, flat unlimited pricing can turn your best users into your least profitable. Tiers, limits or usage-based pricing keep margins healthy while leaving room for value; Duolingo, for example, put its GenAI features in a premium tier (Duolingo Max, 2023). B is tempting because it is simple, but it charges light users for heavy users' costs and may push them away. *(Grow · 8.2)*

</details>

**51. Six months after launch, SME Instant Finance's approval rate has drifted up while its early repayment performance has weakened. Nothing in the model has changed. What is the most likely explanation, and the right response?**

- A. The kind of applicants or the economic conditions have shifted, so the data no longer matches training. Investigate drift in inputs and outcomes and trigger review or retraining
- B. The model has a software bug; roll back to an older version
- C. Relationship managers are overriding decisions; restrict their access
- D. It is random noise; wait another six months

<details><summary>Answer</summary>

**A.** A model can degrade without any code change when the world it scores changes. Monitoring input distributions and outcomes, and having a defined review and retraining path, is part of running an AI product after launch. D is tempting because noise is possible, but in credit, waiting six months could be expensive. *(Grow · 8.3)*

</details>

**52. The model vendor behind Najm Assist announces that it will retire the model version the bank uses and move customers to a newer one. What should Faisal do?**

- A. Assume the newer version is better and switch on the retirement date
- B. Ask the vendor to keep the old version forever
- C. Rebuild the assistant from scratch
- D. Run the full eval suite on the new version before switching, compare results on the golden set and key risk cases, and fix any regressions in prompts or guardrails

<details><summary>Answer</summary>

**D.** A new model version can change behaviour in ways a general benchmark will not show on your task. Regression evaluation on your own data is the only way to know. A is the tempting distractor because newer models are often better on average, but "better on average" can still break a behaviour your product depends on. *(Grow · 8.3)*

</details>

**53. In its first two weeks, Najm Assist's new spending-insights feature had very high weekly usage, which has since fallen steadily. What should Faisal look at to understand the real picture?**

- A. Total usage since launch, which is still high
- B. Retention by launch cohort, to see whether people who tried it keep coming back, and what the returning users use it for
- C. The number of app downloads
- D. The feature's average response time

<details><summary>Answer</summary>

**B.** Early spikes often reflect curiosity rather than lasting value. This is a novelty effect. Cohort retention shows whether the feature became a habit for anyone, and for whom. A is tempting because it looks good in a report, but a cumulative total hides the decline you need to understand. *(Grow · 8.1)*

</details>

### Lead

**54. Najm's board asks what will protect the Credit Memo Copilot from being copied, when competitors can buy the same models. What is the best answer?**

- A. Our prompts are secret
- B. We use the largest model available
- C. We launched first
- D. Our advantage comes from what others cannot easily copy: our credit data and feedback from our experts' edits, deep integration into our lending workflow, and the trust of our relationship managers

<details><summary>Answer</summary>

**D.** When models are widely available, defensibility comes from proprietary data, feedback loops that improve the product with use, workflow integration and distribution. C is tempting because being first can help, but on its own it rarely lasts if the product is easy to copy. A and B are easy for competitors to match. *(Lead · 9.1)*

</details>

**55. New models appear every few months, and Tariq worries that the team's choices will quickly go out of date. Which roadmap principle helps most?**

- A. Wait for the models to settle before building anything
- B. Commit to one vendor for five years to avoid churn
- C. Design so the model can be changed: keep a thin layer between the product and the model, own the eval suite, and treat the model as a replaceable component
- D. Rebuild the product each time a new model is released

<details><summary>Answer</summary>

**C.** Under fast model change, the durable assets are your evals, data, workflow integration and product logic. Keeping the model swappable, and your own evals as the test for any switch, lets you take improvements without rebuilding. A is tempting as a cautious choice, but waiting means you never learn or deliver. B locks you in. *(Lead · 9.2)*

</details>

**56. Rania asks Faisal to redo his 12-month roadmap, which lists ten AI features with fixed delivery dates. What is she most likely asking for?**

- A. More features, to show ambition
- B. A roadmap framed as bets: the outcome each bet targets, the key uncertainty, how it will be tested, and the point at which the team will continue, change or stop
- C. Dates moved later to add buffer
- D. A single feature, to reduce risk

<details><summary>Answer</summary>

**B.** AI work carries real uncertainty about whether quality can be reached. Framing the roadmap as bets with evidence points and decision rules is more honest and helps the team decide sooner. C is tempting because it reduces the risk of missing dates, but it keeps the false certainty of a feature-and-date list. *(Lead · 9.2)*

</details>

**57. Najm Bank now has five AI products. Each team built its own evaluation tools, guardrails and model access, and costs and quality vary widely. What operating model change fits best?**

- A. A shared AI platform team that provides common model access, evaluation tooling, guardrails and cost tracking, with product teams keeping ownership of their product outcomes
- B. Merge all five product teams into one central team
- C. Let each team continue as it is, since autonomy drives speed
- D. Outsource all AI products to one vendor

<details><summary>Answer</summary>

**A.** As AI products multiply, the parts every team needs, such as evals, guardrails, model access and cost visibility, are worth building once. Product teams keep responsibility for their users and outcomes. B is tempting because it gives consistency, but centralising product decisions slows teams and moves decisions away from the users. C keeps the duplication and uneven quality. *(Lead · 9.3)*

</details>

**58. SME Instant Finance is designed to automatically decline some applications from EU sole traders, with no human involvement. Which requirement must Faisal design for, working with Layla and Sara?**

- A. A notice in the app's terms and conditions is enough
- B. Declines are allowed only if the model is more accurate than humans
- C. Nothing, since invoice finance is a business product
- D. Under GDPR Article 22, people have rights around solely automated decisions with significant effects, including in many cases the right to obtain human intervention and to contest the decision, so the product needs a real human review path

<details><summary>Answer</summary>

**D.** A sole trader is a natural person, and a credit decline can have a significant effect on them. Article 22 of the GDPR restricts solely automated decisions of this kind and, where they are allowed, requires safeguards such as human intervention and the right to contest. The PM's part is to design that path into the product. C is the tempting distractor because the product is for businesses, but sole traders are individuals. The legal detail belongs in *AI Governance: Zero to Hero*. *(Lead · 9.4)*

</details>

**59. Khalid wants to raise SME Instant Finance's automatic approval limit sharply after a strong first quarter. What is the best leadership response?**

- A. Agree, since the results are strong
- B. Refuse any increase until the model has run for five years
- C. Increase in stages with exposure caps, keep monitoring outcomes and drift, and agree in advance what would trigger a pull-back
- D. Leave the decision to the data science team

<details><summary>Answer</summary>

**C.** One good quarter says little about how a model behaves under different conditions. Staged expansion with limits caps the damage if the world changes. Zillow Offers was wound down in 2021 after its pricing algorithm mispriced homes at scale, with large write-downs. A is tempting because the results are good, but it takes on the full downside of a model that has not been tested in a different economy. *(Lead · 9.2)*

</details>

**60. In an interview for an AI product manager role, Faisal is asked to talk about a project in his portfolio. Which answer will impress most?**

- A. A detailed description of the model architecture and the prompts he wrote
- B. The problem and user, the decision he made about where AI fit, how he defined and measured quality, a trade-off he chose and why, and what the results showed, including what did not work
- C. A live demo of the product working well on a hand-picked example
- D. A list of every AI tool he has used

<details><summary>Answer</summary>

**B.** Hiring managers for AI PM roles look for product judgement: problem framing, evaluation, trade-offs and learning from results. Showing what did not work demonstrates honesty and rigour. C is tempting because demos are vivid, but a polished demo on a chosen example hides exactly what an AI PM is paid to understand. The gap between demo and real workflow is one lesson often drawn from IBM Watson Health, whose units were sold in 2022 after a large investment. *(Lead · 10.2)*

</details>

## 🧾 Recap
- **54–60 correct:** excellent. You are ready to lead an AI product from idea to scale. Use the error log to polish the few gaps.
- **48–53 correct:** strong, and at this course's rule of thumb. Re-read the lessons behind every wrong answer.
- **36–47 correct:** solid foundations with gaps. Find your two weakest stages in the table under "How it works", re-work those modules and their check-yourself questions, then sit the exam again after a week.
- **Below 36:** go back through Modules 2–9 in order, doing the exercises this time, and take the capstone in 10.1 before trying again.
- Whatever your score, review every question you guessed. A lucky guess is a gap you have not found yet.

## 📚 References
- Teresa Torres, *Continuous Discovery Habits* (2021) — https://www.producttalk.org/
- Marty Cagan, *Inspired* (2nd ed., 2017) — https://www.svpg.com/
- Ron Kohavi, Diane Tang and Ya Xu, *Trustworthy Online Controlled Experiments* (2020) — https://experimentguide.com/
- Saleema Amershi et al., "Guidelines for Human-AI Interaction", CHI 2019 — https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/
- Google PAIR, People + AI Guidebook — https://pair.withgoogle.com/guidebook/
- Lianmin Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (2023) — https://arxiv.org/abs/2306.05685
- Kerry Rodden, Hilary Hutchinson and Xin Fu, "Measuring the User Experience on a Large Scale: User-Centered Metrics for Web Applications", CHI 2010 — https://research.google/
- EU AI Act, Regulation (EU) 2024/1689 — https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- GDPR, Regulation (EU) 2016/679 — https://eur-lex.europa.eu/eli/reg/2016/679/oj
