"""The Najm Transfers REST API (sample system under test). Run it with:

    uvicorn najm.api:app --port 8000

Tokens are fake: "Bearer token-alice" and "Bearer token-bob". Use create_app() in tests
so every test gets a fresh, isolated service."""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

from fastapi import FastAPI, Header, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from .transfers import TransferRejected, TransferService

STATUS = {"not_owner": 403, "not_found": 404, "idempotency_key_reuse": 409}
USERS = {"token-alice": "alice", "token-bob": "bob"}
PAGE = Path(__file__).resolve().parent.parent / "static" / "transfer.html"


class TransferIn(BaseModel):
    from_account: str
    to_account: str
    amount: Decimal
    currency: str
    kind: str = "domestic"


def _error(status: int, code: str, message: str = "") -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message or code}})


def create_app(service: TransferService | None = None) -> FastAPI:
    app = FastAPI(title="Najm Transfers (sample)")
    svc = service or TransferService()

    @app.exception_handler(TransferRejected)
    async def rejected(_: Request, exc: TransferRejected):
        return _error(STATUS.get(exc.code, 422), exc.code, str(exc))

    def user_of(authorization: str | None) -> str | None:
        if not authorization or not authorization.startswith("Bearer "):
            return None
        return USERS.get(authorization.removeprefix("Bearer ").strip())

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/transfers")
    def create_transfer(body: TransferIn, authorization: str | None = Header(None),
                        idempotency_key: str | None = Header(None)):
        user = user_of(authorization)
        if user is None:
            return _error(401, "unauthenticated")
        if not idempotency_key:
            return _error(400, "missing_idempotency_key")
        transfer, created = svc.submit(user, body.model_dump(), idempotency_key, datetime.now(ZoneInfo("UTC")))
        public = {k: v for k, v in transfer.items() if k != "owner"}
        return JSONResponse(status_code=201 if created else 200, content=public,
                            headers={} if created else {"Idempotent-Replay": "true"})

    @app.get("/transfers/{transfer_id}")
    def get_transfer(transfer_id: str, authorization: str | None = Header(None)):
        user = user_of(authorization)
        if user is None:
            return _error(401, "unauthenticated")
        t = svc.get(user, transfer_id)
        return {k: v for k, v in t.items() if k != "owner"}

    @app.get("/accounts/{account_id}/balance")
    def balance(account_id: str, authorization: str | None = Header(None)):
        user = user_of(authorization)
        if user is None:
            return _error(401, "unauthenticated")
        return svc.balance(user, account_id)

    @app.get("/app", response_class=HTMLResponse)
    def page():
        return PAGE.read_text(encoding="utf-8")

    return app


app = create_app()
