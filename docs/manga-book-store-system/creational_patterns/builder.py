from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from uuid import uuid4

from src.orders import Order, OrderItem


@dataclass
class OrderBuilder:
    """
    Builder: build complex Order objects step-by-step (variable items + validation).
    """
    customer_id: str
    shipping_address: Optional[str] = None
    _items: List[OrderItem] = field(default_factory=list)

    def ship_to(self, address: str) -> "OrderBuilder":
        if not address or not address.strip():
            raise ValueError("shipping address required")
        self.shipping_address = address.strip()
        return self

    def add_item(self, isbn: str, title: str, unit_price: float, quantity: int) -> "OrderBuilder":
        if not isbn:
            raise ValueError("isbn required")
        if unit_price < 0:
            raise ValueError("unit_price must be >= 0")
        if quantity <= 0:
            raise ValueError("quantity must be > 0")
        self._items.append(OrderItem(isbn=isbn, title=title, unit_price=unit_price, quantity=quantity))
        return self

    def build(self) -> Order:
        if not self.shipping_address:
            raise ValueError("shipping address must be set (ship_to)")
        if not self._items:
            raise ValueError("order must contain at least one item")

        return Order(
            order_id=str(uuid4()),
            customer_id=self.customer_id,
            shipping_address=self.shipping_address,
            items=list(self._items),
        )
