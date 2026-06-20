# DataNarrate - API Design Document

## Base URL
`https://api.datanarrate.com/v1`

---

## 1. GET /health

### Purpose
Health check endpoint to verify service availability.

### Request
- Method: GET
- Headers: None required
- Body: None

### Response (200 OK)
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-06-19T00:00:00Z"
}
```

### Error Cases
- N/A - always returns 200 if service is running

---

## 2. GET /schema

### Purpose
Retrieve database schema information for a specific connection.

### Request
- Method: GET
- Headers:
  - `Authorization: Bearer <jwt_token>`
- Query Parameters:
  - `connection_id` (string, required): UUID of the database connection

### Response (200 OK)
```json
{
  "connection_id": "550e8400-e29b-41d4-a716-446655440000",
  "tables": [
    {
      "name": "customers",
      "columns": [
        {
          "name": "customer_id",
          "data_type": "integer",
          "is_nullable": false,
          "is_primary_key": true
        },
        {
          "name": "email",
          "data_type": "varchar",
          "is_nullable": false,
          "is_primary_key": false
        }
      ],
      "row_count": 1250
    }
  ],
  "cached_at": "2026-06-19T00:00:00Z"
}
```

### Error Cases
| Status | Error | Description |
|--------|-------|-------------|
| 400 | Bad Request | Missing or invalid connection_id |
| 401 | Unauthorized | Missing or invalid JWT token |
| 403 | Forbidden | User doesn't have access to this connection |
| 404 | Not Found | Connection doesn't exist |
| 500 | Internal Server Error | Failed to retrieve schema |

---

## 3. POST /query

### Purpose
Execute a natural language query against a database.

### Request
- Method: POST
- Headers:
  - `Authorization: Bearer <jwt_token>`
  - `Content-Type: application/json`
- Body:
```json
{
  "connection_id": "550e8400-e29b-41d4-a716-446655440000",
  "natural_language_query": "Show top 10 customers by revenue",
  "include_charts": true,
  "include_insights": true
}
```

### Response (200 OK)
```json
{
  "history_id": "550e8400-e29b-41d4-a716-446655440001",
  "natural_language_query": "Show top 10 customers by revenue",
  "generated_sql": "SELECT c.customer_id, c.first_name, c.last_name, SUM(oi.subtotal) AS total_revenue FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_items oi ON o.order_id = oi.order_id GROUP BY c.customer_id, c.first_name, c.last_name ORDER BY total_revenue DESC LIMIT 10;",
  "execution_status": "success",
  "execution_time_ms": 125,
  "row_count": 10,
  "results": {
    "columns": ["customer_id", "first_name", "last_name", "total_revenue"],
    "rows": [
      [1, "John", "Doe", 12500.50],
      [2, "Jane", "Smith", 11200.75]
    ]
  },
  "charts": [
    {
      "type": "bar",
      "title": "Top 10 Customers by Revenue",
      "x_axis": "last_name",
      "y_axis": "total_revenue",
      "data": [...]
    }
  ],
  "insights": [
    "John Doe is the top customer with $12,500.50 in revenue",
    "Top 5 customers contribute 45% of total revenue"
  ],
  "created_at": "2026-06-19T00:00:00Z"
}
```

### Error Cases
| Status | Error | Description |
|--------|-------|-------------|
| 400 | Bad Request | Missing required fields, invalid query |
| 401 | Unauthorized | Missing or invalid JWT token |
| 403 | Forbidden | User doesn't have access to this connection |
| 404 | Not Found | Connection doesn't exist |
| 422 | Unprocessable Entity | SQL validation failed |
| 500 | Internal Server Error | Query execution failed |

---

## 4. GET /history

### Purpose
Retrieve query history for the authenticated user.

### Request
- Method: GET
- Headers:
  - `Authorization: Bearer <jwt_token>`
- Query Parameters:
  - `connection_id` (string, optional): Filter by connection
  - `limit` (integer, optional, default 20): Number of results
  - `offset` (integer, optional, default 0): Pagination offset
  - `status` (string, optional): Filter by status (success, failed, pending)
  - `start_date` (string, optional): Filter by start date (ISO 8601)
  - `end_date` (string, optional): Filter by end date (ISO 8601)

### Response (200 OK)
```json
{
  "total": 150,
  "limit": 20,
  "offset": 0,
  "items": [
    {
      "history_id": "550e8400-e29b-41d4-a716-446655440001",
      "connection_id": "550e8400-e29b-41d4-a716-446655440000",
      "connection_name": "Production DB",
      "natural_language_query": "Show top 10 customers by revenue",
      "execution_status": "success",
      "execution_time_ms": 125,
      "row_count": 10,
      "created_at": "2026-06-19T00:00:00Z"
    }
  ]
}
```

### Error Cases
| Status | Error | Description |
|--------|-------|-------------|
| 401 | Unauthorized | Missing or invalid JWT token |
| 400 | Bad Request | Invalid query parameters |

---

## 5. GET /saved-queries

### Purpose
Retrieve saved queries for the authenticated user.

### Request
- Method: GET
- Headers:
  - `Authorization: Bearer <jwt_token>`
- Query Parameters:
  - `connection_id` (string, optional): Filter by connection
  - `tags` (string, optional): Comma-separated tags to filter
  - `search` (string, optional): Search query by name/description
  - `limit` (integer, optional, default 20): Number of results
  - `offset` (integer, optional, default 0): Pagination offset

### Response (200 OK)
```json
{
  "total": 25,
  "limit": 20,
  "offset": 0,
  "items": [
    {
      "saved_query_id": "550e8400-e29b-41d4-a716-446655440002",
      "connection_id": "550e8400-e29b-41d4-a716-446655440000",
      "connection_name": "Production DB",
      "query_name": "Top Customers by Revenue",
      "description": "Monthly top customers report",
      "natural_language_query": "Show top 10 customers by revenue",
      "generated_sql": "SELECT ...",
      "tags": ["customers", "revenue", "monthly"],
      "is_public": false,
      "created_at": "2026-06-19T00:00:00Z",
      "updated_at": "2026-06-19T00:00:00Z"
    }
  ]
}
```

### Error Cases
| Status | Error | Description |
|--------|-------|-------------|
| 401 | Unauthorized | Missing or invalid JWT token |
| 400 | Bad Request | Invalid query parameters |

---

## 6. POST /saved-queries

### Purpose
Save a query for future use.

### Request
- Method: POST
- Headers:
  - `Authorization: Bearer <jwt_token>`
  - `Content-Type: application/json`
- Body:
```json
{
  "connection_id": "550e8400-e29b-41d4-a716-446655440000",
  "query_name": "Top Customers by Revenue",
  "description": "Monthly top customers report",
  "natural_language_query": "Show top 10 customers by revenue",
  "generated_sql": "SELECT ...",
  "tags": ["customers", "revenue", "monthly"],
  "is_public": false
}
```

### Response (201 Created)
```json
{
  "saved_query_id": "550e8400-e29b-41d4-a716-446655440002",
  "connection_id": "550e8400-e29b-41d4-a716-446655440000",
  "query_name": "Top Customers by Revenue",
  "description": "Monthly top customers report",
  "natural_language_query": "Show top 10 customers by revenue",
  "generated_sql": "SELECT ...",
  "tags": ["customers", "revenue", "monthly"],
  "is_public": false,
  "created_at": "2026-06-19T00:00:00Z",
  "updated_at": "2026-06-19T00:00:00Z"
}
```

### Error Cases
| Status | Error | Description |
|--------|-------|-------------|
| 400 | Bad Request | Missing required fields |
| 401 | Unauthorized | Missing or invalid JWT token |
| 403 | Forbidden | User doesn't have access to this connection |
| 404 | Not Found | Connection doesn't exist |

---

## 7. GET /export

### Purpose
Export query results to various formats.

### Request
- Method: GET
- Headers:
  - `Authorization: Bearer <jwt_token>`
- Query Parameters:
  - `history_id` (string, required): History entry ID to export
  - `format` (string, required): Export format (csv, excel, json)

### Response (200 OK)
- Content-Type: Depends on format
- Content-Disposition: `attachment; filename="export_20260619.csv"`
- Body: Binary file content

### Error Cases
| Status | Error | Description |
|--------|-------|-------------|
| 400 | Bad Request | Missing or invalid parameters |
| 401 | Unauthorized | Missing or invalid JWT token |
| 403 | Forbidden | User doesn't have access to this history entry |
| 404 | Not Found | History entry doesn't exist |
| 500 | Internal Server Error | Export generation failed |
