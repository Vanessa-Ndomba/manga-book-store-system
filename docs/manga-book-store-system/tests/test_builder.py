import pytest
from creational_patterns.builder import OrderBuilder


def test_builder_builds_valid_order():
    order = (
        OrderBuilder(customer_id="cust-1")
        .ship_to("123 Main St")
        .add_item(isbn="978-1", title="Naruto Vol 1", unit_price=9.99, quantity=2)
        .build()
    )
    assert order.customer_id == "cust-1"
    assert order.shipping_address == "123 Main St"
    assert len(order.items) == 1
    assert order.total() == pytest.approx(9.99 * 2)


def test_builder_requires_shipping_address():
    with pytest.raises(ValueError):
        OrderBuilder(customer_id="cust-1").add_item("978", "X", 1.0, 1).build()


def test_builder_rejects_empty_items():
    with pytest.raises(ValueError):
        OrderBuilder(customer_id="cust-1").ship_to("A").build()