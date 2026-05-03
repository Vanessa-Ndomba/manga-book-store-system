"""Unit tests for the Abstract Factory pattern (NotificationFactory)."""
import pytest
from creational_patterns.abstract_factory.notification_factory import (
    EmailNotificationFactory,
    SmsNotificationFactory,
    NotificationFactory,
    OrderConfirmationNotifier,
    RegistrationNotifier,
    PasswordResetNotifier,
)


def _run_notification_suite(factory: NotificationFactory):
    """Helper: exercise all notifiers produced by a factory."""
    order_notifier = factory.create_order_confirmation_notifier()
    assert isinstance(order_notifier, OrderConfirmationNotifier)
    result = order_notifier.notify("user@example.com", "ORD-001", 49.99)
    assert result is True

    reg_notifier = factory.create_registration_notifier()
    assert isinstance(reg_notifier, RegistrationNotifier)
    result = reg_notifier.notify("user@example.com", "Alice")
    assert result is True

    pwd_notifier = factory.create_password_reset_notifier()
    assert isinstance(pwd_notifier, PasswordResetNotifier)
    result = pwd_notifier.notify("user@example.com", "RESET-TOKEN-XYZ")
    assert result is True


class TestEmailNotificationFactory:
    def test_factory_creates_correct_types(self):
        factory = EmailNotificationFactory()
        _run_notification_suite(factory)

    def test_order_notifier_stores_message(self):
        factory = EmailNotificationFactory()
        notifier = factory.create_order_confirmation_notifier()
        notifier.notify("a@b.com", "ORD-999", 29.99)
        assert len(notifier.sent_messages) == 1
        msg = notifier.sent_messages[0]
        assert "ORD-999" in msg["subject"]
        assert "to" in msg

    def test_registration_notifier_content(self):
        factory = EmailNotificationFactory()
        notifier = factory.create_registration_notifier()
        notifier.notify("alice@example.com", "Alice")
        msg = notifier.sent_messages[0]
        assert "Alice" in msg["body"]

    def test_password_reset_notifier_content(self):
        factory = EmailNotificationFactory()
        notifier = factory.create_password_reset_notifier()
        notifier.notify("alice@example.com", "ABC123")
        msg = notifier.sent_messages[0]
        assert "ABC123" in msg["body"]

    def test_multiple_messages_accumulate(self):
        factory = EmailNotificationFactory()
        notifier = factory.create_order_confirmation_notifier()
        notifier.notify("a@b.com", "ORD-1", 10.00)
        notifier.notify("c@d.com", "ORD-2", 20.00)
        assert len(notifier.sent_messages) == 2


class TestSmsNotificationFactory:
    def test_factory_creates_correct_types(self):
        factory = SmsNotificationFactory()
        _run_notification_suite(factory)

    def test_sms_order_notifier_stores_message(self):
        factory = SmsNotificationFactory()
        notifier = factory.create_order_confirmation_notifier()
        notifier.notify("+1234567890", "ORD-001", 99.99)
        assert len(notifier.sent_messages) == 1
        msg = notifier.sent_messages[0]
        assert "ORD-001" in msg["text"]

    def test_sms_registration_content(self):
        factory = SmsNotificationFactory()
        notifier = factory.create_registration_notifier()
        notifier.notify("+1234567890", "Bob")
        msg = notifier.sent_messages[0]
        assert "Bob" in msg["text"]

    def test_sms_password_reset_content(self):
        factory = SmsNotificationFactory()
        notifier = factory.create_password_reset_notifier()
        notifier.notify("+1234567890", "TOKEN999")
        msg = notifier.sent_messages[0]
        assert "TOKEN999" in msg["text"]


class TestFactoryInterchangeability:
    """Both factories honour the same interface."""

    @pytest.mark.parametrize("factory_cls", [EmailNotificationFactory, SmsNotificationFactory])
    def test_order_confirmation_interchangeable(self, factory_cls):
        factory = factory_cls()
        notifier = factory.create_order_confirmation_notifier()
        assert notifier.notify("recipient", "ORD-X", 1.00) is True
