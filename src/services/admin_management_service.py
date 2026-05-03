"""AdminManagementService for the Manga Book Store system."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from ..users.user import User, UserStatus

if TYPE_CHECKING:
    from ..orders.order import Order, OrderStatus
    from ..orders.order_service import OrderService
    from ..services.auth_service import AuthService
    from ..catalog.catalog import CatalogService


class AdminManagementService:
    """Provides administrative operations over users, orders, and the catalogue.

    Delegates to :class:`~services.auth_service.AuthService` and
    :class:`~catalog.catalog.CatalogService` for the underlying data
    operations, enforcing that only admin-role users can perform
    privileged actions.

    Attributes:
        _auth_service: AuthService for user management.
        _catalog_service: CatalogService for catalogue management.
    """

    def __init__(
        self,
        auth_service: "AuthService",
        catalog_service: "CatalogService",
    ) -> None:
        """Initialise the AdminManagementService.

        Args:
            auth_service: Provides user CRUD and password management.
            catalog_service: Provides manga catalogue operations.
        """
        self._auth_service = auth_service
        self._catalog_service = catalog_service

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _assert_admin(admin: User) -> None:
        """Raise PermissionError unless *admin* holds an admin role.

        Args:
            admin: The user performing the privileged action.

        Raises:
            PermissionError: If the user is not a STORE_MANAGER or SYSTEM_ADMIN.
        """
        from ..users.user import UserRole

        admin_roles = {UserRole.STORE_MANAGER, UserRole.SYSTEM_ADMIN}
        if admin.role not in admin_roles:
            raise PermissionError(
                f"User '{admin.user_id}' with role '{admin.role.value}' "
                "does not have administrative privileges."
            )

    # ------------------------------------------------------------------
    # User management
    # ------------------------------------------------------------------

    def get_all_users(self) -> List[User]:
        """Return all registered users in the system.

        Returns:
            List of all User objects.
        """
        return self._auth_service.get_all_users()

    def get_user(self, user_id: str) -> User:
        """Retrieve a specific user by their ID.

        Args:
            user_id: Unique user identifier.

        Returns:
            The matching User.

        Raises:
            KeyError: If no user with the given ID exists.
        """
        return self._auth_service.get_user(user_id)

    def deactivate_user(self, admin: User, user_id: str) -> None:
        """Deactivate a user account.

        Args:
            admin: The admin requesting the action.
            user_id: ID of the user to deactivate.

        Raises:
            PermissionError: If *admin* lacks admin privileges.
            KeyError: If the target user does not exist.
        """
        self._assert_admin(admin)
        self._auth_service.deactivate_user(user_id)

    def reactivate_user(self, admin: User, user_id: str) -> None:
        """Reactivate a previously deactivated user account.

        Args:
            admin: The admin requesting the action.
            user_id: ID of the user to reactivate.

        Raises:
            PermissionError: If *admin* lacks admin privileges.
            KeyError: If the target user does not exist.
        """
        self._assert_admin(admin)
        user = self._auth_service.get_user(user_id)
        user._status = UserStatus.ACTIVE

    def reset_password(self, admin: User, user_id: str, new_password: str) -> str:
        """Forcibly reset a user's password.

        Args:
            admin: The admin requesting the action.
            user_id: ID of the target user.
            new_password: New plain-text password.

        Returns:
            A reset-confirmation token string.

        Raises:
            PermissionError: If *admin* lacks admin privileges.
            KeyError: If the target user does not exist.
            ValueError: If new_password is empty.
        """
        self._assert_admin(admin)
        return self._auth_service.reset_password(user_id, new_password)

    # ------------------------------------------------------------------
    # Order management
    # ------------------------------------------------------------------

    def get_all_orders(self, order_service: "OrderService") -> List["Order"]:
        """Return all orders in the system.

        Args:
            order_service: The OrderService to query.

        Returns:
            List of all Order objects.
        """
        return order_service.get_all_orders()

    def update_order_status(
        self,
        admin: User,
        order_id: str,
        new_status: "OrderStatus",
        order_service: "OrderService",
    ) -> "Order":
        """Update the status of an order.

        Args:
            admin: The admin requesting the action.
            order_id: ID of the order to update.
            new_status: New OrderStatus value.
            order_service: The OrderService managing orders.

        Returns:
            The updated Order.

        Raises:
            PermissionError: If *admin* lacks admin privileges.
            KeyError: If the order does not exist.
        """
        self._assert_admin(admin)
        return order_service.update_order_status(order_id, new_status, admin)
