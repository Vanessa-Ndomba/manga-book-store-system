# Assignment 8 Traceability

> Note: Assignment 4 functional requirements are not available in-repo. The FR/US/ST identifiers below are **placeholders** derived from the provided use case model and should be aligned to official course artifacts.

## Placeholder requirement key
- FR-101..FR-124: Functional requirements inferred from use cases
- US-101..US-208: User stories inferred from actor goals
- ST-101..ST-208: Sprint tasks inferred from implementation work items

## A) Object State Diagram Traceability

| Diagram | Primary Use Cases (Provided) | Placeholder FR | Placeholder US/ST |
|---|---|---|---|
| `state-diagrams/manga-listing-state.md` | Add New Manga Title; Update Manga Information; Remove Manga Listing; Browse Manga Catalog; View Manga Details | FR-101, FR-102, FR-103 | US-101 / ST-101 |
| `state-diagrams/user-account-state.md` | Register Account; Login/Authentication; Manage User Accounts; Manage User Profile | FR-104, FR-105, FR-106 | US-102 / ST-102 |
| `state-diagrams/shopping-cart-state.md` | Add Items to Shopping Cart; Modify Cart Quantity; Remove Items from Cart; Checkout Process; Place Order | FR-107, FR-108, FR-109 | US-103 / ST-103 |
| `state-diagrams/order-state.md` | Checkout Process; Place Order; Track Order Status; View All Customer Orders; Update Order Status | FR-110, FR-111, FR-112 | US-104 / ST-104 |
| `state-diagrams/payment-state.md` | Process Payment; Checkout Process; Place Order | FR-113, FR-114, FR-115 | US-105 / ST-105 |
| `state-diagrams/shipment-fulfillment-state.md` | Track Order Status; Update Order Status; View All Customer Orders | FR-116, FR-117 | US-106 / ST-106 |
| `state-diagrams/inventory-item-state.md` | Validate Stock Availability; Update Inventory; View Inventory Levels; Add Items to Shopping Cart | FR-118, FR-119, FR-120 | US-107 / ST-107 |
| `state-diagrams/admin-report-state.md` | Generate Sales Reports; View Inventory Levels | FR-121, FR-122 | US-108 / ST-108 |

## B) Activity Workflow Traceability

| Diagram | Primary Use Cases (Provided) | Placeholder FR | Placeholder US/ST |
|---|---|---|---|
| `activity-diagrams/user-registration-workflow.md` | Register Account | FR-104, FR-105 | US-201 / ST-201 |
| `activity-diagrams/login-authentication-workflow.md` | Login/Authentication | FR-105, FR-106 | US-202 / ST-202 |
| `activity-diagrams/browse-search-filter-view-workflow.md` | Browse Manga Catalog; Search Manga by Title/Author/ISBN; Filter by Genre/Category; View Manga Details | FR-123, FR-124 | US-203 / ST-203 |
| `activity-diagrams/add-to-cart-validate-stock-workflow.md` | Add Items to Shopping Cart; Validate Stock Availability | FR-107, FR-118 | US-204 / ST-204 |
| `activity-diagrams/modify-remove-cart-items-workflow.md` | Modify Cart Quantity; Remove Items from Cart; Validate Stock Availability | FR-107, FR-108 | US-205 / ST-205 |
| `activity-diagrams/checkout-process-workflow.md` | Checkout Process; Process Payment; Validate Stock Availability | FR-110, FR-113, FR-118 | US-206 / ST-206 |
| `activity-diagrams/place-order-workflow.md` | Place Order; Send Confirmation Email; Update Inventory | FR-111, FR-119 | US-207 / ST-207 |
| `activity-diagrams/admin-order-fulfillment-workflow.md` | Update Order Status; View All Customer Orders; Track Order Status | FR-117, FR-121 | US-208 / ST-208 |
