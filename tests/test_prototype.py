"""Unit tests for the Prototype pattern (MangaPrototypeCache)."""
import pytest
from decimal import Decimal
from creational_patterns.prototype.manga_prototype_cache import (
    MangaPrototypeCache,
    MangaPrototype,
    Genre,
    StockStatus,
)


class TestMangaPrototype:
    """Tests for the MangaPrototype clone mechanics."""

    def _make_prototype(self) -> MangaPrototype:
        p = MangaPrototype(
            title="Dragon Ball Vol. 1",
            author="Akira Toriyama",
            isbn="978-1-56931-920-1",
            genre=Genre.ACTION,
            price=Decimal("9.99"),
            description="Goku's first adventure.",
            stock_status=StockStatus.IN_STOCK,
        )
        p.add_tag("shonen")
        p.add_tag("classic")
        return p

    def test_clone_is_different_object(self):
        original = self._make_prototype()
        clone = original.clone()
        assert clone is not original

    def test_clone_has_different_id(self):
        original = self._make_prototype()
        clone = original.clone()
        assert clone.manga_id != original.manga_id

    def test_clone_shares_same_attributes(self):
        original = self._make_prototype()
        clone = original.clone()
        assert clone.title == original.title
        assert clone.author == original.author
        assert clone.isbn == original.isbn
        assert clone.price == original.price
        assert clone.genre == original.genre

    def test_deep_clone_is_different_object(self):
        original = self._make_prototype()
        deep = original.deep_clone()
        assert deep is not original

    def test_deep_clone_has_different_id(self):
        original = self._make_prototype()
        deep = original.deep_clone()
        assert deep.manga_id != original.manga_id

    def test_deep_clone_tags_independent(self):
        original = self._make_prototype()
        deep = original.deep_clone()
        deep.add_tag("new-tag")
        # Original should NOT have the new tag
        assert "new-tag" not in original.tags
        assert "new-tag" in deep.tags

    def test_modifying_clone_title_does_not_affect_original(self):
        original = self._make_prototype()
        clone = original.clone()
        clone.title = "Modified Title"
        assert original.title == "Dragon Ball Vol. 1"

    def test_modifying_clone_price_does_not_affect_original(self):
        original = self._make_prototype()
        clone = original.clone()
        clone.price = Decimal("14.99")
        assert original.price == Decimal("9.99")

    def test_negative_price_raises(self):
        p = self._make_prototype()
        with pytest.raises(ValueError, match="negative"):
            p.price = Decimal("-1.00")

    def test_to_dict_contains_expected_keys(self):
        p = self._make_prototype()
        d = p.to_dict()
        for key in ("manga_id", "title", "author", "isbn", "genre", "price", "stock_status"):
            assert key in d


class TestMangaPrototypeCache:
    """Tests for the MangaPrototypeCache registry."""

    def setup_method(self):
        self.cache = MangaPrototypeCache()

    def test_default_prototypes_loaded(self):
        keys = self.cache.list_keys()
        assert "action_template" in keys
        assert "romance_template" in keys
        assert "preorder_template" in keys

    def test_clone_returns_prototype_instance(self):
        cloned = self.cache.clone("action_template")
        assert isinstance(cloned, MangaPrototype)

    def test_clone_is_not_same_object_as_prototype(self):
        original = self.cache.get_prototype("action_template")
        cloned = self.cache.clone("action_template")
        assert cloned is not original

    def test_clone_has_different_id_from_prototype(self):
        original = self.cache.get_prototype("action_template")
        cloned = self.cache.clone("action_template")
        assert cloned.manga_id != original.manga_id

    def test_clone_has_same_genre(self):
        cloned = self.cache.clone("action_template")
        original = self.cache.get_prototype("action_template")
        assert cloned.genre == original.genre

    def test_deep_clone_tags_independence(self):
        deep = self.cache.deep_clone("action_template")
        original = self.cache.get_prototype("action_template")
        deep.add_tag("exclusive")
        assert "exclusive" not in original.tags

    def test_multiple_clones_have_unique_ids(self):
        ids = {self.cache.clone("action_template").manga_id for _ in range(10)}
        assert len(ids) == 10

    def test_register_new_prototype(self):
        custom = MangaPrototype(
            title="Custom Template",
            author="Test Author",
            isbn="000-0-00-999999-9",
            genre=Genre.DRAMA,
            price=Decimal("12.99"),
        )
        self.cache.register("drama_template", custom)
        assert "drama_template" in self.cache.list_keys()

    def test_register_empty_key_raises(self):
        custom = MangaPrototype("T", "A", "ISBN", Genre.COMEDY, Decimal("5.00"))
        with pytest.raises(ValueError, match="empty"):
            self.cache.register("", custom)

    def test_clone_unknown_key_raises(self):
        with pytest.raises(KeyError):
            self.cache.clone("nonexistent_key")

    def test_deep_clone_unknown_key_raises(self):
        with pytest.raises(KeyError):
            self.cache.deep_clone("nonexistent_key")

    def test_unregister_prototype(self):
        self.cache.register(
            "temp",
            MangaPrototype("Temp", "A", "I", Genre.COMEDY, Decimal("5.00")),
        )
        self.cache.unregister("temp")
        assert "temp" not in self.cache.list_keys()

    def test_preorder_template_stock_status(self):
        cloned = self.cache.clone("preorder_template")
        assert cloned.stock_status == StockStatus.PRE_ORDER
