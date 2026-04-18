# Assignment 8 - UML State Transition Diagrams (Mermaid)

This document models the lifecycle of **8 critical MangaBookStore objects**.  
Each section includes a Mermaid state transition diagram and a brief mapping to Assignment 4 functional requirements and Assignment 6 user stories/sprint work.

---

## 1) User Account

```mermaid
stateDiagram-v2
    [*] --> Unregistered
    Unregistered --> Registered: submitRegistration [validEmail && strongPassword && uniqueEmail]
    Unregistered --> RegistrationRejected: submitRegistration [invalidInput || duplicateEmail]
    RegistrationRejected --> Unregistered: correctAndResubmit

    Registered --> Active: verifyEmail
    Active --> Locked: failedLoginAttempts >= 5
    Locked --> Active: passwordResetSuccess

    Active --> Suspended: adminSuspendsAccount
    Suspended --> Active: adminReactivatesAccount

    Active --> Deactivated: userRequestsDeletion
    Deactivated --> [*]
```

**Explanation:** Captures onboarding, activation, security lockout, and admin moderation transitions.  
**Traceability:** FR-1, FR-2, FR-15; US-001, US-002, US-015.

---

## 2) Book Inventory Item

```mermaid
stateDiagram-v2
    [*] --> InStock
    InStock --> Reserved: addToCheckout [stock > 0]
    Reserved --> InStock: reservationReleased [checkoutExpired]
    Reserved --> Allocated: orderConfirmed

    InStock --> LowStock: stockDrops [qty <= reorderThreshold && qty > 0]
    LowStock --> InStock: replenished [qty > reorderThreshold]
    InStock --> OutOfStock: stockDepleted [qty == 0]
    LowStock --> OutOfStock: stockDepleted [qty == 0]

    OutOfStock --> Restocking: purchaseOrderPlaced
    Restocking --> InStock: supplierDeliveryReceived [qualityCheckPassed]
    Restocking --> Quarantined: supplierDeliveryReceived [qualityCheckFailed]
    Quarantined --> Restocking: reorderApproved

    InStock --> Discontinued: adminDiscontinuesSKU
    LowStock --> Discontinued: adminDiscontinuesSKU
    OutOfStock --> Discontinued: adminDiscontinuesSKU
    Discontinued --> [*]
```

**Explanation:** Shows real-time stock behavior tied to checkout reservations and admin inventory controls.  
**Traceability:** FR-7, FR-11, FR-12, FR-13, FR-14; US-007, US-011, US-012, US-013, US-014.

---

## 3) Shopping Cart

```mermaid
stateDiagram-v2
    [*] --> Empty
    Empty --> Active: addItem [stockAvailable]
    Empty --> Empty: addItem [stockUnavailable]

    Active --> Updated: updateQtyOrRemoveItem
    Updated --> Active: totalsRecalculated

    Active --> CheckedOut: submitCheckout [hasItems && hasDeliveryAddress]
    Updated --> CheckedOut: submitCheckout [hasItems && hasDeliveryAddress]

    Active --> Abandoned: inactivityTimeout [24h]
    Updated --> Abandoned: inactivityTimeout [24h]
    Abandoned --> Active: userReturnsAndEdits

    Active --> Empty: removeAllItems
    Updated --> Empty: removeAllItems
    CheckedOut --> ConvertedToOrder: orderIdGenerated
    ConvertedToOrder --> [*]
```

**Explanation:** Models cart persistence, validation guards, and conversion to order.  
**Traceability:** FR-7, FR-8, FR-9; US-007, US-008, US-009.

---

## 4) Order

```mermaid
stateDiagram-v2
    [*] --> Created
    Created --> PaymentPending: checkoutSubmitted
    PaymentPending --> Confirmed: paymentAuthorized [paymentValid]
    PaymentPending --> PaymentFailed: paymentDeclined [paymentInvalid]
    PaymentFailed --> PaymentPending: retryPayment

    Confirmed --> Processing: inventoryAllocated
    Processing --> Packed: pickPackCompleted
    Packed --> Shipped: carrierPickupConfirmed
    Shipped --> Delivered: proofOfDeliveryReceived

    Created --> Cancelled: userCancels [beforeCapture]
    PaymentPending --> Cancelled: userCancels [beforeCapture]
    Confirmed --> Cancelled: adminCancels [fraudCheckFailed]
    Processing --> Cancelled: adminCancels [stockAllocationFailed]

    Delivered --> Completed: returnWindowExpired
    Cancelled --> Refunded: refundIssued
    Refunded --> [*]
    Completed --> [*]
```

