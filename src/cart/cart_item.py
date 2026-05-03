"""CartItem domain model for the Manga Book Store system."""

from __future__ import annotations

import uuid
from typing import Any, Dict, Optional


class CartItem:
    """A single line item within a shopping cart.

    Stores a snapshot of the manga's title and price at the moment the
    item was added, so cart totals remain accurate if catalogue data changes.

    Attributes:
        _cart_item_id: Unique identifier for this cart line.
        _manga_id: Reference to the manga listing.
        _manga_title: Snapshot of the manga title at the time of adding.
        _quantity: Number of units requested.
        _unit_price_at_add: Price per unit when the item was added.
    """

    def __init__(
        self,
        manga_id: str,
        manga_title: str,
        quantity: int,
        unit_price_at_add: float,
        cart_item_id: Optional[str] = None,
    ) -> None:
        """Initialise a CartItem.

        Args:
            manga_id: ID of the manga being added.
            manga_title: Title snapshot at add-time.
            quantity: Units to add (must be >= 1).
            unit_price_at_add: Price per unit at add-time (must be >= 0).
            cart_item_id: Optional explicit UUID.

        Raises:
            ValueError: If quantity < 1 or unit_price_at_add < 0.
        """
        if quantity < 1:
            raise ValueError("quantity must be at least 1.")
        if unit_price_at_add < 0:
            raise ValueError("unit_price_at_add must be non-negative.")

        self._cart_item_id: str = cart_item_id or str(uuid.uuid4())
        self._manga_id: str = manga_id
        self._manga_title: str = manga_title
        self._quantity: int = quantity
        self._unit_price_at_add: float = unit_price_at_add

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def cart_item_id(self) -> str:
        """Unique cart-item identifier."""
        return self._cart_item_id

    @property
    def manga_id(self) -> str:
        """ID of the associated manga listing."""
        return self._manga_id

    @property
    def manga_title(self) -> str:
        """Snapshot of the manga title."""
        return self._manga_title

    @property
    def quantity(self) -> int:
        """Number of units in this line item."""
        return self._quantity

    @property
    def unit_price_at_add(self) -> float:
        """Price per unit when the item was first added."""
        return self._unit_price_at_add

    @property
    def line_total(self) -> float:
        """Computed total for this line (quantity × unit price)."""
        return self.compute_line_total()

    # ------------------------------------------------------------------
    # Behaviour
    # ------------------------------------------------------------------

    def compute_line_total(self) -> float:
        """Calculate and return the line total.

        Returns:
            Product of quantity and unit price.
        """
        return round(self._quantity * self._unit_price_at_add, 2)

    def increment_qty(self, amount: int = 1) -> None:
        """Increase the quantity by *amount*.

        Args:
            amount: Units to add (must be >= 1). Defaults to 1.

        Raises:
            ValueError: If amount < 1.
        """
        if amount < 1:
            raise ValueError("increment amount must be at least 1.")
        self._quantity += amount

    def decrement_qty(self, amount: int = 1) -> None:
        """Decrease the quantity by *amount*.

        Args:
            amount: Units to subtract (must be >= 1). Defaults to 1.

        Raises:
            ValueError: If amount < 1 or the result would drop below 1.
        """
        if amount < 1:
            raise ValueError("decrement amount must be at least 1.")
        if self._quantity - amount < 1:
            raise ValueError("Quantity cannot fall below 1; use Cart.remove_item() to delete the line.")
        self._quantity -= amount

    def update_quantity(self, qty: int) -> None:
        """Set the quantity to an explicit value.

        Args:
            qty: New quantity (must be >= 1).

        Raises:
            ValueError: If qty < 1.
        """
        if qty < 1:
            raise ValueError("quantity must be at least 1.")
        self._quantity = qty

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the cart item to a plain dictionary.

        Returns:
            Dictionary containing all field values.
        """
        return {
            "cart_item_id": self._cart_item_id,
            "manga_id": self._manga_id,
            "manga_title": self._manga_title,
            "quantity": self._quantity,
            "unit_price_at_add": self._unit_price_at_add,
            "line_total": self.compute_line_total(),
        }

    def __repr__(self) -> str:
        return (
            f"CartItem("
            f"cart_item_id={self._cart_item_id!r}, "
            f"manga_id={self._manga_id!r}, "
            f"qty={self._quantity!r}, "
            f"line_total={self.line_total!r})"
        )
