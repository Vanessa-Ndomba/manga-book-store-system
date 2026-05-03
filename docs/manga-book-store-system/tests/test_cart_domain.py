import pytest
from src.cart import Cart


def test_cart_add_and_set_qty():
    cart = Cart(customer_id="cust-1")
    cart.add("isbn-1", qty=2)
    assert cart.items["isbn-1"].quantity == 2

    cart.set_qty("isbn-1", 5)
    assert cart.items["isbn-1"].quantity == 5


def test_cart_set_qty_to_zero_removes_item():
    cart = Cart(customer_id="cust-1")
    cart.add("isbn-1", qty=1)
    cart.set_qty("isbn-1", 0)
    assert "isbn-1" not in cart.items


def test_cart_rejects_negative_qty():
    cart = Cart(customer_id="cust-1")
    with pytest.raises(ValueError):
        cart.add("isbn-1", qty=-1) 