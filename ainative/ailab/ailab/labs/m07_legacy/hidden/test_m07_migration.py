"""Hidden tests for lab m07, part 3: after the najmkit migration Remit writes the same audit lines and
the same ids as before. The fraud team's parser reads these lines, so they are compared as text."""
import json

import pytest

from najmkit import audit
from remit.errors import LimitExceeded, NotificationError
from remit.money import Money


def qar(value):
    return Money(value, "QAR")


def lines(path):
    return path.read_text(encoding="utf-8").splitlines()


def test_a_sent_transfer_writes_this_exact_audit_line(hx_build, tmp_path):
    audit.configure(tmp_path / "audit.jsonl")
    hx_build().send("C001", qar("500"), "INR", "Ravi Kumar", express=True)
    assert lines(tmp_path / "audit.jsonl") == [
        '{"corridor": "QAR-INR", "customer_id": "C001", "event": "transfer.sent", "express": true, '
        '"fee": "27.00 QAR", "send_amount": "500.00 QAR", "transfer_id": "TRF-000001", "ts": "2026-03-02T09:00:00+00:00"}'
    ]


def test_a_refused_transfer_writes_this_exact_audit_line(hx_build, tmp_path):
    audit.configure(tmp_path / "audit.jsonl")
    service = hx_build()
    service.send("C002", qar("1500"), "INR", "Ravi Kumar")
    with pytest.raises(LimitExceeded):
        service.send("C002", qar("600"), "INR", "Ravi Kumar")
    rejected = [line for line in lines(tmp_path / "audit.jsonl") if '"transfer.rejected"' in line]
    assert rejected == [
        '{"corridor": "QAR-INR", "customer_id": "C002", "event": "transfer.rejected", "reason": "limit_exceeded", '
        '"send_amount": "600.00 QAR", "ts": "2026-03-02T09:00:00+00:00"}'
    ]


def test_a_failed_notification_writes_this_exact_audit_line(hx_build, tmp_path):
    class Broken:
        def notify(self, customer, template_id, **values):
            raise NotificationError("gateway down")

    audit.configure(tmp_path / "audit.jsonl")
    service = hx_build()
    service.notifier = Broken()
    service.send("C001", qar("100"), "PHP", "Maria Santos")
    first = lines(tmp_path / "audit.jsonl")[0]
    assert first == '{"customer_id": "C001", "event": "notification.failed", "reason": "notification_error", "template": "transfer_sent", "ts": "2026-03-02T09:00:00+00:00"}'


def test_every_audit_line_is_json_with_text_amounts(hx_build, tmp_path):
    audit.configure(tmp_path / "audit.jsonl")
    service = hx_build()
    service.send("C003", qar("250.50"), "PHP", "Maria Santos")
    for line in lines(tmp_path / "audit.jsonl"):
        record = json.loads(line)
        assert record["send_amount"] == "250.50 QAR" and record["fee"].endswith(" QAR")


def test_the_command_line_audit_file_is_unchanged(tmp_path, hx_clock):
    import io

    from remit.cli import main

    env = {"REMIT_DB": str(tmp_path / "remit.db"), "REMIT_AUDIT_LOG": str(tmp_path / "audit.jsonl")}
    out = io.StringIO()
    main(["customer", "add", "--id", "C001", "--name", "Aisha Rahman", "--kyc", "T2"], environ=env, clock=hx_clock, out=out)
    main(["send", "--customer", "C001", "QAR", "500", "INR", "--recipient", "Ravi Kumar"], environ=env, clock=hx_clock, out=out)
    assert lines(tmp_path / "audit.jsonl") == [
        '{"corridor": "QAR-INR", "customer_id": "C001", "event": "transfer.sent", "express": false, '
        '"fee": "12.00 QAR", "send_amount": "500.00 QAR", "transfer_id": "TRF-000001", "ts": "2026-03-02T09:00:00+00:00"}'
    ]


def test_new_customers_and_transfers_still_get_the_same_style_of_id(hx_build):
    service = hx_build()
    customer = service.store.create_customer("Omar Farooq")
    assert customer.id == "CUS-000001"
    assert service.send("C001", qar("500"), "INR", "Ravi Kumar").transfer.id == "TRF-000002"
