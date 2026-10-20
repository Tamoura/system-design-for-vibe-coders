# As-is process: how a ticket really moves through the Service Desk (fictional)

Lab material for lesson 6.1. Najm Bank, its people, its systems and every number below are fictional training data, not facts about a real organisation.

- Shadowing notes by **Lujain** (graduate engineer, Developer Enablement) and **You**: Sunday 07:00 to 11:00 and Wednesday 08:00 to 11:00, sitting beside agents on the Service Desk floor.
- Counts and shares are four-week averages from a TicketHub export that Yara ran for us, unless a line says otherwise. Observations are ours, with a stopwatch and small samples, so treat them as leads, not statistics.
- Every line has an id such as `[A-04]` for your notes to cite.

---

## Where tickets come from

[A-01] Logged tickets arrive by phone (38%), the portal (31%), email (24%) and walk-up (7%). About 1,800 a week in total.

[A-02] Not in those counts: staff send direct messages on Teams to agents they know. We saw 11 in the seven hours we sat there. Yara's own estimate is 200 to 300 a week. The agent answers; nobody logs a ticket.

## What the tickets are about (logged tickets per week)

[A-03] Policy and "how do I" questions 450; access, password and MFA 450; hardware 330; software 240; network 200; security 70; other 60. Total 1,800.

[A-04] Inside the 450 access tickets: lost or changed authenticator (new phone) about 200; account locked after failed attempts about 110; password reset where self-service failed about 60; new access or permission requests about 80.

[A-05] Yara read a sample of 40 "how do I" tickets. 22 were fully answered by a policy document, 10 were partly answered (the policy says who approves but not where to click), and 8 were in no document at all. Agents answered 14 of the 40 with one of ten saved macros.

## The steps, as we watched them

[A-06] **Intake.** The portal and email create a TicketHub ticket. Phone calls are typed in by the agent who picks up. TicketHub routes email by exact keyword only; every other ticket lands in one shared queue.

[A-07] **Triage.** One duty agent per shift reads every new ticket, sets the category and priority and assigns it. About 4 minutes a ticket. Nothing is routed by category automatically.

[A-08] **Clarify.** On Wednesday we followed 14 tickets. 11 needed at least one round trip to get missing information: which device, which network, the exact error text, since when. Each round trip cost the agent 3 to 4 minutes and the requester a wait.

[A-09] **Resolve.** Agents work from the intranet policy pages, ten saved macros, Yara's own Word cheat sheet and the old password-policy PDF. Several agents corrected the PDF by hand because it still says passwords need 12 characters.

[A-10] **Verify identity (access tickets).** When the authenticator is lost, the agent phones the requester's manager, using the number in PeopleCore, before touching Najm ID. We watched one call-back take 35 minutes because the manager did not answer. Yara says 20 minutes to 2 hours is normal. The agent works other tickets while waiting.

[A-11] **Approve (requests).** New laptops need the line manager's approval; software outside the catalogue needs Information Security and a licence owner. The agent chases these by email.

[A-12] **Close and survey.** TicketHub sends a satisfaction survey when a ticket closes. About 1 requester in 8 answers; the average among those who do is 4.2 out of 5. About 8% of tickets are reopened.

## Facts about the data and the clock

[A-13] TicketHub stops the "first response" clock at the first comment by an agent. That comment is often the triage note "looking into this". The 3 hours 40 minutes median therefore includes notes that tell the requester nothing. No one measures a "first useful response".

[A-14] Sunday 07:00 to 10:00 brings about a seventh of the week's tickets, because people return from the weekend with new phones and forgotten passwords. About 200 are waiting at 10:00.

[A-15] Stopwatch timings per ticket: macro answer 3 to 5 minutes; written answer 8 to 10 minutes; account lockout 5 to 8 minutes; authenticator re-enrolment about 15 minutes of agent time plus the call-back wait.

[A-16] Of 200 recent portal and email tickets we read, 47 were written in Arabic and 21 mixed Arabic and English. TicketHub's category field and all reports are in English.

[A-17] TicketHub has a "restricted" flag for security incidents, HR matters and the executive office. About 3% of tickets carry it. The requester sees only "In progress"; agents see everything.

[A-18] About 1 requester in 20 is a contractor. Contractors are guests in Najm ID and have no PeopleCore record; a named sponsor stands in for the manager.

[A-19] On Sunday an agent found a password typed into a ticket description and edited it out by hand. Yara says it happens a couple of times a month.

[A-20] An agent switches between five tools on a typical access ticket: TicketHub, the Najm ID admin console, PeopleCore (read only), DeviceDesk (read only) and the intranet.

## Outside the desk's hours

[A-21] The desk is open Sunday to Thursday, 07:00 to 17:00 Qatar time. Outside those hours only P1 incidents are handled, through the on-call number. Friday and Saturday are closed. Staff in the EU office work Monday to Friday.

[A-22] A suspected phishing click is not a ticket. The policy says to call the Security Operations hotline at once; the device is isolated until it is checked. Staff still forward phishing emails to the desk.
