# Agent log

One entry per session with an agent, in the format of lesson 0.1. If you used no agent this week, write
"no agent used" and say why.

Entry: 2026-03-02, ONB-101, part 2 (read-only session on the fee module)
Prompt (paste or summarise): explain how the fee for a transfer is calculated, starting from src/remit/service.py, and propose one change to make the fee module easier to understand, without applying it
What the agent did: read service.py, fees.py, corridors.py and test_fees.py; explained the tiers, the minimum, the cap and the express surcharge; proposed a worked-example table in the fees.py docstring
What I corrected: its claim that rounding happens at the end; the code rounds once, when the Money is built
What I checked myself: the claim about rounding against fees.py and test_fees.py, and that git status was clean afterwards
Minutes: agent 6 · reading and checking its claims 14
Would I delegate it again? Yes for reading and explaining, with a request to quote the line behind each claim
