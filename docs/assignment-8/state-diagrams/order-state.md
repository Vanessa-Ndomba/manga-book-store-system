# Order State Diagram

```mermaid
stateDiagram-v2
    [*] --> Created
    Created --> PendingPayment: Checkout submitted
    PendingPayment --> Confirmed: Payment authorized [paymentValid]
    PendingPayment --> PaymentFailed: Payment declined [paymentInvalid]
    PaymentFailed --> PendingPayment: Retry payment
    Confirmed --> Processing: Stock allocated [stockReserved]
    Processing --> Packed: Packing complete
    Packed --> Shipped: Carrier pickup
    Shipped --> Delivered: Delivery confirmed
    Delivered --> Closed: Return window elapsed
    Created --> Cancelled: User cancels [beforeConfirmation]
    PendingPayment --> Cancelled: User cancels [beforeConfirmation]
    Confirmed --> Cancelled: Admin cancels [fraudDetected]
    Cancelled --> Refunded: Refund completed
    Refunded --> [*]
    Closed --> [*]
```

## Explanation
- **Key states/transitions:** Payment and fulfillment states are separated to represent checkout risk and operational flow.
- **Use case mapping:** Checkout Process, Place Order, Track Order Status, View All Customer Orders, Update Order Status.
- **Placeholder traceability:** FR-110 (create order), FR-111 (track order), FR-112 (cancel/refund order); US-104; ST-104.
