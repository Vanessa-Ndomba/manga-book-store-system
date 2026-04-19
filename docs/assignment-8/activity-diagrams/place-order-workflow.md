# Place Order Workflow Activity Diagram

```mermaid
flowchart TD
    Start([Start]) --> U1

    subgraph Registered_Customer[Registered Customer]
      U1[Confirm place order]
    end

    subgraph System
      S1[Finalize order record]
      F1{{Fork}}
      S2[Update inventory quantities]
      S3[Create shipment request]
      S4[Generate confirmation payload]
      J1{{Join}}
      D1{Inventory update successful?}
      D2{Shipment request successful?}
      S5[Persist order timeline event]
      S6[Trigger compensation and flag order for review]
    end

    subgraph Inventory_DB[Inventory DB]
      I1[Commit stock deduction]
    end

    subgraph Email_Service[Email Service]
      E1[Send confirmation email]
    end

    U1 --> S1 --> F1
    F1 --> S2 --> I1 --> J1
    F1 --> S3 --> J1
    F1 --> S4 --> E1 --> J1
    J1 --> D1
    D1 -- No --> S6 --> End([End])
    D1 -- Yes --> D2
    D2 -- No --> S6 --> End
    D2 -- Yes --> S5 --> End
```

## Explanation
- **Stakeholder concerns:** Customers need quick confirmations; operations need inventory/shipping updates without manual delay.
- **Decisions/parallelism:** Parallel post-order tasks (inventory update, shipment creation, and email) improve speed, while post-join decisions add consistency checks and compensation on failure.
- **Use case and placeholder mapping:** Place Order, Send Confirmation Email, Update Inventory; FR-111, FR-119; US-207; ST-207.
