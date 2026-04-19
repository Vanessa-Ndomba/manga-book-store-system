# Admin Report State Diagram

```mermaid
stateDiagram-v2
    [*] --> Requested
    Requested --> Queued: Submit report job
    Queued --> Generating: Worker picks job
    Generating --> Generated: Build succeeds [dataAvailable]
    Generating --> Failed: Build fails [queryError]
    Failed --> Queued: Retry generation
    Generated --> Published: Publish to dashboard [managerApproved]
    Generated --> Archived: Archive without publish
    Published --> Archived: Archive report version
    Archived --> [*]
```

## Explanation
- **Key states/transitions:** Reporting moves through queueing, generation, quality gate, and publication/archival.
- **Use case mapping:** Generate Sales Reports, View Inventory Levels.
- **Placeholder traceability:** FR-121 (generate reports), FR-122 (publish report outputs); US-108; ST-108.
