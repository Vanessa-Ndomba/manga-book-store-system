from creational_patterns.factory_method import CreditCardProcessor, PayPalProcessor


def test_credit_card_processor_approves_positive_amount():
    r = CreditCardProcessor().process_payment(10.0)
    assert r.approved is True
    assert r.transaction_id


def test_paypal_processor_rejects_nonpositive_amount():
    r = PayPalProcessor().process_payment(0.0)
    assert r.approved is False
    assert r.transaction_id