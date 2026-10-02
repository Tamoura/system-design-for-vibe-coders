# Module 1 — The skills employers check

*A degree tells an employer that you can learn. It does not tell them that you can work in a shared codebase, find a bug you did not write, check what an AI agent produced, or keep software running once real people use it. Those are the things hiring managers and interviewers now look for in a junior, and many graduates have never been taught them directly. This module names that baseline and shows what "good enough for a junior" looks like for each part. It starts with the everyday skills: Git, reading code, debugging, testing and writing things down. It then covers building with AI coding agents in a way that shows your judgement rather than hiding the lack of it. It ends with production thinking: the gap between "it runs on my laptop" and "it runs for users". You will follow Omar, who has never deployed anything; Reem, who builds fast with agents but cannot always explain her code; Huda, Yousef and Mohammed. Khalid, the Najm Bank engineering manager who hires juniors, and Tariq, who runs technical interviews, explain how they tell the difference. Each lesson points you to the lessons elsewhere in the library that build the skill in depth, and leaves you with an artefact: a skills audit, a verification checklist and a ship-ready checklist.*

> **Steps:** Learn, Build — learning the baseline every employer checks, and building the habits and evidence that show you have it.

---

# 1.1 — The junior baseline: Git, reading code, debugging, testing and writing it down
*Level: 🟢 Beginner* · *Prerequisites: 0.1, 0.2* · *Step: Learn, Build*

## ⚡ In 60 seconds
- Whatever the role (software, AI, data, platform or security), employers expect five everyday skills from a junior: **Git**, **reading code**, **debugging**, **testing** and **writing it down**.
- None of them is advanced. Together they show that you can work safely in someone else's codebase, and that is what a hiring manager is really asking about.
- The rule that matters most: **leave a trail**. Small commits with clear messages, a test that proves the fix, a pull request that explains why. Your reasoning should be visible to the next person.
- Decision cue: before asking for help, can you say what you expected, what happened and what you tried? If not, you are still debugging.
- Biggest trap: treating these skills as "too basic to show". Interviewers check them directly, through your repository history, live debugging rounds and "walk me through this code".

## 🧭 Why it matters
Omar has a first-class CS degree and excels at algorithm puzzles. For Najm Bank's graduate take-home, he builds a small transaction-categorisation service, and the code is good. He submits it as a zip file: no Git history, no tests, a README that says only "run main.py". In the follow-up interview, Tariq shows a failing input Omar never tried and asks him to find the cause. Omar reads from the top, changes three things at once, and loses track of which change mattered. Twenty minutes pass. The problem was a date-format assumption on line 41.

Khalid explains the decision to Aisha, the recruiter: "His algorithms are better than mine. But in his first month he will mostly read code he didn't write, chase bugs he didn't cause, and explain his changes in pull requests. I saw no evidence he can do that yet." Omar is invited to reapply to the next intake, with a list of what was missing.

Omar's gap is common, and it is not about intelligence. University often grades the final answer; workplaces grade the process, because other people live with your work. This lesson names the five baseline skills, what each looks like at junior level, and how to show it.

## 📐 How it works

### 🟢 The essentials

**Why these five.** A junior rarely starts on a blank page. You join an existing codebase and change it in small pieces that others review. These five skills make that safe:

| Skill | What "good enough for a junior" looks like | What "not yet" looks like |
|---|---|---|
| **Git** | Branch, commit small changes with clear messages, open a pull request, respond to review, resolve a simple conflict, undo a mistake calmly | Code shared as zip files or one giant commit called "final"; fear of the terminal; force-pushing over others' work |
| **Reading code** | Find the entry point, follow one request through the code, use search, read the tests | Reading from line 1 to the end; rewriting code you do not understand yet |
| **Debugging** | Reproduce, read the stack trace, narrow down, test one idea at a time, confirm the fix | Changing things at random until it works; not knowing why it now works |
| **Testing** | Write a unit test, run the suite, add a test that fails before your fix and passes after | "I tested it manually"; tests that check nothing; deleting a failing test to make it pass |
| **Writing it down** | Commit messages that say why, a pull request a reviewer can follow, a README others can run, questions that say what you tried | "fixed stuff"; "it doesn't work, help"; a README that only you can use |

**Git, briefly.** **Git** is a version control system: it records every change so you can see who changed what, when and why, and go back. A **commit** is one saved change with a message. A **branch** is a separate line of work. A **pull request** (PR; GitLab calls it a merge request) asks for your branch to be reviewed and merged, usually on GitHub, GitLab or Bitbucket. If this is new, the library's [*System Design for Vibe Coders*, lesson F.3 — Versions, repos, and deploys — how software moves](../vibe/index.en.html#lF-3) explains it from scratch.

A commit message is where your reasoning lives. Compare:

| Weak | Strong |
|---|---|
| `fix` | `Parse transaction dates in day-first format` |
| `changes` | `Reject negative amounts in categoriser input` |
| `final version 2` | `Add test for empty merchant name` |

The strong versions say what the commit does, one change each. When the reason is not obvious, add a body after a blank line explaining why. Some teams use the **Conventional Commits** format (`fix: …`, `feat: …`); follow what the team already does.

**Reading code.** The skill nobody teaches, and the one you will use most. A method for an unfamiliar repository:

1. Read the README and find how to run it and how to run its tests. Run both.
2. Find the **entry point**: the `main` function, the web route, the command, the scheduled job.
3. Pick one real action ("a user uploads a statement") and follow it through the code, writing down the files and functions it touches.
4. Read the **tests** for that part: they show what the code is supposed to do, with examples.
5. Search (`git grep` or "find in files") for the error message or function name instead of scrolling.

The library's [*SaaS Building Blocks*, lesson 0.2 — How to read a giant open-source codebase without drowning](../saas/index.html#/0.2) applies the same method to large open-source projects.

**Debugging.** Debugging is a loop you can follow under pressure, not a talent:

```mermaid
flowchart LR
    R["Reproduce it reliably"] --> O["Observe: read the error and stack trace"]
    O --> H["Form one hypothesis"]
    H --> T["Test it with one change or one print"]
    T -->|"wrong"| H
    T -->|"right"| F["Fix it and add a test"]
    F --> V["Verify the original case and the suite"]
```

Two habits matter most: **reproduce first** (or you cannot know you fixed it), and **change one thing at a time**. A **stack trace** lists the function calls active when an error happened; the useful line is usually the last one in *your* code. Learn your editor's **debugger** (breakpoints, stepping, inspecting variables); it beats twenty print statements.

**Testing.** A **unit test** checks one small piece of code (usually a function) in isolation. An **integration test** checks that several pieces work together, for example your code and a real database. Most tests follow the shape **arrange, act, assert**: set up the input, run the code, check the result.

```python
# A regression test: it failed before Omar's fix and passes after it
from categoriser import parse_date

def test_parses_day_first_dates():
    # arrange: a date that is ambiguous if read month-first
    raw = "03/11/2025"
    # act
    result = parse_date(raw)
    # assert: 3 November, not 11 March
    assert (result.day, result.month) == (3, 11)
```

