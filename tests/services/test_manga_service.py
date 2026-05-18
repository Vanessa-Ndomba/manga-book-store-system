import pytest

from services.exceptions import AlreadyExistsError, NotFoundError

# Adjust these imports if your file/class names differ:
from services.manga_service import MangaService
from src.catalog import Manga


class FakeMangaRepo:
    def __init__(self):
        self.storage = {}

    def save(self, entity: Manga):
        self.storage[entity.isbn] = entity
        return entity

    def find_by_id(self, isbn: str):
        return self.storage.get(isbn)

    def find_all(self):
        return list(self.storage.values())

    def delete(self, isbn: str):
        self.storage.pop(isbn, None)


def test_create_manga_success():
    repo = FakeMangaRepo()
    service = MangaService(repo)

    m = Manga(isbn="978-500", title="Naruto", author="Kishimoto", price=12.99)
    created = service.create_manga(m)
    assert created.isbn == "978-500"


def test_create_manga_duplicate_raises():
    repo = FakeMangaRepo()
    service = MangaService(repo)

    m = Manga(isbn="978-501", title="Naruto", author="Kishimoto", price=12.99)
    service.create_manga(m)

    with pytest.raises(AlreadyExistsError):
        service.create_manga(m)


def test_get_manga_missing_raises():
    repo = FakeMangaRepo()
    service = MangaService(repo)

    with pytest.raises(NotFoundError):
        service.get_manga("missing-isbn")