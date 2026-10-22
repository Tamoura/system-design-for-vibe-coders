#!/usr/bin/env python3
"""Builds lab-assets/prod.log for lab m06 by RUNNING the Remit service against a source tree.

This file is lab-author material, not learner material (it is not copied to the learner's work
directory). The prod.log the learner receives is constructed for teaching: it was produced by
replaying the scripted attempts below through the real ``RemitService`` with a fixed clock, so
every line is exactly what ``najmkit.audit`` would write, and it is consistent with the seeded
bug. It is not a recording of real traffic, and every customer is fictional.

usage:   python make_prod_log.py SRC_DIR [--out FILE]

SRC_DIR is the ``src`` folder of a started m06 lab (the buggy code) or of a fixed one. With the
buggy code the output must equal ``assets/prod.log`` byte for byte (the kit's tests check that);
with the fixed code the output shows what production would have logged without the bug.

The same script, imported as a module, exposes the script of attempts (``ATTEMPTS``), the
customers (``CUSTOMERS``) and the ground truth about who was affected (``WRONGLY_REFUSED``,
``WRONGLY_ALLOWED``) for the grader and the tests.
"""
from __future__ import annotations

import hashlib
import itertools
import sys
from datetime import datetime, timezone
from pathlib import Path

# customer id -> (display name, KYC tier). Names never reach the audit log (the house rule is
# "log identifiers, never names"); the tiers are what lab-assets/kyc_tiers.csv publishes.
CUSTOMERS: dict[str, tuple[str, str]] = {
    # the customers at the heart of the incident
    "C1190": ("Customer 1190", "T1"),
    "C2207": ("Customer 2207", "T1"),
    "C3042": ("Customer 3042", "T1"),
    "C4410": ("Customer 4410", "T2"),
    "C5521": ("Customer 5521", "T1"),
    "C6003": ("Customer 6003", "T1"),
    "C7788": ("Customer 7788", "T1"),
    "C8120": ("Customer 8120", "T1"),
    # customers whose refusals are correct (decoys: they look similar but are right)
    "C9001": ("Customer 9001", "T1"),
    "C9002": ("Customer 9002", "T1"),
    "C9003": ("Customer 9003", "T2"),
    "C9005": ("Customer 9005", "T1"),
    "C9006": ("Customer 9006", "T1"),
    # everyone else: ordinary daytime traffic
    "C1001": ("Customer 1001", "T1"),
    "C1002": ("Customer 1002", "T2"),
    "C1003": ("Customer 1003", "T1"),
    "C1004": ("Customer 1004", "T3"),
    "C1005": ("Customer 1005", "T1"),
    "C1006": ("Customer 1006", "T2"),
    "C1007": ("Customer 1007", "T1"),
    "C1008": ("Customer 1008", "T1"),
    "C1009": ("Customer 1009", "T1"),
    "C1010": ("Customer 1010", "T2"),
    "C1011": ("Customer 1011", "T1"),
    "C1012": ("Customer 1012", "T2"),
    "C1013": ("Customer 1013", "T3"),
    "C1014": ("Customer 1014", "T1"),
    "C1015": ("Customer 1015", "T1"),
    "C1016": ("Customer 1016", "T2"),
    "C1017": ("Customer 1017", "T1"),
    "C1018": ("Customer 1018", "T1"),
    "C1019": ("Customer 1019", "T2"),
    "C1020": ("Customer 1020", "T1"),
    "C1021": ("Customer 1021", "T3"),
    "C1022": ("Customer 1022", "T2"),
    "C1023": ("Customer 1023", "T1"),
    "C1024": ("Customer 1024", "T1"),
}

# The customer who is screened (the recipient name hits the demo watchlist).
SANCTIONED_RECIPIENT = "Test Sanctioned Person"
# The customer whose "transfer sent" message cannot be delivered (noise: notification.failed).
NOTIFICATION_FAILS_FOR = "C1016"

