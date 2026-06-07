import pytest
from fastapi.testclient import TestClient
from api.app import app


@pytest.fixture
def client():
    """
    Create a test client with fresh/clean repositories for each test.
    Clears all shared repository storage to avoid cross-test pollution.
    """
    # Reset all repositories before each test
    from api.routes.user_routes import user_repo
    from api.routes.manga_routes import manga_repo
    from api.routes.order_routes import order_repo
    
    user_repo._storage = {}
    manga_repo._storage = {}
    order_repo._storage = {}
    
    return TestClient(app)


class TestCompleteWorkflow:
    """Test the complete user-to-checkout flow."""
    
    def test_create_user_manga_order_and_checkout(self, client):
        """Test the complete workflow: create user → create manga → create order → checkout."""
        # Step 1: Create a user
        user_payload = {
            "user_id": "user_workflow_1",
            "email": "workflow1@example.com",
            "display_name": "Workflow User",
        }
        user_response = client.post("/api/users", json=user_payload)
        assert user_response.status_code == 201, user_response.text
        user_data = user_response.json()
        assert user_data["user_id"] == "user_workflow_1"
        assert user_data["email"] == "workflow1@example.com"
        assert user_data["display_name"] == "Workflow User"
        assert user_data["active"] is True

        # Step 2: Create a manga
        manga_payload = {
            "isbn": "978-0-123456-01",
            "title": "Bleach",
            "author": "Kubo Tite",
            "price": 10.99,
        }
        manga_response = client.post("/api/manga", json=manga_payload)
        assert manga_response.status_code == 201, manga_response.text
        manga_data = manga_response.json()
        assert manga_data["isbn"] == "978-0-123456-01"
        assert manga_data["title"] == "Bleach"
        assert manga_data["author"] == "Kubo Tite"
        assert manga_data["price"] == 10.99

        # Step 3: Create an order
        order_payload = {
            "order_id": "order_workflow_1",
            "customer_id": "user_workflow_1",
            "shipping_address": "123 Main Street, Tokyo, Japan",
            "items": [{"isbn": "978-0-123456-01", "quantity": 2}],
        }
        order_response = client.post("/api/orders", json=order_payload)
        assert order_response.status_code == 201, order_response.text
        order_data = order_response.json()
        assert order_data["order_id"] == "order_workflow_1"
        assert order_data["customer_id"] == "user_workflow_1"
        assert order_data["shipping_address"] == "123 Main Street, Tokyo, Japan"
        assert len(order_data["items"]) == 1
        assert order_data["items"][0]["isbn"] == "978-0-123456-01"
        assert order_data["items"][0]["title"] == "Bleach"
        assert order_data["items"][0]["unit_price"] == 10.99
        assert order_data["items"][0]["quantity"] == 2
        assert order_data["total"] == 21.98
        assert order_data["status"] == "CREATED"

        # Step 4: Checkout the order
        checkout_response = client.post("/api/orders/order_workflow_1/checkout")
        assert checkout_response.status_code == 200, checkout_response.text
        checkout_data = checkout_response.json()
        assert checkout_data["order_id"] == "order_workflow_1"
        assert checkout_data["status"] == "CHECKED_OUT"
        assert checkout_data["total"] == 21.98
        assert "payment_transaction_id" in checkout_data

    def test_multiple_items_in_order(self, client):
        """Test creating an order with multiple manga items."""
        # Create user
        client.post("/api/users", json={
            "user_id": "multi_user",
            "email": "multi@example.com",
            "display_name": "Multi Item User"
        })
        
        # Create multiple manga
        manga1 = {
            "isbn": "978-0-111111-01",
            "title": "Naruto",
            "author": "Kishimoto Masashi",
            "price": 12.99
        }
        manga2 = {
            "isbn": "978-0-222222-02",
            "title": "One Piece",
            "author": "Oda Eiichiro",
            "price": 14.99
        }
        manga3 = {
            "isbn": "978-0-333333-03",
            "title": "Dragon Ball",
            "author": "Toriyama Akira",
            "price": 9.99
        }
        
        client.post("/api/manga", json=manga1)
        client.post("/api/manga", json=manga2)
        client.post("/api/manga", json=manga3)
        
        # Create order with multiple items
        order_payload = {
            "order_id": "multi_order",
            "customer_id": "multi_user",
            "shipping_address": "456 Anime Street",
            "items": [
                {"isbn": "978-0-111111-01", "quantity": 1},
                {"isbn": "978-0-222222-02", "quantity": 2},
                {"isbn": "978-0-333333-03", "quantity": 3},
            ]
        }
        
        order_response = client.post("/api/orders", json=order_payload)
        assert order_response.status_code == 201
        order_data = order_response.json()
        assert len(order_data["items"]) == 3
        assert order_data["items"][0]["quantity"] == 1
        assert order_data["items"][1]["quantity"] == 2
        assert order_data["items"][2]["quantity"] == 3
        expected_total = (12.99 * 1) + (14.99 * 2) + (9.99 * 3)
        assert abs(order_data["total"] - expected_total) < 0.01
    
    def test_order_flow_get_order_before_checkout(self, client):
        """Test retrieving order details before checkout."""
        # Setup
        client.post("/api/users", json={
            "user_id": "get_user",
            "email": "get@example.com",
            "display_name": "Get User"
        })
        client.post("/api/manga", json={
            "isbn": "978-0-444444-04",
            "title": "Jujutsu Kaisen",
            "author": "Gege Akutami",
            "price": 13.99
        })
        
        order_payload = {
            "order_id": "get_order",
            "customer_id": "get_user",
            "shipping_address": "789 Cursed Street",
            "items": [{"isbn": "978-0-444444-04", "quantity": 1}]
        }
        create_response = client.post("/api/orders", json=order_payload)
        assert create_response.status_code == 201
        
        # Get the order
        get_response = client.get("/api/orders/get_order")
        assert get_response.status_code == 200
        order_data = get_response.json()
        assert order_data["order_id"] == "get_order"
        assert order_data["status"] == "CREATED"
        assert order_data["customer_id"] == "get_user"
        assert len(order_data["items"]) == 1


