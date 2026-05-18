from fastapi import APIRouter, HTTPException
from typing import List

from api.schemas import UserCreate, UserOut
from services.user_service import UserService
from services.exceptions import AlreadyExistsError, NotFoundError

from src.users import User  # <-- your dataclass

router = APIRouter()


class InMemoryUserRepo:
    def __init__(self):
        self._storage = {}

    def save(self, entity: User):
        self._storage[entity.user_id] = entity

    def find_by_id(self, user_id: str):
        return self._storage.get(user_id)

    def find_all(self):
        return list(self._storage.values())

    def delete(self, user_id: str):
        self._storage.pop(user_id, None)


# shared instance (Orders will import this)
user_repo = InMemoryUserRepo()
user_service = UserService(user_repo)


@router.get("/users", response_model=List[UserOut], summary="List Users")
def list_users():
    users = user_service.list_users()
    return [
        UserOut(
            user_id=u.user_id,
            email=u.email,
            display_name=u.display_name,
            active=u.active,
        )
        for u in users
    ]


@router.post("/users", response_model=UserOut, status_code=201, summary="Create User")
def create_user(payload: UserCreate):
    try:
        user = User(
            user_id=payload.user_id,
            email=payload.email,
            display_name=payload.display_name,
        )
        created = user_service.create_user(user)
        return UserOut(
            user_id=created.user_id,
            email=created.email,
            display_name=created.display_name,
            active=created.active,
        )
    except AlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/users/{user_id}", response_model=UserOut, summary="Get User by ID")
def get_user(user_id: str):
    try:
        u = user_service.get_user(user_id)
        return UserOut(
            user_id=u.user_id,
            email=u.email,
            display_name=u.display_name,
            active=u.active,
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/users/{user_id}", status_code=204, summary="Delete User")
def delete_user(user_id: str):
    try:
        user_service.delete_user(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))