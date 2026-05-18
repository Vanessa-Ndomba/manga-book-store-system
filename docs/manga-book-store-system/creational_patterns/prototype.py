from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
from typing import Dict

from src.catalog import Manga


@dataclass
class MangaPrototypeCache:
    """
    Prototype: cache preconfigured Manga templates and clone them quickly.
    """
    _cache: Dict[str, Manga]

    def register(self, key: str, manga: Manga) -> None:
        self._cache[key] = manga

    def clone(self, key: str) -> Manga:
        if key not in self._cache:
            raise KeyError(f"Prototype not found: {key}")
        return deepcopy(self._cache[key])
