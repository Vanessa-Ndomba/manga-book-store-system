# User Account State Diagram

```mermaid
stateDiagram-v2
    [*] --> Guest
    Guest --> PendingVerification: Register account
    PendingVerification --> Active: Verify email [tokenValid]
    PendingVerification --> Guest: Verification expired [tokenExpired]
    Active --> LoggedIn: Login [credentialsValid]
    LoggedIn --> Active: Logout
    Active --> Locked: Too many failed logins [attempts >= 5]
    Locked --> Active: Unlock account [adminApproved]
    Active --> Suspended: Suspend user [policyViolation]
    Suspended --> Active: Reinstate [adminApproved]
    Active --> Deleted: User requests deletion
    Deleted --> [*]
```

## Explanation
- **Key states/transitions:** Registration and verification control entry into `Active`; security events move accounts to `Locked` or `Suspended` with guarded recovery.
- **Use case mapping:** Register Account, Login/Authentication, Manage User Accounts, Manage User Profile.
- **Placeholder traceability:** FR-104 (register user), FR-105 (authenticate user), FR-106 (account administration); US-102; ST-102.
