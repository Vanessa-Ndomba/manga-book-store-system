from __future__ import annotations
import threading
from dataclasses import dataclass


@dataclass
class InventoryDBConnection:
    """
    Singleton: ensure one shared DB connection object globally (thread-safe).
    """
    dsn: str

    _instance = None
    _lock = threading.Lock()

    @classmethod
    def instance(cls, dsn: str = "mysql://localhost:3306/manga_store") -> "InventoryDBConnection":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(dsn=dsn)
        return cls._instance