# Changelog



### Added
- Python implementation for Assignment 10:
  - Domain model under `src/`:
    - `users.py` (User, Customer, Admin)
    - `catalog.py` (Manga, InventoryItem)
    - `cart.py` (Cart, CartItem)
    - `orders.py` (Order, OrderItem, OrderStatus)
  - Creational patterns under `creational_patterns/`:
    - Simple Factory (`simple_factory.py`): `PaymentMethodFactory` creates `CreditCard` and `PayPal` objects.
    - Factory Method (`factory_method.py`): `PaymentProcessor` with `CreditCardProcessor` and `PayPalProcessor`.
    - Abstract Factory (`abstract_factory.py`): Email/SMS notification family (receipt formatter + sender).
    - Builder (`builder.py`): `OrderBuilder` to construct an `Order` step-by-step with validation.
    - Prototype (`prototype.py`): `MangaPrototypeCache` for cloning preconfigured `Manga` objects.
    - Singleton (`singleton.py`): thread-safe `InventoryDBConnection`.
  - Unit tests under `tests/`:
    - Pattern tests for all six creational patterns.
    - Thread-safety test for the Singleton implementation.
    - Additional domain tests to improve coverage for `src/` modules.
- Testing and coverage configuration:
  - `requirements.txt` (pytest, pytest-cov)
  - `pytest.ini` (test discovery + coverage reporting)

### Notes
- The domain model is a lightweight implementation intended to demonstrate object creation patterns and unit testing, not a full deployed web application.
