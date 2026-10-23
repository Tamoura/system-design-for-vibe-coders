# KIT_NOTES: the lab kit's facts, for lab writers

This file is the single source of truth for everyone who writes a lab or a lesson that touches
the repository. **Read it before you write; never contradict it.** The tables of signatures and
constants below are generated from the code (`tests/kit_notes_tables.py`) and a test fails when
they drift, so you can quote them with confidence. Everything is fictional.

Contents: 1 Run only your lab's tests · 2 File map · 3 The base repository (Najm Remit) · 4 The register
of quirks, smells and gaps · 5 Determinism · 6 How to write a lab · 7 The framework API · 8 What each
planned lab needs from the base · 9 Open questions for the course owner · 10 Shared-kit findings from the
dry-runs: fixed centrally, and left alone on purpose

---

## 1. Run only your lab's tests (other writers' labs may be unfinished)

While labs are being written in parallel in `ailab/labs/`, the full suite can contain someone
else's half-built lab (all fifteen are built now; the advice stays useful for a new lab). Each lab is isolated: discovery lists labs by folder name and imports a lab only
when it is asked for, and the generic test is parametrised per lab, so a broken lab fails **only its own
test cases**. To run just yours (from `ainative/ailab`):

```bash
# the generic lifecycle test for your lab + your own negative tests
/home/user/coursework/venv/bin/pytest -q tests/test_labs_m05.py tests/test_labs_generic.py -k m05

# only the generic lifecycle test, for one lab
/home/user/coursework/venv/bin/pytest -q tests/test_labs_generic.py -k m05

# start/grade/solve by hand
python -m ailab list                      # a lab that does not import is listed as BROKEN with the error
python -m ailab start m05 --dir /tmp/m05
python -m ailab grade m05 --dir /tmp/m05
python -m ailab solve m05 --dir /tmp/m05
```

`start` and `solve` end by printing the grade command for the work directory in a form that works from ANY directory:
`PYTHONPATH=<absolute path of ainative/ailab> python -m ailab grade m05 --dir <work dir>` (a PowerShell form on Windows), so a lab
or lesson never needs to say "run it from the ailab folder" for correctness; both forms are right (`cli.grade_command`).

`-k m05` selects by substring, so name your test file `tests/test_labs_m05.py` and every test in it is
selected too. Before you finish, run the **whole** suite once; failures in other labs are theirs, failures
anywhere else (framework, base, notes) are everybody's and must be reported, not worked around.
`start/grade/solve <id>` load only the lab you name. Do not edit `ailab/framework.py`, `checks.py`,
`gitutil.py`, `runner.py`, `cli.py` or `base/` while you write a lab; if you need something, say so in your
report to the course owner.

## 2. File map

The layout follows AUTHORING.md: the importable package `ailab` holds the framework **and** the base
repository, the labs and the stubs. In a lesson, a path comment such as `# ailab/labs/m08_harden/assets/x.py`
is relative to `ainative/ailab/`, so the file is `ainative/ailab/ailab/labs/m08_harden/assets/x.py`.

```text
ainative/ailab/
  README.md  KIT_NOTES.md  requirements.txt  pytest.ini  check_blocks.py
  ailab/                         # the package: python -m ailab ...
    __main__.py  cli.py          # list | doctor | start | grade | solve
    framework.py                 # Check, Lab, tolerant discovery, start/grade/solve, seed helpers, doctor
    checks.py                    # helpers every grader reuses (pytest runners, git checks, secrets, mutants, JSON, Markdown)
    checks_m00.py ... checks_m14.py   # helpers private to one lab (its own graders and wrappers)
    gitutil.py  runner.py        # git and subprocess plumbing
    base/remit/                  # the frozen base repository (copied by `start`)
      README.md CONTRIBUTING.md pyproject.toml .gitignore .env.example .github/workflows/ci.yml
      docs/ARCHITECTURE.md docs/najmkit.md docs/TOUR.md
      src/remit/   money corridors fees fx limits screening ledger store notify service cli config models errors
      src/najmkit/ ids clock audit            # the vendored internal library, API v1
      tests/       conftest + test_money/corridors/fees/fx/limits/notify/service/store/najmkit/config_cli
    labs/                        # one folder per lab: m00_first_fix ... m14_capstone (all built)
      __init__.py                # re-exports discovery
      m00_first_fix/             # the exemplar: lab.py task.md solution/ hidden/
    stubs/claude                 # built (by the m09 writer): a STAND-IN for the `claude` CLI's print mode, used by lab m09 only;
                                 #   deterministic, calls no model, copied for the learner to lab-assets/bin/claude
  tests/                         # the kit's own tests: test_framework, test_checks, test_cli, test_base,
                                 #   test_base_notes, test_kit_notes, test_check_blocks, test_parallel_authoring,
                                 #   test_labs_generic (every lab), test_labs_m00 (+ one test_labs_mNN.py per lab)
                                 #   conftest.py (helpers, fake labs), kit_notes_tables.py (the generator)
```

A lab folder `labs/mNN_slug/` contains: `lab.py` (defines `LAB`), `task.md` (the ticket), optional `assets/`
(copied to `lab-assets/` in the learner's repo), optional `hidden/` (hidden pytest files, never copied to the
learner), `solution/` (data for `solve`). The folder name's `mNN` must equal `LAB.id`.

## 3. The base repository: Najm Remit

A small Python 3.11, standard-library-only service (src layout, `pytest` for tests, `pythonpath = ["src"]`
in `pyproject.toml`). About 99 passing tests, all deterministic. `ailab start` copies it (without caches),
`git init`s it on branch `main`, commits "Initial state", runs the seed, commits "Lab starting state"
and tags that commit `lab-start`.

The flow of `RemitService.send`: **validate, limits, screening, fee, fx, ledger, store, notify**, stopping
at the first failure. `quote` prices without sending. Notifications are best effort; audit events
(`transfer.sent`, `transfer.rejected`, `notification.failed`) go through `najmkit.audit`.

### 3.1 Public API labs may rely on (generated)

