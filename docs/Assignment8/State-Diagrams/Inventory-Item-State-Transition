stateDiagram-v2
    [*] --> InStock
    InStock --> Reserved: customer adds item during checkout
    Reserved --> InStock: checkout cancelled / cart expires
    Reserved --> Sold: payment confirmed
    Sold --> Returned: customer requests return
    Returned --> InStock: item passes inspection
    Returned --> Damaged: item fails inspection
    InStock --> OutOfStock: quantity reaches zero
    OutOfStock --> InStock: stock replenished
