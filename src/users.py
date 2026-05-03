from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    user_id: str
    email: str
    display_name: str
    active: bool = True

    def deactivate(self) -> None:
        self.active = False


@dataclass
class Customer(User):
    default_shipping_address: Optional[str] = None

    def update_profile(self, display_name: Optional[str] = None, address: Optional[str] = None) -> None:
        if display_name:
            self.display_name = display_name
        if address:
            self.default_shipping_address = address


@dataclass
class Admin(User):
    role: str = "admin"