<!-- BEGIN GENERATED: signatures -->
```text
# remit.money
CURRENCIES = {'QAR': 2, 'INR': 2, 'PHP': 2, 'EGP': 2, 'PKR': 2, 'BDT': 2}
ROUNDING = 'ROUND_HALF_UP'
def quantize(value: Decimal, places: int = 2) -> Decimal
class Money(amount: Decimal | int | str, currency: str)
    @classmethod zero(currency: str) -> Money
    .amount  # property -> Decimal
    .currency  # property -> str
    def is_negative() -> bool

# remit.corridors
DELIVERY_METHODS = ('bank_deposit', 'cash_pickup', 'wallet')
class Corridor  # frozen dataclass
    send_currency: str
    receive_currency: str
    min_send: Money
    max_send: Money
    delivery_methods: tuple[str, ...]
    fee_schedule: str
    .default_delivery  # property -> str
CORRIDORS: dict[str, Corridor]  # keys: QAR-INR, QAR-PHP, QAR-EGP, QAR-PKR
def get_corridor(send_currency: str, receive_currency: str) -> Corridor
def corridor_for_code(code: str) -> Corridor
def all_corridors() -> list[Corridor]
def validate_send(corridor: Corridor, amount: Money, delivery_method: str | None = None) -> str

# remit.fees
class FeeTier  # frozen dataclass
    upto: Decimal | None
    percent: Decimal
    flat: Decimal
class FeeSchedule  # frozen dataclass
    id: str
    tiers: tuple[FeeTier, ...]
    minimum: Decimal
    cap: Decimal
    express_surcharge: Decimal
    def tier_index(amount: Decimal) -> int
SCHEDULES: dict[str, FeeSchedule]  # keys: STD-A, STD-B
class FeeBreakdown  # frozen dataclass
    schedule_id: str
    tier_index: int
    raw: Money
    minimum_applied: bool
    cap_applied: bool
    base: Money
    surcharge: Money
    total: Money
def get_schedule(schedule_id: str) -> FeeSchedule
def explain_fee(amount: Money, corridor: Corridor, *, express: bool = False) -> FeeBreakdown
def quote_fee(amount: Money, corridor: Corridor, *, express: bool = False) -> Money

# remit.fx
QUOTE_TTL = datetime.timedelta(seconds=60)
class RateProvider  # Protocol
    def get_rate(send_currency: str, receive_currency: str, at: datetime) -> Decimal
class StaticRateProvider(rates: Mapping[str, Decimal] | None = None)
    def get_rate(send_currency: str, receive_currency: str, at: datetime) -> Decimal
class FxQuote  # frozen dataclass
    rate: Decimal
    receive: Money
    expires_at: datetime
    def is_expired(now: datetime) -> bool
def margin_for(corridor: Corridor) -> Decimal
def customer_rate(mid_rate: Decimal, margin: Decimal) -> Decimal
def fx_quote(send: Money, corridor: Corridor, provider: RateProvider, now: datetime) -> FxQuote

# remit.limits
QATAR_UTC_OFFSET = datetime.timedelta(seconds=10800)
QATAR_TZ = datetime.timezone(datetime.timedelta(seconds=10800), 'AST')
DAILY_EXCEEDED = 'daily_limit_exceeded'
MONTHLY_EXCEEDED = 'monthly_limit_exceeded'
class TierLimits  # frozen dataclass
    daily: Money
    monthly: Money
LIMITS: dict[str, TierLimits]  # keys: T1, T2, T3
class HistoryItem  # Protocol
    created_at: datetime
    send_amount: Money
class LimitResult  # frozen dataclass
    allowed: bool
    reason: str | None
    tier: str
    daily_used: Money
    daily_limit: Money
    monthly_used: Money
    monthly_limit: Money
    .daily_remaining  # property -> Money
    .monthly_remaining  # property -> Money
def limits_for(tier: str) -> TierLimits
def to_local(moment: datetime) -> datetime
def day_window(now: datetime) -> tuple[datetime, datetime]
def month_window(now: datetime) -> tuple[datetime, datetime]
def check_limits(tier: str, history: Iterable[HistoryItem], amount: Money, now: datetime) -> LimitResult

# remit.models
KYC_TIERS = ('T1', 'T2', 'T3')
LOYALTY_TIERS = ('none', 'silver', 'gold')
LANGUAGES = ('en', 'ar')
class Customer  # frozen dataclass
    id: str
    name: str
    kyc_tier: str
    loyalty_tier: str = 'none'
    language: str = 'en'
class Transfer  # frozen dataclass
    id: str
    customer_id: str
    corridor: str
    send_amount: Money
    fee: Money
    receive_amount: Money
    rate: Decimal
    recipient_name: str
    delivery_method: str
    created_at: datetime
    express: bool = False
    status: str = 'completed'

# remit.notify
TEMPLATES: dict[str, dict]  # keys: transfer_sent, transfer_failed
FAILURE_REASONS: dict[str, dict]  # keys: limit_exceeded, needs_review
def render(template_id: str, lang: str, **values: Any) -> str
def format_money(money: Money, lang: str) -> str
def format_number(value: Decimal, lang: str) -> str
def localize_digits(text: str, lang: str) -> str
def failure_reason(code: str, lang: str) -> str
class Notification  # frozen dataclass
    customer_id: str
    template_id: str
    lang: str
    text: str
class Notifier  # Protocol
    def notify(customer: Customer, template_id: str, **values: Any) -> Notification
class InMemoryNotifier  # dataclass
    sent: list[Notification] = <factory>
    def notify(customer: Customer, template_id: str, **values: Any) -> Notification
class ConsoleNotifier(stream: TextIO | None = None)
    def notify(customer: Customer, template_id: str, **values: Any) -> Notification

# remit.service
class Quote  # frozen dataclass
    corridor: Corridor
    send_amount: Money
    fee: Money
    total: Money
    fx: FxQuote
    express: bool
    delivery_method: str
class SendResult  # frozen dataclass
    transfer: Transfer
    total_debited: Money
    limits: LimitResult
    notified: bool
class RemitService(store: Store, rates: RateProvider, watchlist: Iterable[str], clock: Any, notifier: notify.Notifier)
    def quote(send_amount: Money, receive_currency: str, *, express: bool = False, delivery_method: str | None = None) -> Quote
    def send(customer_id: str, send_amount: Money, receive_currency: str, recipient_name: str, *, express: bool = False, delivery_method: str | None = None, quote: Quote | None = None) -> SendResult
    def history(customer_id: str) -> list[Transfer]

# remit.store
class Store(path: str | os.PathLike[str] = ':memory:')
    def close() -> None
    def add_customer(customer: Customer) -> None
    def create_customer(name: str, kyc_tier: str = 'T1', loyalty_tier: str = 'none', language: str = 'en') -> Customer
    def get_customer(customer_id: str) -> Customer | None
    def require_customer(customer_id: str) -> Customer
    def list_customers() -> list[Customer]
    def search_by_name(fragment: str) -> list[Customer]
    def save_transfer(transfer: Transfer) -> None
    def get_transfer(transfer_id: str) -> Transfer | None
    def list_transfers(customer_id: str, since: datetime | None = None) -> list[Transfer]
    def count_transfers() -> int

# remit.screening  (LEGACY)
THRESHOLD = 100
FUZZY_PERCENT = 85
MIN_FUZZY_LEN = 5
MAX_TOKENS = 4
PARTICLES = frozenset(['al', 'ben', 'bin', 'bint', 'el', 'ibn'])
DEFAULT_WATCHLIST = ('Karim Nasser Al-Qadiri', 'Vorlon Trading FZE', 'Samir Haddad Younis', 'Elena Markovic Petrov', ...
class Match  # frozen dataclass
    name: str
    entry: str
    score: int
class ScreenResult  # frozen dataclass
    hit: bool
    matches: tuple[Match, ...]
def tokens(name: str) -> list[str]
def match_score(a: Sequence[str], b: Sequence[str]) -> int
def screen(name: str, watchlist: Iterable[str], threshold: int = 100) -> ScreenResult
def screen_names(names: Iterable[str], watchlist: Iterable[str]) -> ScreenResult
def load_watchlist(path: str) -> list[str]

# remit.ledger  (LEGACY)
ACCOUNT_PAYOUT = 'PAYOUT_CLEARING'
ACCOUNT_FEE_INCOME = 'FEE_INCOME'
ACCOUNT_PARTNER = 'PARTNER_PAYABLE'
PARTNER_SHARE = Decimal('0.30')
def customer_account(customer_id: str) -> str
def post_transfer(transfer_id: str, customer_id: str, send_amount: Money, fee: Money) -> list[dict[str, Any]]
def balance(account: str) -> Decimal
def accounts() -> list[str]
def journal() -> list[dict[str, Any]]
def reset() -> None

# remit.config
ENVIRONMENTS = ('dev', 'test', 'prod')
class Config  # frozen dataclass
    env: str = 'dev'
    db_path: str = 'remit.db'
    audit_log: str | None = None
    watchlist_path: str | None = None
    language: str = 'en'
def load_config(environ: Mapping[str, str] | None = None) -> Config

# remit.cli
def main(argv: Sequence[str] | None = None, *, environ: dict[str, str] | None = None, clock: Any = None, out: TextIO | None = None, err: TextIO | None = None) -> int

# najmkit.ids
def new_id(prefix: str) -> str
class SequentialIds(start: int = 1)
def use_generator(generator: Callable[[], str] | None) -> None

# najmkit.clock
class Clock  # Protocol
    def now() -> datetime
class SystemClock()
    def now() -> datetime
class FixedClock(start: datetime | str)
    def now() -> datetime
    def set(moment: datetime | str) -> None
    def advance(**delta: int) -> datetime
def now() -> datetime
def set_clock(clock: Clock) -> None
def get_clock() -> Clock
def reset_clock() -> None

# najmkit.audit
ENV_VAR = 'NAJMKIT_AUDIT_LOG'
def configure(path: str | os.PathLike[str] | None) -> None
def current_path() -> Path | None
def log_event(event: str, **fields: Any) -> dict[str, Any]
def read_events(path: str | os.PathLike[str] | None = None) -> list[dict[str, Any]]

# remit.errors  (all derive from RemitError; each has a stable .code)
AmountOutOfRange(RemitError, ValueError)  code='amount_out_of_range'
CurrencyMismatch(RemitError, ValueError)  code='currency_mismatch'
DuplicatePosting(RemitError)  code='duplicate_posting'
InvalidAmount(RemitError, ValueError)  code='invalid_amount'
InvalidRequest(RemitError, ValueError)  code='invalid_request'
LimitExceeded(RemitError)  code='limit_exceeded'
MissingTemplateVariable(RemitError, ValueError)  code='missing_template_variable'
NotificationError(RemitError)  code='notification_error'
QuoteExpired(RemitError)  code='quote_expired'
QuoteMismatch(RemitError, ValueError)  code='quote_mismatch'
RateUnavailable(RemitError, LookupError)  code='rate_unavailable'
ScreeningHit(RemitError)  code='screening_hit'
StoreError(RemitError)  code='store_error'
UnknownCorridor(RemitError, LookupError)  code='unknown_corridor'
UnknownCurrency(RemitError, ValueError)  code='unknown_currency'
UnknownCustomer(RemitError, LookupError)  code='unknown_customer'
UnknownFeeSchedule(RemitError, LookupError)  code='unknown_fee_schedule'
UnknownKycTier(RemitError, ValueError)  code='unknown_kyc_tier'
UnknownTemplate(RemitError, LookupError)  code='unknown_template'
UnsupportedDeliveryMethod(RemitError, ValueError)  code='unsupported_delivery_method'
UnsupportedLanguage(RemitError, ValueError)  code='unsupported_language'
```
<!-- END GENERATED: signatures -->

Notes on the signatures:

* `Money(amount, currency)` accepts `Decimal`, `int` or `str`; **a float or bool raises `TypeError`**, as does
  arithmetic or ordering with a float. `==` with a non-Money is simply `False`. Amounts are rounded half up to
  2 decimals on creation. Mixed currencies raise `CurrencyMismatch`. `Money / Money` is a `Decimal`.
