"""
Singleton Pattern — DatabaseConnection

Justification: The bookstore backend must have exactly one connection pool to the
MySQL database to avoid resource exhaustion and inconsistent transactional state.
The Singleton ensures that every service (CatalogService, OrderService, etc.)
shares the same connection instance.  Thread-safety is provided via a
threading.Lock acquired during instance creation.
"""
from __future__ import annotations
import threading
import time
from typing import Optional, Any


class DatabaseConnection:
    """
    Thread-safe Singleton representing the application's database connection pool.

    Thread Safety
    -------------
    A class-level ``_lock`` (``threading.Lock``) is used with a double-checked
    locking pattern so that the first-time instance creation is protected from
    race conditions without imposing lock overhead on every subsequent access.
    """

    _instance: Optional["DatabaseConnection"] = None
    _lock: threading.Lock = threading.Lock()

    # ── Singleton enforcement ─────────────────────────────────────────────────

    def __new__(cls, host: str = "localhost", port: int = 3306,
                database: str = "mangabookstore", **kwargs) -> "DatabaseConnection":
        if cls._instance is None:
            with cls._lock:
                # Double-checked locking: re-verify inside the lock
                if cls._instance is None:
                    instance = super().__new__(cls)
                    instance._initialised = False
                    cls._instance = instance
        return cls._instance

    def __init__(self, host: str = "localhost", port: int = 3306,
                 database: str = "mangabookstore", **kwargs):
        # Guard: only initialise the underlying connection once
        if self._initialised:
            return
        self._host: str = host
        self._port: int = port
        self._database: str = database
        self._connection: Optional[Any] = None
        self._is_connected: bool = False
        self._query_count: int = 0
        self._initialised: bool = True

    # ── Connection lifecycle ─────────────────────────────────────────────────

    def connect(self) -> None:
        """Open the database connection (simulated)."""
        if self._is_connected:
            return
        # In production this would call a real DB driver; here we simulate.
        self._connection = object()  # sentinel representing an open connection
        self._is_connected = True

    def disconnect(self) -> None:
        """Close the database connection."""
        self._connection = None
        self._is_connected = False

    def execute_query(self, query: str, params: Optional[tuple] = None) -> list[dict]:
        """
        Execute a SQL query (simulated).

        Args:
            query: SQL string.
            params: Optional bind parameters.

        Returns:
            A list of row dicts (always empty in the simulation).

        Raises:
            RuntimeError: If the connection is not open.
        """
        if not self._is_connected:
            raise RuntimeError("DatabaseConnection is not connected. Call connect() first.")
        self._query_count += 1
        return []  # simulated empty result set

    # ── Properties ───────────────────────────────────────────────────────────

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def database(self) -> str:
        return self._database

    @property
    def query_count(self) -> int:
        return self._query_count

    # ── Utility ──────────────────────────────────────────────────────────────

    @classmethod
    def reset(cls) -> None:
        """
        Reset the singleton for testing purposes.

        .. warning::
            This method must **never** be called in production code.
        """
        with cls._lock:
            if cls._instance is not None:
                cls._instance.disconnect()
            cls._instance = None

    def __repr__(self) -> str:
        status = "connected" if self._is_connected else "disconnected"
        return (
            f"DatabaseConnection(host={self._host!r}, db={self._database!r}, "
            f"status={status}, queries={self._query_count})"
        )
