# Assignment 8 Reflection

## 1) Challenges in Choosing Granularity

The biggest challenge was deciding how detailed each state and action should be.  
If diagrams are too high-level, important business rules (for example stock guards, payment outcomes, and return eligibility) disappear. If diagrams are too detailed, readability suffers and stakeholder discussion becomes harder.

For state models, I kept business-significant states only (for example `PaymentPending`, `Authorized`, `Refunded`) and used transition events/guards to keep control logic explicit without over-fragmenting states.

For activity models, I used concise actions and focused on key decision points plus parallel work that matters to operations (notifications, logging, persistence, inventory updates).

## 2) Challenges Aligning with Agile User Stories

Assignment 6 artifacts include strong user stories but limited sprint task decomposition outside early stories (search, cart, registration).  
To maintain traceability quality, I mapped every diagram to user stories first (stable IDs like `US-009`) and then mapped sprint tasks where concrete task lines existed in `AGILE_PLANNING_DOCUMENT.md`.

Where Assignment 6 had no explicit task breakdown (for example payment, fulfillment, returns), I marked mappings as inferred/not explicitly decomposed instead of inventing fake sprint tasks.

## 3) State Diagrams vs Activity Diagrams

State diagrams and activity diagrams supported different analysis goals:

- **State diagrams (object behavior):** Best for lifecycle correctness of one domain object (for example order cancellation windows, payment authorization/capture/refund path, shipment exceptions).
- **Activity diagrams (process flow):** Best for cross-actor workflow coordination (user, system, admin, carrier, gateway) and for showing decisions and parallel actions.

In practice, the two views complement each other:
- State diagrams answer **“what condition is this object in now?”**
- Activity diagrams answer **“what sequence of work happens across roles to move work forward?”**

Using both made requirement coverage clearer and highlighted where the process and lifecycle views need to stay synchronized.