class TestWorkflowErrorCases:
    """Test error handling in workflow scenarios."""
    
    def test_create_order_with_nonexistent_user(self, client):
        """Test creating order fails when user doesn't exist."""
        # Create manga
        client.post("/api/manga", json={
            "isbn": "978-0-555555-05",
            "title": "Attack on Titan",
            "author": "Hajime Isayama",
            "price": 11.99
        })
        
        # Try to create order with non-existent user
        order_payload = {
            "order_id": "fail_order_1",
            "customer_id": "nonexistent_user",
            "shipping_address": "Wall Maria",
            "items": [{"isbn": "978-0-555555-05", "quantity": 1}]
        }
        
        response = client.post("/api/orders", json=order_payload)
        assert response.status_code == 400
        assert "user 'nonexistent_user' not found" in response.json()["detail"]
    
    def test_create_order_with_nonexistent_manga(self, client):
        """Test creating order fails when manga doesn't exist."""
        # Create user
        client.post("/api/users", json={
            "user_id": "error_user",
            "email": "error@example.com",
            "display_name": "Error User"
        })
        
        # Try to create order with non-existent manga
        order_payload = {
            "order_id": "fail_order_2",
            "customer_id": "error_user",
            "shipping_address": "Unknown Location",
            "items": [{"isbn": "978-0-999999-99", "quantity": 1}]
        }
        
        response = client.post("/api/orders", json=order_payload)
        assert response.status_code == 400
        assert "manga '978-0-999999-99' not found" in response.json()["detail"]
    
    def test_checkout_nonexistent_order(self, client):
        """Test checkout fails for non-existent order."""
        response = client.post("/api/orders/nonexistent_order/checkout")
        assert response.status_code == 404
    
    def test_duplicate_manga_returns_409(self, client):
        """Test that creating duplicate manga returns 409 Conflict."""
        manga_payload = {
            "isbn": "978-0-666666-06",
            "title": "Demon Slayer",
            "author": "Gotouge Koyoharu",
            "price": 13.99,
        }
        
        # First create should succeed
        response1 = client.post("/api/manga", json=manga_payload)
        assert response1.status_code == 201

        # Second create with same ISBN should fail
        response2 = client.post("/api/manga", json=manga_payload)
        assert response2.status_code == 409
    
    def test_duplicate_user_returns_409(self, client):
        """Test that creating duplicate user returns 409 Conflict."""
        user_payload = {
            "user_id": "dup_user",
            "email": "dup@example.com",
            "display_name": "Duplicate User"
        }
        
        # First create should succeed
        response1 = client.post("/api/users", json=user_payload)
        assert response1.status_code == 201

        # Second create with same user_id should fail
        response2 = client.post("/api/users", json=user_payload)
        assert response2.status_code == 409


class TestListAndRetrieve:
    """Test listing and retrieving resources."""
    
    def test_list_users_after_workflow(self, client):
        """Test listing users after creating several."""
        # Create multiple users
        for i in range(3):
            client.post("/api/users", json={
                "user_id": f"list_user_{i}",
                "email": f"list{i}@example.com",
                "display_name": f"List User {i}"
            })
        
        response = client.get("/api/users")
        assert response.status_code == 200
        users = response.json()
        assert len(users) == 3
    
    def test_list_manga_after_workflow(self, client):
        """Test listing manga after creating several."""
        # Create multiple manga
        for i in range(3):
            client.post("/api/manga", json={
                "isbn": f"978-0-{i:06d}-{i:02d}",
                "title": f"Manga {i}",
                "author": f"Author {i}",
                "price": 10.0 + i
            })
        
        response = client.get("/api/manga")
        assert response.status_code == 200
        manga_list = response.json()
        assert len(manga_list) == 3
    
    def test_list_orders_after_workflow(self, client):
        """Test listing orders after workflow."""
        # Setup: create user and manga
        client.post("/api/users", json={
            "user_id": "list_order_user",
            "email": "list_order@example.com",
            "display_name": "List Order User"
        })
        client.post("/api/manga", json={
            "isbn": "978-0-777777-07",
            "title": "Test Manga",
            "author": "Test Author",
            "price": 15.99
        })
        
        # Create multiple orders
        for i in range(2):
            client.post("/api/orders", json={
                "order_id": f"list_order_{i}",
                "customer_id": "list_order_user",
                "shipping_address": f"Address {i}",
                "items": [{"isbn": "978-0-777777-07", "quantity": i + 1}]
            })
        
        response = client.get("/api/orders")
        assert response.status_code == 200
        orders = response.json()
        assert len(orders) == 2