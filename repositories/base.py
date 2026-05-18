from __future__ import annotations

from typing import Generic, List, Optional, Protocol, TypeVar

T = TypeVar("T")
ID = TypeVar("ID")


class Repository(Protocol, Generic[T, ID]):
    """
    Generic repository interface (CRUD).
    Mirrors: Repository<T, ID> from the assignment prompt.
    """

    def save(self, entity: T) -> None:
        """Create or Update an entity."""
        ...

    def find_by_id(self, id: ID) -> Optional[T]:
        """Read an entity by ID."""
        ...

    def find_all(self) -> List[T]:
        """Read all entities."""
        ...

    def delete(self, id: ID) -> None:
        """Delete an entity by ID."""
        ...