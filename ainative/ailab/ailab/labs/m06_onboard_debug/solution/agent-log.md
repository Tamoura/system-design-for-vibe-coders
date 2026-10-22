# Agent log for REMIT-231

| # | Prompt (short) | What the agent did | What I corrected | Time |
|---|---|---|---|---|
| 1 | "Map this repo: entry points, data flow, tests. Cite the file for every claim." | Wrote a map. It named a `risk.py` (copied from docs/ARCHITECTURE.md) and old limits. | Opened the files: `risk.py` does not exist, limits are in `limits.py`. Rewrote those lines. | 25 min |
| 2 | "From these log lines, give three ranked hypotheses for the refusals and what would disprove each." | Ranked: UTC day boundary, rounding, history double counting. | Kept the first; the other two I disproved by reading `check_limits`. | 15 min |
| 3 | "Write a failing test for customer C2207's sequence." | Wrote a test; it passed on the original code. | The first version used the wrong times. I rewrote it from the log (16:42 and 22:18 UTC) and it failed as it should. | 20 min |
| 4 | "Propose the smallest fix. Do not touch tests." | Changed both helpers. | Checked the diff: two lines, one file. | 5 min |

Total about 65 minutes. Without the agent I would have taken longer on the map and on reading `prod.log`; the
agent was wrong on the first map and on the first test, which is why I opened the files.
