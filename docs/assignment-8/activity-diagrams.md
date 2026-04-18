# Assignment 8 - UML Activity Diagrams (Mermaid)

This document contains **8 workflow activity diagrams** with swimlanes (actors), decisions, and parallel actions, plus short traceability notes.

---

## 1) User Registration

```mermaid
flowchart TD
    Start([Start]) --> U1

    subgraph User
      U1[Open registration page]
      U2[Enter registration details]
      U3[Submit form]
      U4[Correct form errors]
      U5[Open verification email]
    end

    subgraph System
      S1[Validate email and password]
      D1{Input valid?}
      S2[Create account record]
      F1{{Fork}}
      S3[Send confirmation email]
      S4[Write audit log]
      J1{{Join}}
      D2{Email verified?}
      S5[Activate account]
    end

    U1 --> U2 --> U3 --> S1 --> D1
    D1 -- No --> U4 --> U2
    D1 -- Yes --> S2 --> F1
    F1 --> S3
    F1 --> S4
    S3 --> J1
    S4 --> J1
    J1 --> U5 --> D2
    D2 -- Yes --> S5 --> End([End])
    D2 -- No --> End
```

**Explanation:** Handles account creation, validation loops, and parallel confirmation/audit actions.  
**Traceability:** FR-1, FR-2; US-001; Assignment 6 tasks AP6-T07, AP6-T08.

---

## 2) User Login

```mermaid
flowchart TD
    Start([Start]) --> U1

    subgraph User
      U1[Open login page]
      U2[Enter credentials]
      U3[Submit login request]
      U4[Retry credentials]
      U5[Access dashboard]
    end

    subgraph System
      S1[Validate credentials]
      D1{Credentials valid?}
      S2[Create secure session]
      F1{{Fork}}
      S3[Record login event]
      S4[Load role permissions]
      J1{{Join}}
      D2{Session timed out?}
      S5[Invalidate session]
    end

    U1 --> U2 --> U3 --> S1 --> D1
    D1 -- No --> U4 --> U2
    D1 -- Yes --> S2 --> F1
    F1 --> S3
    F1 --> S4
    S3 --> J1
    S4 --> J1
    J1 --> U5 --> D2
    D2 -- No --> U5
    D2 -- Yes --> S5 --> End([End])
```

**Explanation:** Models secure authentication, session initialization, and timeout behavior.  
**Traceability:** FR-2; US-002; Assignment 6: inferred from account/security work (not explicitly decomposed).

---

## 3) Browse/Search and View Book

```mermaid
flowchart TD
    Start([Start]) --> U1

    subgraph User
      U1[Open catalog]
      U2[Enter search query / apply filters]
      U3[Select manga title]
    end

    subgraph System
      S1[Load catalog and trending content]
      F1{{Fork}}
      S2[Query search index]
      S3[Fetch recommendations metadata]
      J1{{Join}}
      D1{Results found?}
      S4[Display matching results]
      S5[Display no-results guidance]
      S6[Render manga details page]
    end

    U1 --> S1 --> F1
    F1 --> S2
    F1 --> S3
    S2 --> J1
    S3 --> J1
    J1 --> U2 --> D1
    D1 -- Yes --> S4 --> U3 --> S6 --> End([End])
    D1 -- No --> S5 --> U2
```

**Explanation:** Captures discovery flow and high-performance search behavior with alternate no-result loop.  
**Traceability:** FR-3, FR-4, FR-5, FR-6; US-003, US-004, US-005, US-006; Assignment 6 tasks AP6-T01, AP6-T02, AP6-T03.

---

## 4) Add to Cart and Update Cart

```mermaid
flowchart TD
    Start([Start]) --> U1

    subgraph User
      U1[Choose title and quantity]
      U2[Add item to cart]
      U3[Update quantity/remove item]
      U4[Proceed to checkout]
    end

    subgraph System
      S1[Validate stock]
      D1{Stock sufficient?}
      S2[Add/update cart line item]
      F1{{Fork}}
      S3[Recalculate cart totals]
      S4[Persist cart state]
      J1{{Join}}
      D2{Cart has items?}
      S5[Show stock error]
    end

    U1 --> U2 --> S1 --> D1
    D1 -- No --> S5 --> U1
    D1 -- Yes --> S2 --> F1
    F1 --> S3
    F1 --> S4
    S3 --> J1
    S4 --> J1
    J1 --> U3 --> D2
    D2 -- No --> U1
    D2 -- Yes --> U4 --> End([End])
```

**Explanation:** Ensures stock-safe cart updates with concurrent persistence and total recalculation.  
**Traceability:** FR-7, FR-8; US-007, US-008; Assignment 6 tasks AP6-T04, AP6-T05, AP6-T06.

---

## 5) Checkout and Place Order

