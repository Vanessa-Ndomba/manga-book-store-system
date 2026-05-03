"""
Prototype Pattern — MangaPrototypeCache

Justification: Certain Manga catalogue entries (e.g. promotional bundles, demo
listings, new-arrival templates) share the same base configuration.  Cloning a
pre-configured prototype is cheaper than re-running full initialisation and
validation for each new entry derived from the same template.
"""
from __future__ import annotations
import copy
import uuid
from decimal import Decimal
from enum import Enum
from typing import Optional


class StockStatus(str, Enum):
    IN_STOCK = "in_stock"
    OUT_OF_STOCK = "out_of_stock"
    PRE_ORDER = "pre_order"


class Genre(str, Enum):
    ACTION = "action"
    ADVENTURE = "adventure"
    COMEDY = "comedy"
    DRAMA = "drama"
    FANTASY = "fantasy"
    ROMANCE = "romance"
    SCI_FI = "sci_fi"
    SLICE_OF_LIFE = "slice_of_life"


class MangaPrototype:
    """
    A cloneable Manga catalogue entry.

    Provides ``clone()`` for shallow copy and ``deep_clone()`` for a fully
    independent copy (used when the genres list must diverge between copies).
    """

    def __init__(
        self,
        title: str,
        author: str,
        isbn: str,
        genre: Genre,
        price: Decimal,
        description: str = "",
        cover_image_url: str = "",
        rating: float = 0.0,
        stock_status: StockStatus = StockStatus.IN_STOCK,
    ):
        self._manga_id: str = str(uuid.uuid4())
        self._title: str = title
        self._author: str = author
        self._isbn: str = isbn
        self._genre: Genre = genre
        self._price: Decimal = price
        self._description: str = description
        self._cover_image_url: str = cover_image_url
        self._rating: float = rating
        self._stock_status: StockStatus = stock_status
        self._tags: list[str] = []

    # ── properties ──────────────────────────────────────────────────────────

    @property
    def manga_id(self) -> str:
        return self._manga_id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value

    @property
    def author(self) -> str:
        return self._author

    @property
    def isbn(self) -> str:
        return self._isbn

    @isbn.setter
    def isbn(self, value: str) -> None:
        self._isbn = value

    @property
    def genre(self) -> Genre:
        return self._genre

    @property
    def price(self) -> Decimal:
        return self._price

    @price.setter
    def price(self, value: Decimal) -> None:
        if value < Decimal("0"):
            raise ValueError("Price cannot be negative")
        self._price = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def stock_status(self) -> StockStatus:
        return self._stock_status

    @stock_status.setter
    def stock_status(self, value: StockStatus) -> None:
        self._stock_status = value

    @property
    def rating(self) -> float:
        return self._rating

    @property
    def tags(self) -> list[str]:
        return list(self._tags)

    def add_tag(self, tag: str) -> None:
        if tag not in self._tags:
            self._tags.append(tag)

    # ── clone methods ────────────────────────────────────────────────────────

    def clone(self) -> "MangaPrototype":
        """Return a shallow copy with a new manga_id."""
        new_obj = copy.copy(self)
        new_obj._manga_id = str(uuid.uuid4())
        return new_obj

    def deep_clone(self) -> "MangaPrototype":
        """Return a deep copy with a new manga_id (independent tags list)."""
        new_obj = copy.deepcopy(self)
        new_obj._manga_id = str(uuid.uuid4())
        return new_obj

    def to_dict(self) -> dict:
        return {
            "manga_id": self._manga_id,
            "title": self._title,
            "author": self._author,
            "isbn": self._isbn,
            "genre": self._genre.value,
            "price": str(self._price),
            "description": self._description,
            "stock_status": self._stock_status.value,
            "rating": self._rating,
            "tags": list(self._tags),
        }

    def __repr__(self) -> str:
        return f"MangaPrototype(id={self._manga_id!r}, title={self._title!r}, price={self._price})"


class MangaPrototypeCache:
    """
    Registry of pre-configured Manga prototypes.

    Usage::

        cache = MangaPrototypeCache()
        cache.register("action_template", MangaPrototype(...))
        new_manga = cache.clone("action_template")
        new_manga.title = "My New Title"
        new_manga.isbn = "978-0-00-000001-1"
    """

    def __init__(self):
        self._prototypes: dict[str, MangaPrototype] = {}
        self._load_defaults()

    def _load_defaults(self) -> None:
        """Pre-load commonly used prototype templates."""
        action_template = MangaPrototype(
            title="[Action Template]",
            author="TBD",
            isbn="000-0-00-000000-0",
            genre=Genre.ACTION,
            price=Decimal("9.99"),
            description="High-octane action manga.",
            stock_status=StockStatus.IN_STOCK,
        )
        action_template.add_tag("action")
        action_template.add_tag("shonen")
        self._prototypes["action_template"] = action_template

        romance_template = MangaPrototype(
            title="[Romance Template]",
            author="TBD",
            isbn="000-0-00-000001-0",
            genre=Genre.ROMANCE,
            price=Decimal("8.99"),
            description="Heartfelt romance manga.",
            stock_status=StockStatus.IN_STOCK,
        )
        romance_template.add_tag("romance")
        romance_template.add_tag("shojo")
        self._prototypes["romance_template"] = romance_template

        preorder_template = MangaPrototype(
            title="[Pre-Order Template]",
            author="TBD",
            isbn="000-0-00-000002-0",
            genre=Genre.FANTASY,
            price=Decimal("11.99"),
            description="Upcoming fantasy manga.",
            stock_status=StockStatus.PRE_ORDER,
        )
        preorder_template.add_tag("pre-order")
        self._prototypes["preorder_template"] = preorder_template

    def register(self, key: str, prototype: MangaPrototype) -> None:
        """Register a new prototype under *key*."""
        if not key or not key.strip():
            raise ValueError("Prototype key must not be empty")
        self._prototypes[key] = prototype

    def clone(self, key: str) -> MangaPrototype:
        """Return a shallow clone of the prototype registered under *key*."""
        if key not in self._prototypes:
            raise KeyError(f"No prototype registered under {key!r}")
        return self._prototypes[key].clone()

    def deep_clone(self, key: str) -> MangaPrototype:
        """Return a deep clone of the prototype registered under *key*."""
        if key not in self._prototypes:
            raise KeyError(f"No prototype registered under {key!r}")
        return self._prototypes[key].deep_clone()

    def get_prototype(self, key: str) -> MangaPrototype:
        """Return the original prototype (not a clone)."""
        if key not in self._prototypes:
            raise KeyError(f"No prototype registered under {key!r}")
        return self._prototypes[key]

    def list_keys(self) -> list[str]:
        """Return all registered prototype keys."""
        return list(self._prototypes.keys())

    def unregister(self, key: str) -> None:
        """Remove a prototype from the cache."""
        self._prototypes.pop(key, None)
