import pytest
from fastapi.testclient import TestClient
from api.app import app
from factories.repository_factory import RepositoryFactory

@pytest.fixture
def client():
    # Reset all relevant repositories
    from api.routes.order_routes import order_repo, manga_repo, user_repo
    order_repo._storage = {}
    user_repo._storage = {}
    manga_repo._storage = {}
    
    return TestClient(app)

def test_create_order_success(client):
    # Setup dependencies
    client.post("/api/users", json={"user_id": "u1", "email": "a@e.com", "display_name": "Alice"})
    client.post("/api/manga", json={"isbn": "m1", "title": "T1", "author": "A1", "price": 10})
    
    payload = {
        "order_id": "o1",
        "customer_id": "u1",
        "shipping_address": "Street 1",
        "items": [{"isbn": "m1", "quantity": 2}]
    }
    response = client.post("/api/orders", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["order_id"] == "o1"
    assert data["customer_id"] == "u1"
    assert len(data["items"]) == 1
    assert data["status"] == "CREATED"

def test_create_order_user_not_found(client):
    client.post("/api/manga", json={"isbn": "m1", "title": "T1", "author": "A1", "price": 10})
    payload = {
        "order_id": "o1",
        "customer_id": "u1",
        "shipping_address": "Street 1",
        "items": [{"isbn": "m1", "quantity": 2}]
    }
    response = client.post("/api/orders", json=payload)
    assert response.status_code == 400
    assert "user 'u1' not found" in response.json()["detail"]

def test_checkout_order(client):
    # Setup
    client.post("/api/users", json={"user_id": "u1", "email": "a@e.com", "display_name": "Alice"})
    client.post("/api/manga", json={"isbn": "m1", "title": "T1", "author": "A1", "price": 10})
    client.post("/api/orders", json={
        "order_id": "o1", "customer_id": "u1", "shipping_address": "S1",
        "items": [{"isbn": "m1", "quantity": 1}]
    })
    
    response = client.post("/api/orders/o1/checkout")
    assert response.status_code == 200
    assert response.json()["status"] == "CHECKED_OUT"

def test_get_order(client):
    client.post("/api/users", json={"user_id": "u1", "email": "a@e.com", "display_name": "Alice"})
    client.post("/api/manga", json={"isbn": "m1", "title": "T1", "author": "A1", "price": 10})
    client.post("/api/orders", json={
        "order_id": "o1", "customer_id": "u1", "shipping_address": "S1",
        "items": [{"isbn": "m1", "quantity": 1}]
    })
    
    response = client.get("/api/orders/o1")
    assert response.status_code == 200
    assert response.json()["order_id"] == "o1"

def test_delete_order(client):
    client.post("/api/users", json={"user_id": "u1", "email": "a@e.com", "display_name": "Alice"})
    client.post("/api/manga", json={"isbn": "m1", "title": "T1", "author": "A1", "price": 10})
    client.post("/api/orders", json={
        "order_id": "o1", "customer_id": "u1", "shipping_address": "S1",
        "items": [{"isbn": "m1", "quantity": 1}]
    })
    
    response = client.delete("/api/orders/o1")
    assert response.status_code == 204
    
    response = client.get("/api/orders/o1")
    assert response.status_code == 404
