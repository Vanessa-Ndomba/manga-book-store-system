# Shipment Fulfillment State Diagram

```mermaid
stateDiagram-v2
    [*] --> NotScheduled
    NotScheduled --> Scheduled: Create shipment [orderConfirmed]
    Scheduled --> Picking: Start picking
    Picking --> Packed: Pack items [allItemsPicked]
    Packed --> InTransit: Handover to carrier
    InTransit --> OutForDelivery: Last-mile dispatch
    OutForDelivery --> Delivered: Delivery success
    InTransit --> Exception: Carrier issue [deliveryBlocked]
    OutForDelivery --> Exception: Delivery failed [recipientUnavailable]
    Exception --> InTransit: Reattempt delivery [addressConfirmed]
    Delivered --> Completed: Proof of delivery recorded
    Completed --> [*]
```

## Explanation
- **Key states/transitions:** Fulfillment transitions from scheduling through carrier events, with guarded exception recovery.
- **Use case mapping:** Track Order Status, Update Order Status, View All Customer Orders.
- **Placeholder traceability:** FR-116 (fulfillment tracking), FR-117 (delivery exception handling); US-106; ST-106.
