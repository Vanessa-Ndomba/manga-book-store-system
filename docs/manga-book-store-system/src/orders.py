from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class OrderStatus(str, Enum):
    CREATED = "CREATED"
    PAYMENT_PENDING = "PAYMENT_PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


@dataclass
class OrderItem:
    isbn: str
    title: str
    unit_price: float
    quantity: int

    def line_total(self) -> float:
        return self.unit_price * self.quantity


@dataclass
class Order:
    order_id: str
    customer_id: str
    shipping_address: str
    items: List[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.CREATED
    payment_transaction_id: Optional[str] = None

    def total(self) -> float:
        return sum(i.line_total() for i in self.items)

    def mark_payment_pending(self) -> None:
        if self.status != OrderStatus.CREATED:
            raise ValueError("Order must be CREATED first")
        self.status = OrderStatus.PAYMENT_PENDING

    def confirm(self, txn_id: str) -> None:
        if self.status != OrderStatus.PAYMENT_PENDING:
            raise ValueError("Order must be PAYMENT_PENDING to confirm")
        self.status = OrderStatus.CONFIRMED
        self.payment_transaction_id = txn_id