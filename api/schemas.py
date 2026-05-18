from pydantic import BaseModel, Field
from typing import List, Optional


# -------------------------
# Manga
# -------------------------
class MangaCreate(BaseModel):
    isbn: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    price: float = Field(..., ge=0)


class MangaUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1)
    price: Optional[float] = Field(None, ge=0)


class MangaOut(BaseModel):
    isbn: str
    title: str
    author: str
    price: float


# -------------------------
# Users (matches src/users.py)
# -------------------------
class UserCreate(BaseModel):
    user_id: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    display_name: str = Field(..., min_length=1)


class UserOut(BaseModel):
    user_id: str
    email: str
    display_name: str
    active: bool


# -------------------------
# Orders (matches src/orders.py)
# -------------------------
class OrderItemCreate(BaseModel):
    isbn: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1)


class OrderCreate(BaseModel):
    order_id: str = Field(..., min_length=1)
    customer_id: str = Field(..., min_length=1)
    shipping_address: str = Field(..., min_length=1)
    items: List[OrderItemCreate] = Field(..., min_length=1)


class OrderItemOut(BaseModel):
    isbn: str
    title: str
    unit_price: float
    quantity: int


class OrderOut(BaseModel):
    order_id: str
    customer_id: str
    shipping_address: str
    items: List[OrderItemOut]
    status: str
    payment_transaction_id: Optional[str] = None
    total: float