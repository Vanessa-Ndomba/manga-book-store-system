"""Adapters package for the Manga Book Store system."""

from .payment_gateway import PaymentGateway, MockPaymentGateway
from .email_service import EmailService, MockEmailService
from .inventory_repository import InventoryRepository, MockInventoryRepository

__all__ = [
    "PaymentGateway",
    "MockPaymentGateway",
    "EmailService",
    "MockEmailService",
    "InventoryRepository",
    "MockInventoryRepository",
]
