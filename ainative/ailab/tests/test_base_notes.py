"""Every quirk, smell and gap in KIT_NOTES.md section 4 is executed here against the pristine base.

These tests are the proof that what the notes tell lab writers is true. They run the base code in a
subprocess (so its modules never mix with the kit's) and compare JSON results.
"""
from __future__ import annotations

import json
import re
import textwrap
from decimal import Decimal

import pytest

from ailab import framework, runner

BASE = framework.BASE_REPO
PRELUDE = textwrap.dedent('''
    import json, sys
    from decimal import Decimal
    from datetime import datetime, timezone
    from najmkit import audit, clock, ids
    from remit import ledger, screening
    from remit.money import Money
    ids.use_generator(ids.SequentialIds())
    clock.set_clock(clock.FixedClock("2026-03-02T09:00:00+00:00"))
    ledger.reset()
    def show(value):
        print(json.dumps(value, default=str, ensure_ascii=False))
''')


def probe(code: str):
    """Run ``code`` against the base (after a prelude) and return the JSON it ``show()``s."""
    result = runner.run_python(["-c", PRELUDE + textwrap.dedent(code)], pythonpath=[BASE / "src"], timeout=60)
    assert result.ok, result.output
    return json.loads(result.stdout.strip().splitlines()[-1])


def test_q_led_1_partner_share_is_rounded_half_even():
    got = probe('''
        entries = ledger.post_transfer("TRF-1", "C1", Money("500", "QAR"), Money("10.15", "QAR"))
        show([[e["account"], e["side"], str(e["amount"])] for e in entries])
    ''')
    assert got == [["CUSTOMER:C1", "D", "510.15"], ["PAYOUT_CLEARING", "C", "500.00"], ["FEE_INCOME", "C", "7.11"],
                   ["PARTNER_PAYABLE", "C", "3.04"]]
    # half-up would give 3.05 and 7.10: the base rounds this one share half-even
    assert Decimal("10.15") * Decimal("0.30") == Decimal("3.0450")


def test_q_led_1_each_posting_balances_and_a_clean_fee_has_no_rounding():
    got = probe('''
        for i, fee in enumerate(["12.00", "10.15", "5.01", "150.00"]):
            ledger.post_transfer(f"T{i}", "C1", Money("500", "QAR"), Money(fee, "QAR"))
        entries = ledger.journal()
        debits = sum(e["amount"] for e in entries if e["side"] == "D")
        credits = sum(e["amount"] for e in entries if e["side"] == "C")
        by_transfer = {}
        for e in entries:
            by_transfer.setdefault(e["transfer_id"], {"D": Decimal(0), "C": Decimal(0)})[e["side"]] += e["amount"]
        show({"balanced": all(v["D"] == v["C"] for v in by_transfer.values()),
              "partner": str(ledger.balance("PARTNER_PAYABLE")), "income": str(ledger.balance("FEE_INCOME"))})
    ''')
    assert got["balanced"] is True
    assert Decimal(got["partner"]) + Decimal(got["income"]) == Decimal("177.16")  # the fees 12.00 + 10.15 + 5.01 + 150.00, exactly


def test_q_led_2_reading_a_balance_creates_the_account():
    got = probe('''
        before = ledger.accounts()
        value = ledger.balance("NOPE")
        show({"before": before, "value": repr(value), "after": ledger.accounts()})
    ''')
    assert got == {"before": [], "value": "Decimal('0')", "after": ["NOPE"]}


def test_q_led_3_state_is_module_level_and_ids_and_time_are_global():
    got = probe('''
        ledger.post_transfer("TRF-1", "C1", Money("100", "QAR"), Money("5", "QAR"))
        ledger.post_transfer("TRF-2", "C1", Money("100", "QAR"), Money("5", "QAR"))
        first = ledger.journal()[0]
        accumulated = str(ledger.balance("CUSTOMER:C1"))
        try:
            ledger.post_transfer("TRF-1", "C1", Money("100", "QAR"), Money("5", "QAR"))
            duplicate = None
        except Exception as exc:
            duplicate = type(exc).__name__
        ledger.reset()
        show({"entry_id": first["entry_id"], "posted_at": first["posted_at"], "accumulated": accumulated,
              "duplicate": duplicate, "after_reset": [ledger.accounts(), len(ledger.journal())]})
    ''')
    assert got == {"entry_id": "JNL-000001", "posted_at": "2026-03-02T09:00:00+00:00", "accumulated": "-210.00",
                   "duplicate": "DuplicatePosting", "after_reset": [[], 0]}


