"""ReportService and related models for the Manga Book Store system."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from ..adapters.inventory_repository import InventoryRepository
    from ..orders.order_service import OrderService


class ReportType(Enum):
    """Enumeration of supported report types."""

    SALES = "sales"
    INVENTORY = "inventory"
    USER_ACTIVITY = "user_activity"


class Report:
    """Represents a generated business report.

    Attributes:
        _report_id: Unique identifier for the report.
        _report_type: The type of report (ReportType enum).
        _generated_at: UTC timestamp of report generation.
        _data: Raw data payload as a dictionary.
        _summary: Human-readable summary string.
    """

    def __init__(
        self,
        report_type: ReportType,
        data: Dict[str, Any],
        summary: str,
        report_id: Optional[str] = None,
        generated_at: Optional[datetime] = None,
    ) -> None:
        """Initialise a Report.

        Args:
            report_type: Type of this report.
            data: Dictionary containing report data.
            summary: Short human-readable summary.
            report_id: Optional explicit UUID.
            generated_at: Optional explicit generation timestamp.
        """
        self._report_id: str = report_id or str(uuid.uuid4())
        self._report_type: ReportType = report_type
        self._generated_at: datetime = generated_at or datetime.now(timezone.utc)
        self._data: Dict[str, Any] = data
        self._summary: str = summary

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def report_id(self) -> str:
        """Unique report identifier."""
        return self._report_id

    @property
    def report_type(self) -> ReportType:
        """The type of report."""
        return self._report_type

    @property
    def generated_at(self) -> datetime:
        """UTC timestamp of report generation."""
        return self._generated_at

    @property
    def data(self) -> Dict[str, Any]:
        """Raw data payload."""
        return self._data

    @property
    def summary(self) -> str:
        """Human-readable summary."""
        return self._summary

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the report to a plain dictionary.

        Returns:
            Dictionary containing all field values.
        """
        return {
            "report_id": self._report_id,
            "report_type": self._report_type.value,
            "generated_at": self._generated_at.isoformat(),
            "summary": self._summary,
            "data": self._data,
        }

    def __repr__(self) -> str:
        return (
            f"Report("
            f"report_id={self._report_id!r}, "
            f"report_type={self._report_type.value!r}, "
            f"generated_at={self._generated_at.isoformat()!r})"
        )


class ReportService:
    """Generates and stores business reports.

    Attributes:
        _order_service: OrderService used for sales data.
        _inventory_repo: InventoryRepository used for stock data.
        _reports: Mapping of report_id → Report.
    """

    def __init__(
        self,
        order_service: "OrderService",
        inventory_repo: "InventoryRepository",
    ) -> None:
        """Initialise the ReportService.

        Args:
            order_service: Provides order data for sales reports.
            inventory_repo: Provides stock data for inventory reports.
        """
        self._order_service = order_service
        self._inventory_repo = inventory_repo
        self._reports: Dict[str, Report] = {}

    # ------------------------------------------------------------------
    # Report generation
    # ------------------------------------------------------------------

    def generate_sales_report(
        self,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ) -> Report:
        """Generate a sales report, optionally filtered by date range.

        Args:
            date_from: Optional start of the date range.
            date_to: Optional end of the date range.

        Returns:
            A Report of type SALES stored in the service.
        """
        all_orders = self._order_service.get_all_orders()

        if date_from:
            all_orders = [o for o in all_orders if o.order_date >= date_from]
        if date_to:
            all_orders = [o for o in all_orders if o.order_date <= date_to]

        total_revenue = sum(o.total_amount for o in all_orders)
        order_count = len(all_orders)

        data: Dict[str, Any] = {
            "total_orders": order_count,
            "total_revenue": round(total_revenue, 2),
            "date_from": date_from.isoformat() if date_from else None,
            "date_to": date_to.isoformat() if date_to else None,
            "orders": [o.to_dict() for o in all_orders],
        }
        summary = (
            f"Sales report: {order_count} orders, "
            f"total revenue £{total_revenue:.2f}."
        )
        report = Report(report_type=ReportType.SALES, data=data, summary=summary)
        self._reports[report.report_id] = report
        return report

    def generate_inventory_report(self) -> Report:
        """Generate a snapshot report of current stock levels.

        Returns:
            A Report of type INVENTORY stored in the service.
        """
        stock_data = self._inventory_repo.get_all_stock() if hasattr(
            self._inventory_repo, "get_all_stock"
        ) else {}

        total_skus = len(stock_data)
        out_of_stock = sum(1 for qty in stock_data.values() if qty == 0)

        data: Dict[str, Any] = {
            "total_skus": total_skus,
            "out_of_stock_count": out_of_stock,
            "stock_levels": stock_data,
        }
        summary = (
            f"Inventory report: {total_skus} SKUs tracked, "
            f"{out_of_stock} out of stock."
        )
        report = Report(report_type=ReportType.INVENTORY, data=data, summary=summary)
        self._reports[report.report_id] = report
        return report

    def generate_user_activity_report(self) -> Report:
        """Generate a user-activity summary report.

        Current implementation reports aggregate order activity as a proxy
        for user activity.

        Returns:
            A Report of type USER_ACTIVITY stored in the service.
        """
        all_orders = self._order_service.get_all_orders()
        unique_users = {o.user_id for o in all_orders}

        data: Dict[str, Any] = {
            "unique_customers_with_orders": len(unique_users),
            "total_orders_placed": len(all_orders),
        }
        summary = (
            f"User activity report: {len(unique_users)} customers placed "
            f"{len(all_orders)} orders in total."
        )
        report = Report(report_type=ReportType.USER_ACTIVITY, data=data, summary=summary)
        self._reports[report.report_id] = report
        return report

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def get_report(self, report_id: str) -> Report:
        """Retrieve a previously generated report by its ID.

        Args:
            report_id: Unique report identifier.

        Returns:
            The matching Report.

        Raises:
            KeyError: If no report with the given ID exists.
        """
        if report_id not in self._reports:
            raise KeyError(f"Report '{report_id}' not found.")
        return self._reports[report_id]

    def get_all_reports(self) -> List[Report]:
        """Return all stored reports.

        Returns:
            List of all Report objects.
        """
        return list(self._reports.values())
