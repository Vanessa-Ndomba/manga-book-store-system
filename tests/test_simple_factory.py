import pytest
from creational_patterns.simple_factory import PaymentMethodFactory, CreditCard, PayPal


def test_creates_credit_card():
    obj = PaymentMethodFactory.create("credit_card", last4="1234")
    assert isinstance(obj, CreditCard)
    assert obj.last4 == "1234"


def test_creates_paypal():
    obj = PaymentMethodFactory.create("paypal", email="user@example.com")
    assert isinstance(obj, PayPal)
    assert obj.paypal_email == "user@example.com"


def test_invalid_cc_last4():
    with pytest.raises(ValueError):
        PaymentMethodFactory.create("credit_card", last4="12")


def test_unknown_method():
    with pytest.raises(ValueError):
        PaymentMethodFactory.create("crypto")  # type: ignore