def test_q_led_4_balances_are_bare_decimals_and_only_qar_is_accepted():
    got = probe('''
        ledger.post_transfer("TRF-1", "C1", Money("100", "QAR"), Money("5", "QAR"))
        try:
            ledger.post_transfer("TRF-2", "C1", Money("100", "EGP"), Money("5", "QAR"))
            error = None
        except Exception as exc:
            error = type(exc).__name__
        show({"type": type(ledger.balance("PAYOUT_CLEARING")).__name__, "customer": str(ledger.balance("CUSTOMER:C1")), "error": error})
    ''')
    assert got == {"type": "Decimal", "customer": "-105.00", "error": "CurrencyMismatch"}


def test_q_scr_quirks():
    got = probe('''
        s = screening
        show({
          "q1_omar_omer": s.screen("Omar Khan", ["Omer Khan"]).hit,
          "q1_same": s.screen("Omar Khan", ["Omar Khan"]).hit,
          "q1_hasan_hassan": s.screen("Hasan", ["Hassan"]).hit,
          "q2_single_vs_multi": s.screen("Madonna", ["Madonna Ciccone"]).hit,
          "q2_single_vs_single": s.screen("Madonna", ["Madonna"]).hit,
          "q2_two_in_three": s.screen("Karim Qadiri", ["Karim Nasser Al-Qadiri"]).hit,
          "q2_order": s.screen("Sanctioned Test Person", ["Test Sanctioned Person"]).hit,
          "q3_fifth_token": s.screen("A B C D X", ["A B C D Y"]).hit,
          "q3_tokens": s.tokens("A B C D X"),
          "q4_hmza": s.tokens("حمزة"),
          "q4_arabic_vs_latin": s.screen("حمزة", ["Hamza"]).hit,
          "q4_arabic_vs_arabic": s.screen("حمزة", ["حمزة"]).hit,
          "q4_chinese": s.tokens("张伟"),
          "accents": s.screen("Elena Marković", s.DEFAULT_WATCHLIST).hit,
          "arabic_names": s.screen("كريم القادري", s.DEFAULT_WATCHLIST).hit,
          "particles": s.tokens("Khalid bin Al-Walid ibn Said"),
        })
    ''')
    assert got == {
        "q1_omar_omer": False, "q1_same": True, "q1_hasan_hassan": True,
        "q2_single_vs_multi": False, "q2_single_vs_single": True, "q2_two_in_three": True, "q2_order": True,
        "q3_fifth_token": True, "q3_tokens": ["a", "b", "c", "d"],
        "q4_hmza": ["hmza"], "q4_arabic_vs_latin": False, "q4_arabic_vs_arabic": True, "q4_chinese": [],
        "accents": True, "arabic_names": True, "particles": ["khalid", "walid", "said"],
    }


def test_s_store_1_search_by_name_is_built_with_string_formatting():
    got = probe('''
        from remit.models import Customer
        from remit.store import Store
        db = Store()
        for i, name in enumerate(["Aisha Rahman", "Bilal Khan", "Mariam O'Brien"]):
            db.add_customer(Customer(f"C{i}", name, "T1"))
        try:
            db.search_by_name("O'B")
            error = None
        except Exception as exc:
            error = type(exc).__name__
        show({"normal": [c.id for c in db.search_by_name("khan")], "quote_error": error,
              "injection": [c.id for c in db.search_by_name("zzz%' OR name LIKE '%")]})
    ''')
    assert got == {"normal": ["C1"], "quote_error": "OperationalError", "injection": ["C0", "C1", "C2"]}


def test_every_other_store_query_is_parameterised():
    source = (BASE / "src" / "remit" / "store.py").read_text(encoding="utf-8")
    assert source.count(".format(") == 1 and "S-STORE-1" in source
    assert not re.search(r"execute\(f[\"']", source)


def test_d_arch_1_and_2_the_architecture_doc_is_partly_stale():
    doc = " ".join((BASE / "docs" / "ARCHITECTURE.md").read_text(encoding="utf-8").split())  # line breaks do not matter
    assert doc.count("risk.py") >= 2 and not (BASE / "src" / "remit" / "risk.py").exists()
    assert "T1 (identity checked) may send up to QAR 5,000 per day" in doc and "There is no monthly limit" in doc
    # ...and the code says otherwise
    probe_result = probe('''
        from remit import limits
        show({t: [str(v.daily.amount), str(v.monthly.amount)] for t, v in limits.LIMITS.items()})
    ''')
    assert probe_result == {"T1": ["2000.00", "8000.00"], "T2": ["10000.00", "40000.00"], "T3": ["30000.00", "120000.00"]}
    # the parts that must stay true
    assert "A \"day\" is a Qatar calendar day" in doc and "21:00 to 21:00 UTC" in doc


