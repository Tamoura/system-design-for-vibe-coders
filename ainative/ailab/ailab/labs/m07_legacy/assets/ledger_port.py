# ailab/labs/m07_legacy/assets/ledger_port.py
"""A seam for the ledger tests: one way to get a ledger before and after the refactor.

Copy this file to ``tests/ledger_port.py``. Write your characterization tests against
``make_ledger()`` and ``ledger_of(service)``, never against ``remit.ledger`` directly. Today they
reach the module-level functions; once ``remit.ledger.Ledger`` exists they use it, so the same tests
run before and after the refactor and tell you whether behaviour changed.

One trap: before the refactor ``make_ledger()`` wipes the shared legacy books, so do not call it after
a ``send`` in the same test. Use ``ledger_of(service)`` to look at what a service posted.
"""
from __future__ import annotations

from remit import ledger as _ledger_module


class _ModuleLedger:
    """The legacy module-level functions, wearing the shape of the new Ledger class."""

    def __init__(self, fresh: bool = True) -> None:
        if fresh:
            _ledger_module.reset()  # the legacy state is shared, so "a new ledger" means "wipe it"

    def post_transfer(self, transfer_id, customer_id, send_amount, fee):
        return _ledger_module.post_transfer(transfer_id, customer_id, send_amount, fee)

    def balance(self, account):
        return _ledger_module.balance(account)

    def accounts(self):
        return _ledger_module.accounts()

    def journal(self):
        return _ledger_module.journal()


def make_ledger():
    """A fresh, empty ledger: ``Ledger()`` once the class exists, the wrapped module before."""
    ledger_class = getattr(_ledger_module, "Ledger", None)
    return ledger_class() if ledger_class is not None else _ModuleLedger()


def ledger_of(service):
    """The ledger a RemitService posts to (``service.ledger`` once the service owns one)."""
    own = getattr(service, "ledger", None)
    return own if own is not None else _ModuleLedger(fresh=False)
