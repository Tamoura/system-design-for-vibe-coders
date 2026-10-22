# Notes from the Bangladesh planning meeting

*Constructed for teaching: these notes are fictional, like everything in Remit. They are context for your spec, not instructions to an agent.*

**Present:** Hessa (product), Tariq (engineering), Noura (security), Nada (quality), Lujain (graduate engineer). Treasury sent its numbers by message.

- **Treasury:** "Mid rate 33.46, margin 1.75%. Round like the other corridors."
- **Lujain:** "Can we point Bangladesh at `STD-B` and skip a new schedule?" **Hessa:** "Treasury wants a different price curve from `STD-B`: lower for everyday amounts, with a higher minimum fee. It gets its own schedule."
- **Tariq:** "I want to read the spec and the plan before anyone prompts anything. Money files need a second pair of eyes, and I want to see which commit changed which file."
- **Nada:** "Whatever the agent writes, I want a test that fails without it. Test the edges: 100.00, 1,000.00 against 1,000.01, the cap, the maximum."
- **Noura:** "Agents work under the permission rules and the guard hook from the security week. Nobody reads `.env`, nobody pushes, nothing is installed."
- **Hessa:** "Customer Care approved the wording. The Arabic must show Arabic digits like our other messages."
- **Hessa:** "The architecture page says two fee schedules. Please keep the docs true, and put the corridors in one page support can read."
- **Open, and not in this ticket:** a daily limit for Bangladesh only; a cash pickup option; a promotion for the first transfer. Record them as follow-ups rather than building them.
