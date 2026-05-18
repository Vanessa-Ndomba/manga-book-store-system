import pytest

from services.user_service import UserService
from services.exceptions import AlreadyExistsError, NotFoundError
from src.users import User


class FakeUserRepo:
    def __init__(self):
        self.storage = {}

    def save(self, entity: User):
        self.storage[entity.user_id] = entity

    def find_by_id(self, user_id: str):
        return self.storage.get(user_id)

    def find_all(self):
        return list(self.storage.values())

    def delete(self, user_id: str):
        self.storage.pop(user_id, None)


def test_create_user_success():
    repo = FakeUserRepo()
    service = UserService(repo)

    u = User(user_id="u100", email="u100@example.com", display_name="Vanessa")
    created = service.create_user(u)

    assert created.user_id == "u100"
    assert repo.find_by_id("u100") is not None


def test_create_user_duplicate_raises():
    repo = FakeUserRepo()
    service = UserService(repo)

    u = User(user_id="u101", email="u101@example.com", display_name="Vanessa")
    service.create_user(u)

    with pytest.raises(AlreadyExistsError):
        service.create_user(u)


def test_get_user_missing_raises():
    repo = FakeUserRepo()
    service = UserService(repo)

    with pytest.raises(NotFoundError):
        service.get_user("does-not-exist")