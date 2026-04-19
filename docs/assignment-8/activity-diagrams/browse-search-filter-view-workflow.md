# Browse/Search/Filter/View Manga Workflow Activity Diagram

```mermaid
flowchart TD
    Start([Start]) --> U1

    subgraph Customer
      U1[Open catalog]
      U2[Enter keyword or select genre]
      U3[Select manga title]
    end

    subgraph System
      F1{{Fork}}
      S1[Query catalog by keyword]
      S2[Apply genre/category filters]
      J1{{Join}}
      D1{Any results?}
      S3[Render results list]
      S4[Show no-results guidance]
      S5[Load manga details]
    end

    subgraph Inventory_DB[Inventory DB]
      I1[Fetch stock and pricing snapshot]
    end

    U1 --> U2 --> F1
    F1 --> S1 --> J1
    F1 --> S2 --> J1
    J1 --> D1
    D1 -- No --> S4 --> End([End])
    D1 -- Yes --> S3 --> U3 --> S5 --> I1 --> End
```

## Explanation
- **Stakeholder concerns:** Shoppers expect responsive discovery and accurate details before purchase.
- **Decisions/parallelism:** Search and filter processing run in parallel; decision branch handles empty results gracefully.
- **Use case and placeholder mapping:** Browse Manga Catalog, Search Manga by Title/Author/ISBN, Filter by Genre/Category, View Manga Details; FR-123, FR-124; US-203; ST-203.
