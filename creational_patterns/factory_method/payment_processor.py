"""
Factory Method Pattern — PaymentProcessor

Justification: Different payment providers (credit card, PayPal) share a common
interface but differ in how they authenticate and charge.  The Factory Method
pattern lets each PaymentProcessorCreator subclass decide which concrete
processor to instantiate, keeping the order-processing workflow provider-agnostic.
"""
from __future__ import annotations
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional


@dataclass
class PaymentResult:
    """Holds the outcome of a payment attempt."""
    success: bool
    transaction_id: str
    amount: Decimal
    provider: str
    failure_reason: Optional[str] = None

    def __repr__(self) -> str:
        status = "OK" if self.success else f"FAILED({self.failure_reason})"
        return f"PaymentResult({status}, txn={self.transaction_id!r}, {self.amount} via {self.provider})"


# ── Product interface ────────────────────────────────────────────────────────

class PaymentProcessor(ABC):
    """Abstract product: processes a payment and returns a PaymentResult."""

    @abstractmethod
    def process(self, order_id: str, amount: Decimal) -> PaymentResult:
        """Attempt to charge *amount* for *order_id*."""

    @abstractmethod
    def refund(self, transaction_id: str, amount: Decimal) -> PaymentResult:
        """Issue a refund for a previous transaction."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Human-readable provider identifier."""


# ── Concrete products ────────────────────────────────────────────────────────

class CreditCardProcessor(PaymentProcessor):
    """Concrete processor for credit/debit card payments."""

    def __init__(self, card_number: str, expiry: str, cvv: str):
        if len(card_number) < 13:
            raise ValueError("Card number must be at least 13 digits")
        self._card_last4 = card_number[-4:]
        self._expiry = expiry
        self._cvv = cvv

    @property
    def provider_name(self) -> str:
        return "CreditCard"

    def process(self, order_id: str, amount: Decimal) -> PaymentResult:
        if amount <= 0:
            return PaymentResult(
                success=False,
                transaction_id="",
                amount=amount,
                provider=self.provider_name,
                failure_reason="Amount must be positive",
            )
        txn_id = f"CC-{uuid.uuid4().hex[:12].upper()}"
        return PaymentResult(
            success=True,
            transaction_id=txn_id,
            amount=amount,
            provider=self.provider_name,
        )

    def refund(self, transaction_id: str, amount: Decimal) -> PaymentResult:
        refund_id = f"CC-REF-{uuid.uuid4().hex[:8].upper()}"
        return PaymentResult(
            success=True,
            transaction_id=refund_id,
            amount=amount,
            provider=self.provider_name,
        )


class PayPalProcessor(PaymentProcessor):
    """Concrete processor for PayPal payments."""

    def __init__(self, paypal_email: str):
        if "@" not in paypal_email:
            raise ValueError("Invalid PayPal email address")
        self._paypal_email = paypal_email

    @property
    def provider_name(self) -> str:
        return "PayPal"

    def process(self, order_id: str, amount: Decimal) -> PaymentResult:
        if amount <= 0:
            return PaymentResult(
                success=False,
                transaction_id="",
                amount=amount,
                provider=self.provider_name,
                failure_reason="Amount must be positive",
            )
        txn_id = f"PP-{uuid.uuid4().hex[:12].upper()}"
        return PaymentResult(
            success=True,
            transaction_id=txn_id,
            amount=amount,
            provider=self.provider_name,
        )

    def refund(self, transaction_id: str, amount: Decimal) -> PaymentResult:
        refund_id = f"PP-REF-{uuid.uuid4().hex[:8].upper()}"
        return PaymentResult(
            success=True,
            transaction_id=refund_id,
            amount=amount,
            provider=self.provider_name,
        )


# ── Creator (abstract) ───────────────────────────────────────────────────────

class PaymentProcessorCreator(ABC):
    """Abstract creator; subclasses implement factory_method() to instantiate processors."""

    @abstractmethod
    def factory_method(self) -> PaymentProcessor:
        """Return a concrete PaymentProcessor instance."""

    def process_payment(self, order_id: str, amount: Decimal) -> PaymentResult:
        """
        Template method: uses factory_method() to obtain a processor,
        then delegates the actual payment call.
        """
        processor = self.factory_method()
        return processor.process(order_id, amount)


# ── Concrete creators ────────────────────────────────────────────────────────

class CreditCardProcessorCreator(PaymentProcessorCreator):
    """Creator that produces CreditCardProcessor instances."""

    def __init__(self, card_number: str, expiry: str, cvv: str):
        self._card_number = card_number
        self._expiry = expiry
        self._cvv = cvv

    def factory_method(self) -> CreditCardProcessor:
        return CreditCardProcessor(self._card_number, self._expiry, self._cvv)


class PayPalProcessorCreator(PaymentProcessorCreator):
    """Creator that produces PayPalProcessor instances."""

    def __init__(self, paypal_email: str):
        self._paypal_email = paypal_email

    def factory_method(self) -> PayPalProcessor:
        return PayPalProcessor(self._paypal_email)
