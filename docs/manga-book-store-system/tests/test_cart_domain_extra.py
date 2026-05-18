import pytest
from src.cart import Cart


def test_cart_set_qty_raises_when_isbn_missing():
    cart = Cart(customer_id="cust-1")
    with pytest.raises(KeyError):
        cart.set_qty("missing", 1)


def test_cart_clear_empties_cart():
    cart = Cart(customer_id="cust-1")
    cart.add("isbn-1", 1)
    cart.add("isbn-2", 1)
    cart.clear()
    assert cart.items == {}