```mermaid
flowchart TD
    Start([Start]) --> U1

    subgraph User
      U1[Open checkout]
      U2[Confirm address and contact details]
      U3[Review order summary]
      U4[Place order]
    end

    subgraph System
      S1[Validate cart and delivery details]
      D1{Checkout data valid?}
      S2[Reserve inventory]
      S3[Create order in Payment Pending]
      F1{{Fork}}
      S4[Generate order ID]
      S5[Send order confirmation stub]
      J1{{Join}}
    end

    U1 --> U2 --> U3 --> U4 --> S1 --> D1
    D1 -- No --> U2
    D1 -- Yes --> S2 --> S3 --> F1
    F1 --> S4
    F1 --> S5
    S4 --> J1
    S5 --> J1
    J1 --> End([End])
```

**Explanation:** Separates order creation from gateway execution, leaving order in payment-pending state.  
**Traceability:** FR-9; US-009; Assignment 6: inferred from checkout scope (not explicitly decomposed).

---

## 6) Process Payment

```mermaid
flowchart TD
    Start([Start]) --> S1

    subgraph System
      S1[Load Payment Pending order]
      S2[Build payment request]
    end

    subgraph PaymentGateway
      P1[Authorize payment]
      D1{Authorized?}
      P2[Capture payment]
      D2{Capture success?}
      P3[Return decline/error code]
    end

    subgraph System_2[System]
      F1{{Fork}}
      S3[Mark order Confirmed]
      S4[Send receipt email]
      J1{{Join}}
      S5[Mark payment failed]
      S6[Release reserved stock]
    end

    S1 --> S2 --> P1 --> D1
    D1 -- No --> P3 --> S5 --> S6 --> End([End])
    D1 -- Yes --> P2 --> D2
    D2 -- No --> P3 --> S5 --> S6 --> End
    D2 -- Yes --> F1
    F1 --> S3
    F1 --> S4
    S3 --> J1
    S4 --> J1
    J1 --> End
```

**Explanation:** Isolates payment gateway lifecycle and order outcome updates for clarity and failure handling.  
**Traceability:** FR-9, FR-14; US-009, US-014; Assignment 6: inferred (not explicitly decomposed).

---

## 7) Admin Add/Update Book Inventory

```mermaid
flowchart TD
    Start([Start]) --> A1

    subgraph Admin
      A1[Open inventory management]
      A2[Add or edit manga listing]
      A3[Submit inventory form]
    end

    subgraph System
      S1[Validate required fields and ISBN rules]
      D1{Validation passed?}
      F1{{Fork}}
      S2[Save listing changes]
      S3[Write change history log]
      J1{{Join}}
      D2{Stock quantity is zero?}
      S4[Set status Out of Stock]
      S5[Set status In Stock / Low Stock]
    end

    A1 --> A2 --> A3 --> S1 --> D1
    D1 -- No --> A2
    D1 -- Yes --> F1
    F1 --> S2
    F1 --> S3
    S2 --> J1
    S3 --> J1
    J1 --> D2
    D2 -- Yes --> S4 --> End([End])
    D2 -- No --> S5 --> End
```

**Explanation:** Supports controlled catalog maintenance with validation and audit logging.  
**Traceability:** FR-11, FR-12, FR-13; US-011, US-012, US-013; Assignment 6: admin work not explicitly scheduled.

---

## 8) Order Fulfillment/Shipping and Return/Refund

```mermaid
flowchart TD
    Start([Start]) --> A1

    subgraph Admin_Warehouse[Admin/Warehouse]
      A1[Open confirmed order]
      A2[Pick, pack, handoff to carrier]
      A3[Receive return request]
      A4[Inspect returned item]
    end

    subgraph Carrier
      C1[Pick up shipment]
      C2[Deliver package]
    end

    subgraph Customer
      U1[Receive delivery]
      U2[Request return/refund]
    end

    subgraph System
      S1[Update order to Processing/Packed/Shipped]
      F1{{Fork}}
      S2[Notify customer of shipment]
      S3[Persist tracking/status history]
      J1{{Join}}
      D1{Return requested?}
      D2{Return eligible?}
      S4[Issue return label]
      S5[Reject return request]
      S6[Process refund]
      S7[Close order]
    end

    A1 --> A2 --> C1 --> S1 --> F1
    F1 --> S2
    F1 --> S3
    S2 --> J1
    S3 --> J1
    J1 --> C2 --> U1 --> D1
    D1 -- No --> S7 --> End([End])
    D1 -- Yes --> U2 --> A3 --> D2
    D2 -- No --> S5 --> End
    D2 -- Yes --> S4 --> A4 --> S6 --> S7 --> End
```

**Explanation:** Covers downstream logistics and post-delivery return/refund branch in one operational workflow.  
**Traceability:** FR-10, FR-14; US-010, US-014; Assignment 6: inferred (not explicitly decomposed).
