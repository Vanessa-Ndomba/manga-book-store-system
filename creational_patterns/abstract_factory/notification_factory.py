"""
Abstract Factory Pattern — NotificationFactory

Justification: The bookstore must send notifications via different channels
(Email vs SMS) depending on user preferences or deployment environment.  The
Abstract Factory groups the related notifier objects (OrderConfirmation,
RegistrationWelcome, PasswordReset) per channel so the rest of the system never
directly instantiates channel-specific classes.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


# ── Abstract products ────────────────────────────────────────────────────────

class OrderConfirmationNotifier(ABC):
    """Sends an order-confirmation notification."""
    @abstractmethod
    def notify(self, recipient: str, order_id: str, total: float) -> bool:
        """Send notification; returns True on success."""


class RegistrationNotifier(ABC):
    """Sends a registration-welcome notification."""
    @abstractmethod
    def notify(self, recipient: str, user_name: str) -> bool:
        """Send notification; returns True on success."""


class PasswordResetNotifier(ABC):
    """Sends a password-reset notification."""
    @abstractmethod
    def notify(self, recipient: str, reset_token: str) -> bool:
        """Send notification; returns True on success."""


# ── Abstract factory ─────────────────────────────────────────────────────────

class NotificationFactory(ABC):
    """
    Abstract Factory: declares creation methods for a family of notification objects.
    Each concrete factory provides a consistent channel (Email or SMS).
    """

    @abstractmethod
    def create_order_confirmation_notifier(self) -> OrderConfirmationNotifier:
        ...

    @abstractmethod
    def create_registration_notifier(self) -> RegistrationNotifier:
        ...

    @abstractmethod
    def create_password_reset_notifier(self) -> PasswordResetNotifier:
        ...


# ── Email channel ─────────────────────────────────────────────────────────────

class EmailOrderConfirmationNotifier(OrderConfirmationNotifier):
    """Email implementation of order-confirmation notifier."""

    def __init__(self):
        self._sent: list[dict] = []

    def notify(self, recipient: str, order_id: str, total: float) -> bool:
        msg = {
            "to": recipient,
            "subject": f"Order Confirmation #{order_id}",
            "body": f"Your order #{order_id} totalling ${total:.2f} has been placed.",
        }
        self._sent.append(msg)
        return True

    @property
    def sent_messages(self) -> list[dict]:
        return list(self._sent)


class EmailRegistrationNotifier(RegistrationNotifier):
    """Email implementation of registration notifier."""

    def __init__(self):
        self._sent: list[dict] = []

    def notify(self, recipient: str, user_name: str) -> bool:
        msg = {
            "to": recipient,
            "subject": "Welcome to MangaBookStore!",
            "body": f"Hi {user_name}, welcome! Please verify your email.",
        }
        self._sent.append(msg)
        return True

    @property
    def sent_messages(self) -> list[dict]:
        return list(self._sent)


class EmailPasswordResetNotifier(PasswordResetNotifier):
    """Email implementation of password-reset notifier."""

    def __init__(self):
        self._sent: list[dict] = []

    def notify(self, recipient: str, reset_token: str) -> bool:
        msg = {
            "to": recipient,
            "subject": "Password Reset Request",
            "body": f"Use this token to reset your password: {reset_token}",
        }
        self._sent.append(msg)
        return True

    @property
    def sent_messages(self) -> list[dict]:
        return list(self._sent)


class EmailNotificationFactory(NotificationFactory):
    """Concrete factory that produces email-channel notification objects."""

    def create_order_confirmation_notifier(self) -> EmailOrderConfirmationNotifier:
        return EmailOrderConfirmationNotifier()

    def create_registration_notifier(self) -> EmailRegistrationNotifier:
        return EmailRegistrationNotifier()

    def create_password_reset_notifier(self) -> EmailPasswordResetNotifier:
        return EmailPasswordResetNotifier()


# ── SMS channel ───────────────────────────────────────────────────────────────

class SmsOrderConfirmationNotifier(OrderConfirmationNotifier):
    """SMS implementation of order-confirmation notifier."""

    def __init__(self):
        self._sent: list[dict] = []

    def notify(self, recipient: str, order_id: str, total: float) -> bool:
        msg = {
            "to": recipient,
            "text": f"MangaStore: Order #{order_id} placed. Total: ${total:.2f}",
        }
        self._sent.append(msg)
        return True

    @property
    def sent_messages(self) -> list[dict]:
        return list(self._sent)


class SmsRegistrationNotifier(RegistrationNotifier):
    """SMS implementation of registration notifier."""

    def __init__(self):
        self._sent: list[dict] = []

    def notify(self, recipient: str, user_name: str) -> bool:
        msg = {
            "to": recipient,
            "text": f"MangaStore: Welcome {user_name}! Your account is active.",
        }
        self._sent.append(msg)
        return True

    @property
    def sent_messages(self) -> list[dict]:
        return list(self._sent)


class SmsPasswordResetNotifier(PasswordResetNotifier):
    """SMS implementation of password-reset notifier."""

    def __init__(self):
        self._sent: list[dict] = []

    def notify(self, recipient: str, reset_token: str) -> bool:
        msg = {
            "to": recipient,
            "text": f"MangaStore password reset code: {reset_token}",
        }
        self._sent.append(msg)
        return True

    @property
    def sent_messages(self) -> list[dict]:
        return list(self._sent)


class SmsNotificationFactory(NotificationFactory):
    """Concrete factory that produces SMS-channel notification objects."""

    def create_order_confirmation_notifier(self) -> SmsOrderConfirmationNotifier:
        return SmsOrderConfirmationNotifier()

    def create_registration_notifier(self) -> SmsRegistrationNotifier:
        return SmsRegistrationNotifier()

    def create_password_reset_notifier(self) -> SmsPasswordResetNotifier:
        return SmsPasswordResetNotifier()
