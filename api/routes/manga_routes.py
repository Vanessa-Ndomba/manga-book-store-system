from fastapi import APIRouter, HTTPException
from typing import List

from api.schemas import MangaCreate, MangaUpdate, MangaOut
from factories.repository_factory import RepositoryFactory
from services.manga_service import MangaService
from services.exceptions import AlreadyExistsError, NotFoundError, BusinessRuleError

from src.catalog import Manga  # uses your domain model


router = APIRouter()

manga_repo = RepositoryFactory.get_manga_repository("MEMORY")
manga_service = MangaService(manga_repo)


def to_manga_out(m: Manga) -> MangaOut:
    return MangaOut(isbn=m.isbn, title=m.title, author=m.author, price=m.price)


@router.get("/manga", response_model=List[MangaOut], summary="List Manga")
def list_manga():
    return [to_manga_out(m) for m in manga_service.list_manga()]


@router.post("/manga", response_model=MangaOut, status_code=201, summary="Create Manga")
def create_manga(payload: MangaCreate):
    try:
        manga = Manga(isbn=payload.isbn, title=payload.title, author=payload.author, price=payload.price)
        created = manga_service.create_manga(manga)
        return to_manga_out(created)
    except AlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BusinessRuleError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/manga/{isbn}", response_model=MangaOut, summary="Get Manga by ISBN")
def get_manga(isbn: str):
    try:
        manga = manga_service.get_manga(isbn)
        return to_manga_out(manga)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/manga/{isbn}", response_model=MangaOut, summary="Update Manga")
def update_manga(isbn: str, payload: MangaUpdate):
    try:
        updated = manga_service.update_manga(isbn, title=payload.title, author=payload.author, price=payload.price)
        return to_manga_out(updated)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BusinessRuleError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/manga/{isbn}", status_code=204, summary="Delete Manga")
def delete_manga(isbn: str):
    try:
        manga_service.delete_manga(isbn)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))