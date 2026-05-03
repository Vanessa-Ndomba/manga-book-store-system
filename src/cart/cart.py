"""Cart domain model and CartStatus enum for the Manga Book Store system."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from .cart_item import CartItem


class CartStatus(Enum):
    """Possible lifecycle states of a shopping cart."""

    ACTIVE = "active"
    CONVERTED = "converted"
    ABANDONED = "abandoned"
    EXPIRED = "expired"


class Cart:
    """Shopping cart (ShoppingCart in the domain model).

    Maintains a collection of CartItem line items for a single user and
    computes the running total.

    Attributes:
        _cart_id: Unique cart identifier.
        _user_id: Owner's user ID.
        _items: Ordered list of CartItem objects.
        _status: Current CartStatus of the cart.
        _created_at: UTC timestamp of cart creation.
        _updated_at: UTC timestamp of the last modification.
    """

    def __init__(
        self,
        user_id: str,
        cart_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        """Initialise a Cart.

        Args:
            user_id: ID of the owning user.
            cart_id: Optional explicit UUID.
            created_at: Optional explicit creation timestamp.
        """
        now = created_at or datetime.now(timezone.utc)
        self._cart_id: str = cart_id or str(uuid.uuid4())
        self._user_id: str = user_id
        self._items: List[CartItem] = []
        self._status: CartStatus = CartStatus.ACTIVE
        self._created_at: datetime = now
        self._updated_at: datetime = now

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def cart_id(self) -> str:
        """Unique cart identifier."""
        return self._cart_id

    @property
    def user_id(self) -> str:
        """ID of the user who owns this cart."""
        return self._user_id

    @property
    def status(self) -> CartStatus:
        """Current lifecycle status of the cart."""
        return self._status

    @property
    def created_at(self) -> datetime:
        """UTC timestamp when the cart was created."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """UTC timestamp of the last modification."""
        return self._updated_at

    @property
    def item_count(self) -> int:
        """Total number of individual units across all line items."""
        return sum(item.quantity for item in self._items)

    @property
    def total_amount(self) -> float:
        """Computed grand total for the cart."""
        return self.calculate_total()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _touch(self) -> None:
        """Update the last-modified timestamp."""
        self._updated_at = datetime.now(timezone.utc)

    def _assert_active(self) -> None:
        """Raise RuntimeError unless the cart is ACTIVE."""
        if self._status != CartStatus.ACTIVE:
            raise RuntimeError(f"Cannot modify a cart with status '{self._status.value}'.")

    # ------------------------------------------------------------------
    # Item management
    # ------------------------------------------------------------------

    def add_item(
        self,
        manga_id: str,
        manga_title: str,
        quantity: int,
        unit_price: float,
    ) -> CartItem:
        """Add a manga to the cart or increase its quantity if already present.

        Args:
            manga_id: ID of the manga to add.
            manga_title: Snapshot title.
            quantity: Units to add (must be >= 1).
            unit_price: Price per unit at add-time.

        Returns:
            The affected (new or updated) CartItem.

        Raises:
            RuntimeError: If the cart is not ACTIVE.
            ValueError: If quantity < 1 or unit_price < 0.
        """
        self._assert_active()
        existing = self.get_item(manga_id)
        if existing:
            existing.increment_qty(quantity)
            self._touch()
            return existing
        item = CartItem(manga_id, manga_title, quantity, unit_price)
        self._items.append(item)
        self._touch()
        return item

    def remove_item(self, manga_id: str) -> None:
        """Remove the line item for the given manga.

        Args:
            manga_id: ID of the manga to remove.

        Raises:
            RuntimeError: If the cart is not ACTIVE.
            KeyError: If no item with that manga_id exists.
        """
        self._assert_active()
        for i, item in enumerate(self._items):
            if item.manga_id == manga_id:
                self._items.pop(i)
                self._touch()
                return
        raise KeyError(f"No cart item found for manga_id '{manga_id}'.")

    def update_quantity(self, manga_id: str, qty: int) -> None:
        """Update the quantity of an existing cart item.

        Args:
            manga_id: ID of the manga to update.
            qty: New quantity (must be >= 1).

        Raises:
            RuntimeError: If the cart is not ACTIVE.
            KeyError: If no item with that manga_id exists.
            ValueError: If qty < 1.
        """
        self._assert_active()
        item = self.get_item(manga_id)
        if item is None:
            raise KeyError(f"No cart item found for manga_id '{manga_id}'.")
        item.update_quantity(qty)
        self._touch()

    def get_item(self, manga_id: str) -> Optional[CartItem]:
        """Return the CartItem for the given manga_id, or None.

        Args:
            manga_id: Manga to look up.

        Returns:
            Matching CartItem or None.
        """
        for item in self._items:
            if item.manga_id == manga_id:
                return item
        return None

    def get_items(self) -> List[CartItem]:
        """Return a shallow copy of the item list.

        Returns:
            List of CartItem objects.
        """
        return list(self._items)

    def is_empty(self) -> bool:
        """Return True if the cart has no line items."""
        return len(self._items) == 0

    # ------------------------------------------------------------------
    # Financials
    # ------------------------------------------------------------------

    def calculate_total(self) -> float:
        """Sum all line totals and return the grand total.

        Returns:
            Grand total rounded to 2 decimal places.
        """
        return round(sum(item.line_total for item in self._items), 2)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """Remove all items from the cart.

        Raises:
            RuntimeError: If the cart is not ACTIVE.
        """
        self._assert_active()
        self._items.clear()
        self._touch()

    def convert_to_order(self) -> None:
        """Mark the cart as CONVERTED (i.e. an order has been placed).

        Raises:
            RuntimeError: If the cart is not ACTIVE or is empty.
        """
        self._assert_active()
        if self.is_empty():
            raise RuntimeError("Cannot convert an empty cart to an order.")
        self._status = CartStatus.CONVERTED
        self._touch()

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the cart to a plain dictionary.

        Returns:
            Dictionary representation of the cart and its items.
        """
        return {
            "cart_id": self._cart_id,
            "user_id": self._user_id,
            "status": self._status.value,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat(),
            "items": [item.to_dict() for item in self._items],
            "total_amount": self.calculate_total(),
        }

    def __repr__(self) -> str:
        return (
            f"Cart("
            f"cart_id={self._cart_id!r}, "
            f"user_id={self._user_id!r}, "
            f"status={self._status.value!r}, "
            f"items={len(self._items)!r})"
        )
