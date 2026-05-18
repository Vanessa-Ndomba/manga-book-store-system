from __future__ import annotations

from typing import Protocol

from repositories.base import Repository
from src.users import User


class UserRepository(Repository[User, str], Protocol):
    """
    Entity-specific repository interface for User.
    ID is user_id (str).
    """
    pass
