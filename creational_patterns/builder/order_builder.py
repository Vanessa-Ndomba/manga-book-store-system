"""
Builder Pattern — OrderBuilder

Justification: An Order is a complex object with many optional fields
(delivery address, payment method, discount codes, gift wrapping, special
notes).  The Builder pattern lets the system compose an Order step by step
and validate the result before finalising it, preventing partially-initialised
orders from entering the system.
"""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Optional


class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    DEBIT_CARD = "debit_card"


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class OrderItem:
    manga_id: str
    manga_title: str
    quantity: int
    unit_price: Decimal

    @property
    def line_total(self) -> Decimal:
        return self.unit_price * self.quantity


@dataclass
class Order:
    """Represents a completed, validated manga order."""
    order_id: str
    user_id: str
    items: list[OrderItem]
    delivery_address: str
    payment_method: PaymentMethod
    status: OrderStatus
    discount_amount: Decimal
    gift_wrap: bool
    special_notes: str
    subtotal: Decimal
    total_amount: Decimal
    confirmation_number: str

    def __repr__(self) -> str:
        return (
            f"Order(id={self.order_id!r}, user={self.user_id!r}, "
            f"items={len(self.items)}, total={self.total_amount}, "
            f"status={self.status.value})"
        )


class OrderBuilder:
    """
    Fluent Builder for constructing Order objects.

    Required fields: user_id, at least one item, delivery_address, payment_method.
    Optional fields: discount_amount, gift_wrap, special_notes.

    Example::

        order = (
            OrderBuilder("user-123")
            .add_item("manga-1", "Naruto Vol. 1", 2, Decimal("9.99"))
            .set_delivery_address("123 Manga St, Tokyo 100-001")
            .set_payment_method(PaymentMethod.PAYPAL)
            .apply_discount(Decimal("5.00"))
            .set_gift_wrap(True)
            .set_special_notes("Leave at door")
            .build()
        )
    """

    def __init__(self, user_id: str):
        if not user_id or not user_id.strip():
            raise ValueError("user_id must not be empty")
        self._user_id: str = user_id
        self._items: list[OrderItem] = []
        self._delivery_address: Optional[str] = None
        self._payment_method: Optional[PaymentMethod] = None
        self._discount_amount: Decimal = Decimal("0.00")
        self._gift_wrap: bool = False
        self._special_notes: str = ""

    # ── item management ──────────────────────────────────────────────────────

    def add_item(
        self,
        manga_id: str,
        manga_title: str,
        quantity: int,
        unit_price: Decimal,
    ) -> "OrderBuilder":
        """Add an OrderItem to the order."""
        if quantity < 1:
            raise ValueError(f"Quantity must be ≥ 1, got {quantity}")
        if unit_price <= Decimal("0"):
            raise ValueError(f"Unit price must be > 0, got {unit_price}")
        self._items.append(OrderItem(manga_id, manga_title, quantity, unit_price))
        return self

    def clear_items(self) -> "OrderBuilder":
        self._items.clear()
        return self

    # ── required fields ───────────────────────────────────────────────────────

    def set_delivery_address(self, address: str) -> "OrderBuilder":
        if not address or not address.strip():
            raise ValueError("Delivery address must not be empty")
        self._delivery_address = address.strip()
        return self

    def set_payment_method(self, method: PaymentMethod | str) -> "OrderBuilder":
        try:
            self._payment_method = PaymentMethod(method)
        except ValueError:
            raise ValueError(
                f"Invalid payment method {method!r}. "
                f"Valid: {[m.value for m in PaymentMethod]}"
            )
        return self

    # ── optional fields ───────────────────────────────────────────────────────

    def apply_discount(self, amount: Decimal) -> "OrderBuilder":
        if amount < Decimal("0"):
            raise ValueError("Discount amount cannot be negative")
        self._discount_amount = amount
        return self

    def set_gift_wrap(self, enabled: bool) -> "OrderBuilder":
        self._gift_wrap = bool(enabled)
        return self

    def set_special_notes(self, notes: str) -> "OrderBuilder":
        self._special_notes = str(notes)
        return self

    # ── build ─────────────────────────────────────────────────────────────────

    def _validate(self) -> None:
        """Raise ValueError if required fields are missing."""
        errors: list[str] = []
        if not self._items:
            errors.append("Order must contain at least one item")
        if not self._delivery_address:
            errors.append("Delivery address is required")
        if self._payment_method is None:
            errors.append("Payment method is required")
        if errors:
            raise ValueError("Cannot build order: " + "; ".join(errors))

    def build(self) -> Order:
        """Validate all fields and return an immutable Order object."""
        self._validate()
        subtotal = sum(item.line_total for item in self._items)
        discount = min(self._discount_amount, subtotal)  # discount cannot exceed subtotal
        total = subtotal - discount

        return Order(
            order_id=str(uuid.uuid4()),
            user_id=self._user_id,
            items=list(self._items),
            delivery_address=self._delivery_address,  # type: ignore[arg-type]
            payment_method=self._payment_method,       # type: ignore[arg-type]
            status=OrderStatus.PENDING,
            discount_amount=discount,
            gift_wrap=self._gift_wrap,
            special_notes=self._special_notes,
            subtotal=subtotal,
            total_amount=total,
            confirmation_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
        )
