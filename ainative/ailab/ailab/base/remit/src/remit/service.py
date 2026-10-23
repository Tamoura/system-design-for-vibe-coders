"""RemitService: the one place where a transfer is orchestrated.

``send`` runs these steps in this order, and stops at the first failure:

    validate -> limits -> screening -> fee -> fx -> ledger -> store -> notify

* validate   the customer exists, the recipient is named, the corridor, amount and
             delivery method are allowed (errors: UnknownCustomer, InvalidRequest,
             UnknownCorridor, AmountOutOfRange, UnsupportedDeliveryMethod)
* limits     LimitExceeded; the customer is told ("transfer_failed") and an audit
             event is written
* screening  the sender's and the recipient's names against the watchlist: ScreeningHit;
             the customer gets a deliberately vague "transfer_failed" message
* fee, fx    priced now, or taken from a ``quote`` the caller already showed the
             customer (QuoteMismatch if it does not match, QuoteExpired after 60 s)
* ledger     the double-entry postings (remit.ledger)
* store      the Transfer row
* notify     "transfer_sent" in the customer's language. Notification is best effort:
             if the notifier raises NotificationError the transfer still stands and
             ``SendResult.notified`` is False.

Known limitation (D-SVC-1): the steps from ledger onwards are not one atomic unit. If
the store fails after the ledger has posted, the posting is not reversed.

Time comes only from the injected ``clock`` and ids from najmkit, so a service built
with a FixedClock and najmkit's SequentialIds is fully deterministic.
"""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from najmkit import audit, ids
from remit import ledger, notify
from remit.corridors import Corridor, get_corridor, validate_send
from remit.errors import (
    InvalidRequest,
    LimitExceeded,
    NotificationError,
    QuoteExpired,
    QuoteMismatch,
    ScreeningHit,
)
from remit.fees import quote_fee
from remit.fx import FxQuote, RateProvider, fx_quote
from remit.limits import LimitResult, check_limits
from remit.models import Customer, Transfer
from remit.money import Money
from remit.screening import screen_names
from remit.store import Store


@dataclass(frozen=True)
class Quote:
    corridor: Corridor
    send_amount: Money
    fee: Money
    total: Money  # what the customer pays: send_amount + fee
    fx: FxQuote
    express: bool
    delivery_method: str


@dataclass(frozen=True)
class SendResult:
    transfer: Transfer
    total_debited: Money  # send amount + fee
    limits: LimitResult  # the limit position *before* this transfer
    notified: bool  # False if the "transfer_sent" notification could not be delivered


class RemitService:
    def __init__(
        self,
        store: Store,
        rates: RateProvider,
        watchlist: Iterable[str],
        clock: Any,
        notifier: notify.Notifier,
    ) -> None:
        self.store = store
        self.rates = rates
        self.watchlist = list(watchlist)
        self.clock = clock  # anything with .now() -> aware datetime
        self.notifier = notifier

    # -- quoting -------------------------------------------------------------
    def quote(
        self,
        send_amount: Money,
        receive_currency: str,
        *,
        express: bool = False,
        delivery_method: str | None = None,
    ) -> Quote:
        """Price a transfer without sending it. The exchange rate is good for 60 seconds."""
        corridor = get_corridor(send_amount.currency, receive_currency)
        method = validate_send(corridor, send_amount, delivery_method)
        fee = quote_fee(send_amount, corridor, express=express)
        fx = fx_quote(send_amount, corridor, self.rates, self.clock.now())
        return Quote(corridor, send_amount, fee, send_amount + fee, fx, express, method)

    # -- sending -------------------------------------------------------------
    def send(
        self,
        customer_id: str,
        send_amount: Money,
        receive_currency: str,
        recipient_name: str,
        *,
        express: bool = False,
        delivery_method: str | None = None,
        quote: Quote | None = None,
    ) -> SendResult:
        now = self.clock.now()

        # 1. validate
        customer = self.store.require_customer(customer_id)
        recipient = recipient_name.strip()
        if not recipient:
            raise InvalidRequest("the recipient's name is required")
        corridor = get_corridor(send_amount.currency, receive_currency)
        method = validate_send(corridor, send_amount, delivery_method)

        # 2. limits
        limits = check_limits(customer.kyc_tier, self.store.list_transfers(customer.id), send_amount, now)
        if not limits.allowed:
            self._reject(customer, "limit_exceeded", corridor, send_amount, recipient)
            raise LimitExceeded(limits)

        # 3. screening (sender and recipient)
        screened = screen_names([customer.name, recipient], self.watchlist)
        if screened.hit:
            self._reject(customer, "needs_review", corridor, send_amount, recipient)
            raise ScreeningHit(screened.matches)

        # 4. fee and 5. fx: from the quote the customer saw, or priced now
        if quote is not None:
            if (quote.corridor.code, quote.send_amount, quote.express, quote.delivery_method) != (
                corridor.code,
                send_amount,
                express,
                method,
            ):
                raise QuoteMismatch("the quote does not match this transfer")
            if quote.fx.is_expired(now):
                raise QuoteExpired(f"the quote expired at {quote.fx.expires_at.isoformat()}")
            fee, fx = quote.fee, quote.fx
        else:
            fee = quote_fee(send_amount, corridor, express=express)
            fx = fx_quote(send_amount, corridor, self.rates, now)

        # 6. ledger
        transfer_id = ids.new_id("TRF")
        ledger.post_transfer(transfer_id, customer.id, send_amount, fee)

        # 7. store
        transfer = Transfer(
            id=transfer_id,
            customer_id=customer.id,
            corridor=corridor.code,
            send_amount=send_amount,
            fee=fee,
            receive_amount=fx.receive,
            rate=fx.rate,
            recipient_name=recipient,
            delivery_method=method,
            created_at=now,
            express=express,
        )
        self.store.save_transfer(transfer)

        # 8. notify (best effort), then the audit trail
        notified = self._notify(
            customer,
            "transfer_sent",
            transfer_id=transfer_id,
            recipient=recipient,
            send_amount=send_amount,
            fee=fee,
            receive_amount=fx.receive,
        )
        audit.log_event(
            "transfer.sent",
            transfer_id=transfer_id,
            customer_id=customer.id,
            corridor=corridor.code,
            send_amount=send_amount,
            fee=fee,
            express=express,
        )
        return SendResult(transfer, send_amount + fee, limits, notified)

    def history(self, customer_id: str) -> list[Transfer]:
        """The customer's transfers, oldest first."""
        return self.store.list_transfers(self.store.require_customer(customer_id).id)

    # -- helpers -------------------------------------------------------------
    def _notify(self, customer: Customer, template_id: str, **values: Any) -> bool:
        try:
            self.notifier.notify(customer, template_id, **values)
        except NotificationError as exc:
            audit.log_event("notification.failed", customer_id=customer.id, template=template_id, reason=exc.code)
            return False
        return True

    def _reject(self, customer: Customer, reason: str, corridor: Corridor, amount: Money, recipient: str) -> None:
        """Tell the customer, in their language, that the transfer was not made; audit it."""
        audit.log_event(
            "transfer.rejected",
            customer_id=customer.id,
            reason=reason,
            corridor=corridor.code,
            send_amount=amount,
        )
        self._notify(
            customer,
            "transfer_failed",
            recipient=recipient,
            send_amount=amount,
            reason=notify.failure_reason(reason, customer.language),
        )