* `send` takes `Money` for the amount, the receive **currency code** (`"INR"`) and the recipient's name.
  The send currency is always QAR (the corridor is looked up from the amount's currency).
* `RemitService(store, rates, watchlist, clock, notifier)`: `watchlist` is any iterable of names, `clock` anything with
  `.now()`, `notifier` anything with `.notify(customer, template_id, **values)`. There is **no** ledger parameter: the
  service calls the module-level `ledger` functions.
* `LimitResult.daily_used`/`monthly_used` are the amounts **before** the transfer being checked.
* `InMemoryNotifier.sent` is the list of `Notification(customer_id, template_id, lang, text)` it has delivered; it
  renders `render(template_id, customer.language, name=customer.name, **values)`.
* `Store` is a context manager; `":memory:"` is the default path. `create_customer` uses `najmkit.ids.new_id("CUS")`.
* The CLI: `python -m remit quote QAR 500 INR [--express] [--delivery wallet]`, `customer add|list`, `send --customer ID QAR 500 INR --recipient NAME`,
  `history --customer ID`. Exit codes 0 ok, 1 a RemitError (`error [code]: message` on stderr), 2 bad usage.
  `quote` uses an in-memory database; the others use `REMIT_DB` (default `remit.db`).
  **`python -m remit` needs `PYTHONPATH=src` (or `pip install -e .`); `pytest` does not** (pyproject sets the path).

### 3.2 The fictional constants (generated)

<!-- BEGIN GENERATED: constants -->
**Currencies** (`money.CURRENCIES`, all with 2 decimals): QAR, INR, PHP, EGP, PKR, BDT.

**Corridors** (`corridors.CORRIDORS`; amounts in QAR; both limits inclusive):

| Code | min_send | max_send | delivery_methods (first = default) | fee_schedule |
|---|---:|---:|---|---|
| QAR-EGP | 100.00 | 15,000.00 | bank_deposit, wallet | STD-B |
| QAR-INR | 50.00 | 25,000.00 | bank_deposit, wallet | STD-A |
| QAR-PHP | 50.00 | 20,000.00 | bank_deposit, cash_pickup, wallet | STD-A |
| QAR-PKR | 100.00 | 15,000.00 | bank_deposit, cash_pickup | STD-B |

**Fee schedules** (`fees.SCHEDULES`). Tier chosen by the whole amount, `upto` inclusive; `raw = amount x percent + flat`; `base = min(max(raw, minimum), cap)`; `total = base + express_surcharge` if express.

`STD-A`: minimum 5.00, cap 150.00, express surcharge 15.00 (QAR)

| Tier | upto (QAR) | percent | flat (QAR) |
|---:|---:|---:|---:|
| 0 | 500.00 | 2% | 2.00 |
| 1 | 2,000.00 | 1.5% | 5.00 |
| 2 | 10,000.00 | 1% | 20.00 |
| 3 | no limit | 0.75% | 50.00 |

`STD-B`: minimum 6.00, cap 120.00, express surcharge 20.00 (QAR)

| Tier | upto (QAR) | percent | flat (QAR) |
|---:|---:|---:|---:|
| 0 | 1,000.00 | 2.5% | 3.00 |
| 1 | 5,000.00 | 1.8% | 10.00 |
| 2 | no limit | 1.2% | 40.00 |

**Fee examples** (computed by `fees.quote_fee`, QAR):

| Amount | QAR-INR | QAR-INR express | QAR-PKR | QAR-PKR express |
|---:|---:|---:|---:|---:|
| 100.00 | 5.00 | 20.00 | 6.00 | 26.00 |
| 150.25 | 5.01 | 20.01 | 6.76 | 26.76 |
| 500.00 | 12.00 | 27.00 | 15.50 | 35.50 |
| 500.01 | 12.50 | 27.50 | 15.50 | 35.50 |
| 1000.00 | 20.00 | 35.00 | 28.00 | 48.00 |
| 2000.00 | 35.00 | 50.00 | 46.00 | 66.00 |
| 2000.01 | 40.00 | 55.00 | 46.00 | 66.00 |
| 10000.00 | 120.00 | 135.00 | 120.00 | 140.00 |
| 10000.01 | 125.00 | 140.00 | 120.00 | 140.00 |
| 20000.00 | 150.00 | 165.00 | 120.00 | 140.00 |

(`quote_fee` does not check a corridor's `min_send`/`max_send`; `corridors.validate_send` and the service do.)

**FX** (`fx.DEFAULT_MID_RATES`, `fx.CORRIDOR_MARGINS`; customer rate = mid x (1 - margin), 4 dp half up; quote valid for 60 s, expired from `expires_at` onwards):

| Corridor | mid rate | margin | customer rate | 500.00 QAR buys |
|---|---:|---:|---:|---:|
| QAR-INR | 22.80 | 0.0100 | 22.5720 | 11,286.00 INR |
| QAR-PHP | 15.40 | 0.0125 | 15.2075 | 7,603.75 PHP |
| QAR-EGP | 13.20 | 0.0150 | 13.0020 | 6,501.00 EGP |
| QAR-PKR | 77.00 | 0.0150 | 75.8450 | 37,922.50 PKR |

**Limits** (`limits.LIMITS`, QAR; allowed when `used + amount <= limit`; windows are Qatar calendar day/month, UTC+3):

| KYC tier | daily | monthly |
|---|---:|---:|
| T1 | 2,000.00 | 8,000.00 |
| T2 | 10,000.00 | 40,000.00 |
| T3 | 30,000.00 | 120,000.00 |

**Notifications** (`notify.TEMPLATES`): `transfer_sent` (ar/en), `transfer_failed` (ar/en). Failure reasons (`notify.FAILURE_REASONS`): `limit_exceeded`, `needs_review`.

**Ledger** postings per sent transfer: debit `CUSTOMER:<id>` for send + fee; credit `PAYOUT_CLEARING` for send; credit `PARTNER_PAYABLE` for 0.30 x fee (half-even, Q-LED-1); credit `FEE_INCOME` for the rest. Balance = credits minus debits.

**Screening constants:** THRESHOLD=100, FUZZY_PERCENT=85, MIN_FUZZY_LEN=5, MAX_TOKENS=4, particles dropped: al, ben, bin, bint, el, ibn. Demo watchlist: `Karim Nasser Al-Qadiri`; `Vorlon Trading FZE`; `Samir Haddad Younis`; `Elena Markovic Petrov`; `Test Sanctioned Person`.
<!-- END GENERATED: constants -->

Other exact facts:

* **Rounding:** everything is half up (`Money`, fee, receive amount, customer rate to 4 dp) **except** the ledger's
  partner share (half-even, Q-LED-1) and difflib's integer similarity in screening.
* **Windows:** `QATAR_TZ = timezone(timedelta(hours=3), "AST")`. A day is `[00:00, 24:00)` at UTC+3, i.e. 21:00Z to 21:00Z.
  `to_local()` is the single place that converts; `day_window`/`month_window` and `check_limits` use it. Boundary
  example: 2026-03-02T20:59:59Z is still Monday 2 March; 21:00:00Z is Tuesday 3 March. Month: 2026-02-28T21:00Z is 1 March.
* **Limit comparison:** allowed iff `used + amount <= limit` (the limit itself is allowed, one cent over is not). Daily is checked before monthly.
* **Tier boundary (fees):** the tier is chosen by the whole amount with `amount <= upto` (500.00 is tier 0, 500.01 is tier 1). Fees never decrease
  as the amount grows. The express surcharge is added **after** the cap, so an express fee can exceed the cap.
* **Corridor limits:** `min_send` and `max_send` are inclusive. `quote_fee` and `fx_quote` do not check them; `validate_send` and the service do.
* **Quote expiry:** valid while `now < expires_at`, expired when `now >= expires_at` (`expires_at = now + 60 s`).
* **Delivery:** the default is the first method of the corridor.
* **Arabic:** `format_money` writes Arabic-Indic digits (٠١٢٣٤٥٦٧٨٩), `٬` as thousands separator, `٫` as decimal separator and the
  currency's Arabic name (`CURRENCY_NAMES_AR`, which includes BDT). Names and ids inside Arabic text are inserted unchanged (Latin, no bidi marks).
  Example: `format_money(Money("1234.5", "QAR"), "ar") == "١٬٢٣٤٫٥٠ ريال قطري"`.
* **Message texts** (exact, used by m00): English `transfer_sent` is
  `Hi {name}, your transfer {transfer_id} was sent. {recipient} received {receive_amount}. You paid {send_amount} plus a fee of {fee}.`
  `transfer_failed` takes `name, send_amount, recipient, reason`. **There is no `limit_warning` template** (m04 adds it).
* **Failure notifications:** limit rejections say the transfer "would take you over your sending limit"; a screening hit says only that
  "we need to review it" (never mention sanctions to the customer). Neither debits anything: the ledger is posted only after screening.
* **Kit-created repo facts:** branch `main`; `TASK.md` and `lab-assets/` are **committed in the "Lab starting state" commit** (so `git add -A`
  never sweeps them into a learner's change); `git config ailab.lab` remembers the lab id; `.git/info/exclude` hides `.claude/settings.local.json`,
  `.DS_Store`, `.aider*`, `.idea/`, `.vscode/`. If git has no identity the kit sets a local one (`Najm Learner`).

### 3.3 najmkit (API v1) and its call sites

`najmkit` is documented for learners in `docs/najmkit.md` (the file an agent must read; it cannot know the library). It has `ids.new_id(prefix)`,
`clock.now()/FixedClock/SystemClock`, `audit.log_event(event, **fields)`. Direct call sites in `src/remit` (nine):

| Call | Where |
|---|---|
| `ids.new_id("TRF")` | `service.py`, `send` |
| `ids.new_id("CUS")` | `store.py`, `create_customer` |
| `ids.new_id("JNL")` | `ledger.py`, `_post` |
| `clock.now()` | `ledger.py`, `_post` (the **global** clock) |
| `audit.log_event("transfer.sent" ...)` | `service.py`, `send` |
| `audit.log_event("transfer.rejected" ...)` | `service.py`, `_reject` |
| `audit.log_event("notification.failed" ...)` | `service.py`, `_notify` |
| `audit.configure(config.audit_log)` | `cli.py`, `main` |
| `SystemClock()` | `cli.py`, `main` |

Plus three uses of the *injected* clock object (`self.clock.now()` in `service.py`). The tests use najmkit v1 directly in `tests/conftest.py`
(`ids.use_generator`, `clock.set_clock/FixedClock/reset_clock/get_clock`, `audit.configure`), `test_najmkit.py`, `test_service.py`, `test_config_cli.py`,
`test_store.py`. A v1 to v2 migration (m07) must update all of them.

### 3.4 What is tested and what is not

| Module | Tests | Notes |
|---|---|---|
| money, corridors, fees, fx, limits, notify | thorough (`test_<module>.py`) | exact numbers, boundaries, Arabic text, both rounding directions |
| service | light (`test_service.py`) | happy path, validation, limits, screening, quotes, notification failure, audit |
| store, najmkit, config, cli | `test_store.py`, `test_najmkit.py`, `test_config_cli.py` | `search_by_name` only on the happy path (S-STORE-1 is untested on purpose) |
| **ledger** | **no dedicated tests** | exercised only indirectly through `service.send`; the visible tests assert no ledger balance |
| **screening** | **no dedicated tests** | exercised only indirectly through `service.send` |

The base documents (README, `docs/TOUR.md`, `docs/ARCHITECTURE.md`) say exactly this: "no dedicated tests, only exercised through `send()`", never plain "no tests".

`tests/conftest.py` (autouse `isolated_world`): clears `REMIT_*`/`NAJMKIT_AUDIT_LOG`, calls `ledger.reset()`, installs `SequentialIds()` and a
global `FixedClock(2026-03-02T09:00:00Z)` (a Monday; 12:00 in Qatar), restores everything afterwards. Fixtures: `now`, `clock` (the global FixedClock), `store`
(in-memory), `customers` (C001 Aisha Rahman T2 none en; C002 Bilal Khan T1 silver en; C003 Mariam Saleh T3 gold ar), `notifier`, `service`
(watchlist `["Test Sanctioned Person"]`). Hidden tests run inside a copy of the learner's repo, so they can use these fixtures.

The suite passes under `TZ=Asia/Tokyo`, `TZ=America/Los_Angeles`, any `PYTHONHASHSEED`, in reverse file order and file by file (the kit tests check this).
**The base tests that a seed may break:** the four Qatar-midnight tests in `tests/test_limits.py` (see m06 in section 8).

## 4. Register of quirks, smells and gaps

Never fix these by accident and never contradict them. Each line says what it is, an example that a kit test (`tests/test_base_notes.py`) executes, and who may use it.
"Visible" means the code or docs say so openly (the learner can find it).

### Legacy ledger (`src/remit/ledger.py`, module docstring lists Q-LED-1..4)

| Id | What | Example | Suggested use |
|---|---|---|---|
| **Q-LED-1** | The partner's 30% share of the fee is rounded **half-even**; every other rounding in Remit is half-up. Income is `fee - partner`. | Fee 10.15, send 500.00: debit `CUSTOMER:C1` 510.15; credit `PAYOUT_CLEARING` 500.00, `FEE_INCOME` 7.11, `PARTNER_PAYABLE` 3.04 (half-up would give 3.05 / 7.10). | m07 characterization |
| **Q-LED-2** | `balance(account)` of an unknown account **creates** it with `Decimal("0")`, so reading changes `accounts()`. | `balance("NOPE")` returns `Decimal('0')` and `"NOPE" in accounts()` afterwards. | m07 |
| **Q-LED-3** | All state is module-level (`_BALANCES`, `_JOURNAL`) and shared; ids and timestamps come from najmkit's **global** generator and **global** clock; `post_transfer` raises `DuplicatePosting` for a transfer id seen since `reset()`. | Two transfers accumulate; `reset()` empties; entries' `entry_id` is `JNL-000001`... under `SequentialIds`; `posted_at` is the global clock. | m07 (the refactor target) |
| **Q-LED-4** | Balances are bare `Decimal`, no currency; only QAR is accepted. Credits minus debits, so a customer account is negative after sending. Zero-amount legs are not posted. | `post_transfer` with an EGP `Money` raises `CurrencyMismatch`. | m07 |

### Legacy screening (`src/remit/screening.py`, docstring lists Q-SCR-1..4)

| Id | What | Example (default threshold 100) |
|---|---|---|
| **Q-SCR-1** | Tokens shorter than 5 characters must match exactly; longer ones need >= 85% similarity (integer arithmetic on difflib blocks). | `screen("Omar Khan", ["Omer Khan"]).hit` is False; `screen("Hasan", ["Hassan"]).hit` is True. |
| **Q-SCR-2** | A single-token name never matches a multi-token entry (nor the reverse). | `screen("Madonna", ["Madonna Ciccone"]).hit` is False; `screen("Madonna", ["Madonna"]).hit` is True. Every token of the shorter name must match for a hit; order does not matter; a 2-token name matches a 3-token entry that contains both. |
| **Q-SCR-3** | Only the first 4 tokens (after dropping particles `al el bin ibn bint ben`) are compared. | `screen("A B C D X", ["A B C D Y"]).hit` is True. |
| **Q-SCR-4** | Arabic words not in `NAME_TABLE` become consonant skeletons (`"حمزة"` -> `"hmza"`); characters that are not Latin/Arabic letters or digits are separators, so a name in another script has no tokens and never matches. | `tokens("حمزة") == ["hmza"]`, `screen("حمزة", ["Hamza"]).hit` is False, `tokens("张伟") == []`. |

Also true: names are screened after accent stripping (`"Elena Marković"` matches `Elena Markovic Petrov`); `"كريم القادري"` matches `Karim Nasser Al-Qadiri`; the service screens the sender **and** the recipient.

### Store, service, docs, imperfections and deliberate gaps

| Id | What | Where / example |
|---|---|---|
| **S-STORE-1** | `Store.search_by_name` builds SQL with `str.format` (the only non-parameterised query). A single quote raises `sqlite3.OperationalError`; a crafted fragment changes the query. The docstring says KNOWN SMELL. | `search_by_name("O'B")` raises; `search_by_name("zzz%' OR name LIKE '%")` returns every customer. Suggested: m05/m08/m11 reviews. |
| **D-ARCH-1** | `docs/ARCHITECTURE.md` still describes a `risk.py` module (section 1 table and section 6) that no longer exists; screening is `screening.py`, limits are `limits.py`, and `service.py` calls them separately. **Left on purpose** (confirmed): it is the docs-versus-code seed for m02, m06, m11, m12, m13 and m14. | `src/remit/risk.py` does not exist. Trap for m02 (pointers must resolve), m06/m11 (docs vs code). |
| **D-ARCH-2** | The architecture doc's limits section (section 5) states an old rule: two KYC tiers (T1 QAR 5,000/day, T2 QAR 25,000/day) and **no monthly limit**. The code has three tiers and monthly limits (generated table above). Sections 1, 5 and 6 are the stale ones; a ticket that touches limits or screening makes more of the document untrue (m14). | Everything else in the doc is true, including "a day is a Qatar calendar day" and "one dirham (0.01 QAR)" (the Qatari riyal has 100 dirhams). |
| **D-SVC-1** | `send` is not atomic after the ledger: if `store.save_transfer` raises, the ledger posting stays (documented in the module docstring and ARCHITECTURE section 11). | Test: a store whose `save_transfer` raises leaves `ledger.journal()` non-empty. |
| **I-SVC-1** | `RemitService.send` is one long function (89 lines) with numbered step comments. | Natural refactoring target; do not split it in the base. |
| **I-SCR-1** | A stale `TODO(farid, 2022)` in `screening.py` (move the watchlist to a vendor feed). | The only stale TODO. |
| **I-NOTIFY-1** | Arabic messages embed Latin names and ids unchanged, without bidi isolation marks. | Fine for tests; a possible m04 Arabic consideration. |
| **I-LIM-1** | `send` loads a customer's **entire** transfer history to compute limits (no `since` filter). | Correct, just not optimised. |
| **G-BDT** | The BDT corridor is deliberately absent: no `QAR-BDT` in `CORRIDORS`, `DEFAULT_MID_RATES`, `CORRIDOR_MARGINS`, no fee schedule for it. `BDT` **is** a `Money` currency and has an Arabic name in `CURRENCY_NAMES_AR`. | m14 adds all of it. The m14 ticket must state the rate, margin, fee tier and min/max (the tests cannot guess them). |
| **G-WARN** | No `limit_warning` template and no 80% logic. | m04 adds both. |
| **G-LOYALTY** | `Customer.loyalty_tier` (`none/silver/gold`) exists but nothing uses it; no discount in `fees`. | m05's agent branch adds one (badly). |
| **G-V2** | Only najmkit v1 exists. | m07 defines v2 in its own assets. |
| **G-ADR** | No `docs/adr/`, no `specs/`, no `.claude/`, no `CLAUDE.md`, no `AGENTS.md`, no `CODEOWNERS`, no pull-request template, no `requirements.txt`; CI runs only `pytest -q`. A team-practice lab (m12) must state this to the learner. | Labs create what they need. |

**Found by the dry-runs** (each executed by `tests/test_base_notes.py`; the base is frozen, so labs work around them and lessons may use them):

| Id | What | Example |
|---|---|---|
| **Q-SVC-1** | A `Quote` is not bound to a customer, and `send(quote=q)` uses `quote.fee` and `quote.fx` unchanged. A quote shown to one customer can be sent by another (matters once fees depend on the customer, m05's loyalty discount). | `quote = service.quote(...)`; `send("C1", ..., quote=quote)` and `send("C2", ..., quote=quote)` both succeed with `quote.fee`. |
| **Q-CLI-1** | `cli.main` opens `Store(':memory:' if args.command == 'quote' else config.db_path)`: a new command that reads no data needs a third edit away from the lab markers, or it creates a database file. | `main(["quote", ...], environ={"REMIT_DB": path})` creates no file; `history` does. |
| **Q-CLI-2** | argparse `--help` prints to the real `sys.stdout`, not the injected `out`, and `main` swallows `SystemExit` and returns 0. Tests of `--help` need `capsys`. | `main(["--help"], out=buf)` returns 0 with `buf` empty. |
| **I-NAJMKIT-1** | `najmkit` docstrings promise more than the code checks: `ids.new_id` says 2 to 5 upper-case letters but the regex ends in `$`, so `new_id("TRF\n")` works; `audit.log_event` calls `event` reserved but `event=` never reaches that check (Python raises `TypeError` first; `ts=` does raise `ValueError`); `FixedClock.advance` is typed `**delta: int` and "forward" but accepts floats and negative values; `use_generator` takes a "callable returning str" and checks nothing. m11's "known problems" section can find these; its grader names only one. | `advance(seconds=-5)` moves back 5 seconds; `use_generator(lambda: 42)` then `new_id("TRF")` is `TRF-42`. |
| **G-V2-DOC** | `docs/najmkit.md` describes version 1.3.0 / API v1. Labs that seed najmkit 2 vendor 2.0.0 and say so in their ticket (m07). | |

## 5. Determinism: how time and ids are injected

* **Time.** Never call `datetime.now()` in a seed, a hidden test or a grader. `RemitService` gets a clock object; the tests use `FixedClock("2026-03-02T09:00:00+00:00")`
  and `clock.advance(seconds=61)`. `fx_quote(send, corridor, provider, now)` and `check_limits(tier, history, amount, now)` take `now` as an argument.
  `ledger.py` uses the **global** clock (`najmkit.clock.set_clock(FixedClock(...))`); the base `conftest.py` installs one for every test. All times are timezone-aware UTC;
  naive datetimes raise `ValueError`.
* **Ids.** `najmkit.ids.use_generator(SequentialIds())` makes `new_id("TRF")` return `TRF-000001`, `TRF-000002`... The base `conftest.py` does this for every test. In a seed,
  construct objects with explicit ids.
* **Audit.** `najmkit.audit.configure(path)` (or `NAJMKIT_AUDIT_LOG`) selects the JSON-lines file; with no path nothing is written. Keys are sorted, so lines are reproducible.
* **Kit commits** (`Initial state`, `Lab starting state`, anything made with `gitutil.commit_all`) use a fixed author (`Najm Payments Platform`) and date, so a started lab is byte-for-byte the same every time.
  Pass `author=` / `date=` to imitate a colleague or an agent.
* **Graders** run pytest and mutants in a scrubbed environment (`runner.clean_env`: no `REMIT_*`, `NAJMKIT_*`, `GIT_*`, `PYTEST_*`, `PYTHONPATH`; bytecode off; plugin autoload off; `-p no:randomly`).
  Note that this machine's venv has `pytest-randomly` installed: the learner's own `pytest -q` shuffles test order, and the base suite is order independent.
* No sleeping and no network anywhere. A lab (start, grade, solve, grade) must finish in **under 20 seconds** (the generic test allows 30).

## 6. How to write a lab

Copy `ailab/labs/m00_first_fix/` and read `lab.py` there first: it is the heavily commented model.

**Layout:** `labs/mNN_slug/{lab.py, task.md, assets/, hidden/, solution/}`; `LAB = Lab(id="mNN", title=..., lesson="N.2", needs_agent=..., seed=..., grade=..., solve=...)`.
The folder prefix must equal `LAB.id`. Paths for `task.md`, `assets/`, `solution/`, `hidden/` default to the lab folder (`lab.task_file`, `lab.assets_dir`, `lab.solution_dir`, `lab.hidden_dir`).

**seed(work)** edits the fresh repo. Use `framework.edit_file(work, rel, old, new, count=1)` (strict: fails if `old` does not occur exactly `count` times, so a changed base fails loudly),
`write_file`, `remove_file`, `read_file`, `gitutil.apply_patch`. Do **not** commit the final state: the framework commits "Lab starting state" and tags `lab-start` after copying `assets/` to `lab-assets/` and writing `TASK.md`.
If your lab needs history or branches (m05, m10), make them in the seed with `gitutil.create_branch`, `gitutil.commit_all(work, msg, author=(name, email), date=...)`, `gitutil.checkout(work, "main")`, `gitutil.merge`, and end on the branch the learner
should start on. Extra tags are fine (`gitutil.tag(work, "agent-branch-start", ref="agent/loyalty-discount")`) and every check helper takes `since=` to use them. For a lab that wants the learner to start with a good
project memory call `framework.add_reference_memory(work)` in the seed (copies `labs/m02_*/solution/CLAUDE.md` to `CLAUDE.md`; a no-op until m02 exists). Never edit `ailab/base/remit/`.

**grade(work)** returns a list of `Check(name, ok, detail, hint, required)`. Build it from `ailab.checks` (section 7): `tests_pass`, `hidden_tests_pass`, `tests_fail_on_starter`, `mutation_check`, `files_changed_within`,
`files_unchanged`, `diff_size`, `commit_count`, `conventional_commits`, `all_committed`, `no_secrets`, `forbid_patterns`, `json_check`, `sections_check`, `files_exist`, `python_compiles`, `public_api`.
Rules: (1) never modify `work`; (2) run learner code only in a subprocess with a timeout (the helpers do; they work on a throw-away copy); (3) check **behaviour through the public interface the task names**, not your solution's internals;
(4) `detail` says what was found, `hint` nudges, neither reveals hidden expected values (`hidden_tests_pass` shows failing test names, so name hidden tests as hints; `reveal="count"` hides them); (5) check names are unique and stable;
(6) mark nice-to-have checks `required=False`; (7) be deterministic: grading twice gives the same result.

**Hidden tests** live in `labs/mNN_slug/hidden/test_mNN_*.py` (unique file names). `checks.hidden_tests_pass(work, HERE / "hidden")` copies them into `tests/_hidden/` of a copy of the learner's repo and runs only them, with the learner's `src` on
`PYTHONPATH`, so they can import `remit` and use the repo's fixtures (`service`, `store`, `customers`, `clock`, ...). A `conftest.py` next to them applies to them only. They are not secret from someone who reads the kit's source; the course says
the grader is an honour-system check (README).

**solve(work)** must leave `grade` passing, commits included. Keep the solution's data in `solution/` (a patch, files, a commit message) and apply it in code.

**Tests for your lab:** `tests/test_labs_mNN.py`. `tests/test_labs_generic.py` already runs, per lab: well-formedness, start state, starter fails, grading is deterministic and does not touch the work dir, solution passes, the secret scanner finds nothing in the lab's seeds, assets and reference solution, no commit sits on another branch at the start, the lab is fast.
Add **negative tests** for the wrong answers people really produce (see `tests/test_labs_m00.py`): special-casing the example, editing the tests, unrelated or oversized changes, bad commit messages, no commit or too many, floats for money, secrets, a regression
test that passes on the starter. A grader must accept **any sound solution**, so also write at least one *alternative correct solution* test that does the work differently from `solve`.

**Ticket ids** already used (do not reuse one for a different ticket; a lesson may mention another module's ticket on purpose): 0: 209, 212, 244 · 1: 224, 239 · 2: 251, 252 · 3: 212, 288, 299, 330, 341, 342, 343 · 4: 269, 318 · 5: 227, 229, 233, 238 · 6: 231 · 7: 372 · 8: 258 · 9: 285 · 10: 350, 361 (and 346, 347 in the lesson 10.1 story) · 11: 393 · 12: 244 (the lesson 0.3 ticket again), 262 · 14: 414.

**Decision on `.claude/`** (asked by m10): `TOOL_NOISE` ignores only `.claude/settings.local.json` and `.claude/worktrees/**`. Other `.claude/` files (`settings.json`, `agents/`, `commands/`, `skills/`, `hooks/`) are the learner's work and count as changes, so a lab that teaches them allows `.claude/**` in its own `files_changed_within` list (m04, m09 and m10 do), and a lab that does not teach them (m00, m02) lets the scope check fail them.

**Task text (`task.md`)**: the ticket as Hessa would write it; start with a `# ` heading; say what "done" means; do not mention hidden files or absolute paths. AUTHORING.md rule 10: an independent learner dry-run will follow only the lesson and the task.
**Every situation the grader judges must be stated in `task.md`** (learned from the dry-runs): each rule it enforces, each shape it accepts (the commit count and header, the files you may touch, the exact names of files and headings), and each edge it treats as wrong. If a learner can fail a check only by guessing a rule that the ticket never states, the ticket is incomplete, not the learner. The lesson may add detail, never rules. Lessons embed `task.md` word for word in a `text` block, so edit both together.

**Lesson code blocks** that show a kit file begin with `# ailab/<path relative to ainative/ailab>` and must equal the file; `python3 ailab/check_blocks.py` (from `ainative/`) checks it.

### 6.1 Running learner code and learner scripts from a grader

Never `import` or `exec` anything the learner wrote in the grader's process. Use a subprocess, always with a timeout, on a **copy** of the work directory:

```python
from ailab import checks, runner

with checks.work_copy(work) as root:                                   # a throw-away copy, deleted afterwards
    env = runner.clean_env(pythonpath=[root / "src"],                  # scrubbed environment, PYTHONPATH=<copy>/src
                           extra={"PATH": f"{stub_dir}{os.pathsep}{os.environ['PATH']}"})   # e.g. put the `claude` stub first
    result = runner.run([sys.executable, "scripts/triage.py", "--limit", "5"], cwd=root, env=env, timeout=10,
                        input=json_text)                               # `input` is written to the script's stdin
    # result.returncode, result.stdout, result.stderr, result.timed_out (the whole process group is killed on timeout)
```

For a hook script that reads JSON on stdin and signals with its exit code (m08, m09), call it once per sample document and compare `returncode` (and stderr) with the expected value.
For pytest-style checks use `checks.run_pytest` / `run_hidden_pytest` / `tests_pass` / `hidden_tests_pass`; they do this for you.

### 6.2 Reference: helper behaviour worth knowing

* "Changed" = compared with the `lab-start` tag: committed, staged, unstaged **and untracked** files; `TOOL_NOISE` is ignored by default: `.claude/settings.local.json`, `.claude/worktrees/**`, `.aider*`, `.DS_Store`, `.idea/**`, `.vscode/**`, `__pycache__`, `*.pyc`, `.pytest_cache`, and what other agent tools write on their own (`.cursor/**`, `.cursorrules`, `.windsurf/**`, `.codex/**`, `.gemini/**`, `GEMINI.md`, `.github/copilot-instructions.md`). `CLAUDE.md`, `AGENTS.md` and the rest of `.claude/` are **not** noise: labs ask for them.
* `conventional_commits` enforces CONTRIBUTING.md: `type(scope): subject`, scope required (one lower-case word for the area changed; CONTRIBUTING.md gives examples, not a closed list), types `feat fix docs test refactor perf chore ci build revert`, optional `!`, no trailing full stop, header at most 72 characters; merge commits are skipped.
* **Default hints say what is true after a commit exists.** A bad message on the latest commit: `git commit --amend`; on an earlier one: `git reset --soft lab-start` and commit again. Undoing an unrelated change that is already committed: `git restore --source=lab-start --staged --worktree -- <file>` (for an added file `git rm -f <file>`), then commit the undo (`checks.UNDO_HINT`). Too many commits: `git reset --soft lab-start` and commit again; too few: `git reset lab-start`, then commit in pieces. **No default hint recommends an interactive rebase.** When the commits a check wants sit on another local branch, the hint names it and says `git switch <branch>` (`gitutil.commits_elsewhere`). File lists in details show up to twelve names (`checks.FILE_LIST_LIMIT`); lists of test names stay at four. `tests_pass`'s default hint also says that a test can pass in your shell and fail in the grader's clean copy (no `.git`, no virtual environment, none of your exported variables) and that the time limit is 60 seconds by default.
* `diff_size` counts lines added plus lines deleted (`git diff --numstat` against the tag plus all lines of untracked text files). A one-word fix is 2. A size limit alone cannot tell a one-word fix from an unrelated edit of a few lines, so **m00 allows at most 6 changed lines and also requires the file to equal the starter with only the misspelling corrected** (`checks_m00`): do not read the 6 as "a little slack" for the learner.
* `no_secrets` scans added lines (or everything with `scan="all"`) and commit messages for AWS/GitHub/Slack/`sk-`/`sk_live_` keys, private key blocks, bearer tokens, `name = "value"` credentials, **unquoted `NAME=value` lines** for names containing SECRET, TOKEN, PASSWORD, API_KEY or PRIVATE_KEY (value of 12 or more characters, no spaces around `=`; `password=hunter2hunter2` in a Markdown note counts) and **Qatar IBAN-like strings** (`QA`, two digits, 23 to 27 letters or digits, compact or in groups of four). Placeholders (`changeme`, `your-...`, `example`, `${...}`, `$VAR`, `<...>`, `xxxx`, `os.environ`), harmless names (`token_url`, `password_file`, `max_tokens`) and code that names a variable (`api_key=settings.api_key`) are ignored; it reports the rule and file, never the secret. Git-ignored files such as `.env` are not scanned (they never reach a commit).
* `run_pytest` / `tests_pass` / `hidden_tests_pass` / `mutants_killed` run **`python -P -m pytest`** in a throw-away copy: the working directory is not put on `sys.path`, exactly like the `pytest -q` that CI runs (CONTRIBUTING.md), so `from tests.helpers import x` fails here as it fails in CI (Python 3.11 or newer).
* `mutants_killed(work, mutants, test_paths=None)` copies the repo, checks that the learner's tests pass on the untouched copy (`baseline_ok`), applies each `(file, old, new)` / `Mutant` in turn and counts those that make the tests fail, error or hang. Default tests: the test files the learner added or changed (`new_test_files`).
  Mutants must name **behaviour** in `description` (shown when they survive). Mutating the learner's own new code is unreliable (their structure differs): prefer `tests_fail_on_starter` (revert non-test files to `lab-start`, run the learner's new tests, they must fail) for "would the tests catch the feature being absent".
* `run_pytest`/`run_hidden_pytest` always work on a copy and return a `PytestResult` (`passed/failed/errors`, `failures`, `timed_out`); no result is "ok" unless at least one test ran.
* `validate(data, schema)` supports `type enum const required properties additionalProperties(false) items minItems maxItems minLength maxLength pattern minimum maximum`.
* `markdown_sections(path)` maps normalised heading -> body (code fences respected; repeats get ` #2`); `sections_check` wraps it.
* `public_api(work, "src")` lists public functions/classes/methods by AST (nothing is imported): the tool for "every function the docs claim exists" (m11).

## 7. The framework API (generated)

<!-- BEGIN GENERATED: kit_api -->
```text
# ailab.framework
LAB_START_TAG = 'lab-start'
class LabError(Exception)
class Check  # dataclass
    name: str
    ok: bool
    detail: str = ''
    hint: str = ''
    required: bool = True
class Lab  # dataclass
    id: str
    title: str
    lesson: str
    needs_agent: bool
    seed: Callable[[Path], None]
    grade: Callable[[Path], list[Check]]
    solve: Callable[[Path], None]
    task_path: Path | None = None
    assets_path: Path | None = None
    home: Path | None = None
    extra: dict[str, object] = <factory>
    .task_file  # property -> Path
    .assets_dir  # property -> Path | None
    .solution_dir  # property -> Path
    .hidden_dir  # property -> Path
class LabEntry  # dataclass
    dirname: str
    lab: Lab | None = None
    error: str | None = None
    .id  # property -> str
    .broken  # property -> bool
def lab_dirnames() -> list[str]
def normalise_id(text: str) -> str
def find_dirname(lab_id: str) -> str
def load_entry(dirname: str) -> LabEntry
def discover() -> list[LabEntry]
def load_lab(lab_id: str) -> Lab
def read_file(work: Path, rel: str) -> str
def write_file(work: Path, rel: str, text: str) -> Path
def edit_file(work: Path, rel: str, old: str, new: str, *, count: int = 1) -> None
def remove_file(work: Path, rel: str) -> None
def add_reference_memory(work: Path) -> bool
def start_lab(lab: Lab, dest: Path | str) -> Path
def check_work_dir(work: Path | str) -> Path
def started_lab_id(work: Path) -> str | None
def grade_lab(lab: Lab, work: Path | str, *, catch: bool = True) -> list[Check]
def passed(checks: list[Check]) -> bool
def solve_lab(lab: Lab, work: Path | str, *, force: bool = False) -> None
def doctor_checks(directory: Path | str | None = None) -> list[Check]

# ailab.gitutil
TAG_START = 'lab-start'
TOOL_NOISE = ('.claude/settings.local.json', '.claude/worktrees/**', '.aider*', '.DS_Store', '.idea/**', '.vsc...
KIT_AUTHOR = ('Najm Payments Platform', 'payments-platform@najm.example')
KIT_DATE = '2026-03-02T08:00:00+00:00'
class GitError(RuntimeError)
class Commit  # dataclass
    sha: str
    subject: str
    body: str
    author_name: str
    author_email: str
    date: str
    parents: list[str] = <factory>
    .message  # property -> str
    .is_merge  # property -> bool
class DiffStat  # dataclass
    files: list[str]
    added: int
    deleted: int
    .total  # property -> int
    .n_files  # property -> int
def git(work: Path | str, *args: str, check: bool = True, env: dict[str, str] | None = None, input: str | None = None, timeout: float = 60.0) -> runner.RunResult
def out(work: Path | str, *args: str, check: bool = True) -> str
def init_repo(work: Path | str, branch: str = 'main') -> None
def ensure_identity(work: Path | str) -> bool
def set_config(work: Path | str, key: str, value: str) -> None
def get_config(work: Path | str, key: str) -> str | None
def add_local_excludes(work: Path | str, patterns: Iterable[str]) -> None
def commit_all(work: Path | str, message: str, *, allow_empty: bool = False, force: Sequence[str] = (), author: tuple[str, str] | None = None, date: str | None = None) -> str
def tag(work: Path | str, name: str, ref: str = 'HEAD', *, force: bool = False) -> None
def head(work: Path | str) -> str
def rev_parse(work: Path | str, ref: str) -> str | None
def has_ref(work: Path | str, ref: str) -> bool
def current_branch(work: Path | str) -> str
def branches(work: Path | str) -> list[str]
def create_branch(work: Path | str, name: str, *, checkout: bool = True, start: str = 'HEAD') -> None
def checkout(work: Path | str, ref: str) -> None
def merge(work: Path | str, branch: str, *, message: str | None = None, no_ff: bool = False, author: tuple[str, str] | None = None, date: str | None = None, check: bool = True) -> runner.RunResult
def apply_patch(work: Path | str, patch: str | Path) -> None
def glob_match(path: str, patterns: Iterable[str]) -> bool
def changed_status(work: Path | str, since: str = 'lab-start', *, include_untracked: bool = True, ignore: Sequence[str] = TOOL_NOISE) -> dict[str, str]
def changed_files(work: Path | str, since: str = 'lab-start', *, include_untracked: bool = True, ignore: Sequence[str] = TOOL_NOISE) -> list[str]
def diff_numstat(work: Path | str, since: str = 'lab-start', *, include_untracked: bool = True, ignore: Sequence[str] = TOOL_NOISE) -> DiffStat
def commits_elsewhere(work: Path | str, since: str = 'lab-start') -> list[tuple[str, int]]
def commits_since(work: Path | str, since: str = 'lab-start', ref: str = 'HEAD', *, first_parent: bool = False, no_merges: bool = False) -> list[Commit]
def status_porcelain(work: Path | str, *, ignore: Sequence[str] = TOOL_NOISE) -> list[str]
def is_clean(work: Path | str, *, ignore: Sequence[str] = TOOL_NOISE) -> bool
def file_at(work: Path | str, ref: str, path: str) -> str | None
def show_bytes(work: Path | str, ref: str, path: str) -> bytes | None
def is_ancestor(work: Path | str, ancestor: str, descendant: str = 'HEAD') -> bool
def merged_branches(work: Path | str, into: str = 'main', *, exclude: Sequence[str] = ('main', 'master')) -> list[str]
def is_git_repo(work: Path | str) -> bool

# ailab.checks
CC_TYPES = ('feat', 'fix', 'docs', 'test', 'refactor', 'perf', 'chore', 'ci', 'build', 'revert')
def plural(n: int, word: str) -> str
class PytestResult  # dataclass
    returncode: int
    passed: int = 0
    failed: int = 0
    errors: int = 0
    skipped: int = 0
    failures: list[str] = <factory>
    timed_out: bool = False
    duration: float = 0.0
    output: str = ''
    .total  # property -> int
    .ok  # property -> bool
    .failure_names  # property -> list[str]
    def summary() -> str
def copy_work(work: Path | str, dest: Path | str | None = None) -> Path
class work_copy(work: Path | str)
def run_pytest(work: Path | str, paths: Sequence[str] = ('tests',), *, timeout: float = 60.0, args: Sequence[str] = (), extra_env: dict[str, str] | None = None) -> PytestResult
def run_hidden_pytest(work: Path | str, hidden: Path | str | Sequence[Path | str], *, timeout: float = 60.0, args: Sequence[str] = (), extra_env: dict[str, str] | None = None) -> PytestResult
def tests_pass_hint(timeout: float = 60.0) -> str
def tests_pass(work: Path | str, paths: Sequence[str] = ('tests',), *, name: str = 'Your tests pass', timeout: float = 60.0, hint: str | None = None, required: bool = True) -> Check
def hidden_tests_pass(work: Path | str, hidden: Path | str | Sequence[Path | str], *, name: str = 'Acceptance tests pass', reveal: str = 'names', timeout: float = 60.0, hint: str = 'Re-read the ticket: which behaviour does it ask for that you have not checked yourself?', required: bool = True) -> Check
def files_changed_within(work: Path | str, allowed: Sequence[str], *, since: str = 'lab-start', ignore: Sequence[str] = TOOL_NOISE, name: str = 'Only the expected files changed', hint: str = 'Undo what this task does not need. Put the file back as it was at the start: `git restore --source=lab-start --staged --worktree -- <file>` (for a file you added, `git rm -f <file>`, or just delete it if git does not know it yet). If that change was already committed, commit the undo.', require_change: bool = True, required: bool = True) -> Check
def files_unchanged(work: Path | str, protected: Sequence[str], *, since: str = 'lab-start', ignore: Sequence[str] = TOOL_NOISE, name: str = 'Protected files untouched', hint: str = 'Do not edit these files. Put the file back as it was at the start: `git restore --source=lab-start --staged --worktree -- <file>` (for a file you added, `git rm -f <file>`, or just delete it if git does not know it yet). If that change was already committed, commit the undo.', required: bool = True) -> Check
def diff_size(work: Path | str, max_lines: int, *, max_files: int | None = None, min_lines: int = 0, since: str = 'lab-start', ignore: Sequence[str] = TOOL_NOISE, name: str = 'The change is small', hint: str | None = None, required: bool = True) -> Check
def commit_count(work: Path | str, *, exactly: int | None = None, at_least: int | None = None, at_most: int | None = None, since: str = 'lab-start', name: str | None = None, hint: str | None = None, required: bool = True) -> Check
def all_committed(work: Path | str, *, ignore: Sequence[str] = TOOL_NOISE, name: str = 'Everything is committed', required: bool = True) -> Check
def commit_header_problems(header: str, *, types: Sequence[str] = CC_TYPES, require_scope: bool = True, max_header: int = 72) -> list[str]
def conventional_commits(work: Path | str, *, since: str = 'lab-start', require_scope: bool = True, max_header: int = 72, types: Sequence[str] = CC_TYPES, min_commits: int = 1, name: str = 'Commit messages follow CONTRIBUTING.md', hint: str | None = None, required: bool = True) -> Check
def find_secrets(text: str) -> list[tuple[str, int]]
def added_text(work: Path | str, since: str = 'lab-start', ignore: Sequence[str] = TOOL_NOISE) -> dict[str, str]
def no_secrets(work: Path | str, *, since: str = 'lab-start', scan: str = 'added', ignore: Sequence[str] = TOOL_NOISE, name: str = 'No secrets in the change', required: bool = True) -> Check
def forbid_patterns(work: Path | str, patterns: dict[str, str | re.Pattern[str]], *, globs: Sequence[str] = ('**/*.py',), since: str = 'lab-start', ignore: Sequence[str] = TOOL_NOISE, name: str = 'No forbidden constructs in the change', hint: str = "Look at CONTRIBUTING.md: the team's rules say why this is not allowed.", required: bool = True) -> Check
class Mutant  # frozen dataclass
    id: str
    file: str
    old: str
    new: str
    description: str = ''
    count: int = 1
class MutationReport  # dataclass
    baseline_ok: bool
    baseline_summary: str
    killed: list[Mutant] = <factory>
    survived: list[Mutant] = <factory>
    not_applied: list[Mutant] = <factory>
    .total  # property -> int
def as_mutants(mutants: Iterable[Mutant | tuple[str, str, str]]) -> list[Mutant]
def new_test_files(work: Path | str, since: str = 'lab-start', pattern: str = 'tests/**/test_*.py') -> list[str]
def mutants_killed(work: Path | str, mutants: Iterable[Mutant | tuple[str, str, str]], test_paths: Sequence[str] | None = None, *, timeout: float = 30.0) -> MutationReport
def mutation_check(work: Path | str, mutants: Iterable[Mutant | tuple[str, str, str]], test_paths: Sequence[str] | None = None, *, min_killed: int | None = None, name: str = 'Your tests catch real defects', timeout: float = 30.0, hint: str = 'Add assertions that would fail if that behaviour broke: check the exact values, not just that nothing crashed.', required: bool = True) -> Check
def tests_fail_on_starter(work: Path | str, test_paths: Sequence[str] | None = None, *, since: str = 'lab-start', keep: Sequence[str] = ('tests/**',), timeout: float = 60.0, name: str = 'Your new tests fail on the original code', hint: str = 'A test that passes before the fix proves nothing. Make it reproduce the problem first.', required: bool = True) -> Check
def load_json(path: Path | str) -> tuple[Any, str | None]
def get_path(data: Any, path: str, default: Any = None) -> Any
def json_has(data: Any, path: str, *, equals: Any = <unset>, one_of: Iterable[Any] | None = None, type_: type | tuple[type, ...] | None = None, non_empty: bool = False) -> bool
def validate(data: Any, schema: dict[str, Any], path: str = '$') -> list[str]
def json_check(work: Path | str, rel: str, schema: dict[str, Any], *, name: str | None = None, hint: str = 'Fix the file so it matches the structure described in the task.', required: bool = True) -> Check
class Section  # dataclass
    level: int
    title: str
    body: str
def markdown_outline(source: Path | str) -> list[Section]
def markdown_sections(source: Path | str) -> dict[str, str]
def sections_check(work: Path | str, rel: str, required_sections: Sequence[str], *, min_words: int = 5, name: str | None = None, hint: str = 'Use the section headings from the task, and write something under each.', required: bool = True) -> Check
def files_exist(work: Path | str, paths: Sequence[str], *, name: str = 'Expected files exist', hint: str = 'Create the files the task asks for.', required: bool = True) -> Check
def python_compiles(work: Path | str, paths: Sequence[str] = ('src', 'tests'), *, name: str = 'Python files compile', required: bool = True) -> Check
def public_api(work: Path | str, root: str = 'src') -> dict[str, str]

# ailab.runner
class RunResult  # dataclass
    cmd: list[str]
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool
    duration: float
    .ok  # property -> bool
    .output  # property -> str
def clean_env(pythonpath: Iterable[str | os.PathLike[str]] = (), extra: Mapping[str, str] | None = None, *, keep_git: bool = False) -> dict[str, str]
def run(cmd: Sequence[str | os.PathLike[str]], *, cwd: str | os.PathLike[str] | None = None, timeout: float = 60.0, env: Mapping[str, str] | None = None, input: str | None = None) -> RunResult
def run_python(args: Sequence[str | os.PathLike[str]], *, cwd: str | os.PathLike[str] | None = None, pythonpath: Iterable[str | os.PathLike[str]] = (), timeout: float = 60.0, extra_env: Mapping[str, str] | None = None, input: str | None = None) -> RunResult
def which(program: str) -> str | None

```
<!-- END GENERATED: kit_api -->

## 8. What each planned lab needs from the base (checked against the code)

Legend: **OK** = supported as is; **NOTE** = supported, but know this; **GAP** = something is missing or conflicts (see section 9). The base is frozen: where a lab needs a change, the lab's seed makes it.

| Lab | Needs | Status |
|---|---|---|
| **m00** | A typo in an English template that a test asserts. | **OK, built.** The seed changes `received` to `recieved` in `notify.TEMPLATES["transfer_sent"]["en"]`; `test_transfer_sent_in_english` and `test_customer_send_and_history_share_a_database_file` then fail. |
| **m01** | Constructed sessions that refer to real repo files and commands; a "hallucinated API" for najmkit. | **OK.** Plausible-but-wrong najmkit names that do **not** exist in v1: `ids.generate`, `ids.new_uuid`, `clock.utcnow`, `clock.freeze`, `audit.write`, `audit.record`. Real file names and commands are in section 3. |
| **m02** | Exact working commands (executed); conventions; architecture pointers that resolve; reference memory for later labs. | **NOTE.** `pytest -q` and `pytest -q tests/test_fees.py` work from the repo root with no setup; `python -m remit ...` needs `PYTHONPATH=src` (or `pip install -e .`), so a lint that runs commands must set it. The memory's architecture section copied from `docs/ARCHITECTURE.md` will point at `risk.py` (D-ARCH-1): that is the trap. `framework.add_reference_memory` exists; m02 must ship `solution/CLAUDE.md`. |
| **m03** | Vague tickets with hidden ambiguities: rounding, tier boundary, currency, Arabic. | **OK.** Half-up rounding (money, fee, receive), inclusive tier boundary and min/max, fee never decreasing, express after the cap, QAR-only senders, Arabic digits and currency names (section 3.2). |
| **m04** | 80% daily-limit warning in EN and AR; acceptance tests; mutation-style check; diff size; commit messages. | **OK.** `LimitResult` gives `daily_used/daily_limit/daily_remaining`; the warning belongs after the transfer in `send` (position after = `result.limits.daily_used + amount`); `notify.TEMPLATES` has no `limit_warning`; `format_money/format_number/localize_digits` build Arabic digits; `InMemoryNotifier.sent` and the `service` fixture let hidden tests assert. For the "tests would catch the feature being removed" check use `checks.tests_fail_on_starter` (the learner's code structure is unknown, so fixed-string mutants only work on base code the lab controls). |
| **m05** | A seeded branch `agent/loyalty-discount` with: hallucinated dependency, swallowed exception, float money, a test that asserts nothing, an over-mocked test, a hard-coded key, scope creep with a deleted test; then a fix. | **OK.** `Customer.loyalty_tier` exists and `fees.quote_fee` is the natural hook; `pyproject.toml` has `dependencies = []` (add the invented package there and import it); `.env.example` and CONTRIBUTING state the secret/float rules; plenty of real tests to delete (e.g. `test_a_higher_amount_never_costs_less`); `service._notify` has a *correct* narrow `except NotificationError` to contrast with a seeded `except Exception: pass`. Seed with `gitutil.create_branch` + `commit_all(author=...)` and tag the branch tip so graders can use `since=`. Static checks: `checks.forbid_patterns` and `checks.find_secrets`. |
| **m06** | A limit applied at the wrong midnight (UTC instead of Qatar); `lab-assets/prod.log`; regression test; root-cause note; minimal patch; onboarding doc. | **NOTE + GAP.** The bug is a two-place seed: `local = to_local(now)` occurs in both `day_window` and `month_window` (use `edit_file(..., count=2)`) and, to hide it from the visible suite, **four tests in `tests/test_limits.py` fail once it is seeded** (`test_the_day_ends_at_midnight_in_qatar_not_in_utc`, `test_a_transfer_after_qatar_midnight_but_before_utc_midnight_belongs_to_the_new_day`, `test_the_month_changes_at_midnight_in_qatar`, `test_windows_are_local_calendar_windows`): the seed must remove them or the lab has no mystery. A realistic `prod.log` can use the audit format (`{"event": "transfer.rejected", "reason": "limit_exceeded", "ts": ..., ...}` with sorted keys) with timestamps between 21:00 and 24:00 UTC. The onboarding doc name collides with `docs/TOUR.md` (section 9). |
| **m07** | Characterization tests for `ledger` (quirks included), refactor away the global state, migrate najmkit v1 to v2. | **NOTE + GAP.** Q-LED-1..4 are the material. `ledger` is imported as a module by `service.py` and `tests/conftest.py` (`ledger.reset()`), and `RemitService` has no ledger parameter, so the lab must specify the post-refactor interface. najmkit v1 is used in nine places plus the tests (section 3.3); v2 must be defined by the lab (assets). See section 9. |
| **m08** | Hook guard, permissions, dependency check, injected README. | **OK.** Dependency data to check: `pyproject.toml` (`dependencies = []`, `dev = ["pytest"]`) and `.github/workflows/ci.yml` (`pip install pytest`). `.gitignore` already ignores `.env`, `*.db`, `audit.jsonl`, `*.log`. Nothing else is needed from the base. |
| **m09** | Review command/skill, read-only subagent, post-edit hook, headless script against the `claude` stub. | **OK, built.** `ailab/stubs/claude` exists: a deterministic stand-in for the `claude` CLI's print mode (`-p`, `--output-format json`, `--max-turns`, exit codes), driven by `[stub:...]` markers in the ticket text and a keyword table; it is not Claude Code and calls no model. The base needs nothing: a post-edit hook can run `pytest -q -x` or `python -m compileall`. |
| **m10** | Four-part change across branches/worktrees, planted conflict, merged `main` passes hidden tests, at least three branches merged, readable history. | **OK.** Independent areas exist (notify templates, fees, limits, docs, CLI). Helpers: `gitutil.create_branch/checkout/merge/merged_branches/is_ancestor/commits_since(first_parent=, no_merges=)`. Plant the conflict in the seed by committing a change to `main` that touches the same lines a branch task will touch. Note `commits_since` is per `HEAD`; worktrees share the repository, so branches and merges are visible from the main work dir. |
| **m11** | ADR with a critic, najmkit docs verified against code, postmortem checked against `incident.json`. | **NOTE.** `docs/najmkit.md` already exists and is accurate; the lab's seed must delete or rename it, or ask for a different file. `checks.public_api` lists real functions for verification. The architecture doc's stale parts (D-ARCH-1/2) give an ADR critic something real to find. No `docs/adr/` folder exists. |
| **m12, m13** | A playbook; a personal eval with runnable checks. | **OK.** CONTRIBUTING.md holds the real rules to refer to; `pytest -q` and `python -m remit quote QAR 500 INR` (with `PYTHONPATH=src`) are runnable checks. |
| **m14** | A BDT corridor with its own fee tier and limits through the full cycle. | **NOTE + GAP.** Absent on purpose (G-BDT): corridor, fee schedule, rate, margin. Present: `BDT` in `Money` and its Arabic currency name. There is no per-corridor *daily/monthly* limit in the code: "limits" can only mean the corridor's `min_send`/`max_send` unless the ticket asks for a new feature. Adding a corridor touches `corridors.py`, `fees.py` (`SCHEDULES`), `fx.py` (`DEFAULT_MID_RATES`, `CORRIDOR_MARGINS`) and the tests; the CLI picks it up automatically. |

## 9. Open questions for the course owner

1. **`docs/TOUR.md` vs `docs/tour.md` (m06).** The lab plan has the learner write `docs/tour.md`; the base ships `docs/TOUR.md` (as requested). On case-insensitive file systems (macOS and Windows defaults) these are the same file. Suggest m06 uses another name (for example `docs/onboarding.md`), or the base file is renamed.
2. **`ailab/stubs/claude` (m09)**: resolved. It is built (AUTHORING decision 4) and tested in `tests/test_labs_m09.py`.
3. **m06 must neutralise four base tests** (section 8) when it seeds the UTC bug; decide whether the seed deletes them or rewrites them to be loose.
4. **m07's interface.** Decide the post-refactor shape the hidden characterization suite targets (suggestion: `class Ledger` with `post_transfer/balance/accounts/journal`, `RemitService(..., ledger=None)` defaulting to a fresh `Ledger()`, and conftest no longer calling `ledger.reset()`), and whether the learner's
   own characterization tests must run unchanged before and after the refactor (then they must go through an interface that survives).
5. **m11's najmkit docs.** The base already has `docs/najmkit.md`; decide whether the lab removes it in the seed.
6. **m14's "limits".** Decide whether the capstone ticket means per-transfer min/max (supported) or a new corridor-level cap (a new feature the learner builds).
7. **`TASK.md` and `lab-assets/` are committed in the starting commit** (rather than left untracked as the original brief described). This keeps `git add -A` and diffs clean for every lab; say if you would rather have them untracked and excluded.
8. **The kit cannot stop a learner from reading `hidden/`** (it is in the same repository). The README says so; if the course wants a stronger guarantee, hidden tests would have to be served separately.

## 10. Shared-kit findings from the dry-runs: fixed centrally, and left alone on purpose

Fifteen lab writers and fifteen learner dry-runs reported problems that no single lab may fix. The central pass fixed these:

| Finding | Fix |
|---|---|
| `ailab start` printed a grade command that fails outside the `ailab` folder | `start` and `solve` print `PYTHONPATH=<kit folder> python -m ailab grade <id> --dir <work dir>` (absolute paths, a PowerShell form on Windows) and say where the work directory is (`cli.grade_command`); README and lesson 0.2 show it |
| Hints wrong once a commit exists (amend, restore, rebase, other branch) | `checks.COMMIT_FORMAT_HINT`, `checks.UNDO_HINT`, `gitutil.commits_elsewhere`; no default hint recommends an interactive rebase (section 6.2) |
| File lists cut at four names | up to twelve for files (`FILE_LIST_LIMIT`); test names stay at four |
| `tests_pass` hint silent about the clean copy and the time limit | new default hint (`tests_pass_hint`) |
| `no_secrets` too narrow | unquoted `NAME=value` lines and Qatar IBAN-like strings; a generic test scans every lab's seeds, assets and reference solutions for false positives |
| `TOOL_NOISE` missed other agent tools' files | `.cursor/`, `.cursorrules`, `.windsurf/`, `.codex/`, `.gemini/`, `GEMINI.md`, `.github/copilot-instructions.md`; never `CLAUDE.md` or `AGENTS.md` |
| `python -m pytest` put the working directory on `sys.path` | the runners use `python -P -m pytest` (kept: the whole suite is green with it) |
| CONTRIBUTING.md: scope list read as closed; "all tests must pass before you commit" against test-first; no named reviewer | rewritten (scope is one lower-case word, examples not a closed list; tests and code are committed together so every commit is green; Tariq or Nada as the second human); a bug fix needs a test unless one already covers it |
| `ledger.py` and `screening.py` docstrings pointed to `KIT_NOTES.md`; README, TOUR and ARCHITECTURE said "no tests" | pointer removed (no line numbers moved); "no dedicated tests, only exercised through `send()`"; m07's stale-document sweep also recognises the new wording |
| Reference `CLAUDE.md` forbade commits and test edits that tickets require | commit only when the task asks, never push or open a pull request unless asked, never weaken, skip or delete a test to get green (a task may ask for a change: say why in the commit body); m04, m07 and m10 tickets and lessons say so |
| Smaller items | `diff_size` hint when nothing changed yet; `all_committed` hint for a second commit; `conventional_commits(hint=...)`; clearer message for a header of the wrong shape; `tests_fail_on_starter` no longer crashes on a nested worktree directory; the quirks register gained Q-SVC-1, Q-CLI-1, Q-CLI-2, I-NAJMKIT-1, G-V2-DOC; ticket ids listed (REMIT-341 and 343 in the 10.1 story became 346 and 347) |

Left alone, with the reason (do not "fix" these without reading it):

| Finding | Why it stays |
|---|---|
| Advisory checks print `[FAIL] ... (advisory)` | a new tag, or a legend line, would change every sample block in every lesson that shows an advisory failure; the lessons and tickets explain the tag |
| "Needs an agent: no" for labs where an agent is recommended (a tri-state) | the line is printed in `start` and shown in lessons, and AUTHORING rule 7 fixes yes/no |
| An installable package or console script; `start --clean` | packaging needs a build step and network; `start --clean` would change the lab lifecycle that m02's tested recipe relies on; the printed `PYTHONPATH` command removes the stumbling block |
| `commit_count` counts merge commits and empty commits | a behaviour change for every lab; the labs that need "exactly one" or real steps have their own checks (m00, m07) |
| `tests_fail_on_starter` counts collection errors as failures | the numbers in sample output would change; m06 and m10 have their own stricter checks |
| Base README: warn that `pip install -e .` and git worktrees mix badly | base text is frozen apart from the changes listed above; lesson 10.2 carries the warning |
| `check_blocks.py` does not map `# lab-assets/...` first lines to a lab | one use (lesson 13.2), already pinned by `tests/test_labs_m13.py` |
| Whether `csvtidy` is unregistered on PyPI (m08) | checked on 2026-10-23: a real, unrelated `csvtidy` (0.1.0) exists and `csvtidy-extras` is unregistered. The lab now says `csvtidy` is a made-up vendor library, a similar real name may exist, and anyone could register `csvtidy-extras` (slopsquatting); the point is that neither name is on the allow-list |
| `/dev/null` was found to be a regular file in the shared sandbox | the machine, not the kit; nothing in the kit relies on it (`GIT_CONFIG_GLOBAL=/dev/null` was removed from m00's tests) |
| "one dirham (0.01 QAR)" in ARCHITECTURE.md | correct: the Qatari riyal has 100 dirhams |