# (day, "HH:MM:SS" UTC, customer id, amount in QAR, receive currency). Days are March 2026:
# 13 = Friday ... 17 = Tuesday. Qatar is UTC+3, so 21:00 UTC is midnight in Doha.
ATTEMPTS: list[tuple[int, str, str, str, str]] = [
    # Friday 13 March
    (13, "06:12:40", "C1001", "400.00", "INR"),
    (13, "06:55:03", "C1002", "1500.00", "PHP"),
    (13, "07:30:18", "C1003", "650.00", "PKR"),
    (13, "08:05:51", "C1004", "5000.00", "INR"),
    (13, "09:20:09", "C1005", "300.00", "EGP"),
    (13, "10:41:27", "C1006", "2500.00", "INR"),
    (13, "11:03:44", "C1002", "800.00", "PHP"),
    (13, "12:15:36", "C1007", "1200.00", "INR"),
    (13, "13:47:02", "C1008", "900.00", "PKR"),
    (13, "14:00:12", "C4410", "6000.00", "INR"),
    (13, "15:22:30", "C1009", "750.00", "PHP"),
    (13, "16:42:07", "C2207", "1200.00", "INR"),
    (13, "17:08:55", "C1010", "1100.00", "EGP"),
    (13, "18:36:20", "C1001", "700.00", "INR"),
    (13, "19:00:10", "C9005", "1900.00", "INR"),
    (13, "19:30:41", "C4410", "3500.00", "INR"),
    (13, "20:30:05", "C9005", "600.00", "INR"),      # correct refusal, an hour before Doha midnight
    (13, "21:10:14", "C9006", "2000.00", "INR"),      # 00:10 on Saturday in Doha: a new day, allowed
    (13, "21:20:33", "C4410", "2000.00", "INR"),      # wrongly refused: it is Saturday in Doha
    (13, "22:00:47", "C9006", "300.00", "INR"),       # correct refusal: Customer 9006 used the whole day
    (13, "22:18:09", "C2207", "1000.00", "INR"),      # wrongly refused: it is Saturday in Doha
    # Saturday 14 March
    (14, "03:05:26", "C2207", "1000.00", "INR"),      # the retry that "worked"
    (14, "06:30:11", "C1011", "500.00", "INR"),
    (14, "07:45:20", "C1012", "2200.00", "PKR"),
    (14, "08:00:20", "C9002", "1800.00", "INR"),
    (14, "09:12:44", "C9001", "2400.00", "INR"),      # correct refusal: more than a whole day
    (14, "11:00:31", "C9002", "500.00", "INR"),       # correct refusal: over the limit by the afternoon
    (14, "12:30:15", "C9003", "900.00", "PHP"),       # screening: recipient hits the watchlist
    (14, "13:05:00", "C1013", "12000.00", "INR"),
    (14, "15:50:35", "C1014", "600.00", "PHP"),
    (14, "18:30:17", "C1190", "1500.00", "INR"),
    (14, "21:45:50", "C1190", "800.00", "INR"),       # wrongly refused: it is Sunday in Doha
    (14, "22:15:30", "C7788", "1800.00", "INR"),
    # Sunday 15 March
    (15, "00:40:12", "C7788", "1500.00", "INR"),      # wrongly allowed: still Sunday in Doha
    (15, "05:55:08", "C1015", "450.00", "INR"),
    (15, "08:20:33", "C1016", "3000.00", "INR"),
    (15, "10:10:10", "C1017", "1000.00", "PKR"),
    (15, "12:00:00", "C1018", "350.00", "EGP"),
    (15, "14:35:25", "C1003", "400.00", "PKR"),
    (15, "16:05:44", "C1019", "2000.00", "PHP"),
    (15, "20:10:05", "C3042", "1900.00", "INR"),
    (15, "21:30:48", "C3042", "400.00", "INR"),       # wrongly refused: it is Monday in Doha
    # Monday 16 March
    (16, "05:40:16", "C1020", "300.00", "INR"),
    (16, "07:15:00", "C1021", "8000.00", "INR"),
    (16, "09:05:12", "C1001", "650.00", "INR"),
    (16, "11:30:00", "C1022", "4000.00", "PHP"),
    (16, "13:15:47", "C1008", "500.00", "PKR"),
    (16, "15:05:19", "C6003", "1700.00", "INR"),
    (16, "17:20:05", "C5521", "1600.00", "INR"),
    (16, "18:40:00", "C1023", "800.00", "INR"),
    (16, "21:05:30", "C5521", "700.00", "INR"),       # wrongly refused: it is Tuesday in Doha
    (16, "21:30:00", "C8120", "2000.00", "INR"),
    (16, "22:50:41", "C6003", "500.00", "INR"),       # wrongly refused: it is Tuesday in Doha
    # Tuesday 17 March
    (17, "01:10:25", "C8120", "1200.00", "INR"),      # wrongly allowed: still Tuesday in Doha
    (17, "02:30:00", "C1024", "350.00", "PHP"),
]

