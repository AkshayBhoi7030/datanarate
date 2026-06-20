# DataNarrate - Database Design

## Table: users

Stores user account information and authentication details.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| user_id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email address |
| password_hash | VARCHAR(255) | NOT NULL | Hashed user password |
| first_name | VARCHAR(100) | NOT NULL | User first name |
| last_name | VARCHAR(100) | NOT NULL | User last name |
| role | VARCHAR(50) | NOT NULL, DEFAULT 'user' | User role (admin, user, viewer) |
| is_active | BOOLEAN | NOT NULL, DEFAULT true | Account active status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Last update timestamp |
| last_login_at | TIMESTAMP | NULL | Last login timestamp |

---

## Table: database_connections

Stores encrypted database connection configurations.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| connection_id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique connection identifier |
| user_id | UUID | NOT NULL, FOREIGN KEY REFERENCES users(user_id) ON DELETE CASCADE | Associated user |
| connection_name | VARCHAR(100) | NOT NULL | User-friendly connection name |
| db_type | VARCHAR(50) | NOT NULL | Database type (postgresql, mysql, sqlserver, etc.) |
| host | VARCHAR(255) | NOT NULL | Database host |
| port | INTEGER | NOT NULL | Database port |
| database_name | VARCHAR(255) | NOT NULL | Database name |
| username | VARCHAR(255) | NOT NULL | Database username |
| password_encrypted | TEXT | NOT NULL | Encrypted database password |
| ssl_required | BOOLEAN | NOT NULL, DEFAULT false | SSL connection requirement |
| is_default | BOOLEAN | NOT NULL, DEFAULT false | Default connection flag |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Last update timestamp |
| last_connected_at | TIMESTAMP | NULL | Last successful connection timestamp |

---

## Table: query_history

Stores all executed queries and their results.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| history_id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique history entry identifier |
| user_id | UUID | NOT NULL, FOREIGN KEY REFERENCES users(user_id) ON DELETE CASCADE | User who executed the query |
| connection_id | UUID | NOT NULL, FOREIGN KEY REFERENCES database_connections(connection_id) ON DELETE CASCADE | Database connection used |
| natural_language_query | TEXT | NOT NULL | Original natural language query |
| generated_sql | TEXT | NOT NULL | Generated SQL query |
| execution_status | VARCHAR(50) | NOT NULL | Execution status (success, failed, pending) |
| execution_time_ms | INTEGER | NULL | Query execution time in milliseconds |
| row_count | INTEGER | NULL | Number of rows returned |
| error_message | TEXT | NULL | Error message if execution failed |
| results_summary | JSONB | NULL | Summary of results |
| insights | TEXT | NULL | Generated business insights |
| chart_config | JSONB | NULL | Chart visualization configuration |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Execution timestamp |

---

## Table: saved_queries

Stores user-saved queries for future use.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| saved_query_id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique saved query identifier |
| user_id | UUID | NOT NULL, FOREIGN KEY REFERENCES users(user_id) ON DELETE CASCADE | Owner of the saved query |
| connection_id | UUID | NOT NULL, FOREIGN KEY REFERENCES database_connections(connection_id) ON DELETE CASCADE | Associated database connection |
| query_name | VARCHAR(255) | NOT NULL | Name of the saved query |
| description | TEXT | NULL | Query description |
| natural_language_query | TEXT | NOT NULL | Original natural language query |
| generated_sql | TEXT | NOT NULL | Generated SQL query |
| tags | TEXT[] | NULL | Array of tags for categorization |
| is_public | BOOLEAN | NOT NULL, DEFAULT false | Public visibility flag |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Last update timestamp |

---

## Table: audit_logs

Stores audit trail of all system actions.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| log_id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique log identifier |
| user_id | UUID | NULL, FOREIGN KEY REFERENCES users(user_id) ON DELETE SET NULL | User associated with the action |
| action | VARCHAR(100) | NOT NULL | Action performed (login, query_execution, connection_create, etc.) |
| resource_type | VARCHAR(50) | NULL | Type of resource affected (user, connection, query, etc.) |
| resource_id | UUID | NULL | ID of the resource affected |
| action_details | JSONB | NULL | Additional details about the action |
| ip_address | VARCHAR(50) | NULL | IP address of the request |
| user_agent | TEXT | NULL | User agent string |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Action timestamp |

---

## Indexes

```sql
-- Users indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_is_active ON users(is_active);

-- Database connections indexes
CREATE INDEX idx_db_connections_user_id ON database_connections(user_id);
CREATE INDEX idx_db_connections_is_default ON database_connections(is_default);

-- Query history indexes
CREATE INDEX idx_query_history_user_id ON query_history(user_id);
CREATE INDEX idx_query_history_connection_id ON query_history(connection_id);
CREATE INDEX idx_query_history_created_at ON query_history(created_at DESC);
CREATE INDEX idx_query_history_status ON query_history(execution_status);

-- Saved queries indexes
CREATE INDEX idx_saved_queries_user_id ON saved_queries(user_id);
CREATE INDEX idx_saved_queries_connection_id ON saved_queries(connection_id);
CREATE INDEX idx_saved_queries_tags ON saved_queries USING GIN(tags);
CREATE INDEX idx_saved_queries_is_public ON saved_queries(is_public);

-- Audit logs indexes
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at DESC);
```
