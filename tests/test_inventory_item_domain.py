import pytest
from src.catalog import InventoryItem


def test_inventory_can_fulfill_and_reserve():
    item = InventoryItem(isbn="isbn-1", stock_on_hand=5)
    assert item.can_fulfill(3) is True
    item.reserve(3)
    assert item.stock_on_hand == 2


def test_inventory_reserve_insufficient_stock():
    item = InventoryItem(isbn="isbn-1", stock_on_hand=1)
    with pytest.raises(ValueError):
        item.reserve(2)


def test_inventory_reserve_rejects_nonpositive_qty():
    item = InventoryItem(isbn="isbn-1", stock_on_hand=1)
    with pytest.raises(ValueError):
        item.reserve(0)


def test_inventory_restock_increases_stock():
    item = InventoryItem(isbn="isbn-1", stock_on_hand=1)
    item.restock(4)
    assert item.stock_on_hand == 5


def test_inventory_restock_rejects_nonpositive_qty():
    item = InventoryItem(isbn="isbn-1", stock_on_hand=1)
    with pytest.raises(ValueError):
        item.restock(-1)