# Ground truth for the graders and tests: replay the same attempts through the corrected code and
# compare. (Checked by the kit's tests against the real service; kept here so there is one source.)
WRONGLY_REFUSED = ("C1190", "C2207", "C3042", "C4410", "C5521", "C6003")
WRONGLY_ALLOWED = ("C7788", "C8120")
CORRECT_REFUSALS = ("C9001", "C9002", "C9005", "C9006")  # (plus C9003, a screening hold)


def generate(src_dir: str | Path) -> str:
    """Run every attempt through RemitService built from ``src_dir`` and return the audit file text."""
    import tempfile

    sys.path.insert(0, str(Path(src_dir).resolve()))
    for name in [n for n in sys.modules if n == "remit" or n.startswith(("remit.", "najmkit"))]:
        del sys.modules[name]  # a clean import from this src_dir, even if another tree was loaded before
    from najmkit import audit, clock as najm_clock, ids
    from remit import ledger
    from remit.errors import LimitExceeded, NotificationError, ScreeningHit
    from remit.fx import StaticRateProvider
    from remit.models import Customer
    from remit.money import Money
    from remit.notify import InMemoryNotifier
    from remit.service import RemitService
    from remit.store import Store

    class FlakyNotifier(InMemoryNotifier):
        """Fails to deliver "transfer sent" to one customer, like a real SMS gateway on a bad day."""

        def notify(self, customer, template_id, **values):
            if customer.id == NOTIFICATION_FAILS_FOR and template_id == "transfer_sent":
                raise NotificationError("gateway timeout")
            return super().notify(customer, template_id, **values)

    start = datetime(2026, 3, 13, 6, 0, tzinfo=timezone.utc)
    fixed = najm_clock.FixedClock(start)
    najm_clock.set_clock(fixed)
    counter = itertools.count(1)

    def production_like_token() -> str:
        """Twelve hex digits, as in production, but reproducible (a hash of a counter, not random)."""
        return hashlib.sha256(f"m06-prod-log-{next(counter)}".encode()).hexdigest()[:12].upper()

    ids.use_generator(production_like_token)
    ledger.reset()
    with tempfile.TemporaryDirectory() as scratch:
        log_path = Path(scratch) / "audit.jsonl"
        audit.configure(log_path)
        with Store(":memory:") as store:
            for cid, (name, tier) in CUSTOMERS.items():
                store.add_customer(Customer(cid, name, tier, "none", "en"))
            service = RemitService(store, StaticRateProvider(), [SANCTIONED_RECIPIENT], fixed, FlakyNotifier())
            for day, hms, cid, amount, receive in sorted(ATTEMPTS, key=lambda a: (a[0], a[1])):
                fixed.set(datetime.fromisoformat(f"2026-03-{day:02d}T{hms}+00:00"))
                recipient = SANCTIONED_RECIPIENT if cid == "C9003" else "Recipient " + cid[1:]
                try:
                    service.send(cid, Money(amount, "QAR"), receive, recipient)
                except (LimitExceeded, ScreeningHit):
                    pass  # the rejection is in the audit log, which is all this script wants
        text = log_path.read_text(encoding="utf-8")
        audit.configure(None)
    ids.use_generator(None)
    najm_clock.reset_clock()
    ledger.reset()
    return text


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    out = None
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    text = generate(argv[0])
    if out:
        Path(out).write_text(text, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
