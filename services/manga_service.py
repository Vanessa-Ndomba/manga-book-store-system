from services.exceptions import AlreadyExistsError, NotFoundError, BusinessRuleError


class MangaService:
    def __init__(self, manga_repo):
        self.manga_repo = manga_repo

    def list_manga(self):
        return self.manga_repo.find_all()

    def get_manga(self, isbn: str):
        manga = self.manga_repo.find_by_id(isbn)
        if manga is None:
            raise NotFoundError(f"Manga with ISBN '{isbn}' not found")
        return manga

    def create_manga(self, manga):
        if manga.price < 0:
            raise BusinessRuleError("Price must be >= 0")

        existing = self.manga_repo.find_by_id(manga.isbn)
        if existing is not None:
            raise AlreadyExistsError(f"Manga with ISBN '{manga.isbn}' already exists")

        self.manga_repo.save(manga)
        return manga

    def update_manga(self, isbn: str, title=None, author=None, price=None):
        manga = self.get_manga(isbn)

        if price is not None and price < 0:
            raise BusinessRuleError("Price must be >= 0")

        # Since Manga is a frozen dataclass, we create a new instance with updated values
        from src.catalog import Manga
        updated_manga = Manga(
            isbn=manga.isbn,
            title=title if title is not None else manga.title,
            author=author if author is not None else manga.author,
            price=price if price is not None else manga.price,
            genres=manga.genres
        )

        self.manga_repo.save(updated_manga)
        return updated_manga

    def delete_manga(self, isbn: str):
        # ensure exists first (so we can return 404)
        self.get_manga(isbn)
        self.manga_repo.delete(isbn)