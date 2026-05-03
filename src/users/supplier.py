"""Supplier user class for the Manga Book Store system."""

from __future__ import annotations

from typing import Dict, Optional

from .user import User, UserRole, UserStatus


class Supplier(User):
    """Represents an external supplier who can view and update stock levels.

    Attributes:
        _company_name: The trading name of the supplier's company.
        _contact_email: Dedicated supplier contact email (may differ from login email).
    """

    def __init__(
        self,
        full_name: str,
        email: str,
        password_hash: str,
        company_name: str,
        contact_email: Optional[str] = None,
        status: UserStatus = UserStatus.ACTIVE,
        user_id: Optional[str] = None,
    ) -> None:
        """Initialise a Supplier.

        Args:
            full_name: Representative's display name.
            email: Login email address.
            password_hash: Pre-hashed password.
            company_name: Name of the supply company.
            contact_email: Optional separate contact email; defaults to login email.
            status: Account status; defaults to ACTIVE.
            user_id: Optional explicit UUID.

        Raises:
            ValueError: If company_name is empty.
        """
        if not company_name or not company_name.strip():
            raise ValueError("company_name must not be empty.")

        super().__init__(full_name, email, password_hash, UserRole.SUPPLIER, status, user_id)
        self._company_name: str = company_name.strip()
        self._contact_email: str = (contact_email or email).strip().lower()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def company_name(self) -> str:
        """Trading name of the supplier's company."""
        return self._company_name

    @company_name.setter
    def company_name(self, value: str) -> None:
        """Update the company name.

        Raises:
            ValueError: If value is blank.
        """
        if not value or not value.strip():
            raise ValueError("company_name must not be empty.")
        self._company_name = value.strip()

    @property
    def contact_email(self) -> str:
        """Dedicated contact email for the supplier."""
        return self._contact_email

    @contact_email.setter
    def contact_email(self, value: str) -> None:
        """Update the contact email.

        Raises:
            ValueError: If value is blank.
        """
        if not value or not value.strip():
            raise ValueError("contact_email must not be empty.")
        self._contact_email = value.strip().lower()

    # ------------------------------------------------------------------
    # Explicit getters per specification
    # ------------------------------------------------------------------

    def get_company_name(self) -> str:
        """Return the company name."""
        return self._company_name

    def get_contact_email(self) -> str:
        """Return the contact email address."""
        return self._contact_email

    # ------------------------------------------------------------------
    # Behaviour
    # ------------------------------------------------------------------

    def view_inventory(self) -> str:
        """Return an intent string for viewing current inventory levels.

        Returns:
            Informational string for InventoryService to action.
        """
        return f"Supplier '{self._company_name}' ({self._user_id}) is viewing inventory."

    def update_stock(self, manga_id: str, quantity: int) -> Dict[str, object]:
        """Return a stock-update intent payload.

        Args:
            manga_id: ID of the manga title to restock.
            quantity: Number of units being supplied (must be > 0).

        Returns:
            Dict with ``manga_id``, ``quantity``, and ``supplier_id`` keys.

        Raises:
            ValueError: If manga_id is empty or quantity is not positive.
        """
        if not manga_id or not manga_id.strip():
            raise ValueError("manga_id must not be empty.")
        if quantity <= 0:
            raise ValueError("quantity must be a positive integer.")
        return {
            "manga_id": manga_id.strip(),
            "quantity": quantity,
            "supplier_id": self._user_id,
        }
