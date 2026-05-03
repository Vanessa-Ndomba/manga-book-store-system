"""OrderService for the Manga Book Store system."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional

from .order import Order, OrderStatus
from .order_item import OrderItem
from .payment import PaymentMethod, PaymentStatus, PaymentTransaction

if TYPE_CHECKING:
    from ..adapters.email_service import EmailService
    from ..adapters.inventory_repository import InventoryRepository
    from ..adapters.payment_gateway import PaymentGateway
    from ..cart.cart import Cart
    from ..users.user import User


class OrderService:
    """Orchestrates order placement, cancellation, and status updates.

    Co-ordinates with a payment gateway, email service, and inventory
    repository to complete the full order lifecycle.

    Attributes:
        _payment_gateway: Adapter for processing payments.
        _email_service: Adapter for sending transactional emails.
        _inventory_repo: Adapter for querying and updating stock.
        _orders: In-memory store of Order objects keyed by order_id.
    """

    def __init__(
        self,
        payment_gateway: "PaymentGateway",
        email_service: "EmailService",
        inventory_repo: "InventoryRepository",
    ) -> None:
        """Initialise the OrderService with its external adapters.

        Args:
            payment_gateway: Payment processing adapter.
            email_service: Email sending adapter.
            inventory_repo: Inventory storage adapter.
        """
        self._payment_gateway = payment_gateway
        self._email_service = email_service
        self._inventory_repo = inventory_repo
        self._orders: Dict[str, Order] = {}
        self._payments: Dict[str, PaymentTransaction] = {}

    # ------------------------------------------------------------------
    # Core order operations
    # ------------------------------------------------------------------

    def place_order(
        self,
        cart: "Cart",
        user: "User",
        delivery_address: str,
    ) -> Order:
        """Create and process a new order from an active cart.

        Steps:
        1. Validate stock for all cart items.
        2. Build the Order and OrderItem records.
        3. Process payment via the payment gateway.
        4. Deduct stock for each item.
        5. Convert the cart.
        6. Send confirmation email.

        Args:
            cart: The customer's active, non-empty Cart.
            user: The customer placing the order.
            delivery_address: Delivery address string.

        Returns:
            The newly created and persisted Order.

        Raises:
            RuntimeError: If stock validation fails or payment is declined.
            ValueError: If the cart is empty.
        """
        if cart.is_empty():
            raise ValueError("Cannot place an order from an empty cart.")

        self.validate_stock(cart)

        order = Order(
            user_id=user.user_id,
            delivery_address=delivery_address,
        )
        for ci in cart.get_items():
            order.add_item(
                OrderItem(
                    manga_id=ci.manga_id,
                    manga_title=ci.manga_title,
                    quantity=ci.quantity,
                    unit_price=ci.unit_price_at_add,
                )
            )

        # Process payment (default to CREDIT_CARD; real systems would take method as input)
        payment = PaymentTransaction(
            order_id=order.order_id,
            method=PaymentMethod.CREDIT_CARD,
            amount=order.total_amount,
        )
        success = self._payment_gateway.process_payment(
            order.order_id, order.total_amount, PaymentMethod.CREDIT_CARD
        )
        if success:
            payment.authorize()
            order.update_status(OrderStatus.PROCESSING)
        else:
            payment.fail("Payment gateway declined the transaction.")
            order.update_status(OrderStatus.CANCELLED)
            self._payments[payment.payment_id] = payment
            self._orders[order.order_id] = order
            raise RuntimeError(
                f"Payment failed for order '{order.order_id}'. Order has been cancelled."
            )

        # Deduct stock
        for ci in cart.get_items():
            self._inventory_repo.reserve_stock(ci.manga_id, ci.quantity)

        cart.convert_to_order()

        self._payments[payment.payment_id] = payment
        self._orders[order.order_id] = order

        self._email_service.send_order_confirmation(user.email, order)

        return order

    def cancel_order(self, order_id: str, user: "User") -> Order:
        """Cancel an existing order and issue a refund.

        Args:
            order_id: ID of the order to cancel.
            user: The user requesting the cancellation.

        Returns:
            The cancelled Order.

        Raises:
            KeyError: If the order does not exist.
            RuntimeError: If the order cannot be cancelled or refund fails.
        """
        order = self.get_order(order_id)
        order.cancel()

        # Release reserved stock
        for item in order.get_items():
            self._inventory_repo.release_stock(item.manga_id, item.quantity)

        # Refund the associated payment
        for payment in self._payments.values():
            if payment.order_id == order_id and payment.status == PaymentStatus.AUTHORIZED:
                self._payment_gateway.refund_payment(payment.payment_id)
                payment.refund()
                break

        return order

    def update_order_status(
        self,
        order_id: str,
        status: OrderStatus,
        admin: "User",
    ) -> Order:
        """Update the status of an order (admin action).

        Args:
            order_id: ID of the order.
            status: New OrderStatus value.
            admin: The admin user performing the update.

        Returns:
            The updated Order.

        Raises:
            KeyError: If the order does not exist.
            ValueError: If status is not a valid OrderStatus.
        """
        order = self.get_order(order_id)
        order.update_status(status)
        return order

    # ------------------------------------------------------------------
    # Query methods
    # ------------------------------------------------------------------

    def get_order(self, order_id: str) -> Order:
        """Retrieve an order by its ID.

        Args:
            order_id: Unique order identifier.

        Returns:
            The matching Order.

        Raises:
            KeyError: If no order with the given ID exists.
        """
        if order_id not in self._orders:
            raise KeyError(f"Order '{order_id}' not found.")
        return self._orders[order_id]

    def get_user_orders(self, user_id: str) -> List[Order]:
        """Return all orders belonging to a specific user.

        Args:
            user_id: ID of the user.

        Returns:
            List of Order objects for the user, sorted by order_date descending.
        """
        user_orders = [o for o in self._orders.values() if o.user_id == user_id]
        user_orders.sort(key=lambda o: o.order_date, reverse=True)
        return user_orders

    def get_all_orders(self) -> List[Order]:
        """Return all orders in the system.

        Returns:
            List of all Order objects.
        """
        return list(self._orders.values())

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------

    def validate_stock(self, cart: "Cart") -> None:
        """Verify that sufficient stock exists for every item in the cart.

        Args:
            cart: The cart to validate.

        Raises:
            RuntimeError: If any item lacks sufficient stock.
        """
        for item in cart.get_items():
            available = self._inventory_repo.get_stock(item.manga_id)
            if available < item.quantity:
                raise RuntimeError(
                    f"Insufficient stock for manga '{item.manga_id}'. "
                    f"Available: {available}, requested: {item.quantity}."
                )
