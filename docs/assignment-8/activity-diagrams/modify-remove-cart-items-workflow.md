# Modify/Remove Cart Items Workflow Activity Diagram

```mermaid
flowchart TD
    Start([Start]) --> U1

    subgraph Registered_Customer[Registered Customer]
      U1[Open shopping cart]
      U2[Change quantity or remove item]
      U3[Submit cart update]
    end

    subgraph System
      D1{Action type?}
      S1[Validate requested quantity]
      D2{Quantity valid and in stock?}
      F1{{Fork}}
      S2[Update cart line item]
      S3[Recompute totals]
      J1{{Join}}
      S4[Remove selected item]
      D3{Cart empty?}
      S5[Set cart state to Empty]
      S6[Show validation error]
    end

    subgraph Inventory_DB[Inventory DB]
      I1[Revalidate stock]
    end

    U1 --> U2 --> U3 --> D1
    D1 -- Modify --> S1 --> I1 --> D2
    D2 -- No --> S6 --> U2
    D2 -- Yes --> F1
    F1 --> S2 --> J1
    F1 --> S3 --> J1
    J1 --> End([End])
    D1 -- Remove --> S4 --> D3
    D3 -- Yes --> S5 --> End
    D3 -- No --> End
```

## Explanation
- **Stakeholder concerns:** Cart edits must remain accurate while keeping customer friction low.
- **Decisions/parallelism:** Decision branches distinguish modify vs remove paths; update and total recomputation run concurrently.
- **Use case and placeholder mapping:** Modify Cart Quantity, Remove Items from Cart, Validate Stock Availability; FR-107, FR-108; US-205; ST-205.
