"""Every error Remit raises on purpose.

All of them derive from RemitError, so a caller can catch one class. Each has a
stable machine-readable ``code`` that goes into audit events and CLI output.
Where it makes sense they also derive from the matching built-in (ValueError,
LookupError) so generic code keeps working.
"""
from __future__ import annotations

from typing import Any


class RemitError(Exception):
    """Base class for all Remit errors."""

    code = "remit_error"


# -- money ---------------------------------------------------------------
class InvalidAmount(RemitError, ValueError):
    code = "invalid_amount"


class UnknownCurrency(RemitError, ValueError):
    code = "unknown_currency"


class CurrencyMismatch(RemitError, ValueError):
    code = "currency_mismatch"


# -- corridors, fees, fx --------------------------------------------------
class UnknownCorridor(RemitError, LookupError):
    code = "unknown_corridor"


class AmountOutOfRange(RemitError, ValueError):
    code = "amount_out_of_range"


class UnsupportedDeliveryMethod(RemitError, ValueError):
    code = "unsupported_delivery_method"


class UnknownFeeSchedule(RemitError, LookupError):
    code = "unknown_fee_schedule"


class RateUnavailable(RemitError, LookupError):
    code = "rate_unavailable"


class QuoteExpired(RemitError):
    code = "quote_expired"


class QuoteMismatch(RemitError, ValueError):
    code = "quote_mismatch"


# -- limits, screening ----------------------------------------------------
class UnknownKycTier(RemitError, ValueError):
    code = "unknown_kyc_tier"


class LimitExceeded(RemitError):
    """The transfer would exceed a daily or monthly limit. ``result`` is the LimitResult."""

    code = "limit_exceeded"

    def __init__(self, result: Any) -> None:
        super().__init__(f"limit exceeded: {result.reason}")
        self.result = result


class ScreeningHit(RemitError):
    """A name matched the watchlist. ``matches`` lists (name, entry, score) tuples."""

    code = "screening_hit"

    def __init__(self, matches: Any) -> None:
        super().__init__("name screening hit: transfer held for review")
        self.matches = matches


# -- service, store, notify, ledger ----------------------------------------
class InvalidRequest(RemitError, ValueError):
    code = "invalid_request"


class UnknownCustomer(RemitError, LookupError):
    code = "unknown_customer"


class StoreError(RemitError):
    code = "store_error"


class UnknownTemplate(RemitError, LookupError):
    code = "unknown_template"


class UnsupportedLanguage(RemitError, ValueError):
    code = "unsupported_language"


class MissingTemplateVariable(RemitError, ValueError):
    code = "missing_template_variable"


class NotificationError(RemitError):
    code = "notification_error"


class DuplicatePosting(RemitError):
    code = "duplicate_posting"
