# Assignment 9: Class Diagram (Mermaid.js)

## Mermaid Class Diagram

```mermaid
classDiagram
    class UserAccount {
        +String userId
        +String fullName
        +String email
        +String passwordHash
        +String role
        +String accountStatus
        +register()
        +authenticate()
        +updateProfile()
        +addAddress()
        +logout()
    }

    class Customer {
        +viewCatalog()
        +addToCart()
        +checkout()
    }

    class Admin {
        +createMangaListing()
        +updateInventory()
        +updateOrderStatus()
    }

    class MangaListing {
        +String mangaId
        +String isbn
        +String title
        +String author
        +String genre
        +Decimal price
        +String listingStatus
        +publish()
        +archive()
        +updateDetails()
        +updatePrice()
    }

    class InventoryItem {
        +String inventoryItemId
        +int quantityOnHand
        +int reservedQuantity
        +int reorderThreshold
        +String stockState
        +reserveStock(qty)
        +releaseReservation(qty)
        +allocateForOrder(qty)
        +replenish(qty)
    }

    class ShoppingCart {
        +String cartId
        +String cartStatus
        +DateTime createdAt
        +DateTime updatedAt
        +DateTime expiresAt
        +Decimal subtotalAmount
        +addItem(mangaId, qty)
        +updateItemQty(cartItemId, qty)
        +removeItem(cartItemId)
        +calculateTotals()
        +checkout()
    }

    class CartItem {
        +String cartItemId
        +int quantity
        +Decimal unitPriceSnapshot
        +Decimal lineTotal
        +setQuantity(qty)
        +recalculateLineTotal()
        +validateAgainstStock()
    }

    class Order {
        +String orderId
        +DateTime orderDate
        +String orderStatus
        +Decimal subtotal
        +Decimal shippingFee
        +Decimal totalAmount
        +String confirmationCode
        +place()
        +calculateTotal()
        +cancel(reason)
        +markProcessing()
        +markShipped()
        +markDelivered()
    }

    class OrderItem {
        +String orderItemId
        +int quantity
        +Decimal unitPrice
        +Decimal lineTotal
        +calculateLineTotal()
    }

    class PaymentTransaction {
        +String paymentId
        +String paymentMethod
        +Decimal amount
        +String paymentStatus
        +String gatewayReference
        +DateTime initiatedAt
        +authorize()
        +capture()
        +void()
        +refund(amount)
    }

    UserAccount <|-- Customer
    UserAccount <|-- Admin

    Customer "1" --> "0..*" ShoppingCart : owns
    Customer "1" --> "0..*" Order : places

    ShoppingCart "1" *-- "1..*" CartItem : contains
    CartItem "0..*" --> "1" MangaListing : references

    MangaListing "1" *-- "1" InventoryItem : stock record

    ShoppingCart "0..1" --> "1" Order : convertsTo
    Order "1" *-- "1..*" OrderItem : contains
    OrderItem "0..*" --> "1" MangaListing : purchasedItem

    Order "1" o-- "0..1" PaymentTransaction : paidBy

    note for Order "Order states align with Assignment 8 order lifecycle: Created -> PaymentPending -> Confirmed -> Processing -> Packed -> Shipped -> Delivered/Cancelled"
    note for ShoppingCart "Checkout allowed only when cart has items and a delivery address is provided"
```

## Key Design Decisions

- **Inheritance for roles:** `Customer` and `Admin` inherit from `UserAccount` to share identity/security fields while separating role-specific behaviors.
- **Composition for lifecycle ownership:** `ShoppingCart` composes `CartItem`, and `Order` composes `OrderItem` because child records should not exist independently.
- **Composition for stock model:** `InventoryItem` is composition-bound to `MangaListing` in this simplified design to represent one stock record per SKU.
- **Association with multiplicity:** Multiplicity clarifies business constraints (for example, one customer can place many orders, while each order has at most one primary payment transaction).
- **State-model alignment:** Order and payment operations are intentionally consistent with Assignment 8 state diagrams (authorization before capture, constrained transitions).
