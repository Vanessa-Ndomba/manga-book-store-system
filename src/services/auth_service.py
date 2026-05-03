"""AuthService for the Manga Book Store system."""

from __future__ import annotations

import hashlib
import secrets
from typing import Dict, Optional

from ..users.user import User, UserRole, UserStatus, UserSession
from ..users.customer import RegisteredCustomer
from ..users.admin import StoreManager, SystemAdmin
from ..users.supplier import Supplier


class AuthService:
    """Manages user account registration, authentication, and session lifecycle.

    Attributes:
        _users: Mapping of user_id → User object.
        _sessions: Mapping of session_id → UserSession object.
        _email_index: Mapping of lower-cased email → user_id for fast lookup.
    """

    def __init__(self) -> None:
        """Initialise an empty AuthService."""
        self._users: Dict[str, User] = {}
        self._sessions: Dict[str, UserSession] = {}
        self._email_index: Dict[str, str] = {}

    # ------------------------------------------------------------------
    # Password utilities
    # ------------------------------------------------------------------

    @staticmethod
    def _hash_password(password: str) -> str:
        """Return a SHA-256 hex digest of *password*.

        Args:
            password: Plain-text password string.

        Returns:
            Hex-encoded SHA-256 digest.
        """
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @staticmethod
    def _verify_password(password: str, password_hash: str) -> bool:
        """Return True if the hash of *password* matches *password_hash*.

        Args:
            password: Plain-text password to verify.
            password_hash: Stored hex digest to compare against.

        Returns:
            True when the hashes match.
        """
        return hashlib.sha256(password.encode("utf-8")).hexdigest() == password_hash

    # ------------------------------------------------------------------
    # Account management
    # ------------------------------------------------------------------

    def register(
        self,
        full_name: str,
        email: str,
        password: str,
        role: UserRole = UserRole.CUSTOMER,
    ) -> User:
        """Register a new user account.

        Args:
            full_name: Display name.
            email: Unique email address.
            password: Plain-text password (will be hashed).
            role: Role for the new account. Defaults to CUSTOMER.

        Returns:
            The newly created User object.

        Raises:
            ValueError: If a user with the same email already exists or
                        if any required field is empty.
        """
        if not full_name or not full_name.strip():
            raise ValueError("full_name must not be empty.")
        if not email or not email.strip():
            raise ValueError("email must not be empty.")
        if not password:
            raise ValueError("password must not be empty.")

        normalised_email = email.strip().lower()
        if normalised_email in self._email_index:
            raise ValueError(f"An account with email '{normalised_email}' already exists.")

        password_hash = self._hash_password(password)

        user: User
        if role == UserRole.CUSTOMER:
            user = RegisteredCustomer(
                full_name=full_name,
                email=normalised_email,
                password_hash=password_hash,
                status=UserStatus.ACTIVE,
            )
        elif role == UserRole.STORE_MANAGER:
            user = StoreManager(
                full_name=full_name,
                email=normalised_email,
                password_hash=password_hash,
                status=UserStatus.ACTIVE,
            )
        elif role == UserRole.SYSTEM_ADMIN:
            user = SystemAdmin(
                full_name=full_name,
                email=normalised_email,
                password_hash=password_hash,
                status=UserStatus.ACTIVE,
            )
        elif role == UserRole.SUPPLIER:
            user = Supplier(
                full_name=full_name,
                email=normalised_email,
                password_hash=password_hash,
                company_name=full_name,
                status=UserStatus.ACTIVE,
            )
        else:
            user = RegisteredCustomer(
                full_name=full_name,
                email=normalised_email,
                password_hash=password_hash,
                status=UserStatus.ACTIVE,
            )

        self._users[user.user_id] = user
        self._email_index[normalised_email] = user.user_id
        return user

    def login(self, email: str, password: str, ip_address: str) -> UserSession:
        """Authenticate a user and return an active session.

        Args:
            email: Account email address.
            password: Plain-text password.
            ip_address: Client IP address.

        Returns:
            A started UserSession for the authenticated user.

        Raises:
            ValueError: If credentials are invalid or the account is not active.
        """
        normalised_email = email.strip().lower()
        user_id = self._email_index.get(normalised_email)
        if user_id is None:
            raise ValueError("Invalid email or password.")

        user = self._users[user_id]
        if not self._verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password.")
        if not user.is_active():
            raise ValueError(f"Account is not active (status: {user.status.value}).")

        session = UserSession(user_id=user_id, ip_address=ip_address)
        session.start()
        self._sessions[session.session_id] = session
        return session

    def logout(self, session_id: str) -> None:
        """Terminate an active session.

        Args:
            session_id: ID of the session to terminate.

        Raises:
            KeyError: If the session does not exist.
        """
        if session_id not in self._sessions:
            raise KeyError(f"Session '{session_id}' not found.")
        self._sessions[session_id].end()

    def validate_session(self, session_id: str) -> User:
        """Validate a session and return the associated User.

        Args:
            session_id: ID of the session to validate.

        Returns:
            The User associated with the valid, active session.

        Raises:
            KeyError: If the session does not exist.
            RuntimeError: If the session has expired or is inactive.
        """
        if session_id not in self._sessions:
            raise KeyError(f"Session '{session_id}' not found.")
        session = self._sessions[session_id]
        if not session.is_active or session.is_expired():
            raise RuntimeError(f"Session '{session_id}' is expired or inactive.")
        session.refresh_activity()
        return self._users[session.user_id]

    def get_user(self, user_id: str) -> User:
        """Retrieve a user by their ID.

        Args:
            user_id: Unique user identifier.

        Returns:
            The matching User.

        Raises:
            KeyError: If no user with the given ID exists.
        """
        if user_id not in self._users:
            raise KeyError(f"User '{user_id}' not found.")
        return self._users[user_id]

    def get_all_users(self) -> list:
        """Return all registered users.

        Returns:
            List of all User objects.
        """
        return list(self._users.values())

    def change_password(self, user_id: str, old_password: str, new_password: str) -> None:
        """Change a user's password after verifying the current one.

        Args:
            user_id: ID of the user.
            old_password: Current plain-text password for verification.
            new_password: New plain-text password to set.

        Raises:
            KeyError: If the user does not exist.
            ValueError: If old_password is incorrect or new_password is empty.
        """
        user = self.get_user(user_id)
        if not self._verify_password(old_password, user.password_hash):
            raise ValueError("Current password is incorrect.")
        if not new_password:
            raise ValueError("new_password must not be empty.")
        user._password_hash = self._hash_password(new_password)

    def deactivate_user(self, user_id: str) -> None:
        """Deactivate a user account.

        Args:
            user_id: ID of the user to deactivate.

        Raises:
            KeyError: If the user does not exist.
        """
        user = self.get_user(user_id)
        user.deactivate()

    def reset_password(self, user_id: str, new_password: str) -> str:
        """Forcibly reset a user's password (admin action).

        Args:
            user_id: ID of the target user.
            new_password: New plain-text password.

        Returns:
            A reset-confirmation token string.

        Raises:
            KeyError: If the user does not exist.
            ValueError: If new_password is empty.
        """
        if not new_password:
            raise ValueError("new_password must not be empty.")
        user = self.get_user(user_id)
        user._password_hash = self._hash_password(new_password)
        return secrets.token_urlsafe(16)