The junior habit: **every bug fix comes with a test that would have caught it.** It is your proof, and it stops the bug returning.

**Writing it down.** Commit messages, pull request descriptions, READMEs and questions cover most of a junior's writing. A good question to a colleague has four parts: what you are trying to do, what you expected, what happened instead (with the exact error), and what you already tried. "The tests don't work, can you help?" costs a senior ten minutes of questions; the four-part version often gets answered in one, and sometimes you answer it yourself while writing it.

### 🟡 Going deeper

**How interviews test the baseline.** Few interviews say "now we will test your Git". The skills are checked indirectly:

| Where | What they look at | What a strong signal looks like |
|---|---|---|
| Your GitHub or take-home repository | Commit history, tests, README | Many small commits with clear messages; tests that run; a README a stranger can follow |
| Live debugging round | Your process under mild pressure | You reproduce first, state a hypothesis, change one thing at a time |
| Code-reading round | Whether you can follow unfamiliar code | You trace inputs to outputs and spot an edge case |
| "Walk me through your project" | Whether you understand your own work | You can explain any file, any decision, and what you would change |

Module 5 covers interview formats. A well-kept repository is evidence an interviewer can check before meeting you.

**A pull request a reviewer can follow.** The description should answer three questions: what changed, why, and how you know it works.

```text
What:
Parse statement dates as day-first (DD/MM/YYYY).

Why:
Najm's CSV export uses day-first dates. We parsed them month-first,
so 03/11 became 11 March. Reported in issue #14.

How I tested it:
- Added `test_parses_day_first_dates` (fails on main, passes here).
- Ran the full suite: 42 passed.
- Imported the November sample file; all 318 rows have correct dates.
```

Keep pull requests small: a 50-line change gets a careful review; a 2,000-line change gets skimmed.

**Undoing and searching history.** Know the escape routes: `git status` and `git diff` to see where you are, `git restore` to drop uncommitted changes, `git revert` to undo a shared commit with a new one, and `git reflog` to find a "lost" commit. Avoid force-pushing a shared branch. `git bisect` binary-searches history for the commit that introduced a bug; on small commits it points to five lines, on one huge commit to everything.

**Testing beyond the basics.** Juniors extend an existing suite rather than design a strategy. Know the vocabulary: **fixtures** (shared setup), **mocks** (stand-ins for external things such as a payment API), **coverage** (a useful hint, a bad target) and **continuous integration** (CI: tests run automatically on every push). The library's [*System Design for Vibe Coders*, lesson 8.2 — Tests as the spec the agent can't ignore](../vibe/index.en.html#l8-2) shows why tests matter even more when an agent writes the code, and [*System Design for Vibe Coders*, lesson 8.3 — CI preflight and the boy-who-cried-wolf check](../vibe/index.en.html#l8-3) covers CI.

**The baseline by role.** Huda (data science) reads SQL and pipeline code, and her tests include data checks such as "no duplicate rows". Yousef (cloud) reads infrastructure code and logs. Mohammed (bootcamp) has good Git habits; his gap is reading codebases larger than his own. Module 2 maps each role.

### 🔴 Expert view

**What seniors actually notice.** Reviewing a junior's first month, Khalid does not count lines of code. He asks: are the changes **small and reversible**, does each fix come with **evidence**, and can he **follow the reasoning** without asking? Juniors who do this are trusted with bigger work quickly, because they are cheap to supervise.

**Why AI makes the baseline more important.** As AI tools write more routine code, human effort moves to this lesson's skills: reading the agent's code, debugging failures you did not cause, testing to verify a claim, and writing down what changed. Lesson 1.2 builds on this. A graduate who can generate code but not check it is replaceable by the tool; one who can check the tool's work is who the team needs.

**Writing is a technical skill.** Much engineering happens in issues, pull requests and chat. In the Gulf, many teams work in English with Arabic-speaking colleagues and customers; clear technical English, and explaining the same thing in Arabic to a business user, are real advantages. Put the conclusion first and include the exact command or error.

**Make your baseline visible.** "Proficient in Git" on a CV means nothing. A clean repository history, a well-described pull request, tests in CI and a short bug write-up prove it. Module 3 turns this into a portfolio.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Pro Git** (Scott Chacon and Ben Straub) | The free, official Git book: concepts, commands, branching and undoing mistakes | Learning Git properly instead of memorising commands |
| **Conventional Commits** | A lightweight convention for commit messages (`fix:`, `feat:`, `docs:`) | When a team uses it, or for your own projects to keep history readable |
| **git bisect** | Built-in Git command that binary-searches history to find the commit that introduced a bug | A bug that "used to work"; practising on your own project |
| **pytest** | A widely used Python test framework with simple `assert`-based tests (Jest and JUnit fill the same role in JavaScript and Java) | Writing your first unit and regression tests |
| **Minimal reproducible example** | The smallest code and input that still shows the bug, as described in Stack Overflow's help centre | Before asking a question anywhere; often it reveals the answer |
| **Pull request template** | A short What / Why / How I tested it / Notes form added to the repository | Every pull request, including on solo projects |

## 🏛️ In practice at Najm Bank
Khalid asks every graduate to fill in the **Junior baseline audit** in week zero of the Najm Tech Graduate Programme, and gives the same template to candidates invited to reapply. The rule is "evidence, not adjectives": every rating needs a link someone else can check. Here is Omar's, done six weeks after his first interview, before he reapplies.

| Skill | Can I show it? Evidence (link or file) | Rating: not yet / getting there / ready | Next action and date |
|---|---|---|---|
| Git | Categoriser repository with 37 commits, 4 merged pull requests | Getting there | Resolve a real merge conflict on a pair project by 15 Nov |
| Reading code | A one-page trace of how an upload moves through an open-source finance app's code | Getting there | Trace a second project, this time in a language I know less well |
| Debugging | A write-up of the date-format bug, with reproduce, hypothesis, fix and test | Ready | Practise one timed "fix the failing test" exercise a week |
| Testing | 42 tests running in CI, a regression test for every fixed bug | Ready | Learn fixtures and mocks for the bank-API client |
| Writing it down | README a classmate followed from scratch in ten minutes; pull request descriptions in the template | Getting there | Ask Huda to review two pull request descriptions |

Khalid's review questions for each row: "Could a stranger verify this in two minutes? Is the rating honest? Is the next action specific?" The mentor reviews it again at day 30 (Module 6).

## 🛠️ Exercises
- 🟢 Put one existing project in Git and make five small commits that each do one thing: a README with run instructions, a `.gitignore`, one test, one small fix, one tidy-up. *Done when:* `git log --oneline` shows five or more commits whose messages a classmate can understand without opening the code.
- 🟡 In a small open-source project, use the five-step reading method to trace one user action from entry point to result, and list the files and functions in order on one page. Run its tests, then break one thing on purpose and see which test fails. *Done when:* the note exists, and a peer who follows your list of files can find the same path in under ten minutes.
- 🔴 Have a friend hide a realistic bug among several small commits in your project. Find it with `git bisect`, fix it with a regression test, and open a pull request using this lesson's template. *Done when:* the pull request shows the failing-then-passing test, the description states the commit that introduced the bug, and someone else can review it without asking you a question.

## ⚠️ Mistakes and traps
- **Thinking the baseline is too basic to show.** Interviewers check it directly. Instead, make it visible: clean history, tests, a README, a debugging write-up.
- **One giant commit at the end.** It hides your process and makes review impossible. Commit small, working steps as you go.
- **Changing several things at once while debugging.** You lose track of what fixed it. Reproduce, then test one hypothesis at a time.
- **Fixing a bug without a test.** The bug comes back and nobody can verify your claim. Add a regression test that fails before the fix.
- **Asking "it doesn't work, help?"** It costs a senior ten minutes to find out what you already know. Ask with the goal, the expectation, the actual result and what you tried.

## 🧾 Recap
- The junior baseline is five everyday skills: Git, reading code, debugging, testing and writing it down.
- Debug with a loop: reproduce, observe, one hypothesis, test it, fix with a test, verify.
- Every fix gets a regression test; every change gets a message that says why.
- AI tools raise the value of these skills: reading, checking and explaining become more of the job.
- Show the baseline with evidence (repository history, tests, write-ups), not adjectives on a CV.

## ✍️ Check yourself

**1. In Omar's take-home follow-up, Tariq shows a failing input and asks him to find the cause. What should Omar do first?**

- A. Read the whole codebase from the top so he understands everything before touching it
- B. Reproduce the failure reliably and read the error and stack trace
- C. Change the three most likely lines at once to save time
- D. Rewrite the parsing function in a cleaner style

<details><summary>Answer</summary>

**B.** You cannot know you fixed a bug you cannot reproduce, and the stack trace points where to look. C is what Omar did, and it hid which change mattered. (🟢 The essentials, debugging loop.)

</details>

**2. Which commit message best follows the advice in this lesson?**

- A. `final version`
- B. `fixed bug`
- C. `changes to parser and tests and readme`
- D. `Parse statement dates as day-first`

<details><summary>Answer</summary>

**D.** It says what the commit does, in the imperative, and covers one change. C at least lists what changed, but it bundles three unrelated changes and does not say why. (🟢 The essentials, Git.)

</details>

**3. Huda is stuck on a failing data-import test and wants to ask Dana for help in the team chat. Which message is most useful?**

- A. "`pytest tests/test_import.py` fails with `KeyError: 'amount'` on the March file. I expected the header row to be skipped. The file has a header and the January file passes. Has the March export format changed?"
- B. "The import tests are broken again since this morning's merge, and I have no idea why. Can you take a look when you have time today?"
- C. "Is there any documentation for the import code? I want to understand how the March file is read before I touch anything in it."
- D. "I think the import code has a bug in how it reads the amount column. Should I rewrite the whole module from scratch?"

<details><summary>Answer</summary>

**A.** It gives the goal, the exact error, the expectation and what she already checked, so Dana can answer quickly. B sounds polite but forces Dana to start from zero. (🟢 The essentials, writing it down.)

</details>

**4. You are given an unfamiliar repository and asked to change how one report is generated. According to the reading method in this lesson, what is the best early step after running the project?**

- A. Read every file in the repository in alphabetical order, so that nothing is missed
- B. Delete code that looks unused, to reduce what you must read and review
- C. Find the report's entry point, follow it through the code and read its tests
- D. Ask an AI tool to rewrite the whole module in a style you already understand

<details><summary>Answer</summary>

**C.** Following one real action from its entry point, with the tests as examples, is the fastest way in. B is dangerous: "unused-looking" code may handle a case you have not seen. (🟢 The essentials, reading code.)

</details>

**5. Khalid says the five baseline skills matter more, not less, now that AI agents write much routine code. Why?**

- A. Because AI tools cannot use Git, so a human must still make every commit by hand
- B. Because human effort shifts toward checking and explaining the code the tool produced
- C. Because most employers have now banned AI coding tools for junior developers
- D. Because the skills are needed to pass the interview, even if the job no longer uses them

<details><summary>Answer</summary>

**B.** When a tool writes the code, someone must check and explain it, and that is the baseline. C is not true in general; policies vary by employer and by task. (🔴 Expert view.)

</details>

## 📚 References
- Scott Chacon and Ben Straub, *Pro Git* (free online) — https://git-scm.com/book/en/v2
- Git documentation, `git bisect` — https://git-scm.com/docs/git-bisect
- Conventional Commits — https://www.conventionalcommits.org/
- GitHub Docs, About pull requests — https://docs.github.com/en/pull-requests
- pytest documentation — https://docs.pytest.org/
- Stack Overflow Help Center, How to create a Minimal, Reproducible Example — https://stackoverflow.com/help/minimal-reproducible-example
- [*System Design for Vibe Coders*, lesson F.3 — Versions, repos, and deploys — how software moves](../vibe/index.en.html#lF-3)

---

# 1.2 — Building with AI coding agents without being carried by them
*Level: 🟢 Beginner* · *Prerequisites: 1.1* · *Step: Learn, Build*

## ⚡ In 60 seconds
- Many employers expect developers to use AI coding tools well. They check whether **your judgement** is visible: you specify, read, verify and can explain.
- You are **carried** when you cannot explain, change or debug the code the agent wrote. Interviewers are good at finding this.
- The rule that matters most: **you own every line you submit**, whoever or whatever typed it. If you cannot explain it, you are not ready to commit it.
- Decision cue: before you accept an agent's change, ask "could I explain this diff, line by line, to Tariq, and show how I know it works?"
- Integrity: AI rules differ between employers and rounds. **Always ask**, follow the answer, and disclose AI help honestly.
- Biggest trap: using the agent to skip the learning. It shows in the first interview question that goes one level deeper.

## 🧭 Why it matters
Reem is the fastest builder in the cohort: with an AI coding agent she built three side projects in a month. For Najm's take-home, which allowed AI tools if candidates said which ones they used, she delivers a polished service in an afternoon, with tests and a good README, and discloses her tools.

The follow-up interview goes differently. Tariq opens her code and asks three questions. "Why does the retry loop wait longer each time?" Reem is not sure; the agent added it. "This test mocks the database. What would happen with a real one if two requests arrived at once?" She does not know. "Your config file has an API key in a test fixture. Is it real?" It is: a free-tier key she had pasted into the chat with the agent, which put it in the file. Tariq is not bothered that she used AI. He is bothered that the code was more capable than its author.

Khalid's feedback: "Reem is excellent at getting things built. We need to see that she's in charge of what gets built." This lesson takes the hiring view of that difference: what employers check, how interviews probe it, and how to use agents so they make you stronger rather than hollow.

## 📐 How it works

### 🟢 The essentials

**Three levels of AI help.** Coding tools differ by how much they do on their own:

| Level | What it does | Examples (at the time of writing, 2026) | Main risk for a junior |
|---|---|---|---|
| Autocomplete | Suggests the next lines as you type | Inline suggestions in GitHub Copilot and most editors | Accepting plausible lines without reading them |
| Chat assistant | Answers questions and writes snippets you paste in | Editor chat panels; general assistants | Pasting code into a context it does not fit |
| Coding agent | Reads the repository, edits many files, runs commands and tests, and iterates | Claude Code, GitHub Copilot's agent features, Cursor's agent mode, and others | Large, confident changes you never fully read |

Tools change quickly; the principles below do not depend on which one you use.

**What employers check.** When a team hires a junior who will use AI tools, the questions behind the interview are:
- **Can you specify?** Can you turn a vague request into a clear, small task with acceptance criteria?
- **Can you review?** Do you read the diff (the exact lines changed) and notice what is wrong, missing or unnecessary?
- **Can you verify?** Do you prove it works with tests and real runs, rather than trusting the agent's summary?
- **Can you explain?** Can you say why each part is there, and what you would change?
- **Are you honest?** Do you follow the rules about AI use and say what you used?

Notice that these are the baseline skills of lesson 1.1, aimed at code someone else (the agent) wrote.

**A workflow that keeps you in charge.**

```mermaid
flowchart LR
    S["Specify a small task with acceptance criteria"] --> G["Agent proposes or writes the change"]
    G --> R["You read the whole diff"]
    R -->|"unclear or wrong"| S
    R --> V["Run tests and a real check"]
    V -->|"fails"| S
    V --> E["Explain-back: could you defend every line"]
    E -->|"no"| L["Learn the part you cannot explain"]
    L --> E
    E -->|"yes"| C["Commit with an honest message"]
```

Three habits make this loop work:
1. **Small tasks.** "Validate the amount field, rejecting negatives and non-numbers, with tests" is reviewable. "Build the backend" is not.
2. **Read the whole diff,** not the agent's summary. Agents sometimes report success for incomplete work, or change files you did not ask about.
3. **The explain-back test.** Before committing, explain the change as if to a reviewer. Every hesitation is something to learn before you commit.

**Integrity rules.** Using AI is not cheating when it is allowed. These things are:
- Pretending AI-written work is your own unaided work when you were asked to work alone.
- Using AI in an interview round where it is not allowed, including hidden tools that feed you answers during a live interview.
- Submitting code you cannot explain as evidence of your skill.
- Pasting an employer's or university's confidential code or data into a tool that is not approved for it.

The practical rule: **ask before every assessment** ("Are AI tools allowed in this round? Should I say which I used?"). Many employers allow or expect AI in some rounds, such as take-homes, and ban it in others, such as live algorithm rounds. Never assume.

### 🟡 Going deeper

**What agents commonly get wrong.** Knowing the usual failures tells you where to look in a diff:

| Failure | What it looks like | How to catch it |
|---|---|---|
| Invented APIs or packages | A function or library that does not exist, or a package name that is almost right | Run it; check the official docs; check the package registry before installing |
| Plausible but wrong edge cases | Works on the example; fails on empty input, time zones, currency rounding, concurrent requests | Write tests for the edges yourself before you ask for the code |
| Over-broad changes | Asked to fix one bug, it also "tidied" five unrelated files | Read the full file list in the diff; reject changes you did not ask for |
| Weakened tests | A failing test is changed or deleted until it passes | Treat any test change as suspicious; ask why the test was wrong |
| Insecure defaults | String-built SQL, missing authorisation checks, secrets in code, overly permissive settings | Use a security checklist; run secret scanning and static analysis |
| Confident wrong summaries | "All tests pass" when some were skipped | Run the tests yourself and read the output |

The library covers these in depth: [*Secure AI & Application Security*, lesson 6.3 — Securing AI-generated code: what coding agents get wrong](../secai/index.html#/6.3) for the security side, and [*System Design for Vibe Coders*, lesson 9.4 — Verification before completion](../vibe/index.en.html#l9-4) for the habit of proving work is done.

**Specifying with tests first.** Write the test cases before the agent writes the code: you decide what "correct" means, and the agent has to meet it. A prompt like this shows visible judgement:

```text
Task: add amount validation to POST /transactions.
Rules: reject negative amounts, zero, non-numeric strings and more
than 2 decimal places, with HTTP 422 and a clear error message.
Do not change any other endpoint. Do not modify existing tests.
First, show me the test cases you will add. Wait for my approval
before writing the implementation.
```

[*System Design for Vibe Coders*, lesson 8.2 — Tests as the spec the agent can't ignore](../vibe/index.en.html#l8-2) builds this habit fully.

**How interviews probe it.** Expect some of these, and ask in advance which apply:
- **"Walk me through your take-home."** The interviewer picks a random line and asks why. This is where carried candidates are found.
- **"Extend it live,"** sometimes without AI tools. Easy if you understood your code.
- **AI-allowed live coding.** The interviewer watches how you prompt, read and verify.
- **Reviewing a flawed AI-written pull request.** Described by interviewers and hiring guides as an increasingly common exercise at the time of writing (2026). Lesson 5.2 covers it.
- **Algorithm rounds without AI.** Still common at large technology firms. They test reasoning you cannot borrow.

**Learning mode versus producing mode.** When **learning** something new, ask the agent to explain, quiz you, or review code *you* wrote. When **producing** in an area you understand, let it write more, and review carefully.

Reem's mistake was staying in producing mode for topics (retries, concurrency) she had never learned. A simple rule: **the first time you use a concept, write it yourself or study it until you could.**

**Speed is not the same as productivity.** METR, an AI research non-profit, published a study in July 2025 in which experienced open-source developers working on their own repositories were, on average, slower with AI tools, though they believed the tools had sped them up. It was one study in one setting, and tools have changed since; but measure your own results rather than trust the feeling of speed.

### 🔴 Expert view

**You are directing a teammate.** Think of an agent as a very fast, widely read colleague who never says "I don't know": it needs clear tasks, context and review. The library teaches these skills in [*System Design for Vibe Coders*, lesson 9.1 — You are the architect now](../vibe/index.en.html#l9-1), [*System Design for Vibe Coders*, lesson 9.2 — Context engineering](../vibe/index.en.html#l9-2), and the [*Running AI Agents in Production* learning path, Level 1 — Builder](../agentic/learning-path.html#level-1-builder). For a junior, they are *evidence*: an agent instruction file, tests written before code and small reviewed commits show you are in charge.

**Where the value moves.** When code is cheap to generate, the scarce skills are deciding what to build, breaking it into checkable pieces, noticing what is wrong, and operating the result (lesson 1.3). Your computer science (complexity, concurrency, networks, databases) is how you spot the agent's mistakes.

**Disclosure that builds trust.** A short, factual note in a README or pull request is enough: which tool you used, for what, and how you verified it. "I used an AI coding agent to scaffold the API routes and draft tests; I wrote the validation rules and test cases myself, reviewed every change, and added the concurrency test after finding a race in the generated code." That sentence is a strength in an interview, not a confession.

**Employer data and tools.** At a bank like Najm, code and data are confidential and regulated, and employers typically approve specific AI tools for specific data. Find out what is approved before you paste anything anywhere; saying so in interviews shows the awareness regulated employers value. The governance view is in [*System Design for Vibe Coders*, lesson 9.8 — The governance glance: you own what your agent ships](../vibe/index.en.html#l9-8).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **AI coding agent** (for example Claude Code, GitHub Copilot, Cursor) | Tools that read a repository, edit files, run commands and iterate on a task | Producing code in areas you understand, under review and tests |
| **Explain-back test** | Explaining a change line by line, out loud or in writing, before committing it | Every agent-written change; always before an interview about your own project |
| **Test-first prompt** | A prompt that fixes the rules and asks for test cases before implementation | Any task where "correct" has edge cases: money, dates, permissions |
| **Diff review checklist** | A short list of what to check in a diff: scope, tests, security, secrets, invented APIs | Reviewing an agent's change, or a flawed pull request in an interview |
| **AI use log** | A running note of where AI helped, what you changed and how you verified it | Writing honest disclosures in READMEs, pull requests and interviews |
| **Secret scanning** (for example gitleaks, platform push protection) | Detects keys and passwords in code before they are pushed | On every repository, especially when agents edit config and fixtures |

## 🏛️ In practice at Najm Bank
After Reem's interview, Khalid and Tariq write the one-page **AI-assisted work rules** every Najm graduate receives on day one. Adapt them as a template.

**Part A: the rules**

| Rule | What it means in practice |
|---|---|
| Use approved tools only | Only the AI tools on the internal list, with the settings it states. No Najm code or customer data goes into anything else. |
| You own every line | Whoever typed it, your name is on the commit. If you cannot explain it, do not commit it. |
| Small, specified tasks | Give the agent tasks you could review in fifteen minutes, with acceptance criteria. |
| Tests are yours | Write or approve the test cases yourself. Any change to an existing test needs a reason in the pull request. |
| Disclose in the pull request | One line: tool, what it did, how you verified it. |
| Learning first | The first time you meet a concept, write it yourself or study it until you could. Your mentor will ask. |

**Part B: the pull request disclosure and verification block** (Reem's, on her first Najm pull request)

```text
AI assistance and verification:
- Tool: approved coding agent (internal list, version as configured).
- Used for: drafting the retry wrapper and its tests.
- I wrote: the retry policy (3 attempts, exponential backoff with jitter,
  only on timeouts and 503s, never on 4xx; every attempt reuses the
  same idempotency key, so a retry cannot pay twice), and the test cases.
- Verified by: unit tests (12, all mine or reviewed line by line);
  a manual run against the sandbox with the payment service stopped;
  secret scan clean.
- I changed from the draft: removed a retry on 400 errors
  (would have resent invalid requests) and a hard-coded timeout.
```

Tariq's comment: "I can see where the agent helped, where you overruled it, and how you know it works."

## 🛠️ Exercises
- 🟢 For three files of a project you built with heavy AI help, do the explain-back test in writing: one or two sentences per function on what it does and why. Mark every gap. *Done when:* the note exists, and every marked gap has either been learned (with a sentence added) or listed as a next study item.
- 🟡 Choose a small feature for one of your projects. Write the test cases first, then use an agent with a test-first prompt to implement it. Review the diff with the checklist from 🟡 Going deeper and record every change you rejected or edited. *Done when:* the feature is merged through a pull request whose description includes an AI-assistance and verification block like Najm's, and at least one rejected or edited change is recorded with the reason.
- 🔴 With a friend, each use an agent to add a small feature to the other's project, then plant one realistic flaw (a missing authorisation check, a weakened test, a date off-by-one, a hard-coded secret). Review each other's pull request cold, in 20 minutes. *Done when:* each of you has written review comments, you compare them with the planted flaw, and you note what you missed and why.

## ⚠️ Mistakes and traps
- **Submitting code you cannot explain.** It is the fastest way to fail a follow-up interview. Do the explain-back test before every commit.
- **Assuming AI rules.** Rules differ by employer and by round. Ask in writing before the assessment and follow the answer.
- **Hiding AI use, or over-apologising for it.** Both damage trust. Disclose briefly and factually, with how you verified.
- **Letting the agent change tests to make them pass.** Treat any test change as a design question that needs a reason.
- **Skipping the learning.** Producing code in a topic you have never studied leaves you hollow there. Write it yourself the first time.

## 🧾 Recap
- Employers check judgement when you use AI tools: specify, review, verify, explain, and be honest.
- You are carried when you cannot explain, change or debug what the agent wrote.
- Work in small, specified tasks, read the whole diff, verify with your own tests and runs, then explain back.
- Know the common agent failures: invented APIs, wrong edge cases, over-broad changes, weakened tests, insecure defaults and confident summaries.
- Always ask about AI rules for each assessment, disclose briefly, and never paste confidential code into unapproved tools.
- Your computer science fundamentals are how you catch the agent's mistakes.

## ✍️ Check yourself

**1. Reem's take-home allowed AI tools, and she disclosed them. Why did the follow-up interview still go badly?**

- A. Using AI on a take-home is always a reason for rejection, even when it is allowed
- B. Her code had no tests, so Tariq could not tell whether any of it worked
- C. She could not explain key parts of her own code, such as the retry logic
- D. She used an AI tool that was not on the employer's list of approved tools

<details><summary>Answer</summary>

**C.** The problem was being carried: the code was more capable than its author. A is wrong: the round allowed AI, and Tariq did not mind it. (🧭 Why it matters.)

</details>

**2. Mohammed is invited to a Sadeem Pay technical interview. The invitation does not mention AI tools. What should he do?**

- A. Ask the recruiter in writing whether AI tools are allowed in each round, and follow the answer
- B. Use AI tools in every round, since the invitation does not forbid them
- C. Avoid mentioning AI entirely, so the question never comes up in the process
- D. Use an AI assistant quietly in a second window during the live round

<details><summary>Answer</summary>

**A.** Rules differ between employers and between rounds, so the rule is to ask, never assume. D is plain dishonesty, and B assumes permission that may not exist. (🟢 The essentials, integrity rules.)

</details>

**3. An agent reports "Fixed the bug, all tests pass". The diff shows it also edited an existing test's expected value. What is the best response?**

- A. Accept it, because the full suite passes and the agent says the bug is fixed
- B. Ask the agent to summarise its change again, in more detail this time
- C. Revert only the test change and merge the rest without running anything
- D. Find out why the expected value changed and run the suite yourself

<details><summary>Answer</summary>

**D.** Weakening tests is a common agent failure; a passing suite means little if the test was bent to match the bug, so treat the edit as suspicious and accept it only with a stated reason. C distrusts the edit but merges unverified. (🟡 Going deeper, what agents commonly get wrong.)

</details>

**4. Huda wants to learn how database transactions work, and needs them for her project. According to this lesson, how should she use her AI tool?**

- A. Let the agent write all the transaction code, since it is faster and she can read it later
- B. Write it herself first, using the tool to explain, quiz her and review her code
- C. Avoid AI tools entirely for the rest of the project, so that she learns everything the hard way
- D. Copy a transaction example from the tool's chat window and adjust it until the tests pass

<details><summary>Answer</summary>

**B.** This is learning mode: the first time you meet a concept, write it yourself or study it until you could, and use the tool as a tutor and reviewer. A and D keep her in producing mode and leave her unable to explain or debug the result. (🟡 Going deeper, learning mode versus producing mode.)

</details>

**5. Which pull request note best shows the honest, useful disclosure this lesson recommends?**

- A. "Written entirely by me, from scratch, over the weekend. Every line is my own work and I am happy to explain any of it."
- B. "An AI agent drafted the routes and tests; I wrote the validation rules, reviewed every change and added a concurrency test for a race I found."
- C. "Sorry, I used AI for most of this. I know it is not ideal and I will try to write more of it myself next time."
- D. "AI-generated with an agent. I have not had time to go through all of it, so please check it carefully before merging."

<details><summary>Answer</summary>

**B.** It says what the agent did, what you did, and how you verified it. D hands verification to the reviewer; A is dishonest if AI helped; C apologises without useful detail. (🔴 Expert view, disclosure that builds trust.)

</details>

## 📚 References
- METR — https://metr.org/ (study on AI tools and experienced open-source developer productivity, July 2025)
- GitHub Docs, GitHub Copilot — https://docs.github.com/en/copilot
- Anthropic documentation (Claude Code) — https://docs.anthropic.com/
- OWASP Top 10 for Large Language Model Applications — https://owasp.org/www-project-top-10-for-large-language-model-applications/
- [*Secure AI & Application Security*, lesson 6.3 — Securing AI-generated code: what coding agents get wrong](../secai/index.html#/6.3)
- [*System Design for Vibe Coders*, lesson 9.4 — Verification before completion](../vibe/index.en.html#l9-4)
- [*Running AI Agents in Production*, learning path, Level 1 — Builder](../agentic/learning-path.html#level-1-builder)

---

# 1.3 — Production thinking: the gap between "it runs on my laptop" and "it runs for users"
*Level: 🟢 Beginner* · *Prerequisites: 1.1, 1.2* · *Step: Learn, Build*

## ⚡ In 60 seconds
- **Production** is where real users and data are. Working on your laptop is one test; production asks more: two users at once, a slow database, hostile input, a restart, a bad release.
- Employers do not expect juniors to design large systems. They do expect you to **ask the production questions**, and to have put something live and kept it working at least once.
- The rule that matters most: **if you cannot see it, roll it back and restore its data, you are not ready to ship it.**
- Decision cue: for every project, ask "Where are config and secrets? How do I know it is broken? How do I undo a bad deploy? What happens to the data?"
- One small project, actually deployed and operated, beats five that only run locally. It is one of the cheapest gaps to close.
- Biggest trap: over-engineering to look senior. Kubernetes for three users shows less judgement than a simple deploy you can explain.

## 🧭 Why it matters
Najm's graduate programme ends its first month with a two-day internal hackathon. Each team must put a small app live on the bank's sandbox platform, and on day two the platform team, led by Salem, runs a "game day": they restart servers, slow the database down and send malformed requests.

Omar's team builds a branch-appointment booker that is flawless on his laptop. On the sandbox it fails within ten minutes. The database address is hard-coded to `localhost`, and its password is committed in the repository. When Salem restarts the server, all bookings vanish: they were stored in memory. Two testers book the last slot at the same moment, and both succeed. A request with a missing field crashes the app with no log, and the team spends an hour guessing. Omar has never deployed anything; nobody ever asked him to.

Yousef's team, with less polished code, does far better. From computer engineering, where field failures are expensive, Yousef asked the dull questions on day one: where does config come from, where are the logs, what happens on restart? Khalid's comment at the debrief: "Writing code that works is the entry ticket. Knowing what can go wrong once it's live is what makes me trust a junior with something real." This lesson gives you those questions.

## 📐 How it works

### 🟢 The essentials

**What changes in production.** On your laptop there is one user (you), friendly input and a fast local database, and if something breaks nobody notices. In production, all of that changes. The library's [*System Design for Vibe Coders*, lesson 0.1 — "It works" is not a property of a system](../vibe/index.en.html#l0-1) makes the case in full. For a junior, the gap comes down to ten questions:

| Question | Production answer (junior level) | Library lesson that builds it |
|---|---|---|
| How is it configured? | From environment variables or config files per environment | [*System Design for Vibe Coders*, lesson 5.7 — Secrets and configuration: the keys to the kingdom](../vibe/index.en.html#l5-7) |
| Where are the secrets? | Never in the repository; in the platform's secret store; a `.env.example` lists names only | [*Secure AI & Application Security*, lesson 5.2 — Secrets management: keys, tokens and where they leak](../secai/index.html#/5.2) |
| Where does data live? | In a real database or storage that survives restarts, with backups you have tested | [*System Design for Vibe Coders*, lesson 2.3 — Backups: what, not just whether](../vibe/index.en.html#l2-3) |
| What if two users act at once? | Database constraints and transactions prevent double bookings and lost updates | [*System Design for Vibe Coders*, lesson 2.6 — Two clicks at once: races, transactions, and idempotent writes](../vibe/index.en.html#l2-6) |
| What if input is bad or hostile? | Validate every input; return clear errors; never build queries from raw strings | [*System Design for Vibe Coders*, lesson 5.4 — Input you didn't realize you were trusting](../vibe/index.en.html#l5-4) |
| How do I know it is broken? | Structured logs, an error tracker and an uptime check tell you before users do | [*System Design for Vibe Coders*, lesson 1.3 — Day-one eyes: your first error tracker and uptime check](../vibe/index.en.html#l1-3) |
| How does it get deployed? | A repeatable, automated deploy from the repository, ideally through CI | [*System Design for Vibe Coders*, lesson 4.1 — Shipping is a system](../vibe/index.en.html#l4-1) |
| How do I undo a bad change? | A rollback to the previous version, practised once | [*System Design for Vibe Coders*, lesson 4.4 — Rollback, staging, and release gates](../vibe/index.en.html#l4-4) |
| Which dependencies does it use? | Pinned in a lock file and scanned for known vulnerabilities | [*System Design for Vibe Coders*, lesson 8.4 — The software you didn't write: dependencies and supply chain](../vibe/index.en.html#l8-4) |
| What does it cost? | You know what you pay for, have a budget alert, and shut down what you do not use | [*System Design for Vibe Coders*, lesson 11.4 — Cost engineering](../vibe/index.en.html#l11-4) |

You do not need deep answers to all ten: know the questions, have a simple answer in your own projects, and know where to learn more.

**The path from laptop to users.** A small but real setup looks like this:

```mermaid
flowchart LR
    L["Laptop: code and tests"] --> G["Git repository"]
    G --> C["CI: tests and checks on every push"]
    C --> S["Staging: a copy of production"]
    S --> P["Production: real users and data"]
    P --> M["Logs, errors and uptime alerts"]
    M -->|"bug found"| L
    P -->|"bad release"| B["Roll back to the previous version"]
```

Each arrow is portfolio evidence: a CI badge, a live URL, an alert you received, a note on the time you rolled back.

**Three tiny code habits that carry a long way.**

```python
# Before: works on Omar's laptop only
DB_URL = "postgresql://omar:secret123@localhost/booker"

# After: configured per environment, secret kept out of the code
import os
DB_URL = os.environ["DATABASE_URL"]  # fails loudly at startup if missing
```

```python
# Before: a missing field crashes the app with no trace
slot = request.json["slot_id"]

# After: validate, return a clear error, and log enough to debug
slot = request.json.get("slot_id")
if slot is None:
    log.warning("booking rejected: missing slot_id", extra={"request_id": req_id})
    return {"error": "slot_id is required"}, 422
```

```python
# A health-check endpoint the platform and uptime checks can call
@app.get("/health")
def health():
    db.execute("SELECT 1")  # proves the database is reachable
    return {"status": "ok"}
```

None of these is advanced. Together they answer three of the ten questions.

### 🟡 Going deeper

**How interviews probe production thinking.** Junior interviews rarely ask for a global system design, but often ask questions like these during a project walk-through:

| Interviewer asks | Weak answer | Strong junior answer |
|---|---|---|
| "How would you deploy this?" | "I'd put it on a server." | "It's a container deployed from the main branch by CI to a managed platform; staging deploys first, and I can roll back to the previous image." |
| "What happens if the database is down?" | "It wouldn't be." | "The health check fails, the platform stops sending traffic, users see an error page, and the uptime alert emails me. I haven't added retries yet; I'd add them with a limit." |
| "How would you know it was broken?" | "Users would tell me." | "Errors go to an error tracker, and an uptime check calls `/health` every few minutes." |
| "Where's the API key?" | "In the config file." | "In the platform's secret store. The repository only has `.env.example` with the variable names." |
| "What would you do differently with a thousand times more users?" | "Use Kubernetes." | "First I'd measure where the time goes. Likely the database queries; I'd add indexes and maybe caching, and only then think about more servers." |

The pattern in the strong answers: specific, honest about what is not done yet, and proportionate. "I haven't added that yet, and here's how I would" is a good answer. Lesson 5.3 covers system design interviews for juniors.

**Production thinking by role.** The ten questions take different forms:
- **Software and AI application engineers:** the list above, plus for AI features: cost per request, evaluations of answer quality, and what happens when the model provider is down. See [*System Design for Vibe Coders*, lesson 6.7 — You are someone's client too: surviving third-party APIs](../vibe/index.en.html#l6-7).
- **Data roles:** Huda learns that a notebook that ran once is not a pipeline. Production means safe reruns without duplicating data, quality checks, alerts when a source changes, and numbers traceable to their source. *Data Engineering & Analytics* builds this, from [Module 2 — Ingestion and pipelines](../data/index.html#/2.1) to [Module 5 — Data science and ML in production](../data/index.html#/5.1).
- **Cloud and platform roles:** for Yousef, production is the product: infrastructure as code, least-privilege access, telemetry everywhere. *Cloud & DevOps* covers it, from [Module 1 — Foundations](../cloud/index.html#/1.1) to [Module 5 — Observability and reliability](../cloud/index.html#/5.1).

**What a production-minded portfolio project shows.** A small project, visibly operated: a live URL, CI on every push, no secrets in history, a `/health` endpoint with an uptime check, an error tracker, a README "Operations" section (deploy, roll back, restore), and one short **postmortem**: a blameless write-up of what went wrong, how you found it and what you changed. Module 3 builds this into your capstone. Small deploys are cheap or free on many platforms at the time of writing (2026); check current terms and set a budget alert first.

### 🔴 Expert view

**Production in a regulated employer.** At a bank like Najm, changes go through **change management** (an approved, recorded process for what goes live and when), production access is restricted and logged, and customer data falls under laws such as Qatar's Personal Data Privacy Protection Law (PDPPL, Law No. 13 of 2016). As a junior you will probably not deploy to production alone for months, and should not want to. Graduates who understand *why* the controls exist settle in faster. Regulated employers across the GCC (banks, government, energy, health) value this; saying in an interview why you would never test with real customer data is worth more than a buzzword.

**You build it, you run it.** Many teams expect builders to help operate their service, including being **on call** (responding to alerts outside working hours on a rota). Juniors usually join after some months, shadowing first. Operating your own small project is the best preparation; the capstone of *System Design for Vibe Coders* (Module 12, "You Get Paged") simulates it.

**Proportion is the senior skill.** Production thinking means matching safeguards to risk, not adding every tool. A personal project needs a repeatable deploy, logs, a health check and a backup; a payment service needs far more. Reaching for microservices, Kubernetes or message queues where they are not needed suggests repeating rather than reasoning. The [*System Design for Vibe Coders*, lesson 0.3 — Build vs buy: the highest-leverage decision you'll make](../vibe/index.en.html#l0-3) shows how to choose.

**AI agents and production.** Agents often miss operational details: hard-coded values, skipped error handling, secrets in fixtures (lesson 1.2). State your production requirements in the task and check them in review.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **The Twelve-Factor App** (Adam Wiggins and contributors) | Widely cited principles for deployable web services: config in the environment, logs as streams, disposable processes | Before your first deploy |
| **Ship-ready checklist** | The ten production questions with evidence for each (Najm's version below) | Before you call any portfolio project "done" |
| **.env.example** | A committed file listing configuration variable names with fake values, never real secrets | Every project that needs configuration |
| **Health-check endpoint** | A simple URL that reports whether the app and its key dependencies are working | Every web service; used by platforms, load balancers and uptime checks |
| **Error tracker** (for example Sentry) | Collects application errors with stack traces and context, and alerts you | From your first deploy; free tiers exist at the time of writing (2026) |
| **Uptime check** | An external service that calls your URL on a schedule and alerts you when it fails | Every deployed project, so you hear about outages before users do |
| **Postmortem** | A blameless write-up of an incident: what happened, impact, cause, what you changed | After any real failure in your project; a strong portfolio item |

## 🏛️ In practice at Najm Bank
After the hackathon, Salem and Khalid turn the game-day failures into the **Najm graduate ship-ready checklist**, used for every graduate project. Here is Omar's booker, two weeks later.

| Question | Evidence required | Omar's evidence | Status |
|---|---|---|
| Configured per environment | Config from environment; environments differ only in config | `DATABASE_URL`, `LOG_LEVEL` from environment | Done |
| No secrets in the repository | Secret scan clean on full history; `.env.example` present | Password rotated and purged from history; scan clean | Done |
| Data survives restarts and is backed up | Real database; a restore tested once | Managed Postgres; daily backup; restore tested into staging on 12 Nov | Done |
| Safe under concurrent use | Constraint or transaction preventing the known race | Unique constraint on slot and date; test with two parallel bookings | Done |
| Inputs validated | Clear 4xx errors for bad input; tests for edge cases | Validation on all three endpoints; 9 tests for bad input | Done |
| Visible when broken | Structured logs, error tracker, uptime check on `/health` | All three in place; logs carry request IDs | Done |
| Repeatable deploy | Deploy from the main branch by CI; staging first | CI runs tests, deploys to staging, manual approval to production | Done |
| Rollback practised | Rolled back once, on purpose, and recorded it | Rolled back a deliberate bad release in 4 minutes; noted in README | Done |
| Dependencies pinned and scanned | Lock file; dependency scan in CI | Both; no high-severity findings | Done |
| Cost known | Monthly cost estimate and a budget alert | Not set up yet | Next: by 20 Nov |

The README's "Operations" section gives exact commands to *Deploy*, *Roll back* and *Restore data*, and links Omar's first postmortem, "Bookings lost on restart". Khalid: "I'd let you show this to any interviewer at Najm."

## 🛠️ Exercises
- 🟢 Take one of your projects and answer the ten production questions for it in a table, honestly, with "not yet" where that is the truth. *Done when:* the table is committed to the repository (for example as `OPERATIONS.md`), and every "not yet" has a one-line plan.
- 🟡 Deploy one small project with config from the environment, no secrets in history, a `/health` endpoint, an uptime check and an error tracker. *Done when:* a friend can open the live URL, you can show the uptime check's history and a test error captured by the error tracker, and a secret scan of the full history is clean.
- 🔴 Run your own game day: restart the app, make the database unreachable, send malformed and concurrent requests, ship a broken release and roll it back. Write a one-page postmortem of the worst failure and fix it. *Done when:* the postmortem is linked from your README, the fix is in a pull request with a test, and the README's "Operations" section lists exact deploy, rollback and restore steps you have actually run.

## ⚠️ Mistakes and traps
- **Calling a project "done" because it runs locally.** It has passed one test of many. Deploy it and answer the ten questions.
- **Secrets in the repository.** Deleting the file is not enough; the secret stays in history. Rotate the secret, clean the history and add secret scanning.
- **No way to see failures.** Without logs, an error tracker and an uptime check, you debug by guessing. Add them on day one.
- **Never practising rollback or restore.** An untested backup or rollback is a hope, not a plan. Do each once, on purpose.
- **Over-engineering to look senior.** Heavy infrastructure for a tiny project signals copying, not judgement. Match safeguards to risk and explain why.
- **Testing with real personal data.** It is a legal and trust problem, especially in regulated sectors. Use synthetic or anonymised data.

## 🧾 Recap
- Production is where real users and data are; laptop success is only the first test.
- Employers expect juniors to ask the production questions: config, secrets, data, concurrency, input, visibility, deploy, rollback, dependencies and cost.
- Small habits (config from the environment, input validation, a health check) answer several questions at once.
- In regulated employers, understanding why change management and data protection exist is a real advantage.
- Proportion is the senior skill: match the safeguards to the risk.

## ✍️ Check yourself

**1. During the game day, Salem restarts the server and all of Omar's bookings disappear. Which production question did Omar's team miss?**

- A. How does it get deployed?
- B. What does it cost?
- C. Which dependencies does it use?
- D. Where does data live, and does it survive restarts?

<details><summary>Answer</summary>

**D.** The bookings lived in memory, so a restart wiped them. A matters too, but no deploy process saves data that only lives in memory. (🟢 The essentials, the ten questions.)

</details>

**2. In an interview, Tariq asks Mohammed: "What happens to your app if the database goes down?" Which answer is strongest for a junior?**

- A. "That won't happen; I use a managed database."
- B. "The health check fails, users see an error page, and my uptime check alerts me. I haven't added retries yet; I'd add a limited retry for timeouts."
- C. "I would migrate to Kubernetes so it can self-heal."
- D. "I would ask a senior engineer."

<details><summary>Answer</summary>

**B.** It is specific, honest about what is not done yet, and proportionate. C reaches for heavy infrastructure that does not address the question; A denies the failure can happen. (🟡 Going deeper, how interviews probe production thinking.)

</details>

**3. Omar discovers the database password was committed to his repository three weeks ago. He deletes the file in a new commit. What else must he do?**

- A. Rotate the password, remove it from the repository history, and add secret scanning
- B. Nothing, because the file is deleted
- C. Make the repository private, which fully solves the problem
- D. Add a comment asking people not to use the old password

<details><summary>Answer</summary>

**A.** The secret stays in Git history and may already be copied, so rotate it, clean history and prevent a repeat. C reduces exposure but does not undo the leak. (⚠️ Mistakes and traps.)

</details>

**4. Huda's model runs well in a notebook. Which change would most move it toward production, from a data role's point of view?**

- A. Add more charts to the notebook
- B. Retrain the model with more features
- C. Turn it into a pipeline that can rerun safely without duplicating data, checks data quality and alerts when a source changes
- D. Share the notebook file with the team by email

<details><summary>Answer</summary>

**C.** For data roles, production means safe reruns, quality checks and alerting. B might improve accuracy, but it leaves the work as a one-off notebook. (🟡 Going deeper, production thinking by role.)

</details>

**5. Reem wants her portfolio project to look senior and plans to add Kubernetes, three microservices and a message queue to an app with a handful of users. What would Khalid most likely advise?**

- A. Keep it simple and proportionate: a repeatable deploy, logs, a health check, backups and a rollback she can explain, and say what she would add at larger scale
- B. Go ahead, because more infrastructure always impresses interviewers
- C. Remove deployment entirely and show only the code
- D. Add the infrastructure but leave it out of the README

<details><summary>Answer</summary>

**A.** Proportion is the senior skill; heavy tools for a tiny problem suggest copying, not judgement. C loses the evidence of production thinking. (🔴 Expert view, proportion.)

</details>

## 📚 References
- The Twelve-Factor App — https://12factor.net/
- Google, Site Reliability Engineering books (free online) — https://sre.google/books/
- OWASP Top 10 — https://owasp.org/www-project-top-ten/
- Sentry documentation — https://docs.sentry.io/
- Al Meezan, Qatar Legal Portal (Law No. 13 of 2016, Personal Data Privacy Protection) — https://www.almeezan.qa/
- [*System Design for Vibe Coders*, lesson 0.1 — "It works" is not a property of a system](../vibe/index.en.html#l0-1)
- [*Cloud & DevOps: Zero to Hero*, Module 5 — Observability and reliability](../cloud/index.html#/5.1)
- [*Data Engineering & Analytics: Zero to Hero*, Module 2 — Ingestion and pipelines](../data/index.html#/2.1)
