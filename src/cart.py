from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class CartItem:
    isbn: str
    quantity: int

    def set_quantity(self, qty: int) -> None:
        if qty <= 0:
            raise ValueError("qty must be > 0")
        self.quantity = qty


@dataclass
class Cart:
    customer_id: str
    items: Dict[str, CartItem] = field(default_factory=dict)  # isbn -> CartItem

    def add(self, isbn: str, qty: int = 1) -> None:
        if qty <= 0:
            raise ValueError("qty must be > 0")

        if isbn in self.items:
            self.items[isbn].quantity += qty
        else:
            self.items[isbn] = CartItem(isbn=isbn, quantity=qty)

    def remove(self, isbn: str) -> None:
        self.items.pop(isbn, None)

    def set_qty(self, isbn: str, qty: int) -> None:
        if isbn not in self.items:
            raise KeyError("isbn not in cart")
        if qty <= 0:
            self.remove(isbn)
        else:
            self.items[isbn].set_quantity(qty)

    def clear(self) -> None:
        self.items.clear()