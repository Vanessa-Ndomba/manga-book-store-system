from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


class ReceiptFormatter(ABC):
    @abstractmethod
    def format_receipt(self, order_id: str, total: float) -> str:
        raise NotImplementedError


class ReceiptSender(ABC):
    @abstractmethod
    def send(self, to: str, receipt: str) -> str:
        raise NotImplementedError


@dataclass
class EmailReceiptSender(ReceiptSender):
    def send(self, to: str, receipt: str) -> str:
        return f"EMAIL to={to} receipt={receipt}"


@dataclass
class SmsReceiptSender(ReceiptSender):
    def send(self, to: str, receipt: str) -> str:
        return f"SMS to={to} receipt={receipt}"


@dataclass
class SimpleTextReceiptFormatter(ReceiptFormatter):
    def format_receipt(self, order_id: str, total: float) -> str:
        return f"Order {order_id} total={total:.2f}"


class NotificationFactory(ABC):
    """
    Abstract Factory: creates a family of related objects:
    - ReceiptFormatter
    - ReceiptSender
    """

    @abstractmethod
    def create_formatter(self) -> ReceiptFormatter:
        raise NotImplementedError

    @abstractmethod
    def create_sender(self) -> ReceiptSender:
        raise NotImplementedError


class EmailNotificationFactory(NotificationFactory):
    def create_formatter(self) -> ReceiptFormatter:
        return SimpleTextReceiptFormatter()

    def create_sender(self) -> ReceiptSender:
        return EmailReceiptSender()


class SmsNotificationFactory(NotificationFactory):
    def create_formatter(self) -> ReceiptFormatter:
        return SimpleTextReceiptFormatter()

    def create_sender(self) -> ReceiptSender:
        return SmsReceiptSender()
