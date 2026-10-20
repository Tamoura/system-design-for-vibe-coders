# Najm Desk user guide: v1
<!-- Fictional engagement. For the Service Desk team and for the staff who chat with Najm Desk. One page: what it is, how to use it, and what to do when it is wrong. -->
Version: TODO   Owner: Yara (content) and Lujain (accuracy)   Reviewed: TODO date

## What Najm Desk is
An AI assistant for the bank's IT Service Desk. It answers IT policy questions from the policy library and shows its source, shows the status of your own tickets, drafts a ticket for you to confirm, raises an account-unlock request for an agent to approve, and passes you to a person with everything you told it. It is software and it can be wrong.

## What it can and cannot do
| It can | It cannot (in v1) |
|---|---|
| Answer policy questions and cite the policy, for example [vpn#0] | Decide what a policy leaves to a person |
| Show the status of your own tickets by number | Show anyone else's ticket |
| Draft a ticket, and create it after you say yes | Set a ticket's priority |
| Raise an unlock request that names your manager for a call-back | Unlock, reset or change an account, a password or an MFA factor |
| Hand you to a person with a summary | Promise a response time: it tells you the desk hours instead |

## How to ask
Write as you would to a colleague, in English, Arabic or both. Ask one thing at a time. Give ticket numbers as digits. Say what you already tried and the exact error text.

## Reading an answer
- A policy answer ends with its source in square brackets. Open it. An answer with no source is unreliable: ask for a person.
- "I don't know based on the provided documents" is a good answer. It means the library has nothing, and a person will follow up.
- A draft ticket is not a ticket until you confirm it.

## Never paste
Passwords, one-time codes, card numbers or customer data. Najm Desk masks some of these before they leave the bank's systems, but masking is a safety net, not permission. If you clicked a link or opened an attachment and are worried, call the Security Operations hotline first. Do not wait for the chat.

## When it is wrong
1. Use the rating at the end of the chat and write a few words about what was wrong.
2. Note the reference id Najm Desk shows and tell the Service Desk.
3. Advice that could cause harm (security, access): tell your team lead at once. They will call the on-call engineer, who can switch Najm Desk off.

## For Service Desk agents
- Drafts and hand-offs arrive in TicketHub with the staff member's words, the steps tried, the error text and the language. Check them, edit them, send them.
- Approve an unlock only after the call-back to the manager listed in PeopleCore, never to a number the requester gives you.
- A draft you rewrite is the best feedback we get. Tell your champion what was wrong with it.

## Hours and contacts
Service Desk: Sunday to Thursday, 07:00 to 17:00 Qatar time. Outside those hours only P1 incidents are handled, through the on-call number: TODO. Security Operations hotline: TODO. Najm Desk champion on your shift: TODO.
