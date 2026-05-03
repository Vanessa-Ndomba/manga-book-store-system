"""
Simple Factory Pattern — UserFactory

Justification: A single factory method centralises the creation of all user types
(GuestUser, RegisteredCustomer, StoreManager, SystemAdmin, Supplier).  Callers
pass a string role; the factory handles the conditional logic so the rest of the
codebase never imports concrete user classes directly.
"""
from __future__ import annotations
import uuid
import hashlib
import os
from enum import Enum


class UserType(str, Enum):
    GUEST = "guest"
    REGISTERED_CUSTOMER = "registered_customer"
    STORE_MANAGER = "store_manager"
    SYSTEM_ADMIN = "system_admin"
    SUPPLIER = "supplier"


# ── minimal stand-alone user classes (mirrors src/ but self-contained) ──────

class _BaseUser:
    """Minimal base user for factory demonstration."""
    def __init__(self, full_name: str, email: str, password: str):
        self._user_id: str = str(uuid.uuid4())
        self._full_name: str = full_name
        self._email: str = email
        salt = os.urandom(16)
        self._password_hash: str = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt, 100_000
        ).hex()
        self._user_type: UserType

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def email(self) -> str:
        return self._email

    @property
    def user_type(self) -> UserType:
        return self._user_type

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._user_id!r}, email={self._email!r})"


class GuestUser(_BaseUser):
    def __init__(self, full_name: str, email: str, password: str = ""):
        super().__init__(full_name, email, password or "guest")
        self._user_type = UserType.GUEST

    def register_account(self, full_name: str, email: str, password: str) -> "RegisteredCustomer":
        return RegisteredCustomer(full_name, email, password)

    def login(self, email: str, password: str) -> bool:
        return False  # guests cannot log in; must register first


class RegisteredCustomer(_BaseUser):
    def __init__(self, full_name: str, email: str, password: str):
        super().__init__(full_name, email, password)
        self._user_type = UserType.REGISTERED_CUSTOMER
        self._phone_number: str = ""
        self._delivery_addresses: list[str] = []

    def add_to_cart(self, manga_id: str, qty: int = 1) -> None:
        if qty < 1:
            raise ValueError("Quantity must be at least 1")

    def place_order(self, delivery_address: str) -> str:
        if not delivery_address:
            raise ValueError("Delivery address is required")
        return str(uuid.uuid4())


class StoreManager(_BaseUser):
    def __init__(self, full_name: str, email: str, password: str):
        super().__init__(full_name, email, password)
        self._user_type = UserType.STORE_MANAGER

    def generate_reports(self) -> list[dict]:
        return []

    def view_inventory(self) -> list[dict]:
        return []


class SystemAdmin(_BaseUser):
    def __init__(self, full_name: str, email: str, password: str):
        super().__init__(full_name, email, password)
        self._user_type = UserType.SYSTEM_ADMIN

    def manage_users(self, action: str, user_id: str) -> None:
        pass

    def reset_user_password(self, user_id: str) -> str:
        return str(uuid.uuid4())


class Supplier(_BaseUser):
    def __init__(self, full_name: str, email: str, password: str, company_name: str = ""):
        super().__init__(full_name, email, password)
        self._user_type = UserType.SUPPLIER
        self._company_name: str = company_name

    @property
    def company_name(self) -> str:
        return self._company_name

    def view_inventory(self) -> list[dict]:
        return []


# ── The Simple Factory ───────────────────────────────────────────────────────

class UserFactory:
    """
    Simple Factory for creating User objects.

    Centralises user instantiation: callers supply a UserType enum value
    (or its string equivalent) and receive the correct concrete user object
    without coupling to the concrete classes.
    """

    @staticmethod
    def create_user(
        user_type: UserType | str,
        full_name: str,
        email: str,
        password: str = "",
        **kwargs,
    ) -> _BaseUser:
        """
        Create and return a user object of the requested type.

        Args:
            user_type: A UserType enum value or its string equivalent.
            full_name: Display name.
            email: Unique email address.
            password: Plain-text password (hashed internally).
            **kwargs: Extra keyword arguments forwarded to the concrete class
                      (e.g. company_name for Supplier).

        Returns:
            A concrete user instance.

        Raises:
            ValueError: If user_type is not a recognised UserType.
        """
        try:
            user_type = UserType(user_type)
        except ValueError:
            raise ValueError(
                f"Unknown user type {user_type!r}. "
                f"Valid types: {[t.value for t in UserType]}"
            )

        mapping: dict[UserType, type[_BaseUser]] = {
            UserType.GUEST: GuestUser,
            UserType.REGISTERED_CUSTOMER: RegisteredCustomer,
            UserType.STORE_MANAGER: StoreManager,
            UserType.SYSTEM_ADMIN: SystemAdmin,
            UserType.SUPPLIER: Supplier,
        }

        cls = mapping[user_type]
        return cls(full_name, email, password or "default_pass", **kwargs)