**Explanation:** Covers full order execution including cancellation and refund consequences.  
**Traceability:** FR-9, FR-10, FR-14; US-009, US-010, US-014.

---

## 5) Payment Transaction

```mermaid
stateDiagram-v2
    [*] --> Initiated
    Initiated --> Authorized: gatewayAuthorizationSuccess
    Initiated --> AuthorizationFailed: gatewayAuthorizationFailed
    AuthorizationFailed --> Initiated: retryAuthorization

    Authorized --> Captured: capturePayment [orderConfirmed]
    Authorized --> Voided: voidAuthorization [orderCancelledBeforeCapture]

    Captured --> Settled: settlementCompleted
    Settled --> PartiallyRefunded: partialRefundRequested [amount < capturedAmount]
    Settled --> Refunded: fullRefundRequested [amount == capturedAmount]
    PartiallyRefunded --> Refunded: remainingAmountRefunded

    Voided --> [*]
    Refunded --> [*]
```

**Explanation:** Represents payment gateway outcomes, settlement, and refund branches.  
**Traceability:** FR-9, FR-14; US-009, US-014.

---

## 6) Shipment

```mermaid
stateDiagram-v2
    [*] --> PendingDispatch
    PendingDispatch --> LabelCreated: shippingLabelGenerated
    LabelCreated --> PickedUp: carrierPickupScan
    PickedUp --> InTransit: departedOriginFacility
    InTransit --> OutForDelivery: arrivedDestinationHub
    OutForDelivery --> Delivered: proofOfDeliveryCaptured

    InTransit --> Exception: delayOrDamageReported
    OutForDelivery --> Exception: addressIssueReported
    Exception --> InTransit: issueResolvedAndRerouted
    Exception --> Returned: returnToSenderApproved

    Delivered --> Closed: deliveryAccepted
    Returned --> Closed: returnReceivedWarehouse
    Closed --> [*]
```

**Explanation:** Models shipping progression and exception/return handling.  
**Traceability:** FR-10, FR-14; US-010, US-014.

---

## 7) Return/Refund Request

```mermaid
stateDiagram-v2
    [*] --> Requested
    Requested --> UnderReview: returnEligibilityCheckStarted
    UnderReview --> Approved: returnEligible [withinWindow && conditionAcceptable]
    UnderReview --> Rejected: returnIneligible [outsideWindow || conditionNotAcceptable]

    Approved --> AwaitingItem: returnLabelIssued
    AwaitingItem --> ItemReceived: warehouseReceivesReturn
    ItemReceived --> RefundProcessing: inspectionPassed
    ItemReceived --> Escalated: inspectionDisputeFound

    RefundProcessing --> Refunded: refundCompleted
    Escalated --> RefundProcessing: managerApprovesResolution
    Rejected --> Closed: notifyRejection
    Refunded --> Closed
    Closed --> [*]
```

**Explanation:** Defines return request review, inspection, and refund completion lifecycle.  
**Traceability:** FR-10, FR-14; US-010, US-014.

---

## 8) Manga Listing

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> PendingReview: adminSubmitsListing
    PendingReview --> Published: reviewApproved [requiredFieldsComplete]
    PendingReview --> Draft: reviewRejected [validationIssues]

    Published --> LowStockDisplay: stockDrops [qty <= reorderThreshold && qty > 0]
    LowStockDisplay --> Published: restocked [qty > reorderThreshold]
    Published --> OutOfStockDisplay: stockDepleted [qty == 0]
    LowStockDisplay --> OutOfStockDisplay: stockDepleted [qty == 0]
    OutOfStockDisplay --> Published: replenished [qty > reorderThreshold]

    Published --> Archived: adminArchivesListing
    LowStockDisplay --> Archived: adminArchivesListing
    OutOfStockDisplay --> Archived: adminArchivesListing
    Archived --> [*]
```

**Explanation:** Shows catalog publication and stock-aware visibility states used by browse/search workflows.  
**Traceability:** FR-3, FR-4, FR-5, FR-11, FR-12, FR-13; US-003, US-004, US-005, US-011, US-012, US-013.
