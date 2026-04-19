# Checkout Process Workflow Activity Diagram

```mermaid
flowchart TD
    Start([Start]) --> U1

    subgraph Registered_Customer[Registered Customer]
      U1[Open checkout]
      U2[Confirm shipping and payment details]
      U3[Submit checkout]
      U4[Retry checkout]
    end

    subgraph System
      S1[Validate checkout payload]
      D1{Payload valid?}
      S2[Validate stock for each line]
      D2{All items in stock?}
      S3[Create pending order]
      S4[Call payment gateway]
      D3{Payment authorized?}
      F1{{Fork}}
      S5[Mark order confirmed]
      S6[Reserve inventory]
      J1{{Join}}
      S7[Release holds and mark payment failed]
    end

    subgraph Payment_Gateway[Payment Gateway]
      P1[Authorize payment]
    end

    U1 --> U2 --> U3 --> S1 --> D1
    D1 -- No --> U4 --> U2
    D1 -- Yes --> S2 --> D2
    D2 -- No --> U4
    D2 -- Yes --> S3 --> S4 --> P1 --> D3
    D3 -- No --> S7 --> U4
    D3 -- Yes --> F1
    F1 --> S5 --> J1
    F1 --> S6 --> J1
    J1 --> End([End])
```

## Explanation
- **Stakeholder concerns:** Customers need trustworthy checkout outcomes; finance/inventory teams require atomic confirmation behavior.
- **Decisions/parallelism:** Validation and payment decisions enforce correctness; confirmation and inventory reservation run in parallel to reduce latency.
- **Use case and placeholder mapping:** Checkout Process, Process Payment, Validate Stock Availability; FR-110, FR-113, FR-118; US-206; ST-206.
