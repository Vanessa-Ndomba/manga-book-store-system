from __future__ import annotations

from typing import Protocol

from repositories.base import Repository
from src.orders import Order


class OrderRepository(Repository[Order, str], Protocol):
    """
    Entity-specific repository interface for Orders.
    ID is order_id (str).
    """
    pass