# User Stories - MangaBookStore System

## User Stories Table (15 Functional + 4 Non-Functional Stories)

| Story ID | User Story | Acceptance Criteria | Priority | Req Map | UC Map |
|----------|-----------|-------------------|----------|---------|--------|
| **US-001** | As a customer, I want to register an account with email and password so that I can save my preferences and order history. | AC1: Valid email format validation; AC2: Password minimum 8 characters (uppercase, lowercase, numeric); AC3: Confirmation email within 5 seconds; AC4: Duplicate email prevention; AC5: Clear success feedback. | **High** | FR-1 | UC-1 |
| **US-002** | As a customer, I want to log in securely so that I can access my account safely. | AC1: Email/password login support; AC2: 30-minute session timeout; AC3: Failed attempts logged; AC4: Clear error messages; AC5: Secure session token. | **High** | FR-2 | UC-2 |
| **US-003** | As a customer, I want to view the manga catalog with full details so that I can browse available titles. | AC1: Display title, author, genre, price, stock, image, rating; AC2: 20 items per page pagination; AC3: Stock status clearly shown; AC4: Page loads in ≤3 seconds; AC5: Images display correctly. | **High** | FR-3 | UC-3 |
| **US-004** | As a customer, I want to filter manga by category/genre so that I can find specific content quickly. | AC1: Multi-category filtering available; AC2: Action, Romance, Horror, Slice of Life, Fantasy, Sci-Fi categories; AC3: Results within 2 seconds; AC4: Intuitive filter interface; AC5: Selected filters clearly displayed. | **High** | FR-4 | UC-3 |
| **US-005** | As a customer, I want to search for manga by title, author, or ISBN so that I can locate specific books. | AC1: Search by title/author/ISBN; AC2: Results within 2 seconds for 1,000+ results; AC3: Case-insensitive; AC4: Partial matching supported; AC5: Results ranked by relevance. | **High** | FR-5 | UC-4 |
| **US-006** | As a customer, I want to see trending and recommended manga so that I can discover popular titles. | AC1: Top 10 best-sellers displayed; AC2: Top 10 highest-rated displayed; AC3: Updated daily; AC4: Personalized recommendations if logged in; AC5: Section loads within 3 seconds. | **Medium** | FR-6 | UC-3 |
| **US-007** | As a customer, I want to add manga to my shopping cart so that I can purchase multiple items. | AC1: Quantity selection available; AC2: Stock validation prevents over-ordering; AC3: Real-time price calculation; AC4: Cart persists 24 hours; AC5: Add confirmation feedback. | **High** | FR-7 | UC-5 |
| **US-008** | As a customer, I want to modify my shopping cart so that I can adjust my order before checkout. | AC1: Update quantity (minimum 1); AC2: Remove items available; AC3: Instant price recalculation; AC4: 24-hour persistence; AC5: Undo functionality available. | **High** | FR-8 | UC-5 |
| **US-009** | As a customer, I want to complete checkout and place an order so that I can purchase manga. | AC1: Delivery address required; AC2: Confirmation email within 5 seconds; AC3: Unique order ID generated; AC4: Payment method selection; AC5: Order summary review before confirmation. | **High** | FR-9 | UC-6 |
| **US-010** | As a customer, I want to access my order history so that I can track past purchases. | AC1: View all past orders with details; AC2: Status: Processing, Shipped, Delivered, Cancelled; AC3: Accessible from profile; AC4: Filter by date/status; AC5: Clear order details display. | **High** | FR-10 | UC-7 |
| **US-011** | As a system admin, I want to add new manga titles so that I can expand inventory. | AC1: Input title, author, ISBN, genre, price, quantity; AC2: All fields required with validation; AC3: Cover image upload (JPEG, PNG); AC4: Success confirmation; AC5: Items immediately visible. | **High** | FR-11 | N/A |
| **US-012** | As a system admin, I want to update manga information so that I can keep the catalog current. | AC1: Modify all fields except ISBN; AC2: Updates reflect within 1 minute; AC3: Change history logged; AC4: Confirmation provided; AC5: Audit trail maintained. | **High** | FR-12 | N/A |
| **US-013** | As a system admin, I want to remove manga listings so that I can discontinue outdated items. | AC1: Deletion with confirmation; AC2: Items removed from searches; AC3: Deletion logged; AC4: Soft-delete option for recovery; AC5: User notifications for cart items. | **Medium** | FR-13 | N/A |
| **US-014** | As a system admin, I want to manage all customer orders so that I can process deliveries. | AC1: View all orders with customer info; AC2: Update order status; AC3: Search by ID, customer name, date; AC4: Results within 2 seconds; AC5: Bulk actions available. | **High** | FR-14 | N/A |
| **US-015** | As a customer, I want to manage my profile so that I can keep account details current. | AC1: Edit name, email, phone; AC2: Add/update delivery addresses; AC3: Changes saved and confirmed; AC4: Email verification for changes; AC5: Saved addresses for future use. | **High** | FR-15 | UC-7 |

## Non-Functional User Stories

| Story ID | User Story | Acceptance Criteria | Priority | Req Map |
|----------|-----------|-------------------|----------|---------|
| **US-NFR-001** | As a system admin, I want user data encrypted with AES-256 so that security compliance is met. | AC1: Data encrypted at rest; AC2: TLS 1.2+ transmission; AC3: Secure key management; AC4: Encryption audit completed; AC5: Zero unencrypted sensitive data. | **High** | NFR-9 |
| **US-NFR-002** | As a platform owner, I want to support 1,000 concurrent users so that peak traffic is handled without degradation. | AC1: Connection pooling implemented; AC2: Redis caching reduces queries by 70%; AC3: No degradation at 1,000 users; AC4: Load testing completed; AC5: Performance metrics monitored. | **High** | NFR-7 |
| **US-NFR-003** | As a user with accessibility needs, I want WCAG 2.1 Level AA compliance so that I can use the system effectively. | AC1: Contrast ratio ≥4.5:1; AC2: All images have alt-text; AC3: Full keyboard navigation; AC4: Font size 12-20px adjustable; AC5: Screen reader compatible. | **High** | NFR-1 |
| **US-NFR-004** | As a developer, I want comprehensive API documentation so that I can integrate features efficiently. | AC1: All endpoints documented; AC2: Auto-generated from code comments; AC3: Updated with changes; AC4: OpenAPI/Swagger available; AC5: Examples include edge cases. | **Medium** | NFR-5 |

## INVEST Criteria Compliance

All stories follow INVEST principles:
- **Independent**: Each story developed independently
- **Negotiable**: Clear criteria allowing discussion during refinement
- **Valuable**: Delivers tangible value to customers or business
- **Estimable**: Sufficient detail for effort estimation
- **Small**: Fits within sprint (2-5 story points)
- **Testable**: Acceptance criteria provide clear test cases