def test_d_svc_1_a_failing_store_leaves_the_ledger_posting_behind():
    got = probe('''
        from remit.errors import StoreError
        from remit.fx import StaticRateProvider
        from remit.models import Customer
        from remit.notify import InMemoryNotifier
        from remit.service import RemitService
        from remit.store import Store

        class BrokenStore(Store):
            def save_transfer(self, transfer):
                raise StoreError("disk full")

        db = BrokenStore()
        db.add_customer(Customer("C1", "Aisha", "T2"))
        service = RemitService(db, StaticRateProvider(), [], clock.get_clock(), InMemoryNotifier())
        try:
            service.send("C1", Money("500", "QAR"), "INR", "Ravi Kumar")
            error = None
        except StoreError as exc:
            error = str(exc)
        show({"error": error, "journal": len(ledger.journal()), "transfers": db.count_transfers()})
    ''')
    assert got == {"error": "disk full", "journal": 4, "transfers": 0}


def test_the_ledger_is_posted_only_after_validation_limits_screening_and_quote_checks():
    got = probe('''
        from remit.errors import RemitError
        from remit.fx import StaticRateProvider
        from remit.models import Customer
        from remit.notify import InMemoryNotifier
        from remit.service import RemitService
        from remit.store import Store

        db = Store()
        db.add_customer(Customer("C1", "Aisha", "T1"))
        service = RemitService(db, StaticRateProvider(), ["Test Sanctioned Person"], clock.get_clock(), InMemoryNotifier())
        outcomes = {}
        attempts = {
            "out_of_range": lambda: service.send("C1", Money("10", "QAR"), "INR", "Ravi"),
            "limit": lambda: service.send("C1", Money("2000.01", "QAR"), "INR", "Ravi"),
            "screening": lambda: service.send("C1", Money("100", "QAR"), "INR", "Test Sanctioned Person"),
        }
        for name, attempt in attempts.items():
            try:
                attempt()
            except RemitError as exc:
                outcomes[name] = exc.code
        quote = service.quote(Money("100", "QAR"), "INR")
        clock.get_clock().advance(seconds=60)
        try:
            service.send("C1", Money("100", "QAR"), "INR", "Ravi", quote=quote)
        except RemitError as exc:
            outcomes["expired"] = exc.code
        show({"outcomes": outcomes, "journal": len(ledger.journal()), "transfers": db.count_transfers()})
    ''')
    assert got == {"outcomes": {"out_of_range": "amount_out_of_range", "limit": "limit_exceeded", "screening": "screening_hit",
                                "expired": "quote_expired"}, "journal": 0, "transfers": 0}


def test_g_loyalty_the_loyalty_tier_is_not_used_by_any_business_logic():
    src = BASE / "src" / "remit"
    users = sorted(p.name for p in src.glob("*.py") if "loyalty" in p.read_text(encoding="utf-8"))
    assert users == ["cli.py", "models.py", "store.py"]


def test_m00_anchor_the_correct_spelling_occurs_exactly_once_in_the_template_file():
    text = (BASE / "src" / "remit" / "notify.py").read_text(encoding="utf-8")
    assert text.count("received") == 1 and text.count("recieved") == 0


def test_m06_anchor_the_utc_bug_is_a_two_place_seed_and_four_tests_depend_on_qatar_time():
    limits_src = (BASE / "src" / "remit" / "limits.py").read_text(encoding="utf-8")
    assert limits_src.count("local = to_local(now)") == 2
    tests = (BASE / "tests" / "test_limits.py").read_text(encoding="utf-8")
    for name in ("test_the_day_ends_at_midnight_in_qatar_not_in_utc",
                 "test_a_transfer_after_qatar_midnight_but_before_utc_midnight_belongs_to_the_new_day",
                 "test_the_month_changes_at_midnight_in_qatar", "test_windows_are_local_calendar_windows"):
        assert f"def {name}(" in tests


def test_the_fixed_clock_in_the_base_conftest_is_the_documented_monday():
    conftest = (BASE / "tests" / "conftest.py").read_text(encoding="utf-8")
    assert "NOW = datetime(2026, 3, 2, 9, 0, tzinfo=timezone.utc)" in conftest
    assert "Customer(\"C001\", \"Aisha Rahman\", \"T2\", \"none\", \"en\")" in conftest
    assert "Customer(\"C002\", \"Bilal Khan\", \"T1\", \"silver\", \"en\")" in conftest
    assert "Customer(\"C003\", \"Mariam Saleh\", \"T3\", \"gold\", \"ar\")" in conftest
    assert '["Test Sanctioned Person"]' in conftest


def test_the_documented_najmkit_names_exist_and_the_hallucinated_ones_do_not():
    got = probe('''
        from najmkit import audit, clock, ids
        real = ["new_id", "SequentialIds", "use_generator"]
        show({"ids": [hasattr(ids, n) for n in real],
              "fake": [hasattr(ids, "generate"), hasattr(ids, "new_uuid"), hasattr(clock, "utcnow"), hasattr(clock, "freeze"),
                       hasattr(audit, "write"), hasattr(audit, "record")]})
    ''')
    assert got == {"ids": [True, True, True], "fake": [False] * 6}
