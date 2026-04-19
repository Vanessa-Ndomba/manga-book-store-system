# Shopping Cart State Diagram

```mermaid
stateDiagram-v2
    [*] --> Empty
    Empty --> Active: Add item [stockAvailable]
    Active --> Active: Modify quantity [quantityValid]
    Active --> Active: Remove line item [itemsRemaining]
    Active --> Empty: Remove last item
    Active --> Reserved: Checkout initiated
    Reserved --> Active: Return to cart [sessionValid]
    Reserved --> ConvertedToOrder: Place order [paymentAuthorized]
    Reserved --> Active: Payment failed
    Active --> Abandoned: Session timeout [idleTime > limit]
    Abandoned --> Active: User resumes cart
    ConvertedToOrder --> [*]
    Empty --> [*]
```

## Explanation
- **Key states/transitions:** Cart lifecycle supports add/modify/remove flows, reservation during checkout, and abandonment/resume behavior.
- **Use case mapping:** Add Items to Shopping Cart, Modify Cart Quantity, Remove Items from Cart, Checkout Process, Place Order.
- **Placeholder traceability:** FR-107 (cart operations), FR-108 (cart reservation), FR-109 (recover abandoned carts); US-103; ST-103.
