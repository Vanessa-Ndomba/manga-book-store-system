"""Unit tests for the Builder pattern (OrderBuilder)."""
import pytest
from decimal import Decimal
from creational_patterns.builder.order_builder import (
    OrderBuilder,
    Order,
    OrderStatus,
    PaymentMethod,
)


class TestOrderBuilder:
    """Tests for building valid and invalid orders."""

    def _minimal_builder(self) -> OrderBuilder:
        """Return a builder with the minimum required fields filled in."""
        return (
            OrderBuilder("user-123")
            .add_item("manga-1", "Naruto Vol. 1", 2, Decimal("9.99"))
            .set_delivery_address("123 Manga Street, Tokyo 100-0001")
            .set_payment_method(PaymentMethod.CREDIT_CARD)
        )

    # ── valid builds ─────────────────────────────────────────────────────────

    def test_build_returns_order(self):
        order = self._minimal_builder().build()
        assert isinstance(order, Order)

    def test_order_id_generated(self):
        order = self._minimal_builder().build()
        assert order.order_id and len(order.order_id) > 0

    def test_confirmation_number_generated(self):
        order = self._minimal_builder().build()
        assert order.confirmation_number.startswith("ORD-")

    def test_status_defaults_to_pending(self):
        order = self._minimal_builder().build()
        assert order.status == OrderStatus.PENDING

    def test_subtotal_calculated_correctly(self):
        order = self._minimal_builder().build()
        # 2 × 9.99 = 19.98
        assert order.subtotal == Decimal("19.98")

    def test_total_equals_subtotal_without_discount(self):
        order = self._minimal_builder().build()
        assert order.total_amount == order.subtotal

    def test_discount_applied(self):
        order = (
            self._minimal_builder()
            .apply_discount(Decimal("5.00"))
            .build()
        )
        assert order.discount_amount == Decimal("5.00")
        assert order.total_amount == Decimal("14.98")

    def test_discount_capped_at_subtotal(self):
        order = (
            self._minimal_builder()
            .apply_discount(Decimal("999.00"))
            .build()
        )
        assert order.total_amount == Decimal("0")
        assert order.discount_amount == order.subtotal

    def test_gift_wrap_defaults_false(self):
        order = self._minimal_builder().build()
        assert order.gift_wrap is False

    def test_gift_wrap_set_true(self):
        order = self._minimal_builder().set_gift_wrap(True).build()
        assert order.gift_wrap is True

    def test_special_notes_set(self):
        order = self._minimal_builder().set_special_notes("Leave at door").build()
        assert order.special_notes == "Leave at door"

    def test_multiple_items(self):
        order = (
            OrderBuilder("user-456")
            .add_item("manga-1", "Naruto Vol. 1", 1, Decimal("9.99"))
            .add_item("manga-2", "One Piece Vol. 5", 3, Decimal("10.99"))
            .set_delivery_address("456 Shonen Lane")
            .set_payment_method(PaymentMethod.PAYPAL)
            .build()
        )
        assert len(order.items) == 2
        assert order.subtotal == Decimal("9.99") + Decimal("32.97")

    def test_user_id_stored(self):
        order = self._minimal_builder().build()
        assert order.user_id == "user-123"

    def test_delivery_address_stored(self):
        order = self._minimal_builder().build()
        assert "Tokyo" in order.delivery_address

    def test_payment_method_stored(self):
        order = self._minimal_builder().build()
        assert order.payment_method == PaymentMethod.CREDIT_CARD

    def test_paypal_payment_method(self):
        order = (
            self._minimal_builder()
            .set_payment_method(PaymentMethod.PAYPAL)
            .build()
        )
        assert order.payment_method == PaymentMethod.PAYPAL

    def test_string_payment_method(self):
        order = (
            self._minimal_builder()
            .set_payment_method("paypal")
            .build()
        )
        assert order.payment_method == PaymentMethod.PAYPAL

    def test_unique_order_ids(self):
        orders = [self._minimal_builder().build() for _ in range(5)]
        ids = [o.order_id for o in orders]
        assert len(set(ids)) == 5

    # ── validation errors ─────────────────────────────────────────────────────

    def test_build_without_items_raises(self):
        builder = (
            OrderBuilder("user-1")
            .set_delivery_address("Somewhere")
            .set_payment_method(PaymentMethod.CREDIT_CARD)
        )
        with pytest.raises(ValueError, match="at least one item"):
            builder.build()

    def test_build_without_address_raises(self):
        builder = (
            OrderBuilder("user-1")
            .add_item("m1", "Title", 1, Decimal("5.00"))
            .set_payment_method(PaymentMethod.CREDIT_CARD)
        )
        with pytest.raises(ValueError, match="address"):
            builder.build()

    def test_build_without_payment_raises(self):
        builder = (
            OrderBuilder("user-1")
            .add_item("m1", "Title", 1, Decimal("5.00"))
            .set_delivery_address("Somewhere")
        )
        with pytest.raises(ValueError, match="(?i)payment"):
            builder.build()

    def test_empty_user_id_raises(self):
        with pytest.raises(ValueError, match="user_id"):
            OrderBuilder("")

    def test_add_item_zero_qty_raises(self):
        with pytest.raises(ValueError, match="Quantity"):
            OrderBuilder("u1").add_item("m1", "T", 0, Decimal("5.00"))

    def test_add_item_negative_price_raises(self):
        with pytest.raises(ValueError, match="Unit price"):
            OrderBuilder("u1").add_item("m1", "T", 1, Decimal("-1.00"))

    def test_empty_address_raises(self):
        with pytest.raises(ValueError, match="empty"):
            OrderBuilder("u1").set_delivery_address("")

    def test_invalid_payment_method_raises(self):
        with pytest.raises(ValueError, match="Invalid payment method"):
            OrderBuilder("u1").set_payment_method("bitcoin")

    def test_negative_discount_raises(self):
        with pytest.raises(ValueError, match="negative"):
            OrderBuilder("u1").apply_discount(Decimal("-1.00"))
