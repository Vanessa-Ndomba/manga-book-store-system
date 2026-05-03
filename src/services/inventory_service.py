"""InventoryService for the Manga Book Store system."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..adapters.inventory_repository import InventoryRepository


class InventoryService:
    """Service layer for managing stock levels.

    Wraps an :class:`~adapters.inventory_repository.InventoryRepository`
    and provides higher-level operations such as stock validation, deduction,
    and addition.

    Attributes:
        _inventory_repo: The underlying inventory storage adapter.
    """

    def __init__(self, inventory_repo: "InventoryRepository") -> None:
        """Initialise the InventoryService.

        Args:
            inventory_repo: Concrete InventoryRepository implementation.
        """
        self._inventory_repo = inventory_repo

    def get_stock(self, manga_id: str) -> int:
        """Return the current stock level for a manga.

        Args:
            manga_id: ID of the manga to query.

        Returns:
            Integer stock quantity (0 if the manga has no stock record).
        """
        return self._inventory_repo.get_stock(manga_id)

    def update_stock(self, manga_id: str, quantity: int) -> None:
        """Set the absolute stock level for a manga.

        Args:
            manga_id: ID of the manga to update.
            quantity: New absolute stock level (must be >= 0).

        Raises:
            ValueError: If quantity is negative.
        """
        if quantity < 0:
            raise ValueError("quantity must be non-negative.")
        self._inventory_repo.update_stock(manga_id, quantity)

    def validate_stock(self, manga_id: str, requested_qty: int) -> bool:
        """Return True if sufficient stock is available for the requested quantity.

        Args:
            manga_id: ID of the manga.
            requested_qty: Number of units requested.

        Returns:
            True when available stock >= requested_qty.

        Raises:
            ValueError: If requested_qty is less than 1.
        """
        if requested_qty < 1:
            raise ValueError("requested_qty must be at least 1.")
        return self._inventory_repo.get_stock(manga_id) >= requested_qty

    def deduct_stock(self, manga_id: str, quantity: int) -> None:
        """Reduce the stock level by *quantity* units.

        Args:
            manga_id: ID of the manga.
            quantity: Units to deduct (must be >= 1).

        Raises:
            ValueError: If quantity < 1 or if stock would go negative.
        """
        if quantity < 1:
            raise ValueError("quantity must be at least 1.")
        current = self._inventory_repo.get_stock(manga_id)
        if current < quantity:
            raise ValueError(
                f"Cannot deduct {quantity} units from manga '{manga_id}'; "
                f"only {current} in stock."
            )
        self._inventory_repo.update_stock(manga_id, current - quantity)

    def add_stock(self, manga_id: str, quantity: int) -> None:
        """Increase the stock level by *quantity* units.

        Args:
            manga_id: ID of the manga.
            quantity: Units to add (must be >= 1).

        Raises:
            ValueError: If quantity < 1.
        """
        if quantity < 1:
            raise ValueError("quantity must be at least 1.")
        current = self._inventory_repo.get_stock(manga_id)
        self._inventory_repo.update_stock(manga_id, current + quantity)
