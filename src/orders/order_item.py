"""OrderItem domain model for the Manga Book Store system."""

from __future__ import annotations

import uuid
from typing import Any, Dict, Optional


class OrderItem:
    """A single line item within a placed order.

    Snapshots the manga title and price at the moment the order was placed.

    Attributes:
        _order_item_id: Unique identifier for this order line.
        _manga_id: Reference to the manga listing.
        _manga_title: Snapshot of the manga title at order time.
        _quantity: Number of units ordered.
        _unit_price: Price per unit when the order was placed.
    """

    def __init__(
        self,
        manga_id: str,
        manga_title: str,
        quantity: int,
        unit_price: float,
        order_item_id: Optional[str] = None,
    ) -> None:
        """Initialise an OrderItem.

        Args:
            manga_id: ID of the manga.
            manga_title: Title snapshot at order time.
            quantity: Units ordered (must be >= 1).
            unit_price: Price per unit at order time (must be >= 0).
            order_item_id: Optional explicit UUID.

        Raises:
            ValueError: If quantity < 1 or unit_price < 0.
        """
        if quantity < 1:
            raise ValueError("quantity must be at least 1.")
        if unit_price < 0:
            raise ValueError("unit_price must be non-negative.")

        self._order_item_id: str = order_item_id or str(uuid.uuid4())
        self._manga_id: str = manga_id
        self._manga_title: str = manga_title
        self._quantity: int = quantity
        self._unit_price: float = unit_price

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def order_item_id(self) -> str:
        """Unique order-item identifier."""
        return self._order_item_id

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
        """Number of units in this order line."""
        return self._quantity

    @property
    def unit_price(self) -> float:
        """Price per unit at order time."""
        return self._unit_price

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
            Product of quantity and unit price, rounded to 2 decimal places.
        """
        return round(self._quantity * self._unit_price, 2)

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the order item to a plain dictionary.

        Returns:
            Dictionary containing all field values.
        """
        return {
            "order_item_id": self._order_item_id,
            "manga_id": self._manga_id,
            "manga_title": self._manga_title,
            "quantity": self._quantity,
            "unit_price": self._unit_price,
            "line_total": self.compute_line_total(),
        }

    def __repr__(self) -> str:
        return (
            f"OrderItem("
            f"order_item_id={self._order_item_id!r}, "
            f"manga_id={self._manga_id!r}, "
            f"qty={self._quantity!r}, "
            f"line_total={self.line_total!r})"
        )
