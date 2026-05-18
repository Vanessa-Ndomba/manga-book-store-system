from services.exceptions import BusinessRuleError, NotFoundError
from src.orders import OrderStatus


class OrderService:
    def __init__(self, order_repo, user_repo, manga_repo):
        self.order_repo = order_repo
        self.user_repo = user_repo
        self.manga_repo = manga_repo

    def list_orders(self):
        return self.order_repo.find_all()

    def get_order(self, order_id: str):
        order = self.order_repo.find_by_id(order_id)
        if order is None:
            raise NotFoundError(f"Order '{order_id}' not found")
        return order

    def create_order(self, order):
        # items required
        if not getattr(order, "items", None):
            raise BusinessRuleError("Order must contain at least 1 item")

        # validate customer exists
        customer = self.user_repo.find_by_id(order.customer_id)
        if customer is None:
            raise BusinessRuleError(f"Cannot create order: user '{order.customer_id}' not found")

        # status should start CREATED
        if getattr(order, "status", None) not in (None, OrderStatus.CREATED):
            raise BusinessRuleError("New order must start in CREATED status")

        self.order_repo.save(order)
        return order

    def checkout_order(self, order_id: str):
        order = self.get_order(order_id)

        if order.status == OrderStatus.CHECKED_OUT:
            raise BusinessRuleError("Order is already checked out")

        # you can decide your workflow; for assignment we allow direct checkout
        order.status = OrderStatus.CHECKED_OUT
        self.order_repo.save(order)
        return order

    def delete_order(self, order_id: str):
        self.get_order(order_id)
        self.order_repo.delete(order_id)