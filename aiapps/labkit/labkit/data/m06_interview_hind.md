# Interview transcript: Hind, Head of IT Service Desk (fictional)

Lab material for lesson 6.1. Najm Bank, its people, its systems and every number below are fictional training data, not facts about a real organisation.

- Round 1, interview 1 of 2 for Najm Desk discovery. Interviewee: **Hind**, Head of IT Service Desk, the sponsor. Interviewer: **You**, Developer Enablement.
- Sunday, 35 minutes, in Hind's office. Typed up within the hour from notes; the words are as close as the notes allow.
- Every turn has an id such as `[H-07]`. Cite turns by id in your notes (`labs/m06/check_notes.py` checks that your quotes are real).
- This transcript is imperfect on purpose. Interviewers make mistakes, and sponsors say things that other sources will contradict.

---

[H-01] **You:** Thanks for making the time. Before I say anything about solutions, can you take me through the last time the desk was really under pressure?

[H-02] **Hind:** That's easy, the Sunday after the long holiday. Fourteen agents, and by nine o'clock we had well over two hundred tickets waiting. Half of them were passwords and access. People come back from a break and nothing works. The board watches one number, median first response, and last quarter it was three hours forty minutes. I want that number to fall off a cliff.

[H-03] **You:** If we built an assistant on your policy library that resolved most of those tickets on its own, wouldn't that be great?

[H-04] **Hind:** Seventy percent. That's the number I gave the steering group. If it gets there in three months, I'm a hero.

[H-05] **You:** Tell me about the last time staff asked something the desk could not answer quickly.

[H-06] **Hind:** The VPN change in March. Everybody asked the same two things: which client version, and where to get it. A notice went out, but people don't read notices. Fourteen agents typed the same answer over and over. The answers exist, nobody finds them. The policy library is current, by the way; Legal reviews it every quarter.

[H-07] **You:** What did the desk do about questions like that before?

[H-08] **Hind:** We tried a chatbot in 2022, a vendor FAQ bot. It answered with links to the intranet and there was no way to reach a person. Staff hated it and we switched it off after four months. Whatever we build must always let people reach a human. And it must never say anything wrong. I would rather it said nothing than said something wrong.

[H-09] **You:** When you say wrong, what is the worst thing you can picture it saying?

[H-10] **Hind:** Telling someone they may do something the policy forbids. Last year an agent told a manager that a contractor could have the same laptop as an employee. It became an audit comment. Policy mistakes keep me awake, not typos.

[H-11] **You:** How are password and account problems solved today?

[H-12] **Hind:** Any agent can unlock an account in Najm ID. It takes a minute. I want the assistant to do that by itself, no human, so people stop waiting for us.

[H-13] **You:** Does anything slow that down?

[H-14] **Hind:** Not really. Well, there is a verification step when somebody has lost their phone, but that is quick.

[H-15] **You:** Who uses the desk, and how do they reach you?

[H-16] **Hind:** Staff, through the portal. Everything is a ticket in TicketHub and tickets are routed automatically by category, so nobody triages by hand. Ninety percent of our users write in English; Arabic is a nice-to-have for later.

[H-17] **You:** So English first, then Arabic later?

[H-18] **Hind:** Yes, exactly.

[H-19] **You:** And you think staff would use a chat assistant in the portal?

[H-20] **Hind:** Absolutely. Everybody is on chat these days.

[H-21] **You:** Do contractors use the desk?

[H-22] **Hind:** A few. The same rules apply, I would think. I haven't looked into it.

[H-23] **You:** What would you like the assistant to know about each person who writes in?

[H-24] **Hind:** As much as it can. Their tickets, their laptop from DeviceDesk, their manager from PeopleCore, so it can say "your laptop is due for refresh". I want it to feel like it knows them.

[H-25] **You:** How will you know it worked?

[H-26] **Hind:** Deflection. If they don't open a ticket, it worked. Plus first response time and staff satisfaction. Hand-offs are failures, so fewer is better. And cost: Finance approved the pilot from this year's budget, but I need a case for next year's running costs.

[H-27] **You:** What about outside the desk's hours?

[H-28] **Hind:** That's the best part: twenty-four hours a day, seven days a week. Our colleagues in the EU office work on Fridays when we're closed. They will love it.

[H-29] **You:** Who else must agree before this goes live?

[H-30] **Hind:** Layla's committee, Hamad's team for anything near Najm ID, and Sara will want to know where the chats are stored. The committee sits every second Tuesday, so allow a month for each review. I would like the pilot to start before the end of next month.

[H-31] **You:** Is there anything I haven't asked that I should have?

[H-32] **Hind:** Talk to Yara before you design anything. She knows how it really works. I know how it looks on the dashboard.
