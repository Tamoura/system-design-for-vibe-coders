"""SQLite storage for customers and transfers.

Money is stored as TEXT (``"500.00"``) next to its currency, never as a REAL, so no
amount ever passes through a binary float. Timestamps are stored as ISO-8601 UTC text
(``2026-03-02T09:00:00+00:00``), which sorts correctly as text.

Every query uses ``?`` placeholders except ``search_by_name``: see the note on it.
"""
from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone
from decimal import Decimal

from najmkit import ids
from remit.errors import StoreError, UnknownCustomer
from remit.models import Customer, Transfer
from remit.money import Money

_SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
    id           TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    kyc_tier     TEXT NOT NULL,
    loyalty_tier TEXT NOT NULL,
    language     TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS transfers (
    id               TEXT PRIMARY KEY,
    customer_id      TEXT NOT NULL REFERENCES customers(id),
    corridor         TEXT NOT NULL,
    send_amount      TEXT NOT NULL,
    send_currency    TEXT NOT NULL,
    fee              TEXT NOT NULL,
    receive_amount   TEXT NOT NULL,
    receive_currency TEXT NOT NULL,
    rate             TEXT NOT NULL,
    recipient_name   TEXT NOT NULL,
    delivery_method  TEXT NOT NULL,
    created_at       TEXT NOT NULL,
    express          INTEGER NOT NULL,
    status           TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS transfers_by_customer ON transfers (customer_id, created_at);
"""


class Store:
    """A small repository over one SQLite database (``":memory:"`` by default)."""

    def __init__(self, path: str | os.PathLike[str] = ":memory:") -> None:
        self._db = sqlite3.connect(str(path))
        self._db.row_factory = sqlite3.Row
        self._db.execute("PRAGMA foreign_keys = ON")
        self._db.executescript(_SCHEMA)

    def close(self) -> None:
        self._db.close()

    def __enter__(self) -> Store:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    # -- customers -------------------------------------------------------------
    def add_customer(self, customer: Customer) -> None:
        try:
            with self._db:
                self._db.execute(
                    "INSERT INTO customers (id, name, kyc_tier, loyalty_tier, language) VALUES (?, ?, ?, ?, ?)",
                    (customer.id, customer.name, customer.kyc_tier, customer.loyalty_tier, customer.language),
                )
        except sqlite3.IntegrityError:
            raise StoreError(f"customer {customer.id} already exists") from None

    def create_customer(self, name: str, kyc_tier: str = "T1", loyalty_tier: str = "none", language: str = "en") -> Customer:
        """Create a customer with a fresh ``CUS-...`` id and store it."""
        customer = Customer(ids.make_id("CUS"), name, kyc_tier, loyalty_tier, language)
        self.add_customer(customer)
        return customer

    def get_customer(self, customer_id: str) -> Customer | None:
        row = self._db.execute("SELECT * FROM customers WHERE id = ?", (customer_id,)).fetchone()
        return _customer(row) if row else None

    def require_customer(self, customer_id: str) -> Customer:
        customer = self.get_customer(customer_id)
        if customer is None:
            raise UnknownCustomer(f"no customer {customer_id!r}")
        return customer

    def list_customers(self) -> list[Customer]:
        rows = self._db.execute("SELECT * FROM customers ORDER BY id").fetchall()
        return [_customer(row) for row in rows]

    def search_by_name(self, fragment: str) -> list[Customer]:
        """Customers whose name contains ``fragment`` (SQLite LIKE: ASCII case-insensitive).

        KNOWN SMELL (S-STORE-1): this query is built with string formatting instead of
        a placeholder. A fragment containing a single quote raises
        sqlite3.OperationalError, and a crafted fragment can change the query. Every
        other query in this file is parameterised. Fix it when someone asks.
        """
        query = "SELECT * FROM customers WHERE name LIKE '%{}%' ORDER BY id".format(fragment)
        rows = self._db.execute(query).fetchall()
        return [_customer(row) for row in rows]

    # -- transfers -------------------------------------------------------------
    def save_transfer(self, transfer: Transfer) -> None:
        try:
            with self._db:
                self._db.execute(
                    "INSERT INTO transfers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        transfer.id,
                        transfer.customer_id,
                        transfer.corridor,
                        str(transfer.send_amount.amount),
                        transfer.send_amount.currency,
                        str(transfer.fee.amount),
                        str(transfer.receive_amount.amount),
                        transfer.receive_amount.currency,
                        str(transfer.rate),
                        transfer.recipient_name,
                        transfer.delivery_method,
                        _utc_text(transfer.created_at),
                        1 if transfer.express else 0,
                        transfer.status,
                    ),
                )
        except sqlite3.IntegrityError as exc:
            raise StoreError(f"cannot save transfer {transfer.id}: {exc}") from None

    def get_transfer(self, transfer_id: str) -> Transfer | None:
        row = self._db.execute("SELECT * FROM transfers WHERE id = ?", (transfer_id,)).fetchone()
        return _transfer(row) if row else None

    def list_transfers(self, customer_id: str, since: datetime | None = None) -> list[Transfer]:
        """A customer's transfers, oldest first; with ``since``, only those at or after it."""
        sql = "SELECT * FROM transfers WHERE customer_id = ?"
        args: list[str] = [customer_id]
        if since is not None:
            sql += " AND created_at >= ?"
            args.append(_utc_text(since))
        rows = self._db.execute(sql + " ORDER BY created_at, id", args).fetchall()
        return [_transfer(row) for row in rows]

    def count_transfers(self) -> int:
        return self._db.execute("SELECT COUNT(*) FROM transfers").fetchone()[0]


def _utc_text(moment: datetime) -> str:
    """ISO-8601 UTC text for an aware datetime (a naive one is a bug in the caller, so it is refused)."""
    if moment.tzinfo is None or moment.utcoffset() is None:
        raise ValueError("datetimes must be timezone-aware")
    return moment.astimezone(timezone.utc).isoformat()


def _customer(row: sqlite3.Row) -> Customer:
    return Customer(row["id"], row["name"], row["kyc_tier"], row["loyalty_tier"], row["language"])


def _transfer(row: sqlite3.Row) -> Transfer:
    return Transfer(
        id=row["id"],
        customer_id=row["customer_id"],
        corridor=row["corridor"],
        send_amount=Money(Decimal(row["send_amount"]), row["send_currency"]),
        fee=Money(Decimal(row["fee"]), row["send_currency"]),
        receive_amount=Money(Decimal(row["receive_amount"]), row["receive_currency"]),
        rate=Decimal(row["rate"]),
        recipient_name=row["recipient_name"],
        delivery_method=row["delivery_method"],
        created_at=datetime.fromisoformat(row["created_at"]),
        express=bool(row["express"]),
        status=row["status"],
    )
