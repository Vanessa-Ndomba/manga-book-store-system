"""Customer user classes: Customer, GuestUser, and RegisteredCustomer."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from .user import User, UserRole, UserStatus

if TYPE_CHECKING:
    pass


class Customer(User):
    """Base class for all customers of the Manga Book Store.

    Provides catalogue browsing capabilities available to any customer,
    whether guest or registered.
    """

    def __init__(
        self,
        full_name: str,
        email: str,
        password_hash: str,
        role: UserRole = UserRole.CUSTOMER,
        status: UserStatus = UserStatus.PENDING_VERIFICATION,
        user_id: Optional[str] = None,
    ) -> None:
        """Initialise a Customer.

        Args:
            full_name: Display name.
            email: Contact email.
            password_hash: Pre-hashed password.
            role: Defaults to CUSTOMER.
            status: Account status; defaults to PENDING_VERIFICATION.
            user_id: Optional explicit UUID.
        """
        super().__init__(full_name, email, password_hash, role, status, user_id)

    # ------------------------------------------------------------------
    # Catalogue interactions (return descriptive strings / stubs as the
    # actual storage is managed by CatalogService injected at call sites)
    # ------------------------------------------------------------------

    def browse_catalog(self) -> str:
        """Return a notice indicating that the catalogue is being browsed.

        Returns:
            Informational string for the calling layer to pass to CatalogService.
        """
        return f"{self._full_name} is browsing the manga catalogue."

    def search_manga(self, query: str) -> str:
        """Return a search intent string for the given query.

        Args:
            query: Free-text search term.

        Returns:
            String describing the search intent.

        Raises:
            ValueError: If the query is empty.
        """
        if not query or not query.strip():
            raise ValueError("Search query must not be empty.")
        return f"{self._full_name} is searching for: '{query.strip()}'."

    def filter_by_genre(self, genre: str) -> str:
        """Return a filter intent string for the given genre.

        Args:
            genre: Genre name or enum value string.

        Returns:
            String describing the filter intent.
        """
        return f"{self._full_name} is filtering catalogue by genre: '{genre}'."

    def view_manga_details(self, manga_id: str) -> str:
        """Return an intent string for viewing details of a specific manga.

        Args:
            manga_id: The unique identifier of the manga.

        Returns:
            String describing the view-details intent.
        """
        return f"{self._full_name} is viewing details for manga ID: '{manga_id}'."


class GuestUser(Customer):
    """An unauthenticated visitor with limited functionality.

    Guest users may browse the catalogue but must register or log in to
    make purchases.
    """

    def __init__(self) -> None:
        """Initialise a GuestUser with anonymous placeholder credentials."""
        super().__init__(
            full_name="Guest",
            email="guest@store.local",
            password_hash="",
            role=UserRole.GUEST,
            status=UserStatus.ACTIVE,
        )

    def register_account(self, full_name: str, email: str, password: str) -> Dict[str, str]:
        """Return registration intent data so the AuthService can create an account.

        Args:
            full_name: Desired display name.
            email: Desired email address.
            password: Plain-text password (will be hashed by AuthService).

        Returns:
            Dictionary with ``full_name``, ``email``, and ``password`` keys.

        Raises:
            ValueError: If any argument is empty.
        """
        if not full_name or not full_name.strip():
            raise ValueError("full_name must not be empty.")
        if not email or not email.strip():
            raise ValueError("email must not be empty.")
        if not password:
            raise ValueError("password must not be empty.")
        return {"full_name": full_name.strip(), "email": email.strip().lower(), "password": password}

    def login(self, email: str, password: str) -> Dict[str, str]:
        """Return login intent data for AuthService to process.

        Args:
            email: Account email address.
            password: Plain-text password.

        Returns:
            Dictionary with ``email`` and ``password`` keys.

        Raises:
            ValueError: If either argument is empty.
        """
        if not email or not email.strip():
            raise ValueError("email must not be empty.")
        if not password:
            raise ValueError("password must not be empty.")
        return {"email": email.strip().lower(), "password": password}


class RegisteredCustomer(Customer):
    """A fully registered and authenticated customer.

    In addition to catalogue browsing, registered customers can manage
    their shopping cart, place orders, and maintain a delivery address book.

    Attributes:
        _phone_number: Optional contact phone number.
        _delivery_addresses: List of saved delivery address strings.
    """

    def __init__(
        self,
        full_name: str,
        email: str,
        password_hash: str,
        phone_number: Optional[str] = None,
        status: UserStatus = UserStatus.ACTIVE,
        user_id: Optional[str] = None,
    ) -> None:
        """Initialise a RegisteredCustomer.

        Args:
            full_name: Display name.
            email: Contact email.
            password_hash: Pre-hashed password.
            phone_number: Optional phone number.
            status: Account status; defaults to ACTIVE.
            user_id: Optional explicit UUID.
        """
        super().__init__(full_name, email, password_hash, UserRole.CUSTOMER, status, user_id)
        self._phone_number: Optional[str] = phone_number
        self._delivery_addresses: List[str] = []

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def phone_number(self) -> Optional[str]:
        """Contact phone number, or None if not set."""
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value: Optional[str]) -> None:
        """Set a new phone number."""
        self._phone_number = value

    @property
    def delivery_addresses(self) -> List[str]:
        """Read-only view of saved delivery addresses."""
        return list(self._delivery_addresses)

    # ------------------------------------------------------------------
    # Cart operations (intent strings — CartService handles business logic)
    # ------------------------------------------------------------------

    def add_to_cart(self, manga_id: str, qty: int = 1) -> Dict[str, Any]:
        """Return add-to-cart intent data.

        Args:
            manga_id: Manga to add.
            qty: Quantity; must be >= 1.

        Returns:
            Dict with ``user_id``, ``manga_id``, and ``quantity`` keys.

        Raises:
            ValueError: If qty is less than 1.
        """
        if qty < 1:
            raise ValueError("Quantity must be at least 1.")
        return {"user_id": self._user_id, "manga_id": manga_id, "quantity": qty}

    def modify_cart(self, manga_id: str, qty: int) -> Dict[str, Any]:
        """Return modify-cart intent data.

        Args:
            manga_id: Manga to modify.
            qty: New quantity; must be >= 1.

        Returns:
            Dict with ``user_id``, ``manga_id``, and ``quantity`` keys.

        Raises:
            ValueError: If qty is less than 1.
        """
        if qty < 1:
            raise ValueError("Quantity must be at least 1.")
        return {"user_id": self._user_id, "manga_id": manga_id, "quantity": qty}

    def remove_from_cart(self, manga_id: str) -> Dict[str, str]:
        """Return remove-from-cart intent data.

        Args:
            manga_id: Manga to remove.

        Returns:
            Dict with ``user_id`` and ``manga_id`` keys.
        """
        return {"user_id": self._user_id, "manga_id": manga_id}

    def checkout(self) -> str:
        """Return a checkout intent string for CartService.

        Returns:
            String identifying the customer checking out.
        """
        return f"Customer {self._user_id} is initiating checkout."

    def place_order(self, delivery_address: str) -> Dict[str, str]:
        """Return place-order intent data.

        Args:
            delivery_address: Address to deliver the order to.

        Returns:
            Dict with ``user_id`` and ``delivery_address`` keys.

        Raises:
            ValueError: If delivery_address is empty.
        """
        if not delivery_address or not delivery_address.strip():
            raise ValueError("delivery_address must not be empty.")
        return {"user_id": self._user_id, "delivery_address": delivery_address.strip()}

    # ------------------------------------------------------------------
    # Order management
    # ------------------------------------------------------------------

    def view_order_history(self) -> str:
        """Return an intent string for fetching the order history.

        Returns:
            String for OrderService to action.
        """
        return f"Fetching order history for customer {self._user_id}."

    def track_order(self, order_id: str) -> str:
        """Return a track-order intent string.

        Args:
            order_id: The order to track.

        Returns:
            Informational string with order and user IDs.
        """
        return f"Tracking order '{order_id}' for customer {self._user_id}."

    # ------------------------------------------------------------------
    # Profile & address management
    # ------------------------------------------------------------------

    def manage_profile(self, full_name: str, email: str, phone: Optional[str] = None) -> None:
        """Update profile information for this customer.

        Args:
            full_name: New display name.
            email: New email address.
            phone: New phone number (optional).

        Raises:
            ValueError: If full_name or email is empty.
        """
        self.update_profile(full_name, email)
        if phone is not None:
            self._phone_number = phone

    def add_delivery_address(self, address: str) -> None:
        """Add a new delivery address to the address book.

        Args:
            address: Address string to store.

        Raises:
            ValueError: If address is empty.
        """
        if not address or not address.strip():
            raise ValueError("address must not be empty.")
        self._delivery_addresses.append(address.strip())

    def login(self, email: str, password: str) -> Dict[str, str]:
        """Return login intent data for AuthService to process.

        Args:
            email: Account email address.
            password: Plain-text password.

        Returns:
            Dictionary with ``email`` and ``password`` keys.

        Raises:
            ValueError: If either argument is empty.
        """
        if not email or not email.strip():
            raise ValueError("email must not be empty.")
        if not password:
            raise ValueError("password must not be empty.")
        return {"email": email.strip().lower(), "password": password}
