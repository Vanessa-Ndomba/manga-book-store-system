# Domain Model: MangaBookStore

This domain model captures the key business entities, responsibilities, relationships, and rules for the **MangaBookStore – Online Manga Retail System**.

## 1) Key Domain Entities (7)

> Selected to align with the system requirements (SRD), use cases, and the Assignment 8 behavioral models (cart, order, payment, inventory, shipment, session).

### Domain Model Summary Table

| Entity | Attributes (data fields) | Responsibilities / Methods | Relationships (with multiplicity) |
|---|---|---|---|
| **UserAccount** | userId, fullName, email, passwordHash, phoneNumber, role, status, createdAt | register(), authenticate(), updateProfile(), changePassword(), deactivate() | 1 UserAccount **has** 0..* Orders; 1 UserAccount **has** 0..1 ShoppingCart; 1 UserAccount **has** 0..* UserSessions |
| **UserSession** | sessionId, userId, createdAt, lastActivityAt, expiresAt, ipAddress, isActive | start(), refreshActivity(), isExpired(), end() | Each UserSession **belongs to** 1 UserAccount; 1 UserAccount **owns** 0..* UserSessions |
| **MangaListing** | mangaId, title, author, isbn, genre, description, coverImageUrl, rating, price, stockStatus | updateDetails(), updatePrice(), matchesSearch(query), isAvailable() | 1 MangaListing **is referenced by** 0..* CartItems; 1 MangaListing **is referenced by** 0..* OrderItems (see note below) |
| **ShoppingCart** | cartId, userId, status, createdAt, updatedAt, totalAmount | addItem(mangaId, qty), removeItem(mangaId), updateQuantity(mangaId, qty), calculateTotal(), clear(), convertToOrder() | 1 ShoppingCart **contains** 1..* CartItems (composition); 1 UserAccount **has** 0..1 ShoppingCart |
| **CartItem** | cartItemId, mangaId, quantity, unitPriceAtAdd, lineTotal | computeLineTotal(), incrementQty(), decrementQty() | Each CartItem **belongs to** 1 ShoppingCart; Each CartItem **references** 1 MangaListing |
| **Order** | orderId, userId, orderDate, status, totalAmount, confirmationNumber, deliveryAddress | placeFromCart(cart), cancel(), updateStatus(), computeTotal() | 1 UserAccount **places** 0..* Orders; 1 Order **has** 1 PaymentTransaction; 1 Order **contains** 1..* OrderItems (see note below) |
| **PaymentTransaction** | paymentId, orderId, method, status, amount, createdAt, failureReason | authorize(), fail(reason), refund(), validateAmount() | Each PaymentTransaction **belongs to** 1 Order; 1 Order **has** exactly 1 PaymentTransaction |

**Note on OrderItems:** To keep the entity count within the required range (5–7), the model focuses on `CartItem` for itemization. In a full implementation, `OrderItem` would be introduced as a separate entity so that a placed order preserves the purchased items even if the cart changes later.

---

## 2) Relationships (Narrative)

- A **UserAccount** can create multiple **UserSessions** over time (e.g., different devices). Sessions expire after inactivity.
- A **UserAccount** may have **one active ShoppingCart** at a time (0..1). The cart holds the items the user intends to purchase.
- A **ShoppingCart** is composed of **CartItems**; when the cart is cleared or converted, its CartItems are removed.
- Each **CartItem** references a single **MangaListing** and stores quantity and pricing snapshot data.
- A **UserAccount** can place many **Orders**.
- Each **Order** is paid via exactly one **PaymentTransaction** (simulated payment methods per project constraints).

---

## 3) Business Rules (from SRD / Use Cases)

### Authentication & Session Rules
- **BR-1 (Unique email):** A user’s email must be unique; duplicate registrations are rejected.
- **BR-2 (Password policy):** Passwords must be at least 8 characters and include uppercase, lowercase, and numeric characters.
- **BR-3 (Session timeout):** Sessions expire after **30 minutes of inactivity**.
- **BR-4 (Security logging):** Unauthorized access attempts are logged (IP + timestamp).

### Catalog & Search Rules
- **BR-5 (Catalog pagination):** Catalog results are paginated at **20 items per page**.
- **BR-6 (Search behavior):** Search is case-insensitive and supports partial title matching.
- **BR-7 (Stock status display):** MangaListing stock status is one of: **In Stock**, **Out of Stock**, **Pre-Order**.

### Cart Rules
- **BR-8 (Minimum quantity):** A CartItem quantity cannot be less than 1.
- **BR-9 (Stock validation):** Cart quantities cannot exceed available stock (prevents over-ordering).
- **BR-10 (Cart persistence):** A cart persists for **24 hours** (unless converted to an order).

### Order & Payment Rules
- **BR-11 (Address required):** Delivery address is required before an order can be placed.
- **BR-12 (Order status values):** Order status is one of: **Processing**, **Shipped**, **Delivered**, **Cancelled**.
- **BR-13 (Payment simulation):** Payment processing is simulated; failed payments must return an actionable error and allow retry.
- **BR-14 (Confirmation):** Order confirmation (including a unique order ID) is generated and communicated to the user (email simulated).

---

## 4) Traceability (Quick Mapping)

- **FR-1 / FR-2** → `UserAccount`, `UserSession` (register, authenticate, session timeout)
- **FR-3 to FR-6** → `MangaListing` (catalog details, filtering, search, trending/recommended)
- **FR-7 / FR-8** → `ShoppingCart`, `CartItem` (add/update/remove items, total calculation, persistence)
- **FR-9 / FR-10** → `Order`, `PaymentTransaction` (place order, order history, payment selection/simulation)
