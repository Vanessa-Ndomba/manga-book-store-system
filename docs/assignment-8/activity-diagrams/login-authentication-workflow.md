# Login and Authentication Workflow Activity Diagram

```mermaid
flowchart TD
    Start([Start]) --> U1

    subgraph Registered_Customer[Registered Customer]
      U1[Open login page]
      U2[Enter email and password]
      U3[Submit credentials]
      U4[Retry login]
    end

    subgraph System
      S1[Validate credentials]
      D1{Credentials valid?}
      D2{Account active?}
      F1{{Fork}}
      S2[Create session token]
      S3[Update last-login metadata]
      J1{{Join}}
      S4[Return dashboard]
      S5[Increment failed-attempt count]
      D3{Attempts >= 5?}
      S6[Lock account]
    end

    U1 --> U2 --> U3 --> S1 --> D1
    D1 -- No --> S5 --> D3
    D3 -- Yes --> S6 --> End([End])
    D3 -- No --> U4 --> U2
    D1 -- Yes --> D2
    D2 -- No --> End
    D2 -- Yes --> F1
    F1 --> S2 --> J1
    F1 --> S3 --> J1
    J1 --> S4 --> End
```

## Explanation
- **Stakeholder concerns:** Customers need quick login; security stakeholders need lockout controls and session integrity.
- **Decisions/parallelism:** Credential and account checks are decision points; token creation and audit updates run in parallel.
- **Use case and placeholder mapping:** Login/Authentication; FR-105, FR-106; US-202; ST-202.
