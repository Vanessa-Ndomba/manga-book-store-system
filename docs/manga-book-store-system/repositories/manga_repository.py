from __future__ import annotations

from typing import Protocol

from repositories.base import Repository
from src.catalog import Manga


class MangaRepository(Repository[Manga, str], Protocol):
    """
    Entity-specific repository interface for Manga.
    ID is ISBN (str).
    """
    pass