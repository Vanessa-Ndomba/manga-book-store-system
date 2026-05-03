# MangaBookStore – Online Manga Retail System

## Project Description
MangaBookStore is an online platform designed for anime and manga fans to browse, search, and purchase manga books. The system allows users to view available manga titles, add items to a shopping cart, and place orders online.

The platform also provides administrative tools for managing manga inventory, tracking customer orders, and maintaining product listings.

This system will demonstrate software engineering principles including system specification, architectural modeling, modular system design, and creational design patterns.

## Documentation

System Specification:
[SPECIFICATION.md](SPECIFICATION.md)

System Architecture:
[ARCHITECTURE.md](ARCHITECTURE.md)

---

## Assignment 10: From Class Diagrams to Code with All Creational Patterns

### Language Choice — Python

**Python** was chosen for the following reasons:
- The system is architecture-first (services, adapters, repositories) rather than UI-heavy, and Python's concise syntax lets the design intent remain front-and-centre.
- The `abc` module provides clean abstract base classes, making interface/adapter contracts self-documenting.
- `pytest` + `pytest-cov` gives a single-command test + coverage workflow with minimal configuration.
- Python's `threading.Lock` demonstrates the thread-safety requirements of the Singleton pattern clearly without boilerplate.

---

### Inferred Class Model

The class model was derived from the use-case / architecture Mermaid diagrams supplied in the assignment brief.  The following table summarises the core domain entities and services:

#### Domain Entities

| Class | Key Attributes | Key Methods |
|-------|---------------|-------------|
| `User` (base) | `_user_id`, `_full_name`, `_email`, `_password_hash`, `_role`, `_status`, `_created_at` | `update_profile()`, `deactivate()`, `is_active()` |
| `Customer(User)` | inherits User | `browse_catalog()`, `search_manga()`, `filter_by_genre()`, `view_manga_details()` |
| `GuestUser(Customer)` | inherits Customer | `register_account()`, `login()` |
| `RegisteredCustomer(Customer)` | `_phone_number`, `_delivery_addresses` | `add_to_cart()`, `modify_cart()`, `checkout()`, `place_order()`, `view_order_history()`, `track_order()` |
| `Admin(User)` | inherits User | `add_manga_title()`, `update_manga_info()`, `remove_manga_listing()`, `view_all_orders()`, `update_order_status()` |
| `StoreManager(Admin)` | inherits Admin | `view_inventory()`, `generate_reports()` |
| `SystemAdmin(Admin)` | inherits Admin | `manage_users()`, `reset_user_password()`, `generate_reports()` |
| `Supplier(User)` | `_company_name`, `_contact_email` | `view_inventory()`, `update_stock()` |
| `Manga` | `_manga_id`, `_title`, `_author`, `_isbn`, `_genre`, `_price`, `_stock_quantity`, `_stock_status` | `update_details()`, `update_price()`, `matches_search()`, `is_available()` |
| `Catalog` | `_mangas` (dict) | `add_manga()`, `remove_manga()`, `browse()`, `search()`, `filter_by_genre()` |
| `Cart` | `_cart_id`, `_user_id`, `_items`, `_status` | `add_item()`, `remove_item()`, `update_quantity()`, `calculate_total()`, `convert_to_order()` |
| `CartItem` | `_manga_id`, `_quantity`, `_unit_price_at_add` | `compute_line_total()`, `increment_qty()`, `decrement_qty()` |
| `Order` | `_order_id`, `_user_id`, `_items`, `_status`, `_total_amount`, `_delivery_address` | `place_from_cart()`, `cancel()`, `update_status()`, `compute_total()` |
| `OrderItem` | `_manga_id`, `_quantity`, `_unit_price` | `compute_line_total()` |
| `PaymentTransaction` | `_payment_id`, `_order_id`, `_method`, `_status`, `_amount` | `authorize()`, `fail()`, `refund()` |
| `UserSession` | `_session_id`, `_user_id`, `_created_at`, `_expires_at`, `_is_active` | `start()`, `refresh_activity()`, `is_expired()`, `end()` |

#### Services

