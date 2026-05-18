import pytest
from fastapi.testclient import TestClient
from api.app import app
from factories.repository_factory import RepositoryFactory

@pytest.fixture
def client():
    # Clear memory storage before tests
    from api.routes.manga_routes import manga_repo
    manga_repo._storage = {}
    return TestClient(app)

def test_create_manga(client):
    payload = {
        "isbn": "123",
        "title": "Manga Title",
        "author": "Author Name",
        "price": 15.0
    }
    response = client.post("/api/manga", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["isbn"] == "123"
    assert data["title"] == "Manga Title"

def test_list_manga(client):
    client.post("/api/manga", json={"isbn": "1", "title": "T1", "author": "A1", "price": 10})
    client.post("/api/manga", json={"isbn": "2", "title": "T2", "author": "A2", "price": 20})
    
    response = client.get("/api/manga")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_manga(client):
    client.post("/api/manga", json={"isbn": "1", "title": "T1", "author": "A1", "price": 10})
    response = client.get("/api/manga/1")
    assert response.status_code == 200
    assert response.json()["title"] == "T1"

def test_get_manga_not_found(client):
    response = client.get("/api/manga/999")
    assert response.status_code == 404

def test_update_manga(client):
    client.post("/api/manga", json={"isbn": "1", "title": "T1", "author": "A1", "price": 10})
    response = client.put("/api/manga/1", json={"title": "Updated T1"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated T1"

def test_delete_manga(client):
    client.post("/api/manga", json={"isbn": "1", "title": "T1", "author": "A1", "price": 10})
    response = client.delete("/api/manga/1")
    assert response.status_code == 204
    
    response = client.get("/api/manga/1")
    assert response.status_code == 404
