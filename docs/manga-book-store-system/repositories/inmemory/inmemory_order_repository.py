from __future__ import annotations

from typing import Dict, List, Optional

from repositories.order_repository import OrderRepository
from src.orders import Order


class InMemoryOrderRepository(OrderRepository):
    """
    HashMap/dict-backed repository for Orders.
    """

    def __init__(self) -> None:
        self._storage: Dict[str, Order] = {}

    def save(self, entity: Order) -> None:
        self._storage[entity.order_id] = entity

    def find_by_id(self, id: str) -> Optional[Order]:
        return self._storage.get(id)

    def find_all(self) -> List[Order]:
        return list(self._storage.values())

    def delete(self, id: str) -> None:
        self._storage.pop(id, None)