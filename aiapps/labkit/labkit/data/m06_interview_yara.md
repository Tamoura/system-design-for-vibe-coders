# Interview transcript: Yara, Service Desk team lead (fictional)

Lab material for lesson 6.1. Najm Bank, its people, its systems and every number below are fictional training data, not facts about a real organisation.

- Round 1, interview 2 of 2 for Najm Desk discovery. Interviewee: **Yara**, Service Desk team lead, the domain expert. Interviewer: **You**, Developer Enablement.
- Wednesday, 45 minutes at Yara's desk with TicketHub open on her screen. Typed up the same day; the words are as close as the notes allow.
- Every turn has an id such as `[Y-07]`. Cite turns by id in your notes.
- Yara and Hind agree on more than they disagree on. Read for the places where they do not.

---

[Y-01] **You:** Thanks, Yara. Could you walk me through the last ticket you handled yourself, from the first message?

[Y-02] **Yara:** This morning. A man in Procurement wrote "my VPN doesn't work". That was the whole message. I asked him four things: which network he was on, what the VPN client says, since when, and which device. Three or four minutes, and I ask the same four on most tickets. If the first message already had them, I would get those minutes back on almost every ticket.

[Y-03] **You:** Where do tickets start?

[Y-04] **Yara:** Phone is the biggest, then the portal, then email. Then there are the ones that never become tickets: people message agents directly on Teams. I would guess two to three hundred a week. We answer, nobody logs it, so it is not in the 1,800.

[Y-05] **You:** Who decides a ticket's category and priority?

[Y-06] **Yara:** We do. The duty agent reads every new ticket, sets the category and priority and assigns it. TicketHub only routes email with exact keywords, and that is it. Hind believes it is automatic. It was meant to be, years ago.

[Y-07] **You:** How does the duty agent choose a priority?

[Y-08] **Yara:** The policy says P1 is a service down for many staff, but "many" is a judgement. If three people on one floor report the same VPN fault within ten minutes, I make it P1. An assistant looking at one message cannot see that. So it can suggest a priority, never set one.

[Y-09] **You:** Tell me about the last password problem you remember.

[Y-10] **Yara:** Last Sunday. A woman got a new phone over the weekend and her authenticator was still on the old one, so she could not reset anything. When the authenticator is lost, the policy says we verify her identity by calling her manager, on the number in PeopleCore, never a number she gives us. Managers do not answer at seven in the morning; it takes twenty minutes or two hours. The call-back is the bottleneck, not the unlock.

[Y-11] **You:** What if the manager's details are wrong?

[Y-12] **Yara:** It happens. After reorganisations the manager field in PeopleCore is wrong for roughly one person in ten, so we ask people to confirm who their manager is. Contractors have no manager in PeopleCore at all. They are guests in Najm ID with a sponsor, and the sponsor gets the call.

[Y-13] **You:** How many of the access tickets are plain forgotten passwords?

[Y-14] **Yara:** Fewer than people think, because self-service handles most of them. It is phones: a new phone, a lost phone, an authenticator nobody transferred. Then lockouts. Access is about a quarter of our tickets, not half. If you want real numbers, ask for the export; do not trust the dashboard average.

[Y-15] **You:** What do staff ask that is not about their own accounts?

[Y-16] **Yara:** "How do I" questions, about a quarter of all tickets. I read forty last week. Twenty-two were fully answered by a policy page. Ten were half answered: the policy says who approves but not where to click. Eight were in no document, like how to connect to the printer on floor 4. And agents answered fourteen of the forty with one of our ten macros.

[Y-17] **You:** What are the macros, and what else do agents use?

[Y-18] **Yara:** Saved replies in TicketHub, plus my own cheat sheet. It is a Word file, nothing official, and some of it is out of date: it still says laptops are refreshed every three years.

[Y-19] **You:** Is the policy library up to date?

[Y-20] **Yara:** Mostly. The trouble is notices. When the VPN client moved to version 6 in March, that went out as a notice and the VPN page never changed. The old password PDF on the intranet still says twelve characters, and people find it through search; it is fourteen now. And DeviceDesk still flags a laptop for refresh at three years, because nobody updated that report.

[Y-21] **You:** Which language do people write in?

[Y-22] **Yara:** Roughly a third in Arabic, more from the branches, and many mix them: an Arabic sentence with English product names or a ticket number. Tickets and categories in TicketHub are English. I read both languages, but our reports are in English. So when an assistant drafts a ticket, I want it in English for us, with the person's own words kept next to it.

[Y-23] **You:** What worries you most about an assistant on the desk?

[Y-24] **Yara:** Three things. One: people paste secrets into tickets. A couple of times a month somebody types a password into a description. Two: some tickets are restricted, meaning security incidents, HR matters and the executive office. Agents see them; the requester sees only "In progress". If an assistant reads out a security ticket I will be called into Hamad's office. Three: phishing. The policy says report it, never forward it, and if you clicked, call the hotline. People still forward it to us and write "I think I clicked". That is not a ticket. That is a phone call to Security Operations.

[Y-25] **You:** What happens outside opening hours?

[Y-26] **Yara:** We are closed Friday and Saturday, and outside 07:00 to 17:00 Sunday to Thursday only P1 goes to the on-call number. If a bot opens a ticket at ten at night and says "someone will be in touch", people expect someone. They will be furious on Sunday. And Sunday 07:00 to 10:00 is our peak: about a seventh of the week lands in those three hours.

[Y-27] **You:** What would make you trust a new assistant?

[Y-28] **Yara:** When it says "I don't know" and hands me the case with everything I need. Do not count a handover as a failure. A good handover saves half my work. And a wrong answer costs me more than no answer.

[Y-29] **You:** Is there anything about how your staff or users work that could matter?

[Y-30] **Yara:** Two people on my team and a few in the branches use screen readers, and the old intranet chat could not be used with the keyboard. Also satisfaction: the survey goes out when a ticket closes and about one person in eight answers. If you promise satisfaction, tell me how you will measure it.

[Y-31] **You:** One last thing. How would you count a ticket as deflected?

[Y-32] **Yara:** We do not count it today. If somebody gives up and calls two days later, that is the same problem twice. I would count it only if they do not come back about the same thing within three working days.
