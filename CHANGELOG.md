# Changelog

All notable changes to the MangaBookStore project are documented here.

---

## [Assignment 10] – 2026-05-03

### Added — Class Implementations (`/src`)

- **`src/users/user.py`** — Base `User` class with `UserRole` and `UserStatus` enums, and `UserSession` for session lifecycle management. Password stored as PBKDF2-HMAC-SHA256 hash with per-user salt.
- **`src/users/customer.py`** — `Customer` (base), `GuestUser` (can register/attempt login), `RegisteredCustomer` (full cart/order/profile methods) — all extending `User` via `Customer`.
- **`src/users/admin.py`** — `Admin` (base admin), `StoreManager` (inventory + reports), `SystemAdmin` (user management + reports) — all extending `User` via `Admin`.
- **`src/users/supplier.py`** — `Supplier` with `company_name`, `view_inventory()`, and `update_stock()`.
- **`src/catalog/manga.py`** — `Manga` domain class with `StockStatus` and `Genre` enums; supports `matches_search()`, `is_available()`, and `to_dict()`.
- **`src/catalog/catalog.py`** — `Catalog` (in-memory manga registry) and `CatalogService` (browsing, searching, trending, recommended).
- **`src/cart/cart_item.py`** — `CartItem` with computed `line_total`, quantity guards (`≥ 1`).
- **`src/cart/cart.py`** — `Cart` with `CartStatus` enum; supports add/remove/update/clear/convert-to-order.
- **`src/cart/cart_service.py`** — `CartService` coordinating cart lifecycle with stock validation.
- **`src/orders/order_item.py`** — `OrderItem` snapshot of purchased manga.
- **`src/orders/order.py`** — `Order` with `OrderStatus` enum; `cancel()` enforces valid status transition.
- **`src/orders/payment.py`** — `PaymentTransaction` with `PaymentMethod` and `PaymentStatus` enums.
- **`src/orders/order_service.py`** — `OrderService` orchestrating payment gateway, email, and inventory.
- **`src/services/auth_service.py`** — `AuthService` for registration, login, logout, session validation, and password change.
- **`src/services/inventory_service.py`** — `InventoryService` wrapping the `InventoryRepository` adapter.
- **`src/services/report_service.py`** — `ReportService` with `ReportType` enum; generates sales, inventory, and user-activity reports.
- **`src/services/admin_management_service.py`** — `AdminManagementService` for admin-level user and order management.
- **`src/adapters/payment_gateway.py`** — `PaymentGateway` ABC and `MockPaymentGateway` for testing.
- **`src/adapters/email_service.py`** — `EmailService` ABC and `MockEmailService` that records sent messages.
- **`src/adapters/inventory_repository.py`** — `InventoryRepository` ABC and `MockInventoryRepository` with in-memory dict storage.

### Added — Creational Patterns (`/creational_patterns`)

- **Simple Factory** (`simple_factory/user_factory.py`) — `UserFactory.create_user()` instantiates the correct user subclass from a `UserType` enum value or string.
- **Factory Method** (`factory_method/payment_processor.py`) — `PaymentProcessorCreator` hierarchy; `CreditCardProcessorCreator` and `PayPalProcessorCreator` each implement `factory_method()` to return the appropriate processor.
- **Abstract Factory** (`abstract_factory/notification_factory.py`) — `NotificationFactory` interface with `EmailNotificationFactory` and `SmsNotificationFactory` producing families of `OrderConfirmationNotifier`, `RegistrationNotifier`, and `PasswordResetNotifier` objects.
- **Builder** (`builder/order_builder.py`) — `OrderBuilder` fluent API for constructing `Order` objects; validates required fields (`items`, `delivery_address`, `payment_method`) and optional fields (`discount`, `gift_wrap`, `special_notes`) before building.
- **Prototype** (`prototype/manga_prototype_cache.py`) — `MangaPrototypeCache` pre-loads action, romance, and pre-order templates; `clone()` (shallow) and `deep_clone()` (independent copy) both assign fresh UUIDs.
- **Singleton** (`singleton/database_connection.py`) — `DatabaseConnection` uses double-checked locking with `threading.Lock` to guarantee a single instance across all threads. Includes a `reset()` class method for test isolation only.

### Added — Unit Tests (`/tests`)

- **`tests/test_simple_factory.py`** — 12 tests: correct type creation, unique IDs, attribute validation, invalid type errors, and customer-method edge cases.
- **`tests/test_factory_method.py`** — 17 tests: successful payments, zero/negative amount failures, refunds, invalid credentials, creator delegation, and unique transaction ID generation.
- **`tests/test_abstract_factory.py`** — 12 tests: correct notifier types, message content, multiple-message accumulation, and interchangeability across factories.
- **`tests/test_builder.py`** — 27 tests: valid builds, subtotal/discount/total calculations, discount capping, optional fields, unique IDs, and all required-field validation errors.
- **`tests/test_prototype.py`** — 20 tests: clone independence, deep-clone tag isolation, attribute equality, cache registry operations, unknown-key errors, and pre-order stock status.
- **`tests/test_singleton.py`** — 14 tests: same-instance guarantee, connection lifecycle, query counter, thread-safety with 20 concurrent threads, and reset isolation.

**Total: 102 tests — all passing.**

### Added — Configuration

- **`requirements.txt`** — `pytest>=7.4.0`, `pytest-cov>=4.1.0`.
- **`pytest.ini`** — `testpaths = tests`, verbose short-traceback output.

### Updated — Documentation

- **`README.md`** — Added Assignment 10 section with language justification, inferred class model table, creational pattern justification table, test-running instructions, and full repository structure diagram.
- **`CHANGELOG.md`** — This file (initial entry).

---

## Prior Assignments

### [Assignment 9] – Class Diagram & Domain Model
- `docs/assignment9/Class-Diagram.md` — Mermaid class diagram (placeholder updated from prior work).
- `docs/assignment9/domain-model.md` — Full domain model with 7 entities, business rules, and FR traceability.
- `docs/assignment9/reflection.md` — Reflection on translating use cases to class responsibilities.

### [Assignment 8] – Object State & Activity Workflow Modeling
- Added 8 state-transition diagrams and 8 activity diagrams covering: user account/session, manga listing, shopping cart, order, payment, inventory item, and shipment lifecycle.
- Full traceability matrix and reflection in `docs/assignment8/`.

### [Assignments 1–7]
- System requirements, stakeholder analysis, use-case specifications, test cases, product backlog, sprint planning, architecture diagrams, and agile reflections documented in the repository root and `docs/`.
