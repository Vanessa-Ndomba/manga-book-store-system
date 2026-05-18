from __future__ import annotations

from typing import Dict, List, Optional

from repositories.user_repository import UserRepository
from src.users import User


class InMemoryUserRepository(UserRepository):
    """
    HashMap/dict-backed repository for User.
    """

    def __init__(self) -> None:
        self._storage: Dict[str, User] = {}

    def save(self, entity: User) -> None:
        self._storage[entity.user_id] = entity

    def find_by_id(self, id: str) -> Optional[User]:
        return self._storage.get(id)

    def find_all(self) -> List[User]:
        return list(self._storage.values())

    def delete(self, id: str) -> None:
        self._storage.pop(id, None)
