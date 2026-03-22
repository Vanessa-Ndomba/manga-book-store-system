# System Requirements Document (SRD)
# MangaBookStore – Online Manga Retail System

---

## Executive Summary

This System Requirements Document (SRD) defines the functional and non-functional requirements for the MangaBookStore online retail platform. The system enables customers to browse, search, and purchase manga books while providing administrators with tools to manage inventory, orders, and product listings.

---

## 1. Stakeholder Analysis Summary

| Stakeholder | Role | Key Concerns | Pain Points | Success Metrics |
|---|---|---|---|---|
| **Customers** | End users purchasing manga | Availability, pricing, ease of use, delivery | Limited stock, high shipping costs | Customer satisfaction (4.5+ rating), 25% repeat purchase rate |
| **Store Managers** | Oversee operations | Sales performance, inventory, staffing | Manual tracking, complaint handling | 20% sales growth, 90% employee satisfaction |
| **Suppliers** | Provide merchandise | Timely orders, payment reliability | Unexpected order changes | 95% order accuracy, 100% on-time payment |
| **Developers** | Build/maintain platform | Functionality, performance, UX | Technical issues, integration needs | 99.5% uptime, less than 3 second page load |
| **Marketing Team** | Promote products | Campaign effectiveness, reach | Competition, ROI measurement | 15% conversion rate increase, 50% engagement growth |
| **Investors** | Fund operations | Profitability, sustainability | Market competition | 25% profit margin, 30% annual growth |

---

## 2. Functional Requirements

### 2.1 User Registration and Authentication
**FR-1:** The system shall allow new users to create an account with email and password.  
**Acceptance Criteria:**  
- Valid email format validation required  
- Password minimum 8 characters (uppercase, lowercase, numeric)  
- Confirmation email sent within 5 seconds  
- Duplicate email prevention enforced  

**FR-2:** The system shall authenticate users and maintain secure sessions.  
**Acceptance Criteria:**  
- Email/password login support  
- 30-minute session timeout on inactivity  
- Unauthorized access attempts logged with IP and timestamp  

### 2.2 Manga Catalog Browsing
**FR-3:** The system shall display manga catalog with full details.  
**Acceptance Criteria:**  
- Display: title, author, genre, price, stock status, cover image, rating  
- Pagination support (20 items per page)  
- Stock status: "In Stock", "Out of Stock", "Pre-Order"  

**FR-4:** The system shall enable category/genre filtering.  
**Acceptance Criteria:**  
- Categories: Action, Romance, Horror, Slice of Life, Fantasy, Sci-Fi  
- Multi-category simultaneous filtering  
- Results returned within 2 seconds  

### 2.3 Search and Discovery
**FR-5:** The system shall provide comprehensive search functionality.  
**Acceptance Criteria:**  
- Search by title, author, ISBN  
- Results within 2 seconds for queries with up to 1,000 results  
- Case-insensitive search  
- Partial title matching (e.g., "One" finds "One Piece")  

**FR-6:** The system shall display trending/recommended content.  
**Acceptance Criteria:**  
- Top 10 best-selling titles on homepage  
- Top 10 highest-rated titles on homepage  
- Updated daily  

### 2.4 Shopping Cart Management
**FR-7:** The system shall allow adding items to shopping cart.  
**Acceptance Criteria:**  
- Add with quantity selection  
- Stock validation preventing over-ordering  
- Real-time total price calculation  

**FR-8:** The system shall support cart modifications.  
**Acceptance Criteria:**  
- Update quantity (minimum 1)  
- Remove individual items  
- Instant total recalculation  
- 24-hour cart persistence  

### 2.5 Order Placement and Management
**FR-9:** The system shall facilitate order placement.  
**Acceptance Criteria:**  
- Delivery address requirement  
- Order confirmation email within 5 seconds  
- Unique order ID generation and display  
- Payment method selection (simulated)  

**FR-10:** The system shall provide order history access.  
**Acceptance Criteria:**  
- View all past orders with ID, date, items, status  
- Status display: "Processing", "Shipped", "Delivered", "Cancelled"  
- Accessible from user profile  

### 2.6 Admin Inventory Management
**FR-11:** The system shall allow adding new manga titles.  
**Acceptance Criteria:**  
- Input fields: title, author, ISBN, genre, price, stock quantity  
- All fields required with validation  
- Cover image upload (JPEG, PNG)  

**FR-12:** The system shall support manga information updates.  
**Acceptance Criteria:**  
- Modify all fields except ISBN  
- Catalog reflects updates within 1 minute  
- Change history logging  

**FR-13:** The system shall allow removing manga listings.  
**Acceptance Criteria:**  
- Deletion with confirmation prompt  
- Deleted items removed from searches  
- Deletion logged with admin ID and timestamp  

### 2.7 Admin Order Management
**FR-14:** The system shall enable order management for admins.  
**Acceptance Criteria:**  
- View all orders with customer info and items  
- Update order status  
- Search by order ID, customer name, date range  
- Search results within 2 seconds  

