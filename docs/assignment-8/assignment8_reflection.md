# Assignment 8 Reflection

## Choosing granularity: detail vs readability
A main challenge was choosing enough lifecycle/workflow detail to show business rules without making each diagram too dense to read. I used bounded state/action sets and grouped related logic (for example, stock validation and payment checks) into clear transitions and decisions. Guard conditions were used only where they clarify constraints.

## Aligning diagrams with Agile user stories
Because Assignment 4 FR artifacts were not available in this repository, I used placeholder FR/US/ST IDs tied directly to the provided use cases. This keeps the diagrams sprint-ready while allowing easy remapping to official backlog/story IDs later.

## State diagrams vs activity diagrams
State diagrams describe **how one object changes over time** (e.g., order status from pending to delivered). Activity diagrams describe **how work moves across actors** (e.g., customer, system, payment gateway, email service) including decisions and parallel actions. Together, they provide complementary views: object lifecycle integrity plus end-to-end operational flow.
