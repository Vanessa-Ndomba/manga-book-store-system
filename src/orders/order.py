"""Order domain model and OrderStatus enum for the Manga Book Store system."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from .order_item import OrderItem

if TYPE_CHECKING:
    from ..cart.cart import Cart


class OrderStatus(Enum):
    """Lifecycle states of a customer order."""

    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order:
    """Represents a placed customer order.

    Attributes:
        _order_id: Unique order identifier.
        _user_id: ID of the customer who placed the order.
        _items: List of OrderItem line items.
        _order_date: UTC timestamp when the order was placed.
        _status: Current OrderStatus.
        _total_amount: Computed grand total.
        _confirmation_number: Human-readable confirmation reference.
        _delivery_address: Address to deliver the order to.
    """

    def __init__(
        self,
        user_id: str,
        delivery_address: str,
        order_id: Optional[str] = None,
        order_date: Optional[datetime] = None,
        confirmation_number: Optional[str] = None,
    ) -> None:
        """Initialise an Order.

        Args:
            user_id: Customer ID.
            delivery_address: Delivery address string.
            order_id: Optional explicit UUID.
            order_date: Optional explicit order timestamp.
            confirmation_number: Optional explicit confirmation reference.

        Raises:
            ValueError: If delivery_address is empty.
        """
        if not delivery_address or not delivery_address.strip():
            raise ValueError("delivery_address must not be empty.")

        self._order_id: str = order_id or str(uuid.uuid4())
        self._user_id: str = user_id
        self._items: List[OrderItem] = []
        self._order_date: datetime = order_date or datetime.now(timezone.utc)
        self._status: OrderStatus = OrderStatus.PENDING
        self._total_amount: float = 0.0
        self._confirmation_number: str = confirmation_number or self._generate_confirmation()
        self._delivery_address: str = delivery_address.strip()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _generate_confirmation(self) -> str:
        """Generate a short human-readable confirmation number."""
        return f"ORD-{self._order_id[:8].upper()}"

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def order_id(self) -> str:
        """Unique order identifier."""
        return self._order_id

    @property
    def user_id(self) -> str:
        """ID of the customer who placed the order."""
        return self._user_id

    @property
    def order_date(self) -> datetime:
        """UTC timestamp when the order was placed."""
        return self._order_date

    @property
    def status(self) -> OrderStatus:
        """Current order status."""
        return self._status

    @property
    def total_amount(self) -> float:
        """Grand total for the order."""
        return self._total_amount

    @property
    def confirmation_number(self) -> str:
        """Human-readable confirmation reference."""
        return self._confirmation_number

    @property
    def delivery_address(self) -> str:
        """Delivery address for the order."""
        return self._delivery_address

    @delivery_address.setter
    def delivery_address(self, value: str) -> None:
        """Update the delivery address.

        Raises:
            ValueError: If value is blank.
        """
        if not value or not value.strip():
            raise ValueError("delivery_address must not be empty.")
        self._delivery_address = value.strip()

    # ------------------------------------------------------------------
    # Item management
    # ------------------------------------------------------------------

    def add_item(self, item: OrderItem) -> None:
        """Append an OrderItem to this order and recompute the total.

        Args:
            item: The OrderItem to add.
        """
        self._items.append(item)
        self._total_amount = self.compute_total()

    def get_items(self) -> List[OrderItem]:
        """Return a shallow copy of the order's line items.

        Returns:
            List of OrderItem objects.
        """
        return list(self._items)

    # ------------------------------------------------------------------
    # Class-level factory
    # ------------------------------------------------------------------

    @classmethod
    def place_from_cart(cls, cart: "Cart") -> "Order":
        """Create an Order by converting items from an active Cart.

        This factory method snapshots every cart item into an OrderItem,
        computes the total, and leaves the cart to be converted separately.

        Args:
            cart: An ACTIVE, non-empty Cart instance.

        Returns:
            A new Order in PENDING status.

        Raises:
            RuntimeError: If the cart is empty.
        """
        if cart.is_empty():
            raise RuntimeError("Cannot create an order from an empty cart.")

        order = cls(user_id=cart.user_id, delivery_address="TBD")
        for ci in cart.get_items():
            order.add_item(
                OrderItem(
                    manga_id=ci.manga_id,
                    manga_title=ci.manga_title,
                    quantity=ci.quantity,
                    unit_price=ci.unit_price_at_add,
                )
            )
        return order

    # ------------------------------------------------------------------
    # Behaviour
    # ------------------------------------------------------------------

    def cancel(self) -> None:
        """Cancel the order.

        Raises:
            RuntimeError: If the order is not in PENDING or PROCESSING status.
        """
        if self._status not in (OrderStatus.PENDING, OrderStatus.PROCESSING):
            raise RuntimeError(
                f"Cannot cancel an order with status '{self._status.value}'. "
                "Only PENDING or PROCESSING orders can be cancelled."
            )
        self._status = OrderStatus.CANCELLED

    def update_status(self, status: OrderStatus) -> None:
        """Transition the order to a new status.

        Args:
            status: The new OrderStatus value.

        Raises:
            ValueError: If status is not an OrderStatus instance.
        """
        if not isinstance(status, OrderStatus):
            raise ValueError(f"status must be an OrderStatus enum member, got {type(status)}.")
        self._status = status

    def compute_total(self) -> float:
        """Sum all order-item line totals.

        Returns:
            Grand total rounded to 2 decimal places.
        """
        return round(sum(item.line_total for item in self._items), 2)

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the order to a plain dictionary.

        Returns:
            Dictionary representation of the order.
        """
        return {
            "order_id": self._order_id,
            "user_id": self._user_id,
            "order_date": self._order_date.isoformat(),
            "status": self._status.value,
            "total_amount": self._total_amount,
            "confirmation_number": self._confirmation_number,
            "delivery_address": self._delivery_address,
            "items": [item.to_dict() for item in self._items],
        }

    def __repr__(self) -> str:
        return (
            f"Order("
            f"order_id={self._order_id!r}, "
            f"user_id={self._user_id!r}, "
            f"status={self._status.value!r}, "
            f"total={self._total_amount!r})"
        )
