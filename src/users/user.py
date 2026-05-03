"""User domain models: base User class, UserRole enum, UserStatus enum, and UserSession."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional


class UserRole(Enum):
    """Enumeration of possible roles a user can hold in the system."""

    GUEST = "guest"
    CUSTOMER = "customer"
    STORE_MANAGER = "store_manager"
    SYSTEM_ADMIN = "system_admin"
    SUPPLIER = "supplier"


class UserStatus(Enum):
    """Enumeration of possible account statuses."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"


class User:
    """Abstract base representation of any user in the Manga Book Store system.

    Attributes:
        _user_id: Unique identifier for the user.
        _full_name: Full display name.
        _email: Contact and login email address.
        _password_hash: Hashed password string.
        _role: The UserRole assigned to this account.
        _status: Current UserStatus of the account.
        _created_at: UTC timestamp of account creation.
    """

    def __init__(
        self,
        full_name: str,
        email: str,
        password_hash: str,
        role: UserRole,
        status: UserStatus = UserStatus.PENDING_VERIFICATION,
        user_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        """Initialise a User instance.

        Args:
            full_name: Display name of the user.
            email: Unique email address used for login and contact.
            password_hash: Pre-hashed password string.
            role: Role granted to this user.
            status: Initial account status. Defaults to PENDING_VERIFICATION.
            user_id: Optional explicit UUID; auto-generated when omitted.
            created_at: Optional explicit creation timestamp; defaults to UTC now.

        Raises:
            ValueError: If full_name or email is empty.
        """
        if not full_name or not full_name.strip():
            raise ValueError("full_name must not be empty.")
        if not email or not email.strip():
            raise ValueError("email must not be empty.")

        self._user_id: str = user_id or str(uuid.uuid4())
        self._full_name: str = full_name.strip()
        self._email: str = email.strip().lower()
        self._password_hash: str = password_hash
        self._role: UserRole = role
        self._status: UserStatus = status
        self._created_at: datetime = created_at or datetime.now(timezone.utc)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def user_id(self) -> str:
        """Unique user identifier."""
        return self._user_id

    @property
    def full_name(self) -> str:
        """Full display name of the user."""
        return self._full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        """Set a new display name.

        Raises:
            ValueError: If the value is blank.
        """
        if not value or not value.strip():
            raise ValueError("full_name must not be empty.")
        self._full_name = value.strip()

    @property
    def email(self) -> str:
        """Email address (lower-cased)."""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """Set a new email address.

        Raises:
            ValueError: If the value is blank.
        """
        if not value or not value.strip():
            raise ValueError("email must not be empty.")
        self._email = value.strip().lower()

    @property
    def password_hash(self) -> str:
        """Hashed password string (read-only via property)."""
        return self._password_hash

    def _update_password_hash(self, new_hash: str) -> None:
        """Update the stored password hash.

        Intended for use by AuthService only; not part of the public API.

        Args:
            new_hash: The new password hash string to store.

        Raises:
            ValueError: If new_hash is empty.
        """
        if not new_hash:
            raise ValueError("new_hash must not be empty.")
        self._password_hash = new_hash

    @property
    def role(self) -> UserRole:
        """Role assigned to this user account."""
        return self._role

    @property
    def status(self) -> UserStatus:
        """Current status of the user account."""
        return self._status

    @property
    def created_at(self) -> datetime:
        """UTC timestamp when the account was created."""
        return self._created_at

    # ------------------------------------------------------------------
    # Convenience accessors (explicit get_* methods per specification)
    # ------------------------------------------------------------------

    def get_user_id(self) -> str:
        """Return the unique user identifier."""
        return self._user_id

    def get_full_name(self) -> str:
        """Return the full display name."""
        return self._full_name

    def get_email(self) -> str:
        """Return the email address."""
        return self._email

    def get_role(self) -> UserRole:
        """Return the user's role."""
        return self._role

    def get_status(self) -> UserStatus:
        """Return the user's current status."""
        return self._status

    # ------------------------------------------------------------------
    # Behaviour
    # ------------------------------------------------------------------

    def is_active(self) -> bool:
        """Return True if the account status is ACTIVE."""
        return self._status == UserStatus.ACTIVE

    def update_profile(self, full_name: str, email: str) -> None:
        """Update the user's display name and email.

        Args:
            full_name: New display name.
            email: New email address.

        Raises:
            ValueError: If either argument is blank.
        """
        self.full_name = full_name
        self.email = email

    def deactivate(self) -> None:
        """Set the account status to INACTIVE."""
        self._status = UserStatus.INACTIVE

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"user_id={self._user_id!r}, "
            f"email={self._email!r}, "
            f"role={self._role.value!r}, "
            f"status={self._status.value!r})"
        )


