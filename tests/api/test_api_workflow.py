from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)


def test_create_user_manga_order_and_checkout():
    # 1) Create user
    user_payload = {
        "user_id": "u900",
        "email": "u900@example.com",
        "display_name": "Vanessa",
    }
    r = client.post("/api/users", json=user_payload)
    assert r.status_code in (200, 201), r.text

    # 2) Create manga (use a unique ISBN)
    manga_payload = {
        "isbn": "978-900",
        "title": "Bleach",
        "author": "Kubo",
        "price": 10.5,
    }
    r = client.post("/api/manga", json=manga_payload)
    assert r.status_code in (200, 201), r.text

    # 3) Create order
    order_payload = {
        "order_id": "o900",
        "customer_id": "u900",
        "shipping_address": "123 Main St",
        "items": [{"isbn": "978-900", "quantity": 1}],
    }
    r = client.post("/api/orders", json=order_payload)
    assert r.status_code in (200, 201), r.text
    order = r.json()
    assert order["order_id"] == "o900"
    assert order["customer_id"] == "u900"
    assert len(order["items"]) == 1

    # 4) Checkout
    r = client.post("/api/orders/o900/checkout")
    assert r.status_code == 200, r.text
    checked = r.json()
    # Depending on how you serialize enums, this may be "CHECKED_OUT" or "OrderStatus.CHECKED_OUT"
    assert "CHECKED_OUT" in checked["status"]


def test_duplicate_manga_returns_409():
    manga_payload = {
        "isbn": "978-901",
        "title": "Naruto",
        "author": "Kishimoto",
        "price": 12.99,
    }
    r1 = client.post("/api/manga", json=manga_payload)
    assert r1.status_code in (200, 201), r1.text

    r2 = client.post("/api/manga", json=manga_payload)
    assert r2.status_code == 409, r2.text