# Assignment 9: Domain Model Documentation

## Overview
This domain model for **MangaBookStore** is aligned with the repository artifacts in:
- `SYSTEM_REQUIREMENTS.md` (FR-1 to FR-15, NFRs)
- `USE_CASE_SPECIFICATIONS.md` (registration, login, view/search books, cart, checkout, profile)
- `docs/assignment8/state-diagrams/*` and `docs/assignment8/activity-diagrams/*`

The model focuses on 7 key entities that drive customer ordering and admin inventory workflows.

## Key Domain Entities

| Entity | Attributes (Data Fields) | Responsibilities / Methods | Relationships |
|---|---|---|---|
| **UserAccount** | userId, fullName, email, passwordHash, role, phoneNumber, accountStatus, createdAt, lastLoginAt | register(), authenticate(), logout(), updateProfile(), addAddress(), deactivateAccount() | One UserAccount owns 0..* ShoppingCart records over time; one UserAccount places 0..* Order records; one UserAccount stores 0..* delivery addresses used by Order. |
| **MangaListing** | mangaId, isbn, title, author, genre, price, description, coverImageUrl, listingStatus, averageRating | publish(), archive(), updateDetails(), updatePrice(), markOutOfStock(), markLowStock() | One MangaListing is represented by exactly one InventoryItem; one MangaListing appears in 0..* CartItem entries; one MangaListing appears in 0..* OrderItem entries. |
| **InventoryItem** | inventoryItemId, mangaId, quantityOnHand, reservedQuantity, reorderThreshold, stockState, lastRestockedAt | reserveStock(qty), releaseReservation(qty), allocateForOrder(qty), replenish(qty), markDiscontinued() | InventoryItem is composition-owned by MangaListing (lifecycle bound to listing SKU); InventoryItem supports availability checks for CartItem and OrderItem flows. |
| **ShoppingCart** | cartId, userId, cartStatus, createdAt, updatedAt, expiresAt, subtotalAmount | addItem(mangaId, qty), updateItemQty(cartItemId, qty), removeItem(cartItemId), clear(), calculateTotals(), checkout() | One UserAccount has 0..* ShoppingCart instances over time; one ShoppingCart composition-contains 1..* CartItem while active; one ShoppingCart can convert to 0..1 Order. |
| **CartItem** | cartItemId, cartId, mangaId, quantity, unitPriceSnapshot, lineTotal | setQuantity(qty), recalculateLineTotal(), validateAgainstStock() | CartItem composition child of ShoppingCart; each CartItem references exactly one MangaListing; many CartItem rows can point to the same MangaListing. |
| **Order** | orderId, userId, sourceCartId, shippingAddressId, orderDate, orderStatus, subtotal, shippingFee, totalAmount, confirmationCode | place(), calculateTotal(), cancel(reason), markProcessing(), markShipped(), markDelivered(), generateConfirmation() | One UserAccount places 0..* Order; one Order composition-contains 1..* OrderItem; one Order is paid by 0..1 PaymentTransaction; one Order is created from exactly one checked-out cart snapshot. |
| **PaymentTransaction** | paymentId, orderId, paymentMethod, amount, currency, paymentStatus, gatewayReference, initiatedAt, settledAt | authorize(), capture(), void(), refund(amount), fail(reason) | One PaymentTransaction belongs to exactly one Order; one Order may have 0..1 primary PaymentTransaction in this simplified model. |

## Explicit Business Rules

1. **BR-1 (Unique Account):** Email must be unique per `UserAccount` (aligns with FR-1 duplicate email prevention).
2. **BR-2 (Password Policy):** Registration requires password strength (min 8 chars with mixed character classes, per FR-1).
3. **BR-3 (Cart Quantity Validity):** `CartItem.quantity >= 1`; zero or negative values are invalid (aligns with FR-8).
4. **BR-4 (Stock Constraint):** `ShoppingCart.addItem()` and quantity updates cannot exceed available stock in `InventoryItem` (aligns with FR-7 stock validation).
5. **BR-5 (Checkout Preconditions):** Checkout requires at least one CartItem and a delivery address before order creation (aligns with checkout activity and cart state guards).
6. **BR-6 (Order Identity):** Every placed Order gets a unique order ID and confirmation output (aligns with FR-9).
7. **BR-7 (Order Status Flow):** Order transitions follow a constrained lifecycle (`Created -> PaymentPending -> Confirmed -> Processing -> Packed -> Shipped -> Delivered/Cancelled`) as modeled in Assignment 8.
8. **BR-8 (Payment Capture Rule):** Payment can be captured only after authorization success; failed authorization cannot proceed to capture.
9. **BR-9 (Inventory Reservation Rule):** Stock is reserved at checkout and allocated only after order confirmation; abandoned checkout releases reservation.
10. **BR-10 (Listing Edit Constraint):** ISBN is immutable after creation (aligns with FR-12 rule that all fields except ISBN can be modified).

## Scope Note
This model intentionally keeps external integrations (payment gateway, shipping carrier, notification service) abstract to stay consistent with the repository’s simulation constraint for payment/shipping in MVP scope.
