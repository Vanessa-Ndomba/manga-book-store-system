from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Manga:
    isbn: str
    title: str
    author: str
    genres: List[str] = field(default_factory=list)
    price: float = 0.0
     def __post_init__(self):

        if self.price < 0:
            raise ValueError(
                "Price cannot be negative"
            )


@dataclass
class InventoryItem:
    isbn: str
    stock_on_hand: int = 0

    def can_fulfill(self, qty: int) -> bool:
        return qty > 0 and self.stock_on_hand >= qty

    def reserve(self, qty: int) -> None:
        if qty <= 0:
            raise ValueError("qty must be > 0")
        if self.stock_on_hand < qty:
            raise ValueError("Insufficient stock")
        self.stock_on_hand -= qty

    def restock(self, qty: int) -> None:
        if qty <= 0:
            raise ValueError("qty must be > 0")
        self.stock_on_hand += qty
