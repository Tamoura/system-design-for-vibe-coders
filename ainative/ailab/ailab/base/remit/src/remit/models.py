"""Plain data classes shared by the store, the service and the CLI."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from remit.money import Money

KYC_TIERS = ("T1", "T2", "T3")
LOYALTY_TIERS = ("none", "silver", "gold")
LANGUAGES = ("en", "ar")


@dataclass(frozen=True)
class Customer:
    id: str
    name: str
    kyc_tier: str  # one of KYC_TIERS
    loyalty_tier: str = "none"  # one of LOYALTY_TIERS
    language: str = "en"  # one of LANGUAGES: the language of notifications

    def __post_init__(self) -> None:
        if self.kyc_tier not in KYC_TIERS:
            raise ValueError(f"kyc_tier must be one of {KYC_TIERS}, got {self.kyc_tier!r}")
        if self.loyalty_tier not in LOYALTY_TIERS:
            raise ValueError(f"loyalty_tier must be one of {LOYALTY_TIERS}, got {self.loyalty_tier!r}")
        if self.language not in LANGUAGES:
            raise ValueError(f"language must be one of {LANGUAGES}, got {self.language!r}")


@dataclass(frozen=True)
class Transfer:
    id: str
    customer_id: str
    corridor: str  # corridor code such as "QAR-INR"
    send_amount: Money  # what is sent (QAR), not including the fee
    fee: Money  # QAR
    receive_amount: Money  # what the recipient gets, in the receive currency
    rate: Decimal  # the customer rate that was applied
    recipient_name: str
    delivery_method: str
    created_at: datetime  # aware, UTC
    express: bool = False
    status: str = "completed"
