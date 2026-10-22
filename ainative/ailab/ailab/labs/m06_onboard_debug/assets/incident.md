# INC-0317: customers refused "daily limit" in the middle of the night

*Constructed for teaching: a fictional incident at the fictional Najm Bank, written for this lab.
Nothing here is a real customer, a real log or a real company record.*

**Raised by:** Maha, SRE lead  
**Date:** Tuesday 17 March 2026  
**Severity:** medium (customer-facing; the code involved is money logic)  
**Owner:** Payments Platform (you)  
**Status:** open

## What support reported

Between Saturday 14 and Tuesday 17 March, six customers wrote to support with almost the same
message. One of them, paraphrased:

> "I sent money yesterday evening. It is a new day now and the app says I would go over my daily
> limit. I waited a few hours, tried again, and then it worked."

Three of the six are named in the support tickets: `C2207`, `C1190` and `C3042`. All three are
KYC tier T1. All six customers live in Qatar.

## What I know

- The refusal is the normal one: `transfer.rejected` with reason `limit_exceeded`.
- I pulled the audit trail for Friday 13 March 06:00 UTC to Tuesday 17 March 04:00 UTC. It is in
  `prod.log` next to this file: 56 lines, one JSON object per line, written by `najmkit.audit`.
  **Every timestamp in it is UTC.** Customer ids are pseudonymous. The audit trail holds
  identifiers, amounts and times only (the house rule is "log identifiers, never names"), and I
  added nothing to it.
- The tier of every customer in the extract is in `kyc_tiers.csv`. The limits are in the code
  (`src/remit/limits.py`), not in my head: check them there.
- No configuration changed this week. Release r-0312 went out on Thursday 12 March. I have not
  read what was in it beyond "CI was green".

## What I do not know

- Whether the six customers are the only ones affected.
- Whether the problem is only refusals, or whether something is also being let through.
- Whether only the daily limit is involved.
- Whether it is the same for every KYC tier.

## Ground rules

- **No production access** from your laptop or from your AI tool. Work only from the files in
  this folder and the repository. If a tool asks for more, the answer is no.
- Customer ids are pseudonymous, but treat the extract as internal data: use only tools your team
  has approved, and do not paste it anywhere else.
- Money logic needs a second human reviewer before it ships (CONTRIBUTING.md). Make the change
  small enough that a reviewer can check it in five minutes.
- I want a root-cause note I can paste into the incident record, not a patch and a shrug.
