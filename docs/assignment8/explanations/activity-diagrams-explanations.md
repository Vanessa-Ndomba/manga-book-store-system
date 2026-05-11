# Activity Diagram Explanations

## 1) User Registration Workflow
- **What it does:** Captures registration input, validates it, creates account records, sends confirmation, and activates account after verification.
- **Decisions/parallelism:** `Input valid?` decision; fork/join for sending confirmation email and writing audit logs in parallel.
- **Stakeholder/NFR alignment:** Improves customer onboarding clarity (NFR-2 usability) and maintains auditability (NFR-10 RBAC logging, NFR-11 security controls).
- **Traceability:** FR-1, FR-2; UC-1; US-001; Sprint tasks T-001, T-002, T-003, T-004.

## 2) User Login Workflow
- **What it does:** Authenticates users, creates sessions, loads role permissions, and handles timeout/logout behavior.
- **Decisions/parallelism:** `Credentials valid?` and `Session timed out?` decisions; parallel login event logging and permission loading.
- **Stakeholder/NFR alignment:** Supports secure access and monitoring concerns for customers and developers (NFR-9, NFR-10, NFR-11).
- **Traceability:** FR-2; UC-2, UC-8; US-002; Sprint tasks T-005, T-006, T-007.

## 3) Search and Browse Manga Workflow
- **What it does:** Loads catalog data, processes search/filter input, and returns details for selected manga items.
- **Decisions/parallelism:** `Results found?` decision; parallel catalog query and recommendation metadata fetch.
- **Stakeholder/NFR alignment:** Addresses fast discovery and responsiveness needs (NFR-12 search performance, NFR-13 page load).
- **Traceability:** FR-3, FR-4, FR-5, FR-6; UC-3, UC-4; US-003, US-004, US-005, US-006; Sprint tasks T-008, T-009, T-010, T-011, T-012.

## 4) Cart Management Workflow
- **What it does:** Validates stock before adding items, persists cart state, supports quantity updates/removals, and controls checkout readiness.
- **Decisions/parallelism:** `Stock sufficient?` and `Cart has items?` decisions; parallel total recalculation and cart persistence.
- **Stakeholder/NFR alignment:** Improves consistency and cart reliability for customers under active usage (NFR-2 usability, NFR-14 availability).
- **Traceability:** FR-7, FR-8; UC-5; US-007, US-008; Sprint tasks T-013, T-014, T-015.

## 5) Checkout and Payment Workflow
- **What it does:** Validates checkout data, creates pending orders, calls payment authorization, and finalizes order confirmation.
- **Decisions/parallelism:** `Checkout data valid?` and `Payment authorized?` decisions; parallel generation of order status updates and confirmation email.
- **Stakeholder/NFR alignment:** Supports transaction reliability and user confidence in purchasing flows (NFR-9 security, NFR-13 performance).
- **Traceability:** FR-9, FR-10; UC-6; US-009, US-010; Sprint tasks: Not scheduled in current sprint plan.

## 6) Admin Order Fulfillment Workflow
- **What it does:** Lets admins process confirmed orders through fulfillment and shipment stages.
- **Decisions/parallelism:** `Payment settled?` and `Carrier pickup confirmed?` decisions; parallel inventory reservation/pick list generation and customer notification.
- **Stakeholder/NFR alignment:** Supports operational transparency and controllability for store managers (NFR-5 maintainability through traceable steps).
- **Traceability:** FR-14, FR-10; UC-6; US-014; Sprint tasks: Not scheduled in current sprint plan.

## 7) Admin Inventory Update Workflow
- **What it does:** Handles add/edit inventory actions with validation, persistence, and audit logging.
- **Decisions/parallelism:** `Validation passed?` and `Stock quantity zero?` decisions; parallel data save and change-history logging.
- **Stakeholder/NFR alignment:** Supports catalog accuracy, governance, and auditability for operations teams (NFR-5 maintainability, NFR-10 access control logging).
- **Traceability:** FR-11, FR-12, FR-13; UC-3, UC-4; US-011, US-012, US-013; Sprint tasks: Not scheduled in current sprint plan.

## 8) Profile and Address Update Workflow
- **What it does:** Validates and applies profile/address edits and handles post-update verification when account email changes.
- **Decisions/parallelism:** `Input valid?` and `Email changed?` decisions; parallel profile persistence and confirmation notification.
- **Stakeholder/NFR alignment:** Supports data quality and user trust with clear feedback and verification controls (NFR-2 usability, NFR-9 security).
- **Traceability:** FR-15; UC-7; US-015; Sprint tasks: Not scheduled in current sprint plan.
