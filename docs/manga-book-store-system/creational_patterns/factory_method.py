from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import uuid4


@dataclass
class PaymentResult:
    transaction_id: str
    approved: bool


class PaymentProcessor(ABC):
    """
    Factory Method: concrete subclasses provide their own processing behavior.
    """

    @abstractmethod
    def process_payment(self, amount: float) -> PaymentResult:
        raise NotImplementedError


class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> PaymentResult:
        approved = amount > 0
        return PaymentResult(transaction_id=str(uuid4()), approved=approved)


class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> PaymentResult:
        approved = amount > 0
        return PaymentResult(transaction_id=str(uuid4()), approved=approved)
