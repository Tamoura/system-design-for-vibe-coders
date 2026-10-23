"""Command line: ``python -m remit <command>``.

    python -m remit customer add --id C001 --name "Aisha Rahman" --kyc T2 [--lang ar]
    python -m remit customer list
    python -m remit quote QAR 500 INR [--express] [--delivery wallet]
    python -m remit send --customer C001 QAR 500 INR --recipient "Ravi Kumar" [--express]
    python -m remit history --customer C001

The database is REMIT_DB (default remit.db in the current directory). Exit codes: 0 ok,
1 a Remit error (the message goes to stderr), 2 bad usage.
"""
from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from typing import Any, TextIO

from najmkit import audit, clock as najm_clock
from remit import screening
from remit.config import load_config
from remit.errors import RemitError
from remit.fx import QUOTE_TTL, StaticRateProvider
from remit.models import KYC_TIERS, LANGUAGES, LOYALTY_TIERS, Customer
from remit.money import Money
from remit.notify import ConsoleNotifier
from remit.service import RemitService
from remit.store import Store


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="remit", description="Najm Remit (fictional demo CLI)")
    sub = parser.add_subparsers(dest="command", required=True)

    customer = sub.add_parser("customer", help="manage demo customers")
    csub = customer.add_subparsers(dest="action", required=True)
    add = csub.add_parser("add", help="add a customer")
    add.add_argument("--id", required=True)
    add.add_argument("--name", required=True)
    add.add_argument("--kyc", choices=KYC_TIERS, default="T1")
    add.add_argument("--loyalty", choices=LOYALTY_TIERS, default="none")
    add.add_argument("--lang", choices=LANGUAGES, default=None)
    csub.add_parser("list", help="list customers")

    for name in ("quote", "send"):
        p = sub.add_parser(name, help=f"{name} a transfer")
        p.add_argument("send_currency")
        p.add_argument("amount")
        p.add_argument("receive_currency")
        p.add_argument("--express", action="store_true")
        p.add_argument("--delivery", default=None)
        if name == "send":
            p.add_argument("--customer", required=True)
            p.add_argument("--recipient", required=True)

    history = sub.add_parser("history", help="a customer's transfers")
    history.add_argument("--customer", required=True)
    return parser


def _print_quote(q: Any, out: TextIO) -> None:
    ttl = int(QUOTE_TTL.total_seconds())
    print(f"Corridor:  {q.corridor.send_currency} -> {q.corridor.receive_currency}", file=out)
    print(f"Send:      {q.send_amount}", file=out)
    print(f"Fee:       {q.fee}{' (express)' if q.express else ''}", file=out)
    print(f"Total:     {q.total}", file=out)
    print(f"Rate:      {q.fx.rate} (valid for {ttl} s)", file=out)
    print(f"Receive:   {q.fx.receive}", file=out)
    print(f"Delivery:  {q.delivery_method}", file=out)


def main(
    argv: Sequence[str] | None = None,
    *,
    environ: dict[str, str] | None = None,
    clock: Any = None,
    out: TextIO | None = None,
    err: TextIO | None = None,
) -> int:
    out = out or sys.stdout
    err = err or sys.stderr
    try:
        args = _parser().parse_args(argv)
    except SystemExit as exc:  # argparse already printed the usage message
        return int(exc.code or 0)
    try:
        config = load_config(environ)
    except ValueError as exc:
        print(f"error: {exc}", file=err)
        return 2
    audit.configure(config.audit_log)

    try:
        watchlist = screening.load_watchlist(config.watchlist_path) if config.watchlist_path else screening.DEFAULT_WATCHLIST
    except OSError as exc:
        print(f"error: cannot read the watchlist: {exc.strerror or exc}", file=err)
        return 2

    # A quote touches no data, so it does not create a database file.
    store = Store(":memory:" if args.command == "quote" else config.db_path)
    try:
        service = RemitService(
            store, StaticRateProvider(), watchlist, clock or najm_clock.SystemClock(), ConsoleNotifier(out)
        )
        return _run(args, config.language, service, store, out)
    except RemitError as exc:
        print(f"error [{exc.code}]: {exc}", file=err)
        return 1
    finally:
        store.close()


def _run(args: argparse.Namespace, default_lang: str, service: RemitService, store: Store, out: TextIO) -> int:
    if args.command == "customer":
        if args.action == "add":
            store.add_customer(Customer(args.id, args.name, args.kyc, args.loyalty, args.lang or default_lang))
            print(f"added customer {args.id}", file=out)
        else:
            for c in store.list_customers():
                print(f"{c.id}  {c.name}  {c.kyc_tier}  {c.loyalty_tier}  {c.language}", file=out)
        return 0

    if args.command == "history":
        for t in service.history(args.customer):
            print(
                f"{t.created_at.isoformat()}  {t.id}  {t.corridor}  {t.send_amount}  fee {t.fee}  "
                f"-> {t.receive_amount}  to {t.recipient_name}",
                file=out,
            )
        return 0

    amount = Money(args.amount, args.send_currency)
    if args.command == "quote":
        _print_quote(service.quote(amount, args.receive_currency, express=args.express, delivery_method=args.delivery), out)
        return 0

    result = service.send(
        args.customer, amount, args.receive_currency, args.recipient, express=args.express, delivery_method=args.delivery
    )
    t = result.transfer
    print(f"sent {t.id}: {t.send_amount} (fee {t.fee}) -> {t.receive_amount} at {t.rate}", file=out)
    return 0
