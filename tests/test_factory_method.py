"""Unit tests for the Factory Method pattern (PaymentProcessor)."""
import pytest
from decimal import Decimal
from creational_patterns.factory_method.payment_processor import (
    CreditCardProcessor,
    CreditCardProcessorCreator,
    PayPalProcessor,
    PayPalProcessorCreator,
    PaymentResult,
)


class TestCreditCardProcessor:
    """Tests for CreditCardProcessor."""

    def setup_method(self):
        self.processor = CreditCardProcessor("4111111111111111", "12/26", "123")
        self.creator = CreditCardProcessorCreator("4111111111111111", "12/26", "123")

    def test_process_returns_payment_result(self):
        result = self.processor.process("order-1", Decimal("25.00"))
        assert isinstance(result, PaymentResult)

    def test_successful_payment(self):
        result = self.processor.process("order-1", Decimal("25.00"))
        assert result.success is True
        assert result.provider == "CreditCard"
        assert result.amount == Decimal("25.00")
        assert result.transaction_id.startswith("CC-")

    def test_zero_amount_fails(self):
        result = self.processor.process("order-1", Decimal("0.00"))
        assert result.success is False
        assert "positive" in result.failure_reason.lower()

    def test_negative_amount_fails(self):
        result = self.processor.process("order-1", Decimal("-5.00"))
        assert result.success is False

    def test_refund_returns_success(self):
        pay_result = self.processor.process("order-1", Decimal("10.00"))
        refund = self.processor.refund(pay_result.transaction_id, Decimal("10.00"))
        assert refund.success is True
        assert "REF" in refund.transaction_id

    def test_invalid_card_number_raises(self):
        with pytest.raises(ValueError, match="at least 13"):
            CreditCardProcessor("1234", "12/26", "123")

    def test_creator_factory_method(self):
        processor = self.creator.factory_method()
        assert isinstance(processor, CreditCardProcessor)

    def test_creator_process_payment(self):
        result = self.creator.process_payment("order-2", Decimal("50.00"))
        assert result.success is True


class TestPayPalProcessor:
    """Tests for PayPalProcessor."""

    def setup_method(self):
        self.processor = PayPalProcessor("buyer@paypal.com")
        self.creator = PayPalProcessorCreator("buyer@paypal.com")

    def test_process_returns_payment_result(self):
        result = self.processor.process("order-3", Decimal("30.00"))
        assert isinstance(result, PaymentResult)

    def test_successful_payment(self):
        result = self.processor.process("order-3", Decimal("30.00"))
        assert result.success is True
        assert result.provider == "PayPal"
        assert result.transaction_id.startswith("PP-")

    def test_zero_amount_fails(self):
        result = self.processor.process("order-3", Decimal("0"))
        assert result.success is False

    def test_refund_transaction_id_has_ref(self):
        pay = self.processor.process("order-4", Decimal("20.00"))
        refund = self.processor.refund(pay.transaction_id, Decimal("20.00"))
        assert "REF" in refund.transaction_id

    def test_invalid_email_raises(self):
        with pytest.raises(ValueError, match="Invalid PayPal email"):
            PayPalProcessor("not-an-email")

    def test_creator_factory_method(self):
        processor = self.creator.factory_method()
        assert isinstance(processor, PayPalProcessor)

    def test_unique_transaction_ids(self):
        results = [
            self.processor.process(f"order-{i}", Decimal("15.00")) for i in range(5)
        ]
        txn_ids = [r.transaction_id for r in results]
        assert len(set(txn_ids)) == 5
