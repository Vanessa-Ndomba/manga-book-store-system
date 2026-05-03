"""Manga domain model: Manga (MangaListing), StockStatus enum, and Genre enum."""

from __future__ import annotations

import uuid
from enum import Enum
from typing import Any, Dict, Optional


class StockStatus(Enum):
    """Availability status of a manga title."""

    IN_STOCK = "in_stock"
    OUT_OF_STOCK = "out_of_stock"
    PRE_ORDER = "pre_order"


class Genre(Enum):
    """Genre classification for manga titles."""

    ACTION = "action"
    ADVENTURE = "adventure"
    COMEDY = "comedy"
    DRAMA = "drama"
    FANTASY = "fantasy"
    HORROR = "horror"
    MYSTERY = "mystery"
    ROMANCE = "romance"
    SCI_FI = "sci_fi"
    SLICE_OF_LIFE = "slice_of_life"
    SPORTS = "sports"
    SUPERNATURAL = "supernatural"


class Manga:
    """Represents a manga title listed in the store (MangaListing in the domain model).

    Attributes:
        _manga_id: Unique identifier for this listing.
        _title: Title of the manga.
        _author: Author/artist name.
        _isbn: ISBN-13 identifier.
        _genre: Genre classification (Genre enum).
        _description: Short synopsis.
        _cover_image_url: URL pointing to the cover image.
        _rating: Aggregate customer rating (0.0–5.0).
        _price: Retail price.
        _stock_quantity: Number of units currently in stock.
        _stock_status: Computed or explicitly set stock status.
    """

    def __init__(
        self,
        title: str,
        author: str,
        isbn: str,
        genre: Genre,
        price: float,
        description: str = "",
        cover_image_url: str = "",
        rating: float = 0.0,
        stock_quantity: int = 0,
        stock_status: Optional[StockStatus] = None,
        manga_id: Optional[str] = None,
    ) -> None:
        """Initialise a Manga listing.

        Args:
            title: Manga title.
            author: Author/artist name.
            isbn: ISBN-13 string.
            genre: Genre enum value.
            price: Retail price (must be >= 0).
            description: Optional synopsis.
            cover_image_url: Optional cover image URL.
            rating: Optional aggregate rating (0.0–5.0).
            stock_quantity: Units in stock (must be >= 0).
            stock_status: Explicit stock status; auto-derived when omitted.
            manga_id: Optional explicit UUID.

        Raises:
            ValueError: If title, author, or isbn is empty; price < 0; stock_quantity < 0;
                        or rating is outside 0–5.
        """
        if not title or not title.strip():
            raise ValueError("title must not be empty.")
        if not author or not author.strip():
            raise ValueError("author must not be empty.")
        if not isbn or not isbn.strip():
            raise ValueError("isbn must not be empty.")
        if price < 0:
            raise ValueError("price must be non-negative.")
        if stock_quantity < 0:
            raise ValueError("stock_quantity must be non-negative.")
        if not (0.0 <= rating <= 5.0):
            raise ValueError("rating must be between 0.0 and 5.0.")

        self._manga_id: str = manga_id or str(uuid.uuid4())
        self._title: str = title.strip()
        self._author: str = author.strip()
        self._isbn: str = isbn.strip()
        self._genre: Genre = genre
        self._description: str = description
        self._cover_image_url: str = cover_image_url
        self._rating: float = rating
        self._price: float = price
        self._stock_quantity: int = stock_quantity
        self._stock_status: StockStatus = stock_status or self._derive_stock_status()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _derive_stock_status(self) -> StockStatus:
        """Derive StockStatus from the current stock quantity."""
        if self._stock_quantity > 0:
            return StockStatus.IN_STOCK
        return StockStatus.OUT_OF_STOCK

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def manga_id(self) -> str:
        """Unique manga identifier."""
        return self._manga_id

    @property
    def title(self) -> str:
        """Manga title."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """Set a new title.

        Raises:
            ValueError: If value is blank.
        """
        if not value or not value.strip():
            raise ValueError("title must not be empty.")
        self._title = value.strip()

    @property
    def author(self) -> str:
        """Author/artist name."""
        return self._author

    @author.setter
    def author(self, value: str) -> None:
        """Set a new author name.

        Raises:
            ValueError: If value is blank.
        """
        if not value or not value.strip():
            raise ValueError("author must not be empty.")
        self._author = value.strip()

    @property
    def isbn(self) -> str:
        """ISBN-13 identifier."""
        return self._isbn

    @property
    def genre(self) -> Genre:
        """Genre classification."""
        return self._genre

    @genre.setter
    def genre(self, value: Genre) -> None:
        """Set a new genre."""
        self._genre = value

    @property
    def description(self) -> str:
        """Short synopsis of the manga."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Set a new description."""
        self._description = value

    @property
    def cover_image_url(self) -> str:
        """URL of the cover image."""
        return self._cover_image_url

    @cover_image_url.setter
    def cover_image_url(self, value: str) -> None:
        """Set a new cover image URL."""
        self._cover_image_url = value

    @property
    def rating(self) -> float:
        """Aggregate customer rating (0.0–5.0)."""
        return self._rating

    @rating.setter
    def rating(self, value: float) -> None:
        """Update the rating.

        Raises:
            ValueError: If value is outside 0–5.
        """
        if not (0.0 <= value <= 5.0):
            raise ValueError("rating must be between 0.0 and 5.0.")
        self._rating = value

    @property
    def price(self) -> float:
        """Retail price."""
        return self._price

    @property
    def stock_quantity(self) -> int:
        """Current number of units in stock."""
        return self._stock_quantity

    @stock_quantity.setter
    def stock_quantity(self, value: int) -> None:
        """Update the stock quantity and refresh the stock status.

        Raises:
            ValueError: If value is negative.
        """
        if value < 0:
            raise ValueError("stock_quantity must be non-negative.")
        self._stock_quantity = value
        self._stock_status = self._derive_stock_status()

    @property
    def stock_status(self) -> StockStatus:
        """Current stock availability status."""
        return self._stock_status

    @stock_status.setter
    def stock_status(self, value: StockStatus) -> None:
        """Explicitly override the stock status."""
        self._stock_status = value

    # ------------------------------------------------------------------
    # Behaviour
    # ------------------------------------------------------------------

    def update_details(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        """Update editable details for this listing.

        Args:
            title: New title if provided.
            author: New author name if provided.
            description: New description if provided.

        Raises:
            ValueError: If a provided title or author is blank.
        """
        if title is not None:
            self.title = title
        if author is not None:
            self.author = author
        if description is not None:
            self._description = description

    def update_price(self, price: float) -> None:
        """Set a new retail price.

        Args:
            price: New price (must be >= 0).

        Raises:
            ValueError: If price is negative.
        """
        if price < 0:
            raise ValueError("price must be non-negative.")
        self._price = price

    def matches_search(self, query: str) -> bool:
        """Return True if the query appears in the title, author, or description.

        Args:
            query: Case-insensitive search string.

        Returns:
            True when a match is found in any searchable field.
        """
        q = query.lower()
        return (
            q in self._title.lower()
            or q in self._author.lower()
            or q in self._description.lower()
            or q in self._isbn.lower()
        )

    def is_available(self) -> bool:
        """Return True if the title is available for purchase (IN_STOCK or PRE_ORDER)."""
        return self._stock_status in (StockStatus.IN_STOCK, StockStatus.PRE_ORDER)

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the manga listing to a plain dictionary.

        Returns:
            Dictionary containing all public fields.
        """
        return {
            "manga_id": self._manga_id,
            "title": self._title,
            "author": self._author,
            "isbn": self._isbn,
            "genre": self._genre.value,
            "description": self._description,
            "cover_image_url": self._cover_image_url,
            "rating": self._rating,
            "price": self._price,
            "stock_quantity": self._stock_quantity,
            "stock_status": self._stock_status.value,
        }

    def __repr__(self) -> str:
        return (
            f"Manga("
            f"manga_id={self._manga_id!r}, "
            f"title={self._title!r}, "
            f"author={self._author!r}, "
            f"price={self._price!r}, "
            f"stock_status={self._stock_status.value!r})"
        )
