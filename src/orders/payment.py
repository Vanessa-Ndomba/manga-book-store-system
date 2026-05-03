"""Payment domain models: PaymentTransaction, PaymentMethod, and PaymentStatus enums."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional


class PaymentMethod(Enum):
    """Accepted payment methods."""

    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    DEBIT_CARD = "debit_card"


class PaymentStatus(Enum):
    """Lifecycle states of a payment transaction."""

    PENDING = "pending"
    AUTHORIZED = "authorized"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentTransaction:
    """Records a payment attempt associated with a placed order.

    Attributes:
        _payment_id: Unique payment identifier.
        _order_id: ID of the order being paid.
        _method: PaymentMethod used.
        _status: Current PaymentStatus.
        _amount: Amount charged or to be charged.
        _created_at: UTC timestamp of transaction creation.
        _failure_reason: Optional description of why the transaction failed.
    """

    def __init__(
        self,
        order_id: str,
        method: PaymentMethod,
        amount: float,
        payment_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        """Initialise a PaymentTransaction.

        Args:
            order_id: ID of the associated order.
            method: Payment method used.
            amount: Transaction amount (must be > 0).
            payment_id: Optional explicit UUID.
            created_at: Optional explicit creation timestamp.

        Raises:
            ValueError: If amount is not positive.
        """
        if amount <= 0:
            raise ValueError("amount must be positive.")

        self._payment_id: str = payment_id or str(uuid.uuid4())
        self._order_id: str = order_id
        self._method: PaymentMethod = method
        self._status: PaymentStatus = PaymentStatus.PENDING
        self._amount: float = amount
        self._created_at: datetime = created_at or datetime.now(timezone.utc)
        self._failure_reason: Optional[str] = None

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def payment_id(self) -> str:
        """Unique payment transaction identifier."""
        return self._payment_id

    @property
    def order_id(self) -> str:
        """ID of the associated order."""
        return self._order_id

    @property
    def method(self) -> PaymentMethod:
        """Payment method used."""
        return self._method

    @property
    def status(self) -> PaymentStatus:
        """Current payment status."""
        return self._status

    @property
    def amount(self) -> float:
        """Transaction amount."""
        return self._amount

    @property
    def created_at(self) -> datetime:
        """UTC timestamp of transaction creation."""
        return self._created_at

    @property
    def failure_reason(self) -> Optional[str]:
        """Description of the failure, or None when not failed."""
        return self._failure_reason

    # ------------------------------------------------------------------
    # Behaviour
    # ------------------------------------------------------------------

    def authorize(self) -> None:
        """Mark the transaction as AUTHORIZED.

        Raises:
            RuntimeError: If the transaction is not currently PENDING.
        """
        if self._status != PaymentStatus.PENDING:
            raise RuntimeError(
                f"Cannot authorize a transaction with status '{self._status.value}'."
            )
        self._status = PaymentStatus.AUTHORIZED

    def fail(self, reason: str) -> None:
        """Mark the transaction as FAILED with a descriptive reason.

        Args:
            reason: Human-readable explanation of the failure.

        Raises:
            RuntimeError: If the transaction is not PENDING or AUTHORIZED.
            ValueError: If reason is empty.
        """
        if self._status not in (PaymentStatus.PENDING, PaymentStatus.AUTHORIZED):
            raise RuntimeError(
                f"Cannot fail a transaction with status '{self._status.value}'."
            )
        if not reason or not reason.strip():
            raise ValueError("failure reason must not be empty.")
        self._status = PaymentStatus.FAILED
        self._failure_reason = reason.strip()

    def refund(self) -> None:
        """Mark the transaction as REFUNDED.

        Raises:
            RuntimeError: If the transaction is not AUTHORIZED.
        """
        if self._status != PaymentStatus.AUTHORIZED:
            raise RuntimeError(
                f"Cannot refund a transaction with status '{self._status.value}'. "
                "Only AUTHORIZED transactions can be refunded."
            )
        self._status = PaymentStatus.REFUNDED

    def validate_amount(self) -> bool:
        """Return True if the transaction amount is valid (positive).

        Returns:
            True when amount > 0.
        """
        return self._amount > 0

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the transaction to a plain dictionary.

        Returns:
            Dictionary containing all field values.
        """
        return {
            "payment_id": self._payment_id,
            "order_id": self._order_id,
            "method": self._method.value,
            "status": self._status.value,
            "amount": self._amount,
            "created_at": self._created_at.isoformat(),
            "failure_reason": self._failure_reason,
        }

    def __repr__(self) -> str:
        return (
            f"PaymentTransaction("
            f"payment_id={self._payment_id!r}, "
            f"order_id={self._order_id!r}, "
            f"method={self._method.value!r}, "
            f"status={self._status.value!r}, "
            f"amount={self._amount!r})"
        )
