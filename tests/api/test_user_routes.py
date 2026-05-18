import pytest
from fastapi.testclient import TestClient
from api.app import app
from factories.repository_factory import RepositoryFactory

@pytest.fixture
def client():
    # Access the shared user_repo and clear it
    from api.routes.user_routes import user_repo
    user_repo._storage = {}
    return TestClient(app)

def test_create_user(client):
    payload = {"user_id": "u1", "email": "alice@example.com", "display_name": "Alice"}
    response = client.post("/api/users", json=payload)
    assert response.status_code == 201
    assert response.json()["user_id"] == "u1"
    assert response.json()["display_name"] == "Alice"

def test_list_users(client):
    client.post("/api/users", json={"user_id": "u1", "email": "a@e.com", "display_name": "Alice"})
    client.post("/api/users", json={"user_id": "u2", "email": "b@e.com", "display_name": "Bob"})
    response = client.get("/api/users")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_user(client):
    client.post("/api/users", json={"user_id": "u1", "email": "a@e.com", "display_name": "Alice"})
    response = client.get("/api/users/u1")
    assert response.status_code == 200
    assert response.json()["display_name"] == "Alice"

def test_get_user_not_found(client):
    response = client.get("/api/users/nonexistent")
    assert response.status_code == 404

def test_delete_user(client):
    client.post("/api/users", json={"user_id": "u1", "email": "a@e.com", "display_name": "Alice"})
    response = client.delete("/api/users/u1")
    assert response.status_code == 204
    response = client.get("/api/users/u1")
    assert response.status_code == 404
