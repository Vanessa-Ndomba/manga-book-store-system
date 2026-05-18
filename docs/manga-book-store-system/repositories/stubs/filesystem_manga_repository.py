from __future__ import annotations

from typing import List, Optional

from repositories.manga_repository import MangaRepository
from src.catalog import Manga


class FileSystemMangaRepository(MangaRepository):
    """
    Future-proofing stub:
    A file-system repository could serialize Manga objects to JSON.

    NOTE: This is intentionally a stub for Assignment 11.
    """

    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

    def save(self, entity: Manga) -> None:
        raise NotImplementedError("File system persistence not implemented yet")

    def find_by_id(self, id: str) -> Optional[Manga]:
        raise NotImplementedError("File system persistence not implemented yet")

    def find_all(self) -> List[Manga]:
        raise NotImplementedError("File system persistence not implemented yet")

    def delete(self, id: str) -> None:
        raise NotImplementedError("File system persistence not implemented yet")
