# Manga Listing State Diagram

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> PendingApproval: Submit listing
    PendingApproval --> Active: Approve [metadataValid]
    PendingApproval --> Draft: Reject [missingFields]
    Active --> LowStock: Stock drops [quantity <= reorderThreshold]
    LowStock --> OutOfStock: Sell item [quantity == 0]
    OutOfStock --> Active: Restock [quantity > 0]
    Active --> Archived: Archive listing
    LowStock --> Archived: Archive listing
    OutOfStock --> Archived: Archive listing
    Archived --> Active: Restore [isSellable]
    Archived --> [*]
```

## Explanation
- **Key states/transitions:** Listing moves from `Draft` to `PendingApproval` and becomes `Active` only when validation passes; stock-driven states (`LowStock`, `OutOfStock`) support availability behavior.
- **Use case mapping:** Add New Manga Title, Update Manga Information, Remove Manga Listing, Browse Manga Catalog, View Manga Details.
- **Placeholder traceability:** FR-101 (manage listings), FR-102 (publish validated metadata), FR-103 (reflect stock visibility); US-101; ST-101.
