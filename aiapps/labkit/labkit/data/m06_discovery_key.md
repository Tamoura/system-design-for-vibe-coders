# Answer key for the lesson 6.1 sources (fictional) — SPOILER

Do your own pass over `m06_interview_hind.md`, `m06_interview_yara.md` and `m06_as_is_process.md` first, and write `docs/discovery-notes.md` before you open this file. Then compare. The key is not a model answer: a good reader finds items the author did not plant, and words them better. It is also the yardstick for checking what an AI assistant missed or invented.

## Contradictions (two sources disagree)

| # | Claim | Against | What to do with it |
|---|---|---|---|
| C1 | Half of tickets are passwords and access (H-02) | A quarter: 450 of 1,800 (A-03, Y-14) | Use the export; tell Hind gently, with the number |
| C2 | Ninety percent write in English; Arabic later (H-16, H-18) | A third write Arabic or mix (Y-22, A-16) | Arabic is a v1 requirement, not a later one |
| C3 | Any agent unlocks in a minute; the assistant should do it alone (H-12, H-14) | The policy needs a manager call-back, 20 minutes to 2 hours (Y-10, A-10) | The unlock is a request for an agent; the call-back stays human |
| C4 | Tickets are routed automatically (H-16) | The duty agent triages every ticket by hand (Y-06, A-07) | A drafted ticket must carry category and priority suggestions |
| C5 | Deflected means no ticket opened (H-26) | Count it only if no repeat contact within three working days (Y-32) | Define the metric before promising a number |
| C6 | Twenty-four hours a day is the best part (H-28) | Only P1 is handled outside hours; Friday and Saturday closed (Y-26, A-21) | After-hours behaviour is a requirement; promise no response time |
| C7 | Seventy percent, and never wrong (H-04, H-08) | Only 22 of 40 questions fully covered (A-05) | A coverage-versus-accuracy trade-off nobody has made yet |
| C8 | Hand-offs are failures (H-26) | A good handover is not a failure (Y-28) | Measure hand-off quality, not hand-off count |
| C9 | Contractors: the same rules, not looked into (H-22) | Guests with a sponsor, no PeopleCore record (Y-12, A-18) | A separate path for contractors |
| C10 | The policy library is current (H-06) | Notices never reach the pages; an old PDF says 12 characters (Y-20, A-09) | Source-of-truth and freshness requirements |
| C11 | The first-response median is 3 h 40 min (H-02) | The clock stops at the triage note (A-13) | Define "first useful response" |
| C12 | The assistant should know everything about each person (H-24) | Restricted tickets, stale PeopleCore and DeviceDesk data (Y-12, Y-20, A-17) | Least data, purpose by purpose |

## Hidden requirements (nobody asked for them; they will fail the project if missed)

1. Identity is verified by a call-back to the manager's number in PeopleCore, never a number the requester gives (Y-10).
2. The PeopleCore manager is wrong for about one person in ten, so the requester must confirm it (Y-12).
3. Contractors need a sponsor call-back (Y-12, A-18).
4. A good ticket carries the four facts agents always ask for: network, error text, since when, device (Y-02, A-08).
5. Drafted tickets are in English, with the user's own words kept (Y-22, A-16).
6. Mixed Arabic and English input must work (Y-22, A-16).
7. The assistant suggests a priority and never sets one; cluster detection is out of scope (Y-08).
8. Restricted tickets are never described to the requester (Y-24, A-17).
9. Passwords pasted into chat or tickets must not be repeated or stored (Y-24, A-19).
10. "I think I clicked" means the Security Operations hotline first, not a ticket (Y-24, A-22).
11. After hours: state the hours and the P1 on-call route (Y-26, A-21).
12. The Sunday 07:00 to 10:00 peak sets the load target (Y-26, A-14).
13. Keyboard and screen-reader use (Y-30).
14. Stale sources must be fixed or excluded: the old 12-character PDF, the VPN notice that never reached the page, Yara's cheat sheet, DeviceDesk's three-year refresh flag (Y-18, Y-20, A-09).
15. The measurements need definitions: first useful response, deflection, and a survey that only 1 in 8 answer (A-12, A-13, Y-30, Y-32).
16. About 200 to 300 Teams messages a week are never tickets, so the baseline undercounts the demand (Y-04, A-02).
17. A 2022 vendor bot failed because it had no route to a person (H-08), and an audit comment followed a policy mistake about contractors (H-10).
18. Governance takes time: Layla's committee every second Tuesday, Hamad's team for Najm ID, Sara for chat storage, a month per review, against a pilot "before the end of next month" (H-30). Run costs next year need a case (H-26).

## The interviewer's mistakes

- **H-03**: a leading, hypothetical question that also pitches the solution. It earns a number (70%) and no evidence.
- **H-17**: a closed question that confirms the interviewer's assumption about language. The data later disagreed.
- **H-19**: asks for an opinion about future behaviour ("you think staff would use…"). Look at what people do today: phone is the biggest channel (Y-04, A-01).
- **H-21 and H-22**: a good question, abandoned too early. "I haven't looked into it" deserved a follow-up or a note as an open question.

Good questions to copy: H-01, H-05, H-09 and H-13 (a past event, a specific example, a probe on the worst case, a probe on what slows things down), and Y-01, Y-09 and Y-31.

## Open questions worth asking in the second round

- Which channel will Najm Desk live in: the portal, Teams, both? Phone is the largest channel today (A-01).
- Are Confidential or Restricted data allowed to reach the model service at all? Ticket text can contain personal data and secrets. (Layla, Hamad, Sara.)
- How long may chat logs be kept, and who may read them? (Sara.)
- Does Najm ID offer a way to raise an unlock request, and who may approve one for a privileged account?
- Can the TicketHub API show the restricted flag, and can it limit a read to the requester's own tickets?
- Who owns the policy library and the notices, and who will keep both current?
- What are the hotline's opening hours?
- What does "first useful response" mean to Hind, and may the desk change the TicketHub clock?
- If the manager does not answer, who is the delegate?
- Who in the business will review the first fifty answers, and how many hours a week can Yara give?
