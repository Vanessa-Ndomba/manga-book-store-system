import pytest

from services.order_service import OrderService
from services.exceptions import BusinessRuleError
from src.orders import Order, OrderItem, OrderStatus
from src.users import User


class FakeRepo:
    def __init__(self):
        self.storage = {}

    def save(self, entity):
        key = getattr(entity, "order_id", None) or getattr(entity, "isbn", None) or getattr(entity, "user_id", None)
        self.storage[key] = entity
        return entity

    def find_by_id(self, key):
        return self.storage.get(key)

    def find_all(self):
        return list(self.storage.values())

    def delete(self, key):
        self.storage.pop(key, None)


def test_create_order_requires_existing_customer():
    order_repo = FakeRepo()
    user_repo = FakeRepo()
    manga_repo = FakeRepo()  # not used in our OrderService create_order in the example

    service = OrderService(order_repo, user_repo, manga_repo)

    order = Order(
        order_id="o100",
        customer_id="u999",  # doesn't exist
        shipping_address="123 Main St",
        items=[OrderItem(isbn="978-100", title="Bleach", unit_price=10.5, quantity=1)],
    )

    with pytest.raises(BusinessRuleError):
        service.create_order(order)


def test_create_order_requires_items():
    order_repo = FakeRepo()
    user_repo = FakeRepo()
    manga_repo = FakeRepo()

    user_repo.save(User(user_id="u200", email="u200@example.com", display_name="Vanessa"))

    service = OrderService(order_repo, user_repo, manga_repo)

    order = Order(order_id="o101", customer_id="u200", shipping_address="123 Main St", items=[])

    with pytest.raises(BusinessRuleError):
        service.create_order(order)


def test_checkout_sets_status_checked_out():
    order_repo = FakeRepo()
    user_repo = FakeRepo()
    manga_repo = FakeRepo()

    user_repo.save(User(user_id="u201", email="u201@example.com", display_name="Vanessa"))

    service = OrderService(order_repo, user_repo, manga_repo)

    order = Order(
        order_id="o102",
        customer_id="u201",
        shipping_address="123 Main St",
        items=[OrderItem(isbn="978-100", title="Bleach", unit_price=10.5, quantity=1)],
    )
    service.create_order(order)

    checked = service.checkout_order("o102")
    assert checked.status == OrderStatus.CHECKED_OUT


def test_checkout_twice_raises():
    order_repo = FakeRepo()
    user_repo = FakeRepo()
    manga_repo = FakeRepo()

    user_repo.save(User(user_id="u202", email="u202@example.com", display_name="Vanessa"))

    service = OrderService(order_repo, user_repo, manga_repo)

    order = Order(
        order_id="o103",
        customer_id="u202",
        shipping_address="123 Main St",
        items=[OrderItem(isbn="978-100", title="Bleach", unit_price=10.5, quantity=1)],
    )
    service.create_order(order)
    service.checkout_order("o103")

    with pytest.raises(BusinessRuleError):
        service.checkout_order("o103")