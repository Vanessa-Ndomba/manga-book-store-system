"""Unit tests for the Simple Factory pattern (UserFactory)."""
import pytest
from creational_patterns.simple_factory.user_factory import (
    UserFactory,
    UserType,
    GuestUser,
    RegisteredCustomer,
    StoreManager,
    SystemAdmin,
    Supplier,
)


class TestUserFactory:
    """Tests for UserFactory.create_user()."""

    def test_creates_guest_user(self):
        user = UserFactory.create_user(UserType.GUEST, "Alice", "alice@example.com")
        assert isinstance(user, GuestUser)
        assert user.user_type == UserType.GUEST

    def test_creates_registered_customer(self):
        user = UserFactory.create_user(
            UserType.REGISTERED_CUSTOMER, "Bob", "bob@example.com", "Pass1234!"
        )
        assert isinstance(user, RegisteredCustomer)
        assert user.user_type == UserType.REGISTERED_CUSTOMER

    def test_creates_store_manager(self):
        user = UserFactory.create_user(
            UserType.STORE_MANAGER, "Carol", "carol@manga.com", "Mgr@2025!"
        )
        assert isinstance(user, StoreManager)
        assert user.user_type == UserType.STORE_MANAGER

    def test_creates_system_admin(self):
        user = UserFactory.create_user(
            UserType.SYSTEM_ADMIN, "Dave", "dave@manga.com", "Admin@2025!"
        )
        assert isinstance(user, SystemAdmin)
        assert user.user_type == UserType.SYSTEM_ADMIN

    def test_creates_supplier(self):
        user = UserFactory.create_user(
            UserType.SUPPLIER,
            "Eve",
            "eve@supply.com",
            "Sup@2025!",
            company_name="Manga Wholesale Ltd",
        )
        assert isinstance(user, Supplier)
        assert user.user_type == UserType.SUPPLIER
        assert user.company_name == "Manga Wholesale Ltd"

    def test_accepts_string_user_type(self):
        user = UserFactory.create_user("guest", "Frank", "frank@example.com")
        assert isinstance(user, GuestUser)

    def test_unique_user_ids(self):
        users = [
            UserFactory.create_user(UserType.GUEST, f"User{i}", f"user{i}@x.com")
            for i in range(5)
        ]
        ids = [u.user_id for u in users]
        assert len(set(ids)) == 5, "Each user should have a unique ID"

    def test_attributes_set_correctly(self):
        user = UserFactory.create_user(
            UserType.REGISTERED_CUSTOMER, "Grace", "grace@example.com", "pass"
        )
        assert user.full_name == "Grace"
        assert user.email == "grace@example.com"

    def test_invalid_user_type_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown user type"):
            UserFactory.create_user("wizard", "Harry", "harry@example.com")

    def test_guest_cannot_login(self):
        user = UserFactory.create_user(UserType.GUEST, "Ivy", "ivy@example.com")
        assert user.login("ivy@example.com", "pass") is False

    def test_registered_customer_add_to_cart_invalid_qty(self):
        user = UserFactory.create_user(
            UserType.REGISTERED_CUSTOMER, "Jack", "jack@example.com", "pass"
        )
        with pytest.raises(ValueError, match="Quantity must be at least 1"):
            user.add_to_cart("manga-1", qty=0)

    def test_registered_customer_place_order_no_address(self):
        user = UserFactory.create_user(
            UserType.REGISTERED_CUSTOMER, "Kim", "kim@example.com", "pass"
        )
        with pytest.raises(ValueError, match="Delivery address is required"):
            user.place_order("")
