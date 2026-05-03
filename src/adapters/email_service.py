"""EmailService adapter: abstract base and mock implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List

if TYPE_CHECKING:
    from ..orders.order import Order
    from ..users.user import User


class EmailService(ABC):
    """Abstract base class for email sending adapters.

    Concrete implementations integrate with a real email provider (e.g.
    SendGrid, SES, SMTP) to deliver transactional messages.
    """

    @abstractmethod
    def send_order_confirmation(self, email: str, order: "Order") -> None:
        """Send an order confirmation email.

        Args:
            email: Recipient email address.
            order: The placed Order to confirm.
        """

    @abstractmethod
    def send_registration_confirmation(self, email: str, user: "User") -> None:
        """Send a registration welcome email.

        Args:
            email: Recipient email address.
            user: The newly registered User.
        """

    @abstractmethod
    def send_password_reset(self, email: str, token: str) -> None:
        """Send a password-reset email containing a reset token.

        Args:
            email: Recipient email address.
            token: Secure password-reset token.
        """


class MockEmailService(EmailService):
    """In-memory mock email service for testing and development.

    All sent messages are stored in an internal list so tests can
    inspect what was sent without connecting to a real mail server.

    Attributes:
        _sent_emails: List of dictionaries representing sent email records.
    """

    def __init__(self) -> None:
        """Initialise the MockEmailService with an empty sent-emails list."""
        self._sent_emails: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def sent_emails(self) -> List[Dict[str, Any]]:
        """Read-only copy of all recorded sent emails."""
        return list(self._sent_emails)

    # ------------------------------------------------------------------
    # EmailService implementation
    # ------------------------------------------------------------------

    def send_order_confirmation(self, email: str, order: "Order") -> None:
        """Record an order confirmation email in the sent list.

        Args:
            email: Recipient email address.
            order: The placed Order being confirmed.
        """
        self._sent_emails.append(
            {
                "type": "order_confirmation",
                "to": email,
                "order_id": order.order_id,
                "confirmation_number": order.confirmation_number,
                "total_amount": order.total_amount,
            }
        )

    def send_registration_confirmation(self, email: str, user: "User") -> None:
        """Record a registration confirmation email in the sent list.

        Args:
            email: Recipient email address.
            user: The newly registered User.
        """
        self._sent_emails.append(
            {
                "type": "registration_confirmation",
                "to": email,
                "user_id": user.user_id,
                "full_name": user.full_name,
            }
        )

    def send_password_reset(self, email: str, token: str) -> None:
        """Record a password-reset email in the sent list.

        Args:
            email: Recipient email address.
            token: Secure reset token.
        """
        self._sent_emails.append(
            {
                "type": "password_reset",
                "to": email,
                "token": token,
            }
        )

    def clear(self) -> None:
        """Clear all recorded sent emails (useful between test cases)."""
        self._sent_emails.clear()
