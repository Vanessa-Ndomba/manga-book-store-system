"""CartService for the Manga Book Store system."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional

from .cart import Cart

if TYPE_CHECKING:
    from ..catalog.catalog import CatalogService
    from ..adapters.inventory_repository import InventoryRepository
    from ..orders.order_service import OrderService


class CartService:
    """Manages shopping carts for all users.

    Maintains one active cart per user and co-ordinates with
    :class:`~catalog.catalog.CatalogService` and
    :class:`~adapters.inventory_repository.InventoryRepository` to validate
    stock levels before adding or updating items.

    Attributes:
        _carts: Mapping of user_id → active Cart instance.
    """

    def __init__(self) -> None:
        """Initialise the CartService with an empty cart registry."""
        self._carts: Dict[str, Cart] = {}

    # ------------------------------------------------------------------
    # Cart lifecycle
    # ------------------------------------------------------------------

    def get_or_create_cart(self, user_id: str) -> Cart:
        """Return the active cart for *user_id*, creating one if needed.

        Args:
            user_id: ID of the user requesting their cart.

        Returns:
            The user's active Cart instance.
        """
        if user_id not in self._carts:
            self._carts[user_id] = Cart(user_id)
        return self._carts[user_id]

    # ------------------------------------------------------------------
    # Item operations
    # ------------------------------------------------------------------

    def add_to_cart(
        self,
        user_id: str,
        manga_id: str,
        qty: int,
        catalog_service: "CatalogService",
        inventory_repo: "InventoryRepository",
    ) -> Cart:
        """Add a manga to the user's cart after validating stock.

        Args:
            user_id: ID of the user.
            manga_id: ID of the manga to add.
            qty: Requested quantity (must be >= 1).
            catalog_service: CatalogService to fetch manga details.
            inventory_repo: InventoryRepository to check stock.

        Returns:
            The updated Cart.

        Raises:
            ValueError: If qty < 1.
            KeyError: If manga_id does not exist in the catalogue.
            RuntimeError: If sufficient stock is unavailable.
        """
        if qty < 1:
            raise ValueError("qty must be at least 1.")

        manga = catalog_service.get_manga(manga_id)
        available_stock = inventory_repo.get_stock(manga_id)
        cart = self.get_or_create_cart(user_id)

        # Account for quantity already in the cart
        existing_item = cart.get_item(manga_id)
        current_in_cart = existing_item.quantity if existing_item else 0

        if available_stock < current_in_cart + qty:
            raise RuntimeError(
                f"Insufficient stock for '{manga.title}'. "
                f"Available: {available_stock}, already in cart: {current_in_cart}, requested: {qty}."
            )

        cart.add_item(manga_id, manga.title, qty, manga.price)
        return cart

    def remove_from_cart(self, user_id: str, manga_id: str) -> Cart:
        """Remove a manga from the user's cart.

        Args:
            user_id: ID of the user.
            manga_id: ID of the manga to remove.

        Returns:
            The updated Cart.

        Raises:
            KeyError: If the user has no cart or the manga is not in it.
        """
        cart = self._get_existing_cart(user_id)
        cart.remove_item(manga_id)
        return cart

    def update_cart_quantity(
        self,
        user_id: str,
        manga_id: str,
        qty: int,
        inventory_repo: "InventoryRepository",
    ) -> Cart:
        """Update the quantity of a cart item after validating stock.

        Args:
            user_id: ID of the user.
            manga_id: ID of the manga to update.
            qty: New quantity (must be >= 1).
            inventory_repo: InventoryRepository to check stock.

        Returns:
            The updated Cart.

        Raises:
            ValueError: If qty < 1.
            KeyError: If the user has no cart or the manga is not in it.
            RuntimeError: If sufficient stock is unavailable.
        """
        if qty < 1:
            raise ValueError("qty must be at least 1.")
        cart = self._get_existing_cart(user_id)
        available_stock = inventory_repo.get_stock(manga_id)
        if available_stock < qty:
            raise RuntimeError(
                f"Insufficient stock for manga '{manga_id}'. "
                f"Available: {available_stock}, requested: {qty}."
            )
        cart.update_quantity(manga_id, qty)
        return cart

    def clear_cart(self, user_id: str) -> Cart:
        """Remove all items from the user's cart.

        Args:
            user_id: ID of the user.

        Returns:
            The cleared Cart.

        Raises:
            KeyError: If the user has no existing cart.
        """
        cart = self._get_existing_cart(user_id)
        cart.clear()
        return cart

    def checkout(
        self,
        user_id: str,
        delivery_address: str,
        order_service: "OrderService",
    ) -> object:
        """Convert the active cart into an order.

        Args:
            user_id: ID of the customer checking out.
            delivery_address: Delivery address for the order.
            order_service: OrderService responsible for creating the order.

        Returns:
            The newly created Order object.

        Raises:
            KeyError: If the user has no active cart.
            RuntimeError: If the cart is empty.
        """
        from ..users.customer import RegisteredCustomer  # avoid circular imports

        cart = self._get_existing_cart(user_id)
        if cart.is_empty():
            raise RuntimeError("Cannot checkout: cart is empty.")

        # Delegate order creation to OrderService; a placeholder user object
        # is constructed so OrderService.place_order can inspect the user_id.
        placeholder_user = RegisteredCustomer(
            full_name="Customer",
            email=f"{user_id}@store.local",
            password_hash="",
            user_id=user_id,
        )
        order = order_service.place_order(cart, placeholder_user, delivery_address)
        return order

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_existing_cart(self, user_id: str) -> Cart:
        """Return the existing cart for *user_id*.

        Raises:
            KeyError: If no cart exists for the user.
        """
        if user_id not in self._carts:
            raise KeyError(f"No cart found for user '{user_id}'.")
        return self._carts[user_id]