| Service | Responsibility |
|---------|---------------|
| `AuthService` | Register users, login/logout, session validation, password hashing (PBKDF2-HMAC-SHA256) |
| `CatalogService` | Wraps `Catalog`; provides trending/recommended queries |
| `CartService` | Cart lifecycle; stock validation before add-to-cart |
| `OrderService` | Coordinates `PaymentGateway`, `EmailService`, `InventoryRepository` to place/cancel orders |
| `InventoryService` | Stock level queries and updates via `InventoryRepository` |
| `AdminManagementService` | User deactivation/reactivation, order status updates for admins |
| `ReportService` | Sales, inventory, and user-activity report generation |

#### External Adapters (Abstract Interfaces + Mocks)

| Adapter | Purpose |
|---------|---------|
| `PaymentGateway` | Abstract interface; `MockPaymentGateway` used in tests |
| `EmailService` | Abstract interface; `MockEmailService` records sent emails for verification |
| `InventoryRepository` | Abstract interface; `MockInventoryRepository` uses in-memory dict |

---

### Creational Pattern Justifications

| # | Pattern | Location | Bookstore Use Case | Justification |
|---|---------|----------|--------------------|---------------|
| 1 | **Simple Factory** | `creational_patterns/simple_factory/user_factory.py` | `UserFactory` creates `GuestUser`, `RegisteredCustomer`, `StoreManager`, `SystemAdmin`, or `Supplier` from a role string | Centralises all user instantiation in one place; callers never import concrete user classes directly, making it easy to add new roles. |
| 2 | **Factory Method** | `creational_patterns/factory_method/payment_processor.py` | `PaymentProcessorCreator` with `CreditCardProcessorCreator` and `PayPalProcessorCreator` subclasses | Delegates processor instantiation to subclasses; new payment providers can be added by extending the creator without touching order-processing logic. |
| 3 | **Abstract Factory** | `creational_patterns/abstract_factory/notification_factory.py` | `EmailNotificationFactory` and `SmsNotificationFactory` each produce a consistent family of notifiers (order confirmation, registration, password reset) | Guarantees that all notification objects for a given channel are created together; switching from Email to SMS only requires swapping the factory. |
| 4 | **Builder** | `creational_patterns/builder/order_builder.py` | `OrderBuilder` constructs `Order` objects step-by-step with optional discount, gift-wrap, and special notes | An order has many optional fields; the builder prevents partially-initialised orders, enforces required fields, and keeps construction logic out of the domain class. |
| 5 | **Prototype** | `creational_patterns/prototype/manga_prototype_cache.py` | `MangaPrototypeCache` stores pre-configured Manga templates (action, romance, pre-order) that can be cloned for new listings | Cloning a validated template is cheaper than re-validating every new listing from scratch; ensures consistency across entries derived from the same template. |
| 6 | **Singleton** | `creational_patterns/singleton/database_connection.py` | `DatabaseConnection` singleton with thread-safe double-checked locking | The MySQL connection pool must exist as a single shared resource; multiple instances would exhaust connections and cause inconsistent state. |

---

### Running the Tests

#### Prerequisites

```bash
pip install pytest pytest-cov
```

#### Run all tests

```bash
pytest
```

#### Run tests with coverage report (terminal)

```bash
pytest --cov=creational_patterns --cov-report=term-missing
```

#### Run tests with HTML coverage report

```bash
pytest --cov=creational_patterns --cov-report=html
# Open htmlcov/index.html in your browser
```

#### Run tests with combined src + patterns coverage

```bash
pytest --cov=creational_patterns --cov=src --cov-report=term-missing
```

---

### Repository Structure

