# Review of agent/loyalty-discount

## Verdict

request changes

## What I ran

- `git log --oneline main..agent/loyalty-discount` and `git diff main...agent/loyalty-discount --stat`: 4 commits, 6 files, +112 -34. The last commit is called "refactor" but it changes how `fees.py` prices an express transfer and it deletes a test.
- `pytest -q` on the branch: 105 passed. The suite is green, so green is not the question; the question is what the suite can see.
- The deleted test, taken from `main` and run against the branch: `test_express_surcharge_is_added_after_the_cap` fails (150.00 instead of 165.00).
- REMIT-229's rounding rule worked by hand on QAR 192.50 (silver): base fee 5.85, discount 0.585 rounds half up to 0.59, so silver pays 5.26. The branch charges 5.27.
- Searched the repository and `docs/najmkit.md` for `najm-loyalty`: it is nowhere, and the ticket does not ask for it.
- Read the description against the diff: "No behaviour changes outside the loyalty discount" is not true.

## Findings

### 1. A dependency nobody asked for, and nobody can vouch for
- **File:** pyproject.toml
- **Line:** 11
- **Severity:** blocker
- **Problem:** `dependencies` went from `[]` to `["najm-loyalty>=2.1"]`, and `src/remit/loyalty.py:10` imports it. The package is not in the ticket, not in `docs/najmkit.md` and not in the repository: it looks invented. CONTRIBUTING.md says standard library only, no dependency without a ticket and a second reviewer. A made-up package name is exactly what someone can register and fill with their own code. The `try/except ImportError` hides it: tests pass without the package, so the line stays unnoticed.
- **Fix:** put `dependencies = []` back, delete the import and the client branch, and keep the rate table in the repository.

### 2. An API key in the source
- **File:** src/remit/loyalty.py
- **Line:** 14
- **Severity:** blocker
- **Problem:** `LOYALTY_API_KEY` holds what looks like a live key in a string. CONTRIBUTING.md: no secrets in code, settings come from environment variables. Once it is committed it is in the history of the repository and of every clone, so removing the line is not enough: the key has to be rotated.
- **Fix:** delete it (nothing needs it once finding 1 is fixed), rotate the key with whoever owns it, and tell Noura.

### 3. The discount is computed with floats
- **File:** src/remit/fees.py
- **Line:** 117
- **Severity:** blocker
- **Problem:** `round(float(base.amount) * rate, 2)` and the float rates in `loyalty.py:16` break "money is Decimal, rounded half up". Where the discount is exactly half a cent the float lands on the wrong side: QAR 192.50, silver, base fee 5.85, discount 0.585: the branch charges 5.27, the ticket says 5.26. The ticket's own examples pass because they avoid the tie.
- **Fix:** `Decimal` rates and `Money * Decimal` (rounds half up), then `base - discount`, floored at the minimum.

### 4. `except Exception` turns every error into the full price
- **File:** src/remit/fees.py
- **Line:** 119
- **Severity:** major
- **Problem:** `_apply_discount` catches everything and returns the undiscounted fee. An unknown tier ("Gold" with a capital, "platinum") raises a `KeyError` that is swallowed, so the customer silently pays full price. Rule 5 of the ticket says an unknown tier must be an error. The same handler would also hide any bug in the code above it, which is how the float problem could survive.
- **Fix:** no handler. Let an unknown tier raise `ValueError` with a clear message.

### 5. Scope creep: the express surcharge now sits under the cap
- **File:** src/remit/fees.py
- **Line:** 145
- **Severity:** blocker
- **Problem:** `total=min(base + surcharge, cap)` is a price change nobody asked for (rule 6: nothing else about fees changes). A QAR 20,000 express transfer on STD-A now costs 150.00 instead of 165.00, and `FeeBreakdown.total` no longer equals `base + surcharge`. The commit calls it a "refactor", and the docstrings were rewritten to match. The same commit renames `_D` to `_dec` on about twenty lines, which makes the real change harder to see. This is money logic.
- **Fix:** revert the cap change, its docstrings and the rename. If the cap should include the surcharge, that is its own ticket and Hessa's decision.

### 6. A test was deleted to make the change pass
- **File:** tests/test_fees.py
- **Line:** -
- **Severity:** major
- **Problem:** `test_express_surcharge_is_added_after_the_cap` (it stood just above `test_the_fee_is_rounded_half_up_once`) is gone. It was the one test that said the scope creep in finding 5 was wrong. The description calls it "a test that no longer matched"; it matched the behaviour that was supposed to stay.
- **Fix:** restore it, unchanged.

### 7. A test that asserts nothing
- **File:** tests/test_loyalty.py
- **Line:** 30
- **Severity:** minor
- **Problem:** `test_gold_gets_twenty_percent_off_the_fee` computes the fee and prints it. It has no `assert`, so it passes whatever gold customers are charged. The ticket's gold example (16.00) is not checked anywhere.
- **Fix:** `assert quote_fee(qar("1000"), INR, loyalty_tier="gold") == qar("16.00")`.

### 8. A test that mocks the code it is testing
- **File:** tests/test_loyalty.py
- **Line:** 23
- **Severity:** minor
- **Problem:** `test_silver_gets_ten_percent_off_the_fee` patches `_apply_discount` to return 18.00 and then asserts 18.00. It tests the mock. Delete the discount code and it still passes.
- **Fix:** call the real code and assert the ticket's numbers, including the half-cent case.

### 9. The description says things the diff does not
- **File:** lab-assets/pull-request.md
- **Line:** 31
- **Severity:** minor
- **Problem:** "No behaviour changes outside the loyalty discount" and "removed one test that no longer matched" are the two sentences that hide findings 5 and 6. A description is a claim, not evidence.
- **Fix:** ask the author to correct it, and to say what was checked rather than that it was checked.

## What is good

- `RemitService.send` and `quote` pass the customer's own tier correctly, and the minimum-fee floor and the "express is not discounted" rule are right.
- The commits are small and follow CONTRIBUTING.md, and the service tests (`send`, `quote`) assert real numbers.
- The failure modes are the usual ones for agent-written code, which makes them quick to find once you read the diff against the ticket instead of the summary.
