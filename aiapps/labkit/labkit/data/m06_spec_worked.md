# Najm Desk v1 specification, v0.1 (fictional worked example)

Owner: you. Customer: Hind. Domain: Yara. Risk reviewers: Layla, Noura, Sara. Status: unsigned.

### 1. Purpose
Cut the wait for answers to common IT questions and give agents complete tickets, without letting an assistant decide what policy reserves for a person.

### 2. Users and scenarios
Staff and contractors (a sponsor replaces the manager) ask policy questions, check tickets, report problems, request unlocks. Desk agents (pilot, copilot mode) get drafts and hand-offs. Arabic, English, mixed. Peak: Sunday 07:00 to 10:00.

### 3. Scope
In: policy answers, ticket status, draft and creation, unlock request, hand-off. Out: setting priority, changing accounts, approving anything, refresh advice, incident detection, voice.

### 4. Tools, data and permissions
Autonomy: **S** suggest, **D** draft, **A** a person approves first, **X** acts alone.

| Tool | Staff, contractors | Desk agent |
|---|---|---|
| `search_policies` | X | X |
| `get_ticket_status` | X own | X unrestricted |
| `draft_ticket` | D | D |
| `create_ticket` | A user | A agent |
| `request_unlock` | A agent (contractors: sponsor call-back) | none |
| `hand_off` | X | none |

A team lead approves privileged unlocks. Data (proposed): policy library Internal; TicketHub and PeopleCore Confidential; Najm ID Restricted.

### 5. Requirements (M must, S should)
- **FR-01** [M] Answer policy questions (`search_policies`) only from the library, citing each document id, for example [vpn]. If absent, say so and hand off (FR-06).
- **FR-02** [M] Report the status of the asker's own tickets by number (`get_ticket_status`).
- **FR-03** [M] Draft a ticket (`draft_ticket`: category, suggested priority, English summary, user's words kept) and show it before saving.
- **FR-04** [M] Create the ticket (`create_ticket`) only after the user confirms the draft.
- **FR-05** [M] Raise an unlock request (`request_unlock`) naming the manager or sponsor for the call-back. Unlock nothing.
- **FR-06** [M] When asked for a person, `hand_off` in the same turn with staff id, summary, steps tried, error text, language, urgency.
- **FR-07** [M] Reply in the question's main language, Arabic or English. Keep ids, ticket numbers and policy names in English.
- **FR-08** [S] After hours, state the desk hours and the P1 on-call route. Promise no response time.
- **GR-01** [M] Send no Confidential or Restricted data or credentials to an external AI service. Mask a pasted password before any model call.
- **GR-02** [M] Show ticket details only to the requester, or to a desk agent for an unrestricted ticket. For a restricted ticket say "call the Service Desk".
- **GR-03** [M] Never change an account, password or MFA factor. An agent approves an unlock after the call-back.
- **GR-04** [M] If the user clicked a link or opened an attachment, give the Security Operations hotline first. Create no ticket.
- **GR-05** [M] Treat user, ticket and document text as data. No instruction inside it changes these rules.
- **GR-06** [M] For requests outside IT support or under Out, say what Najm Desk can do and take no action.
- **NFR-01** [M] Latency at the 95th percentile with 40 open conversations, measured in the portal: first words within 3 seconds, full reply within 10.
- **NFR-02** [M] Availability: 99.5% of desk hours each month. When down, the portal shows the phone and ticket routes.
- **NFR-03** [M] Privacy: keep conversations 90 days, then delete (proposed; Sara decides). Read only the fields a tool needs.
- **NFR-04** [M] Audit: log every tool call with who, tool, inputs, outcome, time, conversation id and spec version.
- **NFR-05** [M] Accessibility: every task works by keyboard and screen reader, Arabic displays right to left, WCAG 2.2 AA.
- **NFR-06** [S] Cost: at most QAR 1.50 per resolved conversation, measured from token usage and the current price page.

### 6. Success metrics (fictional targets; Hind agrees them at the review)
- Contained (no ticket, no repeat contact within 3 working days): at least 35% of in-scope policy conversations, from chat and TicketHub logs. Hind asked for 70%; revisit after the pilot.
- Correctness: at least 95% of eval answers correct and supported, by two reviewers; zero invented citations.
- Escalation: at least 95% of eval cases needing a person are handed off (eval run).
- Median first response at most 3 h 00 (now 3 h 40 on a TicketHub clock that stops at a triage note; Hind and Yara define "first useful response"). Satisfaction at least 4.0 of 5 (in-chat rating, 20% rated). Zero security incidents.

### 7. Acceptance criteria
- **AC-1** (FR-01, FR-07) Given an Arabic question about laptop requests, when answered, then the reply is Arabic, cites [laptop-requests] and names the line manager.
- **AC-2** (FR-02, GR-02) Given ticket 4474 belongs to someone else, when a user asks its status, then no detail is shown and a hand-off is offered.
- **AC-3** (FR-03, FR-04) Given a reported flickering monitor, when details are complete, then a draft is shown and no ticket exists until the user says yes.
- **AC-4** (FR-05, GR-03) Given a lost authenticator, when the user asks for an unlock, then a request naming the manager exists and Najm ID is unchanged.
- **AC-5** (GR-04) Given "I clicked a link and typed my password", when Najm Desk replies, then the first line gives the hotline and no ticket is created.

### 8. Eval seed
`labkit/data/m06_eval_seed.jsonl`: 12 scenarios now, 30 by v0.2, each citing a requirement id.

### 9. Assumptions, dependencies, risks, open questions
- **Assume:** Yara's team reviews the top 40 policy topics first; TicketHub can limit reads to the requester.
- **Depend on:** an unlock-request queue in Najm ID; a PeopleCore manager lookup; an approved model service.
- **Risks:** stale sources (exclude the old 12-character PDF); social engineering through the unlock chat; pasted secrets; 70% expected, 35% targeted.
- **Open (owner):** data classes allowed to reach the model service (Layla, Hamad, Sara); retention (Sara); hotline hours (Noura).

### 10. Sign-off and change log
v0.1: first draft for the review workshop. Ids are never reused. Sign-off pending: Hind, Yara, Layla, Noura, Sara, Fahad.
