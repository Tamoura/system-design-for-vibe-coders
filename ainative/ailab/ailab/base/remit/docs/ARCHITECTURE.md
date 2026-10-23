# Najm Remit: architecture

Remit lets Najm Bank's customers in Qatar send money to family abroad. It is a small
Python library with a command line, organised around one orchestrator,
`RemitService`, and a handful of single-purpose modules. All numbers in this document
and in the code are fictional.

## 1. Modules

| Module | Responsibility |
|---|---|
| `money.py` | `Money`: an immutable amount of one currency on `Decimal`, rounded half up |
| `corridors.py` | The registry of supported routes (QAR to INR, PHP, EGP, PKR) and their per-transfer limits |
| `fees.py` | Tiered fee schedules and `quote_fee` |
| `fx.py` | Rate providers, corridor margins and 60-second FX quotes |
| `risk.py` | Risk checks: sending limits and name screening, behind a single `check()` call |
| `ledger.py` | Double-entry postings for a sent transfer (old code, no dedicated tests: only `send()` exercises it) |
| `store.py` | SQLite repository for customers and transfers |
| `notify.py` | Notification templates in English and Arabic, and notifiers |
| `service.py` | `RemitService.quote()` and `RemitService.send()`: the orchestration |
| `cli.py`, `__main__.py` | `python -m remit ...` |
| `config.py`, `models.py`, `errors.py` | Settings, the `Customer` and `Transfer` dataclasses, the error classes |
| `najmkit/` | Vendored internal library: ids, clock, audit trail (see `najmkit.md`) |

Dependencies point one way: `service` uses everything; `fees` and `fx` use `money` and
`corridors`; `limits` uses `money`; `money` uses only `errors`, which uses nothing.

## 2. The life of a transfer

`RemitService.send()` runs these steps in order and stops at the first failure:

```text
validate -> limits -> screening -> fee -> fx -> ledger -> store -> notify
```

1. **Validate.** The customer exists; the recipient has a name; the corridor exists; the
   amount is within the corridor's minimum and maximum (both inclusive); the delivery
   method is offered on that corridor.
2. **Limits.** The customer's earlier transfers are added up for the current day and
   month and compared with the limits of their KYC tier. Over the limit raises
   `LimitExceeded`, writes an audit event and sends a `transfer_failed` notification.
3. **Screening.** The sender's and the recipient's names are checked against the
   watchlist. A match raises `ScreeningHit` and sends a deliberately vague
   `transfer_failed` notification: the customer is never told that a name matched.
4. **Fee** and 5. **FX.** Priced now, or taken from a `Quote` the customer was already
   shown (refused with `QuoteExpired` after 60 seconds, or `QuoteMismatch` when it does
   not belong to this transfer).
6. **Ledger.** The postings are made (section 6).
7. **Store.** The `Transfer` row is saved.
8. **Notify.** `transfer_sent` goes to the customer in their language. This is best
   effort: a `NotificationError` is audited but does not undo the transfer.

Time and ids are never read from globals inside the service: the clock is injected and
ids come from `najmkit.ids`.

## 3. Money

* `Money` wraps a `Decimal` and a currency code (QAR, INR, PHP, EGP, PKR, BDT; two
  decimal places each). It is created already rounded **half up**.
* Floats are rejected with `TypeError`. Mixing currencies raises `CurrencyMismatch`.
* SQLite stores amounts as text, never as `REAL`.

## 4. Fees and exchange rates

* A fee schedule is a table of tiers. The tier is picked by the **whole send amount**
  (not marginally), with the upper bound included. Each tier is a percentage plus a flat
  amount. A minimum and a cap apply, and the express surcharge is added after the cap.
* Two schedules exist, `STD-A` (INR, PHP) and `STD-B` (EGP, PKR).
* FX: the customer rate is the mid-market rate less the corridor's margin, rounded half
  up to four decimals. A quote lasts 60 seconds.

## 5. Limits

Remit applies two checks before money moves.

* **KYC tiers and limits.** Customers have a KYC tier. Two tiers are in use: T1
  (identity checked) may send up to QAR 5,000 per day and T2 (address and employer
  verified) up to QAR 25,000 per day. There is no monthly limit.
* **Windows.** A "day" is a Qatar calendar day: Qatar is UTC+3 all year, so the day runs
  from 21:00 to 21:00 UTC. Timestamps are stored in UTC and converted to Qatar time
  before deciding which day or month a transfer belongs to.
* Reaching the limit exactly is allowed; one dirham (0.01 QAR) over is not.

## 6. Risk checks

Name screening and the limits check are grouped in `risk.py`, which `RemitService`
calls once per transfer through `risk.check(customer, amount, history)`. The result
says whether the transfer may go ahead and why not. Screening data (the watchlist) is
passed in by the caller; `risk.py` never reads files.

## 7. Ledger

Each sent transfer is posted as one debit and up to three credits, all in QAR:

| Side | Account | Amount |
|---|---|---|
| Debit | `CUSTOMER:<id>` | send amount + fee |
| Credit | `PAYOUT_CLEARING` | send amount |
| Credit | `FEE_INCOME` | fee less the partner's share |
| Credit | `PARTNER_PAYABLE` | 30% of the fee |

This is a shadow ledger of Remit's own postings: the customer's real balance is in core
banking. The module keeps its state in module-level variables, which is why the tests
reset it.

## 8. Notifications

`notify.render(template_id, lang, **values)` fills a template. Money values are
formatted per language; Arabic uses Arabic-Indic digits and the currency's Arabic name.
Notifiers deliver in the customer's language: `InMemoryNotifier` for tests,
`ConsoleNotifier` for the CLI.

## 9. Storage and configuration

One SQLite file (`REMIT_DB`) with two tables, `customers` and `transfers`. Queries use
placeholders. Settings come from environment variables (`.env.example`); there is no
`.env` loader.

## 10. Errors

Everything Remit raises on purpose derives from `RemitError` and carries a stable
`code`. The CLI prints `error [code]: message` and exits with status 1.

## 11. Known limitations

* The steps from the ledger onwards are not atomic: if saving fails after the ledger
  has posted, the posting is not reversed.
* There is one rate provider, with fixed rates. There is no real payment gateway,
  e-mail or SMS sender.
