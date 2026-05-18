from repositories.inmemory.inmemory_order_repository import InMemoryOrderRepository
from src.orders import Order, OrderItem


def test_order_repo_crud():
    repo = InMemoryOrderRepository()

    o1 = Order(
        order_id="o-1",
        customer_id="c-1",
        shipping_address="123 St",
        items=[OrderItem(isbn="978-1", title="Naruto", unit_price=9.99, quantity=2)],
    )

    # Create
    repo.save(o1)
    assert repo.find_by_id("o-1") == o1

    # Update
    o1.shipping_address = "999 New St"
    repo.save(o1)
    assert repo.find_by_id("o-1").shipping_address == "999 New St"  # type: ignore[union-attr]

    # Find all
    assert len(repo.find_all()) == 1

    # Delete
    repo.delete("o-1")
    assert repo.find_by_id("o-1") is None