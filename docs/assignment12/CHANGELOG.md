# Changelog 

## Added
- Service layer for Manga, Users, and Orders using repository layer (Assignment 11).
- REST API endpoints under `/api` for:
  - Manga CRUD: list, create, get by ISBN, update, delete.
  - Users CRUD: list, create, get by id, delete.
  - Orders: list, create, get by id.
- Business workflow endpoint:
  - `POST /api/orders/{order_id}/checkout` to checkout an order.

## Business Rules
- Manga ISBN must be unique.
- Orders must contain at least one item.
- Order creation requires an existing customer/user.
- Order creation requires manga ISBNs to exist.
- Checkout cannot be performed twice.

## Documentation
- Swagger UI available at `/docs`.
- OpenAPI schema exported to `docs/openapi.json`.
- Screenshot saved to `docs/swagger-ui.png`.

## Tests
- Unit tests for services in `tests/services`.
- Integration tests for API routes in `tests/api`.