# ---------------------------------------------------------------------------
# UserSession
# ---------------------------------------------------------------------------


class UserSession:
    """Represents an active login session for a user.

    Attributes:
        _session_id: Unique session identifier.
        _user_id: Identifier of the owning user.
        _created_at: UTC timestamp when the session was started.
        _last_activity_at: UTC timestamp of the most recent activity.
        _expires_at: UTC timestamp after which the session is invalid.
        _ip_address: IP address from which the session was initiated.
        _is_active: Whether the session is currently active.
    """

    DEFAULT_TTL_MINUTES: int = 60

    def __init__(
        self,
        user_id: str,
        ip_address: str,
        ttl_minutes: int = DEFAULT_TTL_MINUTES,
        session_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        """Initialise a UserSession.

        Args:
            user_id: ID of the user this session belongs to.
            ip_address: Client IP address.
            ttl_minutes: Session lifetime in minutes. Defaults to 60.
            session_id: Optional explicit session UUID.
            created_at: Optional explicit creation timestamp.
        """
        now = created_at or datetime.now(timezone.utc)
        self._session_id: str = session_id or str(uuid.uuid4())
        self._user_id: str = user_id
        self._created_at: datetime = now
        self._last_activity_at: datetime = now
        self._expires_at: datetime = now + timedelta(minutes=ttl_minutes)
        self._ip_address: str = ip_address
        self._is_active: bool = False

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def session_id(self) -> str:
        """Unique session identifier."""
        return self._session_id

    @property
    def user_id(self) -> str:
        """ID of the user who owns this session."""
        return self._user_id

    @property
    def created_at(self) -> datetime:
        """UTC timestamp when the session was created."""
        return self._created_at

    @property
    def last_activity_at(self) -> datetime:
        """UTC timestamp of the last recorded activity."""
        return self._last_activity_at

    @property
    def expires_at(self) -> datetime:
        """UTC timestamp after which the session expires."""
        return self._expires_at

    @property
    def ip_address(self) -> str:
        """IP address that originated the session."""
        return self._ip_address

    @property
    def is_active(self) -> bool:
        """Whether the session is currently active."""
        return self._is_active

    # ------------------------------------------------------------------
    # Behaviour
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Mark the session as active.

        Raises:
            RuntimeError: If the session has already expired.
        """
        if self.is_expired():
            raise RuntimeError("Cannot start an already-expired session.")
        self._is_active = True

    def refresh_activity(self) -> None:
        """Update the last activity timestamp to now.

        Raises:
            RuntimeError: If the session is not active or has expired.
        """
        if not self._is_active or self.is_expired():
            raise RuntimeError("Cannot refresh an inactive or expired session.")
        self._last_activity_at = datetime.now(timezone.utc)

    def is_expired(self) -> bool:
        """Return True if the current time has passed the expiry timestamp."""
        return datetime.now(timezone.utc) >= self._expires_at

    def end(self) -> None:
        """Terminate the session."""
        self._is_active = False

    def __repr__(self) -> str:
        return (
            f"UserSession("
            f"session_id={self._session_id!r}, "
            f"user_id={self._user_id!r}, "
            f"is_active={self._is_active!r})"
        )
