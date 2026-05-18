from __future__ import annotations
from dataclasses import dataclass
from typing import Literal


@dataclass
class PaymentMethod:
    method: str


@dataclass
class CreditCard(PaymentMethod):
    last4: str


@dataclass
class PayPal(PaymentMethod):
    paypal_email: str


class PaymentMethodFactory:
    """
    Simple Factory: centralized creation for payment method objects.
    """

    @staticmethod
    def create(method: Literal["credit_card", "paypal"], **kwargs) -> PaymentMethod:
        if method == "credit_card":
            last4 = kwargs.get("last4")
            if not last4 or len(last4) != 4:
                raise ValueError("credit_card requires last4 (4 chars)")
            return CreditCard(method="credit_card", last4=last4)

        if method == "paypal":
            email = kwargs.get("email")
            if not email or "@" not in email:
                raise ValueError("paypal requires a valid email")
            return PayPal(method="paypal", paypal_email=email)

        raise ValueError(f"Unknown payment method: {method}")
