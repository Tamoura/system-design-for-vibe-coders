# REMIT-231 root cause: the limits' day and month began at UTC midnight, not Qatar midnight

## Summary

Since release r-0312 (12 March 2026) the daily and monthly sending limits have used UTC calendar days and months
instead of Qatar ones. Customers were refused for up to three hours after Qatar midnight, and a few were let
through over their limit in the same hours. The fix restores the Qatar conversion in two places.

## Symptom

Six customers wrote to support: a new day had started, the app still said they were over their daily limit, and
a retry a few hours later worked. In `prod.log` the wrongful refusals are `transfer.rejected` events with
`limit_exceeded` between 21:00 and 24:00 UTC, which is midnight to 03:00 in Qatar.

## Reproduction

`pytest -q tests/test_limits_qatar_midnight.py`. The first test, `test_c2207_is_not_refused_just_after_qatar_midnight`,
replays customer C2207 from the log: 1,200 sent at 16:42 UTC, then 1,000 attempted at 22:18 UTC. It failed on the
code as released and passes now. The suite had been green all along because the four tests that pinned Qatar
midnight were deleted in the same commit that broke it, so the first step was a failing test, not a code search.

## Root cause

In `src/remit/limits.py`, `day_window` and `month_window` each began with `local = to_local(now)`. A refactor
(commit "simplify the window helpers and their tests") replaced both with `now.astimezone(timezone.utc)`. So the
windows started at 00:00 UTC, which is 03:00 in Qatar, while the module's own docstring says a day is a Qatar
calendar day (UTC+3, no daylight saving). Timestamps are stored in UTC and must be converted before deciding which
window they fall into; the helpers stopped converting. A transfer made after Qatar midnight but before UTC midnight
was counted in the previous day, and the new day began three hours late.

## Why it was missed

The same commit deleted `test_the_day_ends_at_midnight_in_qatar_not_in_utc`, `test_a_transfer_after_qatar_midnight_but_before_utc_midnight_belongs_to_the_new_day`,
`test_the_month_changes_at_midnight_in_qatar` and `test_windows_are_local_calendar_windows`, so CI stayed green. The
commit message did not say that any behaviour changed, and `limits.py` is money logic that needs a second reviewer.
The decoy: the commit before it, a refactor of `month_window`, looks suspicious but changes no behaviour.

## Fix

Two lines in `src/remit/limits.py`: both helpers use `to_local(now)` again. Nothing else in `src` changed, and no
existing test was edited. The new file `tests/test_limits_qatar_midnight.py` is the regression test: it covers the
day and month boundaries on both sides, plus the replay of C2207.

## Impact

Wrongly refused (the log shows `transfer.rejected` but the customer had a new Qatar day): C1190, C2207, C3042,
C4410, C5521 and C6003. Wrongly let through (the log shows `transfer.sent` but the Qatar day's limit was
already used): C7788 (1,300 QAR over the T1 daily limit of 2,000) and C8120 (1,200 over). Customers C9001, C9002, C9005
and C9006 were refused correctly in both models. The monthly limit was affected in the same way, but the extract
covers no month boundary, so I found no case.

## Prevention

Restore the deleted tests as part of the fix (done, in new form). Reviewers should treat a commit that changes
`limits.py` and deletes tests together as a flag, and ask for the behaviour change in words. Compliance should be
told about C7788 and C8120 because they exceeded a daily limit.

## Open questions

- I did not verify what happened to the customers' notifications after a wrongful refusal.
- The extract ends at 04:00 UTC on 17 March; I cannot say how many customers were affected after that.
