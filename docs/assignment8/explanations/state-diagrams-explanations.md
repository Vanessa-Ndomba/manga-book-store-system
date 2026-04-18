# State Diagram Explanations

## 1) User Account
- **Key states/transitions:** Starts at `Unregistered`, moves to `Registered` after valid submission, then `Active` after email verification. Security and administration events move the account through `Locked`, `Suspended`, and `Deactivated`.
- **FR/UC mapping:** FR-1 (registration), FR-2 (authentication/session security), FR-15 (profile/account lifecycle). Use cases: UC-1 User Registration, UC-2 User Login, UC-8 Logout.

## 2) User Session
- **Key states/transitions:** `NoSession` to `Authenticated`/`ActiveSession` on valid login; inactivity transitions to `IdleSession` and `Expired`; user-triggered logout moves to `LoggedOut`.
- **FR/UC mapping:** FR-2 (secure sessions and timeout). Use cases: UC-2 User Login, UC-8 Logout.

## 3) Manga Listing
- **Key states/transitions:** Admin-managed publishing lifecycle: `Draft` → `PendingReview` → `Published`, with stock-driven transitions to `LowStock` and `OutOfStock`, and end-of-life `Archived`.
- **FR/UC mapping:** FR-3 (catalog display), FR-11/FR-12/FR-13 (add/update/remove manga listings). Use case support: UC-3 View Books, UC-4 Search for a Book.

## 4) Shopping Cart
- **Key states/transitions:** Cart lifecycle from `Empty` to `Active`/`Updated`, with guarded checkout transition (`hasItems && hasDeliveryAddress`) and inactivity transition to `Abandoned`.
- **FR/UC mapping:** FR-7 and FR-8 (add/modify cart), FR-9 (checkout prerequisites). Use cases: UC-5 Add Book to Cart, UC-6 Checkout.

## 5) Order
- **Key states/transitions:** Order processing path from `Created` → `PaymentPending` → `Confirmed` → `Processing` → `Packed` → `Shipped` → `Delivered` → `Completed`; includes cancellation and refund paths.
- **FR/UC mapping:** FR-9 (order placement), FR-10 (status visibility), FR-14 (admin order management). Use case: UC-6 Checkout.

## 6) Payment Transaction
- **Key states/transitions:** Payment lifecycle across `Initiated`, `Authorized`, `Captured`, `Settled`, with failure, void, and refund states driven by payment outcomes and order events.
- **FR/UC mapping:** FR-9 (payment method during checkout) and FR-14 (admin visibility into order/payment flow).

## 7) Inventory Item
- **Key states/transitions:** Operational stock states (`InStock`, `LowStock`, `OutOfStock`) plus transactional states (`Reserved`, `Allocated`) and recovery/compliance states (`Restocking`, `Quarantined`, `Discontinued`).
- **FR/UC mapping:** FR-7 (stock validation), FR-11/FR-12/FR-13 (inventory maintenance), FR-14 (order processing dependencies).

## 8) Shipment
- **Key states/transitions:** Logistics flow from `PendingDispatch` to `Delivered`, with exception handling (`Exception`) and return loop (`Returned`) before closure.
- **FR/UC mapping:** FR-10 (track order statuses) and FR-14 (admin-managed fulfillment progression).
