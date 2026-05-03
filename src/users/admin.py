"""Admin user classes: Admin, StoreManager, and SystemAdmin."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from .user import User, UserRole, UserStatus


class Admin(User):
    """Base class for all administrative users.

    Admin users can manage the manga catalogue and oversee orders.
    """

    def __init__(
        self,
        full_name: str,
        email: str,
        password_hash: str,
        role: UserRole = UserRole.STORE_MANAGER,
        status: UserStatus = UserStatus.ACTIVE,
        user_id: Optional[str] = None,
    ) -> None:
        """Initialise an Admin user.

        Args:
            full_name: Display name.
            email: Contact email.
            password_hash: Pre-hashed password.
            role: Admin sub-role; defaults to STORE_MANAGER.
            status: Account status; defaults to ACTIVE.
            user_id: Optional explicit UUID.
        """
        super().__init__(full_name, email, password_hash, role, status, user_id)

    # ------------------------------------------------------------------
    # Catalogue management
    # ------------------------------------------------------------------

    def add_manga_title(self, manga: Any) -> str:
        """Return an intent string for adding a manga title to the catalogue.

        Args:
            manga: Manga object or data dictionary to add.

        Returns:
            Informational string for CatalogService to action.
        """
        return f"Admin {self._user_id} is adding manga title: {manga!r}."

    def update_manga_info(self, manga_id: str, updates: Dict[str, Any]) -> str:
        """Return an intent string for updating a manga entry.

        Args:
            manga_id: ID of the manga to update.
            updates: Dictionary of field→value updates.

        Returns:
            Informational string with update context.

        Raises:
            ValueError: If updates dict is empty.
        """
        if not updates:
            raise ValueError("updates dict must contain at least one field.")
        return f"Admin {self._user_id} is updating manga '{manga_id}' with: {updates}."

    def remove_manga_listing(self, manga_id: str) -> str:
        """Return an intent string for removing a manga listing.

        Args:
            manga_id: ID of the manga to remove.

        Returns:
            Informational string for CatalogService to action.
        """
        return f"Admin {self._user_id} is removing manga listing '{manga_id}'."

    # ------------------------------------------------------------------
    # Order management
    # ------------------------------------------------------------------

    def view_all_orders(self) -> str:
        """Return an intent string for retrieving all orders.

        Returns:
            Informational string for OrderService to action.
        """
        return f"Admin {self._user_id} is viewing all orders."

    def update_order_status(self, order_id: str, status: str) -> str:
        """Return an intent string for updating an order's status.

        Args:
            order_id: ID of the order to update.
            status: New status string (e.g. 'SHIPPED').

        Returns:
            Informational string with context.

        Raises:
            ValueError: If order_id or status is empty.
        """
        if not order_id or not order_id.strip():
            raise ValueError("order_id must not be empty.")
        if not status or not status.strip():
            raise ValueError("status must not be empty.")
        return f"Admin {self._user_id} is updating order '{order_id}' to status '{status}'."


class StoreManager(Admin):
    """A store-manager administrator who can also view inventory and generate reports."""

    def __init__(
        self,
        full_name: str,
        email: str,
        password_hash: str,
        status: UserStatus = UserStatus.ACTIVE,
        user_id: Optional[str] = None,
    ) -> None:
        """Initialise a StoreManager.

        Args:
            full_name: Display name.
            email: Contact email.
            password_hash: Pre-hashed password.
            status: Account status; defaults to ACTIVE.
            user_id: Optional explicit UUID.
        """
        super().__init__(full_name, email, password_hash, UserRole.STORE_MANAGER, status, user_id)

    def view_inventory(self) -> str:
        """Return an intent string for viewing inventory.

        Returns:
            Informational string for InventoryService to action.
        """
        return f"StoreManager {self._user_id} is viewing inventory."

    def generate_reports(
        self,
        report_type: str,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Return report generation intent data.

        Args:
            report_type: Type of report (e.g. 'SALES', 'INVENTORY').
            date_from: Optional start date for date-ranged reports.
            date_to: Optional end date for date-ranged reports.

        Returns:
            Dict with ``report_type``, ``date_from``, ``date_to``, and ``requested_by`` keys.

        Raises:
            ValueError: If report_type is empty.
        """
        if not report_type or not report_type.strip():
            raise ValueError("report_type must not be empty.")
        return {
            "report_type": report_type.strip().upper(),
            "date_from": date_from,
            "date_to": date_to,
            "requested_by": self._user_id,
        }


class SystemAdmin(Admin):
    """A system administrator with full control over users and reports."""

    def __init__(
        self,
        full_name: str,
        email: str,
        password_hash: str,
        status: UserStatus = UserStatus.ACTIVE,
        user_id: Optional[str] = None,
    ) -> None:
        """Initialise a SystemAdmin.

        Args:
            full_name: Display name.
            email: Contact email.
            password_hash: Pre-hashed password.
            status: Account status; defaults to ACTIVE.
            user_id: Optional explicit UUID.
        """
        super().__init__(full_name, email, password_hash, UserRole.SYSTEM_ADMIN, status, user_id)

    def manage_users(self, action: str, user_id: str) -> Dict[str, str]:
        """Return a user-management intent payload.

        Args:
            action: Action to perform (e.g. 'DEACTIVATE', 'REACTIVATE').
            user_id: Target user's ID.

        Returns:
            Dict with ``action``, ``target_user_id``, and ``admin_id`` keys.

        Raises:
            ValueError: If action or user_id is empty.
        """
        if not action or not action.strip():
            raise ValueError("action must not be empty.")
        if not user_id or not user_id.strip():
            raise ValueError("user_id must not be empty.")
        return {
            "action": action.strip().upper(),
            "target_user_id": user_id.strip(),
            "admin_id": self._user_id,
        }

    def generate_reports(
        self,
        report_type: str,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Return report generation intent data.

        Args:
            report_type: Type of report (e.g. 'SALES', 'USER_ACTIVITY').
            date_from: Optional start date.
            date_to: Optional end date.

        Returns:
            Dict with ``report_type``, ``date_from``, ``date_to``, and ``requested_by`` keys.

        Raises:
            ValueError: If report_type is empty.
        """
        if not report_type or not report_type.strip():
            raise ValueError("report_type must not be empty.")
        return {
            "report_type": report_type.strip().upper(),
            "date_from": date_from,
            "date_to": date_to,
            "requested_by": self._user_id,
        }

    def reset_user_password(self, user_id: str) -> Dict[str, str]:
        """Return a password-reset intent payload.

        Args:
            user_id: Target user's ID.

        Returns:
            Dict with ``target_user_id`` and ``admin_id`` keys.

        Raises:
            ValueError: If user_id is empty.
        """
        if not user_id or not user_id.strip():
            raise ValueError("user_id must not be empty.")
        return {
            "target_user_id": user_id.strip(),
            "admin_id": self._user_id,
        }
