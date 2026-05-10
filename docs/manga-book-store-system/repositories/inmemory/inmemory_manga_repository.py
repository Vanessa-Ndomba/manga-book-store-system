from __future__ import annotations

from typing import Dict, List, Optional

from repositories.manga_repository import MangaRepository
from src.catalog import Manga


class InMemoryMangaRepository(MangaRepository):
    """
    HashMap/dict-backed repository for Manga.
    """

    def __init__(self) -> None:
        self._storage: Dict[str, Manga] = {}

    def save(self, entity: Manga) -> None:
        # Create/Update
        self._storage[entity.isbn] = entity

    def find_by_id(self, id: str) -> Optional[Manga]:
        return self._storage.get(id)

    def find_all(self) -> List[Manga]:
        return list(self._storage.values())

    def delete(self, id: str) -> None:
        # Delete should be idempotent (safe if missing)
        self._storage.pop(id, None)