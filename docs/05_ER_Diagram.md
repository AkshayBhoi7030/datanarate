# DataNarrate - ER Diagram

## Part 1: Application Database (DataNarrate Core)

```
┌─────────────────────────────────────────────────────────────────┐
│                            users                                │
├─────────────────────────────────────────────────────────────────┤
│ PK user_id          UUID                                       │
│    email            VARCHAR(255)  UNIQUE                       │
│    password_hash    VARCHAR(255)                               │
│    first_name       VARCHAR(100)                               │
│    last_name        VARCHAR(100)                               │
│    role             VARCHAR(50)                                │
│    is_active        BOOLEAN                                    │
│    created_at       TIMESTAMP                                  │
│    updated_at       TIMESTAMP                                  │
│    last_login_at    TIMESTAMP                                  │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   │ 1
                   │
                   │ N
┌──────────────────▼──────────────────┐     ┌──────────────────────┐
│   database_connections              │     │    audit_logs        │
├─────────────────────────────────────┤     ├──────────────────────┤
│ PK connection_id    UUID            │     │ PK log_id      UUID   │
│ FK user_id          UUID            │◄────│ FK user_id     UUID   │
│    connection_name  VARCHAR(100)    │     │    action       VARCHAR│
│    db_type          VARCHAR(50)     │     │    resource_type     │
│    host             VARCHAR(255)    │     │    resource_id       │
│    port             INTEGER         │     │    action_details    │
│    database_name    VARCHAR(255)    │     │    ip_address        │
│    username         VARCHAR(255)    │     │    user_agent        │
│    password_encrypted TEXT          │     │    created_at        │
│    ssl_required     BOOLEAN         │     └──────────────────────┘
│    is_default       BOOLEAN         │
│    created_at       TIMESTAMP       │
│    updated_at       TIMESTAMP       │
│    last_connected_at TIMESTAMP      │
└──────────┬──────────────────────────┘
           │
           │ 1
           │
           │ N
    ┌──────▼──────────────┐
    │   query_history     │
    ├─────────────────────┤
    │ PK history_id    UUID│
    │ FK user_id       UUID│
    │ FK connection_id UUID│
    │    natural_language_query TEXT│
    │    generated_sql   TEXT│
    │    execution_status VARCHAR│
    │    execution_time_ms INTEGER│
    │    row_count       INTEGER│
    │    error_message   TEXT│
    │    results_summary JSONB│
    │    insights        TEXT│
    │    chart_config    JSONB│
    │    created_at      TIMESTAMP│
    └─────────────────────┘

┌─────────────────────────────────┐
│    saved_queries                │
├─────────────────────────────────┤
│ PK saved_query_id    UUID       │
│ FK user_id           UUID       │
│ FK connection_id     UUID       │
│    query_name        VARCHAR(255)│
│    description       TEXT       │
│    natural_language_query TEXT  │
│    generated_sql     TEXT       │
│    tags              TEXT[]     │
│    is_public         BOOLEAN    │
│    created_at        TIMESTAMP  │
│    updated_at        TIMESTAMP  │
└─────────────────────────────────┘
```

## Part 2: Sample E-Commerce Dataset

```
┌──────────────────┐
│   categories     │
├──────────────────┤
│ PK category_id   │
│    category_name │
│    description   │
│    created_at    │
└────────┬─────────┘
         │ 1
         │
         │ N
┌────────▼──────────┐
│    products       │
├───────────────────┤
│ PK product_id     │
│ FK category_id    │
│    product_name   │
│    description    │
│    price          │
│    stock_quantity │
│    sku            │
│    is_active      │
│    created_at     │
│    updated_at     │
└────────┬──────────┘
         │
         │ 1
         │
         │ N
┌────────▼──────────┐     ┌──────────────────┐
│   order_items     │     │    customers     │
├───────────────────┤     ├──────────────────┤
│ PK order_item_id  │     │ PK customer_id   │
│ FK order_id       │◄────│    first_name    │
│ FK product_id     │     │    last_name     │
│    quantity       │     │    email         │
│    unit_price     │     │    phone         │
│    subtotal       │     │    address       │
└───────────────────┘     │    city          │
         ▲                │    state         │
         │                │    country       │
         │ 1              │    postal_code   │
         │                │    created_at    │
         │ N              │    updated_at    │
┌────────┴──────────┐     └────────┬─────────┘
│     orders        │              │ 1
├───────────────────┤              │
│ PK order_id       │              │ N
│ FK customer_id    │◄─────────────┘
│    order_date     │
│    total_amount   │
│    status         │
│    shipping_addr  │
│    created_at     │
│    updated_at     │
└────────┬──────────┘
         │
         │ 1
         │
         │ N
┌────────▼──────────┐
│    payments       │
├───────────────────┤
│ PK payment_id     │
│ FK order_id       │
│    payment_date   │
│    amount         │
│    payment_method │
│    payment_status │
│    transaction_id │
│    created_at     │
└───────────────────┘
```

## Relationship Legend

| Symbol | Meaning |
|--------|---------|
| PK | Primary Key |
| FK | Foreign Key |
| 1 ──── N | One-to-Many relationship |
| ◄────── | Relationship direction |
