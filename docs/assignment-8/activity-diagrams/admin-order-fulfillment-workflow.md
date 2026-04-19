# Admin Update Order Status / Fulfillment Workflow Activity Diagram

```mermaid
flowchart TD
    Start([Start]) --> A1

    subgraph Admin
      A1[Open order management dashboard]
      A2[Select order]
      A3[Choose new status]
      A4[Submit status update]
    end

    subgraph System
      S1[Validate status transition]
      D1{Transition allowed?}
      F1{{Fork}}
      S2[Update order status]
      S3[Record audit trail]
      J1{{Join}}
      D2{Status = Shipped or Delivered?}
      F2{{Fork}}
      S4[Notify customer]
      S5[Refresh reporting metrics]
      J2{{Join}}
      S6[Show transition error]
    end

    subgraph Email_Service[Email Service]
      E1[Send status notification]
    end

    A1 --> A2 --> A3 --> A4 --> S1 --> D1
    D1 -- No --> S6 --> A3
    D1 -- Yes --> F1
    F1 --> S2 --> J1
    F1 --> S3 --> J1
    J1 --> D2
    D2 -- No --> End([End])
    D2 -- Yes --> F2
    F2 --> S4 --> E1 --> J2
    F2 --> S5 --> J2
    J2 --> End
```

## Explanation
- **Stakeholder concerns:** Admins need controlled transitions; customers need timely shipment updates; management needs updated operational metrics.
- **Decisions/parallelism:** Guarded transition check prevents invalid status changes; notification and metrics refresh execute in parallel after key fulfillment states.
- **Use case and placeholder mapping:** Update Order Status, View All Customer Orders, Track Order Status; FR-117, FR-121; US-208; ST-208.
