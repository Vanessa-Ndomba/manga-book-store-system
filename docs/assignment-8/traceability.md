# Assignment 8 Traceability

This file maps Assignment 8 diagrams to:
- Assignment 4 functional requirements (`SYSTEM_REQUIREMENTS.md`)
- Assignment 6 user stories (`USER_STORIES.md`) and sprint tasks (`AGILE_PLANNING_DOCUMENT.md`)

---

## Assignment 6 Sprint Task Key

Because Assignment 6 sprint tasks are listed without IDs, this mapping uses the following consistent identifiers:
These AP6 task IDs are introduced in Assignment 8 only for traceability clarity and do not exist as literal IDs in the original Assignment 6 file.

- **AP6-T01**: Research existing search algorithms  
- **AP6-T02**: Implement basic search  
- **AP6-T03**: Add advanced filters  
- **AP6-T04**: Setup cart structure in database  
- **AP6-T05**: Develop add-to-cart functionality  
- **AP6-T06**: Implement cart summary display  
- **AP6-T07**: Create user registration form  
- **AP6-T08**: Implement backend for account creation  
- **AP6-T09**: Write unit tests for new features  
- **AP6-T10**: Conduct user testing and gather feedback

---

## A) State Diagrams Traceability

| Diagram | Critical Object | Functional Requirements (A4) | User Stories (A6) | Sprint Tasks (A6) |
|---|---|---|---|---|
| `state-diagrams.md#1-user-account` | User Account | FR-1, FR-2, FR-15 | US-001, US-002, US-015 | AP6-T07, AP6-T08 |
| `state-diagrams.md#2-book-inventory-item` | Book Inventory Item | FR-7, FR-11, FR-12, FR-13, FR-14 | US-007, US-011, US-012, US-013, US-014 | Not explicitly decomposed in A6 sprint plan |
| `state-diagrams.md#3-shopping-cart` | Shopping Cart | FR-7, FR-8, FR-9 | US-007, US-008, US-009 | AP6-T04, AP6-T05, AP6-T06 |
| `state-diagrams.md#4-order` | Order | FR-9, FR-10, FR-14 | US-009, US-010, US-014 | Not explicitly decomposed in A6 sprint plan |
| `state-diagrams.md#5-payment-transaction` | Payment Transaction | FR-9, FR-14 | US-009, US-014 | Not explicitly decomposed in A6 sprint plan |
| `state-diagrams.md#6-shipment` | Shipment | FR-10, FR-14 | US-010, US-014 | Not explicitly decomposed in A6 sprint plan |
| `state-diagrams.md#7-returnrefund-request` | Return/Refund Request | FR-10, FR-14 | US-010, US-014 | Not explicitly decomposed in A6 sprint plan |
| `state-diagrams.md#8-manga-listing` | Manga Listing | FR-3, FR-4, FR-5, FR-11, FR-12, FR-13 | US-003, US-004, US-005, US-011, US-012, US-013 | AP6-T01, AP6-T02, AP6-T03 |

---

## B) Activity Diagrams Traceability

| Diagram | Workflow | Functional Requirements (A4) | User Stories (A6) | Sprint Tasks (A6) |
|---|---|---|---|---|
| `activity-diagrams.md#1-user-registration` | User Registration | FR-1, FR-2 | US-001 | AP6-T07, AP6-T08 |
| `activity-diagrams.md#2-user-login` | User Login | FR-2 | US-002 | Inferred from account security scope; not explicitly decomposed |
| `activity-diagrams.md#3-browsesearch-and-view-book` | Browse/Search and View Book | FR-3, FR-4, FR-5, FR-6 | US-003, US-004, US-005, US-006 | AP6-T01, AP6-T02, AP6-T03 |
| `activity-diagrams.md#4-add-to-cart-and-update-cart` | Add to Cart and Update Cart | FR-7, FR-8 | US-007, US-008 | AP6-T04, AP6-T05, AP6-T06 |
| `activity-diagrams.md#5-checkout-and-place-order` | Checkout and Place Order | FR-9 | US-009 | Inferred from order scope; not explicitly decomposed |
| `activity-diagrams.md#6-process-payment` | Process Payment | FR-9, FR-14 | US-009, US-014 | Inferred from order-management scope; not explicitly decomposed |
| `activity-diagrams.md#7-admin-addupdate-book-inventory` | Admin Add/Update Book Inventory | FR-11, FR-12, FR-13 | US-011, US-012, US-013 | Not explicitly decomposed in A6 sprint plan |
| `activity-diagrams.md#8-order-fulfillmentshipping-and-returnrefund` | Order Fulfillment/Shipping and Return/Refund | FR-10, FR-14 | US-010, US-014 | Not explicitly decomposed in A6 sprint plan |

---

## Coverage Summary

- All major transactional domains are covered: account, catalog, cart, order, payment, shipment, returns.
- Functional requirement alignment covers FR-1 to FR-15 where applicable to Assignment 8 dynamic behavior.
- User story alignment references the structured story IDs in `USER_STORIES.md`.
- Assignment 6 sprint task mapping is explicit where tasks exist; gaps are labeled clearly as inferred/not explicitly decomposed.
