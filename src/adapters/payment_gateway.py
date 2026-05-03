"""PaymentGateway adapter: abstract base and mock implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from ..orders.payment import PaymentMethod


class PaymentGateway(ABC):
    """Abstract base class for payment processing adapters.

    Concrete implementations must handle payment authorisation and
    refund workflows using the chosen payment provider's API.
    """

    @abstractmethod
    def process_payment(
        self,
        order_id: str,
        amount: float,
        method: PaymentMethod,
    ) -> bool:
        """Attempt to process a payment for an order.

        Args:
            order_id: ID of the order being paid.
            amount: Amount to charge.
            method: Payment method to use.

        Returns:
            True if the payment was successfully authorised, False otherwise.
        """

    @abstractmethod
    def refund_payment(self, payment_id: str) -> bool:
        """Attempt to refund a previously authorised payment.

        Args:
            payment_id: ID of the payment to refund.

        Returns:
            True if the refund was successful, False otherwise.
        """


class MockPaymentGateway(PaymentGateway):
    """In-memory mock payment gateway for testing and development.

    Simulates payment success or failure based on a configurable threshold
    and an ``always_fail`` flag.

    Attributes:
        _always_fail: When True, every payment attempt returns False.
        _failure_threshold: Payments above this amount fail (when not always_fail).
        _payment_records: Stores processed payment data keyed by order_id.
    """

    def __init__(
        self,
        always_fail: bool = False,
        failure_threshold: Optional[float] = None,
    ) -> None:
        """Initialise the MockPaymentGateway.

        Args:
            always_fail: If True all payment attempts will fail. Defaults to False.
            failure_threshold: Optional amount above which payments fail.
                               None means no threshold-based failures.
        """
        self._always_fail: bool = always_fail
        self._failure_threshold: Optional[float] = failure_threshold
        self._payment_records: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def payment_records(self) -> Dict[str, Any]:
        """Read-only view of all stored payment records."""
        return dict(self._payment_records)

    @property
    def always_fail(self) -> bool:
        """Whether the gateway is configured to always fail."""
        return self._always_fail

    @always_fail.setter
    def always_fail(self, value: bool) -> None:
        """Configure the gateway to always fail or succeed.

        Args:
            value: True to always fail; False to use normal logic.
        """
        self._always_fail = value

    # ------------------------------------------------------------------
    # PaymentGateway implementation
    # ------------------------------------------------------------------

    def process_payment(
        self,
        order_id: str,
        amount: float,
        method: PaymentMethod,
    ) -> bool:
        """Simulate processing a payment.

        Returns False when ``always_fail`` is True or when *amount* exceeds
        the configured ``failure_threshold``.

        Args:
            order_id: ID of the order being paid.
            amount: Amount to charge.
            method: Payment method used.

        Returns:
            True on simulated success, False on simulated failure.
        """
        if self._always_fail:
            return False
        if self._failure_threshold is not None and amount > self._failure_threshold:
            return False

        self._payment_records[order_id] = {
            "order_id": order_id,
            "amount": amount,
            "method": method.value,
            "status": "authorized",
        }
        return True

    def refund_payment(self, payment_id: str) -> bool:
        """Simulate refunding a payment.

        The mock always succeeds unless ``always_fail`` is set.

        Args:
            payment_id: ID of the payment to refund.

        Returns:
            True on simulated success, False when always_fail is True.
        """
        if self._always_fail:
            return False
        if payment_id in self._payment_records:
            self._payment_records[payment_id]["status"] = "refunded"
        return True
