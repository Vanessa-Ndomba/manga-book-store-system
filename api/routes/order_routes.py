from fastapi import APIRouter, HTTPException
from typing import List

from api.schemas import OrderCreate, OrderOut, OrderItemOut
from factories.repository_factory import RepositoryFactory
from services.order_service import OrderService
from services.exceptions import NotFoundError, BusinessRuleError

from api.routes.user_routes import user_repo  # shared user repo

from src.orders import Order, OrderItem

router = APIRouter()

order_repo = RepositoryFactory.get_order_repository("MEMORY")
manga_repo = RepositoryFactory.get_manga_repository("MEMORY")
order_service = OrderService(order_repo, user_repo, manga_repo)


def to_order_out(o: Order) -> OrderOut:
    items_out = [
        OrderItemOut(isbn=i.isbn, title=i.title, unit_price=i.unit_price, quantity=i.quantity)
        for i in o.items
    ]
    return OrderOut(
        order_id=o.order_id,
        customer_id=o.customer_id,
        shipping_address=o.shipping_address,
        items=items_out,
        status=o.status.value if hasattr(o.status, 'value') else str(o.status),
        payment_transaction_id=o.payment_transaction_id,
        total=o.total(),
    )


@router.get("/orders", response_model=List[OrderOut], summary="List Orders")
def list_orders():
    return [to_order_out(o) for o in order_service.list_orders()]


@router.post("/orders", response_model=OrderOut, status_code=201, summary="Create Order")
def create_order(payload: OrderCreate):
    try:
        # Build order items by looking up manga for title/price
        items = []
        for it in payload.items:
            manga = manga_repo.find_by_id(it.isbn)
            if manga is None:
                raise BusinessRuleError(f"Cannot create order: manga '{it.isbn}' not found")

            items.append(
                OrderItem(
                    isbn=manga.isbn,
                    title=manga.title,
                    unit_price=manga.price,
                    quantity=it.quantity,
                )
            )

        order = Order(
            order_id=payload.order_id,
            customer_id=payload.customer_id,
            shipping_address=payload.shipping_address,
            items=items,
        )

        created = order_service.create_order(order)
        return to_order_out(created)

    except BusinessRuleError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/orders/{order_id}", response_model=OrderOut, summary="Get Order by ID")
def get_order(order_id: str):
    try:
        o = order_service.get_order(order_id)
        return to_order_out(o)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/orders/{order_id}/checkout", response_model=OrderOut, summary="Checkout Order")
def checkout_order(order_id: str):
    try:
        o = order_service.checkout_order(order_id)
        return to_order_out(o)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BusinessRuleError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/orders/{order_id}", status_code=204, summary="Delete Order")
def delete_order(order_id: str):
    try:
        order_service.delete_order(order_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))