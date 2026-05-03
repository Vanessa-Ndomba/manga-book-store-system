"""InventoryRepository adapter: abstract base and mock implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict


class InventoryRepository(ABC):
    """Abstract base class for inventory storage adapters.

    Concrete implementations connect to a database, external API, or
    other persistent store to read and write stock levels.
    """

    @abstractmethod
    def get_stock(self, manga_id: str) -> int:
        """Return the current stock level for a manga.

        Args:
            manga_id: ID of the manga to query.

        Returns:
            Integer stock quantity.
        """

    @abstractmethod
    def update_stock(self, manga_id: str, quantity: int) -> None:
        """Set the absolute stock level for a manga.

        Args:
            manga_id: ID of the manga to update.
            quantity: New absolute stock quantity (must be >= 0).
        """

    @abstractmethod
    def reserve_stock(self, manga_id: str, quantity: int) -> bool:
        """Attempt to reserve a quantity of stock for an order.

        Reserved stock is deducted from the available level immediately,
        pending fulfilment.

        Args:
            manga_id: ID of the manga to reserve.
            quantity: Units to reserve (must be >= 1).

        Returns:
            True when the reservation succeeded, False if insufficient stock.
        """

    @abstractmethod
    def release_stock(self, manga_id: str, quantity: int) -> None:
        """Return previously reserved stock to the available pool.

        Called when an order is cancelled or a reservation is voided.

        Args:
            manga_id: ID of the manga whose stock is being released.
            quantity: Units to return (must be >= 1).
        """


class MockInventoryRepository(InventoryRepository):
    """In-memory mock inventory repository for testing and development.

    Uses a plain dictionary to track stock levels so no database is needed.

    Attributes:
        _stock: Mapping of manga_id → available stock quantity.
    """

    def __init__(self, initial_stock: Dict[str, int] | None = None) -> None:
        """Initialise the mock repository.

        Args:
            initial_stock: Optional pre-populated stock dictionary.
                           Defaults to an empty store.
        """
        self._stock: Dict[str, int] = dict(initial_stock) if initial_stock else {}

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def stock(self) -> Dict[str, int]:
        """Read-only snapshot of the current stock dictionary."""
        return dict(self._stock)

    # ------------------------------------------------------------------
    # InventoryRepository implementation
    # ------------------------------------------------------------------

    def get_stock(self, manga_id: str) -> int:
        """Return the current stock for *manga_id*, defaulting to 0.

        Args:
            manga_id: ID of the manga to query.

        Returns:
            Current stock level (0 if manga has no record).
        """
        return self._stock.get(manga_id, 0)

    def update_stock(self, manga_id: str, quantity: int) -> None:
        """Set the absolute stock level.

        Args:
            manga_id: ID of the manga.
            quantity: New stock level (must be >= 0).

        Raises:
            ValueError: If quantity is negative.
        """
        if quantity < 0:
            raise ValueError(f"Stock quantity for '{manga_id}' cannot be negative.")
        self._stock[manga_id] = quantity

    def reserve_stock(self, manga_id: str, quantity: int) -> bool:
        """Deduct *quantity* units from available stock if possible.

        Args:
            manga_id: ID of the manga to reserve.
            quantity: Units to reserve (must be >= 1).

        Returns:
            True when reservation succeeded, False when insufficient stock.

        Raises:
            ValueError: If quantity < 1.
        """
        if quantity < 1:
            raise ValueError("reserve quantity must be at least 1.")
        current = self._stock.get(manga_id, 0)
        if current < quantity:
            return False
        self._stock[manga_id] = current - quantity
        return True

    def release_stock(self, manga_id: str, quantity: int) -> None:
        """Return *quantity* units to available stock.

        Args:
            manga_id: ID of the manga whose stock is being released.
            quantity: Units to return (must be >= 1).

        Raises:
            ValueError: If quantity < 1.
        """
        if quantity < 1:
            raise ValueError("release quantity must be at least 1.")
        current = self._stock.get(manga_id, 0)
        self._stock[manga_id] = current + quantity

    def get_all_stock(self) -> Dict[str, int]:
        """Return a copy of all stock records.

        Returns:
            Dictionary mapping manga_id to current stock level.
        """
        return dict(self._stock)
