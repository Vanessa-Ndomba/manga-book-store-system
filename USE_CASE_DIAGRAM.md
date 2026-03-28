```mermaid
%%{ init : { "theme" : "default" } }%%

usecaseDiagram
    actor Customer as C
    actor Admin as A
    actor Retailer as R
    actor DeliveryPerson as D
    actor PaymentProcessor as P
    actor InventorySystem as I
    actor ExternalAPI as API

    C --> (Browse Manga)
    C --> (Purchase Manga)
    C --> (Track Order)
    C --> (Review Manga)
    C --> (Update Profile)
    R --> (Manage Inventory)
    R --> (Manage Promotions)
    A --> (Manage Users)
    A --> (Generate Reports)
    P --> (Process Payment)
    I --> (Synchronize Inventory)
    API --> (Fetch Manga Details)
```