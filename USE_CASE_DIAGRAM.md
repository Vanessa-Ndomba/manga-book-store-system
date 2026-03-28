graph TB
    Customer["🧑 Customer"]
    GuestUser["👤 Guest User"]
    RegisteredCustomer["👥 Registered Customer"]
    Admin["🔐 Admin"]
    StoreManager["📊 Store Manager"]
    Supplier["📦 Supplier"]
    SystemAdmin["⚙️ System Admin"]
    PaymentGateway["💳 Payment Gateway"]
    EmailService["📧 Email Service"]
    InventoryDB["💾 Inventory DB"]
    
    %% Use Cases
    RegisterAccount["Register Account"]
    Login["Login/Authentication"]
    BrowseCatalog["Browse Manga Catalog"]
    SearchManga["Search Manga by Title/Author/ISBN"]
    FilterByGenre["Filter by Genre/Category"]
    ViewMangaDetails["View Manga Details"]
    AddToCart["Add Items to Shopping Cart"]
    ModifyCart["Modify Cart Quantity"]
    RemoveFromCart["Remove Items from Cart"]
    Checkout["Checkout Process"]
    PlaceOrder["Place Order"]
    ViewOrderHistory["View Order History"]
    TrackOrder["Track Order Status"]
    ManageProfile["Manage User Profile"]
    
    AddMangaTitle["Add New Manga Title"]
    UpdateMangaInfo["Update Manga Information"]
    RemoveMangaListing["Remove Manga Listing"]
    ViewAllOrders["View All Customer Orders"]
    UpdateOrderStatus["Update Order Status"]
    ViewInventory["View Inventory Levels"]
    GenerateReports["Generate Sales Reports"]
    ManageUsers["Manage User Accounts"]
    
    ProcessPayment["Process Payment"]
    SendConfirmationEmail["Send Confirmation Email"]
    UpdateInventory["Update Inventory"]
    ValidateStock["Validate Stock Availability"]
    
    %% Actor Relationships
    GuestUser -->|inherits| Customer
    RegisteredCustomer -->|inherits| Customer
    StoreManager -->|inherits| Admin
    SystemAdmin -->|inherits| Admin
    
    %% Customer Use Cases
    Customer -->|uses| BrowseCatalog
    Customer -->|uses| SearchManga
    Customer -->|uses| FilterByGenre
    Customer -->|uses| ViewMangaDetails
    
    GuestUser -->|uses| RegisterAccount
    GuestUser -->|uses| Login
    
    RegisteredCustomer -->|uses| AddToCart
    RegisteredCustomer -->|uses| ModifyCart
    RegisteredCustomer -->|uses| RemoveFromCart
    RegisteredCustomer -->|uses| Checkout
    RegisteredCustomer -->|uses| PlaceOrder
    RegisteredCustomer -->|uses| ViewOrderHistory
    RegisteredCustomer -->|uses| TrackOrder
    RegisteredCustomer -->|uses| ManageProfile
    
    %% Admin Use Cases
    Admin -->|uses| AddMangaTitle
    Admin -->|uses| UpdateMangaInfo
    Admin -->|uses| RemoveMangaListing
    Admin -->|uses| ViewAllOrders
    Admin -->|uses| UpdateOrderStatus
    Admin -->|uses| ViewInventory
    
    StoreManager -->|uses| GenerateReports
    SystemAdmin -->|uses| ManageUsers
    
    Supplier -->|uses| ViewInventory
    
    %% Include Relationships (dependencies)
    PlaceOrder -.->|include| Checkout
    Checkout -.->|include| ProcessPayment
    Checkout -.->|include| ValidateStock
    PlaceOrder -.->|include| SendConfirmationEmail
    PlaceOrder -.->|include| UpdateInventory
    AddToCart -.->|include| ValidateStock
    
    %% System Interactions
    ProcessPayment -->|interacts with| PaymentGateway
    SendConfirmationEmail -->|interacts with| EmailService
    UpdateInventory -->|interacts with| InventoryDB
    ValidateStock -->|interacts with| InventoryDB
    ViewInventory -->|interacts with| InventoryDB
    
    style Customer fill:#e1f5ff
    style GuestUser fill:#b3e5fc
    style RegisteredCustomer fill:#81d4fa
    style Admin fill:#ffe0b2
    style StoreManager fill:#ffcc80
    style SystemAdmin fill:#ffb74d
    style Supplier fill:#c8e6c9
    style PaymentGateway fill:#f8bbd0
    style EmailService fill:#f8bbd0
    style InventoryDB fill:#f8bbd0
