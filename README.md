# MangaBookStore – Online Manga Retail System

## Project Description
MangaBookStore is an online platform designed for anime and manga fans to browse, search, and purchase manga books. The system allows users to view available manga titles, add items to a shopping cart, and place orders online.

The platform also provides administrative tools for managing manga inventory, tracking customer orders, and maintaining product listings.

This system will demonstrate software engineering principles including system specification, architectural modeling, and modular system design.

## Documentation

System Specification:
[SPECIFICATION.md](SPECIFICATION.md)

System Architecture:
[ARCHITECTURE.md](ARCHITECTURE.md)

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


  ## Assignment 10: From Class Diagrams to Code (Creational Patterns + Unit Tests)

### Language Choice
This Assignment 10 implementation uses **Python** because it allows rapid, readable implementation of object-oriented designs and provides strong unit testing and coverage tooling via **pytest** and **pytest-cov**.

### Code Structure (Added for Assignment 10)
- `src/` — Manga bookstore domain model classes
  - `users.py` (User, Customer, Admin)
  - `catalog.py` (Manga, InventoryItem)
  - `cart.py` (Cart, CartItem)
  - `orders.py` (Order, OrderItem, OrderStatus)
- `creational_patterns/` — All six creational design patterns
  - `simple_factory.py` — **Simple Factory** (PaymentMethodFactory)
  - `factory_method.py` — **Factory Method** (PaymentProcessor + CreditCardProcessor/PayPalProcessor)
  - `abstract_factory.py` — **Abstract Factory** (Email/SMS notification family: formatter + sender)
  - `builder.py` — **Builder** (OrderBuilder for step-by-step order creation + validation)
  - `prototype.py` — **Prototype** (MangaPrototypeCache for cloning preconfigured Manga objects)
  - `singleton.py` — **Singleton** (thread-safe InventoryDBConnection)
- `tests/` — Unit tests for each creational pattern, including edge cases and thread-safety tests

### Creational Pattern Justification (Why each was used)
- **Simple Factory**: centralizes creation of payment method objects from user input, keeping object creation logic in one place.
- **Factory Method**: allows each payment processor type (Credit Card vs PayPal) to implement its own payment processing behavior while sharing a common interface.
- **Abstract Factory**: creates consistent notification components as a “family” (receipt formatter + sender) for different channels (Email or SMS).
- **Builder**: constructs an `Order` step-by-step and validates required fields (e.g., shipping address and at least one item).
- **Prototype**: enables efficient cloning of preconfigured `Manga` objects (e.g., featured listings) without manually reinitializing them.
- **Singleton**: ensures one shared inventory database connection instance across the system; implemented in a thread-safe manner.

### How to Run Unit Tests + Coverage
1. Create and activate a virtual environment (Windows PowerShell example):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Run tests (includes coverage summary via `pytest.ini`):
   ```powershell
   pytest
   ```



## Assignment 11: Implementing a Persistence Repository Layer

### Repository Interface Design
A generic repository interface was created to standardize CRUD operations across domain entities:

- `repositories/base.py` — `Repository[T, ID]` (generic CRUD contract)

Entity-specific repository interfaces extend the generic repository to keep type-safe, domain-focused contracts:

- `repositories/manga_repository.py` — `MangaRepository` (ID: `isbn: str`)
- `repositories/order_repository.py` — `OrderRepository` (ID: `order_id: str`)

**Justification:** Generics (`Repository[T, ID]`) avoid duplicated CRUD method definitions across each entity repository while still allowing entity-specific repositories for clarity and future extension.

### In-Memory Implementation (HashMap/Dictionary)
In-memory repositories implement the interfaces using Python dictionaries (HashMap storage):

- `repositories/inmemory/inmemory_manga_repository.py`
- `repositories/inmemory/inmemory_order_repository.py`

These repositories support full CRUD:
- `save` (create/update)
- `find_by_id` (read one)
- `find_all` (read all)
- `delete` (delete by id)

### Storage Abstraction Mechanism (Factory Pattern)
A repository factory is used to decouple business code from storage details and to allow easy swapping of storage backends:

- `factories/repository_factory.py` — `RepositoryFactory`

**Justification:** The Factory Pattern allows choosing a storage backend (e.g., `MEMORY`, `FILESYSTEM`, `DATABASE`) without changing calling code, keeping persistence concerns isolated.

### Future-Proofing (Stub Backend)
A stub for a future storage option is included to demonstrate how a new backend can be added without changing the repository interface:

- `repositories/stubs/filesystem_manga_repository.py` — `FileSystemMangaRepository` (stub; raises `NotImplementedError`)

### Tests (CRUD Verification)
Unit tests validate CRUD behavior for the in-memory repositories:

- `tests/test_inmemory_manga_repository_crud.py`
- `tests/test_inmemory_order_repository_crud.py`

### How to Run Tests
```powershell
pip install -r requirements.txt
pytest
