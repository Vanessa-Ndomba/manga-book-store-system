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

### Optional: HTML Coverage Report
```powershell
pytest --cov=src --cov=creational_patterns --cov-report=html
```
Open `htmlcov/index.html` to view the report.
