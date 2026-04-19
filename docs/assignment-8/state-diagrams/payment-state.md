# Payment State Diagram

```mermaid
stateDiagram-v2
    [*] --> Initiated
    Initiated --> Authorized: Gateway authorize [cardValid]
    Initiated --> Failed: Gateway decline [cardInvalid]
    Failed --> Initiated: Retry payment
    Authorized --> Captured: Capture funds [orderConfirmed]
    Authorized --> Voided: Void authorization [orderCancelled]
    Captured --> Settled: Settlement batch completed
    Captured --> RefundPending: Refund requested [withinPolicy]
    RefundPending --> Refunded: Gateway refund success
    RefundPending --> Disputed: Chargeback opened
    Settled --> Disputed: Chargeback opened
    Voided --> [*]
    Refunded --> [*]
    Disputed --> [*]
```

## Explanation
- **Key states/transitions:** Authorization, capture, settlement, and refund/chargeback states model payment risk and finality.
- **Use case mapping:** Process Payment, Checkout Process, Place Order.
- **Placeholder traceability:** FR-113 (authorize payment), FR-114 (capture/settle), FR-115 (refund handling); US-105; ST-105.
