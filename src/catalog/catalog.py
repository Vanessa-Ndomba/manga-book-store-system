"""Catalog domain model and CatalogService for the Manga Book Store system."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .manga import Genre, Manga


class Catalog:
    """In-memory catalogue of manga listings.

    Provides CRUD operations and basic browsing/search capabilities over
    a collection of :class:`~catalog.manga.Manga` objects.
    """

    def __init__(self) -> None:
        """Initialise an empty catalogue."""
        self._mangas: Dict[str, Manga] = {}

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add_manga(self, manga: Manga) -> None:
        """Add a manga listing to the catalogue.

        Args:
            manga: The Manga instance to add.

        Raises:
            ValueError: If a manga with the same ID already exists.
        """
        if manga.manga_id in self._mangas:
            raise ValueError(f"Manga with ID '{manga.manga_id}' already exists in the catalogue.")
        self._mangas[manga.manga_id] = manga

    def remove_manga(self, manga_id: str) -> None:
        """Remove a manga listing from the catalogue.

        Args:
            manga_id: ID of the manga to remove.

        Raises:
            KeyError: If no manga with the given ID exists.
        """
        if manga_id not in self._mangas:
            raise KeyError(f"Manga with ID '{manga_id}' not found in the catalogue.")
        del self._mangas[manga_id]

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def get_manga(self, manga_id: str) -> Manga:
        """Retrieve a manga by its ID.

        Args:
            manga_id: Unique manga identifier.

        Returns:
            The matching Manga instance.

        Raises:
            KeyError: If no manga with the given ID exists.
        """
        if manga_id not in self._mangas:
            raise KeyError(f"Manga with ID '{manga_id}' not found in the catalogue.")
        return self._mangas[manga_id]

    def get_all(self) -> List[Manga]:
        """Return a list of all manga listings.

        Returns:
            List of all Manga objects in the catalogue.
        """
        return list(self._mangas.values())

    def browse(self, page: int = 1, per_page: int = 20) -> List[Manga]:
        """Return a paginated slice of the catalogue.

        Args:
            page: 1-indexed page number. Defaults to 1.
            per_page: Number of items per page. Defaults to 20.

        Returns:
            List of Manga objects for the requested page.

        Raises:
            ValueError: If page < 1 or per_page < 1.
        """
        if page < 1:
            raise ValueError("page must be >= 1.")
        if per_page < 1:
            raise ValueError("per_page must be >= 1.")
        all_items = self.get_all()
        start = (page - 1) * per_page
        return all_items[start : start + per_page]

    def search(self, query: str) -> List[Manga]:
        """Return all manga whose title, author, or description matches the query.

        Args:
            query: Case-insensitive search string.

        Returns:
            List of matching Manga objects.

        Raises:
            ValueError: If query is empty.
        """
        if not query or not query.strip():
            raise ValueError("Search query must not be empty.")
        return [m for m in self._mangas.values() if m.matches_search(query.strip())]

    def filter_by_genre(self, genre: Genre) -> List[Manga]:
        """Return all manga matching the given genre.

        Args:
            genre: Genre enum value to filter by.

        Returns:
            List of Manga objects with the specified genre.
        """
        return [m for m in self._mangas.values() if m.genre == genre]

    def __len__(self) -> int:
        """Return the total number of listings in the catalogue."""
        return len(self._mangas)


class CatalogService:
    """Service layer wrapping :class:`Catalog` with additional business logic.

    Provides trending/recommended queries and validation helpers in addition
    to the core catalogue operations.
    """

    def __init__(self, catalog: Optional[Catalog] = None) -> None:
        """Initialise the service with an optional Catalog instance.

        Args:
            catalog: Existing Catalog; a new one is created when omitted.
        """
        self._catalog: Catalog = catalog or Catalog()

    # ------------------------------------------------------------------
    # Delegate core CRUD to the underlying Catalog
    # ------------------------------------------------------------------

    def add_manga(self, manga: Manga) -> None:
        """Add a Manga listing via the catalogue.

        Args:
            manga: Manga instance to add.
        """
        self._catalog.add_manga(manga)

    def remove_manga(self, manga_id: str) -> None:
        """Remove a Manga listing via the catalogue.

        Args:
            manga_id: ID of the manga to remove.
        """
        self._catalog.remove_manga(manga_id)

    def get_manga(self, manga_id: str) -> Manga:
        """Retrieve a Manga listing by ID.

        Args:
            manga_id: Unique manga identifier.

        Returns:
            The matching Manga instance.
        """
        return self._catalog.get_manga(manga_id)

    def get_all(self) -> List[Manga]:
        """Return all manga listings.

        Returns:
            List of all Manga objects.
        """
        return self._catalog.get_all()

    def browse(self, page: int = 1, per_page: int = 20) -> List[Manga]:
        """Return a paginated page of the catalogue.

        Args:
            page: 1-indexed page number.
            per_page: Items per page.

        Returns:
            Paginated list of Manga objects.
        """
        return self._catalog.browse(page, per_page)

    def search(self, query: str) -> List[Manga]:
        """Search the catalogue by query string.

        Args:
            query: Case-insensitive search term.

        Returns:
            List of matching Manga objects.
        """
        return self._catalog.search(query)

    def filter_by_genre(self, genre: Genre) -> List[Manga]:
        """Filter the catalogue by genre.

        Args:
            genre: Genre enum value.

        Returns:
            List of matching Manga objects.
        """
        return self._catalog.filter_by_genre(genre)

    # ------------------------------------------------------------------
    # Extended service operations
    # ------------------------------------------------------------------

    def get_trending(self, limit: int = 10) -> List[Manga]:
        """Return the top-rated available manga titles.

        Titles are ranked by rating descending; only available titles
        (IN_STOCK or PRE_ORDER) are included.

        Args:
            limit: Maximum number of results to return. Defaults to 10.

        Returns:
            List of up to *limit* trending Manga objects.
        """
        available = [m for m in self._catalog.get_all() if m.is_available()]
        available.sort(key=lambda m: m.rating, reverse=True)
        return available[:limit]

    def get_recommended(self, user_id: str, limit: int = 10) -> List[Manga]:
        """Return recommended manga for a user.

        Current implementation returns the highest-rated available titles
        as a simple recommendation strategy. Future enhancements could use
        purchase history keyed on ``user_id``.

        Args:
            user_id: ID of the user requesting recommendations.
            limit: Maximum number of results. Defaults to 10.

        Returns:
            List of recommended Manga objects.
        """
        return self.get_trending(limit=limit)

    def validate_manga_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate a dictionary of manga field data before creating a listing.

        Args:
            data: Dictionary potentially containing manga fields.

        Returns:
            List of error message strings; empty when data is valid.
        """
        errors: List[str] = []
        required = ["title", "author", "isbn", "genre", "price"]
        for field in required:
            if field not in data or not str(data[field]).strip():
                errors.append(f"'{field}' is required and must not be empty.")

        if "price" in data:
            try:
                if float(data["price"]) < 0:
                    errors.append("'price' must be non-negative.")
            except (TypeError, ValueError):
                errors.append("'price' must be a valid number.")

        if "rating" in data:
            try:
                rating = float(data["rating"])
                if not (0.0 <= rating <= 5.0):
                    errors.append("'rating' must be between 0.0 and 5.0.")
            except (TypeError, ValueError):
                errors.append("'rating' must be a valid number.")

        return errors
