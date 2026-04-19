# Reflection

## 1) Challenge: Choosing the Right Granularity
The main challenge was balancing completeness and readability. If each exception path is modeled explicitly, diagrams become difficult to scan. I handled this by:
- Keeping core business lifecycle states in each state diagram.
- Capturing important edge conditions with guards (for example, stock, payment, and session timeout checks).
- Moving rationale and interpretation into the explanation files so diagrams stay readable.

## 2) Aligning Diagrams with Agile User Stories
User stories and sprint tasks focus on deliverable slices, while state/activity diagrams model behavior across a broader lifecycle. Alignment was improved by:
- Mapping each diagram to FR IDs first, then to US IDs and sprint tasks.
- Explicitly marking workflows that are valid requirements but are not yet represented in the current sprint plan.
- Reusing the same naming vocabulary used in prior assignment documents to reduce ambiguity.

## 3) State Diagrams vs Activity Diagrams
- **State diagrams** were best for lifecycle-centric entities (order, payment, inventory, shipment) where event-triggered transitions and guards drive behavior over time.
- **Activity diagrams** were best for role-based workflow sequencing (user, system, admin, payment gateway), decision paths, and parallel actions.

In short, state diagrams clarified *how objects evolve*, while activity diagrams clarified *how work gets done* across actors and system responsibilities.