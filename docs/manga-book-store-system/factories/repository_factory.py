from __future__ import annotations

from repositories.inmemory.inmemory_manga_repository import InMemoryMangaRepository
from repositories.inmemory.inmemory_order_repository import InMemoryOrderRepository
from repositories.manga_repository import MangaRepository
from repositories.order_repository import OrderRepository


class RepositoryFactory:
    """
    Factory Pattern: switch storage backends without changing business code.
    """

    @staticmethod
    def get_manga_repository(storage_type: str = "MEMORY") -> MangaRepository:
        storage_type = storage_type.upper()
        if storage_type == "MEMORY":
            return InMemoryMangaRepository()

        # future
        if storage_type == "FILESYSTEM":
            from repositories.stubs.filesystem_manga_repository import FileSystemMangaRepository
            return FileSystemMangaRepository(file_path="data/manga.json")

        raise ValueError(f"Invalid storage type: {storage_type}")

    @staticmethod
    def get_order_repository(storage_type: str = "MEMORY") -> OrderRepository:
        storage_type = storage_type.upper()
        if storage_type == "MEMORY":
            return InMemoryOrderRepository()

        # future placeholder
        raise ValueError(f"Invalid storage type: {storage_type}")