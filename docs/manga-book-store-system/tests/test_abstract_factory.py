from creational_patterns.abstract_factory import EmailNotificationFactory, SmsNotificationFactory


def test_email_notification_family():
    f = EmailNotificationFactory()
    formatter = f.create_formatter()
    sender = f.create_sender()

    receipt = formatter.format_receipt("O-1", 12.5)
    out = sender.send("user@example.com", receipt)
    assert out.startswith("EMAIL")


def test_sms_notification_family():
    f = SmsNotificationFactory()
    formatter = f.create_formatter()
    sender = f.create_sender()

    receipt = formatter.format_receipt("O-2", 99.99)
    out = sender.send("+15551234567", receipt)
    assert out.startswith("SMS")
