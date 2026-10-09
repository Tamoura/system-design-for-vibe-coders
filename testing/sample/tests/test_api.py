"""API tests for the Najm Transfers sample. Each test builds its own app, so tests never share state."""
import pytest
from fastapi.testclient import TestClient

from najm.api import create_app

ALICE = {"Authorization": "Bearer token-alice"}
BOB = {"Authorization": "Bearer token-bob"}
BODY = {"from_account": "acc-1", "to_account": "acc-2", "amount": "250.00", "currency": "QAR", "kind": "domestic"}


@pytest.fixture
def client():
    return TestClient(create_app())


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_create_transfer_returns_201_and_the_fee(client):
    r = client.post("/transfers", json=BODY, headers={**ALICE, "Idempotency-Key": "k1"})
    assert r.status_code == 201
    assert r.json()["fee"] == "0.00"
    assert r.json()["status"] == "accepted"


def test_repeating_the_request_replays_the_first_response(client):
    h = {**ALICE, "Idempotency-Key": "k1"}
    first = client.post("/transfers", json=BODY, headers=h)
    again = client.post("/transfers", json=BODY, headers=h)
    assert again.status_code == 200
    assert again.headers["Idempotent-Replay"] == "true"
    assert again.json()["id"] == first.json()["id"]


def test_missing_token_is_401(client):
    assert client.post("/transfers", json=BODY, headers={"Idempotency-Key": "k"}).status_code == 401


def test_missing_idempotency_key_is_400(client):
    assert client.post("/transfers", json=BODY, headers=ALICE).status_code == 400


def test_over_the_per_transfer_maximum_is_422(client):
    r = client.post("/transfers", json={**BODY, "amount": "25000.01"}, headers={**ALICE, "Idempotency-Key": "k"})
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "above_per_transfer_max"


def test_bob_cannot_read_alices_balance(client):
    assert client.get("/accounts/acc-1/balance", headers=BOB).status_code == 403
