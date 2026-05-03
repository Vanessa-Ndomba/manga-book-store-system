import pytest
from src.orders import Order, OrderItem, OrderStatus


def _sample_order():
    return Order(
        order_id="o1",
        customer_id="c1",
        shipping_address="123 St",
        items=[OrderItem(isbn="i1", title="T", unit_price=10.0, quantity=2)],
    )


def test_order_total_and_confirm_flow():
    o = _sample_order()
    assert o.total() == pytest.approx(20.0)
    assert o.status == OrderStatus.CREATED

    o.mark_payment_pending()
    assert o.status == OrderStatus.PAYMENT_PENDING

    o.confirm("txn-123")
    assert o.status == OrderStatus.CONFIRMED
    assert o.payment_transaction_id == "txn-123"


def test_order_mark_payment_pending_wrong_state():
    o = _sample_order()
    o.status = OrderStatus.CONFIRMED
    with pytest.raises(ValueError):
        o.mark_payment_pending()


def test_order_confirm_wrong_state():
    o = _sample_order()
    with pytest.raises(ValueError):
        o.confirm("txn-1")