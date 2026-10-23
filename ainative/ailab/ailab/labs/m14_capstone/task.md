# REMIT-414: open the Bangladesh (BDT) corridor, and show your working

**From:** Hessa, Product Owner, Najm Remit
**Priority:** High. Marketing has announced Bangladesh for the end of the quarter.

Treasury has agreed these numbers. Everything here is fictional, like the rest of Remit.

### The corridor

| | |
|---|---|
| Code | `QAR-BDT` (send QAR, receive BDT) |
| Per transfer | QAR 100.00 to QAR 12,000.00, both inclusive |
| Delivery | `bank_deposit` (the default) and `wallet`; no `cash_pickup` |
| Mid-market rate | 1 QAR = 33.46 BDT |
| Margin | 0.0175, taken off the mid rate like every corridor |
| Fees | a schedule of its own, `STD-C`, below |

`STD-C` works like the others: the whole amount picks the tier, the upper bound is included, the minimum and the cap apply, and the express surcharge comes after the cap.

| Amount up to (QAR) | Percent | Flat (QAR) |
|---:|---:|---:|
| 1,000.00 | 2.20% | 3.50 |
| 5,000.00 | 1.60% | 12.00 |
| no limit | 1.10% | 45.00 |

Minimum fee QAR 7.00, cap QAR 130.00, express surcharge QAR 18.00. The KYC tiers' daily and monthly limits do not change and apply here too: by "limits" above I mean only the minimum and maximum per transfer.

### What the customer reads

A new template, `transfer_sent_bdt`, goes out for `QAR-BDT` transfers; every other corridor keeps `transfer_sent`. Customer Care approved this wording, so do not rephrase it. Values: `name`, `transfer_id`, `recipient`, `receive_amount`, `send_amount`, `fee`, `rate` (the customer rate).

    en: Hi {name}, your transfer {transfer_id} to Bangladesh was sent. {recipient} received {receive_amount} at a rate of 1 QAR = {rate} BDT. You paid {send_amount} plus a fee of {fee}. Please keep this message as your receipt.
    ar: مرحباً {name}، تم إرسال تحويلك {transfer_id} إلى بنغلاديش. تم استلام مبلغ {receive_amount} من قبل {recipient} بسعر صرف ١ ريال قطري مقابل {rate} تاكا. المبلغ المرسل: {send_amount}، والرسوم: {fee}. يرجى الاحتفاظ بهذه الرسالة كإيصال لك.

### How I want it delivered

The change, and the evidence around it. `lab-assets/hessa-notes.md` has my meeting notes, `lab-assets/templates/` a starting point for each document and `lab-assets/README.md` what the grader reads in each one. Use an agent as much as you like; you answer for every line.

- the change in `src/remit/` (`corridors.py`, `fees.py`, `fx.py`, `notify.py`, `service.py`), added to the tables that are already there, and new `tests/test_*.py` files; each acceptance criterion of your spec is named in a test (`AC1`, `AC2`...)
- `CLAUDE.md` (or `AGENTS.md`), updated for corridor work: start from your lesson 2.2 file or `templates/memory.md`
- `specs/REMIT-414.md`, then `specs/REMIT-414-plan.md`: one row per step, the last column that step's commit header
- `docs/adr/0001-<short-title>.md`: one decision
- `docs/review-REMIT-414.md`: your own diff, `AI-assisted: yes` or `no`, the money files needing a second human
- `.claude/settings.json` and `.claude/hooks/guard.py`
- `docs/corridors.md` (new) and the lines of `docs/ARCHITECTURE.md` this change makes untrue
- `docs/agent-log.md`, then `docs/retrospective.md`

`CONTRIBUTING.md` applies (its scopes are examples: `claude` and `specs` are fine). One kind of change per commit: code with its tests (`src/`, `tests/`), or documents (`docs/`, `specs/`), or agent configuration (`CLAUDE.md`, `.claude/`). At least eight commits. Do not edit an existing test, add a dependency or touch files the change does not need; keep scratch scripts outside the repository. Where this ticket is silent, decide, write the decision in your spec and say who confirms it.

Done when every required check of `python -m ailab grade m14 --dir <this directory>` passes (run it from the `ailab` folder of the course repository, on the branch with your commits). It checks the result and how the documents refer to each other, not whether your thinking was good.
