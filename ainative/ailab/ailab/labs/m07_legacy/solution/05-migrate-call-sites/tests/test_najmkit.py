import json
from datetime import datetime, timedelta, timezone

import pytest

from najmkit import audit, clock, ids


def test_make_id_has_a_prefix_and_a_random_token_by_default():
    ids.use_source(None)
    a, b = ids.make_id("TRF"), ids.make_id("TRF")
    assert a != b
    prefix, token = a.split("-")
    assert prefix == "TRF" and len(token) == 12 and token == token.upper()


def test_sequential_ids_are_deterministic():
    ids.use_source(ids.SequentialIds())
    assert [ids.make_id("TRF"), ids.make_id("CUS")] == ["TRF-000001", "CUS-000002"]
    ids.use_source(ids.SequentialIds(start=40))
    assert ids.make_id("JNL") == "JNL-000040"


def test_bad_prefixes_are_rejected():
    for bad in ("", "t", "trf", "TOOLONG", "TR1", None):
        with pytest.raises(ValueError):
            ids.make_id(bad)


def test_fixed_clock_only_moves_when_told():
    fixed = clock.FixedClock("2026-03-02T09:00:00+00:00")
    assert fixed.now() == fixed.now() == datetime(2026, 3, 2, 9, 0, tzinfo=timezone.utc)
    assert fixed.advance(minutes=90) == datetime(2026, 3, 2, 10, 30, tzinfo=timezone.utc)
    fixed.set("2026-03-03T00:00:00+03:00")  # converted to UTC
    assert fixed.now() == datetime(2026, 3, 2, 21, 0, tzinfo=timezone.utc)
    with pytest.raises(ValueError):  # clocks refuse naive times
        clock.FixedClock(datetime(2026, 3, 2, 9, 0))


def test_module_level_now_follows_the_installed_clock():
    clock.install(clock.FixedClock("2030-01-01T00:00:00+00:00"))
    assert clock.utc_now().year == 2030
    clock.restore()
    assert abs(clock.utc_now() - datetime.now(timezone.utc)) < timedelta(minutes=1)
    assert isinstance(clock.current(), clock.SystemClock)


def test_log_event_returns_the_record_and_writes_nothing_without_a_path():
    record = audit.emit("demo.happened", thing="x")
    assert record == {"ts": "2026-03-02T09:00:00+00:00", "event": "demo.happened", "thing": "x"}
    assert audit.current_path() is None and audit.read_events() == []


def test_log_event_appends_json_lines(tmp_path):
    path = tmp_path / "audit.jsonl"
    audit.configure(path)
    audit.emit("transfer.sent", transfer_id="TRF-1")
    audit.emit("transfer.rejected", reason="limit_exceeded")
    lines = path.read_text(encoding="utf-8").splitlines()
    assert [json.loads(line)["event"] for line in lines] == ["transfer.sent", "transfer.rejected"]
    assert lines[0] == '{"event": "transfer.sent", "transfer_id": "TRF-1", "ts": "2026-03-02T09:00:00+00:00"}'


def test_the_audit_path_can_come_from_the_environment(tmp_path, monkeypatch):
    path = tmp_path / "from_env.jsonl"
    monkeypatch.setenv(audit.ENV_VAR, str(path))
    audit.emit("demo.happened")
    assert len(audit.read_events()) == 1 and path.exists()
    audit.configure(tmp_path / "configured.jsonl")  # configure() wins over the environment
    assert audit.current_path() == tmp_path / "configured.jsonl"


def test_event_names_and_reserved_fields_are_checked():
    for bad in ("Transfer.Sent", "transfer sent", ".x", ""):
        with pytest.raises(ValueError):
            audit.emit(bad)
    with pytest.raises(ValueError):
        audit.emit("demo.happened", ts="yesterday")


def test_emit_takes_json_values_only():
    from decimal import Decimal

    for bad in (Decimal("1.50"), datetime(2026, 3, 2, tzinfo=timezone.utc), {1, 2}):
        with pytest.raises(TypeError):
            audit.emit("demo.happened", value=bad)
    record = audit.emit("demo.happened", text="500.00 QAR", count=2, ok=True, nothing=None, tags=["a"], extra={"k": 1.5})
    assert record["text"] == "500.00 QAR" and record["extra"] == {"k": 1.5}