### 2.8 User Profile Management
**FR-15:** The system shall support user profile management.  
**Acceptance Criteria:**  
- Edit name, email, phone number  
- Add/update delivery addresses  
- Changes saved and confirmed  

---

## 3. Non-Functional Requirements

### 3.1 Usability - WCAG 2.1 Compliance
**NFR-1:** Interface shall comply with WCAG 2.1 Level AA standards.  
- Text contrast ratio greater than or equal to 4.5:1 for normal text  
- All images require alt-text descriptions  
- Full keyboard navigation support  
- Font size adjustable 12px-20px  

**NFR-2:** Intuitive user interface design.  
- Checkout completion in less than or equal to 5 steps  
- Clear button labels throughout  
- Specific, actionable error messages  
- Help documentation accessible from all pages  

### 3.2 Deployability
**NFR-3:** Multi-OS server deployment support.  
- Windows and Linux server compatibility  
- Docker container standardization  
- Deployment procedure executable in less than 30 minutes  

**NFR-4:** Multiple database system support.  
- PostgreSQL 12 and above and MySQL 5.7 and above compatibility  
- Version-controlled migration scripts  

### 3.3 Maintainability
**NFR-5:** Comprehensive API documentation required.  
- All endpoints documented with examples  
- Auto-generated documentation from code comments  
- Updated with each API change  

**NFR-6:** Code quality standards enforcement.  
- Industry-standard style guide compliance  
- Greater than or equal to 80 percent unit test coverage  
- Automated testing before merge  

### 3.4 Scalability
**NFR-7:** Support 1,000 concurrent users during peak hours.  
- Database connection pooling implemented  
- Redis caching reduces DB queries by 70 percent  
- No degradation at 1,000 simultaneous connections  

**NFR-8:** Horizontal scaling capability.  
- Stateless application architecture  
- Load balancing across instances  
- Database replication for HA  

### 3.5 Security
**NFR-9:** AES-256 encryption for all user data.  
- Encrypted data at rest  
- TLS 1.2 and above for data transmission  
- Secure key management system  

**NFR-10:** Role-Based Access Control (RBAC) implementation.  
- Roles: Customer, Admin, Moderator  
- Admin functions restricted to authenticated admins  
- All privileged actions logged with user ID and timestamp  

**NFR-11:** OWASP Top 10 vulnerability prevention.  
- Parameterized queries for SQL injection prevention  
- Input validation for XSS prevention  
- CSRF token protection  
- Rate limiting: 100 requests per minute per IP  

### 3.6 Performance
**NFR-12:** Search results load within 2 seconds.  
- Database optimization with proper indexing  
- Repeated search caching  
- Pagination prevents large result set loading  

**NFR-13:** Page load time less than or equal to 3 seconds.  
- Static asset caching and minification  
- Limited essential data queries  
- Gzip compression on API responses  

**NFR-14:** 99.5 percent system uptime.  
- Automated backups every 6 hours  
- Disaster recovery within 1 hour  
- Health monitoring every 5 minutes  

---

## 4. Traceability Matrix

| Requirement ID | Stakeholder | Requirement | Type |
|---|---|---|---|
| FR-1, FR-2 | Customers, Developers | User authentication | Functional |
| FR-3, FR-4, FR-5, FR-6 | Customers, Marketing | Catalog and search | Functional |
| FR-7, FR-8, FR-9, FR-10 | Customers | Shopping and ordering | Functional |
| FR-11, FR-12, FR-13, FR-14 | Store Managers, Suppliers | Inventory and orders | Functional |
| FR-15 | Customers | Profile management | Functional |
| NFR-1, NFR-2 | Customers, Developers | Usability | Non-Functional |
| NFR-3, NFR-4 | Developers | Deployability | Non-Functional |
| NFR-5, NFR-6 | Developers | Maintainability | Non-Functional |
| NFR-7, NFR-8 | Investors, Developers | Scalability | Non-Functional |
| NFR-9, NFR-10, NFR-11 | Customers, Investors | Security | Non-Functional |
| NFR-12, NFR-13, NFR-14 | Customers, Developers | Performance | Non-Functional |

---

## 5. Constraints and Assumptions

**Constraints:**
1. Payment processing and shipping integration are simulated
2. Web-based application for Chrome, Firefox, Safari, Edge browsers
3. Initial launch supports English only
4. User data retained for 2 years post-login
5. Phase 1 (MVP) completion target: 4 months

**Assumptions:**
1. Reliable internet connectivity for users
2. Database availability for order processing
3. Email service availability for confirmations
4. Third-party payment gateway API access (simulated)

---

## Document Version Control
- **Version:** 1.0
- **Date:** March 22, 2026
- **Author:** Requirements Engineering Team
- **Last Updated:** March 22, 2026
- **Status:** Approved