```
manga-book-store-system/
├── src/                          # Domain class implementations
│   ├── users/                    # User hierarchy
│   │   ├── user.py               # User (base), UserRole, UserStatus, UserSession
│   │   ├── customer.py           # Customer, GuestUser, RegisteredCustomer
│   │   ├── admin.py              # Admin, StoreManager, SystemAdmin
│   │   └── supplier.py           # Supplier
│   ├── catalog/
│   │   ├── manga.py              # Manga, StockStatus, Genre
│   │   └── catalog.py            # Catalog, CatalogService
│   ├── cart/
│   │   ├── cart_item.py          # CartItem
│   │   ├── cart.py               # Cart, CartStatus
│   │   └── cart_service.py       # CartService
│   ├── orders/
│   │   ├── order_item.py         # OrderItem
│   │   ├── order.py              # Order, OrderStatus
│   │   ├── payment.py            # PaymentTransaction, PaymentMethod, PaymentStatus
│   │   └── order_service.py      # OrderService
│   ├── services/
│   │   ├── auth_service.py       # AuthService
│   │   ├── inventory_service.py  # InventoryService
│   │   ├── report_service.py     # ReportService
│   │   └── admin_management_service.py
│   └── adapters/
│       ├── payment_gateway.py    # PaymentGateway ABC + MockPaymentGateway
│       ├── email_service.py      # EmailService ABC + MockEmailService
│       └── inventory_repository.py # InventoryRepository ABC + MockInventoryRepository
│
├── creational_patterns/          # All six creational patterns
│   ├── simple_factory/user_factory.py
│   ├── factory_method/payment_processor.py
│   ├── abstract_factory/notification_factory.py
│   ├── builder/order_builder.py
│   ├── prototype/manga_prototype_cache.py
│   └── singleton/database_connection.py
│
├── tests/                        # Unit tests (102 tests)
│   ├── test_simple_factory.py
│   ├── test_factory_method.py
│   ├── test_abstract_factory.py
│   ├── test_builder.py
│   ├── test_prototype.py
│   └── test_singleton.py
│
├── requirements.txt              # pytest + pytest-cov
├── pytest.ini                    # Test configuration
└── README.md
```

## Assignment 8: Object State & Activity Workflow Modeling

- Assignment 8 index:
  - [docs/assignment8/README.md](docs/assignment8/README.md)
- State transition diagrams (8):
  - [docs/assignment8/state-diagrams/user-account-state.md](docs/assignment8/state-diagrams/user-account-state.md)
  - [docs/assignment8/state-diagrams/user-session-state.md](docs/assignment8/state-diagrams/user-session-state.md)
  - [docs/assignment8/state-diagrams/manga-listing-state.md](docs/assignment8/state-diagrams/manga-listing-state.md)
  - [docs/assignment8/state-diagrams/shopping-cart-state.md](docs/assignment8/state-diagrams/shopping-cart-state.md)
  - [docs/assignment8/state-diagrams/order-state.md](docs/assignment8/state-diagrams/order-state.md)
  - [docs/assignment8/state-diagrams/payment-transaction-state.md](docs/assignment8/state-diagrams/payment-transaction-state.md)
  - [docs/assignment8/state-diagrams/inventory-item-state.md](docs/assignment8/state-diagrams/inventory-item-state.md)
  - [docs/assignment8/state-diagrams/shipment-state.md](docs/assignment8/state-diagrams/shipment-state.md)
- Activity diagrams (8):
  - [docs/assignment8/activity-diagrams/user-registration-activity.md](docs/assignment8/activity-diagrams/user-registration-activity.md)
  - [docs/assignment8/activity-diagrams/user-login-activity.md](docs/assignment8/activity-diagrams/user-login-activity.md)
  - [docs/assignment8/activity-diagrams/search-browse-activity.md](docs/assignment8/activity-diagrams/search-browse-activity.md)
  - [docs/assignment8/activity-diagrams/cart-management-activity.md](docs/assignment8/activity-diagrams/cart-management-activity.md)
  - [docs/assignment8/activity-diagrams/checkout-payment-activity.md](docs/assignment8/activity-diagrams/checkout-payment-activity.md)
  - [docs/assignment8/activity-diagrams/admin-order-fulfillment-activity.md](docs/assignment8/activity-diagrams/admin-order-fulfillment-activity.md)
  - [docs/assignment8/activity-diagrams/admin-inventory-update-activity.md](docs/assignment8/activity-diagrams/admin-inventory-update-activity.md)
  - [docs/assignment8/activity-diagrams/profile-address-update-activity.md](docs/assignment8/activity-diagrams/profile-address-update-activity.md)
- Explanations, traceability, and reflection:
  - [docs/assignment8/explanations/state-diagrams-explanations.md](docs/assignment8/explanations/state-diagrams-explanations.md)
  - [docs/assignment8/explanations/activity-diagrams-explanations.md](docs/assignment8/explanations/activity-diagrams-explanations.md)
  - [docs/assignment8/explanations/traceability-matrix.md](docs/assignment8/explanations/traceability-matrix.md)
  - [docs/assignment8/explanations/assignment8_reflection.md](docs/assignment8/explanations/assignment8_reflection.md)
