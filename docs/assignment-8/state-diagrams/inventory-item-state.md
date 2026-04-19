# Inventory Item State Diagram

```mermaid
stateDiagram-v2
    [*] --> InStock
    InStock --> Reserved: Reserve quantity [requestedQty <= availableQty]
    Reserved --> InStock: Reservation released
    Reserved --> Allocated: Confirm order
    Allocated --> InStock: Restock return [isSellable]
    InStock --> LowStock: Quantity drop [availableQty <= reorderPoint]
    LowStock --> OutOfStock: Sell final unit [availableQty == 0]
    OutOfStock --> ReplenishmentPending: Raise purchase request
    ReplenishmentPending --> InStock: Supplier delivery received
    OutOfStock --> Discontinued: Mark title discontinued
    InStock --> Discontinued: Mark title discontinued
    Discontinued --> [*]
```

## Explanation
- **Key states/transitions:** Reservation/allocation and replenishment states maintain stock integrity during checkout and admin updates.
- **Use case mapping:** Validate Stock Availability, Update Inventory, View Inventory Levels, Add Items to Shopping Cart.
- **Placeholder traceability:** FR-118 (reserve inventory), FR-119 (replenish stock), FR-120 (discontinue item); US-107; ST-107.
