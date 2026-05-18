from repositories.inmemory.inmemory_manga_repository import InMemoryMangaRepository
from src.catalog import Manga


def test_manga_repo_crud():
    repo = InMemoryMangaRepository()

    m1 = Manga(isbn="978-1", title="Naruto", author="Kishimoto", genres=["Shonen"], price=9.99)
    m2 = Manga(isbn="978-2", title="One Piece", author="Oda", genres=["Shonen"], price=10.99)

    # Create
    repo.save(m1)
    repo.save(m2)
    assert repo.find_by_id("978-1") == m1
    assert repo.find_by_id("978-2") == m2

    # Read all
    all_items = repo.find_all()
    assert len(all_items) == 2

    # Update (same ISBN)
    m1_updated = Manga(isbn="978-1", title="Naruto Vol 1", author="Kishimoto", genres=["Shonen"], price=8.99)
    repo.save(m1_updated)
    assert repo.find_by_id("978-1") == m1_updated

    # Delete
    repo.delete("978-2")
    assert repo.find_by_id("978-2") is None

    # Delete missing is safe
    repo.delete("does-not-exist")
