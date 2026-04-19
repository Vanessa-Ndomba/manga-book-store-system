# Add to Cart + Validate Stock Workflow Activity Diagram

```mermaid
flowchart TD
    Start([Start]) --> U1

    subgraph Registered_Customer[Registered Customer]
      U1[Open manga details]
      U2[Choose quantity]
      U3[Click Add to Cart]
    end

    subgraph System
      S1[Check cart state]
      S2[Request stock validation]
      D1{Stock available?}
      F1{{Fork}}
      S3[Add or merge cart line]
      S4[Recalculate cart totals]
      J1{{Join}}
      S5[Show out-of-stock message]
    end

    subgraph Inventory_DB[Inventory DB]
      I1[Validate available quantity]
    end

    U1 --> U2 --> U3 --> S1 --> S2 --> I1 --> D1
    D1 -- No --> S5 --> End([End])
    D1 -- Yes --> F1
    F1 --> S3 --> J1
    F1 --> S4 --> J1
    J1 --> End
```

## Explanation
- **Stakeholder concerns:** Customers need immediate feedback; operations require preventing overselling.
- **Decisions/parallelism:** Stock decision ensures guardrails; cart-line update and total recalculation execute in parallel for speed.
- **Use case and placeholder mapping:** Add Items to Shopping Cart, Validate Stock Availability; FR-107, FR-118; US-204; ST-204.
