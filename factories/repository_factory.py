from __future__ import annotations

from repositories.inmemory.inmemory_manga_repository import InMemoryMangaRepository
from repositories.inmemory.inmemory_order_repository import InMemoryOrderRepository
from repositories.inmemory.inmemory_user_repository import InMemoryUserRepository
from repositories.manga_repository import MangaRepository
from repositories.order_repository import OrderRepository
from repositories.user_repository import UserRepository


class RepositoryFactory:
    """
    Factory Pattern: switch storage backends without changing business code.
    """
    _manga_repo = None
    _order_repo = None
    _user_repo = None

    @staticmethod
    def get_manga_repository(storage_type: str = "MEMORY") -> MangaRepository:
        storage_type = storage_type.upper()
        if storage_type == "MEMORY":
            if RepositoryFactory._manga_repo is None:
                RepositoryFactory._manga_repo = InMemoryMangaRepository()
            return RepositoryFactory._manga_repo

        # future
        if storage_type == "FILESYSTEM":
            from repositories.stubs.filesystem_manga_repository import FileSystemMangaRepository
            return FileSystemMangaRepository(file_path="data/manga.json")

        raise ValueError(f"Invalid storage type: {storage_type}")

    @staticmethod
    def get_order_repository(storage_type: str = "MEMORY") -> OrderRepository:
        storage_type = storage_type.upper()
        if storage_type == "MEMORY":
            if RepositoryFactory._order_repo is None:
                RepositoryFactory._order_repo = InMemoryOrderRepository()
            return RepositoryFactory._order_repo

        # future placeholder
        raise ValueError(f"Invalid storage type: {storage_type}")

    @staticmethod
    def get_user_repository(storage_type: str = "MEMORY") -> UserRepository:
        storage_type = storage_type.upper()
        if storage_type == "MEMORY":
            if RepositoryFactory._user_repo is None:
                RepositoryFactory._user_repo = InMemoryUserRepository()
            return RepositoryFactory._user_repo

        raise ValueError(f"Invalid storage type: {storage_type}")