# User Account State Diagram

```mermaid
stateDiagram-v2
    [*] --> Unregistered
    Unregistered --> Registered: Submit registration [validEmail && strongPassword && uniqueEmail]
    Unregistered --> RegistrationRejected: Submit registration [invalidData]
    RegistrationRejected --> Unregistered: Correct details

    Registered --> Active: Verify email
    Registered --> Suspended: Admin lock account

    Active --> Locked: Multiple failed login attempts
    Locked --> Active: Password reset successful

    Active --> Suspended: Admin suspend account
    Suspended --> Active: Admin reactivate

    Active --> Deactivated: User requests account deletion
    Deactivated --> [*]
```
