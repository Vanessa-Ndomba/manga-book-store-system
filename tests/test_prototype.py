from creational_patterns.prototype import MangaPrototypeCache
from src.catalog import Manga


def test_prototype_clones_manga():
    cache = MangaPrototypeCache(_cache={})
    original = Manga(isbn="978-1", title="One Piece", author="Oda", genres=["Shonen"], price=10.0)
    cache.register("featured", original)

    clone = cache.clone("featured")
    assert clone == original
    assert clone is not original