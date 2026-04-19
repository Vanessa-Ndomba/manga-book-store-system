# User Registration Workflow Activity Diagram

```mermaid
flowchart TD
    Start([Start]) --> U1

    subgraph Guest_User[Guest User]
      U1[Open registration page]
      U2[Enter profile and credentials]
      U3[Submit registration]
      U4[Open verification email]
    end

    subgraph System
      S1[Validate form and uniqueness]
      D1{Valid input?}
      S2[Create pending account]
      D2{Account created?}
      F1{{Fork}}
      S3[Store account record]
      S4[Generate verification token]
      J1{{Join}}
      S5[Send verification email]
      D3{Token valid?}
      S6[Activate account]
      S7[Show error and allow retry]
    end

    U1 --> U2 --> U3 --> S1 --> D1
    D1 -- No --> S7 --> U2
    D1 -- Yes --> S2 --> D2
    D2 -- No --> S7 --> U2
    D2 -- Yes --> F1
    F1 --> S3 --> J1
    F1 --> S4 --> J1
    J1 --> S5 --> U4 --> D3
    D3 -- Yes --> S6 --> End([End])
    D3 -- No --> S7
```

## Explanation
- **Stakeholder concerns:** Users need reliable onboarding; admins need verified identities before account activation.
- **Decisions/parallelism:** Validation and token checks handle quality/security gates. Parallel account persistence + token generation reduces processing time, while email is sent only after account creation succeeds.
- **Use case and placeholder mapping:** Register Account, Login/Authentication; FR-104, FR-105; US-201; ST-201.
