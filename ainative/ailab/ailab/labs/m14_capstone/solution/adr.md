# 1. Bangladesh gets its own fee schedule, STD-C

### Status
Accepted, 2 March 2026, with Hessa and Tariq.

### Context
REMIT-414 opens the `QAR-BDT` corridor. Remit has two schedules in `fees.SCHEDULES`: `STD-A` for India and the Philippines, `STD-B` for Egypt and Pakistan. Pointing Bangladesh at `STD-B` would need no new code (Lujain's suggestion in the planning meeting). Treasury wants a different price curve from `STD-B`: lower for everyday amounts (at QAR 500 `STD-B` charges 15.50 and the agreed `STD-C` charges 14.50) and a higher minimum fee (7.00 against 6.00). A corridor names its schedule in `Corridor.fee_schedule` in `src/remit/corridors.py`, so the choice is one string per corridor.

### Decision
We add a third schedule, `STD-C`, with three tiers, a minimum of 7.00, a cap of 130.00 and an express surcharge of 18.00, and we give it to `QAR-BDT` only. `STD-A` and `STD-B` do not change.

### Consequences
Bangladesh can be repriced without touching any other corridor, and the numbers Treasury agreed are in one place. The cost is a third table to keep right: three schedules in `fees.py` that can drift apart, and a page `docs/corridors.md` that must list all of them. If a fourth corridor wants slightly different numbers we will be tempted to add `STD-D`; the answer is to ask whether tiers should become data outside the code, which is a different decision. If Treasury later wants one schedule for all corridors, merging means a fee change for customers, not just a